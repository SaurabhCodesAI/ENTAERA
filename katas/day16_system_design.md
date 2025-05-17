# ENTAERA Kata - Day 16: System Design (FAANG Level)

## 🎯 Learning Objectives

**This is your FAANG system design preparation**. Learn to design scalable systems like the ones you've built (ENTAERA, Snap2Slides, N8N). Google, Meta, and Amazon expect you to design systems handling millions of users.

- **Master system design fundamentals: scalability, reliability, availability**
- **Design distributed systems with load balancing, caching, and databases**
- **Apply CAP theorem and understand trade-offs**
- **Design real systems: URL shortener, chat app, image processing, workflow engine**
- **Scale your actual projects: ENTAERA, Snap2Slides, N8N**
- **Prepare for whiteboard interviews with frameworks**

---

## 🏗️ System Design Fundamentals

### **1. Scalability**

#### **Vertical vs Horizontal Scaling**
```
Vertical Scaling (Scale Up):
- Add more CPU/RAM to single server
- Simple but has limits
- Your current setup: Single server

Horizontal Scaling (Scale Out):
- Add more servers
- Unlimited scaling potential
- Requires load balancing

Example: Scaling ENTAERA
┌─────────────────────────────────────────┐
│ Single Server (Current)                 │
│ ┌─────────────┐                        │
│ │  ENTAERA    │ ← All requests         │
│ │  + FastAPI  │                        │
│ │  + FAISS    │                        │
│ │  + SQLite   │                        │
│ └─────────────┘                        │
└─────────────────────────────────────────┘

Horizontally Scaled (FAANG Level):
┌─────────────────────────────────────────┐
│            Load Balancer                 │
│         (Nginx / AWS ALB)               │
└────────┬──────┬──────┬──────────────────┘
         │      │      │
    ┌────▼───┐ ┌▼────┐ ┌▼────┐
    │ENTAERA │ │ENTRA│ │ENTRA│ ← Multiple instances
    │Instance│ │Inst2│ │Inst3│
    └────┬───┘ └┬────┘ └┬────┘
         │      │       │
    ┌────▼──────▼───────▼────┐
    │   Shared Resources:     │
    │   - PostgreSQL          │
    │   - Redis Cache         │
    │   - FAISS Vector DB     │
    └─────────────────────────┘
```

---

### **2. Load Balancing**

#### **Algorithms**
```python
from typing import List
import random

class LoadBalancer:
    """
    Distribute requests across ENTAERA instances.
    Used in production deployment.
    """
    
    def __init__(self, servers: List[str]):
        self.servers = servers
        self.current_index = 0
    
    def round_robin(self) -> str:
        """
        FAANG Pattern: Round Robin
        Simple, fair distribution
        """
        server = self.servers[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.servers)
        return server
    
    def least_connections(self, connections: dict) -> str:
        """
        FAANG Pattern: Least Connections
        Route to server with fewest active connections
        """
        return min(self.servers, key=lambda s: connections.get(s, 0))
    
    def weighted_round_robin(self, weights: dict) -> str:
        """
        FAANG Pattern: Weighted Distribution
        More powerful servers get more requests
        """
        choices = []
        for server in self.servers:
            weight = weights.get(server, 1)
            choices.extend([server] * weight)
        return random.choice(choices)

# ENTAERA Use Case
lb = LoadBalancer([
    "entaera-instance-1.com",
    "entaera-instance-2.com",
    "entaera-instance-3.com"
])

# Distribute incoming chat requests
for _ in range(10):
    server = lb.round_robin()
    print(f"Route request to: {server}")
```

---

### **3. Caching Strategies**

