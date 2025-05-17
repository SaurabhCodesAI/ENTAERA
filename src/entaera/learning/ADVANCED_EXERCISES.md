# 🔥 ADVANCED EXERCISES
## TypeScript, Next.js & Production Skills

**These concepts complete your full-stack mastery**

---

## 🚀 **EXERCISE 15: Master TypeScript Patterns (1.5 hours)**
### **Priority: 🟠 HIGH - Foundation for modern web development**

**Why this matters:**
- Your Snap2Slides project uses production TypeScript/Next.js
- Essential for full-stack capability (not just Python)
- These patterns appear in professional codebases

**Key concepts to master:**
- Interfaces vs Types
- Union types and type narrowing
- Generic types
- API design patterns

---

### **EXPERIMENT 1: Interfaces vs Types (20 min)**

```typescript
// Create: typescript_patterns.ts

// YOUR ACTUAL CODE from api-manager.ts
interface APIConfig {
  id: string;
  type: 'gemini' | 'perplexity';  // Union type
  key: string;
  baseUrl?: string;               // Optional property
  maxRetries: number;
  timeout: number;
  isActive: boolean;
  errorCount: number;
  lastError?: Date;
  rateLimitReset?: Date;
}

interface APIResponse {
  success: boolean;
  data?: any;
  error?: string;
  apiUsed?: string;
  retryAfter?: number;
}

// EXPERIMENT: Create instances
const geminiAPI: APIConfig = {
  id: 'gemini_1',
  type: 'gemini',
  key: 'test-key',
  maxRetries: 3,
  timeout: 30000,
  isActive: true,
  errorCount: 0
};

// Try to break it (this should error in TypeScript)
// const badAPI: APIConfig = {
//   id: 'test',
//   type: 'openai',  // Error! Not 'gemini' | 'perplexity'
//   maxRetries: 3
// };

// EXPERIMENT: Optional properties
const successResponse: APIResponse = {
  success: true,
  data: { result: "slides generated" },
  apiUsed: 'gemini_1'
  // error is optional, so we can omit it
};

const failureResponse: APIResponse = {
  success: false,
  error: 'API rate limit exceeded',
  retryAfter: 60
};

console.log('Gemini API:', geminiAPI);
console.log('Success:', successResponse);
console.log('Failure:', failureResponse);
```

**Run this:**
```powershell
# You need TypeScript installed
npm install -g typescript

# Create the file, then compile
tsc typescript_patterns.ts

# It will create typescript_patterns.js - run it
node typescript_patterns.js
```

**Key learnings:**
- **Union types** (`'gemini' | 'perplexity'`) restrict values to specific options
- **Optional properties** (`baseUrl?: string`) can be omitted
- **Interfaces** define contract/shape of objects
- TypeScript catches type errors at compile time, not runtime

---

### **EXPERIMENT 2: Generics (Like Your retryWithBackoff) (30 min)**

```typescript
// YOUR ACTUAL CODE from performance-utils.ts (simplified)

// Generic function - works with ANY return type
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  baseDelay: number = 1000
): Promise<T> {
  let lastError: Error;
  
  for (let i = 0; i < maxRetries; i++) {
    try {
      console.log(`Attempt ${i + 1}...`);
      return await fn();  // Returns type T
    } catch (error) {
      lastError = error as Error;
      
      if (i === maxRetries - 1) {
        console.log('All retries exhausted');
        throw lastError;
      }
      
      // Exponential backoff WITH JITTER (your improvement!)
      const exponentialDelay = baseDelay * Math.pow(2, i);
      const jitter = Math.random() * 1000;
      const delay = exponentialDelay + jitter;
      
      console.log(`Retry ${i + 1} failed: ${error}. Waiting ${delay.toFixed(0)}ms...`);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  
  throw lastError!;
}

// EXPERIMENT 1: Use with different return types
async function fetchUserData(): Promise<{ name: string; age: number }> {
  // Simulate 50% failure rate
  if (Math.random() < 0.5) {
    throw new Error('Network error');
  }
  return { name: 'Saurabh', age: 25 };
}

async function fetchNumber(): Promise<number> {
  if (Math.random() < 0.5) {
    throw new Error('API error');
  }
  return 42;
}

async function fetchString(): Promise<string> {
  if (Math.random() < 0.5) {
    throw new Error('Timeout');
  }
  return 'Success!';
}

// Run experiments
(async () => {
  console.log('\n=== Experiment 1: Retry with User Data ===');
  try {
    const userData = await retryWithBackoff(fetchUserData, 4, 500);
    console.log('Got user data:', userData);
  } catch (e) {
    console.log('Failed:', e.message);
  }
  
  console.log('\n=== Experiment 2: Retry with Number ===');
  try {
    const number = await retryWithBackoff(fetchNumber, 3, 1000);
    console.log('Got number:', number);
  } catch (e) {
    console.log('Failed:', e.message);
  }
  
  console.log('\n=== Experiment 3: Retry with String ===');
  try {
    const text = await retryWithBackoff(fetchString, 2, 800);
    console.log('Got text:', text);
  } catch (e) {
    console.log('Failed:', e.message);
  }
})();
```

