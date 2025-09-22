#!/usr/bin/env python3
"""
Day 3 Kata 3.2 - AI Conversation Data Structures Demo
Demonstrates comprehensive conversation management, context windows, and memory persistence.
"""

import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

from src.entaera.core.conversation import (
    ConversationManager, Conversation, Message, MessageRole, MessageType,
    ConversationStatus, ContextWindow, MessageMetadata
)


def demo_basic_conversation_creation():
    """Demonstrate basic conversation creation and message handling."""
    print("\n💬 Basic Conversation Creation Demo")
    print("=" * 50)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = ConversationManager(temp_dir)
        
        # Create a new conversation
        conversation = manager.create_conversation(
            title="AI Assistant Chat",
            description="Getting help with Python programming"
        )
        
        print(f"✅ Created conversation: {conversation.title}")
        print(f"📝 Conversation ID: {conversation.id}")
        print(f"📅 Created at: {conversation.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Add system message
        system_message = Message(
            role=MessageRole.SYSTEM,
            content="You are a helpful Python programming assistant. Be concise and provide practical examples.",
            metadata=MessageMetadata(
                model_name="gpt-4",
                source_system="demo"
            )
        )
        conversation.add_message(system_message)
        print("✅ Added system message")
        
        # Add user messages and assistant responses
        interactions = [
            ("How do I create a list in Python?", "You can create a list using square brackets: my_list = [1, 2, 3, 'hello']"),
            ("What about list comprehensions?", "List comprehensions provide a concise way: [x**2 for x in range(5)] creates [0, 1, 4, 9, 16]"),
            ("Can you show me how to filter a list?", "Use list comprehension with a condition: [x for x in my_list if x > 5] keeps only items greater than 5")
        ]
        
        for user_content, assistant_content in interactions:
            # Add user message
            user_msg = Message(
                role=MessageRole.USER,
                content=user_content,
                metadata=MessageMetadata(
                    source_system="demo",
                    tags=["question", "python"]
                )
            )
            conversation.add_message(user_msg)
            
            # Add assistant response
            assistant_msg = Message(
                role=MessageRole.ASSISTANT,
                content=assistant_content,
                parent_id=user_msg.id,
                metadata=MessageMetadata(
                    model_name="gpt-4",
                    prompt_tokens=50,
                    completion_tokens=30,
                    total_tokens=80,
                    processing_time=1.2,
                    tags=["answer", "python", "example"]
                )
            )
            conversation.add_message(assistant_msg)
        
        print(f"✅ Added {len(interactions)} interactions")
        print(f"📊 Total messages: {len(conversation.messages)}")
        print(f"📊 Total tokens: {conversation.stats.total_tokens}")
        print(f"⏱️  Duration: {conversation.stats.duration_seconds:.1f} seconds")
        
        return manager, conversation


def demo_context_window_management():
    """Demonstrate context window management strategies."""
    print("\n🧠 Context Window Management Demo")
    print("=" * 50)
    
    # Create conversation with small context window for demonstration
    conversation = Conversation(title="Context Window Test")
    conversation.context_window.max_tokens = 300  # Small window
    conversation.context_window.reserve_tokens = 50
    conversation.context_window.strategy = "sliding"
    
    print(f"📏 Context window: {conversation.context_window.max_tokens} tokens")
    print(f"🛡️  Reserved tokens: {conversation.context_window.reserve_tokens}")
    print(f"📐 Strategy: {conversation.context_window.strategy}")
    
    # Add system message (always included)
    system_msg = Message(
        role=MessageRole.SYSTEM,
        content="You are a helpful assistant. Keep responses concise."
    )
    conversation.add_message(system_msg)
    print("✅ Added system message (always included)")
    
    # Add many messages to fill context window
    for i in range(15):
        user_msg = Message(
            role=MessageRole.USER,
            content=f"This is user message number {i+1} with some content to demonstrate context window management."
        )
        conversation.add_message(user_msg)
        
        assistant_msg = Message(
            role=MessageRole.ASSISTANT,
            content=f"This is assistant response number {i+1} providing information about the user's request."
        )
        conversation.add_message(assistant_msg)
        
        # Check context window status
        utilization = conversation.context_window.utilization_percentage()
        print(f"📈 After interaction {i+1}: {utilization:.1f}% utilized, {len(conversation.messages)} messages")
        
        if conversation.context_window.needs_management():
            print("⚠️  Context window management triggered!")
    
    # Show final state
    context_messages = conversation.get_context_messages()
    print(f"\n📋 Final context contains {len(context_messages)} messages:")
    for msg in context_messages:
        role_emoji = {"system": "🤖", "user": "👤", "assistant": "🤖"}
        content_preview = msg.content[:40] + "..." if len(msg.content) > 40 else msg.content
        print(f"   {role_emoji.get(msg.role.value, '💬')} {msg.role.value}: {content_preview}")


def demo_conversation_search():
    """Demonstrate conversation search and filtering capabilities."""
    print("\n🔍 Conversation Search Demo")
    print("=" * 50)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = ConversationManager(temp_dir)
        
        # Create diverse conversations
        conversations_data = [
            ("Python Basics", "Learning Python fundamentals", ["python", "beginner"], [
                ("What is Python?", "Python is a high-level programming language."),
                ("How do I install Python?", "You can download Python from python.org.")
            ]),
            ("Web Development", "Building web applications", ["web", "javascript", "html"], [
                ("What is HTML?", "HTML is the markup language for web pages."),
                ("How do I make a responsive website?", "Use CSS media queries and flexible layouts.")
            ]),
            ("Data Science", "Python for data analysis", ["python", "data", "science"], [
                ("What is pandas?", "Pandas is a data manipulation library for Python."),
                ("How do I visualize data?", "Use matplotlib or seaborn for data visualization.")
            ]),
            ("Machine Learning", "AI and ML concepts", ["ai", "ml", "python"], [
                ("What is machine learning?", "ML is a method of teaching computers to learn patterns."),
                ("How do I train a model?", "Split data, choose algorithm, train, and validate.")
            ])
        ]
        
        for title, description, tags, interactions in conversations_data:
            conv = manager.create_conversation(title, description)
            conv.tags = tags
            
            for user_content, assistant_content in interactions:
                conv.add_message(Message(role=MessageRole.USER, content=user_content))
                conv.add_message(Message(role=MessageRole.ASSISTANT, content=assistant_content))
            
            print(f"✅ Created conversation: {title} ({len(interactions)} interactions)")
        
        # Demonstrate search functionality
        search_queries = ["Python", "web", "data", "machine learning", "visualization"]
        
        for query in search_queries:
            print(f"\n🔎 Searching for: '{query}'")
            results = manager.search_conversations(query, limit=3)
            
            if results:
                for i, result in enumerate(results, 1):
                    print(f"   {i}. {result.conversation.title} (score: {result.relevance_score:.1f})")
                    print(f"      📝 {result.match_summary}")
                    if result.matching_messages:
                        msg = result.matching_messages[0]
                        preview = msg.content[:50] + "..." if len(msg.content) > 50 else msg.content
                        print(f"      💬 \"{preview}\"")
            else:
                print(f"   ❌ No results found for '{query}'")
        
        # Show overall statistics
        stats = manager.get_stats()
        print(f"\n📊 Overall Statistics:")
        print(f"   📚 Total conversations: {stats['total_conversations']}")
        print(f"   💬 Total messages: {stats['total_messages']}")
        print(f"   🎯 Total tokens: {stats['total_tokens']}")
        
        status_dist = stats['status_distribution']
        for status, count in status_dist.items():
            if count > 0:
                print(f"   📋 {status.title()}: {count}")


def demo_conversation_persistence():
    """Demonstrate conversation persistence and loading."""
    print("\n💾 Conversation Persistence Demo")
    print("=" * 50)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"🗂️  Storage location: {temp_dir}")
        
        # Create first manager and conversations
        print("\n🆕 Creating new conversation manager...")
        manager1 = ConversationManager(temp_dir)
        
        conv1 = manager1.create_conversation("Persistent Chat 1", "First test conversation")
        conv1.add_message(Message(role=MessageRole.USER, content="Hello, this is a test message."))
        conv1.add_message(Message(role=MessageRole.ASSISTANT, content="Hi there! I'm here to help."))
        
        conv2 = manager1.create_conversation("Persistent Chat 2", "Second test conversation")
        conv2.add_message(Message(role=MessageRole.USER, content="Can you help me with coding?"))
        conv2.add_message(Message(role=MessageRole.ASSISTANT, content="Of course! What would you like to know?"))
        conv2.status = ConversationStatus.COMPLETED
        conv2.completed_at = datetime.now(timezone.utc)
        
        manager1.save_all_conversations()
        print(f"✅ Saved {len(manager1.conversations)} conversations to storage")
        
        # Verify files were created
        storage_files = list(Path(temp_dir).glob("*.json"))
        print(f"📁 Storage files created: {len(storage_files)}")
        for file in storage_files:
            print(f"   📄 {file.name} ({file.stat().st_size} bytes)")
        
        # Create second manager to test loading
        print("\n🔄 Creating new manager to test persistence...")
        manager2 = ConversationManager(temp_dir)
        
        loaded_conversations = manager2.list_conversations()
        print(f"✅ Loaded {len(loaded_conversations)} conversations from storage")
        
        for conv in loaded_conversations:
            print(f"   📝 {conv.title}: {len(conv.messages)} messages, status: {conv.status.value}")
            if conv.messages:
                first_msg = conv.messages[0]
                preview = first_msg.content[:40] + "..." if len(first_msg.content) > 40 else first_msg.content
                print(f"      💬 First message: \"{preview}\"")
        
        # Test export/import functionality
        print("\n📤 Testing export/import...")
        if loaded_conversations:
            conv_to_export = loaded_conversations[0]
            exported_data = manager2.export_conversation(conv_to_export.id)
            print(f"✅ Exported conversation: {len(str(exported_data))} characters")
            
            # Create new manager and import
            with tempfile.TemporaryDirectory() as import_dir:
                manager3 = ConversationManager(import_dir)
                imported_conv = manager3.import_conversation(exported_data)
                print(f"✅ Imported conversation: {imported_conv.title}")
                print(f"   📊 Messages: {len(imported_conv.messages)}")
                print(f"   🏷️  Tags: {imported_conv.tags}")


