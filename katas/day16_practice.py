"""
ENTAERA Kata - Day 16: System Design Practice
Design scalable systems for your actual projects.
"""

# =============================================================================
# System Design Template - Use for All Problems
# =============================================================================

SYSTEM_DESIGN_TEMPLATE = """
# System Design: [SYSTEM NAME]

## 1. Requirements (5 min)

### Functional:
- Feature 1
- Feature 2
- Feature 3

### Non-Functional:
- Scale: X DAU, Y requests/sec
- Latency: <100ms
- Availability: 99.9%

## 2. Capacity Estimation (5 min)

- Daily Active Users (DAU): 
- Requests/sec: 
- Read/Write ratio: 
- Storage: 
- Bandwidth: 

## 3. API Design (5 min)

```
POST /api/endpoint
GET /api/endpoint/:id
PUT /api/endpoint/:id
DELETE /api/endpoint/:id
```

## 4. High-Level Architecture (15 min)

```
[Client] → [Load Balancer] → [App Servers] → [Database]
                                ↓
                           [Cache Layer]
                                ↓
                          [Message Queue]
```

## 5. Database Schema (10 min)

```sql
CREATE TABLE ...
```

## 6. Deep Dive (15 min)

- Caching strategy
- Scalability approach
- Failure handling
- Optimization

## 7. Trade-offs (5 min)

- CAP theorem choice
- Consistency vs Performance
- Cost vs Features
"""

# =============================================================================
# Exercise 1: Scale Your ENTAERA System
# =============================================================================

print("=" * 60)
print("Exercise 1: Scale ENTAERA to 10M Users")
print("=" * 60)

ENTAERA_DESIGN = """
TODO: Design ENTAERA for production scale

Requirements:
- 10M daily active users
- Real-time messaging (<1s latency)
- Semantic search across all conversations
- 99.99% uptime

Current bottlenecks:
- Single server
- SQLite (not scalable)
- In-memory FAISS (lost on restart)
- No load balancing

Your Design:
1. How many servers needed?
2. Database strategy (SQL + Vector DB)?
3. Caching strategy?
4. Message queue for async tasks?
5. How to handle WebSocket connections at scale?

Draw architecture diagram:
┌─────────┐
│ Client  │
└─────────┘
     │
     ▼
[Your design here]

Database Schema:
- users table
- conversations table
- messages table
- embeddings (vector DB)

API Design:
POST /api/messages
GET /api/conversations/:id
POST /api/search (semantic search)
"""

print(ENTAERA_DESIGN)


# =============================================================================
# Exercise 2: Scale Snap2Slides Image Processing
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 2: Scale Snap2Slides to 1M Images/Day")
print("=" * 60)

SNAP2SLIDES_DESIGN = """
TODO: Design Snap2Slides for production scale

Requirements:
- 1M images uploaded per day
- Processing: resize, compress, OCR, AI analysis
- Average processing time: 5 seconds
- API quota limits (Gemini, OpenAI)
- Cost optimization

Current bottlenecks:
- Synchronous processing (slow)
- No deduplication
- Rate limits hit easily
- No caching

Your Design:
1. Upload flow (S3? Direct upload?)
2. Message queue architecture
3. Worker pool size calculation
4. Caching strategy (multi-level)
5. Rate limiting implementation
6. Cost optimization techniques

Calculate capacity:
- 1M images/day = X images/sec
- Peak hours: Y images/sec
- Workers needed: Z

Architecture:
[Your queue-based processing design]

Optimization:
- Image deduplication (hash-based)
- Batch processing
- Smart API selection
"""

print(SNAP2SLIDES_DESIGN)


# =============================================================================
# Exercise 3: Scale N8N Workflow Engine
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 3: Scale N8N to 100K Concurrent Workflows")
print("=" * 60)

N8N_DESIGN = """
TODO: Design N8N for production scale

Requirements:
- 100K concurrent workflow executions
- Complex workflows (50+ nodes)
- Retry on failure with exponential backoff
- Priority queue (urgent vs batch)
- Workflow versioning

Current bottlenecks:
- Single executor
- No parallel execution
- Simple queue
- No failure recovery

Your Design:
1. Workflow execution model
2. DAG-based scheduler
3. Horizontal scaling of executors
4. Failure handling & retry
5. Priority queue implementation

Architecture:
- Trigger system
- DAG validation
- Executor pool
- Result storage

Database:
- workflow_definitions
- workflow_executions  
- execution_logs
- task_queue

Optimization:
- Topological sort for dependencies
- Parallel execution where possible
- Worker pool management
"""

print(N8N_DESIGN)


# =============================================================================
# Exercise 4: Design Classic Systems with Project Integration
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 4: URL Shortener (Connect to ENTAERA Analytics)")
print("=" * 60)