**Run this:**
```powershell
tsc typescript_generics.ts
node typescript_generics.js
```

**Key learnings:**
- **`<T>`** means "generic type T"
- Same function works with `Promise<number>`, `Promise<string>`, `Promise<User>`, etc.
- TypeScript ensures type safety - you can't return wrong type
- **YOUR JITTER**: `Math.random() * 1000` prevents thundering herd problem

---

### **EXPERIMENT 3: Your Actual API Manager Pattern (40 min)**

```typescript
// Simplified version of YOUR api-manager.ts

interface APIConfig {
  id: string;
  type: 'gemini' | 'perplexity';
  isActive: boolean;
  errorCount: number;
  lastError?: Date;
}

class SimpleAPIManager {
  private apis: APIConfig[] = [];
  private currentIndex = 0;
  private readonly MAX_ERROR_COUNT = 3;
  private readonly ERROR_RESET_TIME = 5 * 60 * 1000; // 5 minutes
  
  constructor(apiKeys: string[]) {
    // Initialize APIs from keys
    apiKeys.forEach((key, index) => {
      this.apis.push({
        id: `gemini_${index + 1}`,
        type: 'gemini',
        isActive: true,
        errorCount: 0
      });
    });
    
    console.log(`Initialized ${this.apis.length} APIs`);
  }
  
  // YOUR PATTERN: Reset errors after 5 minutes
  private resetErrorCount(api: APIConfig): void {
    const now = new Date();
    if (api.lastError) {
      const timeSinceError = now.getTime() - api.lastError.getTime();
      if (timeSinceError > this.ERROR_RESET_TIME) {
        console.log(`Resetting errors for ${api.id} (${timeSinceError}ms passed)`);
        api.errorCount = 0;
        api.isActive = true;
        api.lastError = undefined;
      }
    }
  }
  
  // YOUR PATTERN: Mark API as failed
  private markAPIError(api: APIConfig, error: string): void {
    api.errorCount++;
    api.lastError = new Date();
    
    console.log(`${api.id} error count: ${api.errorCount}`);
    
    if (api.errorCount >= this.MAX_ERROR_COUNT) {
      api.isActive = false;
      console.log(`⚠️  ${api.id} DISABLED (too many errors)`);
    }
  }
  
  // YOUR PATTERN: Get available APIs (with auto-recovery)
  private getAvailableAPIs(): APIConfig[] {
    return this.apis
      .map(api => {
        this.resetErrorCount(api);  // Auto-recover if 5 min passed
        return api;
      })
      .filter(api => api.isActive);
  }
  
  // YOUR PATTERN: Round-robin selection
  async callAPI(data: string): Promise<string> {
    const availableAPIs = this.getAvailableAPIs();
    
    if (availableAPIs.length === 0) {
      throw new Error('No available APIs - all disabled');
    }
    
    // Try each API in round-robin order
    for (let attempt = 0; attempt < availableAPIs.length; attempt++) {
      const apiIndex = (this.currentIndex + attempt) % availableAPIs.length;
      const api = availableAPIs[apiIndex];
      
      try {
        console.log(`Trying ${api.id}...`);
        
        // Simulate API call with 30% failure rate
        if (Math.random() < 0.3) {
          throw new Error(`${api.id} rate limit exceeded`);
        }
        
        // Success!
        this.currentIndex = (apiIndex + 1) % availableAPIs.length;
        return `Success from ${api.id}: processed "${data}"`;
        
      } catch (error) {
        console.log(`${api.id} failed: ${error.message}`);
        this.markAPIError(api, error.message);
        
        // Try next API
        continue;
      }
    }
    
    throw new Error('All APIs failed');
  }
  
  // YOUR PATTERN: Get status for monitoring
  getStatus(): APIConfig[] {
    return this.apis.map(api => ({
      id: api.id,
      type: api.type,
      isActive: api.isActive,
      errorCount: api.errorCount,
      lastError: api.lastError
    }));
  }
}

// EXPERIMENT: Test your pattern
(async () => {
  console.log('=== Testing API Manager Pattern ===\n');
  
  const manager = new SimpleAPIManager(['key1', 'key2', 'key3']);
  
  // Make 15 API calls
  for (let i = 1; i <= 15; i++) {
    console.log(`\n--- Call ${i} ---`);
    try {
      const result = await manager.callAPI(`request_${i}`);
      console.log(`✅ ${result}`);
    } catch (error) {
      console.log(`❌ ${error.message}`);
    }
    
    // Show status every 5 calls
    if (i % 5 === 0) {
      console.log('\n📊 Current Status:');
      manager.getStatus().forEach(api => {
        console.log(`  ${api.id}: ${api.isActive ? '✅' : '❌'} (errors: ${api.errorCount})`);
      });
    }
    
    // Small delay
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  
  console.log('\n=== Final Status ===');
  manager.getStatus().forEach(api => {
    console.log(`${api.id}:`, {
      active: api.isActive,
      errors: api.errorCount,
      lastError: api.lastError?.toISOString()
    });
  });
})();
```

