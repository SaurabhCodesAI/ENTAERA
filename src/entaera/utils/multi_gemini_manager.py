"""
ENTAERA Multi-Gemini API Manager
Smart load balancing across 3 Gemini Student Pro accounts
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class AccountStatus(Enum):
    """Status of a Gemini account."""
    HEALTHY = "healthy"
    RATE_LIMITED = "rate_limited"
    ERROR = "error"
    DISABLED = "disabled"

@dataclass
class GeminiAccount:
    """Represents a single Gemini API account."""
    account_id: str
    api_key: str
    name: str
    
    # Rate limiting
    requests_per_minute: int = 5
    requests_per_day: int = 25
    tokens_per_minute: int = 1000000
    
    # Current usage tracking
    current_minute_requests: int = 0
    current_day_requests: int = 0
    current_minute_tokens: int = 0
    
    # Timing
    minute_reset_time: datetime = field(default_factory=datetime.now)
    day_reset_time: datetime = field(default_factory=lambda: datetime.now().replace(hour=0, minute=0, second=0))
    
    # Health
    status: AccountStatus = AccountStatus.HEALTHY
    last_error: Optional[str] = None
    consecutive_errors: int = 0
    
    def reset_minute_if_needed(self):
        """Reset minute counters if minute has passed."""
        now = datetime.now()
        if now >= self.minute_reset_time + timedelta(minutes=1):
            self.current_minute_requests = 0
            self.current_minute_tokens = 0
            self.minute_reset_time = now
    
    def reset_day_if_needed(self):
        """Reset day counters if day has passed."""
        now = datetime.now()
        if now.date() > self.day_reset_time.date():
            self.current_day_requests = 0
            self.day_reset_time = now.replace(hour=0, minute=0, second=0)
    
    def can_make_request(self, estimated_tokens: int = 1000) -> bool:
        """Check if account can make a request."""
        self.reset_minute_if_needed()
        self.reset_day_if_needed()
        
        if self.status != AccountStatus.HEALTHY:
            return False
        
        # Check rate limits with safety buffer (80%)
        minute_limit = int(self.requests_per_minute * 0.8)
        day_limit = int(self.requests_per_day * 0.8)
        token_limit = int(self.tokens_per_minute * 0.8)
        
        return (
            self.current_minute_requests < minute_limit and
            self.current_day_requests < day_limit and
            self.current_minute_tokens + estimated_tokens < token_limit
        )
    
    def record_request(self, tokens_used: int):
        """Record a successful request."""
        self.current_minute_requests += 1
        self.current_day_requests += 1
        self.current_minute_tokens += tokens_used
        self.consecutive_errors = 0
        self.status = AccountStatus.HEALTHY
        self.last_error = None
    
    def record_error(self, error: str):
        """Record an error."""
        self.consecutive_errors += 1
        self.last_error = error
        
        if self.consecutive_errors >= 3:
            self.status = AccountStatus.ERROR
            logger.warning(f"Account {self.name} marked as ERROR after {self.consecutive_errors} consecutive errors")
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics."""
        self.reset_minute_if_needed()
        self.reset_day_if_needed()
        
        return {
            "account_id": self.account_id,
            "name": self.name,
            "status": self.status.value,
            "requests_today": self.current_day_requests,
            "requests_this_minute": self.current_minute_requests,
            "tokens_this_minute": self.current_minute_tokens,
            "daily_usage_percent": (self.current_day_requests / self.requests_per_day) * 100,
            "minute_usage_percent": (self.current_minute_requests / self.requests_per_minute) * 100,
            "consecutive_errors": self.consecutive_errors,
            "last_error": self.last_error
        }

