
# ENTAERA Kata - Day 11: Agent Orchestration & Workflows

## 🎯 Learning Objectives

Complex problems often require multiple specialized agents working together. Today, you will learn how to orchestrate a team of AI agents, assigning them tasks and managing their collaboration in a structured workflow.

- **Design a base `AIAgent` class with a common interface.**
- **Create specialized agents (e.g., `PlannerAgent`, `CodeWriterAgent`) that inherit from the base class.**
- **Model a `WorkflowTask` that defines a piece of work to be done.**
- **Build an `Orchestrator` that manages a sequence of tasks and delegates them to the appropriate agents.**
- **Understand how a multi-agent system can break down and solve a complex problem.**

---

## 🧠 For the Absolute Beginner

### What is a Multi-Agent System?
Imagine you're building a house. You don't hire one person to do everything. You hire a team of specialists: an architect to draw the plans, a builder to construct the frame, an electrician for the wiring, and a plumber for the pipes. A **multi-agent system** is the same idea for software. Instead of one giant, monolithic AI trying to do everything, we create a team of smaller, specialized AI **agents**. Each agent has a specific role and set of skills.

### What is an Orchestrator?
The **orchestrator** is the general contractor for our house-building project. It doesn't lay bricks or install wires itself. Its job is to manage the workflow:
1.  It reads the main goal ("build a house").
2.  It gives the first task to the architect ("create a blueprint").
3.  It takes the output (the blueprint) and gives it to the builder ("build the frame based on this blueprint").
4.  It continues this process, passing the output of one specialist to the next, until the project is complete.

---

## 📚 Theory & Links

Before you begin, study the implementation in:
- `src/entaera/core/agent_orchestration.py`

Key concepts to focus on:
- **Agent-Based Architecture**: A system composed of autonomous agents that have specific roles and capabilities.
- **Orchestration vs. Choreography**: We are building an *orchestrator*—a central controller that directs the agents. In *choreography*, agents communicate with each other directly without a central controller.
- **Task Decomposition**: The process of breaking a large, complex problem into smaller, manageable tasks that can be assigned to specialized agents.
- **State Passing**: How the output of one task becomes the input for the next task in the workflow.
- **Polymorphism**: The orchestrator can treat all agents the same way through the base `AIAgent` interface, even though their concrete implementations are different.

---

## � Project-Level Deep Dive: Advanced Concepts

### Dynamic Workflows and Graph Execution
The linear workflow in our kata is a simple starting point. Real-world problems are often more complex and can be represented as a **Directed Acyclic Graph (DAG)**. In a DAG, a task can have multiple dependencies, and tasks that don't depend on each other can be run in parallel. The orchestrator becomes a "graph execution engine." It starts with the nodes that have no dependencies, executes them, and then moves on to the next set of nodes whose dependencies have been met. Frameworks like **Apache Airflow** (for data engineering) and **LangGraph** (for LLM agents) are built around this concept.

### Hierarchical Agent Teams
For very complex problems, you can have teams of agents. A high-level "manager" agent might be responsible for decomposing a problem. It then delegates the sub-tasks to a team of "worker" agents. There might even be a "reviewer" agent that checks the work of the worker agents before the result is sent back to the manager. This hierarchical structure mirrors how human organizations solve large-scale problems.

### Collaborative Agents and Shared State
In our simple workflow, state is just passed from one agent to the next. In more advanced systems, agents might need to collaborate in real-time. This requires a shared "scratchpad" or blackboard where agents can post intermediate results, ask questions, and build upon each other's work. The orchestrator's role shifts from a simple director to a facilitator of this collaborative space, ensuring agents don't overwrite each other's work and that the shared state remains consistent.

---

## �💻 Exercises

Create a new Python file named `katas/day11_practice.py` and complete the following exercises.

### Exercise 1: The `AIAgent` Interface

1.  Using the `abc` module, create an abstract base class called `AIAgent`.
2.  It should have one abstract method: `execute(self, task_description: str, context: dict) -> str`.
3.  Create two simple, specialized agents that inherit from `AIAgent`:
    - `PlannerAgent`: Its `execute` method should return a simulated plan, e.g., `f"Plan for '{task_description}': [Step 1, Step 2, Step 3]"`.
    - `CodeWriterAgent`: Its `execute` method should return simulated code, e.g., `f"# Code for '{task_description}'\nprint('Hello, World!')"`.

### Exercise 2: The `WorkflowTask` Model

1.  Using Pydantic or a `dataclass`, create a model called `WorkflowTask`.
2.  It should have the following fields:
    - `task_id: int`
    - `description: str`
    - `agent_role: str` (e.g., 'planner', 'coder')
    - `input_data: dict = field(default_factory=dict)`
    - `output: str = ""`
    - `is_complete: bool = False`

