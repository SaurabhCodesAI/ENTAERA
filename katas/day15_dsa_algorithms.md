# ENTAERA Kata - Day 15: Data Structures & Algorithms (FAANG Prep)

## 🎯 Learning Objectives

**This is your FAANG interview preparation**. Master the data structures and algorithms that appear in 90% of Google, Meta, Amazon, Netflix, and Apple coding interviews. Every problem connects to your real projects.

- **Master core data structures: arrays, hashmaps, sets, stacks, queues, heaps**
- **Understand algorithmic patterns: two pointers, sliding window, binary search**
- **Solve tree and graph problems (BFS, DFS, traversals)**
- **Apply dynamic programming for optimization problems**
- **Practice with real ENTAERA, Snap2Slides, and N8N use cases**
- **Learn to analyze time/space complexity (Big O)**

---

## 🧠 Why This Matters for FAANG

### **Google/Meta/Amazon Ask:**
1. **Array/String manipulation** (30% of problems)
2. **HashMap/HashSet patterns** (25% of problems)
3. **Tree/Graph traversals** (20% of problems)
4. **Dynamic Programming** (15% of problems)
5. **Stack/Queue/Heap** (10% of problems)

### **Your Projects Use These:**
- **ENTAERA**: Tree structures (AST parsing), graph algorithms (conversation flow), dynamic programming (context window optimization)
- **Snap2Slides**: Image processing optimization, cache management (LRU), API rate limiting queues
- **N8N**: Workflow graph traversal, dependency resolution, task scheduling

---

## 📚 Core Data Structures

### **1. Arrays & Strings**

#### **Two Pointers Pattern**
```python
def reverse_string(s: list[str]) -> None:
    """
    LeetCode #344 - Reverse String
    FAANG Frequency: ⭐⭐⭐⭐⭐
    
    Real Use: Text processing in ENTAERA (Day 1)
    """
    left, right = 0, len(s) - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1

# ENTAERA Use Case: Normalize text palindrome check
def is_palindrome(text: str) -> bool:
    """Check if normalized text is palindrome."""
    # Remove non-alphanumeric, lowercase
    cleaned = ''.join(c.lower() for c in text if c.isalnum())
    left, right = 0, len(cleaned) - 1
    while left < right:
        if cleaned[left] != cleaned[right]:
            return False
        left += 1
        right -= 1
    return True
```

#### **Sliding Window Pattern**
```python
def max_sum_subarray(nums: list[int], k: int) -> int:
    """
    Maximum sum of k consecutive elements
    FAANG Frequency: ⭐⭐⭐⭐⭐
    
    Real Use: Context window management in ENTAERA (Day 7)
    """
    if len(nums) < k:
        return 0
    
    # Initial window
    window_sum = sum(nums[:k])
    max_sum = window_sum
    
    # Slide window
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, window_sum)
    
    return max_sum

# ENTAERA Use Case: Find most important conversation segment
def most_important_messages(importance_scores: list[int], window_size: int) -> int:
    """
    Find the window of messages with highest total importance.
    Used in conversation summarization.
    """
    return max_sum_subarray(importance_scores, window_size)
```

---

### **2. HashMap & HashSet**

#### **Frequency Counter Pattern**
```python
from collections import Counter

def two_sum(nums: list[int], target: int) -> list[int]:
    """
    LeetCode #1 - Two Sum
    FAANG Frequency: ⭐⭐⭐⭐⭐
    
    Real Use: Finding matching embeddings in FAISS (Day 5)
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# ENTAERA Use Case: Find similar embeddings
def find_similar_embedding_pairs(embeddings: list[float], threshold: float) -> list[tuple]:
    """
    Find pairs of embeddings with similarity above threshold.
    Used in semantic search deduplication.
    """
    pairs = []
    seen = {}
    for i, emb in enumerate(embeddings):
        for prev_emb, prev_idx in seen.items():
            if abs(emb - prev_emb) <= threshold:
                pairs.append((prev_idx, i))
        seen[emb] = i
    return pairs
```

#### **Character Frequency**
```python
def first_unique_char(s: str) -> int:
    """
    LeetCode #387 - First Unique Character
    FAANG Frequency: ⭐⭐⭐⭐
    
    Real Use: Log analysis in N8N, error detection
    """
    count = Counter(s)
    for i, char in enumerate(s):
        if count[char] == 1:
            return i
    return -1

# N8N Use Case: Find first unique workflow error
def first_unique_error(error_codes: list[str]) -> str:
    """Find first error that only occurred once."""
    count = Counter(error_codes)
    for code in error_codes:
        if count[code] == 1:
            return code
    return None
```

