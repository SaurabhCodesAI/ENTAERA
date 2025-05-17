# 📚 How to Study - Your Complete Learning Strategy

**Last Updated:** November 15, 2025

This guide shows you **exactly** how to study the katas curriculum, apply DSA problems, and build real skills systematically.

---

## 🎯 Quick Start (15 Minutes)

**Want to start RIGHT NOW? Do this:**

1. **Open the mapping table** (top of `README.md`)
2. **Pick Day 0** (Python Fundamentals)
3. **Read:** Open `day0_python_fundamentals.md` (10 min)
4. **Code:** Open `day0_practice.py`, do Exercise 1 (5 min)
5. **Repeat** for each exercise

**That's it!** You've started your journey. 🚀

---

## 📖 The Complete Study System

### **3-Step Learning Loop** (For Each Day)

```
┌─────────────────────────────────────────┐
│  STEP 1: READ (Theory)                  │
│  Open the .md file                      │
│  Read concepts, examples, explanations  │
│  Time: 30-45 minutes                    │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  STEP 2: CODE (Practice)                │
│  Open the _practice.py file             │
│  Fill in TODOs, complete exercises      │
│  Time: 1-2 hours                        │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  STEP 3: APPLY (DSA Problems)           │
│  Open DSA_PROBLEM_MAPPING.md            │
│  Find problems using this concept       │
│  Solve 2-3 problems on LeetCode         │
│  Time: 1-2 hours                        │
└─────────────────────────────────────────┘
```

---

## 🗓️ Study Schedules (Pick Your Pace)

### **Option 1: Fast Track (2-3 hours/day, 4-6 weeks)**

**Daily Routine:**
```markdown
Week 1: Days 0-4 (Python + Data Foundations)
- Mon: Day 0 (2h) - Python fundamentals
- Tue: Day 1 (2h) - Text processing
- Wed: Day 2 (3h) - Unstructured data
- Thu: Day 3 (3h) - SQL mastery
- Fri: Day 4 (2h) - File I/O + Pydantic
- Weekend: Review + solve 10 DSA problems

Week 2: Days 5-9 (Config + AI Fundamentals)
- Mon: Day 5 (2h) - Config & logging
- Tue: Day 6 (2h) - Unit testing
- Wed: Day 7 (3h) - Semantic search
- Thu: Day 8 (3h) - Long-term memory
- Fri: Day 9 (2h) - Context management
- Weekend: Build a semantic search tool

Week 3: Days 10-13 (Production APIs)
- Mon: Day 10 (2h) - API routing
- Tue: Day 11 (3h) - API resilience
- Wed: Day 12 (2h) - Code intelligence
- Thu: Day 13 (3h) - Workflow orchestration
- Fri: Review week 1-3
- Weekend: Build a FastAPI with retries

Week 4-6: Days 15-16 (FAANG Prep)
- Week 4: DSA patterns 1-10 (Arrays, Stacks, Trees)
- Week 5: DSA patterns 11-20 (Graphs, DP, Greedy)
- Week 6: DSA patterns 21-25 + System Design
```

---

### **Option 2: Steady Pace (1-2 hours/day, 8-12 weeks)**

**Daily Routine:**
```markdown
Monday/Wednesday/Friday (1.5h each):
- 30 min: Read theory (.md file)
- 45 min: Code exercises (_practice.py)
- 15 min: Review what you learned

Tuesday/Thursday (1h each):
- Solve 2-3 DSA problems from DSA_PROBLEM_MAPPING.md
- Use concepts from recent kata days

Weekends (2-3h):
- Build a small project using learned skills
- Review the week's concepts
- Prepare next week's plan

Progress:
- Weeks 1-4: Days 0-9 (Foundations + AI)
- Weeks 5-7: Days 10-13 (Production APIs)
- Weeks 8-12: Days 15-16 (FAANG prep)
```

---

### **Option 3: Weekend Warrior (6-8 hours/weekend, 10-15 weeks)**

**Saturday (4 hours):**
```markdown
Morning (2h):
- Complete ONE full kata day
- Read theory + code all exercises
- Test your solutions

Afternoon (2h):
- Solve 5-8 DSA problems
- Use concepts from morning kata
- Build something small (mini-project)
```

**Sunday (4 hours):**
```markdown
Morning (2h):
- Start NEXT kata day
- Read theory, begin exercises

Afternoon (2h):
- Finish exercises from Sunday morning
- Solve 3-5 more DSA problems
- Review both days, write notes
```

