# 🛠️ PRODUCTION SKILLS EXERCISES
## SQL, Testing, Docker, Git, Logging & Monitoring

**These skills separate hobby projects from production systems**

---

## 💾 **EXERCISE 1: SQL Basics (2 hours)**

### **Why This Matters:**
- Databases store all real application data
- SQL is universal across PostgreSQL, MySQL, SQLite
- Every backend engineer needs SQL

### **What You'll Learn:**
- CREATE tables
- INSERT, SELECT, UPDATE, DELETE
- WHERE filtering
- JOIN multiple tables
- Basic aggregations (COUNT, SUM, AVG)

---

### **Part 1: Setup (10 minutes)**

```python
# Create: learn_sql.py
import sqlite3

# Create database
conn = sqlite3.connect('entaera_learning.db')
cursor = conn.cursor()

print("✅ Database created: entaera_learning.db")
```

---

### **Part 2: CREATE Tables (15 minutes)**

```python
# Create conversations table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT NOT NULL,
        response TEXT NOT NULL,
        agent TEXT,
        provider TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        tokens_used INTEGER,
        success BOOLEAN DEFAULT 1
    )
''')

# Create users table (for JOINs later)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# Add user_id to conversations
cursor.execute('''
    ALTER TABLE conversations 
    ADD COLUMN user_id INTEGER REFERENCES users(id)
''')

conn.commit()
print("✅ Tables created")
```

---

### **Part 3: INSERT Data (15 minutes)**

```python
# Insert users
cursor.execute('''
    INSERT INTO users (username, email) 
    VALUES (?, ?)
''', ("saurabh", "saurabh@example.com"))

cursor.execute('''
    INSERT INTO users (username, email) 
    VALUES (?, ?)
''', ("testuser", "test@example.com"))

user_id = cursor.lastrowid
print(f"✅ Inserted user with ID: {user_id}")

# Insert conversations
conversations_data = [
    ("What is Python?", "Python is a programming language...", "Assistant", "ollama", 150, 1, 1),
    ("How do I write a function?", "def function_name():", "Code Assistant", "gemini", 200, 1, 1),
    ("Search AI news", "Here are the latest AI developments...", "Research", "perplexity", 300, 1, 1),
    ("Write a poem", "Roses are red...", "Creative", "gemini", 250, 1, 2),
    ("Invalid query", "Error processing", "Assistant", "ollama", 50, 0, 1),
]

cursor.executemany('''
    INSERT INTO conversations (query, response, agent, provider, tokens_used, success, user_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', conversations_data)

conn.commit()
print(f"✅ Inserted {len(conversations_data)} conversations")
```

---

### **Part 4: SELECT Queries (30 minutes)**

```python
# BASIC SELECT
print("\n=== ALL CONVERSATIONS ===")
cursor.execute('SELECT * FROM conversations')
rows = cursor.fetchall()
for row in rows:
    print(row)

# SELECT specific columns
print("\n=== QUERIES AND AGENTS ===")
cursor.execute('SELECT query, agent FROM conversations')
for query, agent in cursor.fetchall():
    print(f"{agent}: {query[:40]}...")

# WHERE filtering
print("\n=== SUCCESSFUL CONVERSATIONS ===")
cursor.execute('''
    SELECT query, response, tokens_used 
    FROM conversations 
    WHERE success = 1
''')
for row in cursor.fetchall():
    print(row)

# Multiple conditions
print("\n=== GEMINI SUCCESSFUL QUERIES ===")
cursor.execute('''
    SELECT query, tokens_used 
    FROM conversations 
    WHERE provider = 'gemini' AND success = 1
''')
for row in cursor.fetchall():
    print(row)

# ORDER BY
print("\n=== TOP 3 BY TOKENS ===")
cursor.execute('''
    SELECT query, tokens_used 
    FROM conversations 
    ORDER BY tokens_used DESC 
    LIMIT 3
''')
for row in cursor.fetchall():
    print(row)

# LIKE pattern matching
print("\n=== QUERIES ABOUT WRITING ===")
cursor.execute('''
    SELECT query, agent 
    FROM conversations 
    WHERE query LIKE '%write%' OR query LIKE '%Write%'
''')
for row in cursor.fetchall():
    print(row)
```

---

### **Part 5: Aggregations (20 minutes)**

