"""
ENTAERA Conversation Memory System

Day 4 Kata 4.2: Intelligent Context Retrieval and Conversation Memory Integration

This module provides intelligent conversation memory capabilities that leverage
semantic search to find relevant historical context, enabling AI conversations
to maintain coherent context across sessions and topics.

Features:
- Semantic conversation memory with vector-based retrieval
- Context-aware conversation history search
- Intelligent topic threading and conversation linking
- Historical context injection for new conversations
- Multi-conversation context synthesis
- Memory-based conversation recommendations
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from uuid import UUID, uuid4
from pathlib import Path

from pydantic import BaseModel, Field
import numpy as np

from .conversation import (
    Conversation, Message, MessageRole, MessageType, ConversationManager,
    ConversationStatus
)
from .semantic_search import (
    SemanticSearchEngine, SearchResult, SearchFilter, SearchResultType,
    SentenceTransformerProvider, VectorEmbedding
)
from .logger import get_logger

logger = get_logger(__name__)


class MemoryRelevanceScore(BaseModel):
    """Represents the relevance of a memory to current context."""
    conversation_id: str
    message_id: str
    semantic_similarity: float
    temporal_relevance: float
    topic_coherence: float
    combined_score: float
    reason: str


class ConversationContext(BaseModel):
    """Context information for a conversation."""
    conversation_id: str
    primary_topics: List[str] = Field(default_factory=list)
    key_concepts: List[str] = Field(default_factory=list)
    participant_roles: List[str] = Field(default_factory=list)
    conversation_type: str = "general"
    urgency_level: str = "normal"  # low, normal, high, critical
    context_depth: int = 5  # Number of relevant messages to retrieve
    

class MemoryQuery(BaseModel):
    """Query for retrieving relevant conversation memory."""
    current_message: str
    conversation_context: Optional[ConversationContext] = None
    time_window_days: int = 30
    max_memories: int = 10
    min_relevance_score: float = 0.3
    include_system_messages: bool = False
    topic_keywords: List[str] = Field(default_factory=list)


class ConversationMemory(BaseModel):
    """Represents a relevant memory from past conversations."""
    conversation_id: str
    conversation_title: str
    message_id: str
    message_content: str
    message_role: MessageRole
    message_timestamp: datetime
    relevance_score: MemoryRelevanceScore
    context_snippet: str = ""  # Surrounding context from conversation
    

class ContextSummary(BaseModel):
    """Summary of retrieved context for a conversation."""
    query: str
    total_memories_found: int
    relevant_conversations: List[str]
    key_themes: List[str]
    recommended_context: List[ConversationMemory]
    context_confidence: float
    retrieval_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ConversationMemoryManager:
    """Manages conversation memory and context retrieval."""
    
    def __init__(
        self,
        conversation_manager: ConversationManager,
        semantic_engine: SemanticSearchEngine,
        memory_cache_dir: Optional[Path] = None
    ):
        self.conversation_manager = conversation_manager
        self.semantic_engine = semantic_engine
        self.memory_cache_dir = memory_cache_dir or Path.home() / ".entaera" / "memory_cache"
        self.memory_cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Internal state
        self._indexed_conversations: Set[str] = set()
        self._topic_embeddings: Dict[str, np.ndarray] = {}
        
        logger.info("Initialized ConversationMemoryManager")
    
    async def index_conversation(self, conversation: Conversation) -> None:
        """Index a conversation for semantic memory retrieval."""
        if conversation.id in self._indexed_conversations:
            logger.debug(f"Conversation {conversation.id} already indexed")
            return
        
        try:
            # Add all messages to semantic search index
            embeddings = await self.semantic_engine.add_conversation(conversation)
            
            # Extract and cache topic embeddings for this conversation
            await self._extract_conversation_topics(conversation, embeddings)
            
            self._indexed_conversations.add(conversation.id)
            logger.info(f"Indexed conversation '{conversation.title}' with {len(embeddings)} message embeddings")
            
        except Exception as e:
            logger.error(f"Failed to index conversation {conversation.id}: {e}")
            raise
    
    async def index_all_conversations(self) -> None:
        """Index all conversations in the conversation manager."""
        logger.info("Starting full conversation indexing for memory system")
        
        indexed_count = 0
        for conversation in self.conversation_manager.conversations.values():
            if conversation.id not in self._indexed_conversations:
                await self.index_conversation(conversation)
                indexed_count += 1
        
        logger.info(f"Indexed {indexed_count} new conversations. Total indexed: {len(self._indexed_conversations)}")
    
    async def retrieve_relevant_memories(
        self, 
        query: MemoryQuery
    ) -> List[ConversationMemory]:
        """Retrieve relevant memories based on semantic similarity and other factors."""
        # Ensure all conversations are indexed
        await self.index_all_conversations()
        
        # Perform semantic search
        search_filter = SearchFilter(
            max_results=query.max_memories * 3,  # Get more to allow for filtering
            min_similarity=query.min_relevance_score / 2  # Lower threshold for initial search
        )
        
        search_results = await self.semantic_engine.search(
            query.current_message,
            filters=search_filter
        )
        
        # Convert search results to memory objects with enhanced scoring
        memories = []
        for result in search_results:
            memory = await self._create_memory_from_search_result(result, query)
            if memory and memory.relevance_score.combined_score >= query.min_relevance_score:
                memories.append(memory)
        
        # Sort by combined relevance score and limit results
        memories.sort(key=lambda m: m.relevance_score.combined_score, reverse=True)
        
        logger.info(f"Retrieved {len(memories)} relevant memories for query: {query.current_message[:50]}...")
        return memories[:query.max_memories]
    
    async def get_conversation_context(
        self, 
        conversation_id: str,
        message_content: str,
        context_depth: int = 5
    ) -> ContextSummary:
        """Get relevant context for a specific conversation."""
        conversation = self.conversation_manager.get_conversation(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        # Create memory query
        query = MemoryQuery(
            current_message=message_content,
            conversation_context=ConversationContext(
                conversation_id=conversation_id,
                context_depth=context_depth
            ),
            max_memories=context_depth * 2
        )
        
        # Retrieve relevant memories
        memories = await self.retrieve_relevant_memories(query)
        
        # Analyze and summarize context
        relevant_conversations = list(set(m.conversation_id for m in memories))
        key_themes = await self._extract_key_themes_from_memories(memories)
        
        context_confidence = self._calculate_context_confidence(memories, query)
        
        summary = ContextSummary(
            query=message_content,
            total_memories_found=len(memories),
            relevant_conversations=relevant_conversations,
            key_themes=key_themes,
            recommended_context=memories[:context_depth],
            context_confidence=context_confidence
        )
        
        logger.info(f"Generated context summary for conversation {conversation_id}: {context_confidence:.2f} confidence")
        return summary
    
    async def suggest_conversation_topics(
        self, 
        current_message: str,
        max_suggestions: int = 5
    ) -> List[Tuple[str, float]]:
        """Suggest related topics based on conversation history."""
        # Get memories related to current message
        query = MemoryQuery(
            current_message=current_message,
            max_memories=20,
            min_relevance_score=0.2
        )
        
        memories = await self.retrieve_relevant_memories(query)
        
        # Extract topics from retrieved memories
        topic_scores: Dict[str, List[float]] = {}
        
        for memory in memories:
            # Extract potential topics from message content
            topics = await self._extract_topics_from_text(memory.message_content)
            
            for topic in topics:
                if topic not in topic_scores:
                    topic_scores[topic] = []
                topic_scores[topic].append(memory.relevance_score.combined_score)
        
        # Calculate average scores and sort
        suggested_topics = []
        for topic, scores in topic_scores.items():
            avg_score = sum(scores) / len(scores)
            suggested_topics.append((topic, avg_score))
        
        suggested_topics.sort(key=lambda x: x[1], reverse=True)
        
        logger.info(f"Generated {len(suggested_topics)} topic suggestions for: {current_message[:50]}...")
        return suggested_topics[:max_suggestions]
    
    async def find_related_conversations(
        self, 
        conversation_id: str,
        similarity_threshold: float = 0.4
    ) -> List[Tuple[str, float]]:
        """Find conversations related to the given conversation."""
        target_conversation = self.conversation_manager.get_conversation(conversation_id)
        if not target_conversation:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        # Get a representative text from the target conversation
        representative_text = self._get_conversation_representative_text(target_conversation)
        
        # Search for similar content
        search_filter = SearchFilter(
            max_results=50,
            min_similarity=similarity_threshold
        )
        
        results = await self.semantic_engine.search(representative_text, filters=search_filter)
        
        # Group by conversation and calculate conversation-level similarity
        conversation_similarities: Dict[str, List[float]] = {}
        
        for result in results:
            # Extract conversation ID from result metadata
            result_conv_id = result.metadata.get("conversation_id")
            if result_conv_id and result_conv_id != conversation_id:
                if result_conv_id not in conversation_similarities:
                    conversation_similarities[result_conv_id] = []
                conversation_similarities[result_conv_id].append(result.similarity_score)
        
        # Calculate average similarity per conversation
        related_conversations = []
        for conv_id, similarities in conversation_similarities.items():
            avg_similarity = sum(similarities) / len(similarities)
            related_conversations.append((conv_id, avg_similarity))
        
        related_conversations.sort(key=lambda x: x[1], reverse=True)
        
        logger.info(f"Found {len(related_conversations)} related conversations for {conversation_id}")
        return related_conversations
    
    async def _create_memory_from_search_result(
        self, 
        result: SearchResult, 
        query: MemoryQuery
    ) -> Optional[ConversationMemory]:
        """Create a ConversationMemory from a search result."""
        try:
            # Find the source message and conversation
            message_id = result.source_id
            if not message_id:
                return None
            
            # Find the conversation containing this message
            source_conversation = None
            source_message = None
            
            for conversation in self.conversation_manager.conversations.values():
                for message in conversation.messages:
                    if str(message.id) == message_id:
                        source_conversation = conversation
                        source_message = message
                        break
                if source_conversation:
                    break
            
            if not source_conversation or not source_message:
                logger.warning(f"Could not find source message {message_id}")
                return None
            
            # Calculate enhanced relevance scores
            relevance_score = await self._calculate_memory_relevance(
                result, source_message, source_conversation, query
            )
            
            # Get context snippet (surrounding messages)
            context_snippet = self._get_message_context_snippet(
                source_conversation, source_message
            )
            
            memory = ConversationMemory(
                conversation_id=source_conversation.id,
                conversation_title=source_conversation.title,
                message_id=str(source_message.id),
                message_content=source_message.content,
                message_role=source_message.role,
                message_timestamp=source_message.timestamp,
                relevance_score=relevance_score,
                context_snippet=context_snippet
            )
            
            return memory
            
        except Exception as e:
            logger.error(f"Failed to create memory from search result: {e}")
            return None
    
    async def _calculate_memory_relevance(
        self,
        search_result: SearchResult,
        message: Message,
        conversation: Conversation,
        query: MemoryQuery
    ) -> MemoryRelevanceScore:
        """Calculate comprehensive relevance score for a memory."""
        # Semantic similarity (from search result)
        semantic_similarity = search_result.similarity_score
        
        # Temporal relevance (recency factor)
        time_diff = datetime.now(timezone.utc) - message.timestamp
        days_old = time_diff.days
        temporal_relevance = max(0, 1 - (days_old / query.time_window_days))
        
        # Topic coherence (keyword matching)
        topic_coherence = 0.0
        if query.topic_keywords:
            message_text = message.content.lower()
            matches = sum(1 for keyword in query.topic_keywords if keyword.lower() in message_text)
            topic_coherence = matches / len(query.topic_keywords)
        else:
            topic_coherence = 0.5  # Neutral score if no keywords provided
        
        # Combine scores with weights
        combined_score = (
            0.5 * semantic_similarity +
            0.2 * temporal_relevance +
            0.3 * topic_coherence
        )
        
        # Generate reason
        reason_parts = []
        if semantic_similarity > 0.7:
            reason_parts.append("high semantic similarity")
        if temporal_relevance > 0.8:
            reason_parts.append("very recent")
        elif temporal_relevance > 0.5:
            reason_parts.append("moderately recent")
        if topic_coherence > 0.5:
            reason_parts.append("topically relevant")
        
        reason = ", ".join(reason_parts) if reason_parts else "general relevance"
        
        return MemoryRelevanceScore(
            conversation_id=conversation.id,
            message_id=str(message.id),
            semantic_similarity=semantic_similarity,
            temporal_relevance=temporal_relevance,
            topic_coherence=topic_coherence,
            combined_score=combined_score,
            reason=reason
        )
    
    def _get_message_context_snippet(
        self, 
        conversation: Conversation, 
        target_message: Message, 
        context_window: int = 2
    ) -> str:
        """Get surrounding context for a message."""
        try:
            # Find the message index
            message_index = None
            for i, msg in enumerate(conversation.messages):
                if msg.id == target_message.id:
                    message_index = i
                    break
            
            if message_index is None:
                return ""
            
            # Get surrounding messages
            start_idx = max(0, message_index - context_window)
            end_idx = min(len(conversation.messages), message_index + context_window + 1)
            
            context_messages = conversation.messages[start_idx:end_idx]
            context_parts = []
            
            for msg in context_messages:
                role_prefix = f"[{msg.role.value}]"
                content_preview = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
                if msg.id == target_message.id:
                    context_parts.append(f">>> {role_prefix} {content_preview}")
                else:
                    context_parts.append(f"{role_prefix} {content_preview}")
            
            return "\n".join(context_parts)
            
        except Exception as e:
            logger.error(f"Failed to get message context snippet: {e}")
            return ""
    
    async def _extract_conversation_topics(
        self, 
        conversation: Conversation, 
        embeddings: List[VectorEmbedding]
    ) -> None:
        """Extract and cache topic embeddings for a conversation."""
        try:
            # Combine all message content from the conversation
            combined_content = " ".join([msg.content for msg in conversation.messages if msg.content.strip()])
            
            # Extract key topics using simple keyword extraction
            topics = await self._extract_topics_from_text(combined_content)
            
            # Create topic embeddings
            for topic in topics:
                if topic not in self._topic_embeddings:
                    topic_vector = await self.semantic_engine.provider.generate_embedding(topic)
                    self._topic_embeddings[topic] = np.array(topic_vector)
            
            logger.debug(f"Extracted {len(topics)} topics from conversation {conversation.id}")
            
        except Exception as e:
            logger.error(f"Failed to extract conversation topics: {e}")
    
    async def _extract_topics_from_text(self, text: str) -> List[str]:
        """Extract key topics/concepts from text."""
        # Simple topic extraction - can be enhanced with NLP libraries
        words = text.lower().split()
        
        # Filter for meaningful words (simple approach)
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        meaningful_words = [word for word in words if len(word) > 3 and word not in stop_words]
        
        # Count word frequencies
        word_counts = {}
        for word in meaningful_words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        # Return top words as topics
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        topics = [word for word, count in sorted_words[:10] if count > 1]
        
        return topics
    
    async def _extract_key_themes_from_memories(self, memories: List[ConversationMemory]) -> List[str]:
        """Extract key themes from a list of memories."""
        all_content = " ".join([memory.message_content for memory in memories])
        return await self._extract_topics_from_text(all_content)
    
    def _calculate_context_confidence(self, memories: List[ConversationMemory], query: MemoryQuery) -> float:
        """Calculate confidence in the retrieved context."""
        if not memories:
            return 0.0
        
        # Factors affecting confidence:
        # 1. Average relevance score
        avg_relevance = sum(m.relevance_score.combined_score for m in memories) / len(memories)
        
        # 2. Number of memories found vs requested
        coverage_ratio = min(1.0, len(memories) / query.max_memories)
        
        # 3. Diversity of sources (different conversations)
        unique_conversations = len(set(m.conversation_id for m in memories))
        diversity_factor = min(1.0, unique_conversations / max(1, len(memories) // 2))
        
        # Combine factors
        confidence = (0.5 * avg_relevance + 0.3 * coverage_ratio + 0.2 * diversity_factor)
        
        return min(1.0, confidence)
    
    def _get_conversation_representative_text(self, conversation: Conversation) -> str:
        """Get representative text for a conversation."""
        # Combine title and first few user messages
        parts = [conversation.title]
        
        user_messages = [msg for msg in conversation.messages if msg.role == MessageRole.USER][:3]
        for msg in user_messages:
            content_preview = msg.content[:200] + "..." if len(msg.content) > 200 else msg.content
            parts.append(content_preview)
        
        return " ".join(parts)
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory system statistics."""
        return {
            "indexed_conversations": len(self._indexed_conversations),
            "cached_topics": len(self._topic_embeddings),
            "total_conversations": len(self.conversation_manager.conversations),
            "indexing_coverage": len(self._indexed_conversations) / max(1, len(self.conversation_manager.conversations)),
            "semantic_engine_stats": self.semantic_engine.get_stats()
        }