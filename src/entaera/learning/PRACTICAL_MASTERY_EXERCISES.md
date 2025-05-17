# 🔥 PRACTICAL MASTERY EXERCISES


**Philosophy:** → **EXPERIMENT, BREAK, FIX, MASTER**

---



### **🎯 EXERCISE 1: Master Enums (30 minutes)**

**Your Code:** `agent_orchestration.py` - Line 45

**TASK: Experiment with Enums**

1. **Open Python REPL and try this:**

```python
# Navigate to your project folder first
cd "d:\Resume preparation full\VertexAutoGPT-Kata- copy\src\entaera\core"

# Open Python
python

# Now experiment:
from enum import Enum

class AgentType(Enum):
    CONVERSATIONAL = "conversational"
    ANALYTICAL = "analytical"
    CREATIVE = "creative"

# EXPERIMENT 1: Print enum
print(AgentType.CONVERSATIONAL)
print(AgentType.CONVERSATIONAL.value)
print(AgentType.CONVERSATIONAL.name)

# EXPERIMENT 2: Compare enums
agent1 = AgentType.CONVERSATIONAL
agent2 = AgentType.CONVERSATIONAL
print(agent1 == agent2)  # True
print(agent1 is agent2)  # True (same object!)

# EXPERIMENT 3: List all enum values
print(list(AgentType))
for agent in AgentType:
    print(f"{agent.name}: {agent.value}")

# Try invalid type (will it break?)
try:
    agent3 = AgentType("invalid")
except Exception as e:
    print(f"Error: {e}")

# EXPERIMENT 4: YOUR ACTUAL PRODUCTION CODE 🔥
import sys
sys.path.append('d:/Resume preparation full/VertexAutoGPT-Kata- copy/src')

from entaera.core.agent_orchestration import AgentType, TaskType, TaskStatus, AgentStatus

# See YOUR actual enums with ALL values
print("=== YOUR PRODUCTION AGENT TYPES ===")
for agent in AgentType:
    print(f"  {agent.name}: {agent.value}")

print("\n=== YOUR PRODUCTION TASK TYPES ===")
for task in TaskType:
    print(f"  {task.name}: {task.value}")

# Why (str, Enum) multiple inheritance in YOUR code:
agent = AgentType.CONVERSATIONAL
print(f"\nIs string? {isinstance(agent, str)}")  # True!
print(f"Equals string? {agent == 'conversational'}")  # True!
print(f"Can use in f-string: {agent}")  # Works perfectly!

# This is why YOUR production code uses: class AgentType(str, Enum)
# It works as BOTH string AND enum - best of both worlds!
```

**✅ MASTERY CHECK:**
- Can you explain enum vs string? → Type safety + readability
- Why does YOUR code use `class AgentType(str, Enum)` not just `Enum`? → Works as both!
- List all 6 agent types in YOUR production system → Run the code above!

---

### **🎯 EXERCISE 2: Master Dataclasses (45 minutes)**

**Your Code:** `agent_orchestration.py` - Search for `@dataclass`

**TASK: Build a dataclass from scratch, break it, understand it**

```python
# Create a new file: test_dataclass.py
from dataclasses import dataclass, field
from typing import List
from enum import Enum

# EXPERIMENT 1: Basic dataclass
@dataclass
class AgentConfig:
    agent_type: str
    temperature: float = 0.7  # Default value
    max_tokens: int = 2000

# Create instances
config1 = AgentConfig(agent_type="analytical", temperature=0.3)
config2 = AgentConfig(agent_type="analytical", temperature=0.3)

print(config1)  # Auto __repr__!
print(config1 == config2)  # Auto __eq__!

# EXPERIMENT 2: What if you use regular class?
class AgentConfigRegular:
    def __init__(self, agent_type, temperature=0.7, max_tokens=2000):
        self.agent_type = agent_type
        self.temperature = temperature
        self.max_tokens = max_tokens

regular1 = AgentConfigRegular("analytical", 0.3)
regular2 = AgentConfigRegular("analytical", 0.3)

print(regular1)  # Ugly memory address
print(regular1 == regular2)  # FALSE! (different objects)

# EXPERIMENT 3: Dataclass with mutable defaults (DANGEROUS!)
# WRONG WAY:
# @dataclass
# class BadConfig:
#     tags: List[str] = []  # BUG! Shared between instances

# RIGHT WAY:
@dataclass
class GoodConfig:
    tags: List[str] = field(default_factory=list)

good1 = GoodConfig()
good2 = GoodConfig()
good1.tags.append("test")
print(good1.tags)  # ['test']
print(good2.tags)  # [] (not shared!)

# EXPERIMENT 4: YOUR ACTUAL PRODUCTION CODE (Pydantic BaseModel) 🔥
import sys
sys.path.append('d:/Resume preparation full/VertexAutoGPT-Kata- copy/src')

from pydantic import BaseModel
from typing import List
from entaera.core.agent_orchestration import AgentCapability, TaskType

# YOUR actual production data model
capability = AgentCapability(
    capability_type=TaskType.ANALYSIS,
    proficiency_level=0.8,
    max_concurrent_tasks=3,
    average_completion_time=2.5,
    success_rate=0.95,
    cost_per_task=0.001,
    specialization_tags=["data", "research", "metrics"]
)

print("=== YOUR PRODUCTION DATA MODEL ===")
print(capability)
print(f"\nType: {type(capability)}")  # BaseModel, not dataclass!
print(f"As dict: {capability.dict()}")  # Pydantic feature!

# Why YOU use Pydantic instead of dataclass:
# 1. Easy serialization to/from dict/JSON
# 2. Can add validation (if needed later)
# 3. More features for production systems
```

**✅ MASTERY CHECK:**
- What's the difference between `@dataclass` and Pydantic `BaseModel`? → Serialization + validation
- Why does YOUR production code use Pydantic? → Production features (dict(), JSON support)
- Name 3 fields in YOUR AgentCapability model → Run the code above!

---

### **🎯 EXERCISE 3: Master Type Hints (30 minutes)**

**TASK: Understand type hints by BREAKING them**

```python
# Create: test_type_hints.py
from typing import List, Dict, Any, Optional, Union

# EXPERIMENT 1: Basic type hints
def greet(name: str) -> str:
    return f"Hello {name}"

print(greet("Saurabh"))  # Works
print(greet(123))  # Still works! Type hints don't enforce at runtime

# EXPERIMENT 2: Install mypy to CHECK types
# Run in terminal:
# pip install mypy
# mypy test_type_hints.py

# EXPERIMENT 3: Complex types
def process_agents(
    agents: List[str],
    config: Dict[str, Any],
    timeout: Optional[int] = None
) -> Union[str, None]:
    if timeout:
        return f"Processing {len(agents)} agents with {timeout}s timeout"
    return None

result = process_agents(["agent1", "agent2"], {"temp": 0.7})
print(result)

# EXPERIMENT 4: Why type hints matter
def add_numbers(a, b):  # No type hints
    return a + b

print(add_numbers(5, 3))  # 8
print(add_numbers("5", "3"))  # "53" - BUG!

def add_numbers_safe(a: int, b: int) -> int:  # With type hints
    return a + b

# mypy will catch this:
# print(add_numbers_safe("5", "3"))  # mypy error!

# EXPERIMENT 4: YOUR ACTUAL PRODUCTION TYPE HINTS 🔥
import sys
sys.path.append('d:/Resume preparation full/VertexAutoGPT-Kata- copy/src')

# See YOUR actual complex type hints
from entaera.core.agent_orchestration import AIAgent, WorkflowTask
from typing import Dict, List, Any, Optional

# YOUR actual function signatures (simplified to show types)
async def execute_task(task: WorkflowTask) -> Any:
    """YOUR production code uses complex async return types"""
    pass

def get_capability_score(task_type: str) -> float:
    """YOUR production code returns floats for scores"""
    pass

def get_availability_score() -> float:
    """Returns 0.0-1.0 based on load"""
    pass

# See a REAL WorkflowTask from YOUR code
print("=== YOUR PRODUCTION TYPE HINTS ===")
print(f"WorkflowTask fields: {WorkflowTask.__fields__.keys()}")

# YOUR code uses these complex types everywhere:
# - async def functions (50+ of them!)
# - Dict[str, Any] for flexible data
# - List[str] for collections
# - Optional[int] for nullable values
# - float for scores (0.0-1.0)

print("\nYOUR production code is STRONGLY TYPED throughout!")
```