```python
# COUNT
print("\n=== TOTAL CONVERSATIONS ===")
cursor.execute('SELECT COUNT(*) FROM conversations')
total = cursor.fetchone()[0]
print(f"Total: {total}")

# COUNT with GROUP BY
print("\n=== CONVERSATIONS BY AGENT ===")
cursor.execute('''
    SELECT agent, COUNT(*) as count 
    FROM conversations 
    GROUP BY agent 
    ORDER BY count DESC
''')
for agent, count in cursor.fetchall():
    print(f"{agent}: {count}")

# SUM and AVG
print("\n=== TOKEN STATISTICS ===")
cursor.execute('''
    SELECT 
        provider,
        COUNT(*) as total_queries,
        SUM(tokens_used) as total_tokens,
        AVG(tokens_used) as avg_tokens,
        MIN(tokens_used) as min_tokens,
        MAX(tokens_used) as max_tokens
    FROM conversations
    GROUP BY provider
''')
for row in cursor.fetchall():
    print(row)

# HAVING (filter after aggregation)
print("\n=== PROVIDERS WITH > 1 QUERY ===")
cursor.execute('''
    SELECT provider, COUNT(*) as count 
    FROM conversations 
    GROUP BY provider 
    HAVING count > 1
''')
for row in cursor.fetchall():
    print(row)
```

---

### **Part 6: JOINs (30 minutes)**

```python
# INNER JOIN
print("\n=== CONVERSATIONS WITH USERNAMES ===")
cursor.execute('''
    SELECT 
        u.username,
        c.query,
        c.agent,
        c.timestamp
    FROM conversations c
    INNER JOIN users u ON c.user_id = u.id
    ORDER BY c.timestamp DESC
''')
for row in cursor.fetchall():
    print(row)

# LEFT JOIN (show all conversations, even without user)
print("\n=== ALL CONVERSATIONS WITH OPTIONAL USER ===")
cursor.execute('''
    SELECT 
        COALESCE(u.username, 'Anonymous') as user,
        c.query,
        c.success
    FROM conversations c
    LEFT JOIN users u ON c.user_id = u.id
''')
for row in cursor.fetchall():
    print(row)

# Count queries per user
print("\n=== QUERIES PER USER ===")
cursor.execute('''
    SELECT 
        u.username,
        COUNT(c.id) as query_count,
        SUM(c.tokens_used) as total_tokens
    FROM users u
    LEFT JOIN conversations c ON u.id = c.user_id
    GROUP BY u.id, u.username
    ORDER BY query_count DESC
''')
for row in cursor.fetchall():
    print(row)
```

---

### **Part 7: UPDATE and DELETE (15 minutes)**

```python
# UPDATE
print("\n=== UPDATING DATA ===")
cursor.execute('''
    UPDATE conversations 
    SET tokens_used = tokens_used + 10 
    WHERE provider = 'gemini'
''')
print(f"Updated {cursor.rowcount} rows")
conn.commit()

# UPDATE with WHERE
cursor.execute('''
    UPDATE conversations 
    SET success = 0 
    WHERE tokens_used < 100
''')
conn.commit()

# DELETE
cursor.execute('''
    DELETE FROM conversations 
    WHERE success = 0
''')
print(f"Deleted {cursor.rowcount} failed conversations")
conn.commit()
```

---

### **✅ MASTERY CHECK:**

Can you write these queries without looking?

1. Get all conversations from 'gemini' provider
2. Count total conversations per agent
3. Find average tokens used by successful queries
4. Join conversations with users and show usernames
5. Get top 5 most token-heavy queries

**If yes → You know SQL basics! 🎉**

---

## 🧪 **EXERCISE 2: Testing with pytest (2 hours)**

### **Why This Matters:**
- Professional code has tests
- Tests catch bugs before production
- Makes refactoring safer

### **What You'll Learn:**
- Write unit tests with pytest
- Test functions, classes, async code
- Mock external dependencies
- Measure test coverage

---

### **Part 1: Setup (5 minutes)**

```bash
# Install pytest
pip install pytest pytest-asyncio pytest-cov

# Create test file
# tests/test_agent.py
```

---

### **Part 2: Basic Tests (20 minutes)**