---

### **3. Stack & Queue**

#### **Stack for Validation**
```python
def is_valid_parentheses(s: str) -> bool:
    """
    LeetCode #20 - Valid Parentheses
    FAANG Frequency: ⭐⭐⭐⭐⭐
    
    Real Use: AST parsing in ENTAERA (Day 10)
    """
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            stack.append(char)
    
    return len(stack) == 0

# ENTAERA Use Case: Validate JSON structure
def validate_nested_structure(tokens: list[str]) -> bool:
    """
    Validate nested data structures (JSON, XML).
    Used in API response validation (Day 8).
    """
    return is_valid_parentheses(''.join(tokens))
```

#### **Queue for BFS**
```python
from collections import deque

def level_order_traversal(root):
    """
    LeetCode #102 - Binary Tree Level Order
    FAANG Frequency: ⭐⭐⭐⭐⭐
    
    Real Use: Workflow graph traversal in N8N
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result

# N8N Use Case: Execute workflow nodes by dependency level
def execute_workflow_by_level(workflow_graph: dict) -> list[list[str]]:
    """
    Execute workflow nodes level by level (topological order).
    Ensures dependencies are satisfied before execution.
    """
    # workflow_graph = {node_id: [dependency_ids]}
    in_degree = {node: 0 for node in workflow_graph}
    for node in workflow_graph:
        for dep in workflow_graph[node]:
            in_degree[dep] += 1
    
    # Start with nodes that have no dependencies
    queue = deque([node for node in workflow_graph if in_degree[node] == 0])
    levels = []
    
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node)
            
            for neighbor in workflow_graph.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        levels.append(level)
    
    return levels
```

---

### **4. Heap (Priority Queue)**

#### **Top K Elements**
```python
import heapq

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """
    LeetCode #347 - Top K Frequent Elements
    FAANG Frequency: ⭐⭐⭐⭐⭐
    
    Real Use: Finding most important memories in ENTAERA (Day 6)
    """
    count = Counter(nums)
    return [num for num, _ in count.most_common(k)]

# ENTAERA Use Case: Retrieve top K relevant memories
def top_k_relevant_memories(memories: list[dict], k: int) -> list[dict]:
    """
    Get K most relevant memories by importance * recency * relevance score.
    Used in memory retrieval (Day 6).
    """
    # Each memory has: {"content": str, "score": float}
    heap = []
    
    for memory in memories:
        score = memory["score"]
        heapq.heappush(heap, (score, memory))
        
        # Keep only top K
        if len(heap) > k:
            heapq.heappop(heap)
    
    return [memory for score, memory in sorted(heap, reverse=True)]
```

#### **Merge K Sorted Lists**
```python
def merge_k_sorted_lists(lists: list[list[int]]) -> list[int]:
    """
    LeetCode #23 - Merge K Sorted Lists
    FAANG Frequency: ⭐⭐⭐⭐
    
    Real Use: Merging sorted logs from multiple sources (N8N)
    """
    heap = []
    
    # Initialize heap with first element from each list
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))  # (value, list_idx, elem_idx)
    
    result = []
    
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        
        # Add next element from same list
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
    
    return result

# N8N Use Case: Merge logs from multiple workflow executions
def merge_workflow_logs(log_streams: list[list[dict]]) -> list[dict]:
    """
    Merge sorted logs from multiple workflow runs.
    Each log has timestamp - merge chronologically.
    """
    heap = []
    
    for i, logs in enumerate(log_streams):
        if logs:
            heapq.heappush(heap, (logs[0]["timestamp"], i, 0, logs[0]))
    
    merged = []
    
    while heap:
        timestamp, stream_idx, log_idx, log_entry = heapq.heappop(heap)
        merged.append(log_entry)
        
        if log_idx + 1 < len(log_streams[stream_idx]):
            next_log = log_streams[stream_idx][log_idx + 1]
            heapq.heappush(heap, (next_log["timestamp"], stream_idx, log_idx + 1, next_log))
    
    return merged
```

---

### **5. Trees & Graphs**

#### **Binary Tree DFS**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def max_depth(root: TreeNode) -> int:
    """
    LeetCode #104 - Maximum Depth of Binary Tree
    FAANG Frequency: ⭐⭐⭐⭐⭐
    
    Real Use: AST depth analysis in ENTAERA (Day 10)
    """
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

