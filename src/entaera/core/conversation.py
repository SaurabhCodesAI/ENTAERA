#!/usr/bin/env python3
"""
Day 3 Kata 3.2 - AI Conversation Data Structures
Comprehensive data structures for managing AI conversation history, context windows, and memory persistence.
"""

import json
import uuid
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Literal
from dataclasses import field

from pydantic import BaseModel, Field, field_validator, ConfigDict, model_serializer
from pydantic.dataclasses import dataclass

from ..utils.file_ops import FileManager, FileOperationError, FileValidationError


class MessageRole(str, Enum):
    """Enumeration of message roles in a conversation."""
    SYSTEM = "system"
    USER = "user" 
    ASSISTANT = "assistant"
    FUNCTION = "function"
    TOOL = "tool"


class MessageType(str, Enum):
    """Enumeration of message types."""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    DOCUMENT = "document"
    CODE = "code"
    FUNCTION_CALL = "function_call"
    FUNCTION_RESULT = "function_result"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"


class ConversationStatus(str, Enum):
    """Enumeration of conversation statuses."""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"
    ERROR = "error"


class MessageMetadata(BaseModel):
    """Metadata associated with a message."""
    model_config = ConfigDict(extra='allow')
    
    # Token usage information
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    
    # Model information
    model_name: Optional[str] = None
    model_version: Optional[str] = None
    
    # Processing information
    processing_time: Optional[float] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    
    # Source information
    source_system: Optional[str] = None
    source_ip: Optional[str] = None
    user_agent: Optional[str] = None
    
    # Custom metadata (extra fields allowed)
    tags: List[str] = Field(default_factory=list)
    attachments: List[str] = Field(default_factory=list)
    references: List[str] = Field(default_factory=list)


class Message(BaseModel):
    """A single message in a conversation."""
    model_config = ConfigDict(
        extra='forbid',
        str_strip_whitespace=True,
        validate_assignment=True
    )
    
    # Core message fields
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: MessageRole
    content: str = Field(min_length=1)
    message_type: MessageType = MessageType.TEXT
    
    # Temporal information
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    edited_at: Optional[datetime] = None
    
    # Hierarchical information
    parent_id: Optional[str] = None
    thread_id: Optional[str] = None
    
    # Metadata
    metadata: MessageMetadata = Field(default_factory=MessageMetadata)
    
    # Content processing
    raw_content: Optional[str] = None  # Original unprocessed content
    processed_content: Optional[str] = None  # Processed/cleaned content
    
    @field_validator('content')
    @classmethod
    def content_not_empty(cls, v):
        """Validate that content is not empty or just whitespace."""
        if not v or not v.strip():
            raise ValueError("Message content cannot be empty")
        return v
    
    @field_validator('timestamp', 'edited_at')
    @classmethod
    def ensure_timezone(cls, v):
        """Ensure timestamps have timezone information."""
        if v and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v
    
    def get_token_count(self) -> int:
        """Get the total token count for this message."""
        if self.metadata.total_tokens:
            return self.metadata.total_tokens
        # Rough estimate: 1 token ≈ 4 characters
        return len(self.content) // 4
    
    def is_edited(self) -> bool:
        """Check if the message has been edited."""
        return self.edited_at is not None
    
    def get_age_seconds(self) -> float:
        """Get the age of the message in seconds."""
        return (datetime.now(timezone.utc) - self.timestamp).total_seconds()


class ContextWindow(BaseModel):
    """Manages context window for AI conversations."""
    model_config = ConfigDict(extra='forbid')
    
    max_tokens: int = Field(default=4096, ge=1)
    current_tokens: int = Field(default=0, ge=0)
    reserve_tokens: int = Field(default=512, ge=0)  # Reserved for response
    
    # Window management strategy
    strategy: Literal["sliding", "truncate", "summarize"] = "sliding"
    
    # Message inclusion rules
    always_include_system: bool = True
    min_messages: int = Field(default=1, ge=1)
    max_messages: Optional[int] = None
    
    @field_validator('current_tokens')
    @classmethod
    def current_not_exceed_max(cls, v, info):
        """Validate current tokens don't exceed max."""
        if hasattr(info, 'data') and 'max_tokens' in info.data and v > info.data['max_tokens']:
            raise ValueError("Current tokens cannot exceed max tokens")
        return v
    
    @field_validator('reserve_tokens')
    @classmethod
    def reserve_reasonable(cls, v, info):
        """Validate reserve tokens are reasonable."""
        if hasattr(info, 'data') and 'max_tokens' in info.data and v >= info.data['max_tokens']:
            raise ValueError("Reserve tokens must be less than max tokens")
        return v
    
    def available_tokens(self) -> int:
        """Get available tokens for new content."""
        return max(0, self.max_tokens - self.current_tokens - self.reserve_tokens)
    
    def can_fit_message(self, message: Message) -> bool:
        """Check if a message can fit in the current context window."""
        return message.get_token_count() <= self.available_tokens()
    
    def utilization_percentage(self) -> float:
        """Get context window utilization as percentage."""
        return (self.current_tokens / self.max_tokens) * 100 if self.max_tokens > 0 else 0.0
    
    def needs_management(self) -> bool:
        """Check if context window needs management (approaching limit)."""
        return self.utilization_percentage() > 80.0