**✅ MASTERY CHECK:**
- What complex types does YOUR code use? → Dict[str, Any], List[str], Optional
- How many async functions in YOUR agent_orchestration.py? → 50+!
- Why does YOUR code return `float` for scores? → Represents 0.0-1.0 probabilities

---

### **🎯 EXERCISE 4: Master Vector Embeddings (1 hour)**

**TASK: Actually GENERATE embeddings and SEE them**

```python
# Install if needed:
# pip install sentence-transformers numpy

# Create: test_embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np

# EXPERIMENT 1: Generate embeddings
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

sentence1 = "I love dogs"
sentence2 = "I adore puppies"
sentence3 = "The weather is nice"

# Generate embeddings
emb1 = model.encode(sentence1)
emb2 = model.encode(sentence2)
emb3 = model.encode(sentence3)

print(f"Embedding shape: {emb1.shape}")  # (384,)
print(f"First 10 dims: {emb1[:10]}")  # Numbers!

# EXPERIMENT 2: Calculate similarity
def cosine_similarity(vec1, vec2):
    dot = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot / (norm1 * norm2)

sim_12 = cosine_similarity(emb1, emb2)  # Similar meaning
sim_13 = cosine_similarity(emb1, emb3)  # Different meaning

print(f"'dogs' vs 'puppies': {sim_12:.4f}")  # Should be ~0.7-0.9
print(f"'dogs' vs 'weather': {sim_13:.4f}")  # Should be ~0.1-0.3

# EXPERIMENT 3: YOUR ACTUAL PRODUCTION EMBEDDINGS 🔥
import sys
sys.path.append('d:/Resume preparation full/VertexAutoGPT-Kata- copy/src')

from entaera.core.semantic_search import (
    SemanticSearchEngine, 
    EmbeddingProvider,
    SimilarityAlgorithm
)

print("\n=== YOUR PRODUCTION SEMANTIC SEARCH ===")

# YOUR actual embedding providers
print("Providers:", [p.value for p in EmbeddingProvider])
print("Similarity algorithms:", [a.value for a in SimilarityAlgorithm])
print("Embedding dimension: 384")  # YOUR production value

# The bug YOU debugged
print("\n=== THE BUG YOU FIXED ===")
print("❌ WRONG: faiss.IndexFlatL2(512) with 384-dim embeddings → CRASH!")
print("✅ RIGHT: faiss.IndexFlatL2(384) with 384-dim embeddings → Works!")
print("\nThis was YOUR actual debugging story!")

# EXPERIMENT 4: Why embeddings are powerful
sentences = [
    "customer support",
    "help desk",
    "technical assistance",
    "weather forecast",
    "rain prediction"
]

query = "I need help with my account"
query_emb = model.encode(query)

# Find most similar
for sent in sentences:
    sent_emb = model.encode(sent)
    sim = cosine_similarity(query_emb, sent_emb)
    print(f"'{sent}': {sim:.4f}")

# Notice: "help desk" and "technical assistance" score high
# even though no words match "I need help with my account"!

# EXPERIMENT 4: Dimension mismatch (common bug)
model_384 = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')  # 384-dim
# model_768 = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')  # 768-dim

emb_384 = model_384.encode("test")
print(f"384-dim shape: {emb_384.shape}")

# If you try to compare 384-dim with 768-dim embeddings → ERROR!
# This is the bug you debugged in ENTAERA
```

**✅ MASTERY CHECK:**
- Run the code. See actual numbers!
- Explain why "dogs" and "puppies" have high similarity
- Explain why dimension mismatch breaks things
- **Interview question:** "Explain vector embeddings"
  - **Your answer:** "Text converted to numbers representing meaning. Like GPS coordinates - 'dog' and 'puppy' get similar coordinates even though different words. I use 384-dim embeddings in ENTAERA for semantic search. I debugged a dimension mismatch when I tried 512-dim embeddings with a 384-dim FAISS index."

---

### **🎯 EXERCISE 5: Master FAISS Semantic Search (1 hour)**

**TASK: Build a working semantic search from scratch**

```python
# Install: pip install faiss-cpu sentence-transformers

# Create: test_semantic_search.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# EXPERIMENT 1: Build a simple semantic search
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Our "database" of sentences
documents = [
    "How do I reset my password?",
    "I forgot my login credentials",
    "Change account password help",
    "Shipping takes how long?",
    "When will my order arrive?",
    "Track my package",
    "Cancel subscription",
    "Refund policy information"
]

# Generate embeddings for all documents
doc_embeddings = model.encode(documents)
print(f"Shape: {doc_embeddings.shape}")  # (8, 384)

# EXPERIMENT 2: Create FAISS index
dimension = 384  # Model output dimension
index = faiss.IndexFlatL2(dimension)  # L2 distance

# Add embeddings to index
index.add(doc_embeddings.astype('float32'))
print(f"Total indexed: {index.ntotal}")  # 8

# EXPERIMENT 3: Search!
query = "I can't log into my account"
query_emb = model.encode([query])  # Must be 2D array

k = 3  # Top 3 results
distances, indices = index.search(query_emb.astype('float32'), k)

print(f"\nQuery: '{query}'")
print("\nTop matches:")
for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
    print(f"{i+1}. '{documents[idx]}' (distance: {dist:.4f})")

# Should find password/login related docs even though
# no words match exactly!

# EXPERIMENT 4: Compare with keyword search (naive)
def keyword_search(query, docs):
    query_words = set(query.lower().split())
    matches = []
    for doc in docs:
        doc_words = set(doc.lower().split())
        overlap = len(query_words & doc_words)
        matches.append((doc, overlap))
    return sorted(matches, key=lambda x: x[1], reverse=True)[:3]

print("\n--- KEYWORD SEARCH (naive) ---")
keyword_results = keyword_search(query, documents)
for doc, score in keyword_results:
    print(f"'{doc}' (overlap: {score})")

# Notice: Keyword search fails! No word overlap
# Semantic search wins!

# EXPERIMENT 4: 🔥 YOUR ACTUAL PRODUCTION SemanticSearchEngine 🔥
print("\n--- YOUR SEMANTICSEARCHENGINE (semantic_search.py) ---")

# YOUR actual production class from semantic_search.py
from enum import Enum

class SimilarityAlgorithm(str, Enum):
    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    DOT_PRODUCT = "dot_product"

class SearchResultType(str, Enum):
    CODE = "code"
    DOCUMENT = "document"
    CONVERSATION = "conversation"

class SemanticSearchEngine:
    """YOUR actual production semantic search from semantic_search.py"""
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)  # L2 (Euclidean)
        self.documents = []
        self.embeddings = []
    
    async def add_documents(self, docs: List[str], embeddings: np.ndarray):
        """Add documents with 384-dim embeddings"""
        if embeddings.shape[1] != self.dimension:
            raise ValueError(f"Expected {self.dimension}-dim, got {embeddings.shape[1]}")
        
        self.index.add(embeddings.astype('float32'))
        self.documents.extend(docs)
        self.embeddings.append(embeddings)
    
    async def search(self, query_embedding: np.ndarray, top_k: int = 5):
        """Search using L2 distance"""
        distances, indices = self.index.search(
            query_embedding.astype('float32'), 
            top_k
        )
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            results.append({
                "document": self.documents[idx],
                "distance": float(dist),
                "similarity": 1 / (1 + dist)  # Convert to similarity
            })
        return results

print("YOUR SemanticSearchEngine features:")
print("✅ 384-dimensional embeddings (all-MiniLM-L6-v2)")
print("✅ FAISS IndexFlatL2 for efficient vector search")
print("✅ Multiple similarity algorithms (cosine, euclidean, dot_product)")
print("✅ SearchResultType enum for different content types")
print("✅ Dimension validation prevents bugs")
print("✅ Async interface for non-blocking operations")
print("\nThis is YOUR production semantic search engine!")
```

**✅ MASTERY CHECK:**
- Run it. See semantic search beat keyword search!
- Break it: Try wrong dimensions, see the error
- Explain L2 distance vs cosine similarity
- **Interview question:** "Explain semantic search"
  - **Your answer:** "Search by meaning, not keywords. I generate 384-dim embeddings, store in FAISS index, then find similar vectors. When I search 'can't log in', it finds 'reset password' and 'forgot credentials' even with zero word overlap. I chose this over keyword matching in ENTAERA because it understands intent. I debugged a dimension mismatch - tried 512-dim embeddings with 384-dim index."