```python
# tests/test_agent.py
import pytest
from agent import select_agent, SimpleSemanticSearch

def test_select_agent_code_keywords():
    """Test that code-related queries select Code Assistant"""
    agent = select_agent("help me write python code")
    assert agent["name"] == "Code Assistant"
    assert agent["provider"] == "gemini"

def test_select_agent_research_keywords():
    """Test that research queries select Research Assistant"""
    agent = select_agent("search for AI news")
    assert agent["name"] == "Research Assistant"
    assert agent["provider"] == "perplexity"

def test_select_agent_default():
    """Test that generic queries select default Assistant"""
    agent = select_agent("hello")
    assert agent["name"] == "Assistant"
    assert agent["provider"] == "ollama"

def test_select_agent_creative_keywords():
    """Test creative writing queries"""
    agent = select_agent("write a story about robots")
    assert agent["name"] == "Creative Writer"
```

**Run tests:**
```bash
pytest tests/test_agent.py -v
```

---

### **Part 3: Testing Classes (25 minutes)**

```python
def test_semantic_search_add_document():
    """Test adding documents to search index"""
    search = SimpleSemanticSearch()
    
    search.add_document("Python programming language")
    assert len(search.documents) == 1
    
    search.add_document("JavaScript coding")
    assert len(search.documents) == 2

def test_semantic_search_query():
    """Test searching documents"""
    search = SimpleSemanticSearch()
    search.add_document("Python is great for data science")
    search.add_document("Weather is sunny today")
    
    results = search.search("Python programming", top_k=2)
    
    assert len(results) > 0
    assert "Python" in results[0].content

def test_semantic_search_empty_query():
    """Test search with empty query"""
    search = SimpleSemanticSearch()
    search.add_document("Test content")
    
    results = search.search("", top_k=5)
    assert len(results) == 0

def test_semantic_search_no_documents():
    """Test search on empty index"""
    search = SimpleSemanticSearch()
    results = search.search("test query", top_k=5)
    assert len(results) == 0
```

---

### **Part 4: Testing Async Functions (20 minutes)**

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_query_ollama():
    """Test Ollama API call"""
    from agent import query_ollama
    
    response = await query_ollama("What is 2+2?")
    assert isinstance(response, str)
    assert len(response) > 0

@pytest.mark.asyncio  
async def test_query_gemini_with_context():
    """Test Gemini with context"""
    from agent import query_gemini
    
    context = "Previous: User asked about Python"
    response = await query_gemini("Tell me more", context=context)
    assert isinstance(response, str)
```

---

### **Part 5: Mocking (30 minutes)**

```python
from unittest.mock import Mock, patch, AsyncMock

def test_select_agent_with_mock():
    """Test agent selection without actually calling APIs"""
    agent = select_agent("code help")
    # Just testing selection logic, not API calls
    assert agent["name"] == "Code Assistant"

@pytest.mark.asyncio
@patch('agent.query_ollama')
async def test_process_query_mocked(mock_ollama):
    """Test processing with mocked API call"""
    from agent import process_query
    
    # Mock the response
    mock_ollama.return_value = "Mocked response"
    
    response = await process_query("test query")
    
    assert response == "Mocked response"
    mock_ollama.assert_called_once()

@pytest.mark.asyncio
async def test_api_fallback():
    """Test fallback when primary API fails"""
    from agent import query_azure
    
    # Azure not configured, should fallback to Ollama
    response = await query_azure("test")
    assert isinstance(response, str)
```

---

### **Part 6: Fixtures (20 minutes)**

```python
@pytest.fixture
def search_with_data():
    """Fixture providing pre-populated search engine"""
    search = SimpleSemanticSearch()
    search.add_document("Python programming")
    search.add_document("JavaScript coding")
    search.add_document("Machine learning")
    return search

def test_search_with_fixture(search_with_data):
    """Use fixture for testing"""
    results = search_with_data.search("Python", top_k=1)
    assert len(results) == 1
    assert "Python" in results[0].content

@pytest.fixture
async def mock_api_response():
    """Fixture for async mocking"""
    return "Mocked AI response"

@pytest.mark.asyncio
async def test_with_async_fixture(mock_api_response):
    """Test using async fixture"""
    assert mock_api_response == "Mocked AI response"
```

---

### **Part 7: Coverage (15 minutes)**

```bash
# Run with coverage
pytest tests/ --cov=agent --cov-report=html

# View coverage report
# Open htmlcov/index.html in browser

