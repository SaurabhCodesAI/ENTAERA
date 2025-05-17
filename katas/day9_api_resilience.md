
# ENTAERA Kata - Day 9: API Resilience Engineering

## 🎯 Learning Objectives

Calling external APIs can be unreliable. They can be slow, return errors, or enforce strict usage limits. Today, you will learn how to build a resilient API client that can gracefully handle these challenges using rate limiting and load balancing.

- **Implement a token bucket algorithm for rate limiting.**
- **Design a system to manage and track usage across multiple API accounts.**
- **Build a load balancer that intelligently distributes requests to healthy accounts.**
- **Handle API errors and implement a retry mechanism with backoff.**
- **Understand the importance of resilience in distributed systems.**

---

## 🧠 For the Absolute Beginner

### What is Resilience?
Imagine you're driving and there's a traffic jam. A **resilient** driver has options: they can wait, try a different route, or turn around and try again later. A non-resilient driver just gets stuck. In software, **resilience** is the ability for our application to handle problems (like a slow or failing API) and continue to function, perhaps in a limited capacity, rather than just crashing.

### What are Rate Limiting and Load Balancing?
- **Rate Limiting**: This is like a ticket dispenser at a deli. It only gives out a certain number of tickets per minute to prevent the counter from getting overwhelmed. Our code needs to respect the "tickets per minute" limit set by the APIs we use.
- **Load Balancing**: If one deli counter is too busy, you open another one. Load balancing is the process of distributing requests across multiple resources (like different API accounts or servers) so that no single one gets overloaded.

---

## 📚 Theory & Links

Before you begin, study the implementations in:
- `src/entaera/utils/rate_limiter.py`
- `src/entaera/utils/multi_gemini_manager.py`

Key concepts to focus on:
- **Rate Limiting**: The practice of controlling the rate of requests sent to an API to prevent overloading the service and to stay within usage quotas.
- **Token Bucket Algorithm**: A common rate limiting algorithm. A bucket holds tokens, which are added at a fixed rate. A request consumes one or more tokens. If the bucket is empty, the request is delayed or rejected.
- **Load Balancing**: Distributing requests across multiple resources (in this case, API accounts) to optimize throughput, minimize response time, and avoid overloading any single resource.
- **Health Checks**: The process of monitoring the status of each resource (account) to ensure requests are not sent to failing ones.
- **Exponential Backoff**: A retry strategy where the delay between retries increases exponentially to avoid overwhelming a struggling service.

---

## � Project-Level Deep Dive: Advanced Concepts

### The Circuit Breaker Pattern
Our health check is a simple version of a powerful resilience pattern called the **Circuit Breaker**. A circuit breaker is a state machine that wraps a protected function call.
- It starts in a **Closed** state, and all calls pass through.
- If the calls start failing, it tracks the failures. After a certain threshold, it "trips" and moves to the **Open** state.
- In the Open state, all calls to the function fail immediately without even trying to execute it. This prevents the application from repeatedly trying to call a service that is known to be down.
- After a timeout period, the breaker moves to a **Half-Open** state. It allows a single "trial" request to pass through. If that call succeeds, the breaker moves back to Closed. If it fails, it goes back to Open.
This pattern prevents a failing service from cascading failures throughout a distributed system.

### Idempotency
When you implement retries, you might accidentally perform the same action multiple times. If the action is "get user data," that's fine. But if it's "charge credit card," that's a disaster. An **idempotent** operation is one that has the same result whether it's performed once or multiple times. When designing APIs, you can support idempotency by having the client generate a unique "idempotency key" for each transaction. The server then keeps track of these keys and can safely ignore a retried request if it has the same key as one it has already processed.

### Jitter
When a service comes back online after an outage, all the clients that were waiting will retry at the exact same time, creating a "thundering herd" that can immediately knock the service offline again. To prevent this, you add **jitter** (a small, random amount of time) to your retry delays. This spreads out the retry attempts, giving the service a chance to recover gracefully. A common strategy is "exponential backoff with jitter."

---

## �💻 Exercises

Create a new Python file named `katas/day9_practice.py` and complete the following exercises.

### Exercise 1: Simple Rate Limiter

1.  Create a class `RateLimiter`.
2.  In `__init__`, store `requests_per_minute`. Also, initialize a list or `deque` to store the timestamps of recent requests.
3.  Create a method `can_request(self) -> bool`.
4.  Inside this method, first, remove all timestamps from your list that are older than one minute ago.
5.  Then, check if the number of remaining timestamps is less than `requests_per_minute`. If so, return `True`.
6.  Create a method `record_request(self)`. This should add the current time to your list of timestamps.
7.  Test it by creating a `RateLimiter` with a limit of 5 requests per minute and trying to call it 10 times in a loop.

### Exercise 2: API Account Health