class ConversationSummary(BaseModel):
    """Summary of conversation content and metadata."""
    model_config = ConfigDict(extra='forbid')
    
    # Summary content
    summary: str = Field(min_length=1)
    key_points: List[str] = Field(default_factory=list)
    topics: List[str] = Field(default_factory=list)
    
    # Coverage information
    messages_summarized: int = Field(ge=0)
    time_range_start: datetime
    time_range_end: datetime
    total_tokens_summarized: int = Field(ge=0)
    
    # Summary metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    summary_model: Optional[str] = None
    compression_ratio: Optional[float] = None  # Original tokens / summary tokens
    
    @field_validator('time_range_end')
    @classmethod
    def end_after_start(cls, v, info):
        """Validate end time is after start time."""
        if hasattr(info, 'data') and 'time_range_start' in info.data and v < info.data['time_range_start']:
            raise ValueError("End time must be after start time")
        return v


class ConversationStats(BaseModel):
    """Statistics and metrics for a conversation."""
    model_config = ConfigDict(extra='forbid')
    
    # Message counts
    total_messages: int = Field(default=0, ge=0)
    user_messages: int = Field(default=0, ge=0)
    assistant_messages: int = Field(default=0, ge=0)
    system_messages: int = Field(default=0, ge=0)
    
    # Token usage
    total_tokens: int = Field(default=0, ge=0)
    prompt_tokens: int = Field(default=0, ge=0)
    completion_tokens: int = Field(default=0, ge=0)
    
    # Temporal information
    duration_seconds: float = Field(default=0.0, ge=0.0)
    first_message_at: Optional[datetime] = None
    last_message_at: Optional[datetime] = None
    
    # Interaction patterns
    average_response_time: Optional[float] = None
    total_edits: int = Field(default=0, ge=0)
    context_window_resets: int = Field(default=0, ge=0)
    
    def messages_per_minute(self) -> float:
        """Calculate messages per minute rate."""
        if self.duration_seconds > 0:
            return (self.total_messages / self.duration_seconds) * 60
        return 0.0
    
    def tokens_per_message(self) -> float:
        """Calculate average tokens per message."""
        return self.total_tokens / self.total_messages if self.total_messages > 0 else 0.0


