# 🎓 ENTAERA MASTERY CURRICULUM
## Learn at Your Own Pace - No Deadlines, Just Growth

> **📚 Note:** This is one of two learning resources in ENTAERA. Also check out `katas/` folder for comprehensive day-by-day curriculum including FAANG interview prep. See `UNIFIED_LEARNING_GUIDE.md` in the root folder for how to use both together!

---

## 📚 **LEARNING PHILOSOPHY**

> **"Experiment, Break, Fix, Master"**

This isn't about cramming for interviews. This is about **actually understanding** what you built and becoming a better engineer.

---

## 🗂️ **CURRICULUM STRUCTURE**

### **⭐ SEMANTIC SEARCH MASTERY - TF-IDF + FAISS**
**Location:** `katas/SEMANTIC_SEARCH_MASTERY.md` (3-4 hours)

**START HERE if you want to understand semantic search!**

This comprehensive guide teaches BOTH approaches:
- **TF-IDF** - Your current implementation in `agent.py`
- **FAISS** - Industry standard with embeddings
- Side-by-side comparison with real examples
- When to use which approach
- Production patterns (Hybrid, Lazy Loading, Caching)
- 3 hands-on exercises building both from scratch
- Interview talking points for honest answers

**Three paths:** Keep TF-IDF, upgrade to FAISS, or build hybrid

---

### **1. PRACTICAL_MASTERY_EXERCISES.md** (2,194 lines)
**Focus:** Python fundamentals through hands-on experimentation

**Topics covered:**
- Enums, Dataclasses, Type Hints
- Vector Embeddings & FAISS (also see SEMANTIC_SEARCH_MASTERY.md)
- Temperature & Sampling
- Rate Limiting & Exponential Backoff
- Prompt Engineering
- Error Handling Patterns
- Inheritance & Polymorphism
- Abstract Base Classes
- List Comprehensions & Lambda
- Context Managers (`with` statement)
- Generators (`yield`)
- DSA Fundamentals (Stack, Queue, Hash Maps)
- Async/Await patterns

**Time estimate:** 20-30 hours
**Approach:** Pick any exercise, do it when curious

---

### **2. ADVANCED_EXERCISES.md** (1,251 lines)
**Focus:** TypeScript, Next.js, and modern web development

**Topics covered:**
- TypeScript interfaces vs types
- Next.js API routes
- Google Gemini API integration
- FormData processing
- Error handling in production
- API design patterns

**Time estimate:** 15-20 hours
**Approach:** Complete after Python fundamentals

---

### **3. ALGORITHMS_AND_DATA_STRUCTURES.md** (1,377 lines)
**Focus:** Practical algorithms used in real projects

**Topics covered:**
- String parsing & extraction
- Grouping & clustering
- Routing systems
- Duplicate detection
- Caching strategies
- Two pointers pattern
- Sliding window
- Hash maps in practice

**Time estimate:** 10-15 hours
**Approach:** Learn as needed for real problems

---

### **4. PRODUCTION_SKILLS.md** (NEW!)
**Focus:** SQL, Testing, Docker, Git, Logging & Monitoring

**Topics covered:**
- SQL queries (SELECT, JOIN, WHERE, aggregations)
- Testing with pytest (unit tests, mocking, coverage)
- Docker basics (Dockerfile, containers, Docker Compose)
- Git workflow (feature branches, PRs, merge conflicts)
- Logging & monitoring (structured logs, Sentry)

**Time estimate:** 8-10 hours

---

### **5. PRACTICAL_MASTERY_DAYS_3-6.md**
**Focus:** Advanced Python patterns and production skills

**Topics covered:**
- Advanced async patterns
- Performance optimization
- Additional production patterns

**Time estimate:** 6-8 hours

---

## 🎯 **RECOMMENDED LEARNING PATH**

### **🔥 CRITICAL (Must Do First - Day 1-2: 12 hours)**

**Core AI/Backend Skills:**
1. **SEMANTIC_SEARCH_MASTERY.md** (TF-IDF + FAISS) - 3-4 hours ⭐ START HERE
   - **Location:** `katas/SEMANTIC_SEARCH_MASTERY.md`
   - **Why:** Understand BOTH your current implementation (TF-IDF) AND industry standard (FAISS)
   - **Outcome:** Can honestly explain "I built TF-IDF search, explored FAISS, here's when to use each"
   - **Bonus:** Side-by-side comparison, production patterns, interview talking points
   
