# Development Log – The Torchbearer

**Student Name:** Ian Hock
**Student ID:** 129868450

> Instructions: Write at least four dated entries. Required entry types are marked below.
> Two to five sentences per entry is sufficient. Write entries as you go, not all in one
> sitting. Graders check that entries reflect genuine work across multiple sessions.
> Delete all blockquotes before submitting.

---

## Entry 1 – May 7, 2026: Initial Plan

Read through the full assignment. The problem is basically finding the cheapest way to visit every relic in a directed weighted graph and make it to the exit. The tricky part is that the order you visit relics matters and there is no single shortest path that figures that out for you. My plan is to precompute shortest distances between all the important nodes using Dijkstra first, then search over all possible relic orderings using recursion with some pruning to cut bad paths early. I think the pruning in _explore() will be the hardest part. Going to start with Dijkstra since everything else depends on it being correct.

---

## Entry 2 – May 9, 2026: Misread the structure, going back to Part 1

I jumped straight into writing run_dijkstra() because I figured Dijkstra was the foundation and everything else would build on it. But after rereading the assignment I noticed the parts are clearly labeled and each one links a README section directly to a function. The written reasoning is supposed to come before the code, not after. That's a wrong assumption I made about the order of work. Scrapping what I had and starting from Part 1 so my documentation actually reflects my thinking instead of being written backwards.

---

## Entry 3 – [Date]: [Short description]

_Your entry here._

---

## Entry 4 – [Date]: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

_Your entry here._

---

## Final Entry – [Date]: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part                           | Estimated Hours |
| ------------------------------ | --------------- |
| Part 1: Problem Analysis       |                 |
| Part 2: Precomputation Design  |                 |
| Part 3: Algorithm Correctness  |                 |
| Part 4: Search Design          |                 |
| Part 5: State and Search Space |                 |
| Part 6: Pruning                |                 |
| Part 7: Implementation         |                 |
| README and DEVLOG writing      |                 |
| **Total**                      |                 |