class Conversation(BaseModel):
    """A complete conversation with messages and metadata."""
    model_config = ConfigDict(
        extra='forbid',
        str_strip_whitespace=True,
        validate_assignment=True
    )
    
    # Core conversation fields
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default="", max_length=1000)
    
    # Status and categorization
    status: ConversationStatus = ConversationStatus.ACTIVE
    tags: List[str] = Field(default_factory=list)
    category: Optional[str] = None
    
    # Temporal information
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    
    # Conversation content
    messages: List[Message] = Field(default_factory=list)
    context_window: ContextWindow = Field(default_factory=ContextWindow)
    
    # Memory and summarization
    summaries: List[ConversationSummary] = Field(default_factory=list)
    pinned_messages: List[str] = Field(default_factory=list)  # Message IDs
    
    # Metadata and statistics
    metadata: Dict[str, Any] = Field(default_factory=dict)
    stats: ConversationStats = Field(default_factory=ConversationStats)
    
    # Configuration
    auto_summarize: bool = True
    max_message_history: Optional[int] = None
    
    @field_validator('updated_at')
    @classmethod
    def updated_after_created(cls, v, info):
        """Validate updated_at is after created_at."""
        if hasattr(info, 'data') and 'created_at' in info.data and v < info.data['created_at']:
            return info.data['created_at']
        return v
    
    def add_message(self, message: Message) -> None:
        """Add a message to the conversation."""
        # Update timestamps
        message.timestamp = datetime.now(timezone.utc)
        self.updated_at = message.timestamp
        
        # Add to messages
        self.messages.append(message)
        
        # Update context window
        token_count = message.get_token_count()
        self.context_window.current_tokens += token_count
        
        # Update statistics
        self._update_stats()
        
        # Manage context window if needed
        if self.context_window.needs_management():
            self._manage_context_window()
    
    def get_message_by_id(self, message_id: str) -> Optional[Message]:
        """Get a message by its ID."""
        for message in self.messages:
            if message.id == message_id:
                return message
        return None
    
    def get_messages_by_role(self, role: MessageRole) -> List[Message]:
        """Get all messages from a specific role."""
        return [msg for msg in self.messages if msg.role == role]
    
    def get_recent_messages(self, count: int) -> List[Message]:
        """Get the most recent N messages."""
        return self.messages[-count:] if count > 0 else []
    
    def get_context_messages(self) -> List[Message]:
        """Get messages that fit in the current context window."""
        if not self.messages:
            return []
        
        context_messages = []
        current_tokens = 0
        max_available = self.context_window.max_tokens - self.context_window.reserve_tokens
        
        # Always include pinned messages first
        pinned_messages = [msg for msg in self.messages if msg.id in self.pinned_messages]
        for msg in pinned_messages:
            tokens = msg.get_token_count()
            if current_tokens + tokens <= max_available:
                context_messages.append(msg)
                current_tokens += tokens
        
        # Always include system messages if configured
        if self.context_window.always_include_system:
            system_messages = [msg for msg in self.messages 
                             if msg.role == MessageRole.SYSTEM and msg.id not in self.pinned_messages]
            for msg in system_messages:
                tokens = msg.get_token_count()
                if current_tokens + tokens <= max_available:
                    context_messages.append(msg)
                    current_tokens += tokens
        
        # Add messages from most recent backwards (excluding already included ones)
        included_ids = {msg.id for msg in context_messages}
        for message in reversed(self.messages):
            if message.id in included_ids:
                continue  # Already included
            
            tokens = message.get_token_count()
            if current_tokens + tokens <= max_available:
                context_messages.insert(-len([m for m in context_messages 
                                             if m.role == MessageRole.SYSTEM or m.id in self.pinned_messages]), 
                                      message)
                current_tokens += tokens
            else:
                break
        
        # Sort by timestamp to maintain order
        context_messages.sort(key=lambda m: m.timestamp)
        return context_messages
    
    def pin_message(self, message_id: str) -> bool:
        """Pin a message to always include it in context."""
        if message_id not in self.pinned_messages and self.get_message_by_id(message_id):
            self.pinned_messages.append(message_id)
            return True
        return False
    
    def unpin_message(self, message_id: str) -> bool:
        """Unpin a message."""
        if message_id in self.pinned_messages:
            self.pinned_messages.remove(message_id)
            return True
        return False
    
    def create_summary(self, start_index: int = 0, end_index: Optional[int] = None) -> ConversationSummary:
        """Create a summary of conversation messages."""
        end_index = end_index or len(self.messages)
        messages_to_summarize = self.messages[start_index:end_index]
        
        if not messages_to_summarize:
            raise ValueError("No messages to summarize")
        
        # Create basic summary (in a real implementation, this would use an AI model)
        summary_text = f"Conversation covering {len(messages_to_summarize)} messages"
        key_points = [f"Message from {msg.role.value}: {msg.content[:50]}..." for msg in messages_to_summarize[:3]]
        topics = []
        for msg in messages_to_summarize:
            if msg.metadata.tags:
                topics.extend(msg.metadata.tags)
        topics = list(set(topics))
        
        
        total_tokens = sum(msg.get_token_count() for msg in messages_to_summarize)
        
        summary = ConversationSummary(
            summary=summary_text,
            key_points=key_points,
            topics=topics,
            messages_summarized=len(messages_to_summarize),
            time_range_start=messages_to_summarize[0].timestamp,
            time_range_end=messages_to_summarize[-1].timestamp,
            total_tokens_summarized=total_tokens
        )
        
        self.summaries.append(summary)
        return summary
    
    def _update_stats(self) -> None:
        """Update conversation statistics."""
        if not self.messages:
            return
        
        # Count messages by role
        role_counts = {}
        for role in MessageRole:
            role_counts[role] = len(self.get_messages_by_role(role))
        
        # Calculate token usage
        total_tokens = sum(msg.get_token_count() for msg in self.messages)
        prompt_tokens = sum(msg.metadata.prompt_tokens or 0 for msg in self.messages)
        completion_tokens = sum(msg.metadata.completion_tokens or 0 for msg in self.messages)
        
        # Calculate duration
        first_msg = min(self.messages, key=lambda m: m.timestamp)
        last_msg = max(self.messages, key=lambda m: m.timestamp)
        duration = (last_msg.timestamp - first_msg.timestamp).total_seconds()
        
        # Calculate edits
        total_edits = sum(1 for msg in self.messages if msg.is_edited())
        
        # Update stats
        self.stats = ConversationStats(
            total_messages=len(self.messages),
            user_messages=role_counts.get(MessageRole.USER, 0),
            assistant_messages=role_counts.get(MessageRole.ASSISTANT, 0),
            system_messages=role_counts.get(MessageRole.SYSTEM, 0),
            total_tokens=total_tokens,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            duration_seconds=duration,
            first_message_at=first_msg.timestamp,
            last_message_at=last_msg.timestamp,
            total_edits=total_edits
        )
    
    def _manage_context_window(self) -> None:
        """Manage context window when it becomes too full."""
        if self.context_window.strategy == "sliding":
            self._sliding_window_management()
        elif self.context_window.strategy == "truncate":
            self._truncate_management()
        elif self.context_window.strategy == "summarize":
            self._summarize_management()
    
    def _sliding_window_management(self) -> None:
        """Remove oldest messages to maintain context window."""
        while (self.context_window.current_tokens > 
               self.context_window.max_tokens - self.context_window.reserve_tokens):
            if len(self.messages) <= self.context_window.min_messages:
                break
            
            # Don't remove pinned or system messages
            for i, msg in enumerate(self.messages):
                if (msg.id not in self.pinned_messages and 
                    msg.role != MessageRole.SYSTEM):
                    removed_msg = self.messages.pop(i)
                    self.context_window.current_tokens -= removed_msg.get_token_count()
                    break
            else:
                break  # No removable messages found
    
    def _truncate_management(self) -> None:
        """Truncate older messages when context window is full."""
        available_tokens = (self.context_window.max_tokens - 
                          self.context_window.reserve_tokens)
        
        # Keep most recent messages that fit
        current_tokens = 0
        keep_messages = []
        
        for message in reversed(self.messages):
            msg_tokens = message.get_token_count()
            if current_tokens + msg_tokens <= available_tokens:
                keep_messages.insert(0, message)
                current_tokens += msg_tokens
            elif message.role == MessageRole.SYSTEM or message.id in self.pinned_messages:
                # Always keep system and pinned messages
                keep_messages.insert(0, message)
                current_tokens += msg_tokens
        
        self.messages = keep_messages
        self.context_window.current_tokens = current_tokens
    
    def _summarize_management(self) -> None:
        """Create summaries of older messages to free up context space."""
        if len(self.messages) <= self.context_window.min_messages:
            return
        
        # Summarize the oldest half of messages
        split_point = len(self.messages) // 2
        summary = self.create_summary(0, split_point)
        
        # Remove summarized messages (except pinned ones)
        remaining_messages = []
        for i, msg in enumerate(self.messages):
            if i >= split_point or msg.id in self.pinned_messages or msg.role == MessageRole.SYSTEM:
                remaining_messages.append(msg)
        
        self.messages = remaining_messages
        self._recalculate_context_tokens()
        self.stats.context_window_resets += 1
    
    def _recalculate_context_tokens(self) -> None:
        """Recalculate context window token count."""
        self.context_window.current_tokens = sum(
            msg.get_token_count() for msg in self.messages
        )