2. **Exercise 8** (Prompt Engineering) - 1.5 hours
   - **Why:** Direct impact on your Snap2Slides quality
   - **Outcome:** Improve AI outputs from 60% → 80% quality
   
3. **Exercise 7** (Rate Limiting + Backoff) - 1.5 hours
   - **Why:** Production systems need this
   - **Outcome:** APIs don't crash when rate limits hit
   
4. **Exercise 9** (Error Handling) - 1 hour
   - **Why:** Professional code doesn't just crash
   - **Outcome:** Graceful failures with useful error messages

**Data Skills:**
5. **String Parsing** (ALGORITHMS) - 2 hours
   - **Why:** Email/document parsing is real-world skill
   - **Outcome:** Extract structured data from text
   
6. **SQL Basics** (PRODUCTION_SKILLS) - 2 hours
   - **Why:** Databases are everywhere
   - **Outcome:** Write SELECT, JOIN, WHERE queries
   
7. **Exercise 13** (List Comprehensions) - 20 min
   - **Why:** Write Pythonic code
   - **Outcome:** Clean, readable Python

**Total Critical: 10-12 hours**

---

### **💪 NICE TO HAVE (Day 3-5: 20 hours)**

**Python Fundamentals:**
8. **Exercise 1-3** (Enums, Dataclasses, Type Hints) - 2 hours
   - **Why:** Understand your own code structure
   
9. **Exercise 6** (Temperature/Sampling) - 1 hour
   - **Why:** Control AI creativity vs consistency
   
10. **Exercise 10-12** (Inheritance, Polymorphism, ABC) - 2 hours
    - **Why:** Code organization patterns
    
11. **Exercise 14-17** (Lambda, Args/Kwargs, Context Managers, Generators) - 2.5 hours
    - **Why:** Advanced Python patterns

**Algorithms & Data Structures:**
12. **Hash Maps** (ALGORITHMS) - 1 hour
    - **Why:** Fast lookups, caching patterns
    
13. **Two Pointers** (ALGORITHMS) - 1 hour
    - **Why:** Efficient array manipulation
    
14. **Stack/Queue** (ALGORITHMS) - 1 hour
    - **Why:** Ordered processing, undo/redo

**Production Skills:**
15. **Testing with pytest** (PRODUCTION_SKILLS) - 2 hours
    - **Why:** Professional code has tests
    
16. **Docker Basics** (PRODUCTION_SKILLS) - 2 hours
    - **Why:** Modern deployment
    
17. **Git Workflow** (PRODUCTION_SKILLS) - 1 hour
    - **Why:** Team collaboration
    
18. **Logging/Monitoring** (PRODUCTION_SKILLS) - 1.5 hours
    - **Why:** Debug production issues

**Total Nice to Have: 19-20 hours**

---

### **📅 WEEK 1 SCHEDULE (6 hours/day)**

**Day 1 (6 hours):**
- Morning: Vector Embeddings + FAISS (2 hours)
- Afternoon: String Parsing (2 hours)
- Evening: SQL Basics (2 hours)

**Day 2 (6 hours):**
- Morning: Prompt Engineering (1.5 hours)
- Afternoon: Rate Limiting (1.5 hours)
- Evening: Error Handling + List Comprehensions (1.5 hours)
- Review: Check understanding (1.5 hours)

**Day 3 (6 hours):**
- Morning: Enums, Dataclasses, Type Hints (2 hours)
- Afternoon: Temperature + Inheritance patterns (3 hours)
- Evening: Testing basics (1 hour)

**Day 4 (6 hours):**
- Morning: Hash Maps + Two Pointers (2 hours)
- Afternoon: Lambda, Args/Kwargs, Context Managers (2 hours)
- Evening: Docker basics (2 hours)

**Day 5 (6 hours):**
- Morning: Stack/Queue + Generators (2 hours)
- Afternoon: Git Workflow (1 hour)
- Evening: Logging/Monitoring (1.5 hours)
- Review: Build something with new skills (1.5 hours)

**Total: 30 hours across 5 days**

---

## 🎓 **WHAT YOU'LL MASTER**