class MultiGeminiManager:
    """Manages multiple Gemini accounts with intelligent load balancing."""
    
    def __init__(self, accounts: List[Dict[str, str]]):
        """Initialize with list of account configurations."""
        self.accounts = []
        
        for i, account_config in enumerate(accounts):
            account = GeminiAccount(
                account_id=f"gemini_{i+1}",
                api_key=account_config["api_key"],
                name=account_config.get("name", f"Account_{i+1}")
            )
            self.accounts.append(account)
        
        self.current_account_index = 0
        self.total_requests = 0
        self.total_errors = 0
        
        logger.info(f"Initialized MultiGeminiManager with {len(self.accounts)} accounts")
    
    def get_best_account(self, estimated_tokens: int = 1000) -> Optional[GeminiAccount]:
        """Get the best available account for a request."""
        
        # First, try to find a healthy account that can handle the request
        healthy_accounts = [acc for acc in self.accounts if acc.can_make_request(estimated_tokens)]
        
        if not healthy_accounts:
            logger.warning("No healthy accounts available for request")
            return None
        
        # Use round-robin among healthy accounts
        if len(healthy_accounts) == 1:
            return healthy_accounts[0]
        
        # Find account with lowest usage
        best_account = min(healthy_accounts, key=lambda acc: (
            acc.current_day_requests + acc.current_minute_requests * 0.1
        ))
        
        return best_account
    
    async def make_request(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Make a request using the best available account."""
        
        estimated_tokens = len(prompt.split()) * 1.3  # Rough token estimation
        account = self.get_best_account(int(estimated_tokens))
        
        if not account:
            raise Exception("No available Gemini accounts for request")
        
        try:
            # Import here to avoid circular imports
            import google.generativeai as genai
            
            # Configure the account
            genai.configure(api_key=account.api_key)
            
            # Make the request
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt, **kwargs)
            
            # Record successful request
            response_tokens = len(response.text.split()) * 1.3 if response.text else 100
            account.record_request(int(estimated_tokens + response_tokens))
            self.total_requests += 1
            
            logger.info(f"Successful request using {account.name}")
            
            return {
                "success": True,
                "response": response.text,
                "account_used": account.name,
                "tokens_estimated": int(estimated_tokens + response_tokens)
            }
            
        except Exception as e:
            account.record_error(str(e))
            self.total_errors += 1
            
            logger.error(f"Request failed on {account.name}: {e}")
            
            # Try with another account if available
            remaining_accounts = [acc for acc in self.accounts if acc != account and acc.can_make_request(estimated_tokens)]
            if remaining_accounts:
                logger.info("Trying with another account...")
                return await self.make_request(prompt, **kwargs)
            
            raise e
    
    def get_total_usage_stats(self) -> Dict[str, Any]:
        """Get combined usage statistics for all accounts."""
        
        all_stats = [account.get_usage_stats() for account in self.accounts]
        
        total_requests_today = sum(stats["requests_today"] for stats in all_stats)
        total_requests_minute = sum(stats["requests_this_minute"] for stats in all_stats)
        total_tokens_minute = sum(stats["tokens_this_minute"] for stats in all_stats)
        
        healthy_accounts = len([acc for acc in self.accounts if acc.status == AccountStatus.HEALTHY])
        
        return {
            "total_accounts": len(self.accounts),
            "healthy_accounts": healthy_accounts,
            "total_requests_today": total_requests_today,
            "total_requests_this_minute": total_requests_minute,
            "total_tokens_this_minute": total_tokens_minute,
            "combined_daily_limit": len(self.accounts) * 25,
            "combined_minute_limit": len(self.accounts) * 5,
            "combined_token_limit": len(self.accounts) * 1000000,
            "daily_usage_percent": (total_requests_today / (len(self.accounts) * 25)) * 100,
            "minute_usage_percent": (total_requests_minute / (len(self.accounts) * 5)) * 100,
            "lifetime_requests": self.total_requests,
            "lifetime_errors": self.total_errors,
            "error_rate": (self.total_errors / max(1, self.total_requests)) * 100,
            "account_details": all_stats
        }
    
    def print_usage_report(self):
        """Print a detailed usage report."""
        stats = self.get_total_usage_stats()
        
        print("\n📊 MULTI-GEMINI USAGE REPORT")
        print("=" * 50)
        print(f"🤖 Total Accounts: {stats['total_accounts']}")
        print(f"💚 Healthy Accounts: {stats['healthy_accounts']}")
        print(f"📈 Requests Today: {stats['total_requests_today']}/{stats['combined_daily_limit']}")
        print(f"⚡ Requests This Minute: {stats['total_requests_this_minute']}/{stats['combined_minute_limit']}")
        print(f"🔢 Tokens This Minute: {stats['total_tokens_this_minute']:,}/{stats['combined_token_limit']:,}")
        print(f"📊 Daily Usage: {stats['daily_usage_percent']:.1f}%")
        print(f"⚠️ Error Rate: {stats['error_rate']:.2f}%")
        
        print("\n🔍 Account Details:")
        for account_stats in stats['account_details']:
            status_emoji = {"healthy": "💚", "rate_limited": "🟡", "error": "🔴", "disabled": "⚫"}
            emoji = status_emoji.get(account_stats['status'], "❓")
            
            print(f"   {emoji} {account_stats['name']}: {account_stats['requests_today']}/25 daily, "
                  f"{account_stats['requests_this_minute']}/5 minute")
            
            if account_stats['last_error']:
                print(f"      ⚠️ Last error: {account_stats['last_error']}")


# Example usage and testing
async def test_multi_gemini():
    """Test the multi-Gemini setup."""
    
    # Example account configuration (replace with your actual keys)
    accounts = [
        {"api_key": "your_first_gemini_key", "name": "Primary"},
        {"api_key": "your_second_gemini_key", "name": "Secondary"},
        {"api_key": "your_third_gemini_key", "name": "Tertiary"}
    ]
    
    manager = MultiGeminiManager(accounts)
    
    # Test requests
    test_prompts = [
        "Write a Python function to calculate fibonacci numbers",
        "Explain how machine learning works in simple terms",
        "Generate a JavaScript function for handling API calls",
        "What are the best practices for code optimization?"
    ]
    
    print("🧪 Testing Multi-Gemini Load Balancing...")
    
    for i, prompt in enumerate(test_prompts, 1):
        try:
            print(f"\n🔄 Test {i}: '{prompt[:50]}...'")
            result = await manager.make_request(prompt)
            print(f"   ✅ Success using {result['account_used']}")
            print(f"   📝 Response: {result['response'][:100]}...")
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    # Print final usage report
    manager.print_usage_report()

if __name__ == "__main__":
    asyncio.run(test_multi_gemini())