@dataclass
class ConversationSearchResult:
    """Result from searching conversations."""
    conversation: Conversation
    relevance_score: float
    matching_messages: List[Message] = field(default_factory=list)
    match_summary: str = ""


class ConversationManager:
    """Manages multiple conversations with persistence and search capabilities."""
    
    def __init__(self, storage_path: Optional[Union[str, Path]] = None):
        """
        Initialize conversation manager.
        
        Args:
            storage_path: Directory to store conversation files
        """
        self.storage_path = Path(storage_path) if storage_path else Path("data/conversations")
        self.file_manager = FileManager(self.storage_path)
        self.conversations: Dict[str, Conversation] = {}
        
        # Ensure storage directory exists
        self.file_manager.ensure_directory(".")
        
        # Load existing conversations
        self._load_conversations()
    
    def create_conversation(self, title: str, description: str = "") -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(title=title, description=description)
        self.conversations[conversation.id] = conversation
        self._save_conversation(conversation)
        return conversation
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get a conversation by ID."""
        if conversation_id in self.conversations:
            return self.conversations[conversation_id]
        
        # Try to load from storage
        try:
            conversation_data = self.file_manager.read_json_file(f"{conversation_id}.json")
            conversation = Conversation(**conversation_data)
            self.conversations[conversation_id] = conversation
            return conversation
        except (FileOperationError, ValueError):
            return None
    
    def list_conversations(self, status: Optional[ConversationStatus] = None) -> List[Conversation]:
        """List all conversations, optionally filtered by status."""
        conversations = list(self.conversations.values())
        if status:
            conversations = [conv for conv in conversations if conv.status == status]
        return sorted(conversations, key=lambda c: c.updated_at, reverse=True)
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation."""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
        
        try:
            self.file_manager.delete_file(f"{conversation_id}.json")
            return True
        except FileOperationError:
            return False
    
    def search_conversations(self, query: str, limit: int = 10) -> List[ConversationSearchResult]:
        """Search conversations by content."""
        results = []
        query_lower = query.lower()
        
        for conversation in self.conversations.values():
            relevance_score = 0.0
            matching_messages = []
            
            # Search in title and description
            if query_lower in conversation.title.lower():
                relevance_score += 2.0
            if query_lower in conversation.description.lower():
                relevance_score += 1.0
            
            # Search in messages
            for message in conversation.messages:
                if query_lower in message.content.lower():
                    relevance_score += 0.5
                    matching_messages.append(message)
            
            # Search in tags
            for tag in conversation.tags:
                if query_lower in tag.lower():
                    relevance_score += 1.0
            
            if relevance_score > 0:
                result = ConversationSearchResult(
                    conversation=conversation,
                    relevance_score=relevance_score,
                    matching_messages=matching_messages,
                    match_summary=f"Found {len(matching_messages)} matching messages"
                )
                results.append(result)
        
        # Sort by relevance and limit results
        results.sort(key=lambda r: r.relevance_score, reverse=True)
        return results[:limit]
    
    def export_conversation(self, conversation_id: str, format_type: str = "json") -> Dict[str, Any]:
        """Export a conversation in specified format."""
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        if format_type == "json":
            return conversation.model_dump(mode='json')
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
    
    def import_conversation(self, data: Dict[str, Any]) -> Conversation:
        """Import a conversation from data."""
        conversation = Conversation(**data)
        self.conversations[conversation.id] = conversation
        self._save_conversation(conversation)
        return conversation
    
    def get_stats(self) -> Dict[str, Any]:
        """Get overall statistics across all conversations."""
        total_conversations = len(self.conversations)
        total_messages = sum(len(conv.messages) for conv in self.conversations.values())
        total_tokens = sum(conv.stats.total_tokens for conv in self.conversations.values())
        
        status_counts = {}
        for status in ConversationStatus:
            status_counts[status.value] = len([
                conv for conv in self.conversations.values() if conv.status == status
            ])
        
        return {
            "total_conversations": total_conversations,
            "total_messages": total_messages,
            "total_tokens": total_tokens,
            "status_distribution": status_counts,
            "storage_path": str(self.storage_path),
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
    
    def _load_conversations(self) -> None:
        """Load all conversations from storage."""
        try:
            conversation_files = self.file_manager.list_directory(".", pattern="*.json")
            for file_path in conversation_files:
                try:
                    conversation_data = self.file_manager.read_json_file(file_path.name)
                    conversation = Conversation(**conversation_data)
                    self.conversations[conversation.id] = conversation
                except (ValueError, TypeError) as e:
                    # Skip invalid conversation files
                    continue
        except FileOperationError:
            # Storage directory doesn't exist or is empty
            pass
    
    def _save_conversation(self, conversation: Conversation) -> None:
        """Save a conversation to storage."""
        filename = f"{conversation.id}.json"
        
        # Convert conversation to dict with proper datetime serialization
        conversation_data = conversation.model_dump(mode='json')
        
        self.file_manager.write_json_file(filename, conversation_data, indent=2)
    
    def save_all_conversations(self) -> None:
        """Save all conversations to storage."""
        for conversation in self.conversations.values():
            self._save_conversation(conversation)


# Validation function for conversation data
def validate_conversation_data(data: Dict[str, Any]) -> bool:
    """Validate conversation data structure."""
    try:
        Conversation(**data)
        return True
    except (ValueError, TypeError):
        return False