# Aim for 70%+ coverage
```

---

### **✅ MASTERY CHECK:**

Can you write tests for:
1. A function that returns a value?
2. A function that raises an exception?
3. An async function?
4. A class method?
5. Mock an external API call?

**If yes → You can test your code! 🎉**

---

## 🐳 **EXERCISE 3: Docker Basics (2 hours)**

### **Why This Matters:**
- Modern deployment uses containers
- Docker ensures "works on my machine" = "works everywhere"
- Essential for production systems

### **What You'll Learn:**
- Create Dockerfile
- Build images
- Run containers
- Manage container lifecycle
- Docker Compose for multi-service apps

---

### **Part 1: Dockerize ENTAERA (45 minutes)**

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements-local-models.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements-local-models.txt

# Copy application code
COPY agent.py .
COPY .env .

# Expose port (if adding API later)
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run application
CMD ["python", "agent.py"]
```

**Build and run:**
```bash
# Build image
docker build -t entaera:latest .

# Run container
docker run -it entaera:latest

# Run in background
docker run -d --name entaera-app entaera:latest

# View logs
docker logs entaera-app

# Stop container
docker stop entaera-app

# Remove container
docker rm entaera-app
```

---

### **Part 2: Docker Commands (30 minutes)**

```bash
# List images
docker images

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Execute command in running container
docker exec -it entaera-app bash

# Copy files from container
docker cp entaera-app:/app/conversation_memory.pkl ./

# Inspect container
docker inspect entaera-app

# View resource usage
docker stats entaera-app

# Remove image
docker rmi entaera:latest

# Clean up everything
docker system prune -a
```

---

### **Part 3: Docker Compose (45 minutes)**

```yaml
# docker-compose.yml
version: '3.8'

services:
  entaera:
    build: .
    container_name: entaera-app
    environment:
      - OLLAMA_HOST=http://ollama:11434
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    depends_on:
      - ollama
    restart: unless-stopped

  ollama:
    image: ollama/ollama:latest
    container_name: ollama-server
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    container_name: entaera-db
    environment:
      - POSTGRES_DB=entaera
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

volumes:
  ollama-data:
  postgres-data:
```

**Run with Docker Compose:**
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

---

### **✅ MASTERY CHECK:**

Can you:
1. Write a Dockerfile?
2. Build and run a container?
3. Debug a running container?
4. Use Docker Compose for multi-service setup?

**If yes → Docker basics mastered! 🎉**

---

## 📝 **EXERCISE 4: Git Workflow (1 hour)**

### **Why This Matters:**
- Version control is essential
- Professional teams use Git workflow
- Safe collaboration without breaking code

### **What You'll Learn:**
- Feature branch workflow
- Commit message conventions
- Pull requests
- Merge conflict resolution

---

### **Part 1: Feature Branch Workflow (20 minutes)**

```bash
# Check current branch
git branch

# Create and switch to feature branch
git checkout -b feature/add-faiss-search

# Make changes to code
# Edit agent.py, add FAISS implementation

# Check what changed
git status
git diff

# Stage changes
git add agent.py

# Commit with good message
git commit -m "feat: integrate FAISS semantic search

- Replace SimpleSemanticSearch with FAISS
- Add 384-dimensional embeddings
- Benchmark shows 10x speedup
- Maintains backward compatibility"

# Push to remote
git push origin feature/add-faiss-search
```

---

### **Part 2: Commit Message Convention (10 minutes)**

```bash
# Format: <type>: <description>

# Types:
feat: new feature
fix: bug fix
docs: documentation
style: formatting
refactor: code restructure
test: adding tests
chore: maintenance

# Examples:
git commit -m "feat: add health check endpoint"
git commit -m "fix: resolve rate limiting bug in gemini provider"
git commit -m "docs: update README with Docker instructions"
git commit -m "test: add pytest suite for agent selection"
git commit -m "refactor: extract API logic into separate module"
```

---

### **Part 3: Pull Request Workflow (15 minutes)**

```bash
# After pushing feature branch:
# 1. Go to GitHub
# 2. Click "Compare & pull request"
# 3. Write description:

Title: Integrate FAISS Semantic Search

Description:
## Changes
- Replaced TF-IDF with FAISS vector search
- Added sentence-transformers for embeddings
- Benchmarked performance improvement

## Testing
- [x] Unit tests pass
- [x] Manual testing with 1000 documents
- [x] Performance 10x faster than TF-IDF

## Breaking Changes
None - backward compatible

# 4. Request review
# 5. Address feedback
# 6. Merge when approved
```

---

