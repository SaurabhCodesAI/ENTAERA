"""
ENTAERA Multi-Agent System - Framework Integrated

Advanced version with semantic search, conversation memory, and context-aware responses.
"""

import os
import sys
import asyncio
import aiohttp
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import re
from collections import defaultdict
import pickle

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
AZURE_KEY = os.getenv("AZURE_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT", "https://azureopenaiserviceentaera.openai.azure.com/")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-35-turbo")
GEMINI_KEYS = [os.getenv("GEMINI_API_KEY"), os.getenv("GEMINI_API_KEY_2"), os.getenv("GEMINI_API_KEY_3")]
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

@dataclass
class SearchResult:
    content: str
    score: float
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ConversationEntry:
    query: str
    response: str
    agent_name: str
    provider: str
    timestamp: datetime
    def to_text(self): return f"{self.query} {self.response}"

class SimpleSemanticSearch:
    def __init__(self):
        self.documents = []
        self.word_freq = defaultdict(int)
        self.doc_count = defaultdict(int)
    def _tokenize(self, text):
        words = re.findall(r'\b\w+\b', text.lower())
        stop = {'the','a','an','and','or','but','in','on','at','to','for','of','is','are','was','were'}
        return [w for w in words if w not in stop and len(w)>2]
    def add_document(self, content, metadata=None):
        tokens = self._tokenize(content)
        doc = {"content":content,"tokens":tokens,"metadata":metadata or {},"timestamp":datetime.now()}
        self.documents.append(doc)
        for t in set(tokens): self.doc_count[t]+=1
        for t in tokens: self.word_freq[t]+=1
    def search(self, query, top_k=3, min_score=0.1):
        if not self.documents: return []
        tokens = self._tokenize(query)
        if not tokens: return []
        results = []
        for doc in self.documents:
            score = 0.0
            for t in tokens:
                if t in doc["tokens"]:
                    tf = doc["tokens"].count(t)/len(doc["tokens"])
                    idf = 1.0 + len(self.documents)/(1+self.doc_count.get(t,0))
                    score += tf*idf
            if score>=min_score:
                results.append(SearchResult(doc["content"],score,doc["timestamp"],doc["metadata"]))
        results.sort(key=lambda x:x.score,reverse=True)
        return results[:top_k]
    def clear(self):
        self.documents.clear()
        self.word_freq.clear()
        self.doc_count.clear()

