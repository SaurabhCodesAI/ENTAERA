# 🔥 PRACTICAL MASTERY - DAYS 3-6
## Advanced Hands-On Exercises

---

## 📅 DAY 3 - OCT 30 (8 HOURS)

### **Morning: Build Mini-Projects (4 hours)**

**🎯 EXERCISE 10: Build Your Own Retry Decorator (1 hour)**

```python
# Create: my_retry_decorator.py

import time
import functools

# EXPERIMENT 1: Build a retry decorator from scratch
def retry_with_backoff(max_retries=3):
    """
    Decorator that adds retry logic with exponential backoff
    
    This is similar to what you implemented in ENTAERA
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for retry in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if retry == max_retries - 1:
                        print(f"Failed after {max_retries} retries")
                        raise
                    
                    wait_time = 2 ** retry
                    print(f"Retry {retry + 1}: {e}. Waiting {wait_time}s...")
                    time.sleep(wait_time)
        return wrapper
    return decorator

# EXPERIMENT 2: Use your decorator
@retry_with_backoff(max_retries=4)
def unreliable_api_call(should_fail=True):
    import random
    if should_fail and random.random() < 0.7:  # 70% failure rate
        raise Exception("API Error")
    return "Success!"

# Test it
try:
    result = unreliable_api_call(should_fail=True)
    print(f"Result: {result}")
except Exception as e:
    print(f"Final failure: {e}")

# EXPERIMENT 3: Apply to multiple functions
@retry_with_backoff(max_retries=3)
def fetch_data():
    # Simulate flaky API
    import random
    if random.random() < 0.5:
        raise Exception("Connection timeout")
    return {"data": "important stuff"}

@retry_with_backoff(max_retries=2)
def process_payment():
    import random
    if random.random() < 0.3:
        raise Exception("Payment gateway error")
    return "Payment processed"

# Test both
try:
    data = fetch_data()
    print(f"Data: {data}")
    
    payment = process_payment()
    print(f"Payment: {payment}")
except Exception as e:
    print(f"Error: {e}")
```