### **Part 4: Merge Conflicts (15 minutes)**

```bash
# Scenario: Someone else modified the same file

# Update your branch with main
git checkout main
git pull origin main
git checkout feature/add-faiss-search
git merge main

# If conflict:
# Auto-merging agent.py
# CONFLICT (content): Merge conflict in agent.py

# Open agent.py, look for:
# <<<<<<< HEAD
# Your changes
# =======
# Their changes
# >>>>>>> main

# Fix manually, then:
git add agent.py
git commit -m "fix: resolve merge conflict in agent.py"
git push origin feature/add-faiss-search
```

---

### **✅ MASTERY CHECK:**

Can you:
1. Create a feature branch?
2. Write good commit messages?
3. Create a pull request?
4. Resolve merge conflicts?

**If yes → Git workflow mastered! 🎉**

---

## 📊 **EXERCISE 5: Logging & Monitoring (1.5 hours)**

### **Why This Matters:**
- Production debugging requires logs
- Know what's happening in your app
- Track errors and performance

### **What You'll Learn:**
- Structured logging
- Log levels
- Error tracking with Sentry
- Performance monitoring

---

### **Part 1: Replace print() with logging (30 minutes)**

```python
# agent.py - OLD WAY
print("Agent: Code Assistant")
print("Error: API failed")

# agent.py - NEW WAY
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('entaera.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Use different levels
logger.debug("Detailed debug info")
logger.info("Agent: Code Assistant")
logger.warning("API rate limit approaching")
logger.error("API call failed", exc_info=True)
logger.critical("System failure - shutting down")
```

---

### **Part 2: Structured Logging (30 minutes)**

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add extra fields
        if hasattr(record, 'agent'):
            log_obj['agent'] = record.agent
        if hasattr(record, 'provider'):
            log_obj['provider'] = record.provider
        if hasattr(record, 'tokens'):
            log_obj['tokens'] = record.tokens
            
        return json.dumps(log_obj)

# Use it
handler = logging.FileHandler('entaera.json.log')
handler.setFormatter(JSONFormatter())

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Log with extra data
logger.info(
    "Agent processing query",
    extra={
        'agent': 'Code Assistant',
        'provider': 'gemini',
        'tokens': 250
    }
)
```

---

### **Part 3: Error Tracking with Sentry (30 minutes)**

```python
# Install Sentry
# pip install sentry-sdk

import sentry_sdk

# Initialize Sentry
sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
    environment="production"
)

# Automatic error capture
try:
    result = 1 / 0
except Exception as e:
    # Error automatically sent to Sentry
    logger.error("Division error", exc_info=True)
    sentry_sdk.capture_exception(e)

# Add context
sentry_sdk.set_context("agent", {
    "name": "Code Assistant",
    "provider": "gemini"
})

# Add user context
sentry_sdk.set_user({
    "id": "user123",
    "username": "saurabh"
})

# Custom events
sentry_sdk.capture_message(
    "High token usage detected",
    level="warning"
)
```

---

### **✅ MASTERY CHECK:**

Can you:
1. Replace print() with proper logging?
2. Use different log levels correctly?
3. Create structured JSON logs?
4. Set up error tracking?

**If yes → Production logging mastered! 🎉**

---

## 🎓 **COMPLETION CHECKLIST**

After completing all exercises:

- [ ] Can write SQL queries (SELECT, JOIN, WHERE, GROUP BY)
- [ ] Can write pytest tests for functions and classes
- [ ] Can mock external dependencies in tests
- [ ] Can create Dockerfile and build images
- [ ] Can run containers and use Docker Compose
- [ ] Can use Git feature branch workflow
- [ ] Can write good commit messages
- [ ] Can resolve merge conflicts
- [ ] Can set up structured logging
- [ ] Can track errors in production

**If all checked → You have production engineering skills! 🚀**

---

## 📚 **NEXT STEPS**

Apply these skills to your projects:

1. **ENTAERA:**
   - Add SQL database for conversations
   - Write pytest tests (aim for 50% coverage)
   - Dockerize the application
   - Add structured logging

2. **Snap2Slides:**
   - Test API routes with pytest
   - Add Sentry error tracking
   - Docker deployment

3. **N8N:**
   - Store workflow results in PostgreSQL
   - Add comprehensive logging
   - Docker Compose setup

---

**You now have the production skills that separate professionals from hobbyists.** 💪
