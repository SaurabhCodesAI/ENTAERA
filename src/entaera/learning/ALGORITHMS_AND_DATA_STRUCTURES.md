# 🧮 PRACTICAL ALGORITHMS & DATA STRUCTURES
## Real-World Patterns from Your Projects

**Based on:**
- Your actual projects (ENTAERA, Snap2Slides, N8N)
- Common production scenarios
- Skills that make you a better engineer

---

## 🎯 **FOCUS: PRACTICAL PATTERNS**

**Not theoretical CS:**
❌ LeetCode Hard problems
❌ Academic tree/graph traversals
❌ Advanced dynamic programming

**Real engineering skills:**
✅ Parse text and extract structured data
✅ Group similar items efficiently
✅ Design routing systems
✅ Find duplicates and patterns
✅ Cache data to improve performance

---

## 📊 **6 ALGORITHM PATTERNS**

### **TIER 1: CORE PATTERNS**

---

## 🔥 **ALGORITHM 1: String Parsing & Extraction**

### **Why this matters:**
- Your Snap2Slides extracts content from documents
- Text processing is fundamental to AI systems
- Email/document parsing is common in production

### **Real-world scenario:**
*"Given an email or document, extract structured information like order numbers, names, dates"*

---

### **MASTER THIS PATTERN (2 hours):**

```python
# EXERCISE 1A: Extract structured data from text (30 min)

def parse_order_email(email_text):
    """
    Extract order info from customer email
    Like what Revalgo does!
    """
    import re
    
    result = {
        'order_number': None,
        'customer_name': None,
        'issue_type': None,
        'sentiment': None
    }
    
    # Extract order number (various patterns)
    order_patterns = [
        r'order\s*#?\s*([A-Z0-9]{6,})',
        r'order\s*number\s*:?\s*([A-Z0-9]{6,})',
        r'#([A-Z0-9]{6,})'
    ]
    
    for pattern in order_patterns:
        match = re.search(pattern, email_text, re.IGNORECASE)
        if match:
            result['order_number'] = match.group(1)
            break
    
    # Extract customer name (if starts with "Hi" or "Dear")
    name_pattern = r'(?:Hi|Dear|Hello)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)'
    name_match = re.search(name_pattern, email_text)
    if name_match:
        result['customer_name'] = name_match.group(1)
    
    # Classify issue type (keyword matching)
    issue_keywords = {
        'refund': ['refund', 'money back', 'return'],
        'delivery': ['delivery', 'shipping', 'not arrived', 'tracking'],
        'damaged': ['damaged', 'broken', 'defective'],
        'cancellation': ['cancel', 'cancellation']
    }
    
    email_lower = email_text.lower()
    for issue, keywords in issue_keywords.items():
        if any(keyword in email_lower for keyword in keywords):
            result['issue_type'] = issue
            break
    
    # Sentiment analysis (simple)
    negative_words = ['angry', 'frustrated', 'disappointed', 'terrible', 'worst']
    urgent_words = ['urgent', 'immediately', 'asap', 'emergency']
    
    if any(word in email_lower for word in urgent_words):
        result['sentiment'] = 'urgent'
    elif any(word in email_lower for word in negative_words):
        result['sentiment'] = 'negative'
    else:
        result['sentiment'] = 'neutral'
    
    return result

# TEST CASES
emails = [
    """
    Hi Support Team,
    
    I'm extremely frustrated with order #ABC12345. I ordered this item 
    2 weeks ago and it still hasn't arrived. Can I get a refund immediately?
    
    Thanks,
    John Smith
    """,
    
    """
    Dear Customer Service,
    
    My order number ABC67890 arrived damaged. The box was crushed and 
    the product is broken. Please send a replacement or process a refund.
    
    Best regards,
    Sarah Johnson
    """,
    
    """
    Hello,
    
    I need to cancel my order #XYZ99999 as soon as possible. I ordered 
    the wrong size. This is urgent!
    
    Mike
    """
]

print("=== EMAIL PARSING EXERCISE ===\n")
for i, email in enumerate(emails, 1):
    print(f"Email {i}:")
    result = parse_order_email(email)
    print(f"  Order: {result['order_number']}")
    print(f"  Customer: {result['customer_name']}")
    print(f"  Issue: {result['issue_type']}")
    print(f"  Sentiment: {result['sentiment']}")
    print()
```

---

```python
# EXERCISE 1B: Extract key-value pairs (30 min)

def extract_structured_data(text):
    """
    Extract key-value pairs from semi-structured text
    Common in email parsing
    """
    import re
    
    data = {}
    
    # Pattern: "Key: Value" or "Key = Value"
    patterns = [
        r'([A-Za-z\s]+):\s*([^\n]+)',
        r'([A-Za-z\s]+)=\s*([^\n]+)'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for key, value in matches:
            key = key.strip().lower().replace(' ', '_')
            value = value.strip()
            data[key] = value
    
    return data

# TEST
invoice_text = """
Customer Name: John Doe
Order Number: ABC123
Total Amount: $159.99
Payment Method: Credit Card
Shipping Address: 123 Main St, New York, NY 10001
Status: Shipped
"""

result = extract_structured_data(invoice_text)
print("Extracted data:", result)
```

