# 🎯 DSA Problem Mapping: Kata Concepts → LeetCode/Codeforces

## 📋 Overview

**Total Problems: 200** (25 patterns × 8 problems each)
- 5 LeetCode + 3 Codeforces per pattern
- Difficulty: Easy → Medium → Hard progression
- Each problem mapped to BOTH:
  1. **Kata Concept** (what you learned in days 0-16)
  2. **DSA Pattern** (algorithmic approach)

**How to Use:**
1. 📖 Review the kata concept you learned
2. 🎯 Read why the problem uses that concept
3. 🚀 **GO SOLVE THE PROBLEM NOW** (click the link)
4. 🔁 Return and tackle the next problem

---

## 🔥 Pattern 1: Arrays & Hashing

### **Kata Connection: Day 0 (Python Fundamentals) + Day 15 (DSA)**
**Concepts Used:** List comprehensions, dict comprehensions, `enumerate()`, `zip()`, hashmap patterns

---

### ✅ Problem 1.1: Two Sum
- **LeetCode #1** - Two Sum (Easy)
- **Link:** https://leetcode.com/problems/two-sum/
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 0:** Uses `enumerate()` to track indices while iterating
- **Day 15:** HashMap pattern for O(1) lookup

**Why This Problem:**
```python
# You learned enumerate() in Day 0:
for i, num in enumerate(nums):  # ← You practiced this!
    complement = target - num
    if complement in seen:     # ← Dict lookup (Day 0 dict comprehensions)
        return [seen[complement], i]
```

**What You'll Practice:**
- Dictionary as hashmap (Day 0 concept)
- Index tracking with `enumerate()` (Day 0 concept)
- Complement pattern (classic array technique)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/two-sum/

---

### ✅ Problem 1.2: Group Anagrams
- **LeetCode #49** - Group Anagrams (Medium)
- **Link:** https://leetcode.com/problems/group-anagrams/
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 0:** Dict comprehensions for grouping
- **Day 1:** String manipulation and normalization

**Why This Problem:**
```python
# You learned dict comprehensions and string sorting in Day 0:
from collections import defaultdict
anagrams = defaultdict(list)
for word in strs:
    sorted_word = ''.join(sorted(word))  # ← String manipulation (Day 1)
    anagrams[sorted_word].append(word)   # ← Dict grouping (Day 0)
```

**What You'll Practice:**
- Dict comprehensions for grouping (Day 0 concept)
- String sorting and joining (Day 1 text processing)
- `defaultdict` usage (Day 15 DSA)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/group-anagrams/

---

### ✅ Problem 1.3: Top K Frequent Elements
- **LeetCode #347** - Top K Frequent Elements (Medium)
- **Link:** https://leetcode.com/problems/top-k-frequent-elements/
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 0:** `Counter` from collections, dict comprehensions
- **Day 15:** Heap data structure (priority queue)

**Why This Problem:**
```python
# You learned Counter and list comprehensions in Day 0:
from collections import Counter
freq = Counter(nums)  # ← Count frequencies (Day 0)
# Sort by frequency, take top k
return [num for num, count in freq.most_common(k)]  # ← List comp (Day 0)
```

**What You'll Practice:**
- `Counter` for frequency counting (Day 0 concept)
- List comprehensions for extracting results (Day 0 concept)
- Heap/priority queue optimization (Day 15 advanced)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/top-k-frequent-elements/

---

### ✅ Problem 1.4: Valid Sudoku
- **LeetCode #36** - Valid Sudoku (Medium)
- **Link:** https://leetcode.com/problems/valid-sudoku/
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 0:** Set comprehensions for duplicate detection
- **Day 15:** 2D array traversal

**Why This Problem:**
```python
# You learned set comprehensions and nested iteration in Day 0:
seen = set()
for i in range(9):
    for j in range(9):
        if board[i][j] != '.':
            # Check row, col, box using set membership (Day 0)
            if (i, board[i][j]) in seen:  # ← Set lookup (Day 0)
                return False
```

**What You'll Practice:**
- Set comprehensions for uniqueness (Day 0 concept)
- Nested list comprehensions (Day 0 concept)
- 2D matrix navigation (Day 15 DSA)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/valid-sudoku/

---

### ✅ Problem 1.5: Longest Consecutive Sequence
- **LeetCode #128** - Longest Consecutive Sequence (Medium)
- **Link:** https://leetcode.com/problems/longest-consecutive-sequence/
- **Difficulty:** ⭐⭐⭐ Hard (but accessible)

**🎯 Kata Concept Tie:**
- **Day 0:** Set operations for O(1) membership testing
- **Day 15:** Sequence building algorithm

**Why This Problem:**
```python
# You learned set operations in Day 0:
num_set = set(nums)  # ← Convert to set (Day 0)
longest = 0
for num in num_set:
    if num - 1 not in num_set:  # ← Set membership (Day 0)
        # Start of sequence
        current = num
        while current + 1 in num_set:  # ← Efficient lookup (Day 0)
            current += 1
```

**What You'll Practice:**
- Set creation and membership testing (Day 0 concept)
- While loops with conditions (Day 0 fundamentals)
- Sequence identification pattern (Day 15 DSA)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/longest-consecutive-sequence/

---

### ✅ Problem 1.6: Codeforces 4C - Registration System
- **Codeforces 4C** - Registration System (Easy)
- **Link:** https://codeforces.com/problemset/problem/4/C
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 0:** Dictionary for counting/tracking
- **Day 6:** Long-term memory storage pattern

**Why This Problem:**
```python
# You learned dict tracking patterns in Day 0:
usernames = {}
for name in input_names:
    if name not in usernames:  # ← Dict membership (Day 0)
        usernames[name] = 0
        print("OK")
    else:
        usernames[name] += 1  # ← Counter pattern (Day 0)
        print(f"{name}{usernames[name]}")
```

**What You'll Practice:**
- Dictionary as counter (Day 0 concept)
- String formatting (Day 1 text processing)
- Conditional logic (Day 0 fundamentals)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/4/C

---

### ✅ Problem 1.7: Codeforces 1579A - Casimir's String Solitaire
- **Codeforces 1579A** (Easy)
- **Link:** https://codeforces.com/problemset/problem/1579/A
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 0:** `Counter` from collections
- **Day 1:** Character frequency analysis

**Why This Problem:**
```python
# You learned Counter in Day 0:
from collections import Counter
freq = Counter(s)  # ← Count characters (Day 0)
# Check if freq['B'] == freq['A'] + freq['C']
return freq['B'] == freq.get('A', 0) + freq.get('C', 0)
```

**What You'll Practice:**
- `Counter` for character counting (Day 0 concept)
- Dict `.get()` method with defaults (Day 0 concept)
- Mathematical condition checking (Day 0 fundamentals)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/1579/A

---

### ✅ Problem 1.8: Codeforces 1722B - Colourblindness
- **Codeforces 1722B** (Easy)
- **Link:** https://codeforces.com/problemset/problem/1722/B
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 0:** `zip()` for parallel iteration
- **Day 1:** String comparison after normalization

**Why This Problem:**
```python
# You learned zip() in Day 0:
row1, row2 = input(), input()
# Normalize: treat R and G as same
def normalize(s):
    return s.replace('G', 'B').replace('R', 'B')  # ← String manipulation (Day 1)

# Compare character by character
for c1, c2 in zip(normalize(row1), normalize(row2)):  # ← zip() (Day 0)
    if c1 != c2:
        return False
```

**What You'll Practice:**
- `zip()` for parallel iteration (Day 0 concept)
- String replacement (Day 1 text processing)
- All/any patterns (Day 0 fundamentals)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/1722/B

---

## 🔥 Pattern 2: Two Pointers

### **Kata Connection: Day 15 (DSA Algorithms)**
**Concepts Used:** Array traversal, in-place modification, pointer manipulation

---

### ✅ Problem 2.1: Container With Most Water
- **LeetCode #11** - Container With Most Water (Medium)
- **Link:** https://leetcode.com/problems/container-with-most-water/
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 15:** Two pointers pattern (left/right approach)
- **Day 0:** `min()` and `max()` built-in functions

**Why This Problem:**
```python
# You learned two pointers in Day 15:
left, right = 0, len(height) - 1  # ← Two pointers initialization
max_area = 0
while left < right:
    width = right - left
    area = min(height[left], height[right]) * width  # ← min() (Day 0)
    max_area = max(max_area, area)  # ← max() (Day 0)
    # Move pointer with smaller height
    if height[left] < height[right]:
        left += 1
    else:
        right -= 1
```

**What You'll Practice:**
- Two pointers technique (Day 15 DSA)
- `min()`/`max()` usage (Day 0 fundamentals)
- Greedy pointer movement logic (Day 15 advanced)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/container-with-most-water/

---

### ✅ Problem 2.2: 3Sum
- **LeetCode #15** - 3Sum (Medium)
- **Link:** https://leetcode.com/problems/3sum/
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 15:** Two pointers + sorting
- **Day 0:** List comprehensions for deduplication

**Why This Problem:**
```python
# You learned sorting + two pointers in Day 15:
nums.sort()  # ← Sorting (Day 15)
result = []
for i in range(len(nums) - 2):
    if i > 0 and nums[i] == nums[i-1]:  # ← Skip duplicates
        continue
    left, right = i + 1, len(nums) - 1  # ← Two pointers
    while left < right:
        total = nums[i] + nums[left] + nums[right]
        if total == 0:
            result.append([nums[i], nums[left], nums[right]])
```

**What You'll Practice:**
- Sorting before two pointers (Day 15 DSA)
- Duplicate handling (Day 0 set concepts)
- Triple nested logic (Day 0 fundamentals)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/3sum/

---

### ✅ Problem 2.3: 3Sum Closest
- **LeetCode #16** - 3Sum Closest (Medium)
- **Link:** https://leetcode.com/problems/3sum-closest/
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 15:** Two pointers variant
- **Day 0:** `abs()` for distance calculation

**Why This Problem:**
```python
# Similar to 3Sum but tracking closest:
nums.sort()
closest = float('inf')
for i in range(len(nums) - 2):
    left, right = i + 1, len(nums) - 1
    while left < right:
        total = nums[i] + nums[left] + nums[right]
        if abs(total - target) < abs(closest - target):  # ← abs() (Day 0)
            closest = total
```

**What You'll Practice:**
- Two pointers variation (Day 15 DSA)
- `abs()` for distance (Day 0 fundamentals)
- Tracking optimal solution (Day 15 optimization)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/3sum-closest/

---

### ✅ Problem 2.4: Valid Palindrome
- **LeetCode #125** - Valid Palindrome (Easy)
- **Link:** https://leetcode.com/problems/valid-palindrome/
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 1:** Text normalization (remove special chars)
- **Day 15:** Two pointers for palindrome check

**Why This Problem:**
```python
# You learned text cleaning in Day 1:
# Normalize: remove non-alphanumeric, lowercase
s = ''.join(c.lower() for c in s if c.isalnum())  # ← List comp (Day 0) + text cleaning (Day 1)

# Two pointers check (Day 15):
left, right = 0, len(s) - 1
while left < right:
    if s[left] != s[right]:
        return False
    left += 1
    right -= 1
```

**What You'll Practice:**
- Text normalization (Day 1 concept)
- List comprehensions with filter (Day 0 concept)
- Two pointers palindrome (Day 15 DSA)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/valid-palindrome/

---

### ✅ Problem 2.5: Is Subsequence
- **LeetCode #392** - Is Subsequence (Easy)
- **Link:** https://leetcode.com/problems/is-subsequence/
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 15:** Two pointers for sequence matching
- **Day 1:** Character-by-character comparison

**Why This Problem:**
```python
# You learned two pointers in Day 15:
i, j = 0, 0  # ← Two pointers (different arrays)
while i < len(s) and j < len(t):
    if s[i] == t[j]:  # ← Character match (Day 1)
        i += 1
    j += 1
return i == len(s)  # ← All characters found
```

**What You'll Practice:**
- Two pointers on different arrays (Day 15 DSA)
- Character comparison (Day 1 text processing)
- Subsequence vs substring (Day 15 concept)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/is-subsequence/

---

### ✅ Problem 2.6: Codeforces 6A - Triangle
- **Codeforces 6A** - Triangle (Easy)
- **Link:** https://codeforces.com/problemset/problem/6/A
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 0:** List operations and combinations
- **Day 15:** Brute force with conditions

**Why This Problem:**
```python
# You learned list comprehensions in Day 0:
from itertools import combinations
sides = [int(x) for x in input().split()]  # ← List comp (Day 0)
# Check all triplets
for a, b, c in combinations(sides, 3):  # ← combinations (Day 0 advanced)
    if a + b > c and a + c > b and b + c > a:  # ← Triangle inequality
        return "TRIANGLE"
```

**What You'll Practice:**
- List comprehensions (Day 0 concept)
- `itertools.combinations` (Day 0 advanced)
- Mathematical conditions (Day 15 logic)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/6/A

---

### ✅ Problem 2.7: Codeforces 1538A - Stone Game
- **Codeforces 1538A** (Easy)
- **Link:** https://codeforces.com/problemset/problem/1538/A
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 0:** `min()`, `max()`, `enumerate()` for finding indices
- **Day 15:** Greedy choice between endpoints

**Why This Problem:**
```python
# You learned enumerate() and min/max in Day 0:
stones = [int(x) for x in input().split()]
min_val = min(stones)
max_val = max(stones)
min_idx = stones.index(min_val)  # ← Find index (Day 0)
max_idx = stones.index(max_val)
# Calculate moves from either end
```

**What You'll Practice:**
- `enumerate()` for index finding (Day 0 concept)
- `min()`/`max()` operations (Day 0 fundamentals)
- Distance calculation (Day 15 math)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/1538/A

---

### ✅ Problem 2.8: Codeforces 1552A - Subsequence Permutation
- **Codeforces 1552A** (Easy)
- **Link:** https://codeforces.com/problemset/problem/1552/A
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 0:** Sorting and comparison
- **Day 1:** String character operations

**Why This Problem:**
```python
# You learned sorting in Day 0:
s = input()
sorted_s = ''.join(sorted(s))  # ← Sort string (Day 0)
# Count differences
count = sum(1 for c1, c2 in zip(s, sorted_s) if c1 != c2)  # ← zip() (Day 0)
print(count)
```