def demo_conversation_statistics():
    """Demonstrate conversation statistics and analytics."""
    print("\n📈 Conversation Statistics Demo")
    print("=" * 50)
    
    conversation = Conversation(title="Analytics Test")
    
    # Simulate a realistic conversation with varied timing
    base_time = datetime.now(timezone.utc) - timedelta(minutes=30)
    
    # Add system message
    system_msg = Message(
        role=MessageRole.SYSTEM,
        content="You are a helpful coding assistant.",
        timestamp=base_time
    )
    conversation.add_message(system_msg)
    
    # Add realistic conversation flow
    interactions = [
        ("Can you help me with Python functions?", "Of course! Functions in Python are defined using the 'def' keyword.", 2),
        ("How do I pass arguments?", "You can pass arguments inside the parentheses: def my_function(arg1, arg2):", 1),
        ("What about return values?", "Use the 'return' statement to send a value back: return result", 1.5),
        ("Can you show me an example?", "Here's a simple example:\n\ndef add_numbers(a, b):\n    return a + b\n\nresult = add_numbers(5, 3)", 3),
        ("That's helpful, thank you!", "You're welcome! Feel free to ask if you have more questions.", 0.5)
    ]
    
    current_time = base_time
    for i, (user_content, assistant_content, delay_minutes) in enumerate(interactions):
        current_time += timedelta(minutes=delay_minutes)
        
        # User message
        user_msg = Message(
            role=MessageRole.USER,
            content=user_content,
            timestamp=current_time,
            metadata=MessageMetadata(
                source_system="demo",
                tags=["question"]
            )
        )
        conversation.add_message(user_msg)
        
        # Assistant response (1 minute later)
        current_time += timedelta(minutes=1)
        assistant_msg = Message(
            role=MessageRole.ASSISTANT,
            content=assistant_content,
            timestamp=current_time,
            metadata=MessageMetadata(
                model_name="gpt-4",
                prompt_tokens=40 + i*10,
                completion_tokens=25 + i*5,
                total_tokens=65 + i*15,
                processing_time=0.8 + i*0.2,
                tags=["answer", "python"]
            )
        )
        conversation.add_message(assistant_msg)
    
    # Display statistics
    stats = conversation.stats
    print(f"📊 Conversation Statistics for: {conversation.title}")
    print(f"   💬 Total messages: {stats.total_messages}")
    print(f"   👤 User messages: {stats.user_messages}")
    print(f"   🤖 Assistant messages: {stats.assistant_messages}")
    print(f"   🔧 System messages: {stats.system_messages}")
    print(f"   🎯 Total tokens: {stats.total_tokens}")
    print(f"   📝 Prompt tokens: {stats.prompt_tokens}")
    print(f"   ✨ Completion tokens: {stats.completion_tokens}")
    print(f"   ⏱️  Duration: {stats.duration_seconds/60:.1f} minutes")
    print(f"   📈 Messages per minute: {stats.messages_per_minute():.1f}")
    print(f"   🔢 Tokens per message: {stats.tokens_per_message():.1f}")
    print(f"   📅 First message: {stats.first_message_at.strftime('%H:%M:%S')}")
    print(f"   📅 Last message: {stats.last_message_at.strftime('%H:%M:%S')}")
    
    # Context window information
    ctx = conversation.context_window
    print(f"\n🧠 Context Window:")
    print(f"   📏 Max tokens: {ctx.max_tokens}")
    print(f"   🔄 Current tokens: {ctx.current_tokens}")
    print(f"   🛡️  Reserved tokens: {ctx.reserve_tokens}")
    print(f"   📊 Utilization: {ctx.utilization_percentage():.1f}%")
    print(f"   💡 Available tokens: {ctx.available_tokens()}")
    print(f"   ⚠️  Needs management: {'Yes' if ctx.needs_management() else 'No'}")