URL_SHORTENER_DESIGN = """
TODO: Design bit.ly with ENTAERA-style analytics

Requirements:
- 100M URLs shortened per day
- Redirect with <100ms latency
- Analytics (click tracking, geographic data)
- Custom short URLs (premium feature)

Design:
1. Short code generation (base62)
2. Database schema (URLs + analytics)
3. Caching strategy (Redis)
4. Read-heavy optimization
5. Analytics pipeline

Connect to ENTAERA:
- Use similar caching as embedding cache
- Analytics like conversation metrics
- Database sharding strategy

Implementation:
```python
class URLShortener:
    def shorten(self, long_url: str) -> str:
        # TODO: Implement
        pass
    
    def redirect(self, short_code: str) -> str:
        # TODO: Implement with caching
        pass
    
    def track_analytics(self, short_code: str, ip: str):
        # TODO: Async analytics (like ENTAERA logging)
        pass
```
"""

print(URL_SHORTENER_DESIGN)


# =============================================================================
# Exercise 5: Design Real-Time Collaboration (Google Docs Style)
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 5: Real-Time Collaboration (Like Snap2Slides Editor)")
print("=" * 60)

COLLABORATION_DESIGN = """
TODO: Design Google Docs-style real-time collaboration

Requirements:
- Multiple users editing same document
- See each other's cursors/changes in real-time
- Conflict resolution
- Offline mode with sync

Design:
1. WebSocket architecture (like ENTAERA chat)
2. Operational Transformation (OT) or CRDT
3. Conflict resolution strategy
4. Offline sync

Architecture:
┌──────────┐     ┌──────────────┐     ┌──────────┐
│ User A   │────→│ WebSocket    │←────│ User B   │
└──────────┘     │ Server       │     └──────────┘
                 └──────────────┘
                        │
                        ▼
                 ┌──────────────┐
                 │ Change Log   │ (Database)
                 └──────────────┘

Implementation:
```python
class RealtimeEditor:
    def apply_change(self, change: dict, user_id: str):
        # TODO: Apply change and broadcast
        pass
    
    def resolve_conflict(self, change1: dict, change2: dict):
        # TODO: Operational transformation
        pass
```

Connect to Snap2Slides:
- Real-time slide editing
- Collaborative presentation building
"""

print(COLLABORATION_DESIGN)


# =============================================================================
# Exercise 6: Rate Limiter (Applied to All Your Projects)
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 6: Distributed Rate Limiter")
print("=" * 60)

RATE_LIMITER_DESIGN = """
TODO: Design distributed rate limiter

Requirements:
- Limit: 100 requests/minute per user
- Distributed (multiple servers)
- Low latency (<10ms)
- Fair distribution

Algorithms:
1. Token Bucket
2. Leaky Bucket
3. Sliding Window
4. Fixed Window

Design Choice: Token Bucket with Redis

Implementation:
```python
import time
from typing import Optional

class TokenBucket:
    def __init__(self, redis_client, capacity: int, refill_rate: float):
        # capacity: max tokens
        # refill_rate: tokens per second
        self.redis = redis_client
        self.capacity = capacity
        self.refill_rate = refill_rate
    
    def allow_request(self, user_id: str) -> bool:
        '''
        TODO: Implement token bucket in Redis
        
        Redis keys:
        - bucket:{user_id}:tokens (current tokens)
        - bucket:{user_id}:timestamp (last refill time)
        
        Algorithm:
        1. Get current tokens and last timestamp
        2. Calculate tokens to add based on time passed
        3. Refill bucket (max: capacity)
        4. If tokens >= 1, consume and allow
        5. Else deny
        
        Time: O(1), Space: O(1)
        '''
        pass

# Applications in your projects:
# - ENTAERA: Rate limit API calls
# - Snap2Slides: Limit image uploads per user
# - N8N: Limit workflow executions per tenant
```

Connect to:
- ENTAERA API resilience (Day 9)
- Snap2Slides quota management
- N8N workflow throttling
"""

print(RATE_LIMITER_DESIGN)


# =============================================================================
# Exercise 7: Design Newsfeed (Meta/Twitter Style)
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 7: Social Media Newsfeed (Connect to ENTAERA)")
print("=" * 60)