**What You'll Practice:**
- Sorting strings (Day 0 concept)
- `zip()` for parallel iteration (Day 0 concept)
- List comprehension with sum (Day 0 fundamentals)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/1552/A

---

## 🔥 Pattern 3: Sliding Window

### **Kata Connection: Day 7 (Context Management) + Day 15 (DSA)**
**Concepts Used:** Window maintenance, deque, substring tracking

---

### ✅ Problem 3.1: Longest Substring Without Repeating Characters
- **LeetCode #3** - Longest Substring Without Repeating Characters (Medium)
- **Link:** https://leetcode.com/problems/longest-substring-without-repeating-characters/
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 7:** Context window management (sliding window of tokens)
- **Day 15:** Sliding window pattern
- **Day 0:** Set for duplicate detection

**Why This Problem:**
```python
# You learned context windows in Day 7:
seen = {}  # ← Track characters in window (Day 0 dict)
left = 0
max_len = 0
for right, char in enumerate(s):  # ← enumerate() (Day 0)
    if char in seen and seen[char] >= left:  # ← Window membership
        left = seen[char] + 1  # ← Shrink window (Day 7 concept)
    seen[char] = right
    max_len = max(max_len, right - left + 1)
```

**What You'll Practice:**
- Sliding window concept (Day 7 context management)
- Dictionary for tracking (Day 0 concept)
- Window expansion/contraction (Day 15 DSA)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/longest-substring-without-repeating-characters/

---

### ✅ Problem 3.2: Longest Repeating Character Replacement
- **LeetCode #424** - Longest Repeating Character Replacement (Medium)
- **Link:** https://leetcode.com/problems/longest-repeating-character-replacement/
- **Difficulty:** ⭐⭐⭐ Medium-Hard

**🎯 Kata Concept Tie:**
- **Day 7:** Context window with token budget (k replacements = token budget)
- **Day 0:** `Counter` for frequency tracking

**Why This Problem:**
```python
# Similar to Day 7 context window with capacity:
from collections import Counter
count = Counter()  # ← Track frequencies (Day 0)
left = 0
max_len = 0
for right in range(len(s)):
    count[s[right]] += 1
    # Window size - most frequent char <= k (can replace others)
    while (right - left + 1) - max(count.values()) > k:  # ← Budget constraint (Day 7)
        count[s[left]] -= 1
        left += 1
```

**What You'll Practice:**
- Sliding window with constraints (Day 7 concept)
- `Counter` operations (Day 0 concept)
- Budget/capacity management (Day 7 token limits)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/longest-repeating-character-replacement/

---

### ✅ Problem 3.3: Permutation in String
- **LeetCode #567** - Permutation in String (Medium)
- **Link:** https://leetcode.com/problems/permutation-in-string/
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 1:** Anagram detection (string character frequency)
- **Day 15:** Fixed-size sliding window

**Why This Problem:**
```python
# You learned character frequency in Day 1:
from collections import Counter
s1_count = Counter(s1)  # ← Frequency map (Day 0)
window_count = Counter()
# Sliding window of len(s1)
for i in range(len(s2)):
    window_count[s2[i]] += 1
    if i >= len(s1):  # ← Maintain fixed window size (Day 7)
        if window_count[s2[i - len(s1)]] == 1:
            del window_count[s2[i - len(s1)]]
        else:
            window_count[s2[i - len(s1)]] -= 1
    if window_count == s1_count:  # ← Dict comparison (Day 0)
        return True
```

**What You'll Practice:**
- Fixed-size sliding window (Day 7 concept)
- `Counter` comparison (Day 0 concept)
- Anagram detection (Day 1 text processing)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/permutation-in-string/

---

### ✅ Problem 3.4: Minimum Window Substring
- **LeetCode #76** - Minimum Window Substring (Hard)
- **Link:** https://leetcode.com/problems/minimum-window-substring/
- **Difficulty:** ⭐⭐⭐⭐ Hard

**🎯 Kata Concept Tie:**
- **Day 7:** Dynamic window sizing (context management)
- **Day 0:** Dict for character counting

**Why This Problem:**
```python
# Advanced version of Day 7 context window:
from collections import Counter
need = Counter(t)  # ← Characters needed (Day 0)
have = {}  # ← Characters in current window
formed = 0  # ← How many characters satisfied
# Expand window to satisfy need, shrink to minimize
left = 0
for right in range(len(s)):
    # Expand window (Day 7 concept)
    have[s[right]] = have.get(s[right], 0) + 1
    if s[right] in need and have[s[right]] == need[s[right]]:
        formed += 1
    # Shrink window while valid (Day 7 optimization)
    while formed == len(need):
        # Update result, shrink
```

**What You'll Practice:**
- Dynamic window resizing (Day 7 concept)
- Dictionary operations (Day 0 concept)
- Optimization problem (Day 15 DSA)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/minimum-window-substring/

---

### ✅ Problem 3.5: Minimum Size Subarray Sum
- **LeetCode #209** - Minimum Size Subarray Sum (Medium)
- **Link:** https://leetcode.com/problems/minimum-size-subarray-sum/
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 7:** Context window with capacity constraint (sum >= target)
- **Day 0:** Running sum calculation

**Why This Problem:**
```python
# Similar to Day 7 managing context with token budget:
left = 0
current_sum = 0
min_len = float('inf')
for right in range(len(nums)):
    current_sum += nums[right]  # ← Running sum (Day 0)
    # Shrink window while condition met (Day 7)
    while current_sum >= target:
        min_len = min(min_len, right - left + 1)
        current_sum -= nums[left]
        left += 1
```

**What You'll Practice:**
- Variable-size sliding window (Day 7 concept)
- Running sum maintenance (Day 0 fundamentals)
- Window optimization (Day 15 DSA)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/minimum-size-subarray-sum/

---

### ✅ Problem 3.6: Codeforces 279B - Books
- **Codeforces 279B** - Books (Medium)
- **Link:** https://codeforces.com/problemset/problem/279/B
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 7:** Time-bounded context window (t minutes = token budget)
- **Day 0:** List operations

**Why This Problem:**
```python
# Exactly like Day 7 context window with time budget:
left = 0
current_time = 0
max_books = 0
for right in range(len(times)):
    current_time += times[right]  # ← Add to window (Day 7)
    # Shrink while over budget (Day 7 concept)
    while current_time > t:
        current_time -= times[left]
        left += 1
    max_books = max(max_books, right - left + 1)
```

**What You'll Practice:**
- Sliding window with time budget (Day 7 exact concept)
- Window size tracking (Day 7 context length)
- Greedy window expansion (Day 15 DSA)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/279/B

---

### ✅ Problem 3.7: Codeforces 363B - Fence
- **Codeforces 363B** - Fence (Medium)
- **Link:** https://codeforces.com/problemset/problem/363/B
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 15:** Fixed-size sliding window (k consecutive planks)
- **Day 0:** Min tracking

**Why This Problem:**
```python
# Fixed window of k elements (Day 7 fixed context):
# Initial window sum
window_sum = sum(heights[:k])  # ← Sum first k (Day 0)
min_sum = window_sum
min_idx = 0
# Slide window
for i in range(k, len(heights)):
    window_sum += heights[i] - heights[i - k]  # ← Slide (Day 7)
    if window_sum < min_sum:
        min_sum = window_sum
        min_idx = i - k + 1
```

**What You'll Practice:**
- Fixed-size sliding window (Day 7 concept)
- Window sum maintenance (Day 0 fundamentals)
- Index tracking (Day 0 enumerate)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/363/B

---

### ✅ Problem 3.8: Codeforces 165A - Supercentral Point
- **Codeforces 165A** (Easy)
- **Link:** https://codeforces.com/problemset/problem/165/A
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 0:** List comprehensions for filtering
- **Day 4:** Data validation (checking all conditions)

**Why This Problem:**
```python
# You learned list comprehensions with conditions in Day 0:
points = [(x, y) for _ in range(n)]  # ← List comp (Day 0)
count = 0
for px, py in points:
    # Check if supercentral (has point in all 4 directions)
    has_up = any(x == px and y > py for x, y in points)  # ← any() (Day 0)
    has_down = any(x == px and y < py for x, y in points)
    has_left = any(x < px and y == py for x, y in points)
    has_right = any(x > px and y == py for x, y in points)
    if has_up and has_down and has_left and has_right:
        count += 1
```

**What You'll Practice:**
- List comprehensions (Day 0 concept)
- `any()` with generator expressions (Day 0 concept)
- Multi-condition validation (Day 4 data modeling)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/165/A

---

## 🔥 Pattern 4: Binary Search

### **Kata Connection: Day 15 (DSA Algorithms)**
**Concepts Used:** Sorted array search, divide and conquer, logarithmic complexity

---

### ✅ Problem 4.1: Binary Search
- **LeetCode #704** - Binary Search (Easy)
- **Link:** https://leetcode.com/problems/binary-search/
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 15:** Classic binary search template
- **Day 0:** Integer division `//`

**Why This Problem:**
```python
# You learned binary search in Day 15:
left, right = 0, len(nums) - 1
while left <= right:
    mid = (left + right) // 2  # ← Integer division (Day 0)
    if nums[mid] == target:
        return mid
    elif nums[mid] < target:
        left = mid + 1  # ← Search right half
    else:
        right = mid - 1  # ← Search left half
return -1
```

**What You'll Practice:**
- Binary search template (Day 15 DSA)
- Integer division (Day 0 fundamentals)
- Logarithmic complexity O(log n) (Day 15 concept)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/binary-search/

---

### ✅ Problem 4.2: Search in Rotated Sorted Array
- **LeetCode #33** - Search in Rotated Sorted Array (Medium)
- **Link:** https://leetcode.com/problems/search-in-rotated-sorted-array/
- **Difficulty:** ⭐⭐⭐ Medium-Hard

**🎯 Kata Concept Tie:**
- **Day 15:** Modified binary search
- **Day 0:** Conditional logic with multiple branches

**Why This Problem:**
```python
# Advanced binary search from Day 15:
left, right = 0, len(nums) - 1
while left <= right:
    mid = (left + right) // 2
    if nums[mid] == target:
        return mid
    # Determine which half is sorted
    if nums[left] <= nums[mid]:  # ← Left half sorted (Day 0 comparison)
        if nums[left] <= target < nums[mid]:
            right = mid - 1
        else:
            left = mid + 1
    else:  # Right half sorted
        if nums[mid] < target <= nums[right]:
            left = mid + 1
        else:
            right = mid - 1
```

**What You'll Practice:**
- Binary search variation (Day 15 DSA)
- Complex conditional logic (Day 0 fundamentals)
- Rotation handling (Day 15 advanced)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/search-in-rotated-sorted-array/

---

### ✅ Problem 4.3: Find Minimum in Rotated Sorted Array
- **LeetCode #153** - Find Minimum in Rotated Sorted Array (Medium)
- **Link:** https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 15:** Binary search on rotated array
- **Day 0:** Comparison operators

**Why This Problem:**
```python
# Binary search variant from Day 15:
left, right = 0, len(nums) - 1
while left < right:
    mid = (left + right) // 2
    if nums[mid] > nums[right]:  # ← Min in right half
        left = mid + 1
    else:  # Min in left half (including mid)
        right = mid
return nums[left]
```

**What You'll Practice:**
- Binary search for minimum (Day 15 DSA)
- Comparison logic (Day 0 fundamentals)
- Edge case handling (Day 15 concepts)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/

---

### ✅ Problem 4.4: Find First and Last Position
- **LeetCode #34** - Find First and Last Position (Medium)
- **Link:** https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 15:** Binary search for boundaries
- **Day 0:** Function composition (two searches)

**Why This Problem:**
```python
# You learned to write reusable functions in Day 0:
def find_bound(nums, target, find_left):  # ← Function with flag (Day 0)
    left, right = 0, len(nums) - 1
    bound = -1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            bound = mid  # ← Track bound
            if find_left:
                right = mid - 1  # ← Search left for first
            else:
                left = mid + 1   # ← Search right for last
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return bound

# Use function twice
return [find_bound(nums, target, True), find_bound(nums, target, False)]
```

**What You'll Practice:**
- Binary search variations (Day 15 DSA)
- Function parameters (Day 0 fundamentals)
- Boundary finding (Day 15 advanced)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/

---

### ✅ Problem 4.5: Median of Two Sorted Arrays
- **LeetCode #4** - Median of Two Sorted Arrays (Hard)
- **Link:** https://leetcode.com/problems/median-of-two-sorted-arrays/
- **Difficulty:** ⭐⭐⭐⭐⭐ Hard

**🎯 Kata Concept Tie:**
- **Day 15:** Advanced binary search (partition)
- **Day 0:** Math operations (median calculation)

**Why This Problem:**
```python
# Advanced binary search from Day 15:
# Ensure nums1 is smaller
if len(nums1) > len(nums2):
    nums1, nums2 = nums2, nums1  # ← Tuple unpacking (Day 0)
# Binary search on nums1 to find partition
left, right = 0, len(nums1)
while left <= right:
    partition1 = (left + right) // 2
    partition2 = (len(nums1) + len(nums2) + 1) // 2 - partition1
    # Complex partition logic...
```

**What You'll Practice:**
- Advanced binary search (Day 15 DSA)
- Tuple unpacking (Day 0 concept)
- Mathematical reasoning (Day 15 hard problems)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/median-of-two-sorted-arrays/

---

### ✅ Problem 4.6: Codeforces 706B - Interesting Drink
- **Codeforces 706B** (Easy)
- **Link:** https://codeforces.com/problemset/problem/706/B
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 15:** Binary search for counting
- **Day 0:** `bisect` module

**Why This Problem:**
```python
# You can use Python's bisect (Day 0 libraries):
import bisect
prices = [int(x) for x in input().split()]  # ← List comp (Day 0)
prices.sort()  # ← Sort for binary search (Day 15)
for _ in range(q):
    coin = int(input())
    # Count shops with price <= coin
    count = bisect.bisect_right(prices, coin)  # ← Binary search (Day 15)
    print(count)
```

**What You'll Practice:**
- `bisect` module (Day 0 standard library)
- Sorted array search (Day 15 DSA)
- Counting with binary search (Day 15 technique)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/706/B

---

### ✅ Problem 4.7: Codeforces 1605B - Reverse Sort
- **Codeforces 1605B** (Medium)
- **Link:** https://codeforces.com/problemset/problem/1605/B
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 0:** Sorting and string manipulation
- **Day 1:** Character analysis