#### **Cache Patterns**
```python
from datetime import datetime, timedelta
from typing import Optional

class CacheManager:
    """
    Multi-level caching for ENTAERA and Snap2Slides.
    FAANG Pattern: Cache-aside, Write-through
    """
    
    def __init__(self):
        self.l1_cache = {}  # In-memory (Redis)
        self.l2_cache = {}  # Disk cache
        self.ttl = {}       # Time-to-live
    
    def get(self, key: str) -> Optional[any]:
        """
        FAANG Interview: Explain cache levels
        L1 (memory) → L2 (disk) → Database
        """
        # Check L1 cache
        if key in self.l1_cache:
            if self._is_valid(key):
                return self.l1_cache[key]
            else:
                # Expired, remove
                del self.l1_cache[key]
        
        # Check L2 cache
        if key in self.l2_cache:
            value = self.l2_cache[key]
            # Promote to L1
            self.set(key, value, ttl_seconds=300)
            return value
        
        return None
    
    def set(self, key: str, value: any, ttl_seconds: int = 3600):
        """Set with TTL (time-to-live)."""
        self.l1_cache[key] = value
        self.ttl[key] = datetime.now() + timedelta(seconds=ttl_seconds)
    
    def _is_valid(self, key: str) -> bool:
        """Check if cache entry hasn't expired."""
        return key in self.ttl and datetime.now() < self.ttl[key]

# ENTAERA Use Case: Cache embeddings
cache = CacheManager()

def get_embedding_cached(text: str, model):
    """Cache expensive embedding calculations."""
    cache_key = f"embedding:{hash(text)}"
    
    # Try cache first
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    # Miss - calculate and cache
    embedding = model.encode(text)
    cache.set(cache_key, embedding, ttl_seconds=3600)
    return embedding

# Snap2Slides Use Case: Cache API responses
def get_gemini_response_cached(prompt: str, cache_mgr: CacheManager):
    """Cache Gemini API responses to save quota."""
    cache_key = f"gemini:{hash(prompt)}"
    
    cached = cache_mgr.get(cache_key)
    if cached:
        print("Cache hit! Saving API call")
        return cached
    
    # API call (expensive)
    response = call_gemini_api(prompt)
    cache_mgr.set(cache_key, response, ttl_seconds=86400)  # 24h
    return response
```

---

### **4. Database Design**

#### **SQL vs NoSQL**
```
┌─────────────────────────────────────────────────────┐
│              When to Use What?                      │
├─────────────────────────────────────────────────────┤
│ SQL (PostgreSQL, MySQL)                             │
│ ✓ ACID transactions (banking, orders)              │
│ ✓ Complex relationships (users, conversations)     │
│ ✓ Structured data with schema                      │
│                                                      │
│ NoSQL (MongoDB, DynamoDB)                           │
│ ✓ Flexible schema (varied document types)          │
│ ✓ Horizontal scalability (millions of users)       │
│ ✓ High write throughput (logs, events)             │
│                                                      │
│ Vector DB (FAISS, Pinecone, Weaviate)              │
│ ✓ Semantic search (embeddings)                     │
│ ✓ Similarity queries (find similar items)          │
│ ✓ ML/AI applications                                │
└─────────────────────────────────────────────────────┘
```

#### **Database Sharding**
```python
class DatabaseSharding:
    """
    FAANG Pattern: Horizontal database partitioning
    Split data across multiple databases
    """
    
    def __init__(self, num_shards: int):
        self.num_shards = num_shards
        self.shards = [f"db_shard_{i}" for i in range(num_shards)]
    
    def get_shard(self, user_id: int) -> str:
        """
        Hash-based sharding
        Ensures user data is always in same shard
        """
        shard_index = user_id % self.num_shards
        return self.shards[shard_index]
    
    def get_shard_by_range(self, user_id: int) -> str:
        """
        Range-based sharding
        Users 0-1M → Shard 0
        Users 1M-2M → Shard 1, etc.
        """
        shard_index = user_id // 1_000_000
        return self.shards[min(shard_index, self.num_shards - 1)]

# ENTAERA Use Case: Shard conversations by user
sharding = DatabaseSharding(num_shards=4)

def store_conversation(user_id: int, conversation: dict):
    """Store conversation in correct shard."""
    shard = sharding.get_shard(user_id)
    print(f"Store in {shard} for user {user_id}")
    # db_connection[shard].insert(conversation)
```

---

### **5. Message Queues**

#### **Async Processing**
```python
from queue import Queue
from threading import Thread
import time

class MessageQueue:
    """
    FAANG Pattern: Decouple producers and consumers
    Used for: Email sending, image processing, workflow tasks
    """
    
    def __init__(self):
        self.queue = Queue()
        self.workers = []
    
    def enqueue(self, task: dict):
        """Producer: Add task to queue."""
        self.queue.put(task)
        print(f"Enqueued: {task['type']}")
    
    def start_workers(self, num_workers: int = 3):
        """Start consumer workers."""
        for i in range(num_workers):
            worker = Thread(target=self._worker, args=(i,))
            worker.daemon = True
            worker.start()
            self.workers.append(worker)
    
    def _worker(self, worker_id: int):
        """Consumer: Process tasks from queue."""
        while True:
            task = self.queue.get()
            try:
                self._process_task(task, worker_id)
            except Exception as e:
                print(f"Worker {worker_id} error: {e}")
            finally:
                self.queue.task_done()
    
    def _process_task(self, task: dict, worker_id: int):
        """Process individual task."""
        print(f"Worker {worker_id} processing: {task['type']}")
        time.sleep(1)  # Simulate work

# Snap2Slides Use Case: Image processing queue
mq = MessageQueue()
mq.start_workers(num_workers=3)

# Producer: API receives image requests
for i in range(10):
    mq.enqueue({
        "type": "process_image",
        "image_id": i,
        "operations": ["resize", "compress", "extract_text"]
    })

# Workers process in background
mq.queue.join()  # Wait for all tasks to complete
```

