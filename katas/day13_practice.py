"""
ENTAERA Kata - Day 13: SQL Mastery Practice
Complete all exercises to master SQL and database operations.
"""

import sqlite3
from typing import List, Dict, Optional
from datetime import datetime

# =============================================================================
# Exercise 1: Basic Schema Design
# =============================================================================

print("=" * 60)
print("Exercise 1: Basic Schema Design")
print("=" * 60)

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

print("Schema created successfully!")


# =============================================================================
# Exercise 2: Data Insertion
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 2: Data Insertion")
print("=" * 60)

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

print("Data inserted successfully!")


# =============================================================================
# Exercise 3: Querying with Filters
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 3: Querying with Filters")
print("=" * 60)

# TODO: Get all products in the 'Electronics' category

# TODO: Get all products with price less than $50

# TODO: Get products sorted by price (descending)

# TODO: Count how many products are in each category

# TODO: Find the total value of inventory (price * stock) for each product


# =============================================================================
# Exercise 4: JOIN Operations
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 4: JOIN Operations")
print("=" * 60)

# TODO: Get all orders with customer names and total amounts

# TODO: Get detailed order information including:
#       - Order ID
#       - Customer name
#       - Product names
#       - Quantities
#       - Order date

# TODO: Calculate total revenue per product category


# =============================================================================
# Exercise 5: Agent Memory Database
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 5: Agent Memory Database")
print("=" * 60)

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

# Test the AgentMemoryDB
# memory_db = AgentMemoryDB()
# user_id = memory_db.create_user("Alice", "alice@email.com")
# conv_id = memory_db.start_conversation(user_id, "Python Help")
# memory_db.add_message(conv_id, "user", "How do I use list comprehensions?")
# memory_db.add_message(conv_id, "assistant", "List comprehensions are...")


# =============================================================================
# Exercise 6: Advanced Queries
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 6: Advanced Queries")
print("=" * 60)

# TODO: Find users who have sent more than 10 messages

# TODO: Get the most active conversation (most messages)

# TODO: Find all conversations that mention "Python" or "AI"

# TODO: Calculate average messages per conversation for each user

# TODO: Find conversations with no messages (orphaned conversations)

# TODO: Get the last 5 messages across all conversations


# =============================================================================
# Exercise 7: Data Migration
# =============================================================================

print("\n" + "=" * 60)
print("Exercise 7: Data Migration")
print("=" * 60)

# TODO: Add a new column 'sentiment' to messages table
# Use ALTER TABLE

# TODO: Write a function to update sentiment based on keywords:
# - "good", "great", "awesome" → "positive"
# - "bad", "terrible", "awful" → "negative"
# - everything else → "neutral"

def update_sentiment(conn):
    # TODO: Implement sentiment analysis and update
    pass

# update_sentiment(conn)

print("\n" + "=" * 60)
print("All exercises complete! Check your database.")
print("=" * 60)

# Clean up
conn.close()