**Why This Problem:**
```python
# You learned sorting in Day 0:
s = input()
sorted_s = ''.join(sorted(s))  # ← Sort string (Day 0)
if s == sorted_s:
    print(0)  # Already sorted
else:
    # Find positions where s[i] != sorted_s[i]
    positions = [i + 1 for i, (c1, c2) in enumerate(zip(s, sorted_s)) if c1 != c2]
    print(1)  # One operation
    print(len(positions))
    print(*positions)
```

**What You'll Practice:**
- String sorting (Day 0 concept)
- List comprehensions with conditions (Day 0 concept)
- `enumerate()` and `zip()` (Day 0 fundamentals)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/1605/B

---

### ✅ Problem 4.8: Codeforces 236A - Boy or Girl
- **Codeforces 236A** (Easy)
- **Link:** https://codeforces.com/problemset/problem/236/A
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 0:** Set for unique characters
- **Day 1:** String character analysis

**Why This Problem:**
```python
# You learned set operations in Day 0:
username = input()
unique_chars = set(username)  # ← Create set (Day 0)
if len(unique_chars) % 2 == 0:  # ← Even/odd check (Day 0)
    print("CHAT WITH HER!")
else:
    print("IGNORE HIM!")
```

**What You'll Practice:**
- Set creation (Day 0 concept)
- Length and modulo (Day 0 fundamentals)
- String to set conversion (Day 0 concept)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/236/A

---

## 🔥 Pattern 5: Prefix Sum

### **Kata Connection: Day 0 (Python Fundamentals) + Day 15 (DSA)**
**Concepts Used:** Cumulative sums, range queries, optimization

---

### ✅ Problem 5.1: Subarray Sum Equals K
- **LeetCode #560** - Subarray Sum Equals K (Medium)
- **Link:** https://leetcode.com/problems/subarray-sum-equals-k/
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 15:** Prefix sum with hashmap
- **Day 0:** Dictionary for counting occurrences

**Why This Problem:**
```python
# You learned dict tracking in Day 0:
from collections import defaultdict
prefix_sum = 0
sum_count = defaultdict(int)  # ← Dict for counting (Day 0)
sum_count[0] = 1  # ← Base case
count = 0
for num in nums:
    prefix_sum += num  # ← Running sum (Day 0)
    # Check if (prefix_sum - k) exists
    if (prefix_sum - k) in sum_count:  # ← Dict lookup (Day 0)
        count += sum_count[prefix_sum - k]
    sum_count[prefix_sum] += 1
```

**What You'll Practice:**
- Prefix sum concept (Day 15 DSA)
- Dictionary as counter (Day 0 concept)
- Complement pattern (similar to Two Sum)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/subarray-sum-equals-k/

---

### ✅ Problem 5.2: Product of Array Except Self
- **LeetCode #238** - Product of Array Except Self (Medium)
- **Link:** https://leetcode.com/problems/product-of-array-except-self/
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 15:** Prefix product pattern
- **Day 0:** List comprehensions for array building

**Why This Problem:**
```python
# You learned list operations in Day 0:
n = len(nums)
result = [1] * n  # ← Initialize list (Day 0)
# Left products
left_product = 1
for i in range(n):
    result[i] = left_product  # ← Accumulate from left
    left_product *= nums[i]
# Right products
right_product = 1
for i in range(n - 1, -1, -1):  # ← Reverse iteration (Day 0)
    result[i] *= right_product  # ← Multiply from right
    right_product *= nums[i]
```

**What You'll Practice:**
- Prefix/suffix products (Day 15 DSA)
- List initialization (Day 0 concept)
- Reverse iteration (Day 0 fundamentals)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/product-of-array-except-self/

---

### ✅ Problem 5.3: Range Sum Query - Immutable
- **LeetCode #303** - Range Sum Query (Easy)
- **Link:** https://leetcode.com/problems/range-sum-query-immutable/
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 15:** Classic prefix sum
- **Day 0:** List operations

**Why This Problem:**
```python
# You learned list operations in Day 0:
class NumArray:
    def __init__(self, nums):
        self.prefix = [0]  # ← Initialize (Day 0)
        for num in nums:
            self.prefix.append(self.prefix[-1] + num)  # ← Cumulative sum (Day 0)
    
    def sumRange(self, left, right):
        # O(1) range sum
        return self.prefix[right + 1] - self.prefix[left]  # ← Array slicing math
```

**What You'll Practice:**
- Prefix sum array (Day 15 DSA)
- List append operations (Day 0 concept)
- Array indexing (Day 0 fundamentals)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/range-sum-query-immutable/

---

### ✅ Problem 5.4: Contiguous Array
- **LeetCode #525** - Contiguous Array (Medium)
- **Link:** https://leetcode.com/problems/contiguous-array/
- **Difficulty:** ⭐⭐⭐ Medium-Hard

**🎯 Kata Concept Tie:**
- **Day 15:** Prefix sum with transformation
- **Day 0:** Dictionary for index tracking

**Why This Problem:**
```python
# Convert 0 to -1, then find subarray with sum 0
sum_index = {0: -1}  # ← Dict for tracking (Day 0)
max_len = 0
current_sum = 0
for i, num in enumerate(nums):  # ← enumerate() (Day 0)
    current_sum += 1 if num == 1 else -1  # ← Ternary operator (Day 0)
    if current_sum in sum_index:  # ← Dict lookup (Day 0)
        max_len = max(max_len, i - sum_index[current_sum])
    else:
        sum_index[current_sum] = i
```

**What You'll Practice:**
- Prefix sum variation (Day 15 DSA)
- Dictionary for indices (Day 0 concept)
- Ternary operators (Day 0 fundamentals)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/contiguous-array/

---

### ✅ Problem 5.5: Maximum Product Subarray
- **LeetCode #152** - Maximum Product Subarray (Medium)
- **Link:** https://leetcode.com/problems/maximum-product-subarray/
- **Difficulty:** ⭐⭐⭐ Medium-Hard

**🎯 Kata Concept Tie:**
- **Day 15:** Dynamic programming (prefix product)
- **Day 0:** Min/max tracking

**Why This Problem:**
```python
# Track both max and min (negative numbers flip)
max_prod = min_prod = result = nums[0]
for num in nums[1:]:  # ← List slicing (Day 0)
    # Negative flips max/min
    if num < 0:
        max_prod, min_prod = min_prod, max_prod  # ← Tuple swap (Day 0)
    max_prod = max(num, max_prod * num)  # ← max() (Day 0)
    min_prod = min(num, min_prod * num)
    result = max(result, max_prod)
```

**What You'll Practice:**
- Prefix product concept (Day 15 DSA)
- Tuple unpacking for swaps (Day 0 concept)
- Min/max operations (Day 0 fundamentals)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/maximum-product-subarray/

---

### ✅ Problem 5.6: Codeforces 363B - Fence (Revisit)
- **Codeforces 363B** - Fence (Medium)
- **Link:** https://codeforces.com/problemset/problem/363/B
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 15:** Prefix sum for range queries
- **Day 7:** Fixed window (alternative approach to sliding window)

**Why This Problem:**
```python
# Can use prefix sums instead of sliding window:
heights = [int(x) for x in input().split()]  # ← List comp (Day 0)
prefix = [0]
for h in heights:
    prefix.append(prefix[-1] + h)  # ← Prefix sum (Day 15)
# Find minimum sum of k consecutive
min_sum = float('inf')
min_idx = 0
for i in range(len(heights) - k + 1):
    window_sum = prefix[i + k] - prefix[i]  # ← Range sum O(1)
    if window_sum < min_sum:
        min_sum = window_sum
        min_idx = i + 1
```

**What You'll Practice:**
- Prefix sum for range queries (Day 15 DSA)
- List operations (Day 0 concept)
- Alternative to sliding window (Day 15 optimization)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/363/B

---

### ✅ Problem 5.7: Codeforces 474B - Worms
- **Codeforces 474B** (Easy)
- **Link:** https://codeforces.com/problemset/problem/474/B
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 15:** Prefix sum + binary search
- **Day 0:** `bisect` module

**Why This Problem:**
```python
# Build prefix sum, then binary search for queries
import bisect
piles = [int(x) for x in input().split()]  # ← List comp (Day 0)
prefix = [0]
for pile in piles:
    prefix.append(prefix[-1] + pile)  # ← Prefix sum (Day 15)
# For each query, find which pile
for query in queries:
    pile_idx = bisect.bisect_left(prefix, query)  # ← Binary search (Day 15)
    print(pile_idx)
```

**What You'll Practice:**
- Prefix sum construction (Day 15 DSA)
- Binary search on prefix sum (Day 15 technique)
- `bisect` module (Day 0 standard library)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/474/B

---

### ✅ Problem 5.8: Codeforces 1450A - Avoid Trygub
- **Codeforces 1450A** (Easy)
- **Link:** https://codeforces.com/problemset/problem/1450/A
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 0:** Sorting strings
- **Day 1:** String rearrangement

**Why This Problem:**
```python
# You learned string sorting in Day 0:
s = input()
# Simple solution: sort to avoid "bugger"
result = ''.join(sorted(s))  # ← Sort and join (Day 0)
print(result)
```

**What You'll Practice:**
- String sorting (Day 0 concept)
- `sorted()` and `join()` (Day 0 fundamentals)
- String manipulation (Day 1 text processing)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/1450/A

---

## 💾 Progress Checkpoint

**You've completed 40 problems across 5 patterns!**

**Patterns Covered:**
- ✅ Pattern 1: Arrays & Hashing (8 problems)
- ✅ Pattern 2: Two Pointers (8 problems)
- ✅ Pattern 3: Sliding Window (8 problems)
- ✅ Pattern 4: Binary Search (8 problems)
- ✅ Pattern 5: Prefix Sum (8 problems)

**Patterns Remaining:**
- ⏳ Pattern 6: Intervals
- ⏳ Pattern 7: Stack
- ⏳ Pattern 8: Linked List
- ⏳ Pattern 9-25: Trees, Graphs, DP, Heaps, etc. (160 more problems)

---

---

## 🔥 Pattern 6: Intervals

### **Kata Connection: Day 15 (DSA) + Day 4 (Data Modeling)**
**Concepts Used:** Sorting, merging, interval overlaps, edge cases

---

### ✅ Problem 6.1: Merge Intervals
- **LeetCode #56** - Merge Intervals (Medium)
- **Link:** https://leetcode.com/problems/merge-intervals/
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 15:** Interval merging algorithm
- **Day 0:** Sorting with lambda, list operations
- **Day 4:** Data validation (overlap detection)

**Why This Problem:**
```python
# You learned sorting with custom key in Day 0:
intervals.sort(key=lambda x: x[0])  # ← Lambda (Day 0)
merged = []
for interval in intervals:
    # Check overlap (Day 4 validation logic)
    if not merged or merged[-1][1] < interval[0]:  # ← No overlap
        merged.append(interval)  # ← List append (Day 0)
    else:
        # Merge overlapping intervals
        merged[-1][1] = max(merged[-1][1], interval[1])  # ← max() (Day 0)
```

**What You'll Practice:**
- Sorting with lambda (Day 0 concept)
- Interval overlap logic (Day 4 data validation)
- List manipulation (Day 0 fundamentals)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/merge-intervals/

---

### ✅ Problem 6.2: Insert Interval
- **LeetCode #57** - Insert Interval (Medium)
- **Link:** https://leetcode.com/problems/insert-interval/
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 15:** Interval insertion and merging
- **Day 0:** List comprehensions for filtering

**Why This Problem:**
```python
# You learned list operations in Day 0:
result = []
i = 0
# Add all intervals before newInterval
while i < len(intervals) and intervals[i][1] < newInterval[0]:
    result.append(intervals[i])  # ← List append (Day 0)
    i += 1
# Merge overlapping intervals
while i < len(intervals) and intervals[i][0] <= newInterval[1]:
    newInterval[0] = min(newInterval[0], intervals[i][0])  # ← min() (Day 0)
    newInterval[1] = max(newInterval[1], intervals[i][1])
    i += 1
result.append(newInterval)
```

**What You'll Practice:**
- Interval merging logic (Day 15 DSA)
- While loops with conditions (Day 0 fundamentals)
- Min/max operations (Day 0 concept)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/insert-interval/

---

### ✅ Problem 6.3: Non-overlapping Intervals
- **LeetCode #435** - Non-overlapping Intervals (Medium)
- **Link:** https://leetcode.com/problems/non-overlapping-intervals/
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 15:** Greedy algorithm with intervals
- **Day 0:** Sorting by ending time

**Why This Problem:**
```python
# Greedy: Keep interval with earliest end time
intervals.sort(key=lambda x: x[1])  # ← Sort by end (Day 0)
count = 0
end = float('-inf')
for interval in intervals:
    if interval[0] >= end:  # ← No overlap (Day 4 logic)
        end = interval[1]  # ← Update end
    else:
        count += 1  # ← Remove this interval
return count
```

**What You'll Practice:**
- Greedy algorithm (Day 15 DSA)
- Sorting with lambda (Day 0 concept)
- Interval comparison (Day 4 validation)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/non-overlapping-intervals/

---

### ✅ Problem 6.4: Meeting Rooms
- **LeetCode #252** - Meeting Rooms (Easy, Premium)
- **Alternative:** Can practice with interval overlap concept
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 15:** Basic interval overlap detection
- **Day 0:** Sorting and comparison

**Why This Problem:**
```python
# Check if any intervals overlap
intervals.sort(key=lambda x: x[0])  # ← Sort by start (Day 0)
for i in range(1, len(intervals)):
    if intervals[i][0] < intervals[i-1][1]:  # ← Overlap check (Day 4)
        return False  # ← Cannot attend all meetings
return True
```

**What You'll Practice:**
- Interval sorting (Day 0 concept)
- Overlap detection (Day 4 validation)
- Loop with index (Day 0 fundamentals)

**🚀 GO SOLVE NOW:** (Practice with custom test cases)

---

### ✅ Problem 6.5: Meeting Rooms II
- **LeetCode #253** - Meeting Rooms II (Medium, Premium)
- **Alternative Free:** Minimum Platforms problem
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 15:** Heap for scheduling
- **Day 0:** Sorting and heap operations