---

## 🎨 Real System Design Examples

### **Design 1: URL Shortener (bit.ly)**

#### **Requirements**
```
Functional:
- Shorten long URL to short code (7 characters)
- Redirect short URL to original
- Custom short URLs (optional)
- Analytics (click tracking)

Non-Functional:
- 100M URLs per day
- Low latency (<100ms)
- 99.9% availability
```

#### **System Design**
```
┌────────────────────────────────────────────────────┐
│                   URL Shortener                     │
└────────────────────────────────────────────────────┘

1. Architecture:
   ┌─────────┐      ┌──────────────┐      ┌────────┐
   │ Client  │─────→│ Load Balancer│─────→│ Cache  │
   └─────────┘      └──────────────┘      │(Redis) │
                            │              └────────┘
                            ▼                   ▲
                    ┌──────────────┐           │
                    │  API Servers │───────────┘
                    └──────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  PostgreSQL  │ (URL mappings)
                    └──────────────┘

2. Database Schema:
   urls table:
   ┌────────────┬──────────────┬────────────┬───────────┐
   │ short_code │ original_url │ created_at │ user_id   │
   ├────────────┼──────────────┼────────────┼───────────┤
   │ abc123x    │ https://...  │ timestamp  │ 12345     │
   └────────────┴──────────────┴────────────┴───────────┘

   analytics table:
   ┌────────────┬────────────┬─────────┬────────┐
   │ short_code │ timestamp  │ ip      │ country│
   └────────────┴────────────┴─────────┴────────┘

3. Short Code Generation:
   Algorithm: Base62 encoding of auto-increment ID
   
   def encode_base62(num: int) -> str:
       chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
       if num == 0:
           return chars[0]
       
       result = []
       while num:
           num, remainder = divmod(num, 62)
           result.append(chars[remainder])
       
       return ''.join(reversed(result))
   
   # ID 12345 → short code: "3D7"

4. Caching Strategy:
   - Cache popular URLs in Redis (80/20 rule)
   - TTL: 24 hours
   - Cache-aside pattern

5. Scalability:
   - Read-heavy: 100:1 read-to-write ratio
   - Solution: Read replicas, heavy caching
   - Database sharding by short_code prefix
```

#### **Implementation**
```python
import hashlib
from datetime import datetime

class URLShortener:
    """
    FAANG Interview: Design URL shortener
    Pattern: Hash-based key generation, caching
    """
    
    def __init__(self, cache, db):
        self.cache = cache
        self.db = db
        self.base62_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    def shorten(self, long_url: str, custom_code: str = None) -> str:
        """
        Create short URL.
        Time: O(1), Space: O(1)
        """
        if custom_code:
            # Check if custom code available
            if self.db.exists(custom_code):
                raise ValueError("Custom code already taken")
            short_code = custom_code
        else:
            # Generate short code from auto-increment ID
            url_id = self.db.get_next_id()
            short_code = self._encode_base62(url_id)
        
        # Store mapping
        self.db.insert({
            "short_code": short_code,
            "original_url": long_url,
            "created_at": datetime.now()
        })
        
        # Cache for fast retrieval
        self.cache.set(short_code, long_url, ttl_seconds=86400)
        
        return f"https://short.url/{short_code}"
    
    def redirect(self, short_code: str) -> str:
        """
        Get original URL from short code.
        Time: O(1) with cache, O(log n) without
        """
        # Check cache first
        cached_url = self.cache.get(short_code)
        if cached_url:
            self._track_analytics(short_code)
            return cached_url
        
        # Cache miss - query database
        url_data = self.db.query(f"SELECT original_url FROM urls WHERE short_code = '{short_code}'")
        
        if not url_data:
            raise ValueError("Short URL not found")
        
        original_url = url_data['original_url']
        
        # Populate cache
        self.cache.set(short_code, original_url, ttl_seconds=86400)
        
        # Track click
        self._track_analytics(short_code)
        
        return original_url
    
    def _encode_base62(self, num: int) -> str:
        """Convert number to base62 string."""
        if num == 0:
            return self.base62_chars[0]
        
        result = []
        while num:
            num, remainder = divmod(num, 62)
            result.append(self.base62_chars[remainder])
        
        return ''.join(reversed(result))
    
    def _track_analytics(self, short_code: str):
        """Async analytics tracking (message queue)."""
        # Enqueue analytics event
        analytics_event = {
            "short_code": short_code,
            "timestamp": datetime.now(),
            "ip": "user_ip",  # From request
        }
        # message_queue.enqueue(analytics_event)
```