NEWSFEED_DESIGN = """
TODO: Design Twitter/Facebook newsfeed

Requirements:
- 100M users
- Follow graph (user follows other users)
- Newsfeed shows posts from followed users
- Ranked by relevance (not just time)
- Fast feed generation (<500ms)

Design Approaches:

1. Pull Model (Read-heavy):
   - Generate feed on demand
   - Query: Get posts from all followed users, sort, paginate
   - Problem: Slow for users following many people

2. Push Model (Write-heavy):
   - Pre-compute feed on post creation
   - Push post to all followers' feeds
   - Problem: Slow for users with many followers (celebrities)

3. Hybrid (Optimal):
   - Regular users: Push model
   - Celebrities: Pull model
   - Combine both in final feed

Architecture:
```
Post Creation:
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│ User A   │────→│ Post Service │────→│ Fan-out      │
│ posts    │     └──────────────┘     │ Service      │
└──────────┘                          └──────────────┘
                                             │
                    ┌────────────────────────┴────────────┐
                    ▼                                     ▼
              ┌──────────┐                          ┌──────────┐
              │ Feed     │ (Follower 1's feed)      │ Feed     │
              │ Cache    │                          │ Cache    │
              └──────────┘                          └──────────┘

Feed Retrieval:
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│ User B   │────→│ Feed Service │────→│ Feed Cache   │
│ requests │     └──────────────┘     │ (Redis)      │
│ feed     │                          └──────────────┘
└──────────┘                                 │
                                             ▼
                                      ┌──────────────┐
                                      │ Ranking      │
                                      │ Service      │
                                      └──────────────┘
```

Database Schema:
```sql
users (id, name, followers_count)
follows (follower_id, followee_id, created_at)
posts (id, user_id, content, timestamp)
feeds (user_id, post_id, score) -- Pre-computed feeds
```

Ranking Algorithm:
```python
def calculate_feed_score(post: dict, user: dict) -> float:
    '''
    TODO: Implement ranking like ENTAERA's memory relevance
    
    Factors:
    - Recency: Newer posts score higher
    - Engagement: Likes, comments, shares
    - Relevance: Content similarity to user interests
    - Author affinity: Close friends rank higher
    
    Similar to ENTAERA memory retrieval scoring!
    '''
    pass
```

Connect to ENTAERA:
- Feed cache like conversation cache
- Ranking like memory relevance scoring
- WebSocket for real-time updates
"""

print(NEWSFEED_DESIGN)


# =============================================================================
# Exercise 8: Complete System - Design Your Portfolio Project
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 8: Design Production ENTAERA (Complete)")
print("=" * 60)

COMPLETE_ENTAERA = """
TODO: Complete production-ready ENTAERA design

Combine all concepts:
1. Load Balancing (Exercise 1)
2. Caching (Multi-level)
3. Message Queue (Async tasks)
4. Database (SQL + Vector + Cache)
5. WebSocket (Real-time chat)
6. Rate Limiting (API calls)
7. Monitoring & Logging

Architecture Layers:

1. CDN Layer:
   - Static assets (CSS, JS, images)
   - CloudFront or Cloudflare

2. Load Balancer:
   - NGINX or AWS ALB
   - SSL termination
   - Health checks

3. Application Layer (Horizontally scaled):
   - FastAPI instances
   - WebSocket handlers
   - API endpoints

4. Cache Layer:
   - Redis cluster
   - L1: Embedding cache
   - L2: Conversation cache
   - L3: User session cache

5. Database Layer:
   - PostgreSQL (primary, replicas)
   - FAISS (vector search)
   - Sharding by user_id

6. Async Processing:
   - RabbitMQ or Redis Queue
   - Workers: embedding generation, memory indexing

7. Monitoring:
   - Prometheus (metrics)
   - Grafana (dashboards)
   - Sentry (error tracking)

Infrastructure:
```
Kubernetes cluster:
- Deployment: entaera-api (5 replicas)
- StatefulSet: postgresql (1 primary, 2 replicas)
- StatefulSet: redis-cluster
- Deployment: worker-pool (10 replicas)
- Service: LoadBalancer
```

Cost Estimation:
- Servers: $X/month
- Database: $Y/month
- Cache: $Z/month
- Total: $X+Y+Z/month

Disaster Recovery:
- Database backups (daily)
- Redis AOF persistence
- Multi-region deployment

Implementation Checklist:
[ ] API servers auto-scale (CPU > 70%)
[ ] Database read replicas (3)
[ ] Redis cluster (HA mode)
[ ] Message queue (RabbitMQ cluster)
[ ] Monitoring (Prometheus + Grafana)
[ ] Logging (ELK stack)
[ ] CI/CD pipeline (GitHub Actions)
[ ] Blue-green deployment
"""

print(COMPLETE_ENTAERA)

print("\n" + "=" * 60)
print("System Design Practice Complete!")
print("Review your designs with the FAANG framework:")
print("1. Requirements → 2. Capacity → 3. API → 4. Architecture")
print("5. Database → 6. Deep Dive → 7. Trade-offs")
print("=" * 60)