**Why This Problem:**
```python
# Track overlapping meetings with heap
import heapq
intervals.sort(key=lambda x: x[0])  # ← Sort by start (Day 0)
heap = []  # ← Min heap for end times
for interval in intervals:
    if heap and heap[0] <= interval[0]:  # ← Room freed
        heapq.heappop(heap)  # ← Remove (Day 15)
    heapq.heappush(heap, interval[1])  # ← Add end time (Day 15)
return len(heap)  # ← Minimum rooms needed
```

**What You'll Practice:**
- Heap operations (Day 15 DSA)
- Sorting intervals (Day 0 concept)
- Scheduling logic (Day 15 algorithm)

**🚀 GO SOLVE NOW:** (Practice with custom test cases)

---

### ✅ Problem 6.6: Codeforces 558B - Amr and The Large Array
- **Codeforces 558B** (Easy)
- **Link:** https://codeforces.com/problemset/problem/558/B
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 0:** Dictionary for frequency and range tracking
- **Day 15:** Finding intervals with max frequency

**Why This Problem:**
```python
# Track frequency and first/last occurrence (intervals)
from collections import defaultdict
freq = defaultdict(int)  # ← Frequency counter (Day 0)
first = {}  # ← First occurrence (Day 0 dict)
last = {}
for i, num in enumerate(arr):  # ← enumerate() (Day 0)
    freq[num] += 1
    if num not in first:
        first[num] = i
    last[num] = i
# Find max frequency with smallest interval
max_freq = max(freq.values())  # ← max() (Day 0)
candidates = [num for num, f in freq.items() if f == max_freq]
# Choose smallest interval (last - first)
```

**What You'll Practice:**
- Dictionary for tracking (Day 0 concept)
- `enumerate()` for indices (Day 0 concept)
- Interval calculation (Day 15 concept)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/558/B

---

### ✅ Problem 6.7: Codeforces 279C - Ladder
- **Codeforces 279C** (Medium)
- **Link:** https://codeforces.com/problemset/problem/279/C
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 15:** Increasing/decreasing intervals
- **Day 0:** List operations and range tracking

**Why This Problem:**
```python
# Track increasing prefix and decreasing suffix
n = len(arr)
inc_len = [0] * n  # ← List initialization (Day 0)
dec_len = [0] * n
# Calculate increasing lengths
for i in range(1, n):
    if arr[i] >= arr[i-1]:
        inc_len[i] = inc_len[i-1] + 1  # ← Extend interval
# Calculate decreasing lengths
for i in range(n-2, -1, -1):  # ← Reverse iteration (Day 0)
    if arr[i] <= arr[i+1]:
        dec_len[i] = dec_len[i+1] + 1
# Check if [l, r] is "good"
```

**What You'll Practice:**
- List initialization (Day 0 concept)
- Forward/backward passes (Day 15 technique)
- Interval validation (Day 4 concept)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/279/C

---

### ✅ Problem 6.8: Codeforces 817A - Suitable Replacement
- **Codeforces 817A** (Easy)
- **Link:** https://codeforces.com/problemset/problem/817/A
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 0:** Math operations (GCD-like logic)
- **Day 4:** Coordinate interval calculation

**Why This Problem:**
```python
# Calculate if points can reach each other
x1, y1, x2, y2 = map(int, input().split())  # ← map() (Day 0)
dx, dy = abs(x2 - x1), abs(y2 - y1)  # ← abs() (Day 0)
# Check if movements align
if (dx + dy) % 2 != 0:
    print("NO")
else:
    # Calculate moves needed
    moves = (dx + dy) // 2
    print("YES" if moves >= max(dx, dy) else "NO")
```

**What You'll Practice:**
- Math operations (Day 0 fundamentals)
- `map()` function (Day 0 concept)
- Coordinate calculations (Day 4 data modeling)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/817/A

---

## 🔥 Pattern 7: Stack / Monotonic Stack

### **Kata Connection: Day 15 (DSA) + Day 0 (List as Stack)**
**Concepts Used:** LIFO, bracket matching, monotonic sequences

---

### ✅ Problem 7.1: Valid Parentheses
- **LeetCode #20** - Valid Parentheses (Easy)
- **Link:** https://leetcode.com/problems/valid-parentheses/
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 15:** Stack for bracket matching
- **Day 0:** List as stack (append/pop)
- **Day 1:** Character processing

**Why This Problem:**
```python
# You learned list operations in Day 0:
stack = []  # ← List as stack (Day 0)
pairs = {'(': ')', '{': '}', '[': ']'}
for char in s:  # ← Character iteration (Day 1)
    if char in pairs:  # ← Dict membership (Day 0)
        stack.append(char)  # ← Push (Day 0)
    else:
        if not stack or pairs[stack.pop()] != char:  # ← Pop (Day 0)
            return False
return not stack  # ← Stack should be empty
```

**What You'll Practice:**
- List as stack (Day 0 concept)
- Dictionary for mappings (Day 0 concept)
- String iteration (Day 1 text processing)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/valid-parentheses/

---

### ✅ Problem 7.2: Min Stack
- **LeetCode #155** - Min Stack (Medium)
- **Link:** https://leetcode.com/problems/min-stack/
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 15:** Stack with O(1) min operation
- **Day 0:** List operations
- **Day 9:** Optimization patterns

**Why This Problem:**
```python
# Track minimum alongside each element
class MinStack:
    def __init__(self):
        self.stack = []  # ← List as stack (Day 0)
        self.min_stack = []  # ← Track minimums
    
    def push(self, val):
        self.stack.append(val)  # ← Push (Day 0)
        # Push current min to min_stack
        min_val = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(min_val)  # ← Parallel stack (Day 15)
    
    def getMin(self):
        return self.min_stack[-1]  # ← O(1) access (Day 0)
```

**What You'll Practice:**
- Stack operations (Day 0 concept)
- Parallel data structures (Day 15 DSA)
- O(1) optimization (Day 9 performance)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/min-stack/

---

### ✅ Problem 7.3: Evaluate Reverse Polish Notation
- **LeetCode #150** - Evaluate RPN (Medium)
- **Link:** https://leetcode.com/problems/evaluate-reverse-polish-notation/
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 15:** Stack for expression evaluation
- **Day 0:** Type conversion, operators

**Why This Problem:**
```python
# Use stack to evaluate postfix notation
stack = []  # ← List as stack (Day 0)
operators = {'+', '-', '*', '/'}
for token in tokens:
    if token in operators:  # ← Set membership (Day 0)
        b = stack.pop()  # ← Pop operands (Day 0)
        a = stack.pop()
        # Perform operation
        if token == '+':
            stack.append(a + b)  # ← Push result (Day 0)
        # ... other operators
    else:
        stack.append(int(token))  # ← Type conversion (Day 0)
return stack[0]
```

**What You'll Practice:**
- Stack for evaluation (Day 15 DSA)
- Type conversion (Day 0 fundamentals)
- Set operations (Day 0 concept)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/evaluate-reverse-polish-notation/

---

### ✅ Problem 7.4: Daily Temperatures
- **LeetCode #739** - Daily Temperatures (Medium)
- **Link:** https://leetcode.com/problems/daily-temperatures/
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 15:** Monotonic stack (next greater element)
- **Day 0:** `enumerate()` for index tracking

**Why This Problem:**
```python
# Monotonic decreasing stack to find next warmer day
stack = []  # ← Store indices (Day 0)
result = [0] * len(temperatures)  # ← Initialize list (Day 0)
for i, temp in enumerate(temperatures):  # ← enumerate() (Day 0)
    # Pop smaller temperatures
    while stack and temperatures[stack[-1]] < temp:  # ← Monotonic (Day 15)
        prev_i = stack.pop()  # ← Pop (Day 0)
        result[prev_i] = i - prev_i  # ← Days until warmer
    stack.append(i)  # ← Push current index
return result
```

**What You'll Practice:**
- Monotonic stack (Day 15 DSA)
- `enumerate()` usage (Day 0 concept)
- Index tracking (Day 0 fundamentals)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/daily-temperatures/

---

### ✅ Problem 7.5: Largest Rectangle in Histogram
- **LeetCode #84** - Largest Rectangle (Hard)
- **Link:** https://leetcode.com/problems/largest-rectangle-in-histogram/
- **Difficulty:** ⭐⭐⭐⭐ Hard

**🎯 Kata Concept Tie:**
- **Day 15:** Monotonic stack for area calculation
- **Day 0:** Max tracking

**Why This Problem:**
```python
# Monotonic increasing stack for max area
stack = []  # ← Store indices (Day 0)
max_area = 0
heights.append(0)  # ← Sentinel (Day 15 technique)
for i, h in enumerate(heights):  # ← enumerate() (Day 0)
    while stack and heights[stack[-1]] > h:  # ← Monotonic
        height = heights[stack.pop()]
        width = i if not stack else i - stack[-1] - 1
        max_area = max(max_area, height * width)  # ← max() (Day 0)
    stack.append(i)
return max_area
```

**What You'll Practice:**
- Monotonic stack (Day 15 DSA)
- Area calculation (Day 15 geometry)
- Sentinel values (Day 15 technique)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/largest-rectangle-in-histogram/

---

### ✅ Problem 7.6: Codeforces 5C - Longest Regular Bracket Sequence
- **Codeforces 5C** (Medium)
- **Link:** https://codeforces.com/problemset/problem/5/C
- **Difficulty:** ⭐⭐⭐ Medium-Hard

**🎯 Kata Concept Tie:**
- **Day 15:** Stack for bracket matching with length tracking
- **Day 0:** Max tracking, list operations

**Why This Problem:**
```python
# Use stack to find longest valid bracket subsequence
stack = [-1]  # ← Initialize with base (Day 0)
max_len = 0
count = 0
for i, char in enumerate(s):  # ← enumerate() (Day 0)
    if char == '(':
        stack.append(i)  # ← Push index (Day 0)
    else:
        stack.pop()
        if not stack:  # ← No matching '('
            stack.append(i)  # ← New base
        else:
            length = i - stack[-1]  # ← Current valid length
            if length > max_len:
                max_len = length
                count = 1
            elif length == max_len:
                count += 1
```

**What You'll Practice:**
- Stack for bracket matching (Day 15 DSA)
- Index tracking (Day 0 concept)
- Max tracking with count (Day 0 fundamentals)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/5/C

---

### ✅ Problem 7.7: Codeforces 637B - Chat Order
- **Codeforces 637B** (Easy)
- **Link:** https://codeforces.com/problemset/problem/637/B
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 0:** Dictionary for seen tracking (stack-like ordering)
- **Day 6:** Memory management (most recent first)

**Why This Problem:**
```python
# Track most recent message from each user
messages = []
seen = set()  # ← Track seen users (Day 0)
for _ in range(n):
    name = input()
    messages.append(name)  # ← Store in order (Day 0)
# Print in reverse, skip duplicates
for name in reversed(messages):  # ← reversed() (Day 0)
    if name not in seen:  # ← Set membership (Day 0)
        print(name)
        seen.add(name)  # ← Mark seen
```

**What You'll Practice:**
- Set for deduplication (Day 0 concept)
- `reversed()` iteration (Day 0 fundamentals)
- LIFO ordering (Day 15 stack concept)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/637/B

---

### ✅ Problem 7.8: Codeforces 2A - Winner
- **Codeforces 2A** (Medium)
- **Link:** https://codeforces.com/problemset/problem/2/A
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 0:** Dictionary for score tracking
- **Day 6:** Multi-pass processing (history replay)

**Why This Problem:**
```python
# Track scores, then replay to find first winner
from collections import defaultdict
scores = defaultdict(int)  # ← Counter (Day 0)
rounds = []
for _ in range(n):
    name, score = input().split()
    score = int(score)
    rounds.append((name, score))  # ← Store history (Day 6)
    scores[name] += score
# Find max score
max_score = max(scores.values())  # ← max() (Day 0)
# Replay to find first to reach max
current = defaultdict(int)
for name, score in rounds:  # ← Replay history (Day 6)
    current[name] += score
    if current[name] >= max_score and scores[name] == max_score:
        print(name)
        break
```

**What You'll Practice:**
- Dictionary tracking (Day 0 concept)
- Two-pass algorithm (Day 15 technique)
- History replay (Day 6 memory concept)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/2/A

---

## 🔥 Pattern 8: Linked List

### **Kata Connection: Day 15 (DSA) + Day 4 (Data Modeling)**
**Concepts Used:** Node traversal, pointer manipulation, list reversal

---

### ✅ Problem 8.1: Reverse Linked List
- **LeetCode #206** - Reverse Linked List (Easy)
- **Link:** https://leetcode.com/problems/reverse-linked-list/
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 15:** Linked list pointer manipulation
- **Day 4:** Understanding references vs values
- **Day 0:** Variable swapping with tuples

**Why This Problem:**
```python
# Reverse by changing pointers
class ListNode:
    def __init__(self, val=0, next=None):  # ← Class definition (Day 4)
        self.val = val
        self.next = next

def reverseList(head):
    prev = None  # ← Initialize (Day 0)
    current = head
    while current:
        next_temp = current.next  # ← Save next (Day 15)
        current.next = prev  # ← Reverse pointer
        prev = current  # ← Move forward
        current = next_temp
    return prev
```

**What You'll Practice:**
- Pointer manipulation (Day 15 DSA)
- Class attributes (Day 4 data modeling)
- None handling (Day 0 fundamentals)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/reverse-linked-list/

---

### ✅ Problem 8.2: Merge Two Sorted Lists
- **LeetCode #21** - Merge Two Sorted Lists (Easy)
- **Link:** https://leetcode.com/problems/merge-two-sorted-lists/
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 15:** Merge algorithm (like merge sort)
- **Day 4:** Creating linked structures

**Why This Problem:**
```python
# Merge with dummy node technique
dummy = ListNode(0)  # ← Dummy node (Day 15 technique)
current = dummy
while l1 and l2:  # ← Both lists have nodes
    if l1.val <= l2.val:  # ← Comparison (Day 0)
        current.next = l1  # ← Link node
        l1 = l1.next  # ← Move pointer
    else:
        current.next = l2
        l2 = l2.next
    current = current.next
# Attach remaining nodes
current.next = l1 or l2  # ← Short-circuit (Day 0)
return dummy.next
```

**What You'll Practice:**
- Dummy node technique (Day 15 DSA)
- Pointer advancement (Day 15 concept)
- Short-circuit operators (Day 0 fundamentals)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/merge-two-sorted-lists/

---