1.  Create a Pydantic `BaseModel` or a `dataclass` called `APIAccount`.
2.  It should have fields for `api_key: str`, `name: str`, and `is_healthy: bool = True`.
3.  Add a method `record_failure(self)` that sets `is_healthy` to `False`.
4.  Add a method `record_success(self)` that sets `is_healthy` to `True`.

### Exercise 3: The Load Balancer

1.  Create a class `LoadBalancer`.
2.  In `__init__`, it should accept a list of `APIAccount` objects.
3.  Create a method `get_healthy_account(self) -> APIAccount | None`.
4.  This method should iterate through the accounts and return the first one that is healthy. If none are healthy, it should return `None`. Use a simple round-robin approach: keep track of the last used index and start searching from the next one.

### Exercise 4: Resilient API Client

1.  Create a class `ResilientClient`.
2.  In `__init__`, it should instantiate your `LoadBalancer` with a few dummy `APIAccount`s and your `RateLimiter`.
3.  Create a method `make_request(self, prompt: str, retries: int = 3)`.
4.  This method should be the most complex piece:
    - First, check if `rate_limiter.can_request()` is `True`. If not, print a message and return.
    - Get a healthy account from the `load_balancer`. If none, print a message and return.
    - Record the request with the rate limiter.
    - **Simulate the API call**:
        - Use `random.random()` to sometimes "fail" the request.
        - If the call "succeeds," print which account was used and return the result.
        - If the call "fails," record the failure on the account (`account.record_failure()`) and `raise Exception("API call failed")`.
    - Wrap the simulation in a `try...except` block. If an exception occurs and you still have retries left, wait for a short period (e.g., `time.sleep(1)`) and try the whole process again.

---

## 🤔 Expanded Interview Prep Questions

### Beginner
1.  **Why is client-side rate limiting important? Why not just let the server reject your requests?**
    - *Answer Hint:* Being a "good citizen" of the internet is part of it. But more practically, if you repeatedly ignore a server's rate limits, your API key could be temporarily or permanently banned. Client-side limiting prevents this. It also reduces wasted effort; there's no point making a request you know will be rejected.
2.  **What are the trade-offs between different load balancing strategies (e.g., round-robin vs. least connections)?**
    - *Answer Hint:* **Round-robin** is simple and fair, but dumb. It doesn't account for the fact that some servers might be faster or less busy than others. **Least connections** is smarter; it sends new requests to the server with the fewest active connections, which is often a good proxy for the least busy server.

### Intermediate
3.  **Explain the "token bucket" algorithm. How is it different from a "leaky bucket"?**
    - *Answer Hint:* **Token Bucket** (what we used): You have a bucket of tokens. To make a request, you take a token. The bucket is refilled at a constant rate. This allows for *bursts* of traffic as long as there are tokens in the bucket. **Leaky Bucket**: Requests are added to a queue (the bucket). The bucket "leaks" requests at a constant rate. This smooths out traffic into a fixed-rate stream and does *not* allow for bursts.
4.  **What is a "circuit breaker" pattern, and how does it relate to the health checks we implemented?**
    - *Answer Hint:* A circuit breaker is a more formal and robust version of our health check. It automatically wraps a function call and tracks its failures. After a certain number of failures, it "trips" and stops any further calls to the failing service for a while, preventing a struggling system from being overwhelmed. Our manual `is_healthy` flag is a very basic implementation of this idea.
5.  **When implementing retries, why is it important to add a "jitter" (a small, random delay) to your backoff period?**
    - *Answer Hint:* To prevent a "thundering herd." If a service goes down and many clients are waiting to retry, they might all retry at the exact same time when their backoff period ends. This flood of requests can knock the service over again. Adding a random jitter spreads out the retries, giving the service a chance to recover.

### Advanced
6.  **What is a "cascading failure" in a distributed system, and how do patterns like circuit breakers and bulkheads help prevent it?**
    - *Answer Hint:* A cascading failure is when a failure in one component triggers a failure in another, which triggers another, and so on, leading to a total system outage. **Circuit breakers** prevent this by isolating the failing component and stopping the chain reaction. The **Bulkhead** pattern isolates different parts of the system from each other, like the watertight compartments in a ship. If one part fails, it doesn't take the whole system down with it. For example, you might have separate thread pools for calling two different services.
7.  **Your service needs to call an external API that is not idempotent. You are required to implement retries. How can you safely do this?**
    - *Answer Hint:* This is a very difficult problem. If the API can't be changed, you need to build an "idempotency layer" on your side. Before making the first call, you would: 1) Generate a unique transaction ID. 2) Save this ID in a database, marked as "in-progress." 3) Make the API call. 4) If it succeeds, update the status to "complete." If the call fails and you need to retry, you first check the database. If the status is "complete," you know the previous call actually succeeded, so you don't re-run it. This effectively adds idempotency to a non-idempotent service.