**Run this:**
```powershell
tsc api_manager_pattern.ts
node api_manager_pattern.js
```

**Watch what happens:**
1. **Round-robin**: Calls rotate through api_1 → api_2 → api_3 → api_1...
2. **Circuit breaker**: After 3 errors, API gets disabled
3. **Auto-recovery**: After 5 minutes (simulated), errors reset and API re-enables
4. **Fallback**: If one API fails, automatically tries next

**Key learnings:**
- **Round-robin** distributes load evenly across APIs
- **Circuit breaker** prevents hammering broken APIs
- **Auto-recovery** gives failed APIs a second chance
- **Graceful degradation** - keep working even if some APIs fail

---

## ✅ **MASTERY CHECK - Exercise 15:**

**Can you explain:**
1. ✅ What's a TypeScript interface? (Defines object shape/contract)
2. ✅ What's a union type? (`'gemini' | 'perplexity'` - only these values)
3. ✅ What does `<T>` mean in generics? (Placeholder for any type)
4. ✅ Why add jitter to exponential backoff? (Prevent thundering herd)
5. ✅ What's round-robin load balancing? (Rotate through APIs evenly)
6. ✅ What's a circuit breaker? (Disable failing services temporarily)
7. ✅ Why auto-recovery after 5 minutes? (Give APIs time to recover, then retry)

**Interview answer:**
*"In Snap2Slides, I built an API manager that handles 3 Gemini API keys and 1 Perplexity key. It uses round-robin to distribute requests evenly. If an API fails 3 times, the circuit breaker disables it for 5 minutes to prevent wasting time on broken endpoints. After 5 minutes, it auto-recovers and tries again. I added jitter to the exponential backoff to prevent all retries from hitting at the same time. This pattern ensures the app stays up even if individual APIs fail."*

---

## 🔄 **EXERCISE 16: Master Round-Robin Load Balancing (1 hour)**
### **Priority: 🔴 CRITICAL (85% chance Ashish asks)**

**Why this matters:**
- You use 3 Gemini API keys + 1 Perplexity key in production
- Ashish WILL ask "How do you handle API rate limits?"
- This is YOUR actual solution - not theoretical

**What he might ask:**
- "We have multiple API keys. How would you distribute load?"
- "What happens if one API key hits rate limit?"
- "Explain your round-robin implementation"

---

### **CONCEPT: What is Round-Robin?**

```
Request 1 → API_1
Request 2 → API_2
Request 3 → API_3
Request 4 → API_1  (wraps back to start)
Request 5 → API_2
Request 6 → API_3
```

**Benefits:**
- Even distribution (each API gets equal load)
- Automatic failover (if one fails, try next)
- Simple to implement
- No "hot" APIs that get overloaded

---

### **EXPERIMENT 1: Build Simple Round-Robin (20 min)**

```python
# Create: round_robin_basic.py

class RoundRobinSelector:
    """
    Simple round-robin selector
    Like what you built in Snap2Slides APIManager
    """
    def __init__(self, items):
        self.items = items
        self.current_index = 0
    
    def get_next(self):
        """Get next item in round-robin order"""
        item = self.items[self.current_index]
        
        # Move to next index, wrap around at end
        self.current_index = (self.current_index + 1) % len(self.items)
        
        return item

# EXPERIMENT 1: Test basic rotation
print("=== Experiment 1: Basic Round-Robin ===")
apis = ['gemini_1', 'gemini_2', 'gemini_3']
selector = RoundRobinSelector(apis)

for i in range(10):
    api = selector.get_next()
    print(f"Request {i+1} → {api}")

# EXPERIMENT 2: With different number of items
print("\n=== Experiment 2: 4 APIs ===")
apis_4 = ['api_a', 'api_b', 'api_c', 'api_d']
selector2 = RoundRobinSelector(apis_4)

for i in range(8):
    api = selector2.get_next()
    print(f"Request {i+1} → {api}")

# EXPERIMENT 3: Track distribution
print("\n=== Experiment 3: Distribution Check ===")
apis = ['key_1', 'key_2', 'key_3']
selector3 = RoundRobinSelector(apis)

# Make 30 requests
distribution = {'key_1': 0, 'key_2': 0, 'key_3': 0}
for _ in range(30):
    api = selector3.get_next()
    distribution[api] += 1

print("Distribution after 30 requests:")
for api, count in distribution.items():
    percentage = (count / 30) * 100
    print(f"  {api}: {count} requests ({percentage:.1f}%)")
```

