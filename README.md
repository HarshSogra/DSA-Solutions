# DSA Solutions & Interview Preparation

A structured collection of my **Data Structures & Algorithms** solutions, patterns, notes, and problem-solving approaches.

This repository tracks my preparation for **software engineering internships, coding interviews, and competitive programming**.

## 🎯 What This Repository Is For

The goal is not to collect solutions blindly. I use each problem to improve:

- Problem-solving and pattern recognition
- Time and space complexity analysis
- Clean, readable implementation
- Ability to solve problems independently
- Interview speed and consistency

> **Principle:** Don't memorize solutions. Understand the pattern behind the solution.

## 🤖 Automatic LeetCode Sync

Accepted LeetCode submissions are synchronized automatically through **GitHub Actions**.

```text
Solve on LeetCode
      ↓
Submit → Accepted
      ↓
GitHub Actions checks every 15 minutes
      ↓
Fetches accepted code + problem metadata + all tags
      ↓
Organizes the problem by a primary DSA topic
      ↓
Updates PROGRESS.md + this README
      ↓
Commits the changes automatically
```

The workflow is designed so that solving the problem remains the only regular manual step. The automation records accepted code and metadata; explanations, complexity analysis, and independent-solving status remain human-reviewed.

> **Privacy:** The LeetCode session credential is stored as a GitHub Actions secret and is never committed to this repository.

## 📚 Topics

| # | Topic | Target | Status |
|---|---|---:|---|
| 01 | Arrays | 30 | 🟡 In Progress |
| 02 | Strings | 20 | 🟡 In Progress |
| 03 | Hashing | 20 | 🟡 In Progress |
| 04 | Two Pointers | 15 | ⬜ Not Started |
| 05 | Sliding Window | 15 | ⬜ Not Started |
| 06 | Binary Search | 20 | ⬜ Not Started |
| 07 | Linked List | 20 | 🟡 In Progress |
| 08 | Stack | 15 | ⬜ Not Started |
| 09 | Queue | 10 | ⬜ Not Started |
| 10 | Recursion | 15 | ⬜ Not Started |
| 11 | Backtracking | 15 | ⬜ Not Started |
| 12 | Trees | 30 | ⬜ Not Started |
| 13 | BST | 15 | ⬜ Not Started |
| 14 | Heap | 15 | ⬜ Not Started |
| 15 | Greedy | 15 | ⬜ Not Started |
| 16 | Graphs | 30 | ⬜ Not Started |
| 17 | Dynamic Programming | 40 | ⬜ Not Started |
| 18 | Tries | 10 | ⬜ Not Started |

## 📊 Current Progress

<!-- AUTO-PROGRESS:START -->
| Metric | Count |
|---|---:|
| Problems Solved | **17** |
| Easy | 8 |
| Medium | 9 |
| Hard | 0 |
| Patterns Practiced | 17 |
| Patterns Mastered | _Manual review_ |
<!-- AUTO-PROGRESS:END -->

Detailed tracking: **[PROGRESS.md](PROGRESS.md)**

Learning plan: **[ROADMAP.md](ROADMAP.md)**

## 🧠 Core Patterns

- Hash Map / Frequency Counting
- Two Pointers
- Sliding Window
- Prefix Sum
- Binary Search
- Fast & Slow Pointers
- Stack / Monotonic Stack
- Heap / Priority Queue
- DFS / BFS
- Backtracking
- Greedy
- Dynamic Programming
- Union Find
- Trie

## 🗂️ Repository Structure

```text
DSA-Solutions/
├── 01-Arrays/
├── 02-Strings/
├── 03-Hashing/
├── 04-Two-Pointers/
├── 05-Sliding-Window/
├── 06-Binary-Search/
├── 07-Linked-List/
├── 08-Stack/
├── 09-Queue/
├── 10-Recursion/
├── 11-Backtracking/
├── 12-Trees/
├── 13-BST/
├── 14-Heap/
├── 15-Greedy/
├── 16-Graphs/
├── 17-Dynamic-Programming/
├── 18-Tries/
├── scripts/
│   └── leetcode_sync.py
├── .github/workflows/
│   └── leetcode-sync.yml
├── PROGRESS.md
└── ROADMAP.md
```

Each synced problem is stored as:

```text
Topic/
└── 0001-problem-name/
    ├── solution.py
    └── README.md
```

## 📈 Progress Philosophy

Problem count is only one metric. I also care about **independent solving ability**.

| Outcome | Meaning |
|---|---|
| ✅ Independent | Solved without hints or solution |
| 💡 Hint | Needed a small hint but completed the solution |
| 📖 Reviewed | Needed to study the solution/approach |

Automation cannot reliably infer these judgments, so they remain manual.

## 🏆 Milestones

- [ ] 25 problems
- [ ] 50 problems
- [ ] 100 problems
- [ ] 150 problems
- [ ] 200 problems
- [ ] 300 problems
- [ ] 500 problems
- [ ] Master the major interview patterns

## 🛠️ Language

Primary language: **Python**

## 🌐 Platforms

Problems may come from:

- LeetCode
- GeeksforGeeks
- Codeforces
- Coding contests

## 🔄 Manual Workflow

1. Attempt the problem independently.
2. Identify the brute-force approach.
3. Look for a better pattern or data structure.
4. Submit the solution on LeetCode.
5. If accepted, GitHub Actions syncs it automatically.
6. Review the generated problem README and add the approach, complexity, and key takeaway.
7. Revisit difficult problems later.

## ⚠️ Automation Notes

The sync uses LeetCode's GraphQL interface, which is not a stable public API. If LeetCode changes its internal API or blocks automated requests, the workflow may need maintenance. The workflow runs on a schedule rather than claiming to be an instant webhook; scheduled GitHub Actions can also be delayed under platform load.

---

⭐ This repository is a record of my progress, mistakes, patterns learned, and problems solved while becoming a better problem solver.