class ConversationMemory:
    def __init__(self, max_history=100, storage_file="conversation_memory.pkl"):
        self.history = []
        self.max_history = max_history
        self.search_engine = SimpleSemanticSearch()
        self.stats = {"total_queries":0,"by_agent":defaultdict(int),"by_provider":defaultdict(int)}
        self.storage_file = storage_file
        self.load_from_disk()
    def add_interaction(self, query, response, agent_name, provider):
        entry = ConversationEntry(query,response,agent_name,provider,datetime.now())
        self.history.append(entry)
        if len(self.history)>self.max_history: self.history=self.history[-self.max_history:]
        self.search_engine.add_document(entry.to_text(),{"agent":agent_name,"provider":provider,"query":query})
        self.stats["total_queries"]+=1
        self.stats["by_agent"][agent_name]+=1
        self.stats["by_provider"][provider]+=1
        self.save_to_disk()
    def search_memory(self, query, top_k=3): return self.search_engine.search(query,top_k)
    def get_recent(self, n=5): return self.history[-n:]
    def get_context(self, query, max_items=3):
        if not self.history:
            return ""
        
        # Strategy: Smart hybrid context
        # 1. Get semantically relevant conversations (search in both query AND response)
        relevant_results = self.search_memory(query, top_k=max_items+1)
        relevant_queries = {r.metadata.get('query') for r in relevant_results} if relevant_results else set()
        
        # 2. Always include last 2 for conversation flow
        recent = self.history[-2:] if len(self.history) >= 2 else self.history
        
        # 3. Build smart context: relevant + recent, prioritizing semantic matches
        context_entries = []
        seen_queries = set()
        
        # First add semantically relevant matches
        for entry in self.history:
            if entry.query in relevant_queries and entry.query not in seen_queries:
                context_entries.append(entry)
                seen_queries.add(entry.query)
                if len(context_entries) >= max_items:
                    break
        
        # Then fill remaining slots with recent conversations
        if len(context_entries) < max_items:
            for entry in reversed(recent):  # Most recent first
                if entry.query not in seen_queries:
                    context_entries.append(entry)
                    seen_queries.add(entry.query)
                    if len(context_entries) >= max_items:
                        break
        
        if not context_entries:
            return ""
        
        # Sort by timestamp to maintain chronological order
        context_entries.sort(key=lambda x: x.timestamp)
        
        parts = ["Relevant conversation history:"]
        for i, entry in enumerate(context_entries, 1):
            parts.append(f"\n[Conversation {i}]")
            parts.append(f"User said: {entry.query}")
            response_text = entry.response[:250] + "..." if len(entry.response) > 250 else entry.response
            parts.append(f"You replied: {response_text}")
        
        return "\n".join(parts)
    def clear(self):
        self.history.clear()
        self.search_engine.clear()
        self.stats = {"total_queries":0,"by_agent":defaultdict(int),"by_provider":defaultdict(int)}
        self.save_to_disk()
    def get_stats(self):
        return {"total_queries":self.stats["total_queries"],"history_size":len(self.history),"by_agent":dict(self.stats["by_agent"]),"by_provider":dict(self.stats["by_provider"])}

    
    def save_to_disk(self):
        """Save conversation history to disk"""
        try:
            data = {
                "history": [(e.query, e.response, e.agent_name, e.provider, e.timestamp.isoformat()) for e in self.history],
                "stats": {
                    "total_queries": self.stats["total_queries"],
                    "by_agent": dict(self.stats["by_agent"]),
                    "by_provider": dict(self.stats["by_provider"])
                }
            }
            with open(self.storage_file, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            pass  # Silent fail
    
    def load_from_disk(self):
        """Load conversation history from disk"""
        if not os.path.exists(self.storage_file):
            return
        try:
            with open(self.storage_file, 'rb') as f:
                data = pickle.load(f)
            
            # Restore history
            self.history = []
            for q, r, a, p, t in data.get("history", []):
                entry = ConversationEntry(q, r, a, p, datetime.fromisoformat(t))
                self.history.append(entry)
                self.search_engine.add_document(entry.to_text(), {"agent": a, "provider": p, "query": q})
            
            # Restore stats
            saved_stats = data.get("stats", {})
            self.stats["total_queries"] = saved_stats.get("total_queries", 0)
            self.stats["by_agent"] = defaultdict(int, saved_stats.get("by_agent", {}))
            self.stats["by_provider"] = defaultdict(int, saved_stats.get("by_provider", {}))
            
            if len(self.history) > 0:
                print(f"[OK] Loaded {len(self.history)} previous conversations from disk")
        except Exception as e:
            pass  # Silent fail

memory = ConversationMemory()

# Agent definitions
AGENTS = [
    {
        "name": "Assistant",
        "provider": "ollama",
        "keywords": ["hello", "hi", "help", "what can you do", "abilities"],
        "priority": 1
    },
    {
        "name": "Code Assistant",
        "provider": "gemini",
        "keywords": ["code", "program", "python", "javascript", "debug", "fix", "function", "class"],
        "priority": 3
    },
    {
        "name": "Data Analyst",
        "provider": "gemini",
        "keywords": ["data", "analyze", "statistics", "chart", "graph", "csv", "dataframe"],
        "priority": 3
    },
    {
        "name": "Creative Writer",
        "provider": "gemini",
        "keywords": ["write", "story", "creative", "poem", "content", "blog"],
        "priority": 2
    },
    {
        "name": "Research Assistant",
        "provider": "perplexity",
        "keywords": ["search", "find", "research", "news", "current", "latest", "information"],
        "priority": 3
    }
]


async def query_ollama(query: str, context: str="") -> str:
    """Query Ollama local model"""
    try:
        if context:
            full_query = f"Here is our conversation history for context:\n{context}\n\nBased on this context, please answer the user's question. Reference previous responses when relevant.\n\nUser's current question: {query}"
        else:
            full_query = query
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{OLLAMA_HOST}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": full_query,
                    "stream": False
                },
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("response", "No response from Ollama")
                else:
                    return f"Ollama error: HTTP {response.status}"
    except asyncio.TimeoutError:
        return "Ollama timeout - model may be slow or not running"
    except Exception as e:
        return f"Ollama error: {str(e)}"


