"""
ENTAERA Multi-Agent Orchestration System

Day 5 Kata 5.1: Multi-Agent Orchestration and Workflow Management

This module provides sophisticated multi-agent orchestration capabilities that enable
multiple AI agents to collaborate on complex tasks, with intelligent workflow
management, task delegation, and result synthesis.

Features:
- Multi-agent task orchestration and coordination
- Intelligent workflow management and execution
- Dynamic task delegation and load balancing
- Agent capability assessment and selection
- Result aggregation and synthesis
- Workflow monitoring and optimization
"""

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union, Callable
from uuid import UUID, uuid4
from pathlib import Path

from pydantic import BaseModel, Field, field_validator
import numpy as np

from .conversation import (
    Conversation, Message, MessageRole, MessageType, ConversationManager
)
from .conversation_memory import ConversationMemoryManager
from .context_retrieval import ContextRetrievalEngine
from .semantic_search import SemanticSearchEngine
from .logger import get_logger

logger = get_logger(__name__)


class AgentType(str, Enum):
    """Types of AI agents in the orchestration system."""
    CONVERSATIONAL = "conversational"      # Chat and dialogue agents
    ANALYTICAL = "analytical"              # Data analysis and research agents
    CREATIVE = "creative"                  # Content generation and creative agents
    TASK_EXECUTOR = "task_executor"        # Action and task execution agents
    COORDINATOR = "coordinator"            # Workflow coordination agents
    SPECIALIST = "specialist"              # Domain-specific expert agents


class TaskType(str, Enum):
    """Types of tasks that can be orchestrated."""
    RESEARCH = "research"
    ANALYSIS = "analysis"
    CONTENT_GENERATION = "content_generation"
    PROBLEM_SOLVING = "problem_solving"
    CODE_GENERATION = "code_generation"
    CONVERSATION = "conversation"
    WORKFLOW_COORDINATION = "workflow_coordination"


class TaskStatus(str, Enum):
    """Status of tasks in the orchestration system."""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    WAITING_DEPENDENCIES = "waiting_dependencies"


class AgentStatus(str, Enum):
    """Status of agents in the orchestration system."""
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"
    ERROR = "error"


class AgentCapability(BaseModel):
    """Represents a capability of an AI agent."""
    capability_type: TaskType
    proficiency_level: float = Field(ge=0.0, le=1.0)  # 0.0 to 1.0
    max_concurrent_tasks: int = Field(ge=1, default=1)
    average_completion_time: float = 0.0  # seconds
    success_rate: float = Field(ge=0.0, le=1.0, default=1.0)
    cost_per_task: float = 0.0
    specialization_tags: List[str] = Field(default_factory=list)


class WorkflowTask(BaseModel):
    """Represents a task in a workflow."""
    task_id: str = Field(default_factory=lambda: str(uuid4()))
    task_type: TaskType
    description: str
    priority: int = Field(ge=1, le=10, default=5)  # 1 = highest, 10 = lowest
    requirements: Dict[str, Any] = Field(default_factory=dict)
    dependencies: List[str] = Field(default_factory=list)  # Task IDs
    estimated_duration: float = 0.0  # seconds
    max_retries: int = 3
    timeout: float = 300.0  # 5 minutes default
    context: Dict[str, Any] = Field(default_factory=dict)
    
    # Execution state
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent_id: Optional[str] = None
    start_time: Optional[datetime] = None
    completion_time: Optional[datetime] = None
    result: Optional[Any] = None
    error_message: Optional[str] = None
    retry_count: int = 0


class AgentPerformanceMetrics(BaseModel):
    """Performance metrics for an AI agent."""
    total_tasks_completed: int = 0
    total_tasks_failed: int = 0
    average_completion_time: float = 0.0
    success_rate: float = 1.0
    current_load: int = 0
    last_activity: Optional[datetime] = None
    availability_score: float = 1.0  # 0.0 = unavailable, 1.0 = fully available


class AIAgent(ABC):
    """Abstract base class for AI agents in the orchestration system."""
    
    def __init__(
        self,
        agent_id: str,
        agent_type: AgentType,
        name: str,
        capabilities: List[AgentCapability]
    ):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.name = name
        self.capabilities = {cap.capability_type: cap for cap in capabilities}
        self.metrics = AgentPerformanceMetrics()
        self.is_active = True
        self.current_tasks: Set[str] = set()
        
    @abstractmethod
    async def execute_task(self, task: WorkflowTask) -> Any:
        """Execute a specific task and return the result."""
        pass
    
    @abstractmethod
    async def can_handle_task(self, task: WorkflowTask) -> float:
        """Return a score (0.0-1.0) indicating how well this agent can handle the task."""
        pass
    
    def get_capability_score(self, task_type: TaskType) -> float:
        """Get the agent's capability score for a specific task type."""
        if task_type in self.capabilities:
            return self.capabilities[task_type].proficiency_level
        return 0.0
    
    def get_availability_score(self) -> float:
        """Calculate current availability based on load and capabilities."""
        if not self.is_active:
            return 0.0
        
        total_capacity = sum(cap.max_concurrent_tasks for cap in self.capabilities.values())
        current_load = len(self.current_tasks)
        
        if total_capacity == 0:
            return 0.0
        
        load_ratio = current_load / total_capacity
        availability = max(0.0, 1.0 - load_ratio)
        
        # Factor in success rate
        availability *= self.metrics.success_rate
        
        return availability
    
    async def start_task(self, task: WorkflowTask) -> None:
        """Mark a task as started."""
        self.current_tasks.add(task.task_id)
        task.assigned_agent_id = self.agent_id
        task.status = TaskStatus.IN_PROGRESS
        task.start_time = datetime.now(timezone.utc)
        self.metrics.last_activity = task.start_time
    
    async def complete_task(self, task: WorkflowTask, result: Any) -> None:
        """Mark a task as completed with result."""
        self.current_tasks.discard(task.task_id)
        task.status = TaskStatus.COMPLETED
        task.completion_time = datetime.now(timezone.utc)
        task.result = result
        
        # Update metrics
        self.metrics.total_tasks_completed += 1
        if task.start_time and task.completion_time:
            duration = (task.completion_time - task.start_time).total_seconds()
            self._update_average_completion_time(duration)
        
        self._update_success_rate()
    
    async def fail_task(self, task: WorkflowTask, error: str) -> None:
        """Mark a task as failed with error."""
        self.current_tasks.discard(task.task_id)
        task.status = TaskStatus.FAILED
        task.completion_time = datetime.now(timezone.utc)
        task.error_message = error
        
        # Update metrics
        self.metrics.total_tasks_failed += 1
        self._update_success_rate()
    
    def _update_average_completion_time(self, new_duration: float) -> None:
        """Update the running average completion time."""
        total_completed = self.metrics.total_tasks_completed
        if total_completed == 1:
            self.metrics.average_completion_time = new_duration
        else:
            current_avg = self.metrics.average_completion_time
            self.metrics.average_completion_time = (
                (current_avg * (total_completed - 1) + new_duration) / total_completed
            )
    
    def _update_success_rate(self) -> None:
        """Update the success rate based on completed vs failed tasks."""
        total_tasks = self.metrics.total_tasks_completed + self.metrics.total_tasks_failed
        if total_tasks > 0:
            self.metrics.success_rate = self.metrics.total_tasks_completed / total_tasks


