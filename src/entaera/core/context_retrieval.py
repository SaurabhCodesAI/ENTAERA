"""
ENTAERA Context Retrieval Engine

Day 4 Kata 4.2: Intelligent Context Retrieval System

This module provides intelligent context retrieval capabilities that enhance
AI conversations by dynamically selecting and injecting relevant historical
context based on the current conversation flow and user intent.

Features:
- Dynamic context selection based on conversation state
- Intelligent context ranking and prioritization
- Adaptive context window management
- Real-time context relevance scoring
- Context synthesis and summarization
- Performance-optimized context retrieval
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
import numpy as np

from .conversation import (
    Conversation, Message, MessageRole, MessageType, ConversationManager
)
from .conversation_memory import (
    ConversationMemoryManager, ConversationMemory, MemoryQuery, 
    ContextSummary, ConversationContext
)
from .semantic_search import SemanticSearchEngine, SearchFilter
from .logger import get_logger

logger = get_logger(__name__)


class ContextRetrievalStrategy(str, Enum):
    """Strategies for context retrieval."""
    SEMANTIC_SIMILARITY = "semantic_similarity"
    TEMPORAL_PROXIMITY = "temporal_proximity"
    TOPIC_COHERENCE = "topic_coherence"
    CONVERSATION_THREAD = "conversation_thread"
    HYBRID = "hybrid"


class ContextPriority(str, Enum):
    """Priority levels for context items."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ContextType(str, Enum):
    """Types of context that can be retrieved."""
    DIRECT_REFERENCE = "direct_reference"      # Direct mentions/references
    TOPICAL_CONTEXT = "topical_context"        # Same topic/domain
    PROCEDURAL_CONTEXT = "procedural_context"  # How-to/process related
    BACKGROUND_INFO = "background_info"        # General background
    RELATED_DISCUSSION = "related_discussion"  # Related conversations


class RetrievedContext(BaseModel):
    """Represents a piece of retrieved context."""
    context_id: str = Field(default_factory=lambda: str(uuid4()))
    context_type: ContextType
    priority: ContextPriority
    relevance_score: float
    content: str
    source_conversation_id: str
    source_message_id: str
    context_summary: str
    retrieval_reason: str
    temporal_distance_hours: float
    token_count: int = 0


class ContextRetrievalRequest(BaseModel):
    """Request for context retrieval."""
    current_message: str
    conversation_id: Optional[str] = None
    user_intent: Optional[str] = None
    max_context_items: int = 5
    max_total_tokens: int = 2000
    strategy: ContextRetrievalStrategy = ContextRetrievalStrategy.HYBRID
    time_window_hours: int = 24 * 7  # 1 week default
    include_context_types: List[ContextType] = Field(default_factory=lambda: list(ContextType))
    exclude_conversations: List[str] = Field(default_factory=list)
    minimum_relevance: float = 0.4


class ContextWindow(BaseModel):
    """Represents a window of context for a conversation."""
    conversation_id: str
    retrieved_contexts: List[RetrievedContext]
    total_tokens: int
    retrieval_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    strategy_used: ContextRetrievalStrategy
    retrieval_quality_score: float
    synthesis_summary: str = ""


