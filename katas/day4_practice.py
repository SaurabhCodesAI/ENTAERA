
# This is your practice file for the Day 4 Kata.
# Complete the exercises from katas/day4_data_modeling.md here.

from datetime import datetime
from pydantic import BaseModel
from typing import List

# --- Exercise 1: The User and Message Models ---

class User(BaseModel):
    # TODO: Define fields
    pass

class Message(BaseModel):
    # TODO: Define fields, including the nested User model
    pass

print("--- Exercise 1 ---")
# TODO: Instantiate User and Message, then print the message


# --- Exercise 2: The ChatThread Model ---

class ChatThread(BaseModel):
    thread_id: str
    messages: List[Message] = []

    def add_message(self, sender: User, content: str):
        # TODO: Implement the method to add a new message
        pass

print("\n--- Exercise 2 ---")
# TODO: Instantiate ChatThread, add messages, and print the thread


# --- Exercise 3: The ContextWindow ---

class ChatThreadWithContext(ChatThread): # Extend the previous model
    def get_context_window(self, max_messages: int = 5) -> List[Message]:
        # TODO: Implement the method to get the last n messages
        pass

print("\n--- Exercise 3 ---")
# TODO: Create a thread with 10+ messages and test get_context_window


# --- Exercise 4: Serialization and Deserialization ---

print("\n--- Exercise 4 ---")
# TODO: Use the ChatThread object from Exercise 2
# 1. Convert it to a dictionary using .model_dump() and print it.
# 2. Create a new ChatThread object from the dictionary using .model_validate().
# 3. Print the new object to verify it matches the original.