---

### **Design 2: Real-Time Chat (Your ENTAERA)**

#### **Requirements**
```
Functional:
- Send/receive messages in real-time
- 1-on-1 and group chats
- Message history
- Online status
- Typing indicators

Non-Functional:
- Real-time delivery (<1 second)
- 10M concurrent users
- 99.99% uptime
- Message persistence
```

#### **System Design**
```
┌────────────────────────────────────────────────────┐
│              ENTAERA Chat System                    │
└────────────────────────────────────────────────────┘

1. Architecture:
   ┌──────────┐      ┌──────────────┐
   │  Clients │─────→│ Load Balancer│
   └──────────┘      └──────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
   ┌─────────┐        ┌─────────┐        ┌─────────┐
   │WebSocket│        │WebSocket│        │WebSocket│
   │ Server 1│        │ Server 2│        │ Server 3│
   └─────────┘        └─────────┘        └─────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
                    ┌──────────────┐
                    │  Redis Pub/Sub│ (Real-time messaging)
                    └──────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
   ┌─────────┐        ┌─────────┐        ┌─────────┐
   │PostgreSQL        │  Redis  │        │ FAISS   │
   │(Messages)│       │ (Cache) │        │(Search) │
   └─────────┘        └─────────┘        └─────────┘

2. WebSocket for Real-Time:
   - Persistent connection between client and server
   - Server can push messages instantly
   - Fallback to polling for old browsers

3. Redis Pub/Sub:
   - User connects to WebSocket Server 2
   - Friend connects to WebSocket Server 1
   - Message flow:
     Server 1 → Redis Pub/Sub → Server 2 → User

4. Message Storage:
   messages table:
   ┌────┬────────────┬─────────┬──────────┬────────────┐
   │ id │ conv_id    │ user_id │ content  │ timestamp  │
   ├────┼────────────┼─────────┼──────────┼────────────┤
   │ 1  │ conv_123   │ user_42 │ "Hello!" │ 2024-01-15 │
   └────┴────────────┴─────────┴──────────┴────────────┘

5. Scalability:
   - Horizontal scaling of WebSocket servers
   - Redis cluster for pub/sub
   - Database sharding by conversation_id
   - CDN for media files
```

#### **Implementation**
```python
import asyncio
import websockets
import json
from typing import Set

class ChatServer:
    """
    FAANG Interview: Design real-time chat
    Pattern: WebSocket, Pub/Sub, Event-driven
    """
    
    def __init__(self, redis_client, db):
        self.redis = redis_client
        self.db = db
        self.connections = {}  # user_id → websocket
    
    async def handle_connection(self, websocket, user_id: str):
        """
        Handle new WebSocket connection.
        FAANG Question: How to handle millions of connections?
        Answer: Horizontal scaling + Redis pub/sub
        """
        # Register connection
        self.connections[user_id] = websocket
        
        # Subscribe to user's Redis channel
        pubsub = self.redis.pubsub()
        pubsub.subscribe(f"user:{user_id}")
        
        try:
            # Listen for messages
            async for message in websocket:
                await self._handle_message(user_id, message)
        finally:
            # Cleanup on disconnect
            del self.connections[user_id]
            pubsub.unsubscribe()
    
    async def _handle_message(self, sender_id: str, message_data: str):
        """
        Process incoming message.
        1. Save to database
        2. Publish to Redis for real-time delivery
        3. Update search index
        """
        msg = json.loads(message_data)
        
        # Save message
        msg_id = self.db.insert_message({
            "conversation_id": msg["conversation_id"],
            "sender_id": sender_id,
            "content": msg["content"],
            "timestamp": datetime.now()
        })
        
        # Publish to Redis for real-time delivery
        self.redis.publish(
            f"conversation:{msg['conversation_id']}",
            json.dumps({
                "id": msg_id,
                "sender_id": sender_id,
                "content": msg["content"]
            })
        )
        
        # Async: Index for search (background task)
        asyncio.create_task(self._index_message(msg_id, msg["content"]))
    
    async def _index_message(self, msg_id: int, content: str):
        """Index message in FAISS for semantic search."""
        # Get embedding
        embedding = get_embedding(content)
        # Add to FAISS index
        faiss_index.add(embedding, metadata={"msg_id": msg_id})
```