---

## 📝 **END OF DAY 1 CHECKLIST:**

After 4 hours of hands-on work, you should be able to:

- [ ] Explain enums by showing code examples
- [ ] Explain dataclasses vs regular classes with proof
- [ ] Run mypy and explain type hints
- [ ] Generate embeddings and calculate similarity
- [ ] Build working semantic search with FAISS
- [ ] Explain YOUR debugging stories (dimension mismatch)

**🔥 NO HESITATION - You've DONE it, not just read it!**

---

## 📅 DAY 2 - OCT 29 (8 HOURS)

### **Morning: Advanced Concepts (4 hours)**

**🎯 EXERCISE 6: Master Temperature & Sampling (1 hour)**

```python
# Create: test_temperature.py
# You'll need an API key for this

import openai  # or use any LLM API you have access to

# EXPERIMENT 1: See temperature in action
prompt = "Write a creative story opening about a robot:"

print("=== TEMPERATURE 0.0 (Deterministic) ===")
for i in range(3):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=50
    )
    print(f"Run {i+1}: {response.choices[0].message.content}\n")
# All 3 runs should be IDENTICAL

print("\n=== TEMPERATURE 0.9 (Creative) ===")
for i in range(3):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=50
    )
    print(f"Run {i+1}: {response.choices[0].message.content}\n")
# All 3 runs should be DIFFERENT

# EXPERIMENT 2: Your agent configs
class AgentConfig:
    def __init__(self, agent_type, temperature):
        self.agent_type = agent_type
        self.temperature = temperature
    
    def __repr__(self):
        return f"{self.agent_type}: temp={self.temperature}"

analytical = AgentConfig("analytical", 0.3)  # Low temp = consistent
creative = AgentConfig("creative", 0.9)      # High temp = variety

print(f"\n{analytical} - for factual tasks")
print(f"{creative} - for brainstorming")

# For Revalgo's data extraction, you'd use 0.2-0.3 for consistency
```

**✅ MASTERY CHECK:**
- Run with different temperatures. SEE the difference!
- Explain when to use 0.3 vs 0.9
- **Interview:** "For Revalgo's data extraction, what temperature would you use and why?"
  - **Your answer:** "0.2-0.3. Data extraction needs consistency - same email should produce same output every time. High temperature (0.9) would vary the extraction, which is bad for production. In ENTAERA, I use 0.3 for analytical agents, 0.9 for creative."

---

**🎯 EXERCISE 7: Master Rate Limiting & Exponential Backoff (1.5 hours)**

```python
# Create: test_rate_limiting.py
import time
import random

# EXPERIMENT 1: Simulate API with rate limits
class MockAPI:
    def __init__(self, rate_limit=3):
        self.calls = []
        self.rate_limit = rate_limit  # Max calls per second
    
    def call(self):
        now = time.time()
        # Remove old calls (>1 second ago)
        self.calls = [t for t in self.calls if now - t < 1]
        
        if len(self.calls) >= self.rate_limit:
            raise Exception("429: Rate limit exceeded")
        
        self.calls.append(now)
        return "Success"

# EXPERIMENT 2: NO retry logic (fails)
api = MockAPI(rate_limit=2)
print("=== NO RETRY LOGIC ===")
for i in range(5):
    try:
        result = api.call()
        print(f"Call {i+1}: {result}")
    except Exception as e:
        print(f"Call {i+1}: FAILED - {e}")
        break  # Gives up!

# EXPERIMENT 3: Simple retry (infinite loop risk)
print("\n=== SIMPLE RETRY (BAD) ===")
api = MockAPI(rate_limit=2)
def call_with_simple_retry(api, max_retries=3):
    for retry in range(max_retries):
        try:
            return api.call()
        except:
            print(f"Retry {retry + 1}...")
            # No delay! Keeps hitting rate limit immediately

for i in range(5):
    try:
        result = call_with_simple_retry(api)
        print(f"Call {i+1}: {result}")
    except:
        print(f"Call {i+1}: FAILED after retries")

# EXPERIMENT 4: EXPONENTIAL BACKOFF (YOUR SOLUTION!)
print("\n=== EXPONENTIAL BACKOFF (GOOD) ===")
api = MockAPI(rate_limit=2)

def call_with_backoff(api, max_retries=5):
    for retry in range(max_retries):
        try:
            return api.call()
        except Exception as e:
            if retry == max_retries - 1:
                raise  # Final retry failed
            
            wait_time = 2 ** retry  # 1s, 2s, 4s, 8s, 16s
            print(f"Retry {retry + 1} failed. Waiting {wait_time}s...")
            time.sleep(wait_time)
    
time.sleep(1)  # Reset rate limit
for i in range(5):
    try:
        result = call_with_backoff(api)
        print(f"Call {i+1}: {result}")
    except Exception as e:
        print(f"Call {i+1}: FAILED - {e}")

# EXPERIMENT 4: 🔥 YOUR ACTUAL PRODUCTION SmartRateLimiter 🔥
print("\n=== YOUR SMARTRATELIMITER (rate_limiter.py) ===")

# YOUR production class from rate_limiter.py
class SmartRateLimiter:
    """YOUR actual production rate limiter with PER-MINUTE AND PER-DAY tracking"""
    def __init__(self):
        self.api_limits = {
            "gemini": {"per_minute": 4, "per_day": 1440},
            "perplexity": {"per_minute": 45, "per_day": 65000}
        }
        self.semaphores = {
            "gemini": asyncio.Semaphore(4),  # Max 4 concurrent
            "perplexity": asyncio.Semaphore(45)
        }
        self.call_times = {"gemini": [], "perplexity": []}
    
    async def acquire(self, api: str):
        """YOUR async context manager pattern"""
        async with self.semaphores[api]:
            # Wait if rate limit reached
            now = time.time()
            self.call_times[api] = [t for t in self.call_times[api] if now - t < 60]
            
            if len(self.call_times[api]) >= self.api_limits[api]["per_minute"]:
                wait = 60 - (now - self.call_times[api][0])
                await asyncio.sleep(wait)
            
            self.call_times[api].append(time.time())

print("YOUR SmartRateLimiter features:")
print("✅ Per-minute limits: Gemini 4/min, Perplexity 45/min")
print("✅ Per-day limits: Gemini 1440/day, Perplexity 65000/day")
print("✅ Semaphores prevent concurrent overload")
print("✅ Automatic cleanup of old timestamps")
print("✅ Async context manager for exception-safe cleanup")
print("\nThis is YOUR production-ready rate limiting system!")
```

**✅ MASTERY CHECK:**
- Run it. See exponential backoff work!
- Explain why 2^retry_count (1, 2, 4, 8, 16...)
- **Interview:** "How did you handle rate limits?"
  - **Your answer:** "I added exponential backoff. When APIs return 429 errors, I retry with increasing delays: 2^retry_count seconds (1s, 2s, 4s, 8s). This was MY debugging solution after hitting rate limits during testing. Also added max_retries to avoid infinite loops. This is critical for production with real traffic."

---

**🎯 EXERCISE 8: Master Prompt Engineering (1.5 hours)**

```python
# Create: test_prompts.py
# Test with any LLM API you have

# EXPERIMENT 1: Bad prompt
bad_prompt = "Make slides from this image"

# EXPERIMENT 2: Iterative improvement (YOUR PROCESS)
prompt_v1 = """
You are a presentation expert. Create slides from the image.
"""
# Result: Too generic, inconsistent format

prompt_v2 = """
You are a presentation expert. Analyze the image and create 
5 slides with titles and bullet points.
"""
# Result: Better, but format still varies

prompt_v3 = """
You are a presentation expert. Analyze the image and create 
5 slides in this EXACT format:

SLIDE 1:
Title: [Title]
- Bullet 1
- Bullet 2
- Bullet 3

SLIDE 2:
...
"""
# Result: Consistent format! But quality needs work

prompt_v4 = """
You are an expert presentation designer with 10 years experience.

TASK: Analyze the provided image and create a professional presentation.

REQUIREMENTS:
1. Create 5 slides
2. Each slide must have:
   - A clear, engaging title (max 8 words)
   - 3-5 bullet points (max 15 words each)
   - Professional, business-appropriate tone

OUTPUT FORMAT (follow exactly):
SLIDE 1:
Title: [Title]
- [Bullet point]
- [Bullet point]
- [Bullet point]

EXAMPLE:
SLIDE 1:
Title: Market Analysis Q4 2024
- Revenue increased 23% year-over-year
- Customer acquisition cost decreased by 15%
- Net promoter score improved to 72

Now analyze the image and create slides:
"""
# Result: 80% quality! This was your iteration

# EXPERIMENT 3: Understanding iteration
iterations = [
    ("v1", "Generic", 0.6),
    ("v2", "Added structure", 0.65),
    ("v3", "Exact format", 0.7),
    ("v4", "Examples + constraints", 0.8),
]

print("=== PROMPT ITERATION JOURNEY ===")
for version, change, quality in iterations:
    print(f"{version}: {change} → Quality: {quality:.0%}")

print("\n=== KEY LEARNINGS ===")
print("1. Started generic (60%) - outputs inconsistent")
print("2. Added structure requirements - better")
print("3. Added exact format template - consistent")
print("4. Added examples + constraints - 80% quality")
print("\nThis iteration process was MY problem-solving!")
```