**Progress:**
- Weeks 1-5: Days 0-9 (2 days per weekend = 10 days)
- Weeks 6-8: Days 10-13 (1-2 days per weekend)
- Weeks 9-15: Days 15-16 (DSA + System Design, ongoing)

---

## 🎓 How to Study Each Day (Step-by-Step)

### **Phase 1: Read Theory (30-45 minutes)**

**Open the `.md` file** (e.g., `day0_python_fundamentals.md`)

1. **Skim first** (5 min):
   - Read headings
   - Look at code examples
   - Note the "You'll Master" section

2. **Deep read** (20-30 min):
   - Read each section carefully
   - Type out code examples in Python REPL
   - Test variations

3. **Take notes** (5-10 min):
   - Write 3-5 key takeaways
   - Note any confusing parts
   - Bookmark examples you'll reference

**Example for Day 0:**
```python
# Test in Python REPL while reading:
>>> numbers = [1, 2, 3, 4, 5]
>>> [x**2 for x in numbers if x % 2 == 0]
[4, 16]

# Key takeaway: List comprehensions = cleaner loops
```

---

### **Phase 2: Code Exercises (1-2 hours)**

**Open the `_practice.py` file** (e.g., `day0_practice.py`)

1. **Find TODO markers:**
   ```python
   # TODO: Your code here
   ```

2. **Complete each exercise:**
   - Start with Exercise 1
   - Don't peek at solutions (build muscle memory)
   - If stuck after 10 min, review theory section

3. **Test your code:**
   ```bash
   cd d:\projects\entaera\katas
   python day0_practice.py
   ```

4. **Debug if needed:**
   - Read error messages carefully
   - Use `print()` statements
   - Check theory examples

5. **Verify understanding:**
   - Can you explain what your code does?
   - Can you write a similar solution from memory?

**Pro Tips:**
- ✅ Do exercises in order (they build on each other)
- ✅ Type code yourself (don't copy-paste)
- ✅ Commit working code to Git
- ❌ Don't skip hard exercises (that's where learning happens)

---

### **Phase 3: Apply to DSA Problems (1-2 hours)**

**Open `DSA_PROBLEM_MAPPING.md`**

1. **Find relevant problems:**
   - Search for "Day 0" or "Day 1" (whatever you just studied)
   - Look for problems using that concept

2. **Solve 2-3 problems:**
   - Start with Easy problems
   - Click "🚀 GO SOLVE NOW" link
   - Solve on LeetCode/Codeforces

3. **Connect to kata:**
   - Use the concept you just learned
   - Reference your practice code
   - Notice how kata concept applies

**Example Flow (Day 0):**
```markdown
1. Studied: List comprehensions (Day 0)
2. Find problem: Two Sum (Pattern 1, uses enumerate())
3. Solve: https://leetcode.com/problems/two-sum/
4. Use: enumerate() from Day 0 exercises!

def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):  # ← Day 0 concept!
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
```

---

## 🧠 Study Techniques That Work

### **1. The Pomodoro Method**

```
25 min: Focus (read/code)
5 min: Break (stretch, water)
25 min: Focus
5 min: Break
25 min: Focus
15 min: Longer break

Repeat 2-3 cycles per study session
```

### **2. Active Recall**

**After reading theory:**
- Close the file
- Write down 3 things you learned (from memory)
- Open file, check what you missed

**After coding:**
- Delete your solution
- Rewrite it from memory
- Compare to original

### **3. Spaced Repetition**

```
Day 1: Learn concept (Day 0)
Day 3: Review Day 0, solve 2 problems
Day 7: Review Day 0, solve 2 harder problems
Day 14: Review Day 0, solve 1 hard problem
```

### **4. Teach to Learn**

**Explain concepts out loud:**
- "List comprehensions are..."
- "Semantic search works by..."
- "API retries prevent..."

**Write blog posts** (even if not published):
- Solidifies understanding
- Creates reference for future
- Builds portfolio

---

## 📊 Track Your Progress

### **Daily Log Template**

Create `MY_LEARNING_LOG.md`:

```markdown
# My Learning Journey

## Day 0 - Python Fundamentals
**Date:** Nov 15, 2025
**Time Spent:** 2.5 hours
**Status:** ✅ Complete

**What I Learned:**
- List comprehensions: [x**2 for x in nums if x > 0]
- enumerate() for index tracking
- zip() for parallel iteration

**Exercises Completed:** 30/30

**DSA Problems Solved:**
- Two Sum (LC #1) - Easy ✅
- Contains Duplicate (LC #217) - Easy ✅
- Valid Anagram (LC #242) - Easy ✅

**Struggled With:**
- Generator expressions vs list comprehensions
- When to use map() vs comprehension

**Review Needed:**
- [ ] Revisit generators on Day 3

**Next Steps:**
- Move to Day 1 (Text Processing)
- Solve 2 more array problems
```

