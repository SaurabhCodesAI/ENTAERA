"""
ENTAERA Smart API Rate Limiter
Optimized for Gemini Student Pro + Perplexity Airtel API limits
"""

import asyncio
import json
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

@dataclass
class APILimits:
    """API rate limit configuration."""
    requests_per_minute: int
    requests_per_day: int
    tokens_per_request: int
    tokens_per_minute: Optional[int] = None

@dataclass 
class UsageStats:
    """Track API usage statistics."""
    requests_today: int = 0
    requests_this_minute: int = 0
    tokens_used_today: int = 0
    tokens_used_this_minute: int = 0
    last_reset_date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    last_reset_minute: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))

class SmartRateLimiter:
    """Smart rate limiter respecting API constraints."""
    
    def __init__(self):
        # Define API limits based on your actual quotas
        self.limits = {
            "gemini": APILimits(
                requests_per_minute=4,      # 5 limit, use 4 for safety
                requests_per_day=20,        # 25 limit, use 20 for safety  
                tokens_per_request=800000,  # 1M limit, use 800k
                tokens_per_minute=1000000
            ),
            "perplexity": APILimits(
                requests_per_minute=45,     # 50 limit, use 45 for safety
                requests_per_day=200,       # Conservative daily limit
                tokens_per_request=120000,  # 128k limit for Sonar Pro
                tokens_per_minute=None
            ),
            "azure": APILimits(
                requests_per_minute=60,     # Azure is more generous
                requests_per_day=100,       # Budget-based limit
                tokens_per_request=4000,    # GPT-3.5-turbo context
                tokens_per_minute=None
            )
        }
        
        # Usage tracking
        self.usage_file = Path("./cache/api_usage.json")
        self.usage_file.parent.mkdir(exist_ok=True)
        self.usage_stats = self._load_usage_stats()
        
        # Request queues for rate limiting
        self.request_queues = {
            api: deque() for api in self.limits.keys()
        }
        
        # Semaphores for concurrent request limiting
        self.semaphores = {
            api: asyncio.Semaphore(limits.requests_per_minute) 
            for api, limits in self.limits.items()
        }
    
    def _load_usage_stats(self) -> Dict[str, UsageStats]:
        """Load usage statistics from file."""
        if self.usage_file.exists():
            try:
                with open(self.usage_file, 'r') as f:
                    data = json.load(f)
                    return {
                        api: UsageStats(**stats) 
                        for api, stats in data.items()
                    }
            except Exception:
                pass
        
        return {api: UsageStats() for api in self.limits.keys()}
    
    def _save_usage_stats(self):
        """Save usage statistics to file."""
        try:
            data = {
                api: {
                    "requests_today": stats.requests_today,
                    "requests_this_minute": stats.requests_this_minute,
                    "tokens_used_today": stats.tokens_used_today,
                    "tokens_used_this_minute": stats.tokens_used_this_minute,
                    "last_reset_date": stats.last_reset_date,
                    "last_reset_minute": stats.last_reset_minute
                }
                for api, stats in self.usage_stats.items()
            }
            
            with open(self.usage_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Could not save usage stats: {e}")
    
    def _reset_counters_if_needed(self, api: str):
        """Reset counters if time periods have passed."""
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        this_minute = now.strftime("%Y-%m-%d %H:%M")
        
        stats = self.usage_stats[api]
        
        # Reset daily counters
        if stats.last_reset_date != today:
            stats.requests_today = 0
            stats.tokens_used_today = 0
            stats.last_reset_date = today
        
        # Reset minute counters
        if stats.last_reset_minute != this_minute:
            stats.requests_this_minute = 0
            stats.tokens_used_this_minute = 0
            stats.last_reset_minute = this_minute
    
    async def can_make_request(self, api: str, estimated_tokens: int = 1000) -> bool:
        """Check if we can make a request within limits."""
        self._reset_counters_if_needed(api)
        
        limits = self.limits[api]
        stats = self.usage_stats[api]
        
        # Check daily limits
        if stats.requests_today >= limits.requests_per_day:
            return False
        
        if stats.tokens_used_today + estimated_tokens > limits.requests_per_day * limits.tokens_per_request:
            return False
        
        # Check minute limits
        if stats.requests_this_minute >= limits.requests_per_minute:
            return False
        
        if (limits.tokens_per_minute and 
            stats.tokens_used_this_minute + estimated_tokens > limits.tokens_per_minute):
            return False
        
        return True
    
    async def acquire(self, api: str, estimated_tokens: int = 1000) -> bool:
        """Acquire permission to make an API request."""
        # Check if we can make the request
        if not await self.can_make_request(api, estimated_tokens):
            return False
        
        # Acquire semaphore
        await self.semaphores[api].acquire()
        
        # Update usage stats
        self._reset_counters_if_needed(api)
        stats = self.usage_stats[api]
        stats.requests_today += 1
        stats.requests_this_minute += 1
        stats.tokens_used_today += estimated_tokens
        stats.tokens_used_this_minute += estimated_tokens
        
        # Save updated stats
        self._save_usage_stats()
        
        return True
    
    def release(self, api: str):
        """Release the semaphore after request completion."""
        self.semaphores[api].release()
    
    def get_usage_stats(self, api: str) -> Dict:
        """Get current usage statistics for an API."""
        self._reset_counters_if_needed(api)
        
        limits = self.limits[api]
        stats = self.usage_stats[api]
        
        return {
            "api": api,
            "daily_usage": {
                "requests": f"{stats.requests_today}/{limits.requests_per_day}",
                "tokens": f"{stats.tokens_used_today:,}",
                "percentage": f"{(stats.requests_today / limits.requests_per_day) * 100:.1f}%"
            },
            "minute_usage": {
                "requests": f"{stats.requests_this_minute}/{limits.requests_per_minute}",
                "tokens": f"{stats.tokens_used_this_minute:,}",
                "percentage": f"{(stats.requests_this_minute / limits.requests_per_minute) * 100:.1f}%"
            },
            "remaining": {
                "daily_requests": limits.requests_per_day - stats.requests_today,
                "minute_requests": limits.requests_per_minute - stats.requests_this_minute
            }
        }
    
    def get_all_usage_stats(self) -> Dict:
        """Get usage statistics for all APIs."""
        return {
            api: self.get_usage_stats(api) 
            for api in self.limits.keys()
        }
    
    async def wait_for_availability(self, api: str, estimated_tokens: int = 1000) -> bool:
        """Wait until we can make a request (with timeout)."""
        max_wait_time = 300  # 5 minutes max wait
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            if await self.can_make_request(api, estimated_tokens):
                return True
            
            # Wait before checking again
            await asyncio.sleep(10)  # Check every 10 seconds
        
        return False
    
    def print_usage_report(self):
        """Print a formatted usage report."""
        print("\n📊 API Usage Report")
        print("=" * 50)
        
        for api in self.limits.keys():
            stats = self.get_usage_stats(api)
            
            print(f"\n🔗 {api.upper()} API:")
            print(f"   Daily: {stats['daily_usage']['requests']} ({stats['daily_usage']['percentage']})")
            print(f"   Minute: {stats['minute_usage']['requests']} ({stats['minute_usage']['percentage']})")
            print(f"   Remaining today: {stats['remaining']['daily_requests']} requests")
            
            # Alert if approaching limits
            daily_pct = float(stats['daily_usage']['percentage'].replace('%', ''))
            if daily_pct >= 75:
                print(f"   ⚠️  Warning: {daily_pct:.1f}% of daily quota used")
            elif daily_pct >= 90:
                print(f"   🚨 Alert: {daily_pct:.1f}% of daily quota used!")

# Global rate limiter instance
rate_limiter = SmartRateLimiter()

async def test_rate_limiter():
    """Test the rate limiter functionality."""
    print("🧪 Testing Smart Rate Limiter")
    print("=" * 40)
    
    # Test Gemini limits (most restrictive)
    print("\n🤖 Testing Gemini API limits...")
    
    for i in range(3):
        if await rate_limiter.acquire("gemini", 1000):
            print(f"   ✅ Gemini request {i+1} approved")
            rate_limiter.release("gemini")
        else:
            print(f"   ❌ Gemini request {i+1} blocked (rate limit)")
    
    # Test Perplexity limits
    print("\n🔍 Testing Perplexity API limits...")
    
    for i in range(3):
        if await rate_limiter.acquire("perplexity", 5000):
            print(f"   ✅ Perplexity request {i+1} approved")
            rate_limiter.release("perplexity")
        else:
            print(f"   ❌ Perplexity request {i+1} blocked (rate limit)")
    
    # Print usage report
    rate_limiter.print_usage_report()

if __name__ == "__main__":
    asyncio.run(test_rate_limiter())