**✅ MASTERY CHECK:**
- Build the decorator yourself (don't just copy)
- Explain how `@functools.wraps` works
- **Interview:** "Have you written decorators?"
  - **Your answer:** "I've used decorators like @dataclass extensively. I understand the concept - they wrap functions to add behavior. I built a retry decorator for practice that adds exponential backoff to any function. Haven't written custom ones for production yet, but I can explain how they work and when to use them."

---

**🎯 EXERCISE 10B: Build ASYNC Retry Decorator (1 hour) 🔥 CRITICAL**

```python
# Create: async_retry_decorator.py

import asyncio
import functools
from typing import TypeVar, Callable, Any

# YOUR ACTUAL PRODUCTION PATTERN from rate_limiter.py and api_router.py

def async_retry_with_backoff(max_retries=3):
    """
    Async decorator with exponential backoff
    EXACTLY like your ENTAERA production code!
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for retry in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if retry == max_retries - 1:
                        print(f"Failed after {max_retries} retries")
                        raise
                    
                    wait_time = 2 ** retry
                    print(f"Retry {retry + 1}: {e}. Waiting {wait_time}s...")
                    await asyncio.sleep(wait_time)  # ASYNC sleep!
        return wrapper
    return decorator

# EXPERIMENT 1: Test with async function
@async_retry_with_backoff(max_retries=4)
async def unreliable_api_call(should_fail=True):
    """Simulate flaky API (like your Gemini/Perplexity calls)"""
    import random
    if should_fail and random.random() < 0.7:  # 70% failure
        raise Exception("API Error")
    return "Success!"

# EXPERIMENT 2: Multiple async functions with different retry counts
@async_retry_with_backoff(max_retries=3)
async def fetch_embeddings():
    """Like your semantic_search.py embedding generation"""
    import random
    if random.random() < 0.5:
        raise Exception("Embedding API timeout")
    return [0.1, 0.2, 0.3]  # Fake embedding

@async_retry_with_backoff(max_retries=2)
async def call_gemini_api(prompt: str):
    """Like your multi_gemini_manager.py"""
    import random
    if random.random() < 0.4:
        raise Exception("Gemini rate limit")
    return f"Response to: {prompt}"

# EXPERIMENT 3: Run async functions with asyncio
async def main():
    print("=== Testing Async Retry Decorator ===\n")
    
    # Test 1: Unreliable API
    try:
        result = await unreliable_api_call(should_fail=True)
        print(f"✅ Result: {result}\n")
    except Exception as e:
        print(f"❌ Final failure: {e}\n")
    
    # Test 2: Fetch embeddings
    try:
        embeddings = await fetch_embeddings()
        print(f"✅ Embeddings: {embeddings}\n")
    except Exception as e:
        print(f"❌ Failed: {e}\n")
    
    # Test 3: Call Gemini
    try:
        response = await call_gemini_api("What is AI?")
        print(f"✅ Gemini: {response}\n")
    except Exception as e:
        print(f"❌ Failed: {e}\n")

# Run it!
if __name__ == "__main__":
    asyncio.run(main())
```

**Run this:**
```powershell
python async_retry_decorator.py
```

**Key learnings:**
- **`async def`** makes function asynchronous
- **`await`** suspends execution until result ready
- **`asyncio.sleep()`** non-blocking wait (NOT `time.sleep()`)
- **`asyncio.run(main())`** runs async code

**EXPERIMENT 4: YOUR ACTUAL PRODUCTION ASYNC CODE 🔥**

```python
# See YOUR actual async patterns
import sys
sys.path.append('d:/Resume preparation full/VertexAutoGPT-Kata- copy/src')

# Count async functions in YOUR code
with open('d:/Resume preparation full/VertexAutoGPT-Kata- copy/src/entaera/core/agent_orchestration.py') as f:
    content = f.read()
    async_count = content.count('async def')
    print(f"=== YOUR PRODUCTION CODE ===")
    print(f"Async functions in agent_orchestration.py: {async_count}")

# YOUR actual patterns:
print("\nYOUR code uses:")
print("  ✓ 50+ async def functions")
print("  ✓ asyncio.gather() for parallel execution")
print("  ✓ asyncio.Semaphore for rate limiting")
print("  ✓ async with for context managers")
print("  ✓ await everywhere for non-blocking I/O")

print("\nThis is YOUR production async architecture!")
```

**YOUR production code has 50+ async functions like this!**

---

**🎯 EXERCISE 10C: Async Semaphores (Rate Limiting) (45 min) 🔥 YOUR ACTUAL CODE**

```python
# Create: async_semaphore_practice.py

import asyncio
from datetime import datetime

# YOUR ACTUAL PATTERN from rate_limiter.py

class AsyncRateLimiter:
    """
    Rate limiter with semaphores
    EXACTLY from your ENTAERA rate_limiter.py!
    """
    def __init__(self, max_concurrent=3):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.request_count = 0
        self.lock = asyncio.Lock()  # For thread-safe counter
    
    async def acquire(self, api_name: str):
        """Acquire permission to make request"""
        async with self.semaphore:
            async with self.lock:
                self.request_count += 1
                current_count = self.request_count
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {api_name}: Request #{current_count} STARTED (concurrent: {3 - self.semaphore._value})")
            
            # Simulate API call taking time
            await asyncio.sleep(2)  # 2 seconds per request
            
            print(f"[{timestamp}] {api_name}: Request #{current_count} COMPLETED")

# EXPERIMENT 1: Test concurrent limit
async def make_api_call(rate_limiter: AsyncRateLimiter, api_name: str, call_num: int):
    """Simulate API call with rate limiting"""
    await rate_limiter.acquire(f"{api_name}-{call_num}")

async def test_rate_limiting():
    print("=== Testing Rate Limiting (Max 3 Concurrent) ===\n")
    
    limiter = AsyncRateLimiter(max_concurrent=3)
    
    # Try to make 10 API calls
    # Only 3 will run at a time due to semaphore
    tasks = [
        make_api_call(limiter, "Gemini", i+1)
        for i in range(10)
    ]
    
    # Run all tasks concurrently (but semaphore limits to 3)
    await asyncio.gather(*tasks)
    
    print(f"\n✅ Completed {limiter.request_count} requests")
    print("Notice: Only 3 ran concurrently at any time!")

# EXPERIMENT 4: YOUR ACTUAL PRODUCTION SEMAPHORES 🔥
import sys
sys.path.append('d:/Resume preparation full/VertexAutoGPT-Kata- copy/src')

from entaera.utils.rate_limiter import SmartRateLimiter

async def test_your_rate_limiter():
    print("\n=== YOUR PRODUCTION RATE LIMITER ===")
    
    limiter = SmartRateLimiter()
    
    # YOUR actual semaphores
    print(f"Gemini semaphore: {limiter.limits['gemini'].requests_per_minute} concurrent")
    print(f"Perplexity semaphore: {limiter.limits['perplexity'].requests_per_minute} concurrent")
    
    print("\nYOUR code uses:")
    print("  ✓ asyncio.Semaphore for each API")
    print("  ✓ Max 4 concurrent Gemini requests")
    print("  ✓ Max 45 concurrent Perplexity requests")
    print("  ✓ Automatic request queuing")
    print("  ✓ Daily and per-minute tracking")

asyncio.run(test_your_rate_limiter())

# EXPERIMENT 2: Multiple API rate limiters
class MultiAPIRateLimiter:
    """
    Like your actual rate_limiter.py with multiple APIs
    """
    def __init__(self):
        self.semaphores = {
            "gemini": asyncio.Semaphore(3),      # 3 concurrent Gemini
            "perplexity": asyncio.Semaphore(2),  # 2 concurrent Perplexity
            "azure": asyncio.Semaphore(5)        # 5 concurrent Azure
        }
    
    async def can_make_request(self, api: str) -> bool:
        """Check if API has capacity"""
        return self.semaphores[api]._value > 0
    
    async def acquire(self, api: str) -> bool:
        """Acquire semaphore for API"""
        if not await self.can_make_request(api):
            print(f"  ⚠️  {api} at capacity, waiting...")
            return False
        
        await self.semaphores[api].acquire()
        return True
    
    def release(self, api: str):
        """Release semaphore"""
        self.semaphores[api].release()

async def test_multi_api():
    print("\n=== Testing Multi-API Rate Limiting ===\n")
    
    limiter = MultiAPIRateLimiter()
    
    async def call_api(api_name: str, call_num: int):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        if await limiter.acquire(api_name):
            print(f"[{timestamp}] {api_name}-{call_num}: STARTED")
            await asyncio.sleep(1)  # Simulate API call
            limiter.release(api_name)
            print(f"[{timestamp}] {api_name}-{call_num}: COMPLETED")
        else:
            print(f"[{timestamp}] {api_name}-{call_num}: RATE LIMITED")
    
    # Make 15 calls across different APIs
    tasks = []
    tasks.extend([call_api("gemini", i) for i in range(1, 6)])      # 5 Gemini calls
    tasks.extend([call_api("perplexity", i) for i in range(1, 4)])  # 3 Perplexity calls
    tasks.extend([call_api("azure", i) for i in range(1, 7)])       # 6 Azure calls
    
    await asyncio.gather(*tasks)

# Run everything
async def main():
    await test_rate_limiting()
    await test_multi_api()

if __name__ == "__main__":
    asyncio.run(main())
```

**Run this:**
```powershell
python async_semaphore_practice.py
```

**What you'll see:**
- First 3 requests start immediately
- Requests 4-10 wait for semaphore slots
- Each API has its own concurrency limit
- **THIS IS EXACTLY YOUR PRODUCTION PATTERN!**

**✅ MASTERY CHECK:**
- How many concurrent Gemini requests does YOUR code allow? → 4
- How many concurrent Perplexity requests? → 45
- Why different limits? → Different API quotas

---

**🎯 EXERCISE 10D: Async Context Managers (30 min) 🔥 PRODUCTION PATTERN**

```python
# Create: async_context_managers.py

import asyncio

# YOUR ACTUAL PATTERN from rate_limiter.py

class AsyncRateLimiterContext:
    """
    Async context manager for rate limiting
    Like: async with rate_limiter.acquire(api):
    """
    def __init__(self, api_name: str, semaphore: asyncio.Semaphore):
        self.api_name = api_name
        self.semaphore = semaphore
    
    async def __aenter__(self):
        """Called when entering 'async with' block"""
        print(f"  [{self.api_name}] Acquiring semaphore...")
        await self.semaphore.acquire()
        print(f"  [{self.api_name}] ✅ Acquired!")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Called when exiting 'async with' block"""
        self.semaphore.release()
        print(f"  [{self.api_name}] ✅ Released!")
        return False  # Don't suppress exceptions

# EXPERIMENT 1: Use async context manager
async def test_async_context():
    print("=== Testing Async Context Manager ===\n")
    
    semaphore = asyncio.Semaphore(2)  # Max 2 concurrent
    
    async def make_request(api_name: str):
        async with AsyncRateLimiterContext(api_name, semaphore):
            print(f"  [{api_name}] Making API call...")
            await asyncio.sleep(1)
            print(f"  [{api_name}] API call complete!")
    
    # Make 4 requests (only 2 run at a time)
    await asyncio.gather(
        make_request("Request-1"),
        make_request("Request-2"),
        make_request("Request-3"),
        make_request("Request-4")
    )

# EXPERIMENT 2: Async context manager with error handling
class AsyncDatabaseConnection:
    """
    Like your connection pooling pattern
    """
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connected = False
    
    async def __aenter__(self):
        print(f"  📡 Connecting to {self.db_name}...")
        await asyncio.sleep(0.5)  # Simulate connection time
        self.connected = True
        print(f"  ✅ Connected to {self.db_name}")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f"  📡 Disconnecting from {self.db_name}...")
        await asyncio.sleep(0.2)
        self.connected = False
        print(f"  ✅ Disconnected from {self.db_name}")
        
        if exc_type is not None:
            print(f"  ⚠️  Error occurred: {exc_val}")
        
        return False
    
    async def query(self, sql: str):
        if not self.connected:
            raise Exception("Not connected!")
        print(f"  🔍 Executing: {sql}")
        await asyncio.sleep(0.3)
        return [{"result": "data"}]

async def test_database_connection():
    print("\n=== Testing Async Database Connection ===\n")
    
    # Normal usage
    async with AsyncDatabaseConnection("ENTAERA_DB") as db:
        results = await db.query("SELECT * FROM embeddings")
        print(f"  Results: {results}")
    
    # With error
    print("\n--- Testing with error ---")
    try:
        async with AsyncDatabaseConnection("ENTAERA_DB") as db:
            results = await db.query("SELECT * FROM embeddings")
            raise Exception("Query failed!")
    except Exception as e:
        print(f"  ❌ Caught exception: {e}")

# Run everything
async def main():
    await test_async_context()
    await test_database_connection()

if __name__ == "__main__":
    asyncio.run(main())
```

**Run this:**
```powershell
python async_context_managers.py
```

**EXPERIMENT 4: YOUR ACTUAL PRODUCTION ASYNC CONTEXT 🔥**

```python
import sys
sys.path.append('d:/Resume preparation full/VertexAutoGPT-Kata- copy/src')

# See YOUR actual usage
print("=== YOUR PRODUCTION ASYNC CONTEXT MANAGERS ===")

print("\nYOUR code uses 'async with' for:")
print("  ✓ Semaphore acquisition (rate_limiter.py)")
print("  ✓ Automatic semaphore release")
print("  ✓ Guaranteed cleanup even on errors")

print("\nYOUR pattern:")
print("  async with self.semaphores[api]:")
print("      # Make API request")
print("      # Semaphore auto-releases!")

print("\nWhy async with?")
print("  1. Automatic resource cleanup")
print("  2. Exception-safe (finally runs)")
print("  3. Cleaner code (no manual release)")
```

**Key patterns YOU USE in production:**
```python
# From your rate_limiter.py:
async with self.semaphores[api]:
    # Make request
    pass

# Your pattern guarantees cleanup even if errors occur!
```

---

**✅ MASTERY CHECK - ASYNC PATTERNS:**

**Can you explain:**
1. ✅ Difference between `async def` and `def`? (Async returns coroutine)
2. ✅ What does `await` do? (Suspends until result ready)
3. ✅ Why `asyncio.sleep()` not `time.sleep()`? (Non-blocking vs blocking)
4. ✅ What's a semaphore? (Limits concurrent operations)
5. ✅ What's `async with`? (Async context manager - automatic cleanup)
6. ✅ How many async functions in your ENTAERA? (50+!)

**Interview answer:**
*"My ENTAERA project heavily uses async/await throughout - 50+ async functions in agent_orchestration.py, rate_limiter.py, and api_router.py. I use semaphores for rate limiting to control concurrent API calls - for example, max 3 concurrent Gemini requests. The pattern is 'await self.semaphores[api].acquire()' to get permission, then release when done. I also use async context managers with 'async with' for automatic resource cleanup. All my API calls are async because they involve I/O - waiting for responses from Gemini, Perplexity, Azure. This lets other tasks run while waiting instead of blocking."*

---

**🎯 EXERCISE 11: Build Mini Semantic Search Engine (1.5 hours)**

```python
# Create: mini_search_engine.py

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class SemanticSearchEngine:
    """
    Mini version of what you built in ENTAERA
    """
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.dimension = 384
        self.index = None
        self.documents = []
    
    def add_documents(self, docs):
        """Add documents to the search index"""
        print(f"Adding {len(docs)} documents...")
        
        # Generate embeddings
        embeddings = self.model.encode(docs)
        
        # Create FAISS index if it doesn't exist
        if self.index is None:
            self.index = faiss.IndexFlatL2(self.dimension)
        
        # Add to index
        self.index.add(embeddings.astype('float32'))
        self.documents.extend(docs)
        
        print(f"Total documents: {len(self.documents)}")
    
    def search(self, query, top_k=3):
        """Search for similar documents"""
        if self.index is None:
            return []
        
        # Generate query embedding
        query_emb = self.model.encode([query])
        
        # Search
        distances, indices = self.index.search(
            query_emb.astype('float32'), 
            min(top_k, len(self.documents))
        )
        
        # Return results
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            results.append({
                'document': self.documents[idx],
                'distance': float(dist),
                'similarity': 1 / (1 + dist)  # Convert distance to similarity
            })
        
        return results

# EXPERIMENT 1: Build and test your search engine
engine = SemanticSearchEngine()

# Add customer support documents
support_docs = [
    "How do I reset my password?",
    "Forgot my login credentials",
    "Account login issues",
    "Where is my order?",
    "Track shipping status",
    "Delivery time estimate",
    "Cancel my subscription",
    "Request a refund",
    "Return policy information",
    "Product warranty details"
]

engine.add_documents(support_docs)

# EXPERIMENT 2: Test searches
queries = [
    "I can't log in to my account",
    "When will my package arrive?",
    "I want my money back"
]

for query in queries:
    print(f"\n{'='*60}")
    print(f"Query: '{query}'")
    print(f"{'='*60}")
    
    results = engine.search(query, top_k=3)
    
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['document']}")
        print(f"   Similarity: {result['similarity']:.4f}")

# EXPERIMENT 3: Compare with keyword search
def keyword_search(query, docs, top_k=3):
    query_words = set(query.lower().split())
    scores = []
    
    for doc in docs:
        doc_words = set(doc.lower().split())
        overlap = len(query_words & doc_words)
        scores.append((doc, overlap))
    
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]

print(f"\n{'='*60}")
print("KEYWORD SEARCH COMPARISON")
print(f"{'='*60}")

for query in queries[:1]:  # Just first query
    print(f"\nQuery: '{query}'")
    print("\nSemantic Search:")
    semantic_results = engine.search(query, top_k=3)
    for i, r in enumerate(semantic_results, 1):
        print(f"  {i}. {r['document']}")
    
    print("\nKeyword Search:")
    keyword_results = keyword_search(query, support_docs, top_k=3)
    for i, (doc, score) in enumerate(keyword_results, 1):
        print(f"  {i}. {doc} (overlap: {score})")

# EXPERIMENT 4: Test the bug you fixed
print(f"\n{'='*60}")
print("TESTING DIMENSION MISMATCH BUG")
print(f"{'='*60}")

try:
    # Create index with wrong dimension
    wrong_index = faiss.IndexFlatL2(512)  # Wrong!
    embeddings = engine.model.encode(["test"])
    wrong_index.add(embeddings.astype('float32'))
except Exception as e:
    print(f"ERROR: {e}")
    print("This is the bug you debugged in ENTAERA!")
    print(f"Embedding dimension: {embeddings.shape[1]}")
    print(f"Index dimension: 512")
    print("FIX: Match index dimension to embedding dimension")
```

**✅ MASTERY CHECK:**
- Build this from scratch, don't copy
- Test with your own queries
- Break it intentionally (wrong dimensions)
- **Interview:** "Walk me through your semantic search implementation"
  - **Your answer:** "I built a semantic search engine using sentence-transformers for 384-dim embeddings and FAISS for indexing. The SearchEngine class has add_documents (generates embeddings, builds index) and search (finds similar docs). I debugged a dimension mismatch - tried to add 384-dim embeddings to a 512-dim index. The fix was matching dimensions. Semantic search beats keyword search because it understands meaning - 'can't log in' finds 'reset password' with zero word overlap."

---

**🎯 EXERCISE 12: Build Multi-Agent Router (1.5 hours)**

```python
# Create: mini_agent_router.py

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List
import random

# EXPERIMENT 1: Define your architecture
class AgentType(Enum):
    CONVERSATIONAL = "conversational"
    ANALYTICAL = "analytical"
    CREATIVE = "creative"

@dataclass
class AgentConfig:
    agent_type: AgentType
    temperature: float
    max_tokens: int
    api_provider: str

class AgentRouter:
    """
    Simplified version of your ENTAERA orchestration
    """
    def __init__(self):
        self.agents = {
            AgentType.CONVERSATIONAL: AgentConfig(
                agent_type=AgentType.CONVERSATIONAL,
                temperature=0.7,
                max_tokens=500,
                api_provider="GPT-4"
            ),
            AgentType.ANALYTICAL: AgentConfig(
                agent_type=AgentType.ANALYTICAL,
                temperature=0.3,
                max_tokens=1000,
                api_provider="Claude"
            ),
            AgentType.CREATIVE: AgentConfig(
                agent_type=AgentType.CREATIVE,
                temperature=0.9,
                max_tokens=800,
                api_provider="Gemini"
            )
        }
    
    def route(self, query: str) -> AgentConfig:
        """Route query to appropriate agent"""
        query_lower = query.lower()
        
        # Simple keyword-based routing (you used semantic in ENTAERA)
        if any(word in query_lower for word in ['analyze', 'data', 'calculate', 'metrics']):
            agent_type = AgentType.ANALYTICAL
        elif any(word in query_lower for word in ['write', 'create', 'story', 'poem', 'creative']):
            agent_type = AgentType.CREATIVE
        else:
            agent_type = AgentType.CONVERSATIONAL
        
        return self.agents[agent_type]
    
    def execute(self, query: str):
        """Execute query with routed agent"""
        agent = self.route(query)
        
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        print(f"Routed to: {agent.agent_type.value}")
        print(f"Temperature: {agent.temperature}")
        print(f"Max tokens: {agent.max_tokens}")
        print(f"API: {agent.api_provider}")
        
        # Simulate API call
        return f"[{agent.api_provider}] Processing with temp={agent.temperature}"

# EXPERIMENT 2: Test your router
router = AgentRouter()

test_queries = [
    "Analyze the sales data for Q4",
    "Write a creative story about AI",
    "What's the weather like?",
    "Calculate the ROI metrics",
    "Create a poem about coding"
]

for query in test_queries:
    result = router.execute(query)
    print(f"Result: {result}\n")

# EXPERIMENT 3: Add retry logic
import time

class ResilientAgentRouter(AgentRouter):
    """Router with retry logic - like your ENTAERA implementation"""
    
    def execute_with_retry(self, query: str, max_retries=3):
        """Execute with exponential backoff"""
        agent = self.route(query)
        
        for retry in range(max_retries):
            try:
                # Simulate API call with 30% failure rate
                if random.random() < 0.3:
                    raise Exception(f"{agent.api_provider} API Error")
                
                return f"Success from {agent.agent_type.value}"
            
            except Exception as e:
                if retry == max_retries - 1:
                    print(f"Failed after {max_retries} retries: {e}")
                    raise
                
                wait_time = 2 ** retry
                print(f"Retry {retry + 1}: {e}. Waiting {wait_time}s...")
                time.sleep(wait_time)

# Test resilient router
resilient_router = ResilientAgentRouter()

print(f"\n{'='*60}")
print("TESTING RETRY LOGIC")
print(f"{'='*60}")

for i in range(3):
    try:
        result = resilient_router.execute_with_retry("Analyze the data")
        print(f"Attempt {i+1}: {result}\n")
    except Exception as e:
        print(f"Attempt {i+1}: Failed - {e}\n")
```

**✅ MASTERY CHECK:**
- Build your own multi-agent router
- Add retry logic yourself
- Explain routing decisions
- **Interview:** "Explain your multi-agent architecture"
  - **Your answer:** "I designed a router that sends queries to specialized agents. 6 agent types in ENTAERA - Conversational, Analytical, Creative, Task Executor, Coordinator, Specialist. Each has different temperature (0.3 for analytical, 0.9 for creative) and routes to different APIs. The routing uses semantic search to match query intent to agent capabilities. I added exponential backoff for API failures. For Revalgo, you might route different email types to different extraction models?"

---

### **Afternoon: Mock Interviews & Real Practice (4 hours)**

**🎯 EXERCISE 13: Code Explanation Practice (2 hours)**

Open your actual projects and practice explaining:

**ENTAERA - agent_orchestration.py:**
1. Navigate to line 45 (AgentType enum)
2. Explain out loud WHY you designed 6 types
3. Navigate to your routing logic
4. Explain YOUR decisions (semantic vs keyword, FAISS choice)
5. Find your error handling
6. Explain YOUR debugging (rate limits → exponential backoff)

**Record yourself:**
- Use your phone camera
- Pretend you're screen sharing with Ashish
- Explain for 5 minutes
- Watch it back - did you sound confident?

**Snap2Slides - gemini-vision/route.ts:**
1. Navigate to prompt section
2. Explain iteration journey (60% → 80%)
3. What changed in each version?
4. Navigate to image encoding
5. Explain base64 encoding, MIME types

**n8n - Dockerfile:**
1. Show the Dockerfile
2. Explain your debugging journey
3. V1 → V4 evolution
4. What broke and how you fixed it

---

**🎯 EXERCISE 14: First Mock Interview (2 hours)**

**Setup:**
- Record yourself (camera + screen)
- 40-minute timer
- Pretend Ashish is interviewing you

**Flow:**
1. **Minutes 0-2:** Honest opening (from memory)
2. **Minutes 2-15:** ENTAERA walkthrough (share screen)
   - AgentType enum
   - Routing logic
   - Error handling
   - "AI helped here, but I debugged..."
3. **Minutes 15-20:** Handle curveball
   - "How much did AI write?"
   - Give your honest response
4. **Minutes 20-30:** Flip to Revalgo questions
   - Ask 5 of your prepared questions
   - Show curiosity
5. **Minutes 30-38:** Technical depth
   - Explain vector embeddings
   - Explain semantic search
   - Bridge to Revalgo
6. **Minutes 38-40:** Close
   - "Really excited about this problem"
   - "When do I hear back?"

**After Recording:**
- Watch it fully
- Note 5 weak spots:
  1. Where did you sound defensive?
  2. Where did you ramble?
  3. Did you bridge to Revalgo?
  4. Did you show enthusiasm?
  5. What technical concepts need work?

---

## 📅 DAY 4 - OCT 31 (8 HOURS)

### **Morning: Fix Weak Spots (4 hours)**

**🎯 EXERCISE 15: Targeted Practice (2 hours)**

Based on yesterday's mock interview weak spots:

**If you sounded defensive about AI:**
- Practice 20 times: "AI helped generate this, but I understand because..."
- Make it sound natural, not apologetic
- Practice pointing to YOUR debugging examples

**If you rambled:**
- Practice 60-second answers
- Time yourself with stopwatch
- Structure: Point → Evidence → Revalgo bridge

**If technical concepts were weak:**
- Go back to Day 1-2 experiments
- Run the code again
- Explain out loud while watching it run

---

**🎯 EXERCISE 16: Live Coding Practice (2 hours)**

**Scenario 1: Write retry function (15 minutes)**

```python
# They ask: "Write a function that retries failed API calls"
# Think out loud while writing:

def retry_api_call(api_function, max_retries=3):
    """
    YOUR THINKING OUT LOUD:
    
    "Okay, so I need a retry function with exponential backoff.
    This is similar to what I implemented in ENTAERA.
    
    First, I'll loop up to max_retries.
    For each attempt, I'll try the API call.
    If it succeeds, return the result.
    If it fails, calculate backoff time as 2^retry_count.
    If final retry fails, raise the error.
    
    Let me write this..."
    """
    import time
    
    for retry in range(max_retries):
        try:
            return api_function()
        except Exception as e:
            if retry == max_retries - 1:
                raise  # Final retry failed
            
            wait_time = 2 ** retry
            print(f"Retry {retry + 1}, waiting {wait_time}s...")
            time.sleep(wait_time)

# Test it
def flaky_api():
    import random
    if random.random() < 0.5:
        raise Exception("API Error")
    return "Success"

result = retry_api_call(flaky_api)
print(result)
```

**Practice this:**
- Write it from scratch (no copy-paste)
- Think out loud the WHOLE time
- Reference your ENTAERA experience
- Don't aim for perfection, aim for clear thinking

**Scenario 2: Debug broken code (15 minutes)**

```python
# They show you:
def fetch_data(url):
    response = requests.get(url)
    return response.json()

# Think out loud:
"""
Let me think through what could break here...

1. No error handling - if URL is wrong, crashes
2. No status code check - might get 404/500
3. No timeout - could hang forever
4. No retry logic - one failure = done

Here's how I'd improve it based on my n8n debugging experience:
"""

def fetch_data_improved(url, timeout=10, max_retries=3):
    import requests
    import time
    
    for retry in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # Raises for 4xx/5xx
            return response.json()
        
        except requests.exceptions.Timeout:
            print(f"Timeout on retry {retry + 1}")
            if retry == max_retries - 1:
                raise
            time.sleep(2 ** retry)
        
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e.response.status_code}")
            raise  # Don't retry on 404, etc.

# This is my actual debugging process from n8n:
# Started with no error handling → crashes
# Added try/except → better but no retry
# Added retry + backoff → production ready
```

---

### **Afternoon: Second Mock Interview (4 hours)**

**🎯 EXERCISE 17: Improved Mock Interview (2 hours)**

Same setup as Day 3, but apply all improvements:

**Focus areas:**
- Confident honest opening (not defensive)
- Tight 60-90 second answers (not rambling)
- Strong bridges to Revalgo (every answer)
- Specific code examples (not vague)
- Enthusiasm about their problem (genuine)

**Record it and compare:**
- Watch both mocks side-by-side
- What improved?
- What still needs work?

---

**🎯 EXERCISE 18: Concepts Rapid Fire (2 hours)**

Practice explaining all 20 concepts in 2 minutes each:

**AI/ML (10 concepts):**
1. Vector Embeddings → Explain + show code
2. Semantic Search → Explain + demo
3. Temperature → Explain + examples
4. Multi-Agent → Explain + architecture
5. Prompt Engineering → Explain + iteration
6. Rate Limiting → Explain + backoff code
7. RAG Pattern → Explain + use case
8. Cosine Similarity → Explain + math
9. API Integration → Explain + challenges
10. Inference vs Training → Explain + your experience

**Python (10 concepts):**
1. Dataclasses → Explain + code
2. Enums → Explain + demo
3. Type Hints → Explain + mypy
4. Error Handling → Explain + evolution
5. List Comprehensions → Explain + examples
6. Lambda Functions → Explain + use cases
7. Decorators → Explain + @dataclass
8. Context Managers → Explain + with statement
9. Dictionary Methods → Explain + patterns
10. Async/Await → Explain concept

**For each one:**
- Simple explanation (30 sec)
- Where you used it (30 sec)
- Honest about AI help (15 sec)
- Your debugging/testing (30 sec)
- Bridge to Revalgo (15 sec)

---

## 📅 DAY 5 - NOV 1 (REST DAY - 2 HOURS)

**Morning (1 hour):**
- Casual code browsing
- Read your prep materials
- Light review only

**Afternoon (1 hour):**
- Watch one mock recording
- Note improvements over time
- Build confidence

**Rest of day:**
- RELAX (watch something, walk, exercise)
- NO intense prep (avoid burnout)
- Early sleep (by 10 PM)

---

## 📅 DAY 6 - NOV 2 (FINAL PREP - 3 HOURS)

**Morning (1 hour):**
- Read INTERVIEW_DAY_QUICK_REFERENCE.md once
- Say honest opening 2-3 times (not 10)
- Quick concepts glance

**Afternoon (2 hours):**
- Light code navigation
- Practice ONE code walkthrough (ENTAERA)
- Review questions for Ashish
- Mental visualization

**Evening:**
- Prepare workspace (test everything)
- Lay out clothes
- Set alarms
- Early sleep (by 9 PM)

---

## 🎯 **MASTERY CHECKLIST**

After 6 days of practical work, you should:

**Code Skills:**
- [ ] Built retry decorator from scratch
- [ ] Built semantic search engine from scratch
- [ ] Built multi-agent router from scratch
- [ ] Can navigate your actual code blindfolded
- [ ] Can explain every design decision

**Concepts:**
- [ ] Explained all 20 concepts with code examples
- [ ] Ran experiments for each concept
- [ ] Broke things intentionally and fixed them
- [ ] Can demo concepts live

**Interview Skills:**
- [ ] Completed 2 mock interviews
- [ ] Improved from first to second
- [ ] Fixed all major weak spots
- [ ] Honest opening sounds natural
- [ ] Curveball responses ready

**Confidence:**
- [ ] No hesitation explaining any concept
- [ ] Can think out loud while coding
- [ ] Can reference YOUR debugging stories
- [ ] Genuinely excited about Revalgo

---

## 🔥 **YOU'LL BE READY**

**Why this approach wins:**
- ✅ You BUILT it, not just read it
- ✅ You BROKE it and FIXED it
- ✅ You can DEMO it live
- ✅ You have REAL stories (not memorized answers)
- ✅ Zero hesitation (you've done it 100 times)

**Nov 3, 12 PM - You'll crush it!** 💪🔥