class ConversationalAgent(AIAgent):
    """Agent specialized in conversation and dialogue tasks."""
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        conversation_manager: ConversationManager,
        context_engine: Optional[ContextRetrievalEngine] = None
    ):
        capabilities = [
            AgentCapability(
                capability_type=TaskType.CONVERSATION,
                proficiency_level=0.9,
                max_concurrent_tasks=3,
                specialization_tags=["dialogue", "chat", "user_interaction"]
            ),
            AgentCapability(
                capability_type=TaskType.CONTENT_GENERATION,
                proficiency_level=0.7,
                max_concurrent_tasks=2,
                specialization_tags=["text_generation", "responses"]
            )
        ]
        
        super().__init__(agent_id, AgentType.CONVERSATIONAL, name, capabilities)
        self.conversation_manager = conversation_manager
        self.context_engine = context_engine
    
    async def execute_task(self, task: WorkflowTask) -> Any:
        """Execute conversation-related tasks."""
        await self.start_task(task)
        
        try:
            if task.task_type == TaskType.CONVERSATION:
                result = await self._handle_conversation_task(task)
            elif task.task_type == TaskType.CONTENT_GENERATION:
                result = await self._handle_content_generation_task(task)
            else:
                raise ValueError(f"Unsupported task type: {task.task_type}")
            
            await self.complete_task(task, result)
            return result
            
        except Exception as e:
            await self.fail_task(task, str(e))
            raise
    
    async def can_handle_task(self, task: WorkflowTask) -> float:
        """Assess ability to handle conversation tasks."""
        base_score = self.get_capability_score(task.task_type)
        availability = self.get_availability_score()
        
        # Bonus for conversation-related context
        context_bonus = 0.0
        if "conversation" in task.description.lower() or "chat" in task.description.lower():
            context_bonus = 0.1
        
        return min(1.0, base_score * availability + context_bonus)
    
    async def _handle_conversation_task(self, task: WorkflowTask) -> Dict[str, Any]:
        """Handle conversation-specific tasks."""
        conversation_id = task.context.get("conversation_id")
        message_content = task.requirements.get("message", "")
        
        if not conversation_id or not message_content:
            raise ValueError("Conversation task requires conversation_id and message")
        
        # Get or create conversation
        conversation = self.conversation_manager.get_conversation(conversation_id)
        if not conversation:
            conversation = Conversation(title="Agent Orchestrated Conversation")
            await self.conversation_manager.save_conversation(conversation)
        
        # Add user message
        user_message = Message(
            role=MessageRole.USER,
            content=message_content
        )
        conversation.add_message(user_message)
        
        # Generate response (simplified - in real implementation, this would use an LLM)
        response_content = f"Agent {self.name} response to: {message_content}"
        
        # Add assistant response
        assistant_message = Message(
            role=MessageRole.ASSISTANT,
            content=response_content,
            metadata={"agent_id": self.agent_id, "agent_name": self.name}
        )
        conversation.add_message(assistant_message)
        
        # Save conversation
        await self.conversation_manager.save_conversation(conversation)
        
        return {
            "conversation_id": conversation_id,
            "response": response_content,
            "message_id": str(assistant_message.id)
        }
    
    async def _handle_content_generation_task(self, task: WorkflowTask) -> Dict[str, Any]:
        """Handle content generation tasks."""
        content_type = task.requirements.get("content_type", "text")
        prompt = task.requirements.get("prompt", "")
        max_length = task.requirements.get("max_length", 1000)
        
        # Simulate content generation (in real implementation, use LLM)
        generated_content = f"Generated {content_type} content for prompt: {prompt[:50]}..."
        
        return {
            "content_type": content_type,
            "generated_content": generated_content,
            "length": len(generated_content)
        }


class AnalyticalAgent(AIAgent):
    """Agent specialized in analysis and research tasks."""
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        semantic_engine: SemanticSearchEngine
    ):
        capabilities = [
            AgentCapability(
                capability_type=TaskType.ANALYSIS,
                proficiency_level=0.95,
                max_concurrent_tasks=2,
                specialization_tags=["data_analysis", "research", "insights"]
            ),
            AgentCapability(
                capability_type=TaskType.RESEARCH,
                proficiency_level=0.9,
                max_concurrent_tasks=3,
                specialization_tags=["information_gathering", "fact_finding"]
            )
        ]
        
        super().__init__(agent_id, AgentType.ANALYTICAL, name, capabilities)
        self.semantic_engine = semantic_engine
    
    async def execute_task(self, task: WorkflowTask) -> Any:
        """Execute analytical tasks."""
        await self.start_task(task)
        
        try:
            if task.task_type == TaskType.ANALYSIS:
                result = await self._handle_analysis_task(task)
            elif task.task_type == TaskType.RESEARCH:
                result = await self._handle_research_task(task)
            else:
                raise ValueError(f"Unsupported task type: {task.task_type}")
            
            await self.complete_task(task, result)
            return result
            
        except Exception as e:
            await self.fail_task(task, str(e))
            raise
    
    async def can_handle_task(self, task: WorkflowTask) -> float:
        """Assess ability to handle analytical tasks."""
        base_score = self.get_capability_score(task.task_type)
        availability = self.get_availability_score()
        
        # Bonus for analytical keywords
        analysis_bonus = 0.0
        analysis_keywords = ["analyze", "research", "investigate", "study", "examine"]
        if any(keyword in task.description.lower() for keyword in analysis_keywords):
            analysis_bonus = 0.15
        
        return min(1.0, base_score * availability + analysis_bonus)
    
    async def _handle_analysis_task(self, task: WorkflowTask) -> Dict[str, Any]:
        """Handle data analysis tasks."""
        data_source = task.requirements.get("data_source", "")
        analysis_type = task.requirements.get("analysis_type", "general")
        
        # Simulate analysis (in real implementation, perform actual analysis)
        analysis_results = {
            "analysis_type": analysis_type,
            "data_source": data_source,
            "insights": [
                "Key pattern identified in data",
                "Significant correlation discovered",
                "Trend analysis completed"
            ],
            "confidence_score": 0.85,
            "recommendations": [
                "Recommendation 1 based on analysis",
                "Recommendation 2 for optimization"
            ]
        }
        
        return analysis_results
    
    async def _handle_research_task(self, task: WorkflowTask) -> Dict[str, Any]:
        """Handle research tasks."""
        research_query = task.requirements.get("query", "")
        scope = task.requirements.get("scope", "general")
        
        # Use semantic search if available
        search_results = []
        if self.semantic_engine and research_query:
            try:
                results = await self.semantic_engine.search(research_query)
                search_results = [
                    {
                        "content": result.content[:200] + "...",
                        "similarity_score": result.similarity_score,
                        "source": result.source_id
                    }
                    for result in results[:5]
                ]
            except Exception as e:
                logger.warning(f"Semantic search failed: {e}")
        
        research_results = {
            "query": research_query,
            "scope": scope,
            "findings": search_results,
            "summary": f"Research completed for query: {research_query}",
            "sources_found": len(search_results),
            "research_quality": 0.8
        }
        
        return research_results