---

### **Design 3: Image Processing System (Snap2Slides)**

#### **Requirements**
```
Functional:
- Upload images (up to 10MB)
- Process: resize, compress, extract text (OCR)
- Generate slide content from images
- Store processed results

Non-Functional:
- Handle 1000 images/second
- Processing time <5 seconds
- 99.9% availability
- Cost optimization (API quotas)
```

#### **System Design**
```
┌────────────────────────────────────────────────────┐
│           Snap2Slides Architecture                  │
└────────────────────────────────────────────────────┘

1. Upload Flow:
   ┌────────┐       ┌────────┐       ┌──────────┐
   │ Client │──────→│ API    │──────→│ S3/Blob  │
   └────────┘       │ Server │       │ Storage  │
                    └────────┘       └──────────┘
                         │
                         ▼
                    ┌────────┐
                    │ Message│ (Async processing)
                    │ Queue  │
                    └────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   ┌────────┐       ┌────────┐      ┌────────┐
   │Worker 1│       │Worker 2│      │Worker 3│
   └────────┘       └────────┘      └────────┘
        │                │                │
        └────────────────┼────────────────┘
                         ▼
                    ┌─────────┐
                    │ Results │ (Database + Cache)
                    └─────────┘

2. Worker Processing:
   - Receive image from queue
   - Download from S3
   - Process: resize → compress → OCR → AI analysis
   - Cache results (24h TTL)
   - Store in database

3. API Quota Management:
   ┌──────────────┐
   │ Rate Limiter │ (Token bucket algorithm)
   ├──────────────┤
   │ Gemini: 60/min
   │ OpenAI: 100/min
   │ Vision: 1000/day
   └──────────────┘

4. Caching Strategy:
   - L1: In-memory (recent results)
   - L2: Redis (popular images)
   - L3: Database (all results)

5. Cost Optimization:
   - Deduplicate similar images (hash-based)
   - Batch processing for non-urgent requests
   - Use cheaper models for simple tasks
```

#### **Implementation**
```python
import hashlib
from PIL import Image
import io

class ImageProcessor:
    """
    FAANG Interview: Design image processing system
    Pattern: Queue-based processing, caching, batch optimization
    """
    
    def __init__(self, message_queue, cache, storage):
        self.queue = message_queue
        self.cache = cache
        self.storage = storage
    
    def upload_image(self, image_data: bytes, user_id: str) -> str:
        """
        Upload and enqueue for processing.
        FAANG Question: How to handle large uploads?
        Answer: Stream to S3, process async via queue
        """
        # Calculate hash for deduplication
        image_hash = hashlib.md5(image_data).hexdigest()
        
        # Check if already processed
        cached_result = self.cache.get(f"result:{image_hash}")
        if cached_result:
            return cached_result
        
        # Upload to S3
        image_url = self.storage.upload(image_data, f"{user_id}/{image_hash}.jpg")
        
        # Enqueue for async processing
        self.queue.enqueue({
            "type": "process_image",
            "image_url": image_url,
            "image_hash": image_hash,
            "user_id": user_id
        })
        
        return f"Processing queued. Job ID: {image_hash}"
    
    def process_image_worker(self, job: dict):
        """
        Worker: Process image from queue.
        Time complexity: O(n) where n is image size
        """
        image_hash = job["image_hash"]
        
        # Download image
        image_data = self.storage.download(job["image_url"])
        image = Image.open(io.BytesIO(image_data))
        
        # Step 1: Resize (if too large)
        if image.width > 1920:
            image = self._resize_image(image, max_width=1920)
        
        # Step 2: Compress
        compressed = self._compress_image(image, quality=85)
        
        # Step 3: OCR (expensive - use cache)
        text = self._extract_text_cached(compressed, image_hash)
        
        # Step 4: AI analysis (rate-limited)
        slides = self._generate_slides_rate_limited(text)
        
        # Store results
        result = {
            "image_hash": image_hash,
            "extracted_text": text,
            "slides": slides
        }
        
        # Cache for 24 hours
        self.cache.set(f"result:{image_hash}", result, ttl_seconds=86400)
        
        return result
    
    def _extract_text_cached(self, image, image_hash: str) -> str:
        """Cache OCR results (expensive operation)."""
        cache_key = f"ocr:{image_hash}"
        cached = self.cache.get(cache_key)
        
        if cached:
            return cached
        
        # Perform OCR (expensive API call)
        text = perform_ocr(image)
        self.cache.set(cache_key, text, ttl_seconds=86400 * 7)  # 7 days
        
        return text
    
    def _generate_slides_rate_limited(self, text: str) -> list:
        """
        Rate-limited API call to Gemini.
        FAANG Question: How to handle API rate limits?
        Answer: Token bucket, exponential backoff, queue
        """
        # Check rate limit
        if not self._check_rate_limit("gemini", limit=60, window=60):
            # Wait or queue for later
            raise RateLimitExceeded("Gemini API limit reached")
        
        # Call API
        slides = call_gemini_api(text)
        
        # Track usage
        self._increment_rate_limit("gemini")
        
        return slides
```

