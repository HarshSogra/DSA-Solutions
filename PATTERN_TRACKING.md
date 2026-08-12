# Pattern Tracking

The LeetCode sync keeps one canonical folder per problem and separately records all LeetCode topic tags. This means a problem such as **Product of Array Except Self** can live under Arrays while also counting toward patterns such as Prefix Sum.

## How it works

1. You solve and submit on LeetCode.
2. The GitHub Actions workflow syncs accepted submissions.
3. The problem is placed in its canonical topic folder.
4. All LeetCode tags are stored in `data/problems.json`.
5. `PROGRESS.md` is regenerated from that metadata.
6. Topic and pattern counts therefore update automatically.

**No manual progress editing is required.**