# ENTAERA Use Case: Calculate code complexity (nesting depth)
def calculate_code_complexity(ast_root) -> int:
    """
    Calculate max nesting depth of code blocks.
    Used in code intelligence (Day 10).
    """
    return max_depth(ast_root)
```

#### **Graph DFS - Cycle Detection**
```python
def has_cycle_dfs(graph: dict[int, list[int]]) -> bool:
    """
    Detect cycle in directed graph
    FAANG Frequency: ⭐⭐⭐⭐
    
    Real Use: Workflow cycle detection in N8N
    """
    UNVISITED, VISITING, VISITED = 0, 1, 2
    state = {node: UNVISITED for node in graph}
    
    def dfs(node: int) -> bool:
        if state[node] == VISITING:
            return True  # Cycle found
        if state[node] == VISITED:
            return False
        
        state[node] = VISITING
        
        for neighbor in graph.get(node, []):
            if dfs(neighbor):
                return True
        
        state[node] = VISITED
        return False
    
    for node in graph:
        if state[node] == UNVISITED:
            if dfs(node):
                return True
    
    return False

# N8N Use Case: Validate workflow doesn't have circular dependencies
def validate_workflow_no_cycles(workflow: dict) -> bool:
    """
    Ensure workflow DAG has no cycles.
    Critical for workflow execution (Day 11).
    """
    return not has_cycle_dfs(workflow)
```

#### **Graph BFS - Shortest Path**
```python
def shortest_path_bfs(graph: dict, start: str, end: str) -> int:
    """
    Find shortest path between two nodes
    FAANG Frequency: ⭐⭐⭐⭐⭐
    
    Real Use: Finding optimal API call chain in ENTAERA
    """
    if start == end:
        return 0
    
    queue = deque([(start, 0)])
    visited = {start}
    
    while queue:
        node, distance = queue.popleft()
        
        for neighbor in graph.get(node, []):
            if neighbor == end:
                return distance + 1
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))
    
    return -1  # No path

# ENTAERA Use Case: Find shortest API call chain
def find_optimal_api_chain(api_dependencies: dict, start_api: str, target_api: str) -> int:
    """
    Find minimum API calls needed to reach target.
    Used in API orchestration (Day 9).
    """
    return shortest_path_bfs(api_dependencies, start_api, target_api)
```

---

### **6. Dynamic Programming**

#### **Classic DP - Fibonacci/Memoization**
```python
def fib_memo(n: int, memo: dict = None) -> int:
    """
    LeetCode #509 - Fibonacci Number
    FAANG Frequency: ⭐⭐⭐⭐
    
    Real Use: Exponential backoff calculation in ENTAERA (Day 9)
    """
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

# ENTAERA Use Case: Calculate exponential backoff delay
def calculate_backoff_delay(retry_count: int) -> float:
    """
    Calculate delay using Fibonacci sequence for retries.
    Used in API resilience (Day 9).
    """
    return fib_memo(retry_count) * 0.1  # 0.1s base delay
```

#### **DP - Coin Change (Optimization)**
```python
def coin_change(coins: list[int], amount: int) -> int:
    """
    LeetCode #322 - Coin Change
    FAANG Frequency: ⭐⭐⭐⭐⭐
    
    Real Use: Token optimization in ENTAERA context window (Day 7)
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if i >= coin:
                dp[i] = min(dp[i], dp[coin - i] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1

# ENTAERA Use Case: Optimize context window token usage
def optimize_message_selection(message_tokens: list[int], max_tokens: int) -> int:
    """
    Select minimum messages to fill context window optimally.
    Used in conversation management (Day 7).
    """
    return coin_change(message_tokens, max_tokens)
```

#### **DP - Longest Common Subsequence**
```python
def longest_common_subsequence(text1: str, text2: str) -> int:
    """
    LeetCode #1143 - Longest Common Subsequence
    FAANG Frequency: ⭐⭐⭐⭐⭐
    
    Real Use: Text diff/similarity in ENTAERA
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]