### ✅ Problem 8.3: Linked List Cycle
- **LeetCode #141** - Linked List Cycle (Easy)
- **Link:** https://leetcode.com/problems/linked-list-cycle/
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 15:** Floyd's cycle detection (fast/slow pointers)
- **Day 0:** While loop with conditions

**Why This Problem:**
```python
# Two pointers: slow and fast
def hasCycle(head):
    if not head or not head.next:  # ← Edge cases (Day 0)
        return False
    slow = head  # ← Slow pointer (Day 15)
    fast = head.next
    while slow != fast:  # ← Compare references (Day 4)
        if not fast or not fast.next:
            return False  # ← No cycle
        slow = slow.next  # ← Move slow by 1
        fast = fast.next.next  # ← Move fast by 2
    return True  # ← Cycle detected
```

**What You'll Practice:**
- Two pointer technique (Day 15 DSA)
- Reference comparison (Day 4 concept)
- Edge case handling (Day 0 fundamentals)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/linked-list-cycle/

---

### ✅ Problem 8.4: Remove Nth Node From End
- **LeetCode #19** - Remove Nth Node (Medium)
- **Link:** https://leetcode.com/problems/remove-nth-node-from-end-of-list/
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 15:** Two pointers with gap
- **Day 0:** Counting and index manipulation

**Why This Problem:**
```python
# Two pointers with n gap
dummy = ListNode(0)  # ← Dummy node (Day 15)
dummy.next = head
first = second = dummy
# Move first n+1 steps ahead
for _ in range(n + 1):  # ← Loop (Day 0)
    first = first.next
# Move both until first reaches end
while first:
    first = first.next  # ← Advance together
    second = second.next
# Remove nth node
second.next = second.next.next  # ← Skip node (Day 15)
return dummy.next
```

**What You'll Practice:**
- Two pointers with gap (Day 15 DSA)
- Dummy node usage (Day 15 technique)
- Node removal (Day 15 concept)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/remove-nth-node-from-end-of-list/

---

### ✅ Problem 8.5: Reorder List
- **LeetCode #143** - Reorder List (Medium)
- **Link:** https://leetcode.com/problems/reorder-list/
- **Difficulty:** ⭐⭐⭐ Medium-Hard

**🎯 Kata Concept Tie:**
- **Day 15:** Multi-step algorithm (find middle, reverse, merge)
- **Day 0:** Multiple operations composition

**Why This Problem:**
```python
# 1. Find middle (slow/fast pointers)
slow = fast = head  # ← Two pointers (Day 15)
while fast.next and fast.next.next:
    slow = slow.next
    fast = fast.next.next
# 2. Reverse second half
second = reverse(slow.next)  # ← Function reuse (Day 0)
slow.next = None
# 3. Merge two halves
first = head
while second:
    tmp1, tmp2 = first.next, second.next  # ← Tuple unpacking (Day 0)
    first.next = second
    second.next = tmp1
    first, second = tmp1, tmp2
```

**What You'll Practice:**
- Multi-step algorithms (Day 15 DSA)
- Function composition (Day 0 concept)
- Tuple unpacking (Day 0 fundamentals)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/reorder-list/

---

### ✅ Problem 8.6: Codeforces 682A - Alyona and Numbers
- **Codeforces 682A** (Easy)
- **Link:** https://codeforces.com/problemset/problem/682/A
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 0:** Nested loops and modulo operations
- **Day 15:** Counting pairs (combinatorics)

**Why This Problem:**
```python
# Count pairs (i, j) where (i + j) % 5 == 0
n, m = map(int, input().split())  # ← map() (Day 0)
count = 0
# For each remainder mod 5
for rem_i in range(5):  # ← Range (Day 0)
    count_i = (n + 4 - rem_i) // 5  # ← How many i with this remainder
    rem_j = (5 - rem_i) % 5  # ← Complementary remainder
    count_j = (m + 4 - rem_j) // 5
    count += count_i * count_j  # ← Multiplication principle
print(count)
```

**What You'll Practice:**
- Modulo arithmetic (Day 0 fundamentals)
- Combinatorics (Day 15 math)
- Mathematical optimization (Day 15 concept)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/682/A

---

### ✅ Problem 8.7: Codeforces 231A - Team
- **Codeforces 231A** (Easy)
- **Link:** https://codeforces.com/problemset/problem/231/A
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 0:** List comprehensions and `sum()`
- **Day 1:** Input processing

**Why This Problem:**
```python
# Count problems where at least 2 friends are sure
n = int(input())
count = 0
for _ in range(n):  # ← Loop (Day 0)
    opinions = list(map(int, input().split()))  # ← map() + list (Day 0)
    if sum(opinions) >= 2:  # ← sum() (Day 0)
        count += 1
print(count)
```

**What You'll Practice:**
- `map()` with `list()` (Day 0 concept)
- `sum()` for counting (Day 0 fundamentals)
- Input processing (Day 1 concept)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/231/A

---

### ✅ Problem 8.8: Codeforces 580A - Kefa and First Steps
- **Codeforces 580A** (Easy)
- **Link:** https://codeforces.com/problemset/problem/580/A
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 15:** Longest increasing subsequence (simple version)
- **Day 0:** Max tracking in loop

**Why This Problem:**
```python
# Find longest non-decreasing subsequence
n = int(input())
money = list(map(int, input().split()))  # ← List comp (Day 0)
max_days = 1
current_days = 1
for i in range(1, n):  # ← Range with start (Day 0)
    if money[i] >= money[i-1]:  # ← Non-decreasing
        current_days += 1
        max_days = max(max_days, current_days)  # ← max() (Day 0)
    else:
        current_days = 1
print(max_days)
```

**What You'll Practice:**
- Sequence tracking (Day 15 DSA)
- Max tracking (Day 0 fundamentals)
- Comparison operations (Day 0 concept)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/580/A

---

## 🔥 Pattern 9: Binary Trees (DFS)

### **Kata Connection: Day 15 (DSA Trees) + Day 11 (Orchestration/Recursion)**
**Concepts Used:** Recursion, tree traversal, depth-first search

---

### ✅ Problem 9.1: Maximum Depth of Binary Tree
- **LeetCode #104** - Maximum Depth (Easy)
- **Link:** https://leetcode.com/problems/maximum-depth-of-binary-tree/
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 15:** DFS with recursion
- **Day 11:** Recursive task breakdown
- **Day 0:** `max()` function

**Why This Problem:**
```python
# Classic recursion problem (Day 11 concept)
def maxDepth(root):
    if not root:  # ← Base case (Day 11)
        return 0
    # Recursive case: max of left/right + 1
    left_depth = maxDepth(root.left)  # ← Recursive call (Day 11)
    right_depth = maxDepth(root.right)
    return max(left_depth, right_depth) + 1  # ← max() (Day 0)
```

**What You'll Practice:**
- Recursion basics (Day 11 orchestration)
- Tree traversal (Day 15 DSA)
- Base/recursive cases (Day 11 concept)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/maximum-depth-of-binary-tree/

---

### ✅ Problem 9.2: Invert Binary Tree
- **LeetCode #226** - Invert Binary Tree (Easy)
- **Link:** https://leetcode.com/problems/invert-binary-tree/
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 15:** DFS tree manipulation
- **Day 11:** Recursive transformation
- **Day 0:** Tuple swapping

**Why This Problem:**
```python
# Swap left and right subtrees recursively
def invertTree(root):
    if not root:  # ← Base case (Day 11)
        return None
    # Swap children (Day 0 tuple unpacking)
    root.left, root.right = root.right, root.left  # ← Swap (Day 0)
    # Recursively invert children
    invertTree(root.left)  # ← Recursive calls (Day 11)
    invertTree(root.right)
    return root
```

**What You'll Practice:**
- Recursive tree modification (Day 11 + Day 15)
- Tuple swapping (Day 0 concept)
- Post-order operations (Day 15 DSA)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/invert-binary-tree/

---

### ✅ Problem 9.3: Diameter of Binary Tree
- **LeetCode #543** - Diameter (Easy)
- **Link:** https://leetcode.com/problems/diameter-of-binary-tree/
- **Difficulty:** ⭐⭐ Easy-Medium

**🎯 Kata Concept Tie:**
- **Day 15:** DFS with global state tracking
- **Day 11:** Recursive depth calculation
- **Day 0:** Max tracking

**Why This Problem:**
```python
# Track diameter while computing depth
def diameterOfBinaryTree(root):
    diameter = 0  # ← Global state (Day 11)
    
    def depth(node):
        nonlocal diameter  # ← Closure (Day 0)
        if not node:  # ← Base case (Day 11)
            return 0
        left = depth(node.left)  # ← Recursive (Day 11)
        right = depth(node.right)
        # Update diameter (path through this node)
        diameter = max(diameter, left + right)  # ← max() (Day 0)
        return max(left, right) + 1
    
    depth(root)
    return diameter
```

**What You'll Practice:**
- Nested functions (Day 0 concept)
- `nonlocal` keyword (Day 0 advanced)
- DFS with state (Day 15 DSA)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/diameter-of-binary-tree/

---

### ✅ Problem 9.4: Balanced Binary Tree
- **LeetCode #110** - Balanced Binary Tree (Easy)
- **Link:** https://leetcode.com/problems/balanced-binary-tree/
- **Difficulty:** ⭐⭐ Easy-Medium

**🎯 Kata Concept Tie:**
- **Day 15:** DFS with validation
- **Day 11:** Recursive property checking
- **Day 0:** Absolute value

**Why This Problem:**
```python
# Check if height difference <= 1 at all nodes
def isBalanced(root):
    def height(node):
        if not node:  # ← Base case (Day 11)
            return 0
        left = height(node.left)  # ← Recursive (Day 11)
        right = height(node.right)
        # If unbalanced, return -1
        if left == -1 or right == -1 or abs(left - right) > 1:  # ← abs() (Day 0)
            return -1
        return max(left, right) + 1  # ← max() (Day 0)
    
    return height(root) != -1
```

**What You'll Practice:**
- DFS validation (Day 15 DSA)
- Sentinel values (-1) (Day 15 technique)
- `abs()` function (Day 0 fundamentals)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/balanced-binary-tree/

---

### ✅ Problem 9.5: Same Tree
- **LeetCode #100** - Same Tree (Easy)
- **Link:** https://leetcode.com/problems/same-tree/
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 15:** Parallel DFS traversal
- **Day 11:** Recursive comparison
- **Day 0:** Boolean logic

**Why This Problem:**
```python
# Compare two trees recursively
def isSameTree(p, q):
    # Base cases (Day 11)
    if not p and not q:  # ← Both null
        return True
    if not p or not q:  # ← One null
        return False
    # Check values and recursively compare children
    return (p.val == q.val and  # ← Comparison (Day 0)
            isSameTree(p.left, q.left) and  # ← Recursive (Day 11)
            isSameTree(p.right, q.right))
```

**What You'll Practice:**
- Multiple recursion (Day 11 concept)
- Boolean operators (Day 0 fundamentals)
- Parallel traversal (Day 15 DSA)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/same-tree/

---

### ✅ Problem 9.6: Subtree of Another Tree
- **LeetCode #572** - Subtree (Easy)
- **Link:** https://leetcode.com/problems/subtree-of-another-tree/
- **Difficulty:** ⭐⭐ Easy-Medium

**🎯 Kata Concept Tie:**
- **Day 15:** DFS with tree matching
- **Day 11:** Nested recursive functions
- **Day 0:** Function composition

**Why This Problem:**
```python
# Check if subRoot is subtree of root
def isSubtree(root, subRoot):
    if not root:  # ← Base case (Day 11)
        return False
    # Check if trees match at current node
    if isSameTree(root, subRoot):  # ← Function reuse (Day 0)
        return True
    # Check left and right subtrees
    return (isSubtree(root.left, subRoot) or  # ← Recursive (Day 11)
            isSubtree(root.right, subRoot))

def isSameTree(p, q):  # ← Helper function (Day 0)
    # ... same as Problem 9.5
```

**What You'll Practice:**
- Function composition (Day 0 concept)
- Nested recursion (Day 11 advanced)
- Tree matching (Day 15 DSA)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/subtree-of-another-tree/

---

### ✅ Problem 9.7: Path Sum
- **LeetCode #112** - Path Sum (Easy)
- **Link:** https://leetcode.com/problems/path-sum/
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 15:** DFS path finding
- **Day 11:** Recursive sum tracking
- **Day 0:** Subtraction for target

**Why This Problem:**
```python
# Find if root-to-leaf path sums to target
def hasPathSum(root, targetSum):
    if not root:  # ← Base case (Day 11)
        return False
    # Check if leaf node with matching sum
    if not root.left and not root.right:  # ← Leaf check
        return root.val == targetSum
    # Recursively check children with reduced target
    return (hasPathSum(root.left, targetSum - root.val) or  # ← Recursive (Day 11)
            hasPathSum(root.right, targetSum - root.val))
```

**What You'll Practice:**
- Path-to-leaf traversal (Day 15 DSA)
- Accumulator pattern (Day 11 concept)
- Leaf node detection (Day 15 technique)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/path-sum/

---

### ✅ Problem 9.8: Lowest Common Ancestor (BST)
- **LeetCode #235** - LCA of BST (Medium)
- **Link:** https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 15:** BST property (left < root < right)
- **Day 11:** Recursive search with conditions
- **Day 0:** Comparison operators

**Why This Problem:**
```python
# Use BST property to find LCA
def lowestCommonAncestor(root, p, q):
    # Both in left subtree
    if p.val < root.val and q.val < root.val:  # ← BST property (Day 15)
        return lowestCommonAncestor(root.left, p, q)  # ← Recursive (Day 11)
    # Both in right subtree
    elif p.val > root.val and q.val > root.val:
        return lowestCommonAncestor(root.right, p, q)
    else:
        # Split point (LCA)
        return root
```

**What You'll Practice:**
- BST properties (Day 15 DSA)
- Conditional recursion (Day 11 concept)
- Tree navigation (Day 15 technique)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/

---

## 🔥 Pattern 10: Binary Trees (BFS)

### **Kata Connection: Day 15 (DSA Trees/BFS) + Day 0 (Queue with List)**
**Concepts Used:** Level-order traversal, queue operations, breadth-first search

---

### ✅ Problem 10.1: Binary Tree Level Order Traversal
- **LeetCode #102** - Level Order (Medium)
- **Link:** https://leetcode.com/problems/binary-tree-level-order-traversal/
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 15:** BFS with queue
- **Day 0:** List as queue (deque for efficiency)
- **Day 11:** Level-by-level processing