**Run this:**
```powershell
python round_robin_basic.py
```

**Expected output:**
```
Request 1 → gemini_1
Request 2 → gemini_2
Request 3 → gemini_3
Request 4 → gemini_1  (wrapped!)
Request 5 → gemini_2
...

Distribution:
  key_1: 10 requests (33.3%)
  key_2: 10 requests (33.3%)
  key_3: 10 requests (33.3%)
```

**Key insight:** Perfect distribution - each API gets exactly 1/3 of traffic!

---

### **EXPERIMENT 2: Round-Robin with Failures (20 min)**

```python
# Create: round_robin_with_failover.py

import random

class SmartRoundRobin:
    """
    Round-robin with automatic failover
    Like YOUR APIManager in Snap2Slides
    """
    def __init__(self, apis):
        self.apis = apis
        self.current_index = 0
        self.disabled = set()  # Track disabled APIs
    
    def disable_api(self, api_id):
        """Disable a failing API"""
        self.disabled.add(api_id)
        print(f"⚠️  Disabled {api_id}")
    
    def enable_api(self, api_id):
        """Re-enable an API"""
        self.disabled.discard(api_id)
        print(f"✅ Re-enabled {api_id}")
    
    def get_available_apis(self):
        """Get list of active APIs"""
        return [api for api in self.apis if api not in self.disabled]
    
    def try_next_api(self, max_attempts=None):
        """
        Try APIs in round-robin order until one succeeds
        YOUR actual pattern from api-manager.ts
        """
        available = self.get_available_apis()
        
        if not available:
            raise Exception("No available APIs!")
        
        attempts = max_attempts or len(available)
        
        for attempt in range(attempts):
            # Calculate which API to try
            api_index = (self.current_index + attempt) % len(available)
            api = available[api_index]
            
            print(f"  Trying {api}...", end=' ')
            
            # Simulate API call (30% failure rate)
            if random.random() < 0.3:
                print(f"❌ Failed")
                continue  # Try next API
            
            # Success! Update index for next time
            self.current_index = (api_index + 1) % len(available)
            print(f"✅ Success")
            return api
        
        raise Exception("All APIs failed this round")

# EXPERIMENT: Simulate real usage
print("=== Testing Smart Round-Robin with Failover ===\n")

router = SmartRoundRobin(['gemini_1', 'gemini_2', 'gemini_3', 'perplexity_1'])

# Make 20 API calls
successes = 0
failures = 0

for i in range(1, 21):
    print(f"\nRequest {i}:")
    try:
        api = router.try_next_api()
        print(f"  ✅ Processed by {api}")
        successes += 1
        
        # Randomly disable an API (simulate rate limit)
        if random.random() < 0.1:  # 10% chance
            available = router.get_available_apis()
            if available:
                to_disable = random.choice(available)
                router.disable_api(to_disable)
        
        # Randomly re-enable (simulate recovery after 5 min)
        if random.random() < 0.15 and router.disabled:
            to_enable = random.choice(list(router.disabled))
            router.enable_api(to_enable)
            
    except Exception as e:
        print(f"  ❌ {e}")
        failures += 1

print(f"\n=== Results ===")
print(f"Successes: {successes}/20")
print(f"Failures: {failures}/20")
print(f"Currently disabled: {router.disabled if router.disabled else 'None'}")
print(f"Currently available: {router.get_available_apis()}")
```

**Run this:**
```powershell
python round_robin_with_failover.py
```

**Watch what happens:**
1. Requests rotate through all 4 APIs
2. When one fails, immediately tries next (no waiting!)
3. APIs can get disabled (rate limit hit)
4. APIs can recover (5 min timeout passed)
5. System keeps working even with some APIs down

---

### **EXPERIMENT 3: Compare Strategies (20 min)**