# ENTAERA Use Case: Calculate text similarity for deduplication
def calculate_text_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity ratio between two texts.
    Used in memory deduplication (Day 6).
    """
    lcs_length = longest_common_subsequence(text1, text2)
    max_length = max(len(text1), len(text2))
    return lcs_length / max_length if max_length > 0 else 0.0
```

---

## 💻 Exercises - FAANG Practice with Your Projects

### **Exercise 1: Array Manipulation (ENTAERA Context)**

```python
# TODO: Implement these using your ENTAERA knowledge

def merge_conversation_history(conv1: list[dict], conv2: list[dict]) -> list[dict]:
    """
    LeetCode #88 pattern - Merge Sorted Arrays
    Merge two conversation histories sorted by timestamp.
    
    Used in: Day 6 (Long-term memory)
    """
    pass

def find_duplicate_messages(messages: list[str]) -> list[str]:
    """
    LeetCode #287 pattern - Find Duplicates
    Find duplicate messages in conversation for deduplication.
    
    Used in: Day 6 (Memory deduplication)
    """
    pass

def rotate_message_buffer(messages: list[str], k: int) -> list[str]:
    """
    LeetCode #189 - Rotate Array
    Rotate circular message buffer for sliding window.
    
    Used in: Day 7 (Context management)
    """
    pass
```

### **Exercise 2: HashMap Patterns (Snap2Slides Context)**

```python
# TODO: Implement for Snap2Slides image processing

def cache_hit_tracker(requests: list[str]) -> dict[str, int]:
    """
    Track API request frequency for cache optimization.
    Pattern: Frequency Counter
    
    Used in: Snap2Slides API quota management
    """
    pass

def find_similar_slides(slide_hashes: list[int], threshold: int) -> list[tuple]:
    """
    LeetCode #1 pattern - Two Sum
    Find pairs of similar slides by hash difference.
    
    Used in: Snap2Slides duplicate detection
    """
    pass

def lru_cache_implementation(capacity: int):
    """
    LeetCode #146 - LRU Cache
    Implement LRU cache for image processing results.
    
    Used in: Snap2Slides performance optimization
    """
    pass
```

### **Exercise 3: Stack/Queue (N8N Workflow Context)**

```python
# TODO: Implement for N8N workflow execution

def evaluate_workflow_expression(expression: str) -> int:
    """
    LeetCode #224 pattern - Basic Calculator
    Evaluate workflow condition expressions.
    
    Used in: N8N workflow decision nodes
    """
    pass

def task_scheduler(tasks: list[str], cooldown: int) -> int:
    """
    LeetCode #621 - Task Scheduler
    Schedule workflow tasks with dependencies.
    
    Used in: N8N workflow orchestration
    """
    pass

def min_workflow_steps(workflow_graph: dict, start: str, end: str) -> int:
    """
    BFS pattern - Minimum steps
    Find shortest path through workflow.
    
    Used in: N8N workflow optimization
    """
    pass
```

### **Exercise 4: Tree/Graph (All Projects)**

```python
# TODO: Implement for code analysis and workflows

def validate_json_structure(json_str: str) -> bool:
    """
    Tree validation pattern
    Validate nested JSON from API responses.
    
    Used in: ENTAERA (Day 8), Snap2Slides API
    """
    pass

def find_workflow_dependencies(workflow: dict) -> list[list[str]]:
    """
    Topological Sort pattern
    Order workflow nodes by dependencies.
    
    Used in: N8N workflow execution order
    """
    pass

def detect_memory_leaks(object_graph: dict) -> bool:
    """
    Cycle detection pattern
    Detect circular references in memory.
    
    Used in: ENTAERA memory management
    """
    pass
```

### **Exercise 5: Dynamic Programming (Optimization)**

```python
# TODO: Implement optimization problems

def optimize_api_calls(api_costs: dict, target: str) -> int:
    """
    DP optimization pattern
    Minimize API calls to reach target data.
    
    Used in: ENTAERA API orchestration (Day 9)
    """
    pass

def max_context_value(messages: list[dict], token_limit: int) -> int:
    """
    Knapsack pattern
    Maximize information value within token limit.
    
    Used in: ENTAERA context window (Day 7)
    """
    pass

def min_retries_needed(failure_rate: float, success_threshold: float) -> int:
    """
    DP probability pattern
    Calculate minimum retries for target success rate.
    
    Used in: API resilience (Day 9)
    """
    pass
```

---

## 🎓 FAANG Interview Patterns

### **Pattern 1: Two Pointers** ⭐⭐⭐⭐⭐
**When:** Sorted arrays, palindromes, pairs
**Projects:** Text processing (ENTAERA Day 1), Data validation

### **Pattern 2: Sliding Window** ⭐⭐⭐⭐⭐
**When:** Subarray/substring problems, optimization
**Projects:** Context window (ENTAERA Day 7), API rate limiting

### **Pattern 3: Fast & Slow Pointers** ⭐⭐⭐⭐
**When:** Cycle detection, middle finding
**Projects:** Circular buffer (N8N), Memory leak detection

### **Pattern 4: HashMap Frequency** ⭐⭐⭐⭐⭐
**When:** Counting, grouping, duplicates
**Projects:** Cache management (Snap2Slides), Log analysis

### **Pattern 5: Stack for Validation** ⭐⭐⭐⭐
**When:** Matching pairs, nested structures
**Projects:** JSON validation (ENTAERA Day 8), AST parsing

### **Pattern 6: BFS/DFS** ⭐⭐⭐⭐⭐
**When:** Tree/graph traversal, shortest path
**Projects:** Workflow execution (N8N), Dependency resolution

### **Pattern 7: Binary Search** ⭐⭐⭐⭐
**When:** Sorted data, optimization
**Projects:** FAISS index search (ENTAERA Day 5)

### **Pattern 8: Top K with Heap** ⭐⭐⭐⭐
**When:** Ranking, priority
**Projects:** Memory retrieval (ENTAERA Day 6), Error prioritization

### **Pattern 9: Dynamic Programming** ⭐⭐⭐⭐⭐
**When:** Optimization, counting ways
**Projects:** Token optimization (Day 7), API cost minimization

### **Pattern 10: Union Find** ⭐⭐⭐
**When:** Connected components, grouping
**Projects:** Workflow component analysis (N8N)

---

## 🎯 Time Complexity Analysis

### **Must Know:**
```python
O(1)      - Constant: HashMap lookup, array index
O(log n)  - Logarithmic: Binary search, balanced tree
O(n)      - Linear: Single loop, array traversal
O(n log n)- Linearithmic: Merge sort, heap sort
O(n²)     - Quadratic: Nested loops
O(2ⁿ)     - Exponential: Recursive without memoization
```

### **Your Project Examples:**
```python
# ENTAERA semantic search: O(n) for linear search, O(log n) with FAISS
# Snap2Slides cache lookup: O(1) with HashMap
# N8N workflow validation: O(V + E) for graph traversal
# Context window optimization: O(n * capacity) for DP
```

---

## 🤔 FAANG Interview Questions

### **Google Favorites:**
1. **LeetCode #1** - Two Sum (HashMap) → Your FAISS search
2. **LeetCode #20** - Valid Parentheses (Stack) → Your JSON validation
3. **LeetCode #102** - Binary Tree Level Order (BFS) → Your workflow execution
4. **LeetCode #322** - Coin Change (DP) → Your token optimization

### **Meta Favorites:**
1. **LeetCode #146** - LRU Cache → Your Snap2Slides caching
2. **LeetCode #207** - Course Schedule (Topological Sort) → Your N8N workflows
3. **LeetCode #200** - Number of Islands (DFS/BFS) → Component detection

### **Amazon Favorites:**
1. **LeetCode #23** - Merge K Sorted Lists (Heap) → Your log merging
2. **LeetCode #347** - Top K Frequent (Heap) → Your memory retrieval
3. **LeetCode #79** - Word Search (Backtracking) → Text processing

---

## 🚀 Practice Schedule

### **Week 1: Arrays & HashMaps**
- Day 1-2: Two Pointers (5 problems)
- Day 3-4: Sliding Window (5 problems)
- Day 5-6: HashMap patterns (5 problems)
- Day 7: Review + implement in your projects

### **Week 2: Stack, Queue, Heap**
- Day 8-9: Stack problems (5 problems)
- Day 10-11: Queue/BFS (5 problems)
- Day 12-13: Heap/Priority Queue (5 problems)
- Day 14: Review + N8N integration

### **Week 3: Trees & Graphs**
- Day 15-16: Binary Tree (5 problems)
- Day 17-18: Graph DFS/BFS (5 problems)
- Day 19-20: Advanced graphs (5 problems)
- Day 21: Review + workflow optimization

### **Week 4: Dynamic Programming**
- Day 22-23: 1D DP (5 problems)
- Day 24-25: 2D DP (5 problems)
- Day 26-27: Advanced DP (5 problems)
- Day 28: Review + context optimization

**Total:** 60 LeetCode problems mapped to your projects

---

## 📚 Resources

- **LeetCode Patterns:** [LeetCode Patterns](https://seanprashad.com/leetcode-patterns/)
- **NeetCode Roadmap:** [NeetCode](https://neetcode.io/)
- **AlgoExpert:** Platform with video explanations
- **Your Projects:** See how every algorithm applies!

---

**Time to Complete:** 40-60 hours (4 weeks of focused practice)

**Master FAANG DSA while building real features!** 🎯