---

```python
# EXERCISE 1C: Clean and normalize text (30 min)

def normalize_email_text(text):
    """
    Clean email text for processing
    Remove noise, standardize format
    """
    import re
    
    # Remove email signatures
    signature_markers = ['thanks', 'regards', 'best regards', 'sincerely']
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        if any(marker in line.lower() for marker in signature_markers):
            # Keep only text before signature
            text = '\n'.join(lines[:i])
            break
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove URLs
    text = re.sub(r'http[s]?://\S+', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove excessive punctuation
    text = re.sub(r'[!]{2,}', '!', text)
    text = re.sub(r'[?]{2,}', '?', text)
    
    return text.strip()

# TEST
messy_email = """
Hi there!!!!

I'm SO ANGRY about this order https://example.com/order/123

Please contact me at customer@email.com ASAP!!!

Thanks,
John
Sent from my iPhone
"""

clean = normalize_email_text(messy_email)
print("Original:", repr(messy_email))
print("\nCleaned:", repr(clean))
```

**Interview answer:**
*"For email parsing at Revalgo, I'd use regex patterns to extract structured data like order numbers and customer names. I'd classify issues using keyword matching similar to how I extracted content in Snap2Slides. For sentiment, I'd start with keyword-based detection then potentially use the LLM for complex cases. The key is having robust patterns that handle variations in how customers phrase things."*

---

## 🔍 **ALGORITHM 2: Similarity & Grouping (85% probability)**

### **Why this is critical:**
- Your ENTAERA uses **semantic search** and **vector embeddings**
- Revalgo needs to **group similar customer queries**
- Finding duplicates, clustering emails

### **What Ashish might ask:**
*"We get 1000 customer emails per day. How would you group similar ones together?"*

---

### **MASTER THIS PATTERN (2 hours):**

```python
# EXERCISE 2A: String similarity (basic) (30 min)

def calculate_similarity(text1, text2):
    """
    Calculate similarity between two texts
    Multiple methods
    """
    # Method 1: Jaccard similarity (word overlap)
    def jaccard_similarity(s1, s2):
        words1 = set(s1.lower().split())
        words2 = set(s2.lower().split())
        
        intersection = words1 & words2
        union = words1 | words2
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)
    
    # Method 2: Cosine similarity (word frequency)
    def cosine_similarity(s1, s2):
        from collections import Counter
        import math
        
        words1 = Counter(s1.lower().split())
        words2 = Counter(s2.lower().split())
        
        # Get all unique words
        all_words = set(words1.keys()) | set(words2.keys())
        
        # Create vectors
        vec1 = [words1[word] for word in all_words]
        vec2 = [words2[word] for word in all_words]
        
        # Calculate dot product
        dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
        
        # Calculate magnitudes
        mag1 = math.sqrt(sum(v ** 2 for v in vec1))
        mag2 = math.sqrt(sum(v ** 2 for v in vec2))
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        return dot_product / (mag1 * mag2)
    
    # Method 3: Levenshtein distance (character edits)
    def levenshtein_distance(s1, s2):
        if len(s1) < len(s2):
            return levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        # Convert distance to similarity (0-1)
        max_len = max(len(s1), len(s2))
        return 1 - (previous_row[-1] / max_len)
    
    return {
        'jaccard': jaccard_similarity(text1, text2),
        'cosine': cosine_similarity(text1, text2),
        'levenshtein': levenshtein_distance(text1, text2)
    }

# TEST
emails = [
    "Where is my order? I haven't received it yet",
    "My order hasn't arrived. When will it be delivered?",
    "I need a refund for my damaged product"
]

print("=== SIMILARITY COMPARISON ===\n")
print(f"Email 1 vs Email 2 (similar):")
sim1 = calculate_similarity(emails[0], emails[1])
print(f"  Jaccard: {sim1['jaccard']:.3f}")
print(f"  Cosine: {sim1['cosine']:.3f}")
print(f"  Levenshtein: {sim1['levenshtein']:.3f}")

print(f"\nEmail 1 vs Email 3 (different):")
sim2 = calculate_similarity(emails[0], emails[2])
print(f"  Jaccard: {sim2['jaccard']:.3f}")
print(f"  Cosine: {sim2['cosine']:.3f}")
print(f"  Levenshtein: {sim2['levenshtein']:.3f}")
```

---