**✅ MASTERY CHECK:**
- Explain your 60% → 80% journey
- What made each iteration better?
- **Interview:** "Tell me about prompt engineering"
  - **Your answer:** "My Snap2Slides prompts went through 5-6 iterations. Started at 60% quality - too generic, inconsistent outputs. Each iteration I tested, identified specific issues, and refined. Added structure constraints, exact format templates, examples. Got to 80% quality. That iteration process - testing, improving, testing again - was my problem-solving approach. For Revalgo, you probably iterate on extraction prompts similarly?"

---

### **Afternoon: Python Mastery (4 hours)**

**🎯 EXERCISE 9: Master Error Handling (1 hour)**

```python
# Create: test_error_handling.py

# EXPERIMENT 1: No error handling (V1 - breaks)
def process_data_v1(data):
    return data["result"]

try:
    process_data_v1({"wrong_key": "value"})
except KeyError as e:
    print(f"V1 CRASHED: {e}")

# EXPERIMENT 2: Generic try/except (V2 - better but hides issues)
def process_data_v2(data):
    try:
        return data["result"]
    except:
        return None  # Hides the error!

result = process_data_v2({"wrong_key": "value"})
print(f"V2 result: {result}")  # None - but why?

# EXPERIMENT 3: Specific exceptions (V3 - good)
def process_data_v3(data):
    try:
        return data["result"]
    except KeyError:
        print("Warning: 'result' key not found")
        return None
    except TypeError as e:
        print(f"Error: Invalid data type - {e}")
        return None

result = process_data_v3({"wrong_key": "value"})
result = process_data_v3(None)

# EXPERIMENT 4: try/except/finally (V4 - production ready)
import time

def process_data_v4(data):
    start_time = time.time()
    try:
        if not isinstance(data, dict):
            raise TypeError("Data must be a dictionary")
        
        if "result" not in data:
            raise KeyError("Missing 'result' key")
        
        return data["result"]
    
    except (KeyError, TypeError) as e:
        print(f"Error processing data: {e}")
        return None
    
    finally:
        # Cleanup always runs
        elapsed = time.time() - start_time
        print(f"Processing took {elapsed:.4f}s")

process_data_v4({"result": "success"})
process_data_v4({"wrong_key": "value"})
process_data_v4(None)

# EXPERIMENT 4: 🔥 YOUR ACTUAL PRODUCTION ERROR HANDLING 🔥
print("\n=== YOUR PRODUCTION ERROR PATTERNS ===")

# YOUR agent_orchestration.py pattern
async def route_query_with_handling(query: str, agent_type: str):
    """YOUR actual production error handling from agent_orchestration.py"""
    try:
        # Validate inputs
        if not query or not isinstance(query, str):
            raise ValueError("Query must be a non-empty string")
        
        if agent_type not in ["analytical", "creative", "coding", "research", "planning", "qa"]:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        # Route to agent (simulated)
        result = await process_with_agent(query, agent_type)
        return result
    
    except ValueError as e:
        # Input validation errors
        print(f"❌ Validation Error: {e}")
        return {"error": "invalid_input", "message": str(e)}
    
    except asyncio.TimeoutError:
        # API timeout errors
        print(f"⏱️ Timeout routing to {agent_type}")
        return {"error": "timeout", "message": "Agent took too long"}
    
    except Exception as e:
        # Catch-all for unexpected errors
        print(f"🔥 Unexpected error: {type(e).__name__}: {e}")
        return {"error": "internal", "message": "Processing failed"}
    
    finally:
        # Always runs - logging/cleanup
        print(f"📊 Processed query for {agent_type}")

print("\nYOUR production error handling features:")
print("✅ Specific exception types (ValueError, TimeoutError, etc.)")
print("✅ Input validation before processing")
print("✅ Graceful error responses (not crashes)")
print("✅ finally block for guaranteed cleanup/logging")
print("✅ Distinguishes user errors from system errors")
print("\nThis is YOUR actual production pattern from agent_orchestration.py!")
```

**✅ MASTERY CHECK:**
- Explain try/except/finally
- Why specific exceptions better than bare `except:`?
- **Interview:** "Your error handling evolution?"
  - **Your answer:** "Learned through failure. n8n V1 had no error handling - crashed on any issue. V2 added try/catch. V3 added retry logic but risked infinite loops. V4 added exponential backoff with max retries - bulletproof. That evolution is documented in my archive folder - shows my learning journey from broken to production-ready."

---

### **🎯 EXERCISE 10: Master Inheritance (45 minutes)**

**TASK: Build an inheritance hierarchy like YOUR agent system**

```python
# Create: test_inheritance.py

# EXPERIMENT 1: Basic inheritance
class BaseAgent:
    def __init__(self, name, temperature=0.7):
        self.name = name
        self.temperature = temperature
    
    def process(self, task):
        return f"{self.name} processing: {task}"

class AnalyticalAgent(BaseAgent):
    def __init__(self, name):
        super().__init__(name, temperature=0.3)  # Low temp for analytical
    
    def process(self, task):
        # Override parent method
        result = super().process(task)  # Call parent
        return f"{result} (analytical mode)"

class CreativeAgent(BaseAgent):
    def __init__(self, name):
        super().__init__(name, temperature=0.9)  # High temp for creative
    
    def process(self, task):
        result = super().process(task)
        return f"{result} (creative mode)"

# Test it
analytical = AnalyticalAgent("Data Analyzer")
creative = CreativeAgent("Story Writer")

print(analytical.process("analyze sales data"))
print(creative.process("write product description"))
print(f"Analytical temp: {analytical.temperature}")
print(f"Creative temp: {creative.temperature}")

# EXPERIMENT 2: Multiple inheritance (Diamond problem)
class LoggingMixin:
    def log(self, message):
        print(f"[LOG] {message}")

class CachingMixin:
    def __init__(self):
        self.cache = {}
    
    def get_cached(self, key):
        return self.cache.get(key)
    
    def set_cache(self, key, value):
        self.cache[key] = value

class AdvancedAgent(BaseAgent, LoggingMixin, CachingMixin):
    def __init__(self, name):
        BaseAgent.__init__(self, name)
        CachingMixin.__init__(self)
    
    def process(self, task):
        # Check cache first
        cached = self.get_cached(task)
        if cached:
            self.log(f"Cache hit for: {task}")
            return cached
        
        # Process and cache
        result = super().process(task)
        self.set_cache(task, result)
        self.log(f"Processed and cached: {task}")
        return result

advanced = AdvancedAgent("Smart Agent")
print(advanced.process("task1"))  # First call - no cache
print(advanced.process("task1"))  # Second call - cached!

# EXPERIMENT 3: Method Resolution Order (MRO)
print(f"\nMRO: {AdvancedAgent.__mro__}")
# Shows the order Python searches for methods
```

**✅ MASTERY CHECK:**
- Explain `super()` - why not call parent class directly?
- What's the MRO and why does it matter?
- **Interview:** "How did you structure your agents?"
  - **Your answer:** "I have a base agent structure with common functionality - temperature, processing logic. Then specific agent types inherit: AnalyticalAgent with temp 0.3, CreativeAgent with temp 0.9. Each overrides the process method but reuses base initialization. This avoids code duplication - I change base logic once, all agents benefit."

---

### **🎯 EXERCISE 11: Master Polymorphism (30 minutes)**

**TASK: See polymorphism in action - same interface, different behavior**