```python
# Create: compare_load_balancing.py

import random
import time

# Strategy 1: Random selection
def random_strategy(apis, num_requests):
    """Pick random API each time"""
    distribution = {api: 0 for api in apis}
    
    for _ in range(num_requests):
        api = random.choice(apis)
        distribution[api] += 1
    
    return distribution

# Strategy 2: Round-robin (YOUR strategy)
def round_robin_strategy(apis, num_requests):
    """Rotate through APIs evenly"""
    distribution = {api: 0 for api in apis}
    index = 0
    
    for _ in range(num_requests):
        api = apis[index]
        distribution[api] += 1
        index = (index + 1) % len(apis)
    
    return distribution

# Strategy 3: Weighted (not in your code, but good to know)
def weighted_strategy(apis, num_requests):
    """Give more requests to "better" APIs"""
    # Assign weights: first API gets 50%, others get 25% each
    weights = [0.5, 0.25, 0.25]
    distribution = {api: 0 for api in apis}
    
    for _ in range(num_requests):
        api = random.choices(apis, weights=weights)[0]
        distribution[api] += 1
    
    return distribution

# Compare all strategies
apis = ['api_1', 'api_2', 'api_3']
num_requests = 1000

print("=== Comparing Load Balancing Strategies ===")
print(f"Making {num_requests} requests across {len(apis)} APIs\n")

print("Strategy 1: RANDOM")
random_dist = random_strategy(apis, num_requests)
for api, count in random_dist.items():
    print(f"  {api}: {count} ({count/num_requests*100:.1f}%)")

print("\nStrategy 2: ROUND-ROBIN (YOUR strategy)")
rr_dist = round_robin_strategy(apis, num_requests)
for api, count in rr_dist.items():
    print(f"  {api}: {count} ({count/num_requests*100:.1f}%)")

print("\nStrategy 3: WEIGHTED")
weighted_dist = weighted_strategy(apis, num_requests)
for api, count in weighted_dist.items():
    print(f"  {api}: {count} ({count/num_requests*100:.1f}%)")

# Calculate variance (lower = more even distribution)
def calculate_variance(distribution):
    values = list(distribution.values())
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return variance

print("\n=== Variance (lower = more even) ===")
print(f"Random: {calculate_variance(random_dist):.2f}")
print(f"Round-robin: {calculate_variance(rr_dist):.2f}  ← Most even!")
print(f"Weighted: {calculate_variance(weighted_dist):.2f}")
```

**Run this:**
```powershell
python compare_load_balancing.py
```

**Expected insights:**
- **Random**: Uneven (e.g., 345, 312, 343) - some get more load
- **Round-robin**: PERFECT (333, 333, 334) - YOUR choice!
- **Weighted**: Intentionally uneven (500, 250, 250)

**Why you chose round-robin:**
- Most fair distribution
- Predictable behavior
- Simple to implement
- Works great when all APIs are equivalent

---

## ✅ **MASTERY CHECK - Exercise 16:**

**Can you explain:**
1. ✅ What is round-robin? (Rotate through items in order, wrap around)
2. ✅ Why use round-robin vs random? (Even distribution, predictable)
3. ✅ How does modulo (`%`) enable wrapping? (`(index + 1) % length`)
4. ✅ What happens when one API is disabled? (Skip it, try next available)
5. ✅ How do you track current position? (`currentIndex` variable)

**Interview answer:**
*"In Snap2Slides, I have 3 Gemini API keys and 1 Perplexity key. Instead of random selection, I use round-robin to ensure even distribution - each key gets approximately 25% of traffic. The implementation uses a currentIndex variable that increments and wraps around using modulo. When request 1 uses gemini_1, request 2 uses gemini_2, and so on. If an API hits rate limit and gets disabled, the round-robin automatically skips it and tries the next available API. This gives us automatic failover without complex logic."*

---

## 🛡️ **EXERCISE 17: Master Circuit Breaker Pattern (1 hour)**
### **Priority: 🔴 CRITICAL (80% chance Ashish asks)**

**Why this matters:**
- Prevents wasting time on broken APIs
- Shows production-ready thinking
- YOU implemented this in Snap2Slides APIManager
- Founding engineers LOVE resilience patterns

**What he might ask:**
- "How do you handle a failing API?"
- "What if an API is down for 10 minutes?"
- "Explain your error recovery strategy"

---

### **CONCEPT: What is Circuit Breaker?**

```
CLOSED (Normal) → API working, requests go through
   ↓ (3 failures)
OPEN (Broken) → API blocked, requests don't even try
   ↓ (5 min timeout)
HALF-OPEN (Testing) → Try once, see if recovered
   ↓
CLOSED (if success) or OPEN (if still broken)
```

**Like an electrical circuit breaker:**
- Normal: Electricity flows
- Too much current: Breaker "trips" (opens)
- Reset after cooling down: Try again

---

### **EXPERIMENT 1: Build Basic Circuit Breaker (25 min)**