**Why This Problem:**
```python
# BFS using queue
from collections import deque
def levelOrder(root):
    if not root:  # ← Base case (Day 0)
        return []
    result = []
    queue = deque([root])  # ← Deque as queue (Day 0)
    while queue:  # ← BFS loop (Day 15)
        level = []
        for _ in range(len(queue)):  # ← Process one level (Day 15)
            node = queue.popleft()  # ← Dequeue (Day 0)
            level.append(node.val)  # ← Collect values (Day 0)
            if node.left:
                queue.append(node.left)  # ← Enqueue (Day 0)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result
```

**What You'll Practice:**
- BFS algorithm (Day 15 DSA)
- `deque` operations (Day 0 collections)
- Level-by-level processing (Day 15 technique)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/binary-tree-level-order-traversal/

---

### ✅ Problem 10.2: Binary Tree Right Side View
- **LeetCode #199** - Right Side View (Medium)
- **Link:** https://leetcode.com/problems/binary-tree-right-side-view/
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 15:** BFS with level tracking
- **Day 0:** List indexing (last element)

**Why This Problem:**
```python
# BFS, take rightmost node at each level
from collections import deque
def rightSideView(root):
    if not root:
        return []
    result = []
    queue = deque([root])  # ← Queue (Day 0)
    while queue:
        level_size = len(queue)
        for i in range(level_size):  # ← Level iteration (Day 15)
            node = queue.popleft()
            # If last node in level, add to result
            if i == level_size - 1:  # ← Last index (Day 0)
                result.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return result
```

**What You'll Practice:**
- BFS level tracking (Day 15 DSA)
- Index comparison (Day 0 fundamentals)
- Selective node collection (Day 15 technique)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/binary-tree-right-side-view/

---

### ✅ Problem 10.3: Cousins in Binary Tree
- **LeetCode #993** - Cousins (Easy)
- **Link:** https://leetcode.com/problems/cousins-in-binary-tree/
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 15:** BFS with parent/depth tracking
- **Day 0:** Tuple for storing (node, parent, depth)

**Why This Problem:**
```python
# BFS, track depth and parent for each node
from collections import deque
def isCousins(root, x, y):
    queue = deque([(root, None, 0)])  # ← (node, parent, depth) tuple (Day 0)
    x_info = y_info = None
    while queue:
        node, parent, depth = queue.popleft()  # ← Tuple unpacking (Day 0)
        if node.val == x:
            x_info = (parent, depth)
        if node.val == y:
            y_info = (parent, depth)
        # Add children
        if node.left:
            queue.append((node.left, node, depth + 1))
        if node.right:
            queue.append((node.right, node, depth + 1))
    # Cousins: same depth, different parents
    return (x_info and y_info and 
            x_info[1] == y_info[1] and  # ← Same depth
            x_info[0] != y_info[0])      # ← Different parents
```

**What You'll Practice:**
- BFS with metadata (Day 15 DSA)
- Tuple packing/unpacking (Day 0 concept)
- Multi-condition checks (Day 0 fundamentals)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/cousins-in-binary-tree/

---

### ✅ Problem 10.4: Minimum Depth of Binary Tree
- **LeetCode #111** - Minimum Depth (Easy)
- **Link:** https://leetcode.com/problems/minimum-depth-of-binary-tree/
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 15:** BFS for shortest path (first leaf)
- **Day 0:** Early return optimization

**Why This Problem:**
```python
# BFS finds shortest path to leaf
from collections import deque
def minDepth(root):
    if not root:
        return 0
    queue = deque([(root, 1)])  # ← (node, depth) tuple (Day 0)
    while queue:
        node, depth = queue.popleft()  # ← Unpack (Day 0)
        # Check if leaf
        if not node.left and not node.right:  # ← Leaf check
            return depth  # ← Early return (Day 0)
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
```

**What You'll Practice:**
- BFS for shortest path (Day 15 DSA)
- Early termination (Day 0 optimization)
- Leaf detection (Day 15 technique)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/minimum-depth-of-binary-tree/

---

### ✅ Problem 10.5: Average of Levels
- **LeetCode #637** - Average of Levels (Easy)
- **Link:** https://leetcode.com/problems/average-of-levels-in-binary-tree/
- **Difficulty:** ⭐ Easy

**🎯 Kata Concept Tie:**
- **Day 15:** BFS with level aggregation
- **Day 0:** `sum()` and division for average

**Why This Problem:**
```python
# BFS, calculate average per level
from collections import deque
def averageOfLevels(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level_sum = 0
        level_count = len(queue)
        for _ in range(level_count):  # ← Process level (Day 15)
            node = queue.popleft()
            level_sum += node.val  # ← Accumulate (Day 0)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        # Calculate average
        result.append(level_sum / level_count)  # ← Division (Day 0)
    return result
```

**What You'll Practice:**
- BFS level aggregation (Day 15 DSA)
- Sum and average (Day 0 fundamentals)
- Level-wise computation (Day 15 technique)

**🚀 GO SOLVE NOW:** https://leetcode.com/problems/average-of-levels-in-binary-tree/

---

### ✅ Problem 10.6: Codeforces 115A - Party
- **Codeforces 115A** (Medium)
- **Link:** https://codeforces.com/problemset/problem/115/A
- **Difficulty:** ⭐⭐ Medium

**🎯 Kata Concept Tie:**
- **Day 15:** Tree depth (employee hierarchy)
- **Day 11:** Recursive depth calculation
- **Day 0:** Max tracking

**Why This Problem:**
```python
# Find maximum depth of employee tree
def max_depth(employee, managers):
    if managers[employee] == -1:  # ← Base case (Day 11)
        return 1
    # Recursively find manager's depth + 1
    return max_depth(managers[employee], managers) + 1  # ← Recursive (Day 11)

# Build adjacency list
n = int(input())
managers = {}
for i in range(1, n + 1):
    manager = int(input())
    managers[i] = manager
# Find max depth across all employees
max_groups = max(max_depth(i, managers) for i in range(1, n + 1))  # ← max() (Day 0)
```

**What You'll Practice:**
- Tree depth calculation (Day 15 DSA)
- Recursion (Day 11 concept)
- Dictionary for tree (Day 0 fundamentals)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/115/A

---

### ✅ Problem 10.7: Codeforces 580C - Kefa and Park
- **Codeforces 580C** (Medium)
- **Link:** https://codeforces.com/problemset/problem/580/C
- **Difficulty:** ⭐⭐⭐ Medium-Hard

**🎯 Kata Concept Tie:**
- **Day 15:** DFS on tree with constraints
- **Day 11:** Recursive path validation
- **Day 0:** List for adjacency list

**Why This Problem:**
```python
# DFS to count reachable restaurants (leaves)
def dfs(node, parent, consecutive_cats, graph, cats, m):
    # Check if too many consecutive cats
    if consecutive_cats > m:  # ← Constraint (Day 15)
        return 0
    # If leaf (restaurant), count it
    if len(graph[node]) == 1 and node != 1:  # ← Leaf check
        return 1
    count = 0
    for neighbor in graph[node]:  # ← Adjacency list (Day 0)
        if neighbor != parent:  # ← Avoid going back
            new_consecutive = consecutive_cats + 1 if cats[neighbor] else 0
            count += dfs(neighbor, node, new_consecutive, graph, cats, m)
    return count
```

**What You'll Practice:**
- DFS with constraints (Day 15 DSA)
- Tree traversal (Day 11 recursion)
- Adjacency list (Day 0 data structures)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/580/C

---

### ✅ Problem 10.8: Codeforces 510B - Fox and Two Dots
- **Codeforces 510B** (Medium)
- **Link:** https://codeforces.com/problemset/problem/510/B
- **Difficulty:** ⭐⭐⭐ Medium-Hard

**🎯 Kata Concept Tie:**
- **Day 15:** DFS cycle detection in grid
- **Day 11:** Recursive exploration with visited tracking
- **Day 0:** 2D list operations

**Why This Problem:**
```python
# DFS to find cycle in grid
def dfs(r, c, parent_r, parent_c, color, visited, grid):
    visited[r][c] = True  # ← Mark visited (Day 15)
    # Check 4 neighbors
    for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:  # ← Directions (Day 0)
        nr, nc = r + dr, c + dc
        # Check bounds
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):  # ← Bounds (Day 0)
            if grid[nr][nc] == color:
                if visited[nr][nc]:
                    # Found cycle (not parent)
                    if (nr, nc) != (parent_r, parent_c):
                        return True
                else:
                    if dfs(nr, nc, r, c, color, visited, grid):  # ← Recursive (Day 11)
                        return True
    return False
```

**What You'll Practice:**
- DFS on grid (Day 15 DSA)
- Cycle detection (Day 15 algorithm)
- 2D array navigation (Day 0 fundamentals)

**🚀 GO SOLVE NOW:** https://codeforces.com/problemset/problem/510/B

---

## 💾 Progress Checkpoint #2

**You've now completed 80 problems across 10 patterns!**

**Patterns Completed:**
- ✅ Pattern 1: Arrays & Hashing (8 problems)
- ✅ Pattern 2: Two Pointers (8 problems)
- ✅ Pattern 3: Sliding Window (8 problems)
- ✅ Pattern 4: Binary Search (8 problems)
- ✅ Pattern 5: Prefix Sum (8 problems)
- ✅ Pattern 6: Intervals (8 problems)
- ✅ Pattern 7: Stack (8 problems)
- ✅ Pattern 8: Linked List (8 problems)
- ✅ Pattern 9: Trees DFS (8 problems)
- ✅ Pattern 10: Trees BFS (8 problems)

**Patterns Remaining:**
- ⏳ Patterns 11-15: BST, Backtracking, Graphs DFS/BFS, Topological Sort (40 problems)
- ⏳ Patterns 16-20: Dijkstra, DP 1D/2D/Subsequences, Greedy (40 problems)
- ⏳ Patterns 21-25: Heaps, Trie, Bit Manipulation, Matrix, Union-Find (40 problems)

---

## 🎯 Continue for Patterns 11-15?

**Type "continue"** for the next batch:
- Pattern 11: BST (Binary Search Tree)
- Pattern 12: Backtracking
- Pattern 13: Graphs (DFS)
- Pattern 14: Graphs (BFS)
- Pattern 15: Topological Sort

**Progress: 80/200 problems (40% complete)** 🎉

---

## 🔥 Pattern 11: Binary Search Trees (BST)

### **Kata Connection: Day 15 (BST Properties) + Day 11 (Recursion)**

### ✅ 11.1: Validate BST - LeetCode #98 (Medium)
**Link:** https://leetcode.com/problems/validate-binary-search-tree/
**Concepts:** Recursion (Day 11) + BST property validation (Day 15)
**🚀 GO SOLVE NOW**

### ✅ 11.2: Kth Smallest in BST - LeetCode #230 (Medium)
**Link:** https://leetcode.com/problems/kth-smallest-element-in-a-bst/
**Concepts:** Inorder traversal (Day 15) + Counter (Day 0)
**🚀 GO SOLVE NOW**

### ✅ 11.3: Construct BST from Preorder - LeetCode #1008 (Medium)
**Link:** https://leetcode.com/problems/construct-binary-search-tree-from-preorder-traversal/
**Concepts:** BST insertion (Day 15) + Recursion (Day 11)
**🚀 GO SOLVE NOW**

### ✅ 11.4: Convert Sorted Array to BST - LeetCode #108 (Easy)
**Link:** https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/
**Concepts:** Binary search (Day 15) + Tree construction (Day 11)
**🚀 GO SOLVE NOW**

### ✅ 11.5: Range Sum of BST - LeetCode #938 (Easy)
**Link:** https://leetcode.com/problems/range-sum-of-bst/
**Concepts:** BST pruning (Day 15) + DFS (Day 11)
**🚀 GO SOLVE NOW**

### ✅ 11.6: CF 1237A - Balanced Rating - Easy
**Link:** https://codeforces.com/problemset/problem/1237/A
**Concepts:** Rounding logic (Day 0) + Math operations
**🚀 GO SOLVE NOW**

### ✅ 11.7: CF 1430A - Number of Apartments - Easy
**Link:** https://codeforces.com/problemset/problem/1430/A
**Concepts:** Math combinations (Day 0) + Greedy
**🚀 GO SOLVE NOW**

### ✅ 11.8: CF 1352A - Sum of Round Numbers - Easy
**Link:** https://codeforces.com/problemset/problem/1352/A
**Concepts:** String manipulation (Day 1) + List operations (Day 0)
**🚀 GO SOLVE NOW**

---

## 🔥 Pattern 12: Backtracking

### **Kata Connection: Day 11 (Recursion) + Day 15 (Search Algorithms)**

### ✅ 12.1: Subsets - LeetCode #78 (Medium)
**Link:** https://leetcode.com/problems/subsets/
**Concepts:** Recursion (Day 11) + List operations (Day 0)
**🚀 GO SOLVE NOW**

### ✅ 12.2: Permutations - LeetCode #46 (Medium)
**Link:** https://leetcode.com/problems/permutations/
**Concepts:** Backtracking (Day 15) + List comprehensions (Day 0)
**🚀 GO SOLVE NOW**

### ✅ 12.3: Combination Sum - LeetCode #39 (Medium)
**Link:** https://leetcode.com/problems/combination-sum/
**Concepts:** Recursive exploration (Day 11) + Target tracking (Day 0)
**🚀 GO SOLVE NOW**

### ✅ 12.4: Letter Combinations - LeetCode #17 (Medium)
**Link:** https://leetcode.com/problems/letter-combinations-of-a-phone-number/
**Concepts:** Dict mapping (Day 0) + Backtracking (Day 15)
**🚀 GO SOLVE NOW**

### ✅ 12.5: Palindrome Partitioning - LeetCode #131 (Medium)
**Link:** https://leetcode.com/problems/palindrome-partitioning/
**Concepts:** String slicing (Day 1) + Backtracking (Day 15)
**🚀 GO SOLVE NOW**

### ✅ 12.6: CF 520A - Pangram - Easy
**Link:** https://codeforces.com/problemset/problem/520/A
**Concepts:** Set operations (Day 0) + String processing (Day 1)
**🚀 GO SOLVE NOW**

### ✅ 12.7: CF 405A - Gravity Flip - Easy
**Link:** https://codeforces.com/problemset/problem/405/A
**Concepts:** Sorting (Day 0) + List operations
**🚀 GO SOLVE NOW**