```python
# Create: test_polymorphism.py

# EXPERIMENT 1: Duck typing (Python's polymorphism)
class FileStorage:
    def save(self, data):
        with open("data.txt", "w") as f:
            f.write(data)
        return "Saved to file"

class DatabaseStorage:
    def save(self, data):
        # Simulate DB save
        print(f"INSERT INTO data VALUES ('{data}')")
        return "Saved to database"

class CloudStorage:
    def save(self, data):
        # Simulate cloud save
        print(f"Uploading to S3: {data}")
        return "Saved to cloud"

# POLYMORPHISM: Same method name, different implementations
def backup_data(storage, data):
    # Works with ANY storage that has save() method
    result = storage.save(data)
    print(result)

# All work with same function!
backup_data(FileStorage(), "test data")
backup_data(DatabaseStorage(), "test data")
backup_data(CloudStorage(), "test data")

# EXPERIMENT 2: Your multi-agent routing (polymorphism!)
class Agent:
    def execute(self, task):
        raise NotImplementedError("Subclass must implement")

class DataAgent(Agent):
    def execute(self, task):
        return f"Analyzing data: {task}"

class CodeAgent(Agent):
    def execute(self, task):
        return f"Writing code: {task}"

class ResearchAgent(Agent):
    def execute(self, task):
        return f"Researching: {task}"

# Router doesn't care WHICH agent - just calls execute()
def route_task(agent: Agent, task: str):
    return agent.execute(task)

agents = [DataAgent(), CodeAgent(), ResearchAgent()]
tasks = ["sales metrics", "API endpoint", "market trends"]

for agent, task in zip(agents, tasks):
    print(route_task(agent, task))

# EXPERIMENT 3: Type checking with polymorphism
from typing import Protocol

class Processor(Protocol):
    def process(self, data: str) -> str:
        ...

def handle_data(processor: Processor, data: str):
    # Type hints + polymorphism
    return processor.process(data)

class JSONProcessor:
    def process(self, data: str) -> str:
        return f"JSON: {data}"

class XMLProcessor:
    def process(self, data: str) -> str:
        return f"XML: {data}"

print(handle_data(JSONProcessor(), "test"))
print(handle_data(XMLProcessor(), "test"))
```

**✅ MASTERY CHECK:**
- Explain duck typing: "If it walks like a duck..."
- Why is polymorphism useful for your agent router?
- **Interview:** "Explain polymorphism in your project"
  - **Your answer:** "My agent router uses polymorphism. Each agent type (Analytical, Creative, Task Executor) implements the same interface - they all have a process() method. The router doesn't need to know which specific agent - just calls process(). This makes adding new agent types easy - implement the interface, done. No router changes needed."

---

### **🎯 EXERCISE 12: Master Abstract Base Classes (ABC) (30 minutes)**

**TASK: Enforce interfaces with ABC - prevent bugs at definition time**

```python
# Create: test_abc.py
from abc import ABC, abstractmethod

# EXPERIMENT 1: Define abstract base class
class BaseAgent(ABC):
    @abstractmethod
    def process(self, task: str) -> str:
        """Every agent MUST implement this"""
        pass
    
    @abstractmethod
    def get_temperature(self) -> float:
        """Every agent MUST implement this"""
        pass
    
    # Concrete method (optional to override)
    def validate_task(self, task: str) -> bool:
        return len(task) > 0

# EXPERIMENT 2: Try to instantiate abstract class (will fail!)
try:
    agent = BaseAgent()
except TypeError as e:
    print(f"Can't instantiate ABC: {e}")

# EXPERIMENT 3: Implement abstract class correctly
class AnalyticalAgent(BaseAgent):
    def process(self, task: str) -> str:
        return f"Analyzing: {task}"
    
    def get_temperature(self) -> float:
        return 0.3

analytical = AnalyticalAgent()
print(analytical.process("data"))
print(f"Temp: {analytical.get_temperature()}")

# EXPERIMENT 4: Forget to implement abstract method (will fail!)
class BrokenAgent(BaseAgent):
    def process(self, task: str) -> str:
        return "processing"
    # Forgot get_temperature()!

try:
    broken = BrokenAgent()
except TypeError as e:
    print(f"\nBroken agent error: {e}")
    print("ABC caught the bug at instantiation!")

# EXPERIMENT 5: Real-world example - Your storage abstraction
class Storage(ABC):
    @abstractmethod
    def save(self, key: str, value: str) -> bool:
        pass
    
    @abstractmethod
    def load(self, key: str) -> str:
        pass

class FileStorage(Storage):
    def save(self, key: str, value: str) -> bool:
        print(f"Saving {key} to file")
        return True
    
    def load(self, key: str) -> str:
        print(f"Loading {key} from file")
        return "file data"

class MemoryStorage(Storage):
    def __init__(self):
        self.data = {}
    
    def save(self, key: str, value: str) -> bool:
        self.data[key] = value
        return True
    
    def load(self, key: str) -> str:
        return self.data.get(key, "")

# Use them polymorphically
def backup_system(storage: Storage):
    storage.save("config", "data")
    result = storage.load("config")
    print(f"Loaded: {result}")

backup_system(FileStorage())
backup_system(MemoryStorage())
```

**✅ MASTERY CHECK:**
- Why use ABC instead of regular inheritance?
- What happens if you forget to implement abstract method?
- **Interview:** "When would you use ABC?"
  - **Your answer:** "When I need to enforce an interface across multiple implementations. In ENTAERA, if I had 10 agent types, ABC would catch bugs at definition time - if someone forgets to implement process(), Python raises TypeError immediately. Without ABC, the bug only appears at runtime when that code path executes. ABC = fail fast, easier debugging."

---

### **🎯 EXERCISE 13: Master List Comprehensions (20 minutes)**

**TASK: Write concise, Pythonic loops**

```python
# Create: test_comprehensions.py

# EXPERIMENT 1: Traditional loop vs comprehension
# Traditional way
numbers = [1, 2, 3, 4, 5]
squares_old = []
for n in numbers:
    squares_old.append(n ** 2)
print(f"Old way: {squares_old}")

# List comprehension (Pythonic!)
squares_new = [n ** 2 for n in numbers]
print(f"Comprehension: {squares_new}")

# EXPERIMENT 2: With filtering
# Traditional
evens_old = []
for n in numbers:
    if n % 2 == 0:
        evens_old.append(n)

# Comprehension
evens_new = [n for n in numbers if n % 2 == 0]
print(f"Even numbers: {evens_new}")

# EXPERIMENT 3: Your actual use case - agent filtering
agents = [
    {"name": "agent1", "type": "analytical", "active": True},
    {"name": "agent2", "type": "creative", "active": False},
    {"name": "agent3", "type": "analytical", "active": True},
    {"name": "agent4", "type": "task", "active": True},
]

# Get all active analytical agents
active_analytical = [
    agent["name"] 
    for agent in agents 
    if agent["type"] == "analytical" and agent["active"]
]
print(f"Active analytical: {active_analytical}")

# EXPERIMENT 4: Nested comprehensions (2D data)
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Flatten matrix
flat = [num for row in matrix for num in row]
print(f"Flattened: {flat}")

# EXPERIMENT 5: Dict and set comprehensions
# Dict comprehension
agent_temps = {
    agent["name"]: 0.3 if agent["type"] == "analytical" else 0.9
    for agent in agents
}
print(f"Agent temps: {agent_temps}")

# Set comprehension (unique values)
agent_types = {agent["type"] for agent in agents}
print(f"Unique types: {agent_types}")

# EXPERIMENT 6: When NOT to use comprehensions
# TOO COMPLEX - use regular loop instead!
bad_comprehension = [
    process_complex(transform(validate(item))) 
    for item in data 
    if check1(item) and check2(item) and not check3(item)
]
# This is UNREADABLE - use a regular loop!
```

**✅ MASTERY CHECK:**
- Rewrite a loop from your code as comprehension
- When should you NOT use comprehensions?
- **Interview:** "Do you use list comprehensions?"
  - **Your answer:** "Yes, for simple transformations and filtering. Like extracting active agents: `[agent for agent in agents if agent.active]`. Much cleaner than append loops. But I avoid complex nested comprehensions - readability matters more than being clever. If it needs more than 2 conditions or nested logic, I use regular loops."

---

### **🎯 EXERCISE 14: Master Lambda Functions (20 minutes)**