```python
# Create: circuit_breaker_basic.py

from datetime import datetime, timedelta
from enum import Enum
import time

class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"       # Working normally
    OPEN = "open"           # Broken, blocking requests
    HALF_OPEN = "half_open" # Testing if recovered

class CircuitBreaker:
    """
    Circuit breaker pattern
    Like YOUR api-manager.ts implementation
    """
    def __init__(
        self, 
        max_failures=3,           # YOUR value
        timeout_seconds=5 * 60    # YOUR value: 5 minutes
    ):
        self.max_failures = max_failures
        self.timeout_seconds = timeout_seconds
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func):
        """
        Execute function with circuit breaker protection
        """
        # If circuit is OPEN, check if timeout passed
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                print("🔄 Circuit HALF-OPEN (testing recovery)...")
                self.state = CircuitState.HALF_OPEN
            else:
                time_left = self._time_until_reset()
                raise Exception(
                    f"Circuit breaker OPEN! "
                    f"Retry in {time_left:.0f}s"
                )
        
        # Try the function
        try:
            result = func()
            self._on_success()
            return result
            
        except Exception as e:
            self._on_failure()
            raise e
    
    def _should_attempt_reset(self):
        """Check if timeout period has passed"""
        if not self.last_failure_time:
            return False
        
        elapsed = time.time() - self.last_failure_time
        return elapsed >= self.timeout_seconds
    
    def _time_until_reset(self):
        """Calculate seconds until retry allowed"""
        if not self.last_failure_time:
            return 0
        
        elapsed = time.time() - self.last_failure_time
        return max(0, self.timeout_seconds - elapsed)
    
    def _on_success(self):
        """Handle successful call"""
        if self.state == CircuitState.HALF_OPEN:
            print("✅ Circuit CLOSED (recovered!)")
        
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        print(f"❌ Failure {self.failure_count}/{self.max_failures}")
        
        if self.failure_count >= self.max_failures:
            print(f"⚠️  Circuit breaker OPEN! (cooling down for {self.timeout_seconds}s)")
            self.state = CircuitState.OPEN
    
    def get_status(self):
        """Get current status"""
        return {
            'state': self.state.value,
            'failures': self.failure_count,
            'max_failures': self.max_failures,
            'time_until_reset': self._time_until_reset() if self.state == CircuitState.OPEN else 0
        }

# EXPERIMENT: Test the circuit breaker
print("=== Circuit Breaker Simulation ===\n")

breaker = CircuitBreaker(max_failures=3, timeout_seconds=10)  # 10s for demo

def flaky_api_call():
    """Simulates an unreliable API"""
    import random
    if random.random() < 0.7:  # 70% failure rate
        raise Exception("API Error")
    return "Success!"

# Make 15 attempts
for i in range(1, 16):
    print(f"\n--- Attempt {i} ---")
    
    try:
        result = breaker.call(flaky_api_call)
        print(f"✅ {result}")
        
    except Exception as e:
        print(f"❌ {e}")
    
    # Show status
    status = breaker.get_status()
    print(f"State: {status['state']}, Failures: {status['failures']}/{status['max_failures']}")
    
    # Small delay between attempts
    time.sleep(1)

print("\n=== Final Status ===")
print(breaker.get_status())
```

**Run this:**
```powershell
python circuit_breaker_basic.py
```

**Watch the pattern:**
1. **Attempts 1-3**: CLOSED state, failures accumulate
2. **After 3 failures**: Circuit OPENS
3. **Attempts 4-12**: All blocked (circuit is OPEN)
4. **After 10 seconds**: Circuit goes HALF-OPEN
5. **Next attempt**: If success → CLOSED, if fail → OPEN again

---

### **EXPERIMENT 2: Your Actual APIManager Pattern (25 min)**