def demo_message_metadata_and_features():
    """Demonstrate advanced message features and metadata."""
    print("\n🏷️  Message Metadata and Features Demo")
    print("=" * 50)
    
    conversation = Conversation(title="Advanced Features")
    
    # Message with rich metadata
    rich_message = Message(
        role=MessageRole.ASSISTANT,
        content="Here's a comprehensive explanation with multiple features.",
        message_type=MessageType.TEXT,
        metadata=MessageMetadata(
            model_name="gpt-4-turbo",
            model_version="1.0.0",
            prompt_tokens=150,
            completion_tokens=75,
            total_tokens=225,
            processing_time=2.3,
            temperature=0.7,
            max_tokens=1000,
            source_system="advanced_demo",
            tags=["detailed", "comprehensive", "educational"],
            attachments=["diagram.png", "example.py"],
            references=["https://docs.python.org", "https://stackoverflow.com/..."]
        )
    )
    conversation.add_message(rich_message)
    
    print("✅ Created message with rich metadata:")
    print(f"   🏷️  Tags: {rich_message.metadata.tags}")
    print(f"   📎 Attachments: {rich_message.metadata.attachments}")
    print(f"   🔗 References: {len(rich_message.metadata.references)} links")
    print(f"   🎯 Tokens: {rich_message.metadata.total_tokens}")
    print(f"   ⏱️  Processing time: {rich_message.metadata.processing_time}s")
    print(f"   🌡️  Temperature: {rich_message.metadata.temperature}")
    
    # Pin important message
    conversation.pin_message(rich_message.id)
    print(f"📌 Pinned important message (ID: {rich_message.id[:8]}...)")
    
    # Add more messages
    for i in range(3):
        msg = Message(
            role=MessageRole.USER,
            content=f"Follow-up question {i+1}",
            metadata=MessageMetadata(tags=[f"followup_{i+1}"])
        )
        conversation.add_message(msg)
    
    # Show pinned messages
    pinned_ids = conversation.pinned_messages
    print(f"📌 Pinned messages: {len(pinned_ids)}")
    
    # Create conversation summary
    summary = conversation.create_summary()
    print(f"\n📄 Created conversation summary:")
    print(f"   📝 Summary: {summary.summary}")
    print(f"   🔑 Key points: {len(summary.key_points)}")
    print(f"   🏷️  Topics: {summary.topics}")
    print(f"   📊 Messages summarized: {summary.messages_summarized}")
    print(f"   🎯 Tokens summarized: {summary.total_tokens_summarized}")
    
    # Message age and editing
    first_message = conversation.messages[0]
    print(f"\n⏰ Message aging:")
    print(f"   📅 First message age: {first_message.get_age_seconds():.1f} seconds")
    print(f"   ✏️  Is edited: {first_message.is_edited()}")
    
    # Simulate editing
    first_message.content = "This message has been edited for clarity."
    first_message.edited_at = datetime.now(timezone.utc)
    print(f"   ✏️  After edit: {first_message.is_edited()}")


def main():
    """Run all conversation management demonstrations."""
    print("🚀 ENTAERA - Day 3 Kata 3.2: AI Conversation Data Structures")
    print("=" * 70)
    print("Demonstrating comprehensive conversation management, context windows, and persistence")
    
    try:
        # Run all demonstrations
        demo_basic_conversation_creation()
        demo_context_window_management()
        demo_conversation_search()
        demo_conversation_persistence()
        demo_conversation_statistics()
        demo_message_metadata_and_features()
        
        print("\n" + "=" * 70)
        print("✅ AI Conversation Data Structures Demo Completed Successfully!")
        print("✅ Comprehensive conversation management working perfectly")
        print("✅ Context window management functioning correctly")
        print("✅ Conversation search and filtering operational")
        print("✅ Persistent storage with atomic file operations")
        print("✅ Rich metadata and advanced features implemented")
        print("✅ Statistics and analytics fully functional")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        raise


if __name__ == "__main__":
    main()