async def query_azure(query: str, context: str="") -> str:
    """Query Azure OpenAI with fallback to Ollama"""
    if not AZURE_KEY:
        print("Azure API key not set, falling back to Ollama...")
        return await query_ollama(query, context)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{AZURE_ENDPOINT}openai/deployments/{AZURE_DEPLOYMENT_NAME}/chat/completions?api-version=2023-05-15",
                headers={
                    "api-key": AZURE_KEY,
                    "Content-Type": "application/json"
                },
                json={
                    "messages": ([{"role": "system", "content": f"Here is the conversation history for context:\n{context}\n\nUse this context to provide relevant answers that reference previous responses when appropriate."}] if context else []) + [{"role": "user", "content": query}],
                    "max_tokens": 500
                },
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    print(f"Azure API error: {response.status}, falling back to Ollama...")
                    return await query_ollama(query, context)
    except Exception as e:
        print(f"Azure error: {str(e)}, falling back to Ollama...")
        return await query_ollama(query, context)


async def query_gemini(query: str, context: str="") -> str:
    """Query Google Gemini with key rotation"""
    for i, key in enumerate(GEMINI_KEYS):
        if not key:
            continue
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={key}",
                    json={
                        "contents": [{"parts": [{"text": (f"Conversation history:\n{context}\n\nBased on our previous conversation, answer this question:\n{query}" if context else query)}]}],
                        "generationConfig": {"maxOutputTokens": 500}
                    },
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result["candidates"][0]["content"]["parts"][0]["text"]
                    elif response.status == 429:
                        if i < len(GEMINI_KEYS) - 1:
                            print(f"Gemini key {i+1} quota exceeded, trying next key...")
                            continue
                        else:
                            print("All Gemini keys exhausted, falling back to Ollama...")
                            return await query_ollama(query, context)
                    else:
                        if i < len(GEMINI_KEYS) - 1:
                            print(f"Gemini error: {response.status}, trying next key...")
                            continue
        except Exception as e:
            if i < len(GEMINI_KEYS) - 1:
                print(f"Gemini error: {str(e)}, trying next key...")
                continue
    
    print("All Gemini attempts failed, falling back to Ollama...")
    return await query_ollama(query, context)


async def query_perplexity(query: str, context: str="") -> str:
    """Query Perplexity for web search"""
    if not PERPLEXITY_API_KEY:
        print("Perplexity API key not set, falling back to Ollama...")
        return await query_ollama(query, context)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "sonar",
                    "messages": ([{"role": "system", "content": f"Previous conversation:\n{context}\n\nUse this context to provide answers that build on our previous discussion."}] if context else []) + [{"role": "user", "content": query}],
                    "max_tokens": 500
                },
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    print(f"Perplexity API error: {response.status}, falling back to Ollama...")
                    return await query_ollama(query, context)
    except Exception as e:
        print(f"Perplexity error: {str(e)}, falling back to Ollama...")
        return await query_ollama(query, context)


def select_agent(query: str, use_context: bool = True) -> dict:
    """Select best agent based on keywords and context"""
    query_lower = query.lower()
    best_agent = AGENTS[0]  # Default to Assistant
    best_score = 0
    
    for agent in AGENTS:
        score = sum(keyword in query_lower for keyword in agent["keywords"]) * agent["priority"]
        if score > best_score:
            best_score = score
            best_agent = agent
    
    return best_agent


async def process_query(query: str, use_context: bool = True) -> str:
    """Process query through appropriate agent"""
    agent = select_agent(query, use_context)
    context = memory.get_context(query, max_items=2) if use_context and memory.history else ""
    
    print(f"\nAgent: {agent['name']} (Provider: {agent['provider']})")
    if context:
        contexts = len([line for line in context.split('\n') if line.startswith('[Conversation')])
        print(f"Context: Using {contexts} relevant past conversation(s)")
    print("-" * 60)
    
    if agent["provider"] == "ollama":
        response = await query_ollama(query, context)
    elif agent["provider"] == "azure":
        response = await query_azure(query, context)
    elif agent["provider"] == "gemini":
        response = await query_gemini(query, context)
    elif agent["provider"] == "perplexity":
        response = await query_perplexity(query, context)
    else:
        response = "Unknown provider"
    
    memory.add_interaction(query, response, agent["name"], agent["provider"])
    return response