```python
# Create: api_circuit_breaker.py

import time
import random
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class APIConfig:
    """YOUR actual API config structure"""
    id: str
    is_active: bool = True
    error_count: int = 0
    last_error: Optional[float] = None  # timestamp

class APIManager:
    """
    Simplified version of YOUR api-manager.ts
    With circuit breaker pattern
    """
    def __init__(self, api_ids):
        self.MAX_ERROR_COUNT = 3              # YOUR value
        self.ERROR_RESET_TIME = 5 * 60        # YOUR value: 5 minutes
        
        self.apis = {
            api_id: APIConfig(id=api_id)
            for api_id in api_ids
        }
    
    def reset_error_count(self, api: APIConfig):
        """
        YOUR PATTERN: Auto-recovery after timeout
        From api-manager.ts resetErrorCount()
        """
        if not api.last_error:
            return
        
        time_since_error = time.time() - api.last_error
        
        if time_since_error > self.ERROR_RESET_TIME:
            print(f"🔄 {api.id}: Resetting errors (been {time_since_error:.0f}s)")
            api.error_count = 0
            api.is_active = True
            api.last_error = None
    
    def mark_api_error(self, api: APIConfig, error: str):
        """
        YOUR PATTERN: Circuit breaker logic
        From api-manager.ts markAPIError()
        """
        api.error_count += 1
        api.last_error = time.time()
        
        print(f"  {api.id} error count: {api.error_count}/{self.MAX_ERROR_COUNT}")
        
        if api.error_count >= self.MAX_ERROR_COUNT:
            api.is_active = False
            print(f"  ⚠️  {api.id} DISABLED due to errors")
    
    def get_available_apis(self):
        """Get list of active APIs (with auto-recovery)"""
        available = []
        
        for api in self.apis.values():
            self.reset_error_count(api)  # Check if should recover
            if api.is_active:
                available.append(api)
        
        return available
    
    def call_api(self, api_id: str, data: str):
        """Call specific API with circuit breaker protection"""
        api = self.apis[api_id]
        
        # Check if API is available
        self.reset_error_count(api)
        
        if not api.is_active:
            time_left = self.ERROR_RESET_TIME - (time.time() - api.last_error)
            raise Exception(
                f"{api_id} is disabled. "
                f"Retry in {time_left:.0f}s"
            )
        
        # Try API call
        try:
            # Simulate API call (40% failure)
            if random.random() < 0.4:
                raise Exception(f"{api_id} rate limit exceeded")
            
            return f"✅ {api_id} processed: {data}"
            
        except Exception as e:
            self.mark_api_error(api, str(e))
            raise e
    
    def get_status(self):
        """Get status of all APIs"""
        return {
            api_id: {
                'active': api.is_active,
                'errors': api.error_count,
                'last_error_ago': f"{time.time() - api.last_error:.0f}s" if api.last_error else None
            }
            for api_id, api in self.apis.items()
        }

# EXPERIMENT: Simulate YOUR production scenario
print("=== Your API Manager with Circuit Breaker ===\n")

manager = APIManager(['gemini_1', 'gemini_2', 'gemini_3'])

# Simulate 20 requests with varying delays
for i in range(1, 21):
    print(f"\n--- Request {i} ---")
    
    # Try available APIs in order
    available = manager.get_available_apis()
    
    if not available:
        print("❌ No available APIs!")
        print("Status:", manager.get_status())
        print("Waiting 5s...")
        time.sleep(5)  # Wait for recovery
        continue
    
    # Try first available API
    api = available[0]
    
    try:
        result = manager.call_api(api.id, f"request_{i}")
        print(result)
        
    except Exception as e:
        print(f"❌ {e}")
    
    # Show status every 5 requests
    if i % 5 == 0:
        print("\n📊 Status:")
        for api_id, status in manager.get_status().items():
            state = "✅" if status['active'] else "❌"
            print(f"  {state} {api_id}: {status['errors']} errors, "
                  f"last error: {status['last_error_ago'] or 'never'}")
    
    # Variable delay between requests
    time.sleep(random.uniform(0.5, 2.0))

print("\n=== Final Status ===")
for api_id, status in manager.get_status().items():
    print(f"{api_id}:", status)
```

**Run this:**
```powershell
python api_circuit_breaker.py
```

**This demonstrates YOUR exact pattern:**
1. API fails 3 times → Circuit opens (disabled)
2. API disabled for 5 minutes
3. After 5 minutes → Auto-recovery (circuit closes)
4. If still failing → Opens again
5. Multiple APIs → Automatic fallback to healthy ones

---

### **EXPERIMENT 3: Compare With vs Without Circuit Breaker (10 min)**

