"""
ENTAERA Context Injection System

Day 4 Kata 4.2: Smart Context Injection for AI Conversations

This module provides intelligent context injection capabilities that enhance
AI conversations by seamlessly incorporating relevant historical context
into new conversations, improving continuity and contextual awareness.

Features:
- Adaptive context injection based on conversation flow
- Context formatting and presentation optimization
- Dynamic context relevance scoring
- Context conflict resolution and deduplication
- Performance-optimized context integration
- User-configurable context preferences
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
import json

from .conversation import (
    Conversation, Message, MessageRole, MessageType, ConversationManager,
    MessageMetadata
)
from .context_retrieval import (
    ContextRetrievalEngine, ContextWindow, RetrievedContext, 
    ContextRetrievalRequest, ContextType, ContextPriority
)
from .conversation_memory import ConversationMemoryManager
from .logger import get_logger

logger = get_logger(__name__)


class InjectionStrategy(str, Enum):
    """Strategies for injecting context into conversations."""
    SYSTEM_MESSAGE = "system_message"
    CONTEXT_SUMMARY = "context_summary" 
    INLINE_REFERENCES = "inline_references"
    SIDEBAR_CONTEXT = "sidebar_context"
    IMPLICIT_AWARENESS = "implicit_awareness"


class InjectionTiming(str, Enum):
    """When to inject context into conversations."""
    CONVERSATION_START = "conversation_start"
    ON_TOPIC_CHANGE = "on_topic_change"
    ON_USER_REQUEST = "on_user_request"
    CONTINUOUS = "continuous"
    ADAPTIVE = "adaptive"


class ContextFormat(str, Enum):
    """Formats for presenting context."""
    BULLET_POINTS = "bullet_points"
    NARRATIVE = "narrative"
    STRUCTURED = "structured"
    MINIMAL = "minimal"
    DETAILED = "detailed"


class InjectionPreferences(BaseModel):
    """User preferences for context injection."""
    strategy: InjectionStrategy = InjectionStrategy.CONTEXT_SUMMARY
    timing: InjectionTiming = InjectionTiming.ADAPTIVE
    format: ContextFormat = ContextFormat.STRUCTURED
    max_context_length: int = 1000
    include_timestamps: bool = True
    include_source_info: bool = True
    show_relevance_scores: bool = False
    group_by_topic: bool = True
    auto_summarize: bool = True


class InjectedContext(BaseModel):
    """Represents context that has been injected into a conversation."""
    injection_id: str = Field(default_factory=lambda: str(uuid4()))
    conversation_id: str
    message_id: Optional[str] = None
    injected_content: str
    source_contexts: List[str]  # IDs of source RetrievedContext objects
    injection_strategy: InjectionStrategy
    injection_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_visible: bool = True
    tokens_added: int = 0


class ContextInjectionEngine:
    """Engine for intelligently injecting context into AI conversations."""
    
    def __init__(
        self,
        context_retrieval_engine: ContextRetrievalEngine,
        conversation_manager: ConversationManager,
        default_preferences: Optional[InjectionPreferences] = None
    ):
        self.context_retrieval = context_retrieval_engine
        self.conversation_manager = conversation_manager
        self.default_preferences = default_preferences or InjectionPreferences()
        
        # Internal state
        self._injection_history: Dict[str, List[InjectedContext]] = {}
        self._user_preferences: Dict[str, InjectionPreferences] = {}
        self._injection_stats = {
            "total_injections": 0,
            "successful_injections": 0,
            "average_context_length": 0,
            "user_feedback_positive": 0,
            "user_feedback_negative": 0
        }
        
        logger.info("Initialized ContextInjectionEngine")
    
    async def inject_context_for_message(
        self,
        conversation_id: str,
        message: str,
        user_id: Optional[str] = None,
        preferences: Optional[InjectionPreferences] = None
    ) -> Optional[InjectedContext]:
        """Inject relevant context for a specific message."""
        try:
            # Get user preferences
            user_prefs = preferences or self._get_user_preferences(user_id)
            
            # Determine if context injection is needed
            if not await self._should_inject_context(conversation_id, message, user_prefs):
                return None
            
            # Retrieve relevant context
            context_window = await self.context_retrieval.get_context_for_message(
                message=message,
                conversation_id=conversation_id
            )
            
            if not context_window.retrieved_contexts:
                logger.debug(f"No relevant context found for message in conversation {conversation_id}")
                return None
            
            # Format and inject context
            injected_context = await self._format_and_inject_context(
                conversation_id=conversation_id,
                context_window=context_window,
                preferences=user_prefs,
                trigger_message=message
            )
            
            if injected_context:
                # Track injection
                await self._track_injection(injected_context)
                self._injection_stats["total_injections"] += 1
                self._injection_stats["successful_injections"] += 1
                
                logger.info(f"Successfully injected context for conversation {conversation_id}")
            
            return injected_context
            
        except Exception as e:
            logger.error(f"Failed to inject context for message: {e}")
            return None
    
    async def inject_conversation_starter_context(
        self,
        conversation_id: str,
        initial_message: str,
        user_id: Optional[str] = None
    ) -> Optional[InjectedContext]:
        """Inject context when starting a new conversation."""
        try:
            user_prefs = self._get_user_preferences(user_id)
            
            if user_prefs.timing not in [InjectionTiming.CONVERSATION_START, InjectionTiming.ADAPTIVE]:
                return None
            
            # Get relevant context from previous conversations
            context_window = await self.context_retrieval.get_context_for_message(
                message=initial_message,
                conversation_id=None  # Search across all conversations
            )
            
            if not context_window.retrieved_contexts:
                return None
            
            # Create system message with context
            context_content = await self._format_starter_context(
                context_window.retrieved_contexts,
                user_prefs
            )
            
            # Add system message to conversation
            conversation = self.conversation_manager.get_conversation(conversation_id)
            if conversation:
                system_message = Message(
                    role=MessageRole.SYSTEM,
                    content=context_content,
                    message_type=MessageType.CONTEXT,
                    metadata=MessageMetadata(
                        tags=["context_injection", "conversation_starter"],
                        context_sources=[ctx.context_id for ctx in context_window.retrieved_contexts]
                    )
                )
                
                # Insert at the beginning of the conversation
                conversation.messages.insert(0, system_message)
                await self.conversation_manager.save_conversation(conversation)
            
            injected_context = InjectedContext(
                conversation_id=conversation_id,
                message_id=str(system_message.id),
                injected_content=context_content,
                source_contexts=[ctx.context_id for ctx in context_window.retrieved_contexts],
                injection_strategy=InjectionStrategy.SYSTEM_MESSAGE,
                tokens_added=len(context_content.split())
            )
            
            await self._track_injection(injected_context)
            logger.info(f"Injected starter context for conversation {conversation_id}")
            
            return injected_context
            
        except Exception as e:
            logger.error(f"Failed to inject starter context: {e}")
            return None
    
    async def _should_inject_context(
        self,
        conversation_id: str,
        message: str,
        preferences: InjectionPreferences
    ) -> bool:
        """Determine if context injection is appropriate."""
        # Check timing preferences
        if preferences.timing == InjectionTiming.ON_USER_REQUEST:
            # Only inject if explicitly requested
            return "context" in message.lower() or "history" in message.lower() or "previous" in message.lower()
        
        if preferences.timing == InjectionTiming.CONVERSATION_START:
            # Only for new conversations
            conversation = self.conversation_manager.get_conversation(conversation_id)
            return conversation and len(conversation.messages) <= 1
        
        # Check if we've recently injected context
        recent_injections = self._get_recent_injections(conversation_id, hours=1)
        if len(recent_injections) >= 3:  # Limit to 3 injections per hour
            return False
        
        # Adaptive logic
        if preferences.timing == InjectionTiming.ADAPTIVE:
            return await self._adaptive_injection_decision(conversation_id, message)
        
        return True
    
    async def _adaptive_injection_decision(
        self,
        conversation_id: str,
        message: str
    ) -> bool:
        """Make adaptive decision about whether to inject context."""
        # Factors to consider:
        # 1. Topic shift detection
        # 2. Question complexity
        # 3. Reference to past information
        # 4. Conversation length
        
        conversation = self.conversation_manager.get_conversation(conversation_id)
        if not conversation:
            return False
        
        # Check for topic shift
        if len(conversation.messages) > 2:
            topic_shift_score = await self._detect_topic_shift(conversation, message)
            if topic_shift_score > 0.7:
                return True
        
        # Check for references to past information
        past_references = ["before", "earlier", "previous", "last time", "remember", "recall"]
        if any(ref in message.lower() for ref in past_references):
            return True
        
        # Check question complexity
        question_words = ["how", "what", "why", "when", "where", "explain", "tell me about"]
        if any(qw in message.lower() for qw in question_words) and len(message.split()) > 5:
            return True
        
        # For new conversations or after long pauses
        if len(conversation.messages) == 1:
            return True
        
        last_message_time = conversation.messages[-2].timestamp if len(conversation.messages) > 1 else None
        if last_message_time:
            time_gap = (datetime.now(timezone.utc) - last_message_time).total_seconds() / 3600
            if time_gap > 2:  # More than 2 hours gap
                return True
        
        return False
    
    async def _format_and_inject_context(
        self,
        conversation_id: str,
        context_window: ContextWindow,
        preferences: InjectionPreferences,
        trigger_message: str
    ) -> Optional[InjectedContext]:
        """Format context and inject it into the conversation."""
        try:
            # Format context based on preferences
            formatted_content = await self._format_context_content(
                context_window.retrieved_contexts,
                preferences
            )
            
            if not formatted_content.strip():
                return None
            
            # Choose injection strategy
            if preferences.strategy == InjectionStrategy.SYSTEM_MESSAGE:
                injected_context = await self._inject_as_system_message(
                    conversation_id, formatted_content, context_window.retrieved_contexts
                )
            elif preferences.strategy == InjectionStrategy.CONTEXT_SUMMARY:
                injected_context = await self._inject_as_context_summary(
                    conversation_id, formatted_content, context_window.retrieved_contexts
                )
            else:
                # Default to context summary
                injected_context = await self._inject_as_context_summary(
                    conversation_id, formatted_content, context_window.retrieved_contexts
                )
            
            return injected_context
            
        except Exception as e:
            logger.error(f"Failed to format and inject context: {e}")
            return None
    
    async def _format_context_content(
        self,
        contexts: List[RetrievedContext],
        preferences: InjectionPreferences
    ) -> str:
        """Format context content according to user preferences."""
        if not contexts:
            return ""
        
        # Sort contexts by relevance and priority
        sorted_contexts = sorted(
            contexts,
            key=lambda x: (x.priority.value, -x.relevance_score)
        )
        
        # Group by topic if requested
        if preferences.group_by_topic:
            grouped_contexts = self._group_contexts_by_topic(sorted_contexts)
        else:
            grouped_contexts = {"General": sorted_contexts}
        
        # Format based on style preference
        if preferences.format == ContextFormat.BULLET_POINTS:
            formatted = await self._format_as_bullet_points(grouped_contexts, preferences)
        elif preferences.format == ContextFormat.NARRATIVE:
            formatted = await self._format_as_narrative(grouped_contexts, preferences)
        elif preferences.format == ContextFormat.STRUCTURED:
            formatted = await self._format_as_structured(grouped_contexts, preferences)
        elif preferences.format == ContextFormat.MINIMAL:
            formatted = await self._format_as_minimal(grouped_contexts, preferences)
        else:  # DETAILED
            formatted = await self._format_as_detailed(grouped_contexts, preferences)
        
        # Apply length constraints
        if len(formatted) > preferences.max_context_length:
            formatted = formatted[:preferences.max_context_length] + "..."
        
        return formatted
    
    async def _format_as_structured(
        self,
        grouped_contexts: Dict[str, List[RetrievedContext]],
        preferences: InjectionPreferences
    ) -> str:
        """Format context in a structured format."""
        parts = ["📋 **Relevant Context:**\n"]
        
        for topic, contexts in grouped_contexts.items():
            if len(grouped_contexts) > 1:
                parts.append(f"\n**{topic}:**")
            
            for i, context in enumerate(contexts[:3], 1):  # Limit to top 3 per topic
                relevance_info = f" (relevance: {context.relevance_score:.2f})" if preferences.show_relevance_scores else ""
                timestamp_info = f" • {context.temporal_distance_hours:.1f}h ago" if preferences.include_timestamps else ""
                source_info = f" • From: {context.source_conversation_id[:8]}..." if preferences.include_source_info else ""
                
                content_preview = context.content[:100] + "..." if len(context.content) > 100 else context.content
                
                parts.append(f"\n{i}. {content_preview}{relevance_info}{timestamp_info}{source_info}")
        
        return "".join(parts)
    
    async def _format_as_bullet_points(
        self,
        grouped_contexts: Dict[str, List[RetrievedContext]],
        preferences: InjectionPreferences
    ) -> str:
        """Format context as bullet points."""
        parts = ["• **Related Information:**\n"]
        
        for topic, contexts in grouped_contexts.items():
            for context in contexts[:5]:  # Limit to top 5
                content_preview = context.content[:80] + "..." if len(context.content) > 80 else context.content
                parts.append(f"  • {content_preview}")
                
                if preferences.include_timestamps:
                    parts.append(f" ({context.temporal_distance_hours:.1f}h ago)")
                parts.append("\n")
        
        return "".join(parts)
    
    async def _format_as_narrative(
        self,
        grouped_contexts: Dict[str, List[RetrievedContext]],
        preferences: InjectionPreferences
    ) -> str:
        """Format context as a narrative."""
        if not grouped_contexts:
            return ""
        
        # Create a flowing narrative from the contexts
        all_contexts = []
        for contexts in grouped_contexts.values():
            all_contexts.extend(contexts)
        
        # Sort by temporal order
        all_contexts.sort(key=lambda x: x.temporal_distance_hours)
        
        narrative_parts = ["Based on our previous conversations: "]
        
        for i, context in enumerate(all_contexts[:3]):
            if i > 0:
                narrative_parts.append(", and ")
            
            time_ref = "recently" if context.temporal_distance_hours < 6 else "earlier"
            content_summary = context.content[:60] + "..." if len(context.content) > 60 else context.content
            narrative_parts.append(f"{time_ref} we discussed {content_summary}")
        
        narrative_parts.append(".")
        return "".join(narrative_parts)
    
    async def _format_as_minimal(
        self,
        grouped_contexts: Dict[str, List[RetrievedContext]],
        preferences: InjectionPreferences
    ) -> str:
        """Format context minimally."""
        if not grouped_contexts:
            return ""
        
        # Just show the most relevant context
        all_contexts = []
        for contexts in grouped_contexts.values():
            all_contexts.extend(contexts)
        
        if not all_contexts:
            return ""
        
        best_context = max(all_contexts, key=lambda x: x.relevance_score)
        preview = best_context.content[:50] + "..." if len(best_context.content) > 50 else best_context.content
        
        return f"💡 Related: {preview}"
    
    async def _format_as_detailed(
        self,
        grouped_contexts: Dict[str, List[RetrievedContext]],
        preferences: InjectionPreferences
    ) -> str:
        """Format context with full details."""
        parts = ["📚 **Detailed Context Information:**\n"]
        
        for topic, contexts in grouped_contexts.items():
            if len(grouped_contexts) > 1:
                parts.append(f"\n### {topic}\n")
            
            for i, context in enumerate(contexts, 1):
                parts.append(f"\n**Context {i}:**")
                parts.append(f"\n- Content: {context.content}")
                parts.append(f"\n- Relevance: {context.relevance_score:.3f}")
                parts.append(f"\n- Time: {context.temporal_distance_hours:.1f} hours ago")
                parts.append(f"\n- Source: {context.source_conversation_id}")
                parts.append(f"\n- Type: {context.context_type.value}")
                parts.append(f"\n- Priority: {context.priority.value}")
                parts.append(f"\n- Reason: {context.retrieval_reason}\n")
        
        return "".join(parts)
    
    def _group_contexts_by_topic(
        self,
        contexts: List[RetrievedContext]
    ) -> Dict[str, List[RetrievedContext]]:
        """Group contexts by topic/type."""
        groups = {}
        
        for context in contexts:
            # Use context type as grouping key
            group_key = context.context_type.value.replace("_", " ").title()
            
            if group_key not in groups:
                groups[group_key] = []
            groups[group_key].append(context)
        
        return groups
    
    async def _inject_as_system_message(
        self,
        conversation_id: str,
        content: str,
        source_contexts: List[RetrievedContext]
    ) -> Optional[InjectedContext]:
        """Inject context as a system message."""
        try:
            conversation = self.conversation_manager.get_conversation(conversation_id)
            if not conversation:
                return None
            
            system_message = Message(
                role=MessageRole.SYSTEM,
                content=content,
                message_type=MessageType.CONTEXT,
                metadata=MessageMetadata(
                    tags=["context_injection", "system_context"],
                    context_sources=[ctx.context_id for ctx in source_contexts]
                )
            )
            
            # Add to conversation
            conversation.messages.append(system_message)
            await self.conversation_manager.save_conversation(conversation)
            
            injected_context = InjectedContext(
                conversation_id=conversation_id,
                message_id=str(system_message.id),
                injected_content=content,
                source_contexts=[ctx.context_id for ctx in source_contexts],
                injection_strategy=InjectionStrategy.SYSTEM_MESSAGE,
                tokens_added=len(content.split())
            )
            
            return injected_context
            
        except Exception as e:
            logger.error(f"Failed to inject as system message: {e}")
            return None
    
    async def _inject_as_context_summary(
        self,
        conversation_id: str,
        content: str,
        source_contexts: List[RetrievedContext]
    ) -> InjectedContext:
        """Inject context as a context summary (non-message injection)."""
        injected_context = InjectedContext(
            conversation_id=conversation_id,
            injected_content=content,
            source_contexts=[ctx.context_id for ctx in source_contexts],
            injection_strategy=InjectionStrategy.CONTEXT_SUMMARY,
            user_visible=True,
            tokens_added=len(content.split())
        )
        
        return injected_context
    
    async def _format_starter_context(
        self,
        contexts: List[RetrievedContext],
        preferences: InjectionPreferences
    ) -> str:
        """Format context for conversation starters."""
        if not contexts:
            return ""
        
        # Create a welcoming system message with context
        parts = [
            "I have access to our previous conversations and relevant context. ",
            "Here's what might be helpful for our discussion:\n\n"
        ]
        
        # Add top relevant contexts
        for i, context in enumerate(contexts[:3], 1):
            content_preview = context.content[:100] + "..." if len(context.content) > 100 else context.content
            time_ref = f"{context.temporal_distance_hours:.1f} hours ago" if preferences.include_timestamps else "recently"
            
            parts.append(f"{i}. From {time_ref}: {content_preview}\n")
        
        if len(contexts) > 3:
            parts.append(f"\n(And {len(contexts) - 3} more related items available)")
        
        return "".join(parts)
    
    async def _detect_topic_shift(self, conversation: Conversation, new_message: str) -> float:
        """Detect if there's a topic shift in the conversation."""
        if len(conversation.messages) < 2:
            return 0.0
        
        # Simple topic shift detection based on word overlap
        recent_messages = conversation.messages[-3:]  # Last 3 messages
        recent_content = " ".join([msg.content for msg in recent_messages])
        
        # Get word sets
        recent_words = set(recent_content.lower().split())
        new_words = set(new_message.lower().split())
        
        # Calculate overlap
        if not recent_words:
            return 1.0
        
        overlap = len(recent_words.intersection(new_words))
        overlap_ratio = overlap / len(recent_words)
        
        # Topic shift score is inverse of overlap
        topic_shift_score = 1.0 - overlap_ratio
        
        return min(1.0, topic_shift_score)
    
    def _get_user_preferences(self, user_id: Optional[str]) -> InjectionPreferences:
        """Get user preferences for context injection."""
        if user_id and user_id in self._user_preferences:
            return self._user_preferences[user_id]
        return self.default_preferences
    
    def set_user_preferences(self, user_id: str, preferences: InjectionPreferences) -> None:
        """Set user preferences for context injection."""
        self._user_preferences[user_id] = preferences
        logger.info(f"Updated context injection preferences for user {user_id}")
    
    async def _track_injection(self, injected_context: InjectedContext) -> None:
        """Track an injection for analytics and history."""
        conv_id = injected_context.conversation_id
        
        if conv_id not in self._injection_history:
            self._injection_history[conv_id] = []
        
        self._injection_history[conv_id].append(injected_context)
        
        # Update stats
        self._injection_stats["average_context_length"] = (
            (self._injection_stats["average_context_length"] * 
             self._injection_stats["total_injections"] + 
             injected_context.tokens_added) / 
            (self._injection_stats["total_injections"] + 1)
        )
    
    def _get_recent_injections(
        self, 
        conversation_id: str, 
        hours: int = 1
    ) -> List[InjectedContext]:
        """Get recent injections for a conversation."""
        if conversation_id not in self._injection_history:
            return []
        
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        return [
            injection for injection in self._injection_history[conversation_id]
            if injection.injection_timestamp >= cutoff_time
        ]
    
    def get_injection_history(self, conversation_id: str) -> List[InjectedContext]:
        """Get injection history for a conversation."""
        return self._injection_history.get(conversation_id, [])
    
    def get_injection_stats(self) -> Dict[str, Any]:
        """Get injection engine statistics."""
        return {
            **self._injection_stats,
            "conversations_with_injections": len(self._injection_history),
            "total_injection_history": sum(len(hist) for hist in self._injection_history.values())
        }