# ENTAERA Kata - Day 13: SQL Mastery & Data Persistence

## 🎯 Learning Objectives

AI agents need to remember things permanently. While semantic search (Day 5) helps find relevant memories, SQL databases are the gold standard for structured, persistent storage. Today you'll master SQL fundamentals and learn to integrate databases into your Python applications.

- **Understand relational database concepts (tables, rows, columns, relationships)**
- **Master essential SQL: CREATE, SELECT, INSERT, UPDATE, DELETE**
- **Use JOIN operations to combine data from multiple tables**
- **Filter and aggregate data with WHERE, GROUP BY, HAVING**
- **Use Python's `sqlite3` module to interact with databases**
- **Design a schema for storing agent conversations and memories**
- **Implement database-backed persistence for your AI agent**

---

## 🧠 For the Absolute Beginner

### What is a Database?
A **database** is like an organized filing cabinet for your data. Instead of storing everything in Python variables (which disappear when your program stops), you save it to a database file on disk. Next time your program runs, all that data is still there.

### What is SQL?
**SQL** (Structured Query Language) is the language you use to talk to databases. It's like asking questions:
- "Show me all users over age 25" → `SELECT * FROM users WHERE age > 25`
- "Add a new user named Alice" → `INSERT INTO users (name) VALUES ('Alice')`

### What is a Table?
Think of a table like a spreadsheet. It has **columns** (like "name", "age", "email") and **rows** (each row is one person). Every row must have the same columns.

```
users table:
+----+-------+-----+------------------+
| id | name  | age | email            |
+----+-------+-----+------------------+
|  1 | Alice |  25 | alice@email.com  |
|  2 | Bob   |  30 | bob@email.com    |
+----+-------+-----+------------------+
```

---

## 📚 SQL Fundamentals

### 1. Creating Tables (Schema Design)

```sql
-- Create a users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    email TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a conversations table
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create a messages table
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER,
    role TEXT CHECK(role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);
```

**Key Concepts:**
- `PRIMARY KEY`: Unique identifier for each row
- `AUTOINCREMENT`: Database automatically assigns the next number
- `NOT NULL`: This field must have a value
- `UNIQUE`: No two rows can have the same value
- `FOREIGN KEY`: Links to another table (relationships)
- `CHECK`: Validates that values meet a condition

### 2. Inserting Data

```sql
-- Insert a single user
INSERT INTO users (name, age, email) 
VALUES ('Alice', 25, 'alice@email.com');

-- Insert multiple users
INSERT INTO users (name, age, email) VALUES
    ('Bob', 30, 'bob@email.com'),
    ('Charlie', 35, 'charlie@email.com');

-- Insert conversation
INSERT INTO conversations (user_id, title) 
VALUES (1, 'My First Chat');

-- Insert messages
INSERT INTO messages (conversation_id, role, content) VALUES
    (1, 'user', 'Hello, who are you?'),
    (1, 'assistant', 'I am ENTAERA, your AI assistant!');
```

### 3. Querying Data (SELECT)

```sql
-- Get all users
SELECT * FROM users;

-- Get specific columns
SELECT name, email FROM users;

-- Filter with WHERE
SELECT * FROM users WHERE age > 25;

-- Multiple conditions
SELECT * FROM users WHERE age > 25 AND email LIKE '%@email.com';

-- Order results
SELECT * FROM users ORDER BY age DESC;

-- Limit results
SELECT * FROM users LIMIT 5;

-- Count rows
SELECT COUNT(*) FROM users;

-- Get unique values
SELECT DISTINCT role FROM messages;
```

### 4. Updating Data

```sql
-- Update a specific user
UPDATE users 
SET age = 26 
WHERE name = 'Alice';

-- Update multiple fields
UPDATE users 
SET age = 31, email = 'bob_new@email.com' 
WHERE id = 2;
```

### 5. Deleting Data

```sql
-- Delete a specific user
DELETE FROM users WHERE id = 3;

-- Delete all users over 40
DELETE FROM users WHERE age > 40;

-- Delete all rows (careful!)
DELETE FROM users;
```

### 6. JOIN Operations (Combining Tables)

```sql
-- INNER JOIN: Get conversations with user info
SELECT users.name, conversations.title, conversations.created_at
FROM conversations
INNER JOIN users ON conversations.user_id = users.id;

-- LEFT JOIN: Get all users, even those without conversations
SELECT users.name, COUNT(conversations.id) as conversation_count
FROM users
LEFT JOIN conversations ON users.id = conversations.user_id
GROUP BY users.id;

-- Get full conversation history with messages
SELECT 
    users.name,
    conversations.title,
    messages.role,
    messages.content,
    messages.timestamp
FROM messages
INNER JOIN conversations ON messages.conversation_id = conversations.id
INNER JOIN users ON conversations.user_id = users.id
WHERE conversations.id = 1
ORDER BY messages.timestamp;
```

### 7. Aggregation (GROUP BY)