```python
# EXERCISE 2B: Clustering similar items (45 min)

def cluster_similar_emails(emails, similarity_threshold=0.6):
    """
    Group similar emails together
    Like finding duplicate customer requests at Revalgo
    """
    clusters = []
    assigned = set()
    
    for i, email1 in enumerate(emails):
        if i in assigned:
            continue
        
        # Start new cluster
        cluster = [i]
        assigned.add(i)
        
        # Find similar emails
        for j, email2 in enumerate(emails):
            if j <= i or j in assigned:
                continue
            
            # Calculate similarity
            words1 = set(email1.lower().split())
            words2 = set(email2.lower().split())
            
            intersection = words1 & words2
            union = words1 | words2
            
            if union:
                similarity = len(intersection) / len(union)
                
                if similarity >= similarity_threshold:
                    cluster.append(j)
                    assigned.add(j)
        
        clusters.append(cluster)
    
    return clusters

# TEST
customer_emails = [
    "Where is my order ABC123?",
    "My order ABC123 hasn't arrived yet",
    "I want a refund for broken product",
    "The item I received is damaged, need refund",
    "Track my shipment ABC123",
    "When will order ABC123 be delivered?",
    "Return broken item and get money back"
]

print("\n=== CLUSTERING EXERCISE ===\n")
clusters = cluster_similar_emails(customer_emails, similarity_threshold=0.4)

for i, cluster in enumerate(clusters, 1):
    print(f"Cluster {i}:")
    for idx in cluster:
        print(f"  - {customer_emails[idx]}")
    print()
```

---

```python
# EXERCISE 2C: Find duplicates efficiently (45 min)

def find_duplicate_requests(emails, time_window_hours=24):
    """
    Find duplicate customer requests within time window
    Important for Revalgo to avoid duplicate responses
    """
    from datetime import datetime, timedelta
    from collections import defaultdict
    
    # Group by normalized content
    content_groups = defaultdict(list)
    
    for email in emails:
        # Normalize: lowercase, remove punctuation, sort words
        words = sorted(set(email['content'].lower().split()))
        normalized = ' '.join(words)
        
        content_groups[normalized].append(email)
    
    # Find duplicates within time window
    duplicates = []
    
    for normalized, group in content_groups.items():
        if len(group) < 2:
            continue
        
        # Sort by timestamp
        group.sort(key=lambda x: x['timestamp'])
        
        # Check if within time window
        first_time = group[0]['timestamp']
        last_time = group[-1]['timestamp']
        
        if last_time - first_time <= timedelta(hours=time_window_hours):
            duplicates.append({
                'emails': group,
                'count': len(group),
                'time_span': str(last_time - first_time)
            })
    
    return duplicates

# TEST
now = datetime.now()
test_emails = [
    {'id': 1, 'content': 'Where is my order?', 'timestamp': now},
    {'id': 2, 'content': 'My order where is?', 'timestamp': now + timedelta(hours=2)},
    {'id': 3, 'content': 'Need refund please', 'timestamp': now + timedelta(hours=1)},
    {'id': 4, 'content': 'Where is my order?', 'timestamp': now + timedelta(hours=30)},  # Outside window
]

print("=== DUPLICATE DETECTION ===\n")
dupes = find_duplicate_requests(test_emails, time_window_hours=24)

for i, dupe in enumerate(dupes, 1):
    print(f"Duplicate group {i}: {dupe['count']} emails in {dupe['time_span']}")
    for email in dupe['emails']:
        print(f"  - ID {email['id']}: {email['content']}")
    print()
```

**Interview answer:**
*"For grouping similar emails at Revalgo, I'd use the same approach as my ENTAERA semantic search - generate embeddings for each email and calculate cosine similarity. For a simpler version, Jaccard similarity on keywords works well. I'd cluster emails above a similarity threshold (like 0.6) to group duplicate requests. This prevents sending multiple responses to the same customer query and helps identify common issues."*

---

## 🗂️ **ALGORITHM 3: Caching & Memoization (75% probability)**