class ContextRetrievalEngine:
    """Intelligent engine for retrieving and managing conversational context."""
    
    def __init__(
        self,
        memory_manager: ConversationMemoryManager,
        conversation_manager: ConversationManager,
        default_strategy: ContextRetrievalStrategy = ContextRetrievalStrategy.HYBRID
    ):
        self.memory_manager = memory_manager
        self.conversation_manager = conversation_manager
        self.default_strategy = default_strategy
        
        # Internal state
        self._context_cache: Dict[str, ContextWindow] = {}
        self._retrieval_stats = {
            "requests_processed": 0,
            "contexts_retrieved": 0,
            "average_relevance": 0.0,
            "cache_hits": 0
        }
        
        logger.info("Initialized ContextRetrievalEngine")
    
    async def retrieve_context(
        self, 
        request: ContextRetrievalRequest
    ) -> ContextWindow:
        """Retrieve relevant context for a conversation."""
        self._retrieval_stats["requests_processed"] += 1
        
        # Check cache first
        cache_key = self._generate_cache_key(request)
        cached_context = self._get_cached_context(cache_key)
        if cached_context:
            self._retrieval_stats["cache_hits"] += 1
            return cached_context
        
        logger.info(f"Retrieving context with strategy: {request.strategy}")
        
        # Route to appropriate retrieval strategy
        if request.strategy == ContextRetrievalStrategy.SEMANTIC_SIMILARITY:
            contexts = await self._retrieve_semantic_context(request)
        elif request.strategy == ContextRetrievalStrategy.TEMPORAL_PROXIMITY:
            contexts = await self._retrieve_temporal_context(request)
        elif request.strategy == ContextRetrievalStrategy.TOPIC_COHERENCE:
            contexts = await self._retrieve_topical_context(request)
        elif request.strategy == ContextRetrievalStrategy.CONVERSATION_THREAD:
            contexts = await self._retrieve_thread_context(request)
        else:  # HYBRID
            contexts = await self._retrieve_hybrid_context(request)
        
        # Rank and filter contexts
        ranked_contexts = await self._rank_and_filter_contexts(contexts, request)
        
        # Create context window
        context_window = ContextWindow(
            conversation_id=request.conversation_id or "unknown",
            retrieved_contexts=ranked_contexts,
            total_tokens=sum(ctx.token_count for ctx in ranked_contexts),
            strategy_used=request.strategy,
            retrieval_quality_score=self._calculate_quality_score(ranked_contexts)
        )
        
        # Generate synthesis summary
        context_window.synthesis_summary = await self._synthesize_context_summary(ranked_contexts)
        
        # Cache the result
        self._cache_context(cache_key, context_window)
        
        self._retrieval_stats["contexts_retrieved"] += len(ranked_contexts)
        logger.info(f"Retrieved {len(ranked_contexts)} context items with quality score {context_window.retrieval_quality_score:.2f}")
        
        return context_window
    
    async def _retrieve_semantic_context(
        self, 
        request: ContextRetrievalRequest
    ) -> List[RetrievedContext]:
        """Retrieve context using semantic similarity."""
        memory_query = MemoryQuery(
            current_message=request.current_message,
            max_memories=request.max_context_items * 2,  # Get more for filtering
            min_relevance_score=request.minimum_relevance,
            time_window_days=request.time_window_hours // 24
        )
        
        memories = await self.memory_manager.retrieve_relevant_memories(memory_query)
        
        contexts = []
        for memory in memories:
            context = await self._convert_memory_to_context(memory, ContextType.TOPICAL_CONTEXT)
            if context:
                contexts.append(context)
        
        return contexts
    
    async def _retrieve_temporal_context(
        self, 
        request: ContextRetrievalRequest
    ) -> List[RetrievedContext]:
        """Retrieve context based on temporal proximity."""
        contexts = []
        current_time = datetime.now(timezone.utc)
        time_threshold = current_time - timedelta(hours=request.time_window_hours)
        
        # Look through recent conversations
        for conversation in self.conversation_manager.conversations.values():
            if conversation.id in request.exclude_conversations:
                continue
            
            # Find recent messages
            recent_messages = [
                msg for msg in conversation.messages
                if msg.timestamp >= time_threshold
                and msg.content.strip()
            ]
            
            for message in recent_messages[-request.max_context_items:]:
                temporal_distance = (current_time - message.timestamp).total_seconds() / 3600
                
                context = RetrievedContext(
                    context_type=ContextType.BACKGROUND_INFO,
                    priority=self._calculate_priority_by_recency(temporal_distance),
                    relevance_score=max(0.1, 1.0 - (temporal_distance / request.time_window_hours)),
                    content=message.content,
                    source_conversation_id=conversation.id,
                    source_message_id=str(message.id),
                    context_summary=f"Recent message from {conversation.title}",
                    retrieval_reason=f"Temporal proximity ({temporal_distance:.1f} hours ago)",
                    temporal_distance_hours=temporal_distance,
                    token_count=len(message.content.split())
                )
                contexts.append(context)
        
        return contexts
    
    async def _retrieve_topical_context(
        self, 
        request: ContextRetrievalRequest
    ) -> List[RetrievedContext]:
        """Retrieve context based on topic coherence."""
        # Extract topics from current message
        topics = await self._extract_message_topics(request.current_message)
        
        contexts = []
        
        # Search for messages containing similar topics
        for topic in topics:
            memory_query = MemoryQuery(
                current_message=topic,
                max_memories=5,
                min_relevance_score=0.3,
                topic_keywords=[topic]
            )
            
            topic_memories = await self.memory_manager.retrieve_relevant_memories(memory_query)
            
            for memory in topic_memories:
                context = await self._convert_memory_to_context(memory, ContextType.TOPICAL_CONTEXT)
                if context:
                    context.retrieval_reason = f"Topic coherence: {topic}"
                    contexts.append(context)
        
        return contexts
    
    async def _retrieve_thread_context(
        self, 
        request: ContextRetrievalRequest
    ) -> List[RetrievedContext]:
        """Retrieve context from the same conversation thread."""
        contexts = []
        
        if not request.conversation_id:
            return contexts
        
        conversation = self.conversation_manager.get_conversation(request.conversation_id)
        if not conversation:
            return contexts
        
        # Get recent messages from the same conversation
        recent_messages = conversation.messages[-20:]  # Last 20 messages
        
        for message in recent_messages:
            if not message.content.strip():
                continue
            
            temporal_distance = (datetime.now(timezone.utc) - message.timestamp).total_seconds() / 3600
            
            # Calculate relevance based on position in conversation and recency
            position_factor = len(recent_messages) - recent_messages.index(message)
            relevance = min(1.0, (position_factor / len(recent_messages)) * 0.5 + 
                          max(0.1, 1.0 - temporal_distance / 24) * 0.5)
            
            context = RetrievedContext(
                context_type=ContextType.RELATED_DISCUSSION,
                priority=self._calculate_priority_by_position(position_factor, len(recent_messages)),
                relevance_score=relevance,
                content=message.content,
                source_conversation_id=conversation.id,
                source_message_id=str(message.id),
                context_summary=f"Thread message from {message.role.value}",
                retrieval_reason="Same conversation thread",
                temporal_distance_hours=temporal_distance,
                token_count=len(message.content.split())
            )
            contexts.append(context)
        
        return contexts
    
    async def _retrieve_hybrid_context(
        self, 
        request: ContextRetrievalRequest
    ) -> List[RetrievedContext]:
        """Retrieve context using a hybrid approach combining multiple strategies."""
        all_contexts = []
        
        # Retrieve using different strategies
        semantic_contexts = await self._retrieve_semantic_context(request)
        temporal_contexts = await self._retrieve_temporal_context(request)
        thread_contexts = await self._retrieve_thread_context(request)
        
        # Combine and deduplicate
        all_contexts.extend(semantic_contexts)
        all_contexts.extend(temporal_contexts)
        all_contexts.extend(thread_contexts)
        
        # Remove duplicates based on source message ID
        seen_messages = set()
        unique_contexts = []
        
        for context in all_contexts:
            if context.source_message_id not in seen_messages:
                seen_messages.add(context.source_message_id)
                unique_contexts.append(context)
        
        return unique_contexts
    
    async def _rank_and_filter_contexts(
        self, 
        contexts: List[RetrievedContext], 
        request: ContextRetrievalRequest
    ) -> List[RetrievedContext]:
        """Rank and filter contexts based on relevance and constraints."""
        # Filter by context types if specified
        if request.include_context_types:
            contexts = [ctx for ctx in contexts if ctx.context_type in request.include_context_types]
        
        # Filter by minimum relevance
        contexts = [ctx for ctx in contexts if ctx.relevance_score >= request.minimum_relevance]
        
        # Sort by relevance score (descending)
        contexts.sort(key=lambda x: x.relevance_score, reverse=True)
        
        # Apply token limit
        selected_contexts = []
        total_tokens = 0
        
        for context in contexts:
            if (len(selected_contexts) >= request.max_context_items or 
                total_tokens + context.token_count > request.max_total_tokens):
                break
            
            selected_contexts.append(context)
            total_tokens += context.token_count
        
        return selected_contexts
    
    async def _convert_memory_to_context(
        self, 
        memory: ConversationMemory, 
        context_type: ContextType
    ) -> Optional[RetrievedContext]:
        """Convert a ConversationMemory to a RetrievedContext."""
        try:
            temporal_distance = (datetime.now(timezone.utc) - memory.message_timestamp).total_seconds() / 3600
            
            priority = self._determine_context_priority(memory.relevance_score.combined_score, temporal_distance)
            
            context = RetrievedContext(
                context_type=context_type,
                priority=priority,
                relevance_score=memory.relevance_score.combined_score,
                content=memory.message_content,
                source_conversation_id=memory.conversation_id,
                source_message_id=memory.message_id,
                context_summary=f"From '{memory.conversation_title}' - {memory.message_role.value}",
                retrieval_reason=memory.relevance_score.reason,
                temporal_distance_hours=temporal_distance,
                token_count=len(memory.message_content.split())
            )
            
            return context
            
        except Exception as e:
            logger.error(f"Failed to convert memory to context: {e}")
            return None
    
    async def _extract_message_topics(self, message: str) -> List[str]:
        """Extract topics from a message."""
        # Simple topic extraction - can be enhanced with NLP
        words = message.lower().split()
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        topics = [word for word in words if len(word) > 3 and word not in stop_words]
        
        # Get unique topics
        return list(set(topics))
    
    def _calculate_priority_by_recency(self, hours_ago: float) -> ContextPriority:
        """Calculate priority based on recency."""
        if hours_ago < 1:
            return ContextPriority.CRITICAL
        elif hours_ago < 6:
            return ContextPriority.HIGH
        elif hours_ago < 24:
            return ContextPriority.MEDIUM
        else:
            return ContextPriority.LOW
    
    def _calculate_priority_by_position(self, position: int, total: int) -> ContextPriority:
        """Calculate priority based on position in conversation."""
        ratio = position / total
        if ratio > 0.8:
            return ContextPriority.HIGH
        elif ratio > 0.5:
            return ContextPriority.MEDIUM
        else:
            return ContextPriority.LOW
    
    def _determine_context_priority(self, relevance_score: float, temporal_distance: float) -> ContextPriority:
        """Determine context priority based on relevance and temporal factors."""
        # Combine relevance and recency
        recency_factor = max(0, 1 - temporal_distance / 168)  # 168 hours = 1 week
        combined_score = 0.7 * relevance_score + 0.3 * recency_factor
        
        if combined_score > 0.8:
            return ContextPriority.CRITICAL
        elif combined_score > 0.6:
            return ContextPriority.HIGH
        elif combined_score > 0.4:
            return ContextPriority.MEDIUM
        else:
            return ContextPriority.LOW
    
    def _calculate_quality_score(self, contexts: List[RetrievedContext]) -> float:
        """Calculate overall quality score for retrieved contexts."""
        if not contexts:
            return 0.0
        
        # Factors for quality:
        # 1. Average relevance score
        avg_relevance = sum(ctx.relevance_score for ctx in contexts) / len(contexts)
        
        # 2. Diversity of context types
        unique_types = len(set(ctx.context_type for ctx in contexts))
        type_diversity = min(1.0, unique_types / len(ContextType))
        
        # 3. Priority distribution
        high_priority_count = sum(1 for ctx in contexts if ctx.priority in [ContextPriority.CRITICAL, ContextPriority.HIGH])
        priority_factor = high_priority_count / len(contexts)
        
        # Combine factors
        quality_score = 0.5 * avg_relevance + 0.3 * priority_factor + 0.2 * type_diversity
        
        return min(1.0, quality_score)
    
    async def _synthesize_context_summary(self, contexts: List[RetrievedContext]) -> str:
        """Create a summary of the retrieved context."""
        if not contexts:
            return "No relevant context found."
        
        summary_parts = []
        
        # Group by context type
        type_groups = {}
        for context in contexts:
            if context.context_type not in type_groups:
                type_groups[context.context_type] = []
            type_groups[context.context_type].append(context)
        
        # Create summary for each type
        for context_type, contexts_of_type in type_groups.items():
            count = len(contexts_of_type)
            avg_relevance = sum(ctx.relevance_score for ctx in contexts_of_type) / count
            
            type_summary = f"{count} {context_type.value} items (avg. relevance: {avg_relevance:.2f})"
            summary_parts.append(type_summary)
        
        total_contexts = len(contexts)
        avg_total_relevance = sum(ctx.relevance_score for ctx in contexts) / total_contexts
        
        summary = f"Retrieved {total_contexts} context items with average relevance {avg_total_relevance:.2f}. " + "; ".join(summary_parts)
        
        return summary
    
    def _generate_cache_key(self, request: ContextRetrievalRequest) -> str:
        """Generate a cache key for a context retrieval request."""
        key_parts = [
            request.current_message[:50],  # First 50 chars of message
            request.strategy.value,
            str(request.max_context_items),
            str(request.time_window_hours),
            str(request.minimum_relevance)
        ]
        return "|".join(key_parts)
    
    def _get_cached_context(self, cache_key: str) -> Optional[ContextWindow]:
        """Get cached context if available and not expired."""
        if cache_key not in self._context_cache:
            return None
        
        cached_context = self._context_cache[cache_key]
        
        # Check if cache is expired (1 hour)
        if (datetime.now(timezone.utc) - cached_context.retrieval_timestamp).total_seconds() > 3600:
            del self._context_cache[cache_key]
            return None
        
        return cached_context
    
    def _cache_context(self, cache_key: str, context_window: ContextWindow) -> None:
        """Cache a context window."""
        # Limit cache size (keep only 100 most recent)
        if len(self._context_cache) >= 100:
            # Remove oldest entries
            sorted_cache = sorted(
                self._context_cache.items(),
                key=lambda x: x[1].retrieval_timestamp
            )
            for key, _ in sorted_cache[:20]:  # Remove oldest 20
                del self._context_cache[key]
        
        self._context_cache[cache_key] = context_window
    
    async def get_context_for_message(
        self, 
        message: str, 
        conversation_id: Optional[str] = None,
        strategy: Optional[ContextRetrievalStrategy] = None
    ) -> ContextWindow:
        """Convenient method to get context for a message."""
        request = ContextRetrievalRequest(
            current_message=message,
            conversation_id=conversation_id,
            strategy=strategy or self.default_strategy
        )
        
        return await self.retrieve_context(request)
    
    def get_retrieval_stats(self) -> Dict[str, Any]:
        """Get retrieval engine statistics."""
        if self._retrieval_stats["requests_processed"] > 0:
            self._retrieval_stats["average_relevance"] = (
                self._retrieval_stats["contexts_retrieved"] / 
                self._retrieval_stats["requests_processed"]
            )
        
        return {
            **self._retrieval_stats,
            "cache_size": len(self._context_cache),
            "cache_hit_rate": (
                self._retrieval_stats["cache_hits"] / 
                max(1, self._retrieval_stats["requests_processed"])
            )
        }
    
    def clear_cache(self) -> None:
        """Clear the context cache."""
        self._context_cache.clear()
        logger.info("Cleared context retrieval cache")