### ✅ 12.8: CF 1335A - Candies - Easy
**Link:** https://codeforces.com/problemset/problem/1335/A
**Concepts:** Math (Day 0) + Integer division
**🚀 GO SOLVE NOW**

---

## 🔥 Pattern 13: Graphs - DFS

### **Kata Connection: Day 15 (Graph Algorithms) + Day 11 (Recursion)**

### ✅ 13.1: Number of Islands - LeetCode #200 (Medium)
**Link:** https://leetcode.com/problems/number-of-islands/
**Concepts:** DFS on grid (Day 15) + Visited tracking (Day 0 set)
**🚀 GO SOLVE NOW**

### ✅ 13.2: Clone Graph - LeetCode #133 (Medium)
**Link:** https://leetcode.com/problems/clone-graph/
**Concepts:** DFS with dict mapping (Day 0) + Graph traversal (Day 15)
**🚀 GO SOLVE NOW**

### ✅ 13.3: Pacific Atlantic Water - LeetCode #417 (Medium)
**Link:** https://leetcode.com/problems/pacific-atlantic-water-flow/
**Concepts:** Multi-source DFS (Day 15) + Set intersection (Day 0)
**🚀 GO SOLVE NOW**

### ✅ 13.4: Course Schedule - LeetCode #207 (Medium)
**Link:** https://leetcode.com/problems/course-schedule/
**Concepts:** Cycle detection (Day 15) + Adjacency list (Day 0)
**🚀 GO SOLVE NOW**

### ✅ 13.5: Number of Provinces - LeetCode #547 (Medium)
**Link:** https://leetcode.com/problems/number-of-provinces/
**Concepts:** Connected components (Day 15) + DFS (Day 11)
**🚀 GO SOLVE NOW**

### ✅ 13.6: CF 1141A - Game 23 - Easy
**Link:** https://codeforces.com/problemset/problem/1141/A
**Concepts:** While loops (Day 0) + Division logic
**🚀 GO SOLVE NOW**

### ✅ 13.7: CF 1343B - Balanced Array - Easy
**Link:** https://codeforces.com/problemset/problem/1343/B
**Concepts:** Math series (Day 0) + List generation
**🚀 GO SOLVE NOW**

### ✅ 13.8: CF 1328A - Divisibility - Easy
**Link:** https://codeforces.com/problemset/problem/1328/A
**Concepts:** Modulo arithmetic (Day 0) + Math
**🚀 GO SOLVE NOW**

---

## 🔥 Pattern 14: Graphs - BFS

### **Kata Connection: Day 15 (BFS) + Day 0 (Queue with deque)**

### ✅ 14.1: Rotting Oranges - LeetCode #994 (Medium)
**Link:** https://leetcode.com/problems/rotting-oranges/
**Concepts:** Multi-source BFS (Day 15) + Deque (Day 0)
**🚀 GO SOLVE NOW**

### ✅ 14.2: Word Ladder - LeetCode #127 (Hard)
**Link:** https://leetcode.com/problems/word-ladder/
**Concepts:** BFS shortest path (Day 15) + Set operations (Day 0)
**🚀 GO SOLVE NOW**

### ✅ 14.3: Walls and Gates - LeetCode #286 (Medium, Premium)
**Link:** Multi-source BFS practice
**Concepts:** BFS from multiple sources (Day 15) + Grid traversal
**🚀 GO SOLVE NOW**

### ✅ 14.4: 01 Matrix - LeetCode #542 (Medium)
**Link:** https://leetcode.com/problems/01-matrix/
**Concepts:** Multi-source BFS (Day 15) + Distance tracking
**🚀 GO SOLVE NOW**

### ✅ 14.5: Snakes and Ladders - LeetCode #909 (Medium)
**Link:** https://leetcode.com/problems/snakes-and-ladders/
**Concepts:** BFS on graph (Day 15) + Dict mapping (Day 0)
**🚀 GO SOLVE NOW**

### ✅ 14.6: CF 339B - Xenia and Ringroad - Easy
**Link:** https://codeforces.com/problemset/problem/339/B
**Concepts:** Circular array (Day 0) + Position tracking
**🚀 GO SOLVE NOW**

### ✅ 14.7: CF 1367B - Even Array - Easy
**Link:** https://codeforces.com/problemset/problem/1367/B
**Concepts:** Parity checking (Day 0) + Enumerate (Day 0)
**🚀 GO SOLVE NOW**

### ✅ 14.8: CF 1294A - Collecting Coins - Easy
**Link:** https://codeforces.com/problemset/problem/1294/A
**Concepts:** Math equations (Day 0) + Sorting
**🚀 GO SOLVE NOW**

---

## 🔥 Pattern 15: Topological Sort

### **Kata Connection: Day 15 (Graph Algorithms) + Day 11 (DAG Processing)**

### ✅ 15.1: Course Schedule II - LeetCode #210 (Medium)
**Link:** https://leetcode.com/problems/course-schedule-ii/
**Concepts:** Topological sort (Day 15) + Deque (Day 0)
**🚀 GO SOLVE NOW**

### ✅ 15.2: Alien Dictionary - LeetCode #269 (Hard, Premium)
**Link:** Practice with topological sort
**Concepts:** Graph construction (Day 15) + Topo sort
**🚀 GO SOLVE NOW**

### ✅ 15.3: Minimum Height Trees - LeetCode #310 (Medium)
**Link:** https://leetcode.com/problems/minimum-height-trees/
**Concepts:** Topological peeling (Day 15) + BFS
**🚀 GO SOLVE NOW**

### ✅ 15.4: Sort Items by Groups - LeetCode #1203 (Hard)
**Link:** https://leetcode.com/problems/sort-items-by-groups-respecting-dependencies/
**Concepts:** Nested topo sort (Day 15) + Graph algorithms
**🚀 GO SOLVE NOW**

### ✅ 15.5: Find All Recipes - LeetCode #2115 (Medium)
**Link:** https://leetcode.com/problems/find-all-possible-recipes-from-given-supplies/
**Concepts:** Topological sort (Day 15) + Set operations (Day 0)
**🚀 GO SOLVE NOW**

### ✅ 15.6: CF 1370A - Maximum GCD - Easy
**Link:** https://codeforces.com/problemset/problem/1370/A
**Concepts:** Math (Day 0) + GCD concept
**🚀 GO SOLVE NOW**

### ✅ 15.7: CF 59A - Word - Easy
**Link:** https://codeforces.com/problemset/problem/59/A
**Concepts:** String case conversion (Day 1) + Counting (Day 0)
**🚀 GO SOLVE NOW**

### ✅ 15.8: CF 1385A - Three Pairwise Maximums - Easy
**Link:** https://codeforces.com/problemset/problem/1385/A
**Concepts:** Max/min logic (Day 0) + Math reasoning
**🚀 GO SOLVE NOW**

---

## 💾 Progress Checkpoint #3

**Completed: 120/200 problems (60%)** 🎉

**Patterns 11-15 Added:**
- ✅ Pattern 11: BST (8 problems)
- ✅ Pattern 12: Backtracking (8 problems)
- ✅ Pattern 13: Graphs DFS (8 problems)
- ✅ Pattern 14: Graphs BFS (8 problems)
- ✅ Pattern 15: Topological Sort (8 problems)

**Remaining: 80 problems (Patterns 16-25)**

Type **"continue"** for final 80 problems! 🚀

---

## 🔥 Pattern 16: Dijkstra's Algorithm

### **Kata Connection: Day 15 (Shortest Path) + Day 0 (Heapq)**

### ✅ 16.1: Network Delay Time - LC #743 (Medium)
**Link:** https://leetcode.com/problems/network-delay-time/ | **Concepts:** Dijkstra (Day 15) + Heapq (Day 0) | **🚀 GO SOLVE NOW**

### ✅ 16.2: Path with Min Effort - LC #1631 (Medium)
**Link:** https://leetcode.com/problems/path-with-minimum-effort/ | **Concepts:** Modified Dijkstra (Day 15) + Grid | **🚀 GO SOLVE NOW**

### ✅ 16.3: Cheapest Flights K Stops - LC #787 (Medium)
**Link:** https://leetcode.com/problems/cheapest-flights-within-k-stops/ | **Concepts:** Constrained shortest path (Day 15) | **🚀 GO SOLVE NOW**

### ✅ 16.4: Swim in Rising Water - LC #778 (Hard)
**Link:** https://leetcode.com/problems/swim-in-rising-water/ | **Concepts:** Binary search + BFS or Dijkstra (Day 15) | **🚀 GO SOLVE NOW**

### ✅ 16.5: Path with Max Probability - LC #1514 (Medium)
**Link:** https://leetcode.com/problems/path-with-maximum-probability/ | **Concepts:** Modified Dijkstra (Day 15) | **🚀 GO SOLVE NOW**

### ✅ 16.6: CF 1374A - Required Remainder - Easy
**Link:** https://codeforces.com/problemset/problem/1374/A | **Concepts:** Modulo math (Day 0) | **🚀 GO SOLVE NOW**

### ✅ 16.7: CF 1399A - Remove Smallest - Easy
**Link:** https://codeforces.com/problemset/problem/1399/A | **Concepts:** Sorting (Day 0) + Difference check | **🚀 GO SOLVE NOW**

### ✅ 16.8: CF 1462A - Favorite Sequence - Easy
**Link:** https://codeforces.com/problemset/problem/1462/A | **Concepts:** Two pointers (Day 15) + List merge | **🚀 GO SOLVE NOW**

---

## 🔥 Pattern 17: Dynamic Programming - 1D

### **Kata Connection: Day 15 (DP) + Day 0 (List Operations)**

### ✅ 17.1: Climbing Stairs - LC #70 (Easy)
**Link:** https://leetcode.com/problems/climbing-stairs/ | **Concepts:** 1D DP (Day 15) + Fibonacci | **🚀 GO SOLVE NOW**

### ✅ 17.2: House Robber - LC #198 (Medium)
**Link:** https://leetcode.com/problems/house-robber/ | **Concepts:** 1D DP (Day 15) + Max tracking | **🚀 GO SOLVE NOW**

### ✅ 17.3: Coin Change - LC #322 (Medium)
**Link:** https://leetcode.com/problems/coin-change/ | **Concepts:** Unbounded knapsack (Day 15) + DP | **🚀 GO SOLVE NOW**

### ✅ 17.4: Longest Increasing Subseq - LC #300 (Medium)
**Link:** https://leetcode.com/problems/longest-increasing-subsequence/ | **Concepts:** DP + Binary search (Day 15) | **🚀 GO SOLVE NOW**

### ✅ 17.5: Word Break - LC #139 (Medium)
**Link:** https://leetcode.com/problems/word-break/ | **Concepts:** DP + Set lookup (Day 0) | **🚀 GO SOLVE NOW**

### ✅ 17.6: CF 1409A - Yet Another Two Ints - Easy
**Link:** https://codeforces.com/problemset/problem/1409/A | **Concepts:** Math ceiling (Day 0) | **🚀 GO SOLVE NOW**

### ✅ 17.7: CF 1433A - Boring Apartments - Easy
**Link:** https://codeforces.com/problemset/problem/1433/A | **Concepts:** Math series (Day 0) | **🚀 GO SOLVE NOW**

### ✅ 17.8: CF 1475A - Odd Divisor - Easy
**Link:** https://codeforces.com/problemset/problem/1475/A | **Concepts:** Powers of 2 (Day 0) + While loop | **🚀 GO SOLVE NOW**

---

## 🔥 Pattern 18: Dynamic Programming - 2D Grids

### **Kata Connection: Day 15 (2D DP) + Day 0 (2D Lists)**

### ✅ 18.1: Unique Paths - LC #62 (Medium)
**Link:** https://leetcode.com/problems/unique-paths/ | **Concepts:** 2D DP (Day 15) + Grid navigation | **🚀 GO SOLVE NOW**

### ✅ 18.2: Min Path Sum - LC #64 (Medium)
**Link:** https://leetcode.com/problems/minimum-path-sum/ | **Concepts:** 2D DP (Day 15) + Min accumulation | **🚀 GO SOLVE NOW**

### ✅ 18.3: Longest Common Subseq - LC #1143 (Medium)
**Link:** https://leetcode.com/problems/longest-common-subsequence/ | **Concepts:** 2D DP (Day 15) + String matching | **🚀 GO SOLVE NOW**

### ✅ 18.4: Edit Distance - LC #72 (Hard)
**Link:** https://leetcode.com/problems/edit-distance/ | **Concepts:** 2D DP (Day 15) + String operations | **🚀 GO SOLVE NOW**

### ✅ 18.5: Maximal Square - LC #221 (Medium)
**Link:** https://leetcode.com/problems/maximal-square/ | **Concepts:** 2D DP (Day 15) + Square detection | **🚀 GO SOLVE NOW**

### ✅ 18.6: CF 1512A - Spy Detected - Easy
**Link:** https://codeforces.com/problemset/problem/1512/A | **Concepts:** Counter (Day 0) + List ops | **🚀 GO SOLVE NOW**

### ✅ 18.7: CF 1520A - Do Not Be Distracted - Easy
**Link:** https://codeforces.com/problemset/problem/1520/A | **Concepts:** Set tracking (Day 0) + String | **🚀 GO SOLVE NOW**

### ✅ 18.8: CF 1535A - Fair Playoff - Easy
**Link:** https://codeforces.com/problemset/problem/1535/A | **Concepts:** Max comparison (Day 0) | **🚀 GO SOLVE NOW**

---

## 🔥 Pattern 19: DP - Subsequences

### **Kata Connection: Day 15 (DP) + Day 1 (String Processing)**

### ✅ 19.1: Longest Palindromic Subseq - LC #516 (Medium)
**Link:** https://leetcode.com/problems/longest-palindromic-subsequence/ | **Concepts:** 2D DP (Day 15) + Palindrome | **🚀 GO SOLVE NOW**

### ✅ 19.2: Distinct Subsequences - LC #115 (Hard)
**Link:** https://leetcode.com/problems/distinct-subsequences/ | **Concepts:** 2D DP (Day 15) + Counting | **🚀 GO SOLVE NOW**

### ✅ 19.3: Palindromic Substrings - LC #647 (Medium)
**Link:** https://leetcode.com/problems/palindromic-substrings/ | **Concepts:** DP or expand (Day 15) | **🚀 GO SOLVE NOW**