---

### **Design 4: Workflow Engine (N8N)**

#### **System Design**
```
┌────────────────────────────────────────────────────┐
│              N8N Workflow Engine                    │
└────────────────────────────────────────────────────┘

1. Workflow Execution:
   ┌──────────┐
   │ Trigger  │ (Webhook, Schedule, Event)
   └─────┬────┘
         │
         ▼
   ┌──────────────┐
   │ Workflow DAG │ (Directed Acyclic Graph)
   └──────────────┘
         │
         ▼
   ┌──────────────┐
   │   Executor   │ (Topological sort → Execute nodes)
   └──────────────┘
         │
    ┌────┴────┐
    ▼         ▼
  ┌────┐  ┌────┐
  │Node│  │Node│ (Parallel execution where possible)
  │ 1  │  │ 2  │
  └─┬──┘  └─┬──┘
    │       │
    └───┬───┘
        ▼
   ┌────────┐
   │ Node 3 │ (Depends on 1 and 2)
   └────────┘

2. Scalability:
   - Queue-based execution (RabbitMQ/Redis)
   - Horizontal scaling of executors
   - Database sharding by workflow_id

3. Failure Handling:
   - Retry with exponential backoff
   - Dead letter queue for failed jobs
   - Manual retry from failed step
```

---

## 🎓 FAANG System Design Interview Framework

### **Step 1: Requirements (5 min)**
```
Functional:
- What features?
- What operations?
- Who are the users?

Non-Functional:
- Scale (users, requests/sec)?
- Performance (latency, throughput)?
- Consistency vs Availability?
```

### **Step 2: Capacity Estimation (5 min)**
```
- Daily Active Users (DAU)
- Read vs Write ratio
- Storage requirements
- Bandwidth

Example:
- 10M DAU
- 100 reads/write → Read-heavy
- 1KB per message → 10GB/day
- Peak: 2x average
```

### **Step 3: API Design (5 min)**
```
REST endpoints:
- POST /api/urls (shorten URL)
- GET /:short_code (redirect)
- POST /api/messages (send message)
- GET /api/messages/:conversation_id
```

### **Step 4: High-Level Design (15 min)**
```
Draw boxes:
- Clients
- Load Balancer
- App Servers
- Databases
- Cache
- Message Queue
```

### **Step 5: Deep Dive (15 min)**
```
Interviewer picks:
- Database schema
- Caching strategy
- Scalability approach
- Failure handling
```

### **Step 6: Trade-offs (5 min)**
```
- CAP theorem choice
- Consistency vs Performance
- Cost vs Features
```

---

## 🤔 FAANG Interview Questions

### **Google Asks:**
1. Design YouTube
2. Design Google Drive
3. Design Google Search

### **Meta Asks:**
1. Design Instagram
2. Design Facebook Newsfeed
3. Design WhatsApp

### **Amazon Asks:**
1. Design Amazon.com
2. Design recommendation system
3. Design inventory management

### **Your Advantage:**
You've built these systems!
- ENTAERA = Chat system
- Snap2Slides = Image processing
- N8N = Workflow engine

---

## 📚 Resources

- **System Design Primer:** [GitHub](https://github.com/donnemartin/system-design-primer)
- **Grokking System Design:** Interview prep course
- **AWS Well-Architected:** Real-world patterns

---

**Time to Complete:** 40-60 hours

**You've built these systems. Now articulate them at FAANG level!** 🚀