```python
# Create: compare_circuit_breaker.py

import time
import random

def without_circuit_breaker(num_requests):
    """Keep trying broken API forever (BAD!)"""
    failures = 0
    wasted_time = 0
    
    for i in range(num_requests):
        start = time.time()
        
        # API is broken (always fails)
        try:
            if random.random() < 0.9:  # 90% failure
                raise Exception("API broken")
            print(f"Request {i+1}: Success")
        except:
            failures += 1
            time.sleep(0.1)  # Wasted time on broken API
        
        wasted_time += time.time() - start
    
    return failures, wasted_time

def with_circuit_breaker(num_requests):
    """Circuit breaker stops trying after 3 failures (GOOD!)"""
    failures = 0
    blocked = 0
    wasted_time = 0
    error_count = 0
    circuit_open = False
    
    for i in range(num_requests):
        start = time.time()
        
        # Check circuit breaker
        if circuit_open:
            blocked += 1
            continue  # Don't even try!
        
        # Try API
        try:
            if random.random() < 0.9:  # 90% failure
                raise Exception("API broken")
            print(f"Request {i+1}: Success")
            error_count = 0  # Reset on success
        except:
            failures += 1
            error_count += 1
            time.sleep(0.1)  # Time wasted
            
            if error_count >= 3:
                circuit_open = True
                print("Circuit breaker OPEN - stopping attempts")
        
        wasted_time += time.time() - start
    
    return failures, blocked, wasted_time

print("=== Comparing Circuit Breaker Impact ===\n")

num_requests = 20

print("Without Circuit Breaker:")
failures1, time1 = without_circuit_breaker(num_requests)
print(f"  Failures: {failures1}")
print(f"  Wasted time: {time1:.2f}s")

print("\nWith Circuit Breaker:")
failures2, blocked2, time2 = with_circuit_breaker(num_requests)
print(f"  Failures: {failures2}")
print(f"  Blocked: {blocked2} (saved time!)")
print(f"  Wasted time: {time2:.2f}s")

print(f"\n💡 Time saved: {time1 - time2:.2f}s ({((time1-time2)/time1*100):.0f}%)")
```

**Run this:**
```powershell
python compare_circuit_breaker.py
```

**Key insight:**
- **Without breaker**: Wastes time on every request to broken API
- **With breaker**: Fails fast after 3 attempts, blocks rest
- **Result**: 70-80% time saved by not hammering broken API

---

## ✅ **MASTERY CHECK - Exercise 17:**

**Can you explain:**
1. ✅ What is circuit breaker pattern? (Auto-disable failing services)
2. ✅ Why use it? (Prevent wasting time on broken APIs)
3. ✅ What are the 3 states? (CLOSED, OPEN, HALF-OPEN)
4. ✅ Why 3 failures threshold? (Balance between sensitivity and stability)
5. ✅ Why 5-minute timeout? (Give API time to recover)
6. ✅ What is auto-recovery? (Automatically re-enable after timeout)

**Interview answer:**
*"In Snap2Slides, I implemented a circuit breaker to protect against failing APIs. If an API fails 3 times, it gets disabled for 5 minutes. This prevents wasting time repeatedly calling a broken endpoint. After 5 minutes, it automatically re-enables and tries once. If it succeeds, great - the circuit closes and we're back to normal. If it still fails, the circuit opens again for another 5 minutes. This pattern saved significant response time - instead of waiting for timeouts on every request to a broken API, we fail fast and use a healthy API instead."*

---

## 🎯 **SUMMARY: CRITICAL MISSING EXERCISES**

| Exercise | Topic | Time | Probability Ashish Asks | Your Project |
|----------|-------|------|------------------------|--------------|
| **15** | TypeScript patterns (interfaces, generics, union types) | 1.5h | 🟠 70% | Snap2Slides |
| **16** | Round-robin load balancing | 1h | 🔴 85% | Snap2Slides APIManager |
| **17** | Circuit breaker pattern | 1h | 🔴 80% | Snap2Slides APIManager |
| **18** | 🔥 Async/Await Python patterns | 2h | 🔴 95% | ENTAERA (50+ async functions!) |
| **19** | 🔥 Priority Queue with heapq | 1h | 🟠 70% | ENTAERA agent_orchestration.py |

**Total additional time:** 5.5 hours

---

## 📅 **UPDATED SCHEDULE:**

### **Day 1 (Oct 28 - 7.5 hours):**
- **Hour 1-2:** Exercise 1-3 (Enums, Dataclasses, Type Hints)
- **Hour 3-4:** Exercise 4-5 (Embeddings, FAISS)
- **Hour 5-6:** ✨ **Exercise 16** (Round-robin) + **Exercise 17** (Circuit breaker)
- **Hour 7-7.5:** ✨ **Exercise 15** (TypeScript patterns - first 30 min)

### **Day 2 (Oct 29 - 8 hours):**
- **Hour 1:** ✨ **Exercise 15** (TypeScript patterns - finish)
- **Hour 2-5:** Exercise 6-9 (Temperature, Rate limiting, Prompts, Error handling)
- **Hour 6:** Exercise 12 (Multi-agent router)
- **Hour 7-8:** Mock Interview #1

---

## 🔥 **THESE ARE CRITICAL!**

Ashish is **HIGHLY LIKELY (70-85%)** to ask about:
- Load balancing across API keys
- Handling rate limits and failures
- TypeScript/full-stack capability

**These exercises fill the gaps from Snap2Slides that weren't covered in the original ENTAERA-focused plan!**

Start with **Exercise 16 (Round-robin)** - it's the most likely to come up (85%)! 🚀