### **After Day 1-2 (Critical Path - 12 hours):**
✅ FAISS vector search working in your project  
✅ Professional error handling  
✅ SQL queries for data retrieval  
✅ String parsing for real-world text processing  
✅ Prompt engineering for better AI outputs  
✅ Production-grade rate limiting  

**Confidence Level: 70% → Can explain and extend your projects**

### **After Day 3-5 (Nice to Have - 18 hours):**
✅ All Python fundamentals solid  
✅ Practical algorithms mastered  
✅ Testing, Docker, Git workflow  
✅ Production logging and monitoring  

**Confidence Level: 90% → Can build new features independently**

---

## 🚀 **START HERE (Next 30 Minutes)**

### **Option 1: Jump into Critical Path**
Open `PRACTICAL_MASTERY_EXERCISES.md` → Go to Exercise 4 (Vector Embeddings)

### **Option 2: Quick Win First**
Open `PRACTICAL_MASTERY_EXERCISES.md` → Go to Exercise 13 (List Comprehensions) - 20 min

### **Option 3: Most Practical**
Open `ALGORITHMS_AND_DATA_STRUCTURES.md` → String Parsing (immediately useful)

---

## 🎯 **FLEXIBLE APPROACH**

Don't like the schedule? That's fine! Here's the rule:

**Critical items (1-7): Do these however you want, but DO them**  
**Nice to have (8-18): Pick what interests you, skip what doesn't**

No pressure. No deadlines. Just steady progress.

---

## ⏰ **DAILY ROUTINE (Flexible)**

### **Option 1: Deep Focus (2 hours)**
- Pick ONE exercise
- Complete it fully
- Document what you learned

### **Option 2: Breadth Sampling (1 hour)**
- 30 min: Read/understand concept
- 30 min: Quick experiment in REPL

### **Option 3: Project-Based (3-4 hours weekends)**
- Apply learned concept to real project
- Build new feature using the skill
- Write blog post about it

---

## 📊 **TRACKING YOUR PROGRESS**

### **Simple Method:**
Create a file: `my-progress.md`

```markdown
# My Mastery Journey

## Week 1
- ✅ Completed: Enums (Exercise 1)
- ✅ Completed: Dataclasses (Exercise 2)
- 🔄 In Progress: Vector Embeddings (Exercise 4)
- 📝 Learned: Enums provide type safety AND string compatibility

## Week 2
- 🎯 Goal: Understand FAISS deeply
- 📚 Reading: FAISS documentation
- 💻 Building: Replace TF-IDF with FAISS
```

---

## 🚀 **GETTING STARTED (Right Now)**

### **Step 1: Pick One Thing**
What sounds most interesting?
- Python fundamentals? → `PRACTICAL_MASTERY_EXERCISES.md`
- TypeScript/Web? → `ADVANCED_EXERCISES.md`
- Algorithms? → `ALGORITHMS_AND_DATA_STRUCTURES.md`

### **Step 2: Do Exercise 1**
Just open the file and do the first exercise. Takes 30-60 minutes.

### **Step 3: Reflect**
What did you learn? Write it down.

### **Step 4: Repeat**
No pressure. Learn when you're curious. Build when you're inspired.

---

## 💡 **LEARNING TIPS**

### **1. Experiment First**
Don't just read code - run it, break it, fix it.

### **2. Connect to Your Projects**
Every concept relates to something you built. Find the connection.

### **3. Teach to Learn**
Explain concepts out loud. Write blog posts. Help others.

### **4. Take Breaks**
Mastery takes time. It's okay to pause and come back.

### **5. Build Real Things**
Best way to learn: apply it to a real problem you care about.

---

## 🎓 **COMPLETION ≠ MASTERY**

You don't need to complete every exercise. Pick what excites you. Skip what doesn't.

**Mastery = Understanding, not checkbox completion**

---

## 📈 **BEYOND THESE EXERCISES**

When you've gone through what interests you here:

1. **Build something new** - Use these skills in a fresh project
2. **Contribute to open source** - Apply what you learned
3. **Create your own exercises** - Teach others
4. **Start a blog** - Document your journey

---

## 🤝 **NEED HELP?**

- Stuck on a concept? Google it, ChatGPT it, experiment more
- Want to discuss? Find a community (Discord, Reddit)
- Built something cool? Share it!

---

**Remember: This is YOUR journey. Go at YOUR pace. Learn what YOU want.**

**Now pick an exercise and start. Good luck! 🚀**