### ✅ 19.4: Longest Palindromic Substr - LC #5 (Medium)
**Link:** https://leetcode.com/problems/longest-palindromic-substring/ | **Concepts:** Expand or DP (Day 15) | **🚀 GO SOLVE NOW**

### ✅ 19.5: Decode Ways - LC #91 (Medium)
**Link:** https://leetcode.com/problems/decode-ways/ | **Concepts:** 1D DP (Day 15) + String parsing | **🚀 GO SOLVE NOW**

### ✅ 19.6: CF 1549A - Gregor and Cryptography - Easy
**Link:** https://codeforces.com/problemset/problem/1549/A | **Concepts:** Math (Day 0) | **🚀 GO SOLVE NOW**

### ✅ 19.7: CF 1560A - Dislike of Threes - Easy
**Link:** https://codeforces.com/problemset/problem/1560/A | **Concepts:** List generation (Day 0) | **🚀 GO SOLVE NOW**

### ✅ 19.8: CF 1584A - Mathematical Addition - Easy
**Link:** https://codeforces.com/problemset/problem/1584/A | **Concepts:** Math equation (Day 0) | **🚀 GO SOLVE NOW**

---

## 🔥 Pattern 20: Greedy - Advanced

### **Kata Connection: Day 15 (Greedy) + Day 0 (Sorting)**

### ✅ 20.1: Jump Game - LC #55 (Medium)
**Link:** https://leetcode.com/problems/jump-game/ | **Concepts:** Greedy (Day 15) + Max reach | **🚀 GO SOLVE NOW**

### ✅ 20.2: Jump Game II - LC #45 (Medium)
**Link:** https://leetcode.com/problems/jump-game-ii/ | **Concepts:** Greedy BFS (Day 15) | **🚀 GO SOLVE NOW**

### ✅ 20.3: Gas Station - LC #134 (Medium)
**Link:** https://leetcode.com/problems/gas-station/ | **Concepts:** Greedy (Day 15) + Accumulator | **🚀 GO SOLVE NOW**

### ✅ 20.4: Hand of Straights - LC #846 (Medium)
**Link:** https://leetcode.com/problems/hand-of-straights/ | **Concepts:** Counter (Day 0) + Greedy | **🚀 GO SOLVE NOW**

### ✅ 20.5: Partition Labels - LC #763 (Medium)
**Link:** https://leetcode.com/problems/partition-labels/ | **Concepts:** Greedy (Day 15) + Dict tracking | **🚀 GO SOLVE NOW**

### ✅ 20.6: CF 1607A - Linear Keyboard - Easy
**Link:** https://codeforces.com/problemset/problem/1607/A | **Concepts:** Dict for positions (Day 0) | **🚀 GO SOLVE NOW**

### ✅ 20.7: CF 1619A - Square String - Easy
**Link:** https://codeforces.com/problemset/problem/1619/A | **Concepts:** String slicing (Day 1) | **🚀 GO SOLVE NOW**

### ✅ 20.8: CF 1633A - Div 7 - Easy
**Link:** https://codeforces.com/problemset/problem/1633/A | **Concepts:** Modulo (Day 0) | **🚀 GO SOLVE NOW**

---

## 🔥 Pattern 21: Heaps / Priority Queue

### **Kata Connection: Day 15 (Heaps) + Day 0 (Heapq Module)**

### ✅ 21.1: Kth Largest in Stream - LC #703 (Easy)
**Link:** https://leetcode.com/problems/kth-largest-element-in-a-stream/ | **Concepts:** Min heap (Day 0) | **🚀 GO SOLVE NOW**

### ✅ 21.2: Last Stone Weight - LC #1046 (Easy)
**Link:** https://leetcode.com/problems/last-stone-weight/ | **Concepts:** Max heap (Day 0 heapq) | **🚀 GO SOLVE NOW**

### ✅ 21.3: K Closest Points - LC #973 (Medium)
**Link:** https://leetcode.com/problems/k-closest-points-to-origin/ | **Concepts:** Heap + distance (Day 15) | **🚀 GO SOLVE NOW**

### ✅ 21.4: Task Scheduler - LC #621 (Medium)
**Link:** https://leetcode.com/problems/task-scheduler/ | **Concepts:** Heap + greedy (Day 15) | **🚀 GO SOLVE NOW**

### ✅ 21.5: Find Median Data Stream - LC #295 (Hard)
**Link:** https://leetcode.com/problems/find-median-from-data-stream/ | **Concepts:** Two heaps (Day 15) | **🚀 GO SOLVE NOW**

### ✅ 21.6: CF 1650A - Deletions of Two Adjacent - Easy
**Link:** https://codeforces.com/problemset/problem/1650/A | **Concepts:** String indexing (Day 1) | **🚀 GO SOLVE NOW**

### ✅ 21.7: CF 1676A - Lucky - Easy
**Link:** https://codeforces.com/problemset/problem/1676/A | **Concepts:** Sum comparison (Day 0) | **🚀 GO SOLVE NOW**

### ✅ 21.8: CF 1694A - Creep - Easy
**Link:** https://codeforces.com/problemset/problem/1694/A | **Concepts:** String construction (Day 1) | **🚀 GO SOLVE NOW**

---

## 🔥 Pattern 22: Trie (Prefix Tree)

### **Kata Connection: Day 15 (Trie) + Day 4 (Data Structures)**

### ✅ 22.1: Implement Trie - LC #208 (Medium)
**Link:** https://leetcode.com/problems/implement-trie-prefix-tree/ | **Concepts:** Class design (Day 4) + Dict tree | **🚀 GO SOLVE NOW**

### ✅ 22.2: Design Add Search - LC #211 (Medium)
**Link:** https://leetcode.com/problems/design-add-and-search-words-data-structure/ | **Concepts:** Trie + DFS (Day 15) | **🚀 GO SOLVE NOW**

### ✅ 22.3: Word Search II - LC #212 (Hard)
**Link:** https://leetcode.com/problems/word-search-ii/ | **Concepts:** Trie + backtracking (Day 15) | **🚀 GO SOLVE NOW**

### ✅ 22.4: Longest Word in Dict - LC #720 (Medium)
**Link:** https://leetcode.com/problems/longest-word-in-dictionary/ | **Concepts:** Trie or set (Day 0) | **🚀 GO SOLVE NOW**

### ✅ 22.5: Replace Words - LC #648 (Medium)
**Link:** https://leetcode.com/problems/replace-words/ | **Concepts:** Trie + prefix search (Day 15) | **🚀 GO SOLVE NOW**

### ✅ 22.6: CF 1703A - YES or YES - Easy
**Link:** https://codeforces.com/problemset/problem/1703/A | **Concepts:** String case (Day 1) | **🚀 GO SOLVE NOW**

### ✅ 22.7: CF 1742A - Sum - Easy
**Link:** https://codeforces.com/problemset/problem/1742/A | **Concepts:** Sorting + comparison (Day 0) | **🚀 GO SOLVE NOW**

### ✅ 22.8: CF 1750A - Indirect Sort - Easy
**Link:** https://codeforces.com/problemset/problem/1750/A | **Concepts:** Max check (Day 0) | **🚀 GO SOLVE NOW**

---

## 🔥 Pattern 23: Bit Manipulation

### **Kata Connection: Day 15 (Bits) + Day 0 (Bitwise Operators)**

### ✅ 23.1: Single Number - LC #136 (Easy)
**Link:** https://leetcode.com/problems/single-number/ | **Concepts:** XOR (Day 15) + Bit ops | **🚀 GO SOLVE NOW**

### ✅ 23.2: Number of 1 Bits - LC #191 (Easy)
**Link:** https://leetcode.com/problems/number-of-1-bits/ | **Concepts:** Bit counting (Day 0) | **🚀 GO SOLVE NOW**

### ✅ 23.3: Counting Bits - LC #338 (Easy)
**Link:** https://leetcode.com/problems/counting-bits/ | **Concepts:** DP + bit count (Day 15) | **🚀 GO SOLVE NOW**

### ✅ 23.4: Reverse Bits - LC #190 (Easy)
**Link:** https://leetcode.com/problems/reverse-bits/ | **Concepts:** Bit shifting (Day 0) | **🚀 GO SOLVE NOW**

### ✅ 23.5: Missing Number - LC #268 (Easy)
**Link:** https://leetcode.com/problems/missing-number/ | **Concepts:** XOR or sum (Day 0) | **🚀 GO SOLVE NOW**

### ✅ 23.6: CF 1760A - Medium Number - Easy
**Link:** https://codeforces.com/problemset/problem/1760/A | **Concepts:** Sorting (Day 0) + Middle | **🚀 GO SOLVE NOW**

### ✅ 23.7: CF 1765A - Access Levels - Easy
**Link:** https://codeforces.com/problemset/problem/1765/A | **Concepts:** Counter (Day 0) | **🚀 GO SOLVE NOW**

### ✅ 23.8: CF 1788A - One and Two - Easy
**Link:** https://codeforces.com/problemset/problem/1788/A | **Concepts:** Prefix product (Day 15) | **🚀 GO SOLVE NOW**

---

## 🔥 Pattern 24: Matrix

### **Kata Connection: Day 15 (2D Arrays) + Day 0 (Nested Lists)**

### ✅ 24.1: Rotate Image - LC #48 (Medium)
**Link:** https://leetcode.com/problems/rotate-image/ | **Concepts:** Matrix rotation (Day 15) + In-place | **🚀 GO SOLVE NOW**

### ✅ 24.2: Spiral Matrix - LC #54 (Medium)
**Link:** https://leetcode.com/problems/spiral-matrix/ | **Concepts:** Boundary tracking (Day 15) | **🚀 GO SOLVE NOW**

### ✅ 24.3: Set Matrix Zeroes - LC #73 (Medium)
**Link:** https://leetcode.com/problems/set-matrix-zeroes/ | **Concepts:** In-place (Day 15) + Markers | **🚀 GO SOLVE NOW**

### ✅ 24.4: Word Search - LC #79 (Medium)
**Link:** https://leetcode.com/problems/word-search/ | **Concepts:** Backtracking (Day 15) + Grid DFS | **🚀 GO SOLVE NOW**

### ✅ 24.5: Valid Sudoku - LC #36 (Medium)
**Link:** https://leetcode.com/problems/valid-sudoku/ | **Concepts:** Set validation (Day 0) + Grid | **🚀 GO SOLVE NOW**

### ✅ 24.6: CF 1791A - Codeforces Checking - Easy
**Link:** https://codeforces.com/problemset/problem/1791/A | **Concepts:** Set membership (Day 0) | **🚀 GO SOLVE NOW**

### ✅ 24.7: CF 1800A - Is It a Cat - Easy
**Link:** https://codeforces.com/problemset/problem/1800/A | **Concepts:** String pattern (Day 1) | **🚀 GO SOLVE NOW**

### ✅ 24.8: CF 1805A - We Need the Zero - Easy
**Link:** https://codeforces.com/problemset/problem/1805/A | **Concepts:** XOR properties (Day 15) | **🚀 GO SOLVE NOW**

---

## 🔥 Pattern 25: Union-Find (Disjoint Set)

### **Kata Connection: Day 15 (Graph Components) + Day 4 (Data Structures)**

### ✅ 25.1: Number of Connected Components - LC #323 (Medium, Premium)
**Link:** Practice with Union-Find | **Concepts:** Union-Find (Day 15) + Components | **🚀 GO SOLVE NOW**

### ✅ 25.2: Redundant Connection - LC #684 (Medium)
**Link:** https://leetcode.com/problems/redundant-connection/ | **Concepts:** Cycle detection (Day 15) + Union-Find | **🚀 GO SOLVE NOW**

### ✅ 25.3: Accounts Merge - LC #721 (Medium)
**Link:** https://leetcode.com/problems/accounts-merge/ | **Concepts:** Union-Find (Day 15) + Grouping | **🚀 GO SOLVE NOW**

### ✅ 25.4: Graph Valid Tree - LC #261 (Medium, Premium)
**Link:** Practice with Union-Find | **Concepts:** Cycle + connectivity (Day 15) | **🚀 GO SOLVE NOW**

### ✅ 25.5: Longest Consecutive Seq - LC #128 (Medium)
**Link:** https://leetcode.com/problems/longest-consecutive-sequence/ | **Concepts:** Union-Find or Set (Day 0) | **🚀 GO SOLVE NOW**

### ✅ 25.6: CF 1807A - Plus or Minus - Easy
**Link:** https://codeforces.com/problemset/problem/1807/A | **Concepts:** Math check (Day 0) | **🚀 GO SOLVE NOW**

### ✅ 25.7: CF 1811A - Insert Digit - Easy
**Link:** https://codeforces.com/problemset/problem/1811/A | **Concepts:** String insertion (Day 1) | **🚀 GO SOLVE NOW**

### ✅ 25.8: CF 1829A - Love Story - Easy
**Link:** https://codeforces.com/problemset/problem/1829/A | **Concepts:** String comparison (Day 1) + Counter | **🚀 GO SOLVE NOW**

---

## 🎉 COMPLETE: All 200 Problems Mapped!

### 📊 Final Summary

**✅ Patterns 1-5:** Arrays, Two Pointers, Sliding Window, Binary Search, Prefix Sum (40 problems)
**✅ Patterns 6-10:** Intervals, Stack, Linked List, Trees DFS/BFS (40 problems)
**✅ Patterns 11-15:** BST, Backtracking, Graphs DFS/BFS, Topological Sort (40 problems)
**✅ Patterns 16-20:** Dijkstra, DP 1D/2D/Subsequences, Greedy (40 problems)
**✅ Patterns 21-25:** Heaps, Trie, Bit Manipulation, Matrix, Union-Find (40 problems)

### 🎯 How to Use This Mapping

1. **Learn Kata Concept** → Review your Day 0-16 lessons
2. **Understand Connection** → See how kata concept applies to problem
3. **Solve Problem** → Click "GO SOLVE NOW" links
4. **Track Progress** → Mark problems as completed
5. **Master Patterns** → All 25 DSA patterns covered!

### 💪 Your Learning Path

- **200 LeetCode/Codeforces problems**
- **25 algorithmic patterns**
- **16 days of kata concepts**
- **Direct "GO SOLVE NOW" action items**
- **Easy → Medium → Hard progression**

**File saved:** `katas/DSA_PROBLEM_MAPPING.md`

## 🚀 START SOLVING! Pick any pattern and begin! 🎯
