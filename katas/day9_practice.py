
# This is your practice file for the Day 9 Kata.
# Complete the exercises from katas/day9_api_resilience.md here.

import time
import random
from collections import deque
from dataclasses import dataclass
from typing import List, Optional

# --- Exercise 1: Simple Rate Limiter ---

class RateLimiter:
    def __init__(self, requests_per_minute: int):
        # TODO: Initialize variables
        pass

    def can_request(self) -> bool:
        # TODO: Implement the check logic
        pass

    def record_request(self):
        # TODO: Record the timestamp of a request
        pass

print("--- Exercise 1 ---")
# TODO: Test your RateLimiter in a loop


# --- Exercise 2: API Account Health ---

@dataclass
class APIAccount:
    # TODO: Define fields and methods
    pass

print("\n--- Exercise 2 ---")
print("APIAccount class defined.")


# --- Exercise 3: The Load Balancer ---

class LoadBalancer:
    def __init__(self, accounts: List[APIAccount]):
        # TODO: Initialize with a list of accounts
        pass

    def get_healthy_account(self) -> Optional[APIAccount]:
        """
        Finds the next available healthy account using round-robin.
        """
        # TODO: Implement the round-robin health check logic
        pass

print("\n--- Exercise 3 ---")
print("LoadBalancer class defined.")


# --- Exercise 4: Resilient API Client ---

class ResilientClient:
    def __init__(self, accounts: List[APIAccount], requests_per_minute: int):
        # TODO: Initialize the load balancer and rate limiter
        pass

    def make_request(self, prompt: str):
        # TODO: Implement the resilient request logic with rate limiting and retries
        pass

print("\n--- Exercise 4 ---")
# TODO:
# 1. Create a list of dummy APIAccount objects.
# 2. Instantiate ResilientClient.
# 3. Call make_request multiple times to see the resilience features in action.