class CreativeAgent(AIAgent):
    """Agent specialized in creative content generation and ideation."""
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        semantic_engine: Optional[SemanticSearchEngine] = None
    ):
        capabilities = [
            AgentCapability(
                capability_type=TaskType.CONTENT_GENERATION,
                proficiency_level=0.95,
                max_concurrent_tasks=2,
                specialization_tags=["creative_writing", "ideation", "storytelling"]
            ),
            AgentCapability(
                capability_type=TaskType.PROBLEM_SOLVING,
                proficiency_level=0.8,
                max_concurrent_tasks=1,
                specialization_tags=["creative_solutions", "brainstorming"]
            )
        ]
        
        super().__init__(agent_id, AgentType.CREATIVE, name, capabilities)
        self.semantic_engine = semantic_engine
        self.creative_templates = {
            "story": "Once upon a time, {context}...",
            "article": "# {title}\n\n{content}",
            "idea": "💡 {concept}: {description}",
            "solution": "🔧 Solution: {approach}\n\nBenefits: {benefits}"
        }
    
    async def execute_task(self, task: WorkflowTask) -> Any:
        """Execute creative tasks."""
        await self.start_task(task)
        
        try:
            if task.task_type == TaskType.CONTENT_GENERATION:
                result = await self._handle_creative_generation(task)
            elif task.task_type == TaskType.PROBLEM_SOLVING:
                result = await self._handle_creative_problem_solving(task)
            else:
                raise ValueError(f"Unsupported task type: {task.task_type}")
            
            await self.complete_task(task, result)
            return result
            
        except Exception as e:
            await self.fail_task(task, str(e))
            raise
    
    async def can_handle_task(self, task: WorkflowTask) -> float:
        """Assess ability to handle creative tasks."""
        base_score = self.get_capability_score(task.task_type)
        availability = self.get_availability_score()
        
        # Bonus for creative keywords
        creative_bonus = 0.0
        creative_keywords = ["create", "generate", "write", "design", "brainstorm", "ideate"]
        if any(keyword in task.description.lower() for keyword in creative_keywords):
            creative_bonus = 0.2
        
        return min(1.0, base_score * availability + creative_bonus)
    
    async def _handle_creative_generation(self, task: WorkflowTask) -> Dict[str, Any]:
        """Handle creative content generation."""
        content_type = task.requirements.get("content_type", "text")
        theme = task.requirements.get("theme", "general")
        length = task.requirements.get("length", "medium")
        style = task.requirements.get("style", "informative")
        
        # Use semantic search for inspiration if available
        inspiration_sources = []
        if self.semantic_engine and theme != "general":
            try:
                search_results = await self.semantic_engine.search(theme)
                inspiration_sources = [r.content[:100] for r in search_results[:3]]
            except Exception as e:
                logger.warning(f"Failed to get inspiration from semantic search: {e}")
        
        # Generate creative content based on type
        if content_type == "story":
            content = self._generate_story(theme, style, inspiration_sources)
        elif content_type == "article":
            content = self._generate_article(theme, style, inspiration_sources)
        elif content_type == "ideas":
            content = self._generate_ideas(theme, inspiration_sources)
        else:
            content = self._generate_general_content(theme, style, inspiration_sources)
        
        result = {
            "content_type": content_type,
            "theme": theme,
            "style": style,
            "generated_content": content,
            "word_count": len(content.split()),
            "inspiration_sources": len(inspiration_sources),
            "creativity_score": self._calculate_creativity_score(content, theme)
        }
        
        return result
    
    async def _handle_creative_problem_solving(self, task: WorkflowTask) -> Dict[str, Any]:
        """Handle creative problem-solving tasks."""
        problem_description = task.requirements.get("problem", "")
        constraints = task.requirements.get("constraints", [])
        approach = task.requirements.get("approach", "brainstorming")
        
        # Generate creative solutions
        solutions = []
        if approach == "brainstorming":
            solutions = self._brainstorm_solutions(problem_description, constraints)
        elif approach == "lateral_thinking":
            solutions = self._lateral_thinking_solutions(problem_description)
        else:
            solutions = self._general_problem_solving(problem_description, constraints)
        
        result = {
            "problem": problem_description,
            "approach": approach,
            "constraints": constraints,
            "solutions": solutions,
            "solution_count": len(solutions),
            "innovation_score": self._calculate_innovation_score(solutions)
        }
        
        return result
    
    def _generate_story(self, theme: str, style: str, inspiration: List[str]) -> str:
        """Generate a creative story."""
        inspiration_context = " ".join(inspiration[:2]) if inspiration else "a mysterious world"
        
        story_elements = {
            "adventure": "brave hero embarked on a perilous journey",
            "mystery": "detective discovered a puzzling case",
            "romance": "two hearts found each other against all odds",
            "sci-fi": "explorer ventured into uncharted space",
            "fantasy": "magical being awakened from ancient slumber"
        }
        
        element = story_elements.get(theme, "character faced an unexpected challenge")
        
        story = f"""In a world inspired by {inspiration_context}, a {element}. 
        
The {style} narrative unfolded with unexpected twists, revealing deeper truths about {theme}. 
As the story progressed, themes of courage, discovery, and transformation emerged, 
creating a compelling tale that resonated with universal human experiences.

Through creative storytelling, the narrative explored the essence of {theme}, 
weaving together elements of {style} style with imaginative scenarios 
that captured the reader's imagination and left them pondering the possibilities."""
        
        return story
    
    def _generate_article(self, theme: str, style: str, inspiration: List[str]) -> str:
        """Generate an informative article."""
        return f"""# Exploring {theme.title()}: A {style.title()} Perspective

## Introduction

The fascinating world of {theme} offers countless opportunities for exploration and understanding. 
Drawing from diverse sources of inspiration, this article delves into the key aspects that make 
{theme} such a compelling subject.

## Key Insights

Through careful analysis and creative thinking, several important insights emerge:

1. **Innovation Factor**: {theme} represents a unique opportunity for breakthrough thinking
2. **Practical Applications**: Real-world applications demonstrate the value of {theme}
3. **Future Potential**: The trajectory of {theme} suggests exciting developments ahead

## Creative Synthesis

By combining traditional approaches with innovative methodologies, we can unlock new 
perspectives on {theme}. This synthesis approach reveals hidden connections and 
unexpected possibilities.

## Conclusion

The exploration of {theme} through a {style} lens demonstrates the power of creative 
thinking in generating fresh insights and practical solutions."""
    
    def _generate_ideas(self, theme: str, inspiration: List[str]) -> str:
        """Generate creative ideas."""
        ideas = [
            f"💡 Interactive {theme} experience that engages users through immersive storytelling",
            f"🎨 Creative {theme} workshop combining traditional methods with digital innovation",
            f"🔗 Community-driven {theme} platform fostering collaboration and knowledge sharing",
            f"🚀 Gamified {theme} learning system with progressive challenges and rewards",
            f"🌐 Virtual {theme} environment enabling global participation and cultural exchange"
        ]
        
        return "\n".join(ideas)
    
    def _generate_general_content(self, theme: str, style: str, inspiration: List[str]) -> str:
        """Generate general creative content."""
        return f"""Creative exploration of {theme} reveals fascinating possibilities. 
        
Through {style} examination, we discover innovative approaches that challenge 
conventional thinking. The integration of diverse perspectives creates a rich 
tapestry of ideas that inspire further exploration.

Key creative elements include:
- Imaginative problem-solving approaches
- Innovative synthesis of existing concepts  
- Fresh perspectives on familiar challenges
- Unexpected connections between disparate ideas

This creative journey demonstrates the power of open-minded exploration 
and the value of embracing unconventional thinking patterns."""
    
    def _brainstorm_solutions(self, problem: str, constraints: List[str]) -> List[Dict[str, str]]:
        """Generate brainstormed solutions."""
        solutions = [
            {
                "title": "Innovative Approach #1",
                "description": f"Creative solution addressing {problem} through novel methodology",
                "benefits": "Overcomes traditional limitations, offers scalable implementation",
                "feasibility": "High - builds on existing resources"
            },
            {
                "title": "Disruptive Solution #2", 
                "description": f"Radical reimagining of the approach to {problem}",
                "benefits": "Breakthrough potential, competitive advantage",
                "feasibility": "Medium - requires significant innovation"
            },
            {
                "title": "Collaborative Framework #3",
                "description": f"Community-driven solution for {problem}",
                "benefits": "Leverages collective intelligence, sustainable model",
                "feasibility": "High - proven collaboration patterns"
            }
        ]
        
        return solutions
    
    def _lateral_thinking_solutions(self, problem: str) -> List[Dict[str, str]]:
        """Generate lateral thinking solutions."""
        return [
            {
                "title": "Reverse Engineering Solution",
                "description": f"Solve {problem} by working backwards from desired outcome",
                "approach": "Start with perfect result, identify required steps",
                "innovation_level": "High"
            },
            {
                "title": "Analogical Transfer",
                "description": f"Apply solutions from completely different domains to {problem}",
                "approach": "Find successful patterns in nature, other industries",
                "innovation_level": "Very High"
            }
        ]
    
    def _general_problem_solving(self, problem: str, constraints: List[str]) -> List[Dict[str, str]]:
        """Generate general problem-solving approaches."""
        return [
            {
                "title": "Systematic Analysis",
                "description": f"Methodical breakdown and solution of {problem}",
                "methodology": "Divide into sub-problems, solve incrementally",
                "suitability": "Well-defined problems with clear constraints"
            },
            {
                "title": "Iterative Refinement",
                "description": f"Continuous improvement approach to {problem}",
                "methodology": "Rapid prototyping, feedback integration, adaptation", 
                "suitability": "Complex problems requiring flexible solutions"
            }
        ]
    
    def _calculate_creativity_score(self, content: str, theme: str) -> float:
        """Calculate a creativity score for generated content."""
        # Simple heuristic based on vocabulary diversity and length
        words = content.split()
        unique_words = set(word.lower() for word in words)
        vocabulary_diversity = len(unique_words) / len(words) if words else 0
        
        # Bonus for thematic coherence
        theme_coherence = 0.1 if theme.lower() in content.lower() else 0
        
        # Bonus for creative language patterns
        creative_patterns = ["imagine", "envision", "transform", "innovate", "breakthrough"]
        pattern_bonus = sum(0.02 for pattern in creative_patterns if pattern in content.lower())
        
        creativity_score = min(1.0, vocabulary_diversity + theme_coherence + pattern_bonus)
        return creativity_score
    
    def _calculate_innovation_score(self, solutions: List[Dict[str, Any]]) -> float:
        """Calculate innovation score for generated solutions."""
        if not solutions:
            return 0.0
        
        # Simple scoring based on number and diversity of solutions
        base_score = min(1.0, len(solutions) / 5)  # Up to 5 solutions = full score
        
        # Bonus for solution diversity (different approaches)
        unique_approaches = set()
        for solution in solutions:
            approach = solution.get("approach", solution.get("methodology", "standard"))
            unique_approaches.add(approach)
        
        diversity_bonus = len(unique_approaches) / len(solutions) * 0.3
        
        return min(1.0, base_score + diversity_bonus)