### Exercise 3: The `Orchestrator`

1.  Create a class `Orchestrator`.
2.  In `__init__`, it should create and store a dictionary of available agents, mapping roles to agent instances:
    ```python
    self.agents = {
        'planner': PlannerAgent(),
        'coder': CodeWriterAgent()
    }
    ```
3.  Create a method `run_workflow(self, tasks: list[WorkflowTask])`.
4.  This method should loop through the list of tasks:
    - For each task, select the correct agent based on `task.agent_role`.
    - Call the agent's `execute` method, passing the task's description and any input data.
    - Store the result in the task's `output` field and mark it as complete.
    - **Crucially**, for subsequent tasks, pass the output of the *previous* task as part of the `input_data` for the current task.

### Exercise 4: A Simple "Plan and Code" Workflow

1.  Instantiate your `Orchestrator`.
2.  Create a list containing two `WorkflowTask` objects:
    - A task for the `'planner'` agent with the description "Create a plan to write a hello world function."
    - A task for the `'coder'` agent with the description "Write the code based on the plan."
3.  Call the orchestrator's `run_workflow` method with this list of tasks.
4.  After the workflow is complete, print the `output` of each task to see the flow of information from the planner to the coder.

---

## 🤔 Expanded Interview Prep Questions

### Beginner
1.  **What are the advantages of a multi-agent system over a single, monolithic AI model?**
    - *Answer Hint:* **Specialization**: Each agent can be an expert at one thing, leading to higher quality results. **Modularity**: You can update or replace one agent without affecting the others. **Scalability**: Different agents can run in parallel on different machines. **Simplicity**: Each individual agent is simpler to build and debug than one giant "do-everything" agent.
2.  **When would you choose orchestration (a central controller) over choreography (direct peer-to-peer communication) for your agents?**
    - *Answer Hint:* **Orchestration** is better when you have a well-defined, predictable workflow. It's easier to manage, monitor, and debug because everything flows through a central point. **Choreography** is better for more dynamic, event-driven systems where the workflow isn't known in advance and you want the agents to be more autonomous and decoupled.

### Intermediate
3.  **How would you handle a task that fails in the middle of a workflow? What are some possible recovery strategies?**
    - *Answer Hint:* The orchestrator is responsible for error handling. Strategies include: 1) **Retry**: Simply try the failed task again. 2) **Human-in-the-loop**: Pause the workflow and notify a human to fix the problem or make a decision. 3) **Fallback**: Have a backup agent or a simpler strategy to try if the primary one fails. 4) **Compensating Transaction**: For workflows that have side effects (like charging a credit card), you might need to run another task to "undo" the previous steps.
4.  **In this kata, the workflow is a simple linear sequence. How might you modify the `Orchestrator` to support more complex workflows with parallel tasks or conditional branching?**
    - *Answer Hint:* You would need to model the workflow as a graph (a DAG) instead of a list. Each task would declare its dependencies. The orchestrator would then become a graph runner. It would maintain a pool of "ready" tasks (whose dependencies are met) and could execute them in parallel. For conditional branching, a task could output a decision (e.g., "success" or "failure"), and the orchestrator would use that output to decide which branch of the graph to follow next.
5.  **The "context" passed to agents is a simple dictionary. In a real system, what kind of information would you include in this context to help the agent perform its task effectively?**
    - *Answer Hint:* The context should be a rich "briefing document." It would include the overall project goal, the specific task description, the output from previous steps, relevant long-term memories, snippets of relevant files, and any user preferences or constraints.

### Advanced
6.  **What is the "agent reflection" pattern, and how could it be incorporated into a workflow?**
    - *Answer Hint:* Agent reflection is the idea of having an agent critique its own work. After a `CodeWriterAgent` produces some code, you could have a `CodeReviewerAgent` (which might be the same agent with a different prompt) analyze that code for bugs, style issues, or missed requirements. The reviewer's feedback is then passed *back* to the `CodeWriterAgent` to perform a second, improved attempt. This iterative, self-correcting loop can dramatically improve the quality of the final output.
7.  **How do you evaluate the performance of a multi-agent system? What are the challenges?**
    - *Answer Hint:* It's challenging because you need to evaluate both the final outcome and the process. Key metrics include: 1) **Task Success Rate**: Does the system successfully complete the overall goal? 2) **Cost**: How many tokens or API calls were used? 3) **Latency**: How long did it take? 4) **Robustness**: How well does it handle failures or unexpected inputs? The biggest challenge is that the system is non-deterministic; running it twice on the same problem might produce different results, so you need to run many trials to get statistically significant metrics.