async def main():
    """Main interactive loop"""
    print("\n" + "=" * 60)
    print("ENTAERA Multi-Agent System - Framework Integrated")
    print("=" * 60)
    print("\n Features:")
    print("  • Semantic search across conversation history")
    print("  • Context-aware AI responses")
    print("  • Conversation memory with 5 specialized agents")
    print("=" * 60)
    print("=" * 60)
    print("\nAvailable commands:")
    print("  /agents       - List all agents")
    print("  /status       - Show system status")
    print("  /memory [n]   - Show recent n interactions (default: 5)")
    print("  /search <q>   - Search conversation history")
    print("  /stats        - Show memory statistics")
    print("  /clear        - Clear conversation memory")
    print("  /quit         - Exit")
    print("\nType your query or command:")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            if user_input == "/quit":
                print("\nGoodbye!")
                break
            
            elif user_input == "/agents":
                print("\nAvailable Agents:")
                for agent in AGENTS:
                    provider_icon = "[LOCAL]" if agent['provider'] == "ollama" else ("[WEB]" if agent['provider'] == "perplexity" else "[AI]")
                    print(f"  {provider_icon} {agent['name']} - Keywords: {', '.join(agent['keywords'][:3])}")
            
            elif user_input == "/status":
                print("\nSystem Status:")
                print(f"  Ollama:      [OK] ({OLLAMA_HOST})")
                print(f"  Azure:       {'[OK]' if AZURE_KEY else '[NOT SET]'}")
                print(f"  Gemini:      [OK] ({sum(1 for k in GEMINI_KEYS if k)} keys)")
                print(f"  Perplexity:  {'[OK]' if PERPLEXITY_API_KEY else '[NOT SET]'}")
                print(f"  Memory:      {len(memory.history)} interactions")
            
            elif user_input.startswith("/memory"):
                args = user_input.split(maxsplit=1)[1] if len(user_input.split())>1 else ""
                n = int(args) if args.isdigit() else 5
                recent = memory.get_recent(n)
                if not recent:
                    print("\nNo conversation history yet.")
                else:
                    print(f"\nRecent {len(recent)} interactions:")
                    print("=" * 60)
                    for i,e in enumerate(recent,1):
                        print(f"\n{i}. [{e.timestamp.strftime('%H:%M:%S')}] {e.agent_name}")
                        print(f"   Q: {e.query[:60]}{'...' if len(e.query)>60 else ''}")
                        print(f"   A: {e.response[:60]}{'...' if len(e.response)>60 else ''}")
            
            elif user_input.startswith("/search"):
                args = user_input.split(maxsplit=1)[1] if len(user_input.split())>1 else ""
                if not args:
                    print("\nUsage: /search <query>")
                else:
                    results = memory.search_memory(args, 5)
                    if not results:
                        print(f"\nNo results found for: {args}")
                    else:
                        print(f"\nSearch results for '{args}':")
                        print("=" * 60)
                        for i,r in enumerate(results,1):
                            agent = r.metadata.get('agent', 'Unknown')
                            query = r.metadata.get('query', '')
                            print(f"\n{i}. [{r.timestamp.strftime('%H:%M:%S')}] {agent} (Score: {r.score:.2f})")
                            print(f"   Q: {query[:60]}{'...' if len(query)>60 else ''}")
            
            elif user_input == "/stats":
                stats = memory.get_stats()
                print("\nMemory Statistics:")
                print("=" * 60)
                print(f"Total Queries:     {stats['total_queries']}")
                print(f"History Size:      {stats['history_size']}")
                if stats['by_agent']:
                    print("\nBy Agent:")
                    for agent,count in sorted(stats['by_agent'].items(), key=lambda x:x[1], reverse=True):
                        print(f"  {agent}: {count}")
                if stats['by_provider']:
                    print("\nBy Provider:")
                    for provider,count in sorted(stats['by_provider'].items(), key=lambda x:x[1], reverse=True):
                        print(f"  {provider}: {count}")
            
            elif user_input == "/clear":
                memory.clear()
                print("\n[OK] Memory cleared!")
            
            else:
                response = await process_query(user_input)
                print(f"\n{response}")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            print("\n\nGoodbye!")
            break


if __name__ == "__main__":
    asyncio.run(main())
