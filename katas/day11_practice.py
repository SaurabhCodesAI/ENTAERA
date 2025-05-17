
# This is your practice file for the Day 11 Kata.
# Complete the exercises from katas/day11_orchestration.md here.

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any

# --- Exercise 1: The AIAgent Interface and Concrete Agents ---

class AIAgent(ABC):
    @abstractmethod
    def execute(self, task_description: str, context: Dict[str, Any]) -> str:
        pass

class PlannerAgent(AIAgent):
    def execute(self, task_description: str, context: Dict[str, Any]) -> str:
        # TODO: Simulate creating a plan
        pass

class CodeWriterAgent(AIAgent):
    def execute(self, task_description: str, context: Dict[str, Any]) -> str:
        # TODO: Simulate writing code
        pass

print("--- Exercise 1 ---")
print("Agent classes defined.")


# --- Exercise 2: The WorkflowTask Model ---

@dataclass
class WorkflowTask:
    # TODO: Define the fields for the task model
    pass

print("\n--- Exercise 2 ---")
print("WorkflowTask class defined.")


# --- Exercise 3: The Orchestrator ---

class Orchestrator:
    def __init__(self):
        # TODO: Initialize the agents dictionary
        pass

    def run_workflow(self, tasks: List[WorkflowTask]) -> List[WorkflowTask]:
        """
        Runs a sequence of tasks, passing the output of one as the input to the next.
        """
        # TODO: Implement the workflow execution logic
        pass

print("\n--- Exercise 3 ---")
print("Orchestrator class defined.")


# --- Exercise 4: A Simple "Plan and Code" Workflow ---

print("\n--- Exercise 4 ---")
# TODO:
# 1. Instantiate the Orchestrator.
# 2. Create a list of two WorkflowTasks (one for planning, one for coding).
# 3. Run the workflow.
# 4. Print the final output of each task to show the result.