---

### **Weekly Review Checklist**

```markdown
## Week 1 Review
- [ ] Can I write list comprehensions from memory?
- [ ] Can I explain regex patterns?
- [ ] Can I write SQL JOINs?
- [ ] Did I solve 10+ DSA problems?
- [ ] Did I build anything with learned concepts?

## Wins This Week:
- Built a log parser using Day 2 concepts
- Solved 15 LeetCode problems

## Struggles:
- Regex lookaheads are still confusing
- Need more practice with SQL aggregations

## Next Week Focus:
- Master regex by solving text problems
- Practice SQL with 10 more queries
```

---

## 🚀 Study Tips from Experience

### **✅ DO THIS:**

1. **Start Small**
   - Don't try to complete all days in one week
   - Master one concept before moving on

2. **Code by Hand First**
   - Strengthens understanding
   - Reveals gaps in knowledge

3. **Solve DSA Problems Immediately**
   - Don't wait until "I'm ready"
   - Apply concepts while fresh

4. **Build Side Projects**
   - Every 3-4 days, build something
   - Example: After Day 5, build a semantic search for your notes

5. **Join Communities**
   - Share your progress on Twitter/LinkedIn
   - Join LeetCode discussions
   - Ask questions when stuck

6. **Review Regularly**
   - Every Friday: Review the week
   - Every 2 weeks: Revisit earlier days
   - Every month: Solve old problems again

### **❌ DON'T DO THIS:**

1. **Don't Skip Exercises**
   - Theory alone won't stick
   - Exercises build muscle memory

2. **Don't Rush**
   - Better to master 5 days than skim 15

3. **Don't Just Read Solutions**
   - Struggle for 20-30 min first
   - Learning happens in the struggle

4. **Don't Study When Tired**
   - Quality > quantity
   - Better 1 focused hour than 3 distracted hours

5. **Don't Ignore the File Mapping**
   - Use the table at top of README.md
   - Curriculum Day ≠ File number

6. **Don't Study Alone**
   - Find a study buddy
   - Share progress publicly
   - Accountability helps

---

## 🎯 Example Study Day

### **Day 0: Python Fundamentals (2.5 hours)**

**9:00-9:30 AM: Read Theory**
- Open `day0_python_fundamentals.md`
- Read sections on list comprehensions
- Test examples in Python REPL
- Take notes on key concepts

**9:30-10:00 AM: Break + Review**
- Close file
- Write down 5 things learned from memory
- Stretch, coffee break

**10:00-11:30 AM: Code Exercises**
- Open `day0_practice.py`
- Complete Exercises 1-15
- Test each solution
- Debug any errors
- Commit to Git

**11:30 AM-12:00 PM: Lunch Break**