**TASK: Understand when lambda is useful (and when it's not)**

```python
# Create: test_lambda.py

# EXPERIMENT 1: Lambda basics
# Regular function
def square(x):
    return x ** 2

# Lambda (anonymous function)
square_lambda = lambda x: x ** 2

print(square(5))
print(square_lambda(5))

# EXPERIMENT 2: Lambda with map, filter, sorted
numbers = [1, 2, 3, 4, 5]

# Map: apply function to all items
squared = list(map(lambda x: x ** 2, numbers))
print(f"Squared: {squared}")

# Filter: keep items matching condition
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Evens: {evens}")

# EXPERIMENT 3: Sorting with lambda (YOUR USE CASE!)
tasks = [
    {"name": "task1", "priority": 5},
    {"name": "task2", "priority": 1},
    {"name": "task3", "priority": 8},
    {"name": "task4", "priority": 3},
]

# Sort by priority (high to low)
sorted_tasks = sorted(tasks, key=lambda t: t["priority"], reverse=True)
print("\nSorted by priority:")
for task in sorted_tasks:
    print(f"  {task['name']}: priority {task['priority']}")

# EXPERIMENT 4: Lambda in callbacks
def retry_with_callback(operation, on_success, on_error):
    try:
        result = operation()
        on_success(result)
    except Exception as e:
        on_error(e)

# Use lambdas as callbacks
retry_with_callback(
    operation=lambda: 10 / 2,
    on_success=lambda r: print(f"Success: {r}"),
    on_error=lambda e: print(f"Error: {e}")
)

# EXPERIMENT 5: When NOT to use lambda
# BAD - complex logic in lambda (unreadable!)
bad_lambda = lambda x: x ** 2 if x > 0 else -x ** 2 if x < 0 else 0

# GOOD - use regular function
def process_number(x):
    if x > 0:
        return x ** 2
    elif x < 0:
        return -x ** 2
    else:
        return 0

# Lambda rule: If it needs more than one line, use def!
```

**✅ MASTERY CHECK:**
- When is lambda better than def?
- Rewrite a sorting operation with lambda
- **Interview:** "Explain lambda functions"
  - **Your answer:** "Anonymous functions for simple operations. I use them for sorting and filtering - like `sorted(tasks, key=lambda t: t['priority'])` to sort by priority. Lambda is cleaner than defining a separate function for one-liners. But if logic is complex, I use regular def functions for readability."

---

### **🎯 EXERCISE 15: Master *args and **kwargs (30 minutes)**

**TASK: Handle variable arguments like a pro**

```python
# Create: test_args_kwargs.py

# EXPERIMENT 1: *args - variable positional arguments
def sum_all(*args):
    print(f"args type: {type(args)}")  # tuple
    print(f"args: {args}")
    return sum(args)

print(sum_all(1, 2, 3))
print(sum_all(1, 2, 3, 4, 5, 6))

# EXPERIMENT 2: **kwargs - variable keyword arguments
def create_agent(**kwargs):
    print(f"kwargs type: {type(kwargs)}")  # dict
    print(f"kwargs: {kwargs}")
    return kwargs

agent = create_agent(name="analyzer", temperature=0.3, max_tokens=2000)
print(agent)

# EXPERIMENT 3: Combining positional, *args, **kwargs
def route_task(task, *agents, **config):
    print(f"Task: {task}")
    print(f"Agents: {agents}")
    print(f"Config: {config}")
    
    # Process all agents
    for agent in agents:
        print(f"  Routing to {agent}")
    
    # Use config
    timeout = config.get("timeout", 30)
    print(f"  Timeout: {timeout}s")

route_task(
    "analyze data",
    "agent1", "agent2", "agent3",
    timeout=60,
    retries=3
)

# EXPERIMENT 4: Unpacking arguments
def process(x, y, z):
    return x + y + z

# Unpack list with *
values = [1, 2, 3]
print(process(*values))  # Same as process(1, 2, 3)

# Unpack dict with **
config = {"x": 1, "y": 2, "z": 3}
print(process(**config))  # Same as process(x=1, y=2, z=3)

# EXPERIMENT 5: Your retry decorator pattern
def retry_decorator(max_retries=3, backoff=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    # Call original function with original args!
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    wait = backoff ** attempt
                    print(f"Retry {attempt + 1}, wait {wait}s")
                    import time
                    time.sleep(wait)
        return wrapper
    return decorator

@retry_decorator(max_retries=3, backoff=2)
def unstable_api_call(endpoint, data):
    import random
    if random.random() < 0.5:
        raise Exception("API Error")
    return f"Success: {endpoint} with {data}"

# The decorator handles retries for ANY function signature!
result = unstable_api_call("/data", {"key": "value"})
print(result)

# EXPERIMENT 6: Forwarding arguments (YOUR pattern)
class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def _request(self, method, endpoint, **kwargs):
        # kwargs could be: timeout, headers, data, etc.
        print(f"{method} {self.base_url}{endpoint}")
        print(f"Options: {kwargs}")
        return "response"
    
    def get(self, endpoint, **kwargs):
        return self._request("GET", endpoint, **kwargs)
    
    def post(self, endpoint, **kwargs):
        return self._request("POST", endpoint, **kwargs)

client = APIClient("https://api.example.com")
client.get("/users", timeout=30, headers={"Auth": "token"})
client.post("/data", timeout=60, data={"key": "value"})
```

**✅ MASTERY CHECK:**
- Explain the difference between *args and **kwargs
- Why are they useful for decorators?
- **Interview:** "Have you used *args/**kwargs?"
  - **Your answer:** "Yes, in my retry decorator. The decorator needs to work with any function signature - functions with different numbers of arguments. Using *args and **kwargs, I forward all arguments to the wrapped function without knowing them in advance. This makes the decorator generic - works with any function."

---

### **🎯 EXERCISE 16: Master Context Managers (with statement) (30 minutes)**

**TASK: Understand resource management and build your own context manager**

```python
# Create: test_context_managers.py

# EXPERIMENT 1: Why context managers?
# BAD - manual cleanup (easy to forget!)
file = open("data.txt", "w")
file.write("data")
# file.close()  # What if we forget? What if exception happens?

# GOOD - automatic cleanup
with open("data.txt", "w") as file:
    file.write("data")
# File automatically closed, even if exception occurs!

# EXPERIMENT 2: Multiple resources
with open("input.txt", "r") as infile, open("output.txt", "w") as outfile:
    data = infile.read()
    outfile.write(data.upper())
# Both files closed automatically

# EXPERIMENT 3: Build your own context manager (class-based)
class Timer:
    def __enter__(self):
        import time
        self.start = time.time()
        print("Timer started")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        elapsed = time.time() - self.start
        print(f"Timer stopped: {elapsed:.4f}s")
        # Return False to propagate exceptions
        return False

with Timer():
    # Code to time
    total = sum(range(1000000))
    print(f"Sum: {total}")

# EXPERIMENT 4: Build with decorator (easier!)
from contextlib import contextmanager

@contextmanager
def database_connection(db_name):
    # Setup (before yield)
    print(f"Connecting to {db_name}")
    connection = f"Connection to {db_name}"
    
    try:
        yield connection  # This is what 'as' receives
    finally:
        # Cleanup (after yield, always runs)
        print(f"Closing connection to {db_name}")

with database_connection("users_db") as conn:
    print(f"Using {conn}")
    print("Querying data...")
# Cleanup happens automatically

# EXPERIMENT 5: Your API rate limiter as context manager
@contextmanager
def rate_limit_window(max_calls, window_seconds):
    import time
    calls = []
    
    def check_limit():
        now = time.time()
        # Remove old calls
        nonlocal calls
        calls = [t for t in calls if now - t < window_seconds]
        
        if len(calls) >= max_calls:
            oldest = calls[0]
            wait = window_seconds - (now - oldest)
            print(f"Rate limit reached, waiting {wait:.2f}s")
            time.sleep(wait)
        
        calls.append(time.time())
    
    try:
        yield check_limit
    finally:
        print(f"Made {len(calls)} calls in {window_seconds}s window")

# Use it
with rate_limit_window(max_calls=3, window_seconds=1) as check:
    for i in range(5):
        check()  # Automatically enforces rate limit
        print(f"API call {i + 1}")

# EXPERIMENT 6: Error handling in context managers
@contextmanager
def safe_operation(operation_name):
    print(f"Starting {operation_name}")
    try:
        yield
    except Exception as e:
        print(f"Error in {operation_name}: {e}")
        # Could log, send alert, etc.
        raise  # Re-raise after handling
    finally:
        print(f"Finished {operation_name}")

with safe_operation("data processing"):
    print("Processing...")
    # raise Exception("Something went wrong")  # Try uncommenting
```

**✅ MASTERY CHECK:**
- Explain __enter__ and __exit__
- Why is 'with' better than manual cleanup?
- **Interview:** "Have you used context managers?"
  - **Your answer:** "Yes, for resource management. File operations, database connections - anything that needs cleanup. I also built a custom timer context manager for performance profiling during development. Context managers guarantee cleanup happens, even if exceptions occur. Much safer than manual try/finally everywhere."

---

### **🎯 EXERCISE 17: Master Generators (yield) (30 minutes)**

**TASK: Understand lazy evaluation and memory efficiency**

```python
# Create: test_generators.py

# EXPERIMENT 1: List vs Generator (memory)
# List - loads ALL into memory
def get_numbers_list(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result

numbers_list = get_numbers_list(1000000)
print(f"List created: {len(numbers_list)} items")

# Generator - produces items on demand
def get_numbers_generator(n):
    for i in range(n):
        yield i ** 2  # Yields one at a time!

numbers_gen = get_numbers_generator(1000000)
print(f"Generator created: {numbers_gen}")  # Not evaluated yet!

# Use generator
first_five = [next(numbers_gen) for _ in range(5)]
print(f"First 5: {first_five}")

# EXPERIMENT 2: Generator expressions (like list comprehensions)
# List comprehension - creates list in memory
squares_list = [x ** 2 for x in range(1000000)]

# Generator expression - lazy evaluation
squares_gen = (x ** 2 for x in range(1000000))

print(f"List: {type(squares_list)}")
print(f"Generator: {type(squares_gen)}")

# EXPERIMENT 3: Processing large files (YOUR use case!)
def read_large_file(filename):
    """Memory efficient - reads line by line"""
    with open(filename, 'r') as f:
        for line in f:
            yield line.strip()

# Write test file
with open("large_file.txt", "w") as f:
    for i in range(100):
        f.write(f"Line {i}\n")

# Process WITHOUT loading entire file into memory
for line in read_large_file("large_file.txt"):
    if "50" in line:
        print(f"Found: {line}")
        break  # Can stop early!

# EXPERIMENT 4: Pipeline of generators (POWERFUL!)
def read_logs(filename):
    with open(filename, 'r') as f:
        for line in f:
            yield line

def filter_errors(lines):
    for line in lines:
        if "ERROR" in line:
            yield line

def extract_timestamp(lines):
    for line in lines:
        # Simulate timestamp extraction
        yield line.split()[0] if line else ""

# Create test log
with open("app.log", "w") as f:
    f.write("2024-01-01 INFO: Started\n")
    f.write("2024-01-01 ERROR: Connection failed\n")
    f.write("2024-01-02 INFO: Processing\n")
    f.write("2024-01-02 ERROR: Timeout\n")

# Pipeline - each step is lazy!
logs = read_logs("app.log")
errors = filter_errors(logs)
timestamps = extract_timestamp(errors)

print("\nError timestamps:")
for ts in timestamps:
    print(f"  {ts}")

# EXPERIMENT 5: Your agent task stream (practical use case)
def task_stream():
    """Simulate real-time task arrivals"""
    import time
    import random
    
    tasks = [
        "analyze data",
        "generate report", 
        "send email",
        "update database",
        "create backup"
    ]
    
    for task in tasks:
        time.sleep(0.5)  # Simulate delay
        priority = random.randint(1, 10)
        yield {"task": task, "priority": priority}

def high_priority_only(task_stream):
    """Filter to only high priority (≥7)"""
    for task in task_stream:
        if task["priority"] >= 7:
            yield task

# Process tasks as they arrive (not all at once!)
print("\nProcessing high-priority tasks:")
for task in high_priority_only(task_stream()):
    print(f"  {task['task']} (priority: {task['priority']})")

# EXPERIMENT 6: Infinite generators (careful!)
def fibonacci():
    """Infinite Fibonacci sequence"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Take only what you need
fib = fibonacci()
first_10 = [next(fib) for _ in range(10)]
print(f"\nFirst 10 Fibonacci: {first_10}")

# EXPERIMENT 7: Generator with send() (advanced!)
def running_average():
    total = 0
    count = 0
    while True:
        value = yield total / count if count > 0 else 0
        total += value
        count += 1

avg = running_average()
next(avg)  # Prime the generator
print(f"After 10: {avg.send(10)}")
print(f"After 20: {avg.send(20)}")
print(f"After 30: {avg.send(30)}")
```

**✅ MASTERY CHECK:**
- Explain yield vs return
- Why are generators memory efficient?
- When would you use generators in production?
- **Interview:** "Have you used generators?"
  - **Your answer:** "Yes, for processing large datasets without loading everything into memory. Like streaming agent tasks or processing large log files line by line. Generators yield items on demand - memory efficient and can stop early. I'd use them for Revalgo's email processing if dealing with large batches - process one email at a time instead of loading all into memory."

---

### **🎯 EXERCISE 18: DSA Fundamentals - Interview Safety Net (2 hours)**

**TASK: Cover the basics Ashish might ask - practical, not theoretical**

```python
# Create: test_dsa_basics.py

# ============================================
# PART 1: TIME COMPLEXITY (Big O) - 20 minutes
# ============================================

print("=== TIME COMPLEXITY ===\n")

# O(1) - Constant time
def get_first_element(arr):
    return arr[0] if arr else None  # Always 1 operation

# O(n) - Linear time
def find_element(arr, target):
    for item in arr:  # n operations
        if item == target:
            return True
    return False

# O(n²) - Quadratic time
def find_duplicates_naive(arr):
    duplicates = []
    for i in range(len(arr)):  # n times
        for j in range(i + 1, len(arr)):  # n times
            if arr[i] == arr[j]:
                duplicates.append(arr[i])
    return duplicates

# O(log n) - Logarithmic time (binary search)
def binary_search(sorted_arr, target):
    left, right = 0, len(sorted_arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if sorted_arr[mid] == target:
            return mid
        elif sorted_arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# TEST THEM
import time

def measure_time(func, *args):
    start = time.time()
    result = func(*args)
    elapsed = time.time() - start
    return elapsed, result

# See the difference!
small_list = list(range(1000))
large_list = list(range(100000))

t1, _ = measure_time(get_first_element, small_list)
t2, _ = measure_time(get_first_element, large_list)
print(f"O(1): Small={t1:.6f}s, Large={t2:.6f}s (almost same!)")

t1, _ = measure_time(find_element, small_list, 999)
t2, _ = measure_time(find_element, large_list, 99999)
print(f"O(n): Small={t1:.6f}s, Large={t2:.6f}s (grows linearly)")

# ============================================
# PART 2: HASH MAPS (Dict) - YOUR SUPERPOWER - 20 minutes
# ============================================

print("\n=== HASH MAPS ===\n")

# Problem: Find duplicates efficiently
def find_duplicates_efficient(arr):
    seen = {}  # Hash map: O(1) lookup!
    duplicates = []
    
    for item in arr:
        if item in seen:  # O(1) lookup
            if seen[item] == 1:  # First time seeing duplicate
                duplicates.append(item)
            seen[item] += 1
        else:
            seen[item] = 1
    
    return duplicates

# Compare
test_arr = [1, 2, 3, 2, 4, 5, 3, 6]
print(f"Array: {test_arr}")
print(f"Duplicates: {find_duplicates_efficient(test_arr)}")

# YOUR USE CASE: Caching API responses
class APICache:
    def __init__(self):
        self.cache = {}  # Hash map
    
    def get(self, key):
        return self.cache.get(key)  # O(1)
    
    def set(self, key, value):
        self.cache[key] = value  # O(1)
    
    def has(self, key):
        return key in self.cache  # O(1)

cache = APICache()
cache.set("query1", "result1")
print(f"\nCached 'query1': {cache.get('query1')}")
print(f"Has 'query2': {cache.has('query2')}")

# ============================================
# PART 3: TWO POINTERS - Common Interview Pattern - 15 minutes
# ============================================

print("\n=== TWO POINTERS ===\n")

# Problem: Remove duplicates from sorted array IN-PLACE
def remove_duplicates(arr):
    if not arr:
        return 0
    
    # Two pointers
    write_pos = 1  # Where to write next unique element
    
    for read_pos in range(1, len(arr)):
        if arr[read_pos] != arr[read_pos - 1]:
            arr[write_pos] = arr[read_pos]
            write_pos += 1
    
    return write_pos  # Length of unique elements

test = [1, 1, 2, 2, 2, 3, 4, 4, 5]
print(f"Original: {test}")
length = remove_duplicates(test)
print(f"After removing duplicates: {test[:length]}")

# Problem: Valid palindrome
def is_palindrome(s):
    # Remove non-alphanumeric and lowercase
    s = ''.join(c.lower() for c in s if c.isalnum())
    
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

print(f"\n'racecar' palindrome: {is_palindrome('racecar')}")
print(f"'A man, a plan, a canal: Panama' palindrome: {is_palindrome('A man, a plan, a canal: Panama')}")

# ============================================
# PART 4: RECURSION - The Basics - 20 minutes
# ============================================

print("\n=== RECURSION ===\n")

# EXAMPLE 1: Factorial
def factorial(n):
    # Base case
    if n <= 1:
        return 1
    # Recursive case
    return n * factorial(n - 1)

print(f"5! = {factorial(5)}")

# EXAMPLE 2: Fibonacci (inefficient recursive)
def fib_recursive(n):
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)

# EXAMPLE 3: Fibonacci (optimized with memoization)
def fib_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

print(f"Fib(10) recursive: {fib_recursive(10)}")
print(f"Fib(30) memoized: {fib_memo(30)}")  # Much faster!

# YOUR USE CASE: Recursive directory traversal
import os

def count_python_files(directory, count=0):
    try:
        for item in os.listdir(directory):
            path = os.path.join(directory, item)
            if os.path.isdir(path):
                # Recursive case
                count = count_python_files(path, count)
            elif item.endswith('.py'):
                # Base case action
                count += 1
    except PermissionError:
        pass
    return count

# Count Python files in your project
project_path = r"d:\Resume preparation full\VertexAutoGPT-Kata- copy\src"
py_files = count_python_files(project_path)
print(f"\nPython files in project: {py_files}")

# ============================================
# PART 5: STACK - Common Interview Pattern - 15 minutes
# ============================================

print("\n=== STACK (LIFO) ===\n")

# Python list as stack
stack = []
stack.append(1)  # push
stack.append(2)
stack.append(3)
top = stack.pop()  # pop
print(f"Stack operations: pushed 1,2,3, popped {top}, remaining: {stack}")

# Problem: Valid parentheses (CLASSIC!)
def is_valid_parentheses(s):
    stack = []
    pairs = {'(': ')', '[': ']', '{': '}'}
    
    for char in s:
        if char in pairs:  # Opening bracket
            stack.append(char)
        else:  # Closing bracket
            if not stack or pairs[stack.pop()] != char:
                return False
    
    return len(stack) == 0  # All opened brackets closed

test_cases = [
    "()[]{}",
    "([{}])",
    "([)]",
    "{[}]"
]

print("\nValid Parentheses:")
for test in test_cases:
    print(f"  '{test}': {is_valid_parentheses(test)}")

# YOUR USE CASE: Undo/Redo functionality
class UndoStack:
    def __init__(self):
        self.actions = []
    
    def do_action(self, action):
        self.actions.append(action)
        print(f"Did: {action}")
    
    def undo(self):
        if self.actions:
            action = self.actions.pop()
            print(f"Undid: {action}")
            return action
        return None

undo_stack = UndoStack()
undo_stack.do_action("Create agent")
undo_stack.do_action("Configure temperature")
undo_stack.do_action("Run task")
undo_stack.undo()
undo_stack.undo()

# ============================================
# PART 6: SLIDING WINDOW - For Revalgo! - 20 minutes
# ============================================

print("\n=== SLIDING WINDOW ===\n")

# Problem: Maximum sum of k consecutive elements
def max_sum_subarray(arr, k):
    if len(arr) < k:
        return None
    
    # Initial window
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    # Slide window
    for i in range(k, len(arr)):
        window_sum = window_sum - arr[i - k] + arr[i]
        max_sum = max(max_sum, window_sum)
    
    return max_sum

test = [1, 4, 2, 10, 23, 3, 1, 0, 20]
print(f"Array: {test}")
print(f"Max sum of 4 consecutive: {max_sum_subarray(test, 4)}")

# YOUR USE CASE: Moving average for email priorities
def moving_average(values, window_size):
    if len(values) < window_size:
        return []
    
    averages = []
    window_sum = sum(values[:window_size])
    averages.append(window_sum / window_size)
    
    for i in range(window_size, len(values)):
        window_sum = window_sum - values[i - window_size] + values[i]
        averages.append(window_sum / window_size)
    
    return averages

priorities = [5, 3, 8, 2, 9, 1, 7, 4, 6]
print(f"\nPriorities: {priorities}")
print(f"Moving avg (window=3): {moving_average(priorities, 3)}")

# ============================================
# PART 7: STRING MANIPULATION - Revalgo Core! - 10 minutes
# ============================================

print("\n=== STRING MANIPULATION ===\n")

# Problem: Reverse words in a sentence
def reverse_words(s):
    return ' '.join(s.split()[::-1])

print(f"Original: 'Hello World from Python'")
print(f"Reversed: '{reverse_words('Hello World from Python')}'")

# Problem: Is anagram?
def is_anagram(s1, s2):
    # Method 1: Sort
    return sorted(s1) == sorted(s2)
    
    # Method 2: Count (more efficient)
    # from collections import Counter
    # return Counter(s1) == Counter(s2)

print(f"\n'listen' and 'silent' anagram: {is_anagram('listen', 'silent')}")

# YOUR USE CASE: Extract email metadata
def parse_email_subject(subject):
    """Extract key info from email subject"""
    # Remove extra whitespace
    subject = ' '.join(subject.split())
    
    # Extract patterns
    import re
    order_id = re.search(r'Order[#:\s]*(\w+)', subject, re.IGNORECASE)
    priority = 'HIGH' if any(word in subject.upper() for word in ['URGENT', 'ASAP', 'CRITICAL']) else 'NORMAL'
    
    return {
        'subject': subject,
        'order_id': order_id.group(1) if order_id else None,
        'priority': priority
    }

test_subjects = [
    "URGENT: Order #12345 issue",
    "Question about Order 67890",
    "General inquiry about pricing"
]

print("\nEmail Subject Parsing:")
for subject in test_subjects:
    parsed = parse_email_subject(subject)
    print(f"  {parsed}")

print("\n" + "="*50)
print("DSA FUNDAMENTALS COMPLETE!")
print("="*50)
```

**✅ MASTERY CHECK:**

**If Ashish asks:**

1. **"Explain Big O notation"**
   - "Time complexity - how performance scales with input size. O(1) is constant, O(n) is linear, O(n²) is quadratic. I optimize hot paths in my code to avoid O(n²) - like using hash maps for O(1) lookups instead of nested loops."

2. **"What's a hash map and when do you use it?"**
   - "Key-value store with O(1) average lookup. I use dicts for caching API responses in my projects - check if result exists before making expensive API call. Also for counting duplicates, tracking seen items, any fast lookup scenario."

3. **"Explain recursion"**
   - "Function calling itself until base case. Like traversing directories in my project - for each folder, recurse into subfolders. Key is base case to prevent infinite loops. I prefer iteration when possible for better performance, use recursion when problem is naturally recursive like trees."

4. **"What's the difference between list and dict in Python?"**
   - "List: ordered sequence, O(n) search, O(1) append. Dict: key-value pairs, O(1) lookup by key, unordered (before Python 3.7). I use lists for sequences/ordering, dicts for fast lookups. My agent cache uses dict for O(1) response retrieval."

5. **"How would you find duplicates efficiently?"**
   - "Hash map. Iterate once, count occurrences. O(n) time, O(n) space. Better than nested loops which is O(n²). I'd use this for detecting duplicate emails in Revalgo's system."

6. **"What's a sliding window?"**
   - "Technique for array problems with consecutive elements. Instead of recalculating sum of each window from scratch (O(n*k)), slide by removing leftmost and adding rightmost element (O(n)). Useful for moving averages, max/min in windows. Could use for email priority trends over time."

---

**Continue in next message with Day 3-6 practical exercises...**

---

## 🎯 **START NOW - DAY 1 EXERCISE 1**

Open your terminal and run:

```powershell
cd "d:\Resume preparation full\VertexAutoGPT-Kata- copy\src\entaera\core"
python
```

Then copy-paste the Enum experiments from Exercise 1 and START EXPERIMENTING! 

**You're not reading - you're DOING!** 🔥💪