```sql
-- Count messages per conversation
SELECT conversation_id, COUNT(*) as message_count
FROM messages
GROUP BY conversation_id;

-- Average age by email domain
SELECT 
    SUBSTR(email, INSTR(email, '@') + 1) as domain,
    AVG(age) as avg_age
FROM users
GROUP BY domain;

-- Filter aggregated results with HAVING
SELECT conversation_id, COUNT(*) as message_count
FROM messages
GROUP BY conversation_id
HAVING message_count > 5;
```

---

## 🐍 Python + SQLite Integration

### Basic Setup

```python
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, db_path: str = "agent.db"):
        """Initialize database connection."""
        self.db_path = db_path
        self.conn = None
        
    def connect(self):
        """Connect to database."""
        self.conn = sqlite3.connect(self.db_path)
        # Return rows as dictionaries instead of tuples
        self.conn.row_factory = sqlite3.Row
        
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
```

### Creating Schema

```python
def create_schema(self):
    """Create database tables."""
    cursor = self.conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create conversations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Create messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER,
            role TEXT CHECK(role IN ('user', 'assistant', 'system')),
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        )
    """)
    
    self.conn.commit()
```

### Inserting Data

```python
def add_user(self, name: str, email: str) -> int:
    """Add a new user and return their ID."""
    cursor = self.conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        (name, email)
    )
    self.conn.commit()
    return cursor.lastrowid

def add_message(self, conversation_id: int, role: str, content: str) -> int:
    """Add a message to a conversation."""
    cursor = self.conn.cursor()
    cursor.execute(
        "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
        (conversation_id, role, content)
    )
    self.conn.commit()
    return cursor.lastrowid
```

### Querying Data

```python
def get_user(self, user_id: int) -> Optional[Dict]:
    """Get user by ID."""
    cursor = self.conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    return dict(row) if row else None

def get_conversation_messages(self, conversation_id: int) -> List[Dict]:
    """Get all messages in a conversation."""
    cursor = self.conn.cursor()
    cursor.execute("""
        SELECT role, content, timestamp 
        FROM messages 
        WHERE conversation_id = ?
        ORDER BY timestamp
    """, (conversation_id,))
    return [dict(row) for row in cursor.fetchall()]

def search_messages(self, query: str) -> List[Dict]:
    """Search messages by content."""
    cursor = self.conn.cursor()
    cursor.execute("""
        SELECT m.id, m.content, m.timestamp, c.title, u.name
        FROM messages m
        JOIN conversations c ON m.conversation_id = c.id
        JOIN users u ON c.user_id = u.id
        WHERE m.content LIKE ?
        ORDER BY m.timestamp DESC
    """, (f"%{query}%",))
    return [dict(row) for row in cursor.fetchall()]
```

---

## 💻 Exercises

Create `katas/day13_practice.py` and complete these exercises.

### Exercise 1: Basic Schema Design

Design and create a database schema for a simple e-commerce system:

```python
import sqlite3

# TODO: Create database connection
conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

# TODO: Create a 'products' table with:
# - id (PRIMARY KEY, AUTOINCREMENT)
# - name (TEXT, NOT NULL)
# - price (REAL, NOT NULL)
# - category (TEXT)
# - stock (INTEGER, DEFAULT 0)

# TODO: Create an 'orders' table with:
# - id (PRIMARY KEY, AUTOINCREMENT)
# - customer_name (TEXT, NOT NULL)
# - total_amount (REAL)
# - order_date (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

# TODO: Create an 'order_items' table with:
# - id (PRIMARY KEY, AUTOINCREMENT)
# - order_id (INTEGER, FOREIGN KEY to orders)
# - product_id (INTEGER, FOREIGN KEY to products)
# - quantity (INTEGER, NOT NULL)
# - price (REAL, NOT NULL)
```

### Exercise 2: Data Insertion

```python
# TODO: Insert 5 products into the products table
products = [
    ("Laptop", 999.99, "Electronics", 10),
    ("Mouse", 29.99, "Electronics", 50),
    ("Desk Chair", 199.99, "Furniture", 15),
    ("Notebook", 4.99, "Stationery", 100),
    ("Coffee Mug", 12.99, "Kitchen", 30)
]

# TODO: Insert an order
# TODO: Insert multiple order items for that order
```

### Exercise 3: Querying with Filters

```python
# TODO: Get all products in the 'Electronics' category

# TODO: Get all products with price less than $50

# TODO: Get products sorted by price (descending)

# TODO: Count how many products are in each category

# TODO: Find the total value of inventory (price * stock) for each product
```

### Exercise 4: JOIN Operations

```python
# TODO: Get all orders with customer names and total amounts

# TODO: Get detailed order information including:
#       - Order ID
#       - Customer name
#       - Product names
#       - Quantities
#       - Order date

# TODO: Calculate total revenue per product category
```

### Exercise 5: Agent Memory Database

Create a complete database-backed memory system for an AI agent:

```python
class AgentMemoryDB:
    def __init__(self, db_path: str = "agent_memory.db"):
        # TODO: Initialize database connection
        # TODO: Create schema with users, conversations, messages tables
        pass
    
    def create_user(self, name: str, email: str) -> int:
        # TODO: Insert new user and return ID
        pass
    
    def start_conversation(self, user_id: int, title: str = "New Chat") -> int:
        # TODO: Create new conversation and return ID
        pass
    
    def add_message(self, conversation_id: int, role: str, content: str):
        # TODO: Add message to conversation
        pass
    
    def get_conversation_history(self, conversation_id: int) -> list:
        # TODO: Return all messages in conversation with timestamps
        pass
    
    def search_past_conversations(self, user_id: int, keyword: str) -> list:
        # TODO: Search all user conversations for keyword
        # Return list of conversations containing the keyword
        pass
    
    def get_user_stats(self, user_id: int) -> dict:
        # TODO: Return statistics:
        # - total_conversations
        # - total_messages
        # - first_conversation_date
        # - last_conversation_date
        pass
```

### Exercise 6: Advanced Queries

```python
# TODO: Find users who have sent more than 10 messages

# TODO: Get the most active conversation (most messages)

# TODO: Find all conversations that mention "Python" or "AI"

# TODO: Calculate average messages per conversation for each user

# TODO: Find conversations with no messages (orphaned conversations)

# TODO: Get the last 5 messages across all conversations
```

### Exercise 7: Data Migration

```python
# TODO: Add a new column 'sentiment' to messages table
# Use ALTER TABLE

# TODO: Write a function to update sentiment based on keywords:
# - "good", "great", "awesome" → "positive"
# - "bad", "terrible", "awful" → "negative"
# - everything else → "neutral"

def update_sentiment(conn):
    # TODO: Implement sentiment analysis and update
    pass
```

---

## 🚀 Advanced Concepts

### Transactions
```python
# Ensure all-or-nothing execution
try:
    cursor.execute("BEGIN TRANSACTION")
    cursor.execute("INSERT INTO users ...")
    cursor.execute("INSERT INTO conversations ...")
    cursor.execute("COMMIT")
except Exception as e:
    cursor.execute("ROLLBACK")
    print(f"Transaction failed: {e}")
```

### Indexes for Performance
```python
# Create index on frequently queried columns
cursor.execute("CREATE INDEX idx_messages_conversation ON messages(conversation_id)")
cursor.execute("CREATE INDEX idx_messages_timestamp ON messages(timestamp)")
```

### Full-Text Search
```python
# SQLite FTS5 for advanced search
cursor.execute("""
    CREATE VIRTUAL TABLE messages_fts USING fts5(content, conversation_id)
""")

# Search with ranking
cursor.execute("""
    SELECT * FROM messages_fts 
    WHERE messages_fts MATCH 'python AND machine learning'
    ORDER BY rank
""")
```

---

## 🔗 Hybrid: SQL + Vector Search

The ultimate AI memory system combines both:
- **SQL**: Structured data, relationships, exact filters
- **Vector Search (FAISS)**: Semantic similarity

```python
class HybridMemory:
    def __init__(self):
        self.db = AgentMemoryDB()
        self.faiss_index = FAISSIndex()  # From Day 5
    
    def add_memory(self, user_id: int, content: str):
        # Store in SQL
        message_id = self.db.add_message(...)
        
        # Store embedding in FAISS
        embedding = self.get_embedding(content)
        self.faiss_index.add(embedding, metadata={"id": message_id})
    
    def search(self, query: str, user_id: int) -> list:
        # 1. Semantic search with FAISS
        similar_ids = self.faiss_index.search(query, top_k=20)
        
        # 2. Filter by user_id using SQL
        results = self.db.filter_messages_by_ids(similar_ids, user_id)
        
        return results
```

---

## 🤔 Mastery Questions

### Beginner
1. **What's the difference between PRIMARY KEY and UNIQUE?**
   - PRIMARY KEY uniquely identifies rows and cannot be NULL. A table can have multiple UNIQUE constraints but only one PRIMARY KEY

2. **When do you use INNER JOIN vs LEFT JOIN?**
   - INNER JOIN returns only matching rows. LEFT JOIN returns all rows from left table, with NULLs for non-matching right table rows

### Intermediate
3. **What are SQL injection attacks? How do you prevent them?**
   - Malicious SQL code inserted via user input. Prevent with parameterized queries (`?` placeholders) instead of string concatenation

4. **What's the difference between WHERE and HAVING?**
   - WHERE filters rows before grouping. HAVING filters groups after GROUP BY aggregation

### Advanced
5. **When should you use an index? What's the trade-off?**
   - Use for frequently queried columns. Trade-off: faster reads, slower writes (index must be updated)

6. **What's database normalization? What are the normal forms?**
   - Organizing data to reduce redundancy. 1NF: atomic values, 2NF: no partial dependencies, 3NF: no transitive dependencies

---

## 🎯 Integration Path

Now you can combine all your skills:
- **Day 0**: Python fundamentals → Build clean database code
- **Day 1**: Text processing → Clean text before storing in DB
- **Day 4**: Data modeling → Pydantic models ↔ database rows
- **Day 5**: Semantic search → Hybrid search (SQL + vectors)
- **Day 12**: Unit testing → Test database operations
- **Day 13**: SQL mastery → Persistent agent memory

**Time to Complete:** 6-8 hours

You now have **production-grade persistence**! 🎉