**12:00-1:00 PM: DSA Problems**
- Open `DSA_PROBLEM_MAPPING.md`
- Find 3 problems using Day 0 concepts
- Solve Two Sum (LC #1)
- Solve Contains Duplicate (LC #217)
- Solve Valid Anagram (LC #242)

**1:00-1:30 PM: Review & Log**
- Update learning log
- Write blog post draft
- Plan tomorrow's study

**Total: 3 hours focused study**

---

## 📅 Sample 4-Week Plan (Fast Track)

### **Week 1: Foundation (Days 0-4)**
```
Mon: Day 0 (2h) + 2 problems (1h)
Tue: Day 1 (2h) + 2 problems (1h)
Wed: Day 2 (3h) + 2 problems (1h)
Thu: Day 3 (3h) + 2 problems (1h)
Fri: Day 4 (2h) + 2 problems (1h)
Sat: Build log parser project (3h)
Sun: Review week, solve 10 problems (3h)
```

### **Week 2: Config + AI (Days 5-9)**
```
Mon: Day 5 (2h) + 2 problems (1h)
Tue: Day 6 (2h) + 2 problems (1h)
Wed: Day 7 (3h) + install dependencies (1h)
Thu: Day 8 (3h) + 2 problems (1h)
Fri: Day 9 (2h) + 2 problems (1h)
Sat: Build semantic search tool (4h)
Sun: Review week, solve 10 problems (3h)
```

### **Week 3: Production APIs (Days 10-13)**
```
Mon: Day 10 (2h) + 2 problems (1h)
Tue: Day 11 (3h) + 2 problems (1h)
Wed: Day 12 (2h) + 2 problems (1h)
Thu: Day 13 (3h) + 2 problems (1h)
Fri: Review Days 10-13 (2h)
Sat: Build FastAPI with retries (4h)
Sun: Review Weeks 1-3, solve 15 problems (4h)
```

### **Week 4: FAANG Prep Start (Days 15-16)**
```
Mon: Day 15 intro + Patterns 1-3 (3h)
Tue: Patterns 4-6 (3h)
Wed: Patterns 7-9 (3h)
Thu: Patterns 10-12 (3h)
Fri: Patterns 13-15 (3h)
Sat: Day 16 System Design (4h)
Sun: Review all, solve 20 problems (4h)
```

**Continue Weeks 5-6: More DSA patterns + system design practice**

---

## 🏆 Mastery Checkpoints

### **After Day 0-4 (Foundation):**
You should be able to:
- [ ] Write list/dict comprehensions without reference
- [ ] Parse text with regex
- [ ] Extract structured data from logs
- [ ] Write SQL JOINs and aggregations
- [ ] Use Pydantic for data validation
- [ ] Solve 20+ Easy LeetCode problems

### **After Day 5-9 (AI Core):**
You should be able to:
- [ ] Build a semantic search system
- [ ] Implement agent memory
- [ ] Manage token limits
- [ ] Write unit tests
- [ ] Solve 40+ LeetCode problems (Easy + Medium)

### **After Day 10-13 (Production):**
You should be able to:
- [ ] Build REST APIs with FastAPI
- [ ] Implement retry logic
- [ ] Parse code with AST
- [ ] Build workflow orchestration
- [ ] Solve 60+ LeetCode problems

### **After Day 15-16 (FAANG):**
You should be able to:
- [ ] Recognize 25 algorithmic patterns
- [ ] Solve Medium LeetCode in 30-40 min
- [ ] Design scalable systems
- [ ] Explain time/space complexity
- [ ] Pass FAANG coding interviews

---

## 🆘 When You Get Stuck

### **Debugging Your Learning:**

**1. Can't understand theory?**
- Watch YouTube video on the topic
- Read GeeksforGeeks explanation
- Ask ChatGPT to explain like you're 5
- Take a break, come back tomorrow

**2. Can't solve exercise?**
- Reread theory section
- Look at similar example
- Try simpler version first
- Ask in coding communities (Reddit, Discord)

**3. Can't solve DSA problem?**
- Read problem carefully (3 times!)
- Draw out examples
- Try brute force first
- Look at problem hints
- After 30 min stuck, read 1 solution approach (not code)

**4. Feeling overwhelmed?**
- Slow down (quality > speed)
- Skip hard exercises, come back later
- Take a 2-day break
- Remember: This is a marathon, not sprint

---

## 📚 Supplementary Resources

### **When You Need More:**

**Python:**
- Real Python (https://realpython.com)
- Python Docs (https://docs.python.org)

**SQL:**
- SQL Zoo (https://sqlzoo.net)
- SQLBolt (https://sqlbolt.com)

**DSA:**
- NeetCode (https://neetcode.io)
- AlgoExpert (https://algoexpert.io)
- LeetCode Patterns (https://seanprashad.com/leetcode-patterns/)

**System Design:**
- System Design Primer (GitHub)
- ByteByteGo (YouTube)
- Grokking System Design Interview

**AI/ML:**
- Hugging Face Course
- Fast.ai
- Andrew Ng's ML Course

---

## ✅ Final Tips

1. **Consistency > Intensity**
   - 1 hour daily beats 7 hours Sunday

2. **Apply Immediately**
   - Build projects with learned concepts
   - Don't wait until "I'm ready"

3. **Track Progress**
   - Use learning log
   - See how far you've come

4. **Celebrate Wins**
   - Solved hard problem? Celebrate!
   - Completed day? Mark it off!

5. **Be Patient**
   - Mastery takes months, not days
   - Every expert was once a beginner

---

## 🚀 Ready to Start?

**Your First Step (Right Now):**

1. Open `README.md` (find File Mapping Table)
2. Open `day0_python_fundamentals.md`
3. Read for 10 minutes
4. Open `day0_practice.py`
5. Complete Exercise 1

**That's it! You've started your journey.** 🎉

**Remember:** The best time to start was yesterday. The second best time is **RIGHT NOW**.

Good luck! You've got this! 💪

---

**Questions? Check:**
- `README.md` - Full curriculum overview
- `QUICK_START.md` - Fastest way to begin
- `REALITY_CHECK.md` - Honest time estimates
- `DSA_PROBLEM_MAPPING.md` - 200 problems to solve
- `FIXES_APPLIED.md` - Recent improvements

**Now go build something amazing!** 🚀