class TaskExecutorAgent(AIAgent):
    """Agent specialized in executing concrete tasks and actions."""
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        execution_capabilities: Optional[List[str]] = None
    ):
        capabilities = [
            AgentCapability(
                capability_type=TaskType.TASK_EXECUTOR,
                proficiency_level=0.9,
                max_concurrent_tasks=5,
                specialization_tags=["automation", "execution", "actions"]
            ),
            AgentCapability(
                capability_type=TaskType.CODE_GENERATION,
                proficiency_level=0.8,
                max_concurrent_tasks=2,
                specialization_tags=["scripting", "automation", "implementation"]
            )
        ]
        
        super().__init__(agent_id, AgentType.TASK_EXECUTOR, name, capabilities)
        self.execution_capabilities = execution_capabilities or [
            "file_operations", "data_processing", "api_calls", "calculations"
        ]
        self.execution_history: List[Dict[str, Any]] = []
    
    async def execute_task(self, task: WorkflowTask) -> Any:
        """Execute concrete tasks and actions."""
        await self.start_task(task)
        
        try:
            if task.task_type == TaskType.CODE_GENERATION:
                result = await self._handle_code_generation(task)
            else:
                result = await self._handle_task_execution(task)
            
            await self.complete_task(task, result)
            return result
            
        except Exception as e:
            await self.fail_task(task, str(e))
            raise
    
    async def can_handle_task(self, task: WorkflowTask) -> float:
        """Assess ability to handle execution tasks."""
        base_score = self.get_capability_score(task.task_type)
        availability = self.get_availability_score()
        
        # Check if task requires specific execution capabilities
        capability_match = 0.0
        task_requirements = task.requirements.get("capabilities", [])
        if task_requirements:
            matches = sum(1 for req in task_requirements if req in self.execution_capabilities)
            capability_match = matches / len(task_requirements) * 0.3
        
        # Bonus for action-oriented keywords
        execution_bonus = 0.0
        execution_keywords = ["execute", "run", "process", "calculate", "generate", "automate"]
        if any(keyword in task.description.lower() for keyword in execution_keywords):
            execution_bonus = 0.15
        
        return min(1.0, base_score * availability + capability_match + execution_bonus)
    
    async def _handle_task_execution(self, task: WorkflowTask) -> Dict[str, Any]:
        """Handle general task execution."""
        action_type = task.requirements.get("action_type", "general")
        parameters = task.requirements.get("parameters", {})
        
        execution_result = {
            "action_type": action_type,
            "parameters": parameters,
            "execution_status": "completed",
            "output": None,
            "execution_time": 0.0
        }
        
        start_time = datetime.now(timezone.utc)
        
        try:
            if action_type == "file_operations":
                output = await self._execute_file_operations(parameters)
            elif action_type == "data_processing":
                output = await self._execute_data_processing(parameters)
            elif action_type == "calculations":
                output = await self._execute_calculations(parameters)
            elif action_type == "api_calls":
                output = await self._execute_api_calls(parameters)
            else:
                output = await self._execute_generic_action(action_type, parameters)
            
            execution_result["output"] = output
            execution_result["execution_status"] = "completed"
            
        except Exception as e:
            execution_result["execution_status"] = "failed"
            execution_result["error"] = str(e)
        
        end_time = datetime.now(timezone.utc)
        execution_result["execution_time"] = (end_time - start_time).total_seconds()
        
        # Record execution history
        self.execution_history.append({
            "task_id": task.task_id,
            "action_type": action_type,
            "timestamp": start_time,
            "result": execution_result
        })
        
        return execution_result
    
    async def _handle_code_generation(self, task: WorkflowTask) -> Dict[str, Any]:
        """Handle code generation tasks."""
        language = task.requirements.get("language", "python")
        purpose = task.requirements.get("purpose", "general")
        specifications = task.requirements.get("specifications", {})
        
        # Generate code based on specifications
        if language == "python":
            code = self._generate_python_code(purpose, specifications)
        elif language == "javascript":
            code = self._generate_javascript_code(purpose, specifications)
        else:
            code = self._generate_generic_code(language, purpose, specifications)
        
        result = {
            "language": language,
            "purpose": purpose,
            "generated_code": code,
            "line_count": len(code.split('\n')),
            "specifications_met": len(specifications),
            "code_quality_score": self._assess_code_quality(code)
        }
        
        return result
    
    async def _execute_file_operations(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute file operation tasks."""
        operation = parameters.get("operation", "read")
        file_path = parameters.get("file_path", "")
        
        # Simulate file operations (in real implementation, perform actual operations)
        return {
            "operation": operation,
            "file_path": file_path,
            "status": "completed",
            "details": f"Successfully performed {operation} operation on {file_path}"
        }
    
    async def _execute_data_processing(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute data processing tasks."""
        data_source = parameters.get("data_source", "")
        processing_type = parameters.get("processing_type", "transform")
        
        # Simulate data processing
        return {
            "data_source": data_source,
            "processing_type": processing_type,
            "records_processed": 1000,
            "processing_time": 2.5,
            "output_format": "processed_data.json"
        }
    
    async def _execute_calculations(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute mathematical calculations."""
        calculation_type = parameters.get("calculation_type", "arithmetic")
        inputs = parameters.get("inputs", [])
        
        # Perform actual calculations if possible
        result_value = None
        if calculation_type == "sum" and inputs:
            result_value = sum(float(x) for x in inputs if isinstance(x, (int, float)))
        elif calculation_type == "average" and inputs:
            numeric_inputs = [float(x) for x in inputs if isinstance(x, (int, float))]
            result_value = sum(numeric_inputs) / len(numeric_inputs) if numeric_inputs else 0
        
        return {
            "calculation_type": calculation_type,
            "inputs": inputs,
            "result": result_value,
            "calculation_status": "completed"
        }
    
    async def _execute_api_calls(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute API call tasks."""
        endpoint = parameters.get("endpoint", "")
        method = parameters.get("method", "GET")
        
        # Simulate API calls (in real implementation, make actual calls)
        return {
            "endpoint": endpoint,
            "method": method,
            "status_code": 200,
            "response_time": 0.5,
            "data_received": True
        }
    
    async def _execute_generic_action(self, action_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute generic actions."""
        return {
            "action_type": action_type,
            "parameters": parameters,
            "status": "completed",
            "message": f"Successfully executed {action_type} action"
        }
    
    def _generate_python_code(self, purpose: str, specifications: Dict[str, Any]) -> str:
        """Generate Python code for specified purpose."""
        if purpose == "data_analysis":
            return """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def analyze_data(data_file):
    # Load and analyze data
    df = pd.read_csv(data_file)
    
    # Basic statistics
    summary = df.describe()
    
    # Visualizations
    plt.figure(figsize=(10, 6))
    df.hist()
    plt.title('Data Distribution')
    plt.show()
    
    return summary

# Example usage
# result = analyze_data('data.csv')"""
        
        elif purpose == "web_scraping":
            return """import requests
from bs4 import BeautifulSoup
import json

def scrape_website(url):
    # Fetch webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract data
    data = []
    for element in soup.find_all('div', class_='content'):
        data.append({
            'title': element.find('h2').text if element.find('h2') else '',
            'content': element.get_text().strip()
        })
    
    return data

# Example usage
# scraped_data = scrape_website('https://example.com')"""
        
        else:
            function_name = specifications.get("function_name", "process_data")
            return f"""def {function_name}():
    # Generated function for {purpose}
    result = "Processing completed successfully"
    return result

# Example usage
# output = {function_name}()
print(output)"""
    
    def _generate_javascript_code(self, purpose: str, specifications: Dict[str, Any]) -> str:
        """Generate JavaScript code for specified purpose."""
        if purpose == "web_interaction":
            return """// Web interaction functionality
function handleUserInteraction() {
    document.addEventListener('DOMContentLoaded', function() {
        const buttons = document.querySelectorAll('.interactive-button');
        
        buttons.forEach(button => {
            button.addEventListener('click', function() {
                console.log('Button clicked:', this.textContent);
                // Add interaction logic here
            });
        });
    });
}

// Initialize interactions
handleUserInteraction();"""
        
        else:
            function_name = specifications.get("function_name", "processData")
            return f"""function {function_name}() {{
    // Generated function for {purpose}
    console.log('Processing {purpose}...');
    return 'Processing completed successfully';
}}

// Example usage
const result = {function_name}();
console.log(result);"""
    
    def _generate_generic_code(self, language: str, purpose: str, specifications: Dict[str, Any]) -> str:
        """Generate generic code for any language."""
        return f"""// Generated {language} code for {purpose}
// This is a placeholder implementation
// Customize based on specific requirements

function main() {{
    // Implementation for {purpose}
    return "Task completed successfully";
}}

main();"""
    
    def _assess_code_quality(self, code: str) -> float:
        """Assess the quality of generated code."""
        lines = code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        # Simple quality metrics
        has_comments = any('//' in line or '#' in line for line in lines)
        has_functions = any('def ' in line or 'function ' in line for line in lines)
        reasonable_length = 10 <= len(non_empty_lines) <= 100
        
        quality_score = 0.5  # Base score
        if has_comments:
            quality_score += 0.2
        if has_functions:
            quality_score += 0.2
        if reasonable_length:
            quality_score += 0.1
        
        return min(1.0, quality_score)
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get the execution history for this agent."""
        return self.execution_history.copy()
    
    def get_capability_utilization(self) -> Dict[str, int]:
        """Get utilization statistics for each capability."""
        utilization = {cap: 0 for cap in self.execution_capabilities}
        
        for execution in self.execution_history:
            action_type = execution.get("result", {}).get("action_type", "general")
            if action_type in utilization:
                utilization[action_type] += 1
        
        return utilization


class CoordinatorAgent(AIAgent):
    """Agent specialized in workflow coordination and orchestration."""
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        orchestrator: Optional['WorkflowOrchestrator'] = None
    ):
        capabilities = [
            AgentCapability(
                capability_type=TaskType.WORKFLOW_COORDINATION,
                proficiency_level=0.95,
                max_concurrent_tasks=10,
                specialization_tags=["coordination", "orchestration", "management"]
            ),
            AgentCapability(
                capability_type=TaskType.PROBLEM_SOLVING,
                proficiency_level=0.85,
                max_concurrent_tasks=3,
                specialization_tags=["workflow_optimization", "task_delegation"]
            )
        ]
        
        super().__init__(agent_id, AgentType.COORDINATOR, name, capabilities)
        self.orchestrator = orchestrator
        self.coordination_history: List[Dict[str, Any]] = []
    
    async def execute_task(self, task: WorkflowTask) -> Any:
        """Execute coordination and management tasks."""
        await self.start_task(task)
        
        try:
            if task.task_type == TaskType.WORKFLOW_COORDINATION:
                result = await self._handle_workflow_coordination(task)
            elif task.task_type == TaskType.PROBLEM_SOLVING:
                result = await self._handle_coordination_problem_solving(task)
            else:
                raise ValueError(f"Unsupported task type: {task.task_type}")
            
            await self.complete_task(task, result)
            return result
            
        except Exception as e:
            await self.fail_task(task, str(e))
            raise
    
    async def can_handle_task(self, task: WorkflowTask) -> float:
        """Assess ability to handle coordination tasks."""
        base_score = self.get_capability_score(task.task_type)
        availability = self.get_availability_score()
        
        # High bonus for coordination keywords
        coordination_bonus = 0.0
        coordination_keywords = ["coordinate", "manage", "orchestrate", "delegate", "organize"]
        if any(keyword in task.description.lower() for keyword in coordination_keywords):
            coordination_bonus = 0.25
        
        return min(1.0, base_score * availability + coordination_bonus)
    
    async def _handle_workflow_coordination(self, task: WorkflowTask) -> Dict[str, Any]:
        """Handle workflow coordination tasks."""
        workflow_id = task.requirements.get("workflow_id", "")
        coordination_type = task.requirements.get("coordination_type", "general")
        target_agents = task.requirements.get("target_agents", [])
        
        coordination_result = {
            "workflow_id": workflow_id,
            "coordination_type": coordination_type,
            "target_agents": target_agents,
            "coordination_status": "completed",
            "actions_taken": [],
            "recommendations": []
        }
        
        # Perform coordination based on type
        if coordination_type == "load_balancing":
            actions = await self._coordinate_load_balancing(target_agents)
            coordination_result["actions_taken"] = actions
        elif coordination_type == "task_optimization":
            recommendations = await self._optimize_task_distribution(workflow_id)
            coordination_result["recommendations"] = recommendations
        elif coordination_type == "agent_monitoring":
            monitoring_data = await self._monitor_agent_performance(target_agents)
            coordination_result["monitoring_data"] = monitoring_data
        else:
            coordination_result["actions_taken"] = ["General coordination performed"]
        
        # Record coordination history
        self.coordination_history.append({
            "task_id": task.task_id,
            "coordination_type": coordination_type,
            "timestamp": datetime.now(timezone.utc),
            "result": coordination_result
        })
        
        return coordination_result
    
    async def _handle_coordination_problem_solving(self, task: WorkflowTask) -> Dict[str, Any]:
        """Handle coordination-related problem solving."""
        problem_type = task.requirements.get("problem_type", "workflow_issue")
        problem_details = task.requirements.get("problem_details", {})
        
        # Analyze and solve coordination problems
        solutions = []
        if problem_type == "workflow_bottleneck":
            solutions = await self._solve_workflow_bottleneck(problem_details)
        elif problem_type == "agent_failure":
            solutions = await self._solve_agent_failure(problem_details)
        elif problem_type == "resource_contention":
            solutions = await self._solve_resource_contention(problem_details)
        else:
            solutions = await self._solve_general_coordination_problem(problem_details)
        
        return {
            "problem_type": problem_type,
            "problem_details": problem_details,
            "solutions": solutions,
            "solution_count": len(solutions),
            "priority_solution": solutions[0] if solutions else None
        }
    
    async def _coordinate_load_balancing(self, target_agents: List[str]) -> List[str]:
        """Coordinate load balancing across agents."""
        actions = []
        
        if self.orchestrator:
            # Get agent status
            agent_status = self.orchestrator.get_agent_status()
            
            # Identify overloaded and underloaded agents
            overloaded = []
            underloaded = []
            
            for agent_id in target_agents:
                if agent_id in agent_status:
                    status = agent_status[agent_id]
                    if status["availability_score"] < 0.3:
                        overloaded.append(agent_id)
                    elif status["availability_score"] > 0.8:
                        underloaded.append(agent_id)
            
            # Generate load balancing actions
            if overloaded and underloaded:
                actions.append(f"Redistribute tasks from {len(overloaded)} overloaded to {len(underloaded)} underloaded agents")
                actions.append("Implement task queue management for better distribution")
            elif overloaded:
                actions.append(f"Scale up resources for {len(overloaded)} overloaded agents")
            else:
                actions.append("Load distribution optimal - no action required")
        
        return actions
    
    async def _optimize_task_distribution(self, workflow_id: str) -> List[str]:
        """Optimize task distribution for a workflow."""
        recommendations = [
            "Analyze agent capabilities vs task requirements",
            "Implement priority-based task assignment",
            "Consider agent performance history in assignment decisions",
            "Balance workload across available agents",
            "Monitor and adjust distribution based on real-time performance"
        ]
        
        return recommendations
    
    async def _monitor_agent_performance(self, target_agents: List[str]) -> Dict[str, Any]:
        """Monitor performance of target agents."""
        monitoring_data = {
            "monitored_agents": len(target_agents),
            "monitoring_timestamp": datetime.now(timezone.utc).isoformat(),
            "performance_summary": {},
            "alerts": []
        }
        
        if self.orchestrator:
            agent_status = self.orchestrator.get_agent_status()
            
            for agent_id in target_agents:
                if agent_id in agent_status:
                    status = agent_status[agent_id]
                    monitoring_data["performance_summary"][agent_id] = {
                        "availability": status["availability_score"],
                        "success_rate": status["success_rate"],
                        "current_load": status["current_tasks"]
                    }
                    
                    # Generate alerts for concerning metrics
                    if status["success_rate"] < 0.8:
                        monitoring_data["alerts"].append(f"Low success rate for agent {agent_id}")
                    if status["availability_score"] < 0.2:
                        monitoring_data["alerts"].append(f"Agent {agent_id} overloaded")
        
        return monitoring_data
    
    async def _solve_workflow_bottleneck(self, problem_details: Dict[str, Any]) -> List[Dict[str, str]]:
        """Solve workflow bottleneck problems."""
        return [
            {
                "solution": "Parallel Task Execution",
                "description": "Execute independent tasks in parallel to reduce bottleneck",
                "implementation": "Identify parallelizable tasks and modify workflow structure"
            },
            {
                "solution": "Agent Scaling",
                "description": "Add more agents to handle bottleneck tasks",
                "implementation": "Deploy additional agents with required capabilities"
            },
            {
                "solution": "Task Optimization",
                "description": "Optimize bottleneck tasks for better performance",
                "implementation": "Review and refactor task execution logic"
            }
        ]
    
    async def _solve_agent_failure(self, problem_details: Dict[str, Any]) -> List[Dict[str, str]]:
        """Solve agent failure problems."""
        return [
            {
                "solution": "Failover to Backup Agent",
                "description": "Redirect tasks to available backup agents",
                "implementation": "Implement automatic failover mechanism"
            },
            {
                "solution": "Task Redistribution",
                "description": "Redistribute failed agent's tasks to other agents",
                "implementation": "Load balance tasks across remaining active agents"
            },
            {
                "solution": "Agent Recovery",
                "description": "Attempt to recover the failed agent",
                "implementation": "Diagnose failure cause and restart agent if possible"
            }
        ]
    
    async def _solve_resource_contention(self, problem_details: Dict[str, Any]) -> List[Dict[str, str]]:
        """Solve resource contention problems."""
        return [
            {
                "solution": "Resource Queuing",
                "description": "Implement queue system for shared resources",
                "implementation": "Add resource management layer with queuing"
            },
            {
                "solution": "Resource Scaling",
                "description": "Scale up contested resources",
                "implementation": "Provision additional resource instances"
            },
            {
                "solution": "Access Optimization",
                "description": "Optimize resource access patterns",
                "implementation": "Batch operations and cache frequently accessed resources"
            }
        ]
    
    async def _solve_general_coordination_problem(self, problem_details: Dict[str, Any]) -> List[Dict[str, str]]:
        """Solve general coordination problems."""
        return [
            {
                "solution": "Communication Enhancement",
                "description": "Improve inter-agent communication protocols",
                "implementation": "Implement robust messaging and status sharing"
            },
            {
                "solution": "Monitoring Improvement",
                "description": "Enhance monitoring and alerting systems",
                "implementation": "Add comprehensive performance and health monitoring"
            }
        ]
    
    def get_coordination_history(self) -> List[Dict[str, Any]]:
        """Get coordination history for this agent."""
        return self.coordination_history.copy()


class WorkflowOrchestrator:
    """Main orchestrator for managing multi-agent workflows."""
    
    def __init__(self):
        self.agents = {}
        self.workflows = {}
        self.task_queue = []
        self.completed_tasks = []
        self.performance_metrics = {}
        self.logger = logging.getLogger(__name__)
    
    def register_agent(self, agent: AIAgent) -> None:
        """Register an agent with the orchestrator."""
        self.agents[agent.agent_id] = agent
        self.performance_metrics[agent.agent_id] = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "total_execution_time": 0.0,
            "average_execution_time": 0.0
        }
        self.logger.info(f"Registered agent: {agent.name} ({agent.agent_id})")
    
    def unregister_agent(self, agent_id: str) -> None:
        """Unregister an agent from the orchestrator."""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            del self.agents[agent_id]
            del self.performance_metrics[agent_id]
            self.logger.info(f"Unregistered agent: {agent.name} ({agent_id})")
    
    async def create_workflow(
        self,
        workflow_id: str,
        tasks: List[WorkflowTask],
        execution_strategy: str = "sequential"
    ) -> 'Workflow':
        """Create a new workflow."""
        workflow = Workflow(workflow_id, tasks, execution_strategy, self)
        self.workflows[workflow_id] = workflow
        self.logger.info(f"Created workflow: {workflow_id} with {len(tasks)} tasks")
        return workflow
    
    async def assign_task(self, task: WorkflowTask) -> Optional[AIAgent]:
        """Assign a task to the most suitable agent."""
        best_agent = None
        best_score = 0.0
        
        for agent in self.agents.values():
            if agent.status == AgentStatus.AVAILABLE:
                try:
                    score = await agent.can_handle_task(task)
                    if score > best_score:
                        best_score = score
                        best_agent = agent
                except Exception as e:
                    self.logger.warning(f"Error evaluating agent {agent.agent_id} for task: {e}")
        
        if best_agent and best_score > 0.5:  # Minimum score threshold
            self.logger.info(f"Assigned task {task.task_id} to agent {best_agent.agent_id} (score: {best_score:.2f})")
            return best_agent
        
        self.logger.warning(f"No suitable agent found for task {task.task_id}")
        return None
    
    async def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Execute a workflow and return results."""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.workflows[workflow_id]
        self.logger.info(f"Starting execution of workflow: {workflow_id}")
        
        try:
            results = await workflow.execute()
            self.logger.info(f"Completed workflow: {workflow_id}")
            return results
        except Exception as e:
            self.logger.error(f"Workflow {workflow_id} failed: {e}")
            raise
    
    def get_agent_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status information for all agents."""
        status = {}
        for agent_id, agent in self.agents.items():
            metrics = self.performance_metrics[agent_id]
            status[agent_id] = {
                "name": agent.name,
                "type": agent.agent_type.value,
                "status": agent.status.value,
                "current_tasks": len(agent.current_tasks),
                "availability_score": agent.get_availability_score(),
                "success_rate": self._calculate_success_rate(agent_id),
                "average_execution_time": metrics["average_execution_time"]
            }
        return status
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get status information for a workflow."""
        if workflow_id not in self.workflows:
            return {"error": f"Workflow {workflow_id} not found"}
        
        workflow = self.workflows[workflow_id]
        return workflow.get_status()
    
    def _calculate_success_rate(self, agent_id: str) -> float:
        """Calculate success rate for an agent."""
        metrics = self.performance_metrics[agent_id]
        total_tasks = metrics["tasks_completed"] + metrics["tasks_failed"]
        if total_tasks == 0:
            return 1.0
        return metrics["tasks_completed"] / total_tasks
    
    def _update_agent_metrics(self, agent_id: str, execution_time: float, success: bool) -> None:
        """Update performance metrics for an agent."""
        if agent_id in self.performance_metrics:
            metrics = self.performance_metrics[agent_id]
            if success:
                metrics["tasks_completed"] += 1
            else:
                metrics["tasks_failed"] += 1
            
            metrics["total_execution_time"] += execution_time
            total_tasks = metrics["tasks_completed"] + metrics["tasks_failed"]
            metrics["average_execution_time"] = metrics["total_execution_time"] / total_tasks


class Workflow:
    """Represents a workflow consisting of multiple tasks."""
    
    def __init__(
        self,
        workflow_id: str,
        tasks: List[WorkflowTask],
        execution_strategy: str = "sequential",
        orchestrator = None
    ):
        self.workflow_id = workflow_id
        self.tasks = tasks
        self.execution_strategy = execution_strategy
        self.orchestrator = orchestrator
        self.status = TaskStatus.PENDING
        self.start_time = None
        self.end_time = None
        self.results = {}
        self.logger = logging.getLogger(__name__)
    
    async def execute(self) -> Dict[str, Any]:
        """Execute the workflow according to the specified strategy."""
        self.status = TaskStatus.IN_PROGRESS
        self.start_time = datetime.now(timezone.utc)
        self.logger.info(f"Starting workflow {self.workflow_id} with {self.execution_strategy} execution")
        
        try:
            if self.execution_strategy == "sequential":
                results = await self._execute_sequential()
            elif self.execution_strategy == "parallel":
                results = await self._execute_parallel()
            elif self.execution_strategy == "conditional":
                results = await self._execute_conditional()
            else:
                raise ValueError(f"Unknown execution strategy: {self.execution_strategy}")
            
            self.status = TaskStatus.COMPLETED
            self.end_time = datetime.now(timezone.utc)
            self.results = results
            
            return {
                "workflow_id": self.workflow_id,
                "status": self.status.value,
                "execution_time": (self.end_time - self.start_time).total_seconds(),
                "results": results
            }
            
        except Exception as e:
            self.status = TaskStatus.FAILED
            self.end_time = datetime.now(timezone.utc)
            self.logger.error(f"Workflow {self.workflow_id} failed: {e}")
            raise
    
    async def _execute_sequential(self) -> Dict[str, Any]:
        """Execute tasks sequentially."""
        results = {}
        
        for task in self.tasks:
            self.logger.info(f"Executing task {task.task_id} sequentially")
            
            # Assign and execute task
            agent = await self.orchestrator.assign_task(task)
            if agent:
                try:
                    start_time = datetime.now(timezone.utc)
                    result = await agent.execute_task(task)
                    end_time = datetime.now(timezone.utc)
                    
                    execution_time = (end_time - start_time).total_seconds()
                    self.orchestrator._update_agent_metrics(agent.agent_id, execution_time, True)
                    
                    results[task.task_id] = result
                    self.logger.info(f"Task {task.task_id} completed successfully")
                    
                except Exception as e:
                    execution_time = (datetime.now(timezone.utc) - start_time).total_seconds()
                    self.orchestrator._update_agent_metrics(agent.agent_id, execution_time, False)
                    
                    self.logger.error(f"Task {task.task_id} failed: {e}")
                    results[task.task_id] = {"error": str(e)}
            else:
                self.logger.error(f"No agent available for task {task.task_id}")
                results[task.task_id] = {"error": "No suitable agent found"}
        
        return results
    
    async def _execute_parallel(self) -> Dict[str, Any]:
        """Execute tasks in parallel."""
        async def execute_single_task(task: WorkflowTask) -> tuple:
            self.logger.info(f"Executing task {task.task_id} in parallel")
            
            agent = await self.orchestrator.assign_task(task)
            if agent:
                try:
                    start_time = datetime.now(timezone.utc)
                    result = await agent.execute_task(task)
                    end_time = datetime.now(timezone.utc)
                    
                    execution_time = (end_time - start_time).total_seconds()
                    self.orchestrator._update_agent_metrics(agent.agent_id, execution_time, True)
                    
                    return task.task_id, result
                    
                except Exception as e:
                    execution_time = (datetime.now(timezone.utc) - start_time).total_seconds()
                    self.orchestrator._update_agent_metrics(agent.agent_id, execution_time, False)
                    
                    self.logger.error(f"Task {task.task_id} failed: {e}")
                    return task.task_id, {"error": str(e)}
            else:
                self.logger.error(f"No agent available for task {task.task_id}")
                return task.task_id, {"error": "No suitable agent found"}
        
        # Execute all tasks concurrently
        task_coroutines = [execute_single_task(task) for task in self.tasks]
        task_results = await asyncio.gather(*task_coroutines, return_exceptions=True)
        
        # Organize results
        results = {}
        for result in task_results:
            if isinstance(result, Exception):
                self.logger.error(f"Task execution failed with exception: {result}")
                results["unknown"] = {"error": str(result)}
            else:
                task_id, task_result = result
                results[task_id] = task_result
        
        return results
    
    async def _execute_conditional(self) -> Dict[str, Any]:
        """Execute tasks based on conditional logic."""
        results = {}
        
        for task in self.tasks:
            # Check if task should be executed based on conditions
            should_execute = self._evaluate_task_conditions(task, results)
            
            if should_execute:
                self.logger.info(f"Executing conditional task {task.task_id}")
                
                agent = await self.orchestrator.assign_task(task)
                if agent:
                    try:
                        start_time = datetime.now(timezone.utc)
                        result = await agent.execute_task(task)
                        end_time = datetime.now(timezone.utc)
                        
                        execution_time = (end_time - start_time).total_seconds()
                        self.orchestrator._update_agent_metrics(agent.agent_id, execution_time, True)
                        
                        results[task.task_id] = result
                        self.logger.info(f"Conditional task {task.task_id} completed")
                        
                    except Exception as e:
                        execution_time = (datetime.now(timezone.utc) - start_time).total_seconds()
                        self.orchestrator._update_agent_metrics(agent.agent_id, execution_time, False)
                        
                        self.logger.error(f"Conditional task {task.task_id} failed: {e}")
                        results[task.task_id] = {"error": str(e)}
                else:
                    self.logger.error(f"No agent available for conditional task {task.task_id}")
                    results[task.task_id] = {"error": "No suitable agent found"}
            else:
                self.logger.info(f"Skipping conditional task {task.task_id} (conditions not met)")
                results[task.task_id] = {"status": "skipped", "reason": "conditions not met"}
        
        return results
    
    def _evaluate_task_conditions(self, task: WorkflowTask, previous_results: Dict[str, Any]) -> bool:
        """Evaluate whether a task should be executed based on conditions."""
        conditions = task.requirements.get("conditions", [])
        
        if not conditions:
            return True  # No conditions means always execute
        
        for condition in conditions:
            condition_type = condition.get("type", "")
            
            if condition_type == "task_success":
                required_task = condition.get("task_id", "")
                if required_task in previous_results:
                    result = previous_results[required_task]
                    if "error" in result:
                        return False
                else:
                    return False
            
            elif condition_type == "task_result":
                required_task = condition.get("task_id", "")
                expected_value = condition.get("value", "")
                result_path = condition.get("path", "")
                
                if required_task in previous_results:
                    result = previous_results[required_task]
                    if result_path:
                        # Navigate to specific path in result
                        value = result
                        for key in result_path.split("."):
                            if isinstance(value, dict) and key in value:
                                value = value[key]
                            else:
                                return False
                        
                        if value != expected_value:
                            return False
                    else:
                        return False
                else:
                    return False
        
        return True
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the workflow."""
        return {
            "workflow_id": self.workflow_id,
            "status": self.status.value,
            "execution_strategy": self.execution_strategy,
            "total_tasks": len(self.tasks),
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "execution_time": (
                (self.end_time - self.start_time).total_seconds() 
                if self.start_time and self.end_time 
                else None
            )
        }
    """Main orchestrator for managing multi-agent workflows."""
    
    def __init__(self):
        self.agents: Dict[str, AIAgent] = {}
        self.workflows: Dict[str, 'Workflow'] = {}
        self.task_queue: List[WorkflowTask] = []
        self.completed_tasks: List[WorkflowTask] = []
        self.orchestration_stats = {
            "total_workflows": 0,
            "completed_workflows": 0,
            "total_tasks": 0,
            "completed_tasks": 0,
            "average_workflow_time": 0.0
        }
        
        logger.info("Initialized WorkflowOrchestrator")
    
    def register_agent(self, agent: AIAgent) -> None:
        """Register an agent with the orchestrator."""
        self.agents[agent.agent_id] = agent
        logger.info(f"Registered agent: {agent.name} ({agent.agent_type.value})")
    
    def unregister_agent(self, agent_id: str) -> None:
        """Unregister an agent from the orchestrator."""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            del self.agents[agent_id]
            logger.info(f"Unregistered agent: {agent.name}")
    
    async def create_workflow(
        self,
        workflow_id: str,
        tasks: List[WorkflowTask],
        workflow_type: str = "parallel"
    ) -> 'Workflow':
        """Create a new workflow with the given tasks."""
        workflow = Workflow(
            workflow_id=workflow_id,
            tasks=tasks,
            workflow_type=workflow_type,
            orchestrator=self
        )
        
        self.workflows[workflow_id] = workflow
        self.orchestration_stats["total_workflows"] += 1
        self.orchestration_stats["total_tasks"] += len(tasks)
        
        logger.info(f"Created workflow: {workflow_id} with {len(tasks)} tasks")
        return workflow
    
    async def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Execute a workflow and return results."""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.workflows[workflow_id]
        start_time = datetime.now(timezone.utc)
        
        try:
            results = await workflow.execute()
            
            # Update statistics
            completion_time = datetime.now(timezone.utc)
            duration = (completion_time - start_time).total_seconds()
            
            self.orchestration_stats["completed_workflows"] += 1
            self.orchestration_stats["completed_tasks"] += len([t for t in workflow.tasks if t.status == TaskStatus.COMPLETED])
            
            # Update average workflow time
            total_completed = self.orchestration_stats["completed_workflows"]
            if total_completed == 1:
                self.orchestration_stats["average_workflow_time"] = duration
            else:
                current_avg = self.orchestration_stats["average_workflow_time"]
                self.orchestration_stats["average_workflow_time"] = (
                    (current_avg * (total_completed - 1) + duration) / total_completed
                )
            
            logger.info(f"Completed workflow: {workflow_id} in {duration:.2f} seconds")
            return results
            
        except Exception as e:
            logger.error(f"Workflow {workflow_id} failed: {e}")
            raise
    
    async def assign_task_to_best_agent(self, task: WorkflowTask) -> Optional[AIAgent]:
        """Find and assign the best available agent for a task."""
        best_agent = None
        best_score = 0.0
        
        for agent in self.agents.values():
            if not agent.is_active:
                continue
            
            try:
                score = await agent.can_handle_task(task)
                if score > best_score:
                    best_score = score
                    best_agent = agent
            except Exception as e:
                logger.warning(f"Error evaluating agent {agent.name} for task: {e}")
        
        if best_agent and best_score > 0.5:  # Minimum threshold
            task.assigned_agent_id = best_agent.agent_id
            task.status = TaskStatus.ASSIGNED
            logger.info(f"Assigned task {task.task_id} to agent {best_agent.name} (score: {best_score:.3f})")
            return best_agent
        
        logger.warning(f"No suitable agent found for task {task.task_id}")
        return None
    
    def get_agent_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all registered agents."""
        status = {}
        for agent_id, agent in self.agents.items():
            status[agent_id] = {
                "name": agent.name,
                "type": agent.agent_type.value,
                "active": agent.is_active,
                "current_tasks": len(agent.current_tasks),
                "availability_score": agent.get_availability_score(),
                "success_rate": agent.metrics.success_rate,
                "total_completed": agent.metrics.total_tasks_completed,
                "total_failed": agent.metrics.total_tasks_failed,
                "average_completion_time": agent.metrics.average_completion_time
            }
        return status
    
    def get_orchestration_stats(self) -> Dict[str, Any]:
        """Get overall orchestration statistics."""
        return {
            **self.orchestration_stats,
            "active_agents": len([a for a in self.agents.values() if a.is_active]),
            "total_agents": len(self.agents),
            "active_workflows": len([w for w in self.workflows.values() if not w.is_completed]),
            "total_workflows": len(self.workflows)
        }


class Workflow:
    """Represents a workflow consisting of multiple tasks."""
    
    def __init__(
        self,
        workflow_id: str,
        tasks: List[WorkflowTask],
        workflow_type: str = "parallel",
        orchestrator: WorkflowOrchestrator = None
    ):
        self.workflow_id = workflow_id
        self.tasks = tasks
        self.workflow_type = workflow_type  # "parallel", "sequential", "conditional"
        self.orchestrator = orchestrator
        self.start_time: Optional[datetime] = None
        self.completion_time: Optional[datetime] = None
        self.is_completed = False
        self.results: Dict[str, Any] = {}
    
    async def execute(self) -> Dict[str, Any]:
        """Execute the workflow based on its type."""
        self.start_time = datetime.now(timezone.utc)
        
        try:
            if self.workflow_type == "parallel":
                results = await self._execute_parallel()
            elif self.workflow_type == "sequential":
                results = await self._execute_sequential()
            elif self.workflow_type == "conditional":
                results = await self._execute_conditional()
            else:
                raise ValueError(f"Unsupported workflow type: {self.workflow_type}")
            
            self.completion_time = datetime.now(timezone.utc)
            self.is_completed = True
            self.results = results
            
            return results
            
        except Exception as e:
            logger.error(f"Workflow {self.workflow_id} execution failed: {e}")
            raise
    
    async def _execute_parallel(self) -> Dict[str, Any]:
        """Execute all tasks in parallel."""
        # Assign tasks to agents
        task_agent_pairs = []
        for task in self.tasks:
            agent = await self.orchestrator.assign_task_to_best_agent(task)
            if agent:
                task_agent_pairs.append((task, agent))
            else:
                task.status = TaskStatus.FAILED
                task.error_message = "No suitable agent available"
        
        # Execute tasks concurrently
        async def execute_task_with_agent(task: WorkflowTask, agent: AIAgent):
            try:
                return await agent.execute_task(task)
            except Exception as e:
                logger.error(f"Task {task.task_id} failed: {e}")
                return None
        
        # Run all tasks concurrently
        task_results = await asyncio.gather(
            *[execute_task_with_agent(task, agent) for task, agent in task_agent_pairs],
            return_exceptions=True
        )
        
        # Collect results
        results = {}
        for i, (task, agent) in enumerate(task_agent_pairs):
            result = task_results[i] if i < len(task_results) else None
            results[task.task_id] = {
                "task_description": task.description,
                "status": task.status.value,
                "result": result,
                "agent": agent.name,
                "error": task.error_message
            }
        
        return results
    
    async def _execute_sequential(self) -> Dict[str, Any]:
        """Execute tasks in sequence."""
        results = {}
        
        for task in self.tasks:
            # Check dependencies
            if not self._dependencies_satisfied(task, results):
                task.status = TaskStatus.WAITING_DEPENDENCIES
                logger.warning(f"Task {task.task_id} waiting for dependencies")
                continue
            
            # Assign and execute task
            agent = await self.orchestrator.assign_task_to_best_agent(task)
            if agent:
                try:
                    result = await agent.execute_task(task)
                    results[task.task_id] = {
                        "task_description": task.description,
                        "status": task.status.value,
                        "result": result,
                        "agent": agent.name
                    }
                except Exception as e:
                    logger.error(f"Sequential task {task.task_id} failed: {e}")
                    results[task.task_id] = {
                        "task_description": task.description,
                        "status": TaskStatus.FAILED.value,
                        "result": None,
                        "agent": agent.name,
                        "error": str(e)
                    }
            else:
                task.status = TaskStatus.FAILED
                task.error_message = "No suitable agent available"
                results[task.task_id] = {
                    "task_description": task.description,
                    "status": TaskStatus.FAILED.value,
                    "result": None,
                    "agent": None,
                    "error": "No suitable agent available"
                }
        
        return results
    
    async def _execute_conditional(self) -> Dict[str, Any]:
        """Execute tasks based on conditional logic."""
        # For now, implement as sequential with dependency checking
        return await self._execute_sequential()
    
    def _dependencies_satisfied(self, task: WorkflowTask, completed_results: Dict[str, Any]) -> bool:
        """Check if all dependencies for a task are satisfied."""
        for dep_task_id in task.dependencies:
            if dep_task_id not in completed_results:
                return False
            
            dep_result = completed_results[dep_task_id]
            if dep_result["status"] != TaskStatus.COMPLETED.value:
                return False
        
        return True
    
    def get_workflow_summary(self) -> Dict[str, Any]:
        """Get a summary of the workflow execution."""
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks if t.status == TaskStatus.COMPLETED])
        failed_tasks = len([t for t in self.tasks if t.status == TaskStatus.FAILED])
        
        duration = None
        if self.start_time and self.completion_time:
            duration = (self.completion_time - self.start_time).total_seconds()
        
        return {
            "workflow_id": self.workflow_id,
            "workflow_type": self.workflow_type,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "success_rate": completed_tasks / total_tasks if total_tasks > 0 else 0,
            "duration_seconds": duration,
            "is_completed": self.is_completed,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "completion_time": self.completion_time.isoformat() if self.completion_time else None
        }