### **Why this is critical:**
- Your Snap2Slides uses **connection pooling** (`Map<string, GoogleGenerativeAI>`)
- API cost optimization (don't call API for same query twice)
- Performance optimization

### **What Ashish might ask:**
*"Our API costs are high. How would you cache responses to avoid repeated calls?"*

---

### **MASTER THIS PATTERN (1.5 hours):**

```python
# EXERCISE 3A: Simple caching (30 min)

class ResponseCache:
    """
    Cache API responses to avoid repeated calls
    Like YOUR Snap2Slides client pooling
    """
    def __init__(self, max_size=100, ttl_seconds=3600):
        self.cache = {}
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.access_count = {}
        self.timestamps = {}
    
    def _is_expired(self, key):
        """Check if cache entry is expired"""
        import time
        if key not in self.timestamps:
            return True
        
        age = time.time() - self.timestamps[key]
        return age > self.ttl_seconds
    
    def get(self, key):
        """Get cached value"""
        if key not in self.cache or self._is_expired(key):
            return None
        
        self.access_count[key] = self.access_count.get(key, 0) + 1
        return self.cache[key]
    
    def set(self, key, value):
        """Set cache value"""
        import time
        
        # Evict if cache is full
        if len(self.cache) >= self.max_size and key not in self.cache:
            # Remove least recently used
            lru_key = min(self.access_count, key=self.access_count.get)
            del self.cache[lru_key]
            del self.access_count[lru_key]
            del self.timestamps[lru_key]
        
        self.cache[key] = value
        self.access_count[key] = 0
        self.timestamps[key] = time.time()
    
    def stats(self):
        """Get cache statistics"""
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hit_rate': sum(self.access_count.values()) / max(len(self.cache), 1)
        }

# TEST
import time

cache = ResponseCache(max_size=3, ttl_seconds=5)

print("=== CACHING EXERCISE ===\n")

# Simulate API calls
def expensive_api_call(query):
    """Simulate slow API call"""
    print(f"  [API CALL] Processing '{query}'...")
    time.sleep(0.5)
    return f"Response for '{query}'"

queries = ['order status', 'refund policy', 'order status', 'shipping info', 'order status']

for query in queries:
    print(f"\nQuery: '{query}'")
    
    # Check cache first
    cached = cache.get(query)
    
    if cached:
        print(f"  [CACHE HIT] {cached}")
    else:
        print(f"  [CACHE MISS]")
        result = expensive_api_call(query)
        cache.set(query, result)
        print(f"  Cached result")

print(f"\nCache stats: {cache.stats()}")
```

---

```python
# EXERCISE 3B: Semantic cache (for similar queries) (45 min)

class SemanticCache:
    """
    Cache that matches SIMILAR queries, not just exact
    Uses YOUR vector embedding concept!
    """
    def __init__(self, similarity_threshold=0.8):
        self.cache = {}  # {query: response}
        self.threshold = similarity_threshold
    
    def _calculate_similarity(self, query1, query2):
        """Simple word overlap similarity"""
        words1 = set(query1.lower().split())
        words2 = set(query2.lower().split())
        
        intersection = words1 & words2
        union = words1 | words2
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)
    
    def get(self, query):
        """Get cached response for query or similar query"""
        # Check exact match first
        if query in self.cache:
            print(f"    [EXACT MATCH]")
            return self.cache[query]
        
        # Check for similar queries
        for cached_query, response in self.cache.items():
            similarity = self._calculate_similarity(query, cached_query)
            
            if similarity >= self.threshold:
                print(f"    [SIMILAR MATCH] {similarity:.2f} with '{cached_query}'")
                return response
        
        return None
    
    def set(self, query, response):
        """Cache response for query"""
        self.cache[query] = response

# TEST
semantic_cache = SemanticCache(similarity_threshold=0.7)

print("\n=== SEMANTIC CACHING EXERCISE ===\n")

# Simulate queries
test_cases = [
    ("Where is my order?", "Your order is being processed"),
    ("Where is my package?", None),  # Should hit cache (similar)
    ("I need a refund", "Refund processed in 5-7 days"),
    ("Can I get money back?", None),  # Should hit cache (similar)
    ("What are your hours?", None),  # Should miss (different)
]

for query, expected_cache in test_cases:
    print(f"Query: '{query}'")
    
    cached = semantic_cache.get(query)
    
    if cached:
        print(f"  ✅ {cached}")
    else:
        print(f"  ❌ MISS - calling API")
        # Simulate API response
        response = f"[API response for '{query}']"
        semantic_cache.set(query, response)
        print(f"  Cached: {response}")
    
    print()
```

---

```python
# EXERCISE 3C: Cache invalidation strategy (15 min)

class SmartCache:
    """
    Cache with intelligent invalidation
    Important for time-sensitive data
    """
    def __init__(self):
        self.cache = {}
        self.versions = {}  # Track data versions
    
    def get(self, key, version=None):
        """Get with version checking"""
        if key not in self.cache:
            return None
        
        # Check if version matches
        if version and self.versions.get(key) != version:
            print(f"  [STALE] Version mismatch")
            del self.cache[key]
            return None
        
        return self.cache[key]
    
    def set(self, key, value, version=1):
        """Set with version"""
        self.cache[key] = value
        self.versions[key] = version
    
    def invalidate(self, key):
        """Manually invalidate"""
        if key in self.cache:
            del self.cache[key]
            del self.versions[key]
            print(f"  [INVALIDATED] {key}")
    
    def invalidate_pattern(self, pattern):
        """Invalidate all keys matching pattern"""
        import re
        to_delete = [k for k in self.cache.keys() if re.search(pattern, k)]
        
        for key in to_delete:
            self.invalidate(key)

# TEST
smart_cache = SmartCache()

print("=== CACHE INVALIDATION ===\n")

# Cache order status
smart_cache.set('order_ABC123', 'Shipped', version=1)
print("Cached: order_ABC123 = Shipped (v1)")

# Try to get with correct version
result = smart_cache.get('order_ABC123', version=1)
print(f"Get v1: {result}")

# Order gets delivered (version changes)
smart_cache.set('order_ABC123', 'Delivered', version=2)
print("\nOrder updated to Delivered (v2)")

# Old version is stale
result = smart_cache.get('order_ABC123', version=1)
print(f"Get v1: {result}")  # None - stale

# New version works
result = smart_cache.get('order_ABC123', version=2)
print(f"Get v2: {result}")  # Delivered
```

**Interview answer:**
*"For caching at Revalgo, I'd implement a two-level strategy. First, exact match caching for identical queries with TTL of 1 hour. Second, semantic caching for similar queries - if a new query is 80% similar to a cached one, return the cached response. This is like how I used connection pooling in Snap2Slides to reuse API clients. I'd also implement cache invalidation when order status changes to avoid stale data."*

---

## 🔄 **ALGORITHM 4: Queue & Priority Processing (70% probability)**

### **Why this is critical:**
- Your ENTAERA has **task prioritization** (priority: 1-10)
- Revalgo needs to **prioritize urgent customer emails**
- Handle high-volume email processing

### **What Ashish might ask:**
*"How would you handle processing 10,000 emails, prioritizing urgent ones?"*

---

### **MASTER THIS PATTERN (1.5 hours):**

```python
# EXERCISE 4A: Priority queue basics (30 min)

import heapq
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Email:
    """Email with priority"""
    id: int
    content: str
    priority: int  # 1 = highest, 10 = lowest
    timestamp: datetime
    
    def __lt__(self, other):
        """For heap comparison"""
        # Lower priority number = higher priority
        if self.priority != other.priority:
            return self.priority < other.priority
        # If same priority, older email first
        return self.timestamp < other.timestamp

class EmailQueue:
    """
    Priority queue for email processing
    Like YOUR task prioritization in ENTAERA
    """
    def __init__(self):
        self.queue = []
    
    def add(self, email):
        """Add email to queue"""
        heapq.heappush(self.queue, email)
        print(f"  Added: {email.content[:30]}... (priority {email.priority})")
    
    def get_next(self):
        """Get highest priority email"""
        if not self.queue:
            return None
        return heapq.heappop(self.queue)
    
    def peek(self):
        """See next email without removing"""
        if not self.queue:
            return None
        return self.queue[0]
    
    def size(self):
        """Get queue size"""
        return len(self.queue)

# TEST
print("=== PRIORITY QUEUE EXERCISE ===\n")

queue = EmailQueue()

# Add emails with different priorities
emails = [
    Email(1, "My order is wrong!", priority=2, timestamp=datetime.now()),
    Email(2, "When will my order arrive?", priority=5, timestamp=datetime.now()),
    Email(3, "URGENT: Need immediate refund!", priority=1, timestamp=datetime.now()),
    Email(4, "Question about return policy", priority=8, timestamp=datetime.now()),
    Email(5, "Damaged product - need replacement ASAP", priority=2, timestamp=datetime.now()),
]

print("Adding emails:")
for email in emails:
    queue.add(email)

print(f"\nQueue size: {queue.size()}")

print("\nProcessing in priority order:")
while queue.size() > 0:
    email = queue.get_next()
    print(f"  Processing: {email.content} (priority {email.priority})")
```

---

```python
# EXERCISE 4B: Auto-prioritize based on content (45 min)

def calculate_priority(email_text):
    """
    Automatically assign priority based on content
    Like email triage at Revalgo
    """
    email_lower = email_text.lower()
    
    priority = 5  # Default: normal priority
    
    # Urgent keywords = higher priority
    urgent_keywords = ['urgent', 'asap', 'immediately', 'emergency', 'critical']
    if any(keyword in email_lower for keyword in urgent_keywords):
        priority = min(priority, 1)  # Highest
    
    # Negative sentiment = higher priority
    angry_keywords = ['angry', 'frustrated', 'terrible', 'worst', 'furious']
    if any(keyword in email_lower for keyword in angry_keywords):
        priority = min(priority, 2)
    
    # Refund/money = medium-high priority
    money_keywords = ['refund', 'money back', 'charge', 'payment']
    if any(keyword in email_lower for keyword in money_keywords):
        priority = min(priority, 3)
    
    # Delivery issues = medium priority
    delivery_keywords = ['delivery', 'shipping', 'not arrived', 'late']
    if any(keyword in email_lower for keyword in delivery_keywords):
        priority = min(priority, 4)
    
    # General questions = low priority
    question_keywords = ['how do i', 'what is', 'can you explain']
    if any(keyword in email_lower for keyword in question_keywords):
        priority = max(priority, 7)
    
    return priority

# TEST
test_emails = [
    "URGENT: I need a refund immediately for order ABC123!",
    "When will my order arrive?",
    "I'm extremely angry about the terrible service",
    "What is your return policy?",
    "My package is late",
]

print("\n=== AUTO-PRIORITIZATION ===\n")
for email in test_emails:
    priority = calculate_priority(email)
    print(f"Priority {priority}: {email}")
```

---

```python
# EXERCISE 4C: Rate limiting with queue (15 min)

import time
from collections import deque

class RateLimitedQueue:
    """
    Process queue with rate limiting
    Max N items per time window
    """
    def __init__(self, max_per_minute=10):
        self.queue = deque()
        self.max_per_minute = max_per_minute
        self.processed_times = deque()
    
    def add(self, item):
        """Add item to queue"""
        self.queue.append(item)
    
    def can_process_now(self):
        """Check if we can process another item"""
        now = time.time()
        
        # Remove timestamps older than 1 minute
        while self.processed_times and now - self.processed_times[0] > 60:
            self.processed_times.popleft()
        
        # Check if under limit
        return len(self.processed_times) < self.max_per_minute
    
    def process_next(self):
        """Process next item if rate limit allows"""
        if not self.queue:
            return None
        
        if not self.can_process_now():
            return "RATE_LIMITED"
        
        item = self.queue.popleft()
        self.processed_times.append(time.time())
        
        return item

# TEST
print("\n=== RATE-LIMITED QUEUE ===\n")

queue = RateLimitedQueue(max_per_minute=5)

# Add 10 emails
for i in range(10):
    queue.add(f"Email {i+1}")

# Try to process all
processed = 0
rate_limited = 0

for _ in range(15):  # Try more than we have
    result = queue.process_next()
    
    if result is None:
        break
    elif result == "RATE_LIMITED":
        rate_limited += 1
        print(f"  Rate limited (processed {processed}/5 in this minute)")
    else:
        processed += 1
        print(f"  Processed: {result}")

print(f"\nTotal processed: {processed}")
print(f"Rate limited: {rate_limited}")
```

**Interview answer:**
*"For Revalgo's email processing, I'd use a priority queue like in my ENTAERA task system. Emails would be auto-prioritized based on keywords - 'urgent' and 'refund' get priority 1-2, delivery questions get 4-5, general questions get 7-8. I'd process the queue in priority order. For rate limiting, I'd track timestamps of processed emails and ensure we don't exceed API limits per minute. This ensures urgent customer issues get handled first while staying within system limits."*

---

## 📊 **ALGORITHM 5: Data Aggregation & Stats (65% probability)**

### **Why this is critical:**
- Your ENTAERA tracks **agent metrics** (success rate, avg completion time)
- Revalgo needs **reporting** (emails per day, response times, etc.)
- Analytics and monitoring

### **What Ashish might ask:**
*"Given email data, calculate daily statistics like average response time"*

---

### **MASTER THIS PATTERN (1 hour):**

```python
# EXERCISE 5A: Basic aggregation (20 min)

from collections import defaultdict
from datetime import datetime, timedelta

def calculate_email_stats(emails):
    """
    Calculate statistics from email data
    Like YOUR AgentPerformanceMetrics
    """
    stats = {
        'total_emails': len(emails),
        'by_category': defaultdict(int),
        'by_priority': defaultdict(int),
        'by_hour': defaultdict(int),
        'avg_response_time': 0,
        'response_times': []
    }
    
    total_response_time = 0
    emails_with_response = 0
    
    for email in emails:
        # Count by category
        stats['by_category'][email.get('category', 'unknown')] += 1
        
        # Count by priority
        stats['by_priority'][email.get('priority', 5)] += 1
        
        # Count by hour
        hour = email['timestamp'].hour
        stats['by_hour'][hour] += 1
        
        # Calculate response time
        if 'response_time' in email:
            response_time = email['response_time']
            total_response_time += response_time
            emails_with_response += 1
            stats['response_times'].append(response_time)
    
    # Calculate averages
    if emails_with_response > 0:
        stats['avg_response_time'] = total_response_time / emails_with_response
    
    # Calculate percentiles
    if stats['response_times']:
        sorted_times = sorted(stats['response_times'])
        stats['median_response_time'] = sorted_times[len(sorted_times) // 2]
        stats['p95_response_time'] = sorted_times[int(len(sorted_times) * 0.95)]
    
    return stats

# TEST
now = datetime.now()
test_emails = [
    {'category': 'refund', 'priority': 1, 'timestamp': now, 'response_time': 120},
    {'category': 'refund', 'priority': 2, 'timestamp': now, 'response_time': 300},
    {'category': 'delivery', 'priority': 4, 'timestamp': now + timedelta(hours=1), 'response_time': 450},
    {'category': 'delivery', 'priority': 3, 'timestamp': now + timedelta(hours=2), 'response_time': 200},
    {'category': 'general', 'priority': 7, 'timestamp': now + timedelta(hours=3), 'response_time': 600},
]

print("=== EMAIL STATISTICS ===\n")
stats = calculate_email_stats(test_emails)

print(f"Total emails: {stats['total_emails']}")
print(f"\nBy category:")
for cat, count in stats['by_category'].items():
    print(f"  {cat}: {count}")

print(f"\nBy priority:")
for pri, count in sorted(stats['by_priority'].items()):
    print(f"  Priority {pri}: {count}")

print(f"\nResponse time:")
print(f"  Average: {stats['avg_response_time']:.1f}s")
print(f"  Median: {stats.get('median_response_time', 0):.1f}s")
print(f"  95th percentile: {stats.get('p95_response_time', 0):.1f}s")
```

---

```python
# EXERCISE 5B: Time-based aggregation (window) (25 min)

def aggregate_by_time_window(emails, window_minutes=60):
    """
    Group emails into time windows
    For hourly/daily reporting
    """
    windows = defaultdict(list)
    
    for email in emails:
        # Round timestamp to window
        timestamp = email['timestamp']
        window_start = timestamp.replace(
            minute=(timestamp.minute // window_minutes) * window_minutes,
            second=0,
            microsecond=0
        )
        
        windows[window_start].append(email)
    
    # Calculate stats for each window
    window_stats = {}
    for window_start, window_emails in windows.items():
        window_stats[window_start] = {
            'count': len(window_emails),
            'categories': defaultdict(int),
            'avg_priority': sum(e.get('priority', 5) for e in window_emails) / len(window_emails)
        }
        
        for email in window_emails:
            cat = email.get('category', 'unknown')
            window_stats[window_start]['categories'][cat] += 1
    
    return window_stats

# TEST
print("\n=== TIME WINDOW AGGREGATION ===\n")

base_time = datetime.now().replace(minute=0, second=0, microsecond=0)
test_emails = []

# Generate emails across 3 hours
for hour in range(3):
    for i in range(10):
        test_emails.append({
            'timestamp': base_time + timedelta(hours=hour, minutes=i*5),
            'category': ['refund', 'delivery', 'general'][i % 3],
            'priority': (i % 5) + 1
        })

window_stats = aggregate_by_time_window(test_emails, window_minutes=60)

for window, stats in sorted(window_stats.items()):
    print(f"{window.strftime('%H:%M')}:")
    print(f"  Emails: {stats['count']}")
    print(f"  Avg priority: {stats['avg_priority']:.1f}")
    print(f"  Categories: {dict(stats['categories'])}")
    print()
```

---

```python
# EXERCISE 5C: Rolling statistics (15 min)

class RollingStats:
    """
    Calculate rolling statistics
    Like moving average for response times
    """
    def __init__(self, window_size=10):
        self.window_size = window_size
        self.values = []
    
    def add(self, value):
        """Add new value"""
        self.values.append(value)
        
        # Keep only last N values
        if len(self.values) > self.window_size:
            self.values.pop(0)
    
    def get_average(self):
        """Get rolling average"""
        if not self.values:
            return 0
        return sum(self.values) / len(self.values)
    
    def get_trend(self):
        """Determine if trending up or down"""
        if len(self.values) < 2:
            return "stable"
        
        recent_avg = sum(self.values[-5:]) / min(5, len(self.values))
        older_avg = sum(self.values[:-5]) / max(1, len(self.values) - 5)
        
        if recent_avg > older_avg * 1.1:
            return "increasing"
        elif recent_avg < older_avg * 0.9:
            return "decreasing"
        return "stable"

# TEST
print("=== ROLLING STATISTICS ===\n")

rolling = RollingStats(window_size=5)

response_times = [100, 120, 110, 150, 200, 180, 190, 220, 210, 250]

for i, time in enumerate(response_times, 1):
    rolling.add(time)
    avg = rolling.get_average()
    trend = rolling.get_trend()
    
    print(f"Email {i}: {time}s | Rolling avg: {avg:.1f}s | Trend: {trend}")
```

**Interview answer:**
*"For Revalgo's analytics, I'd track metrics similar to my ENTAERA agent performance tracking - total emails processed, average response time, breakdown by category. I'd use time-window aggregation for hourly/daily reports. For monitoring, I'd calculate rolling averages of response times to detect if things are slowing down. I'd also track 95th percentile response time since averages can hide outliers where customers waited too long."*

---

## 🎯 **ALGORITHM 6: Graph/Tree (Lower Priority - 40% probability)**

### **Quick coverage - only if time permits:**

```python
# EXERCISE 6: Email thread structure (conversation tree)

class EmailThread:
    """
    Represent email conversation as tree
    Parent → Child replies
    """
    def __init__(self, email_id, content):
        self.email_id = email_id
        self.content = content
        self.replies = []
        self.parent = None
    
    def add_reply(self, reply):
        """Add reply to this email"""
        reply.parent = self
        self.replies.append(reply)
    
    def get_thread_depth(self):
        """How many levels deep is this thread?"""
        if not self.replies:
            return 1
        return 1 + max(reply.get_thread_depth() for reply in self.replies)
    
    def get_all_emails(self):
        """Get all emails in thread (flatten)"""
        emails = [self]
        for reply in self.replies:
            emails.extend(reply.get_all_emails())
        return emails

# TEST - Quick example
root = EmailThread(1, "Where is my order?")
reply1 = EmailThread(2, "We're checking on that")
reply2 = EmailThread(3, "Your order shipped today")
reply3 = EmailThread(4, "Thank you!")

root.add_reply(reply1)
reply1.add_reply(reply2)
reply2.add_reply(reply3)

print(f"Thread depth: {root.get_thread_depth()}")
print(f"Total emails: {len(root.get_all_emails())}")
```

---

## 📋 **INTERVIEW PREP SUMMARY**

### **Time allocation for coding prep (10.5 hours total):**

| Algorithm | Time | Probability | Must Practice | In Your Code? |
|-----------|------|-------------|---------------|---------------|
| 0. 🔥 **Async/Await patterns** | 2h | 95% | ✅ **CRITICAL** | ✅ 50+ functions! |
| 1. String parsing & extraction | 2h | 90% | ✅ YES | ❌ For Revalgo |
| 2. Similarity & grouping | 2h | 85% | ✅ YES | ✅ semantic_search.py |
| 3. Caching & memoization | 1.5h | 75% | ✅ YES | ✅ EmbeddingCache |
| 4. Queue & priority | 1.5h | 70% | ✅ YES | ⚠️ Has priority field |
| 5. Data aggregation | 1h | 65% | ✅ YES | ⚠️ Partial |
| 6. Graph/tree | 30min | 40% | ⚠️ If time | ❌ No |

---

## 🔥 **ALGORITHM 0: Async/Await Patterns (95% probability) - NEW!**

### **Why this is CRITICAL:**
- **YOUR ENTAERA HAS 50+ ASYNC FUNCTIONS!**
- `agent_orchestration.py`, `rate_limiter.py`, `api_router.py` are ALL async
- This is NOT optional - it's your ACTUAL production code
- Ashish WILL ask "Walk me through your async code"

### **What Ashish might ask:**
*"I see your code uses async/await everywhere. Explain how that works and why you chose it."*

---

### **MASTER THIS PATTERN (2 hours):**

See **CRITICAL_MISSING_EXERCISES.md Exercise 18** for full async/await coverage.

**Quick reference of YOUR async patterns:**

```python
# PATTERN 1: Basic async function (you have 50+ of these)
async def execute_task(self, task: WorkflowTask) -> Any:
    await self.start_task(task)
    result = await self._handle_conversation_task(task)
    await self.complete_task(task, result)
    return result

# PATTERN 2: asyncio.gather for parallel execution
results = await asyncio.gather(
    generate_embedding("doc1"),
    generate_embedding("doc2"),
    search_semantic("query")
)

# PATTERN 3: Semaphore for rate limiting
self.semaphores = {
    "gemini": asyncio.Semaphore(3),      # Max 3 concurrent
    "perplexity": asyncio.Semaphore(2),  # Max 2 concurrent
}

async def acquire(self, api: str) -> bool:
    await self.semaphores[api].acquire()
    # Make API call
    self.semaphores[api].release()

# PATTERN 4: Async context manager
async with AsyncAPIConnection("gemini") as conn:
    result = await conn.make_request(prompt)
    # Automatic cleanup on exit
```

**Interview answer:**
*"My ENTAERA is heavily async - 50+ async functions across multiple modules. I use async because we make many API calls that take 1-5 seconds each. With async/await, we can run multiple API calls in parallel using asyncio.gather() instead of waiting sequentially. For rate limiting, I use asyncio.Semaphore to control concurrency - max 3 concurrent Gemini calls, 2 for Perplexity. The performance difference is huge - 10 API calls take 5 seconds async vs 50 seconds synchronous. I also use async context managers with 'async with' for automatic resource cleanup."*

---

## 🎯 **PRACTICE STRATEGY:**

### **Day 1 (Oct 28) - Add 3 hours:**
- 🔥 **Exercise 0: Async/Await basics (1 hour)** - YOUR PRODUCTION CODE!
- Exercise 1A-C: String parsing (1 hour)
- Exercise 2A: Similarity basics (30 min)
- Exercise 3A: Simple caching (30 min)

### **Day 2 (Oct 29) - Add 3 hours:**
- 🔥 **Exercise 0: Async patterns (semaphores, gather, context managers) (1 hour)**
- Exercise 2B-C: Clustering & duplicates (1.5 hours)
- Exercise 4A: Priority queue (30 min)

### **Day 3 (Oct 30) - Add 1.5 hours:**
- Exercise 3B-C: Semantic caching (1 hour)
- Exercise 4B-C: Auto-priority & rate limiting (30 min)

### **Day 4 (Oct 31) - Add 1 hour:**
- Exercise 5A-C: Aggregation & stats (1 hour)

### **Day 5-6: Practice explaining these algorithms in interviews**

---

## 🔥 **INTERVIEW ANSWERS READY:**

**Ashish:** *"I see your code is heavily async. Why and how does that work?"*
**You:** *"My ENTAERA has 50+ async functions because we make many API calls that take 1-5 seconds. Async lets multiple calls run in parallel - using asyncio.gather() to coordinate them. For example, 10 sequential API calls would take 50 seconds, but with async they take 5 seconds. I use asyncio.Semaphore for rate limiting - max 3 concurrent Gemini calls. The pattern is 'await self.semaphores[api].acquire()' to get permission, then release when done. All defined with 'async def' and called with 'await'."*

**Ashish:** *"Parse this email and extract order info"*
**You:** *"I'd use regex patterns for structured data like order numbers, keyword matching for issue classification, and sentiment analysis for urgency. This is similar to how Snap2Slides extracts document content."*

**Ashish:** *"Group similar customer emails"*
**You:** *"I'd use the same semantic search approach as ENTAERA - calculate similarity with Jaccard or cosine similarity, cluster above a threshold like 0.6. This groups duplicate requests."*

**Ashish:** *"Our API costs are high"*
**You:** *"I'd implement two-level caching - exact match with 1-hour TTL, plus semantic matching for similar queries. Like how Snap2Slides uses connection pooling to reuse clients."*

**Ashish:** *"How to prioritize 10,000 emails?"*
**You:** *"Priority queue based on keywords - 'urgent' and 'refund' get priority 1, general questions get 7. Process in order. Like my ENTAERA task prioritization system."*

**Ready to start? Begin with Algorithm 1 (String Parsing) - most likely to be asked!** 🚀
