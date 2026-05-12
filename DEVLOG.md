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

## Entry 3 – May 9, 2026: Finished Part 2 README

I worked through the questions in Part 2 and filled out the README. I had to figure out which nodes to run Dijkstra from and decide on the right data structure for storing distances. I also calculated the complexity of the Dijkstra precomputation section to be O(k m log n) where k is the number of relics, m is the number of edges, and n is the number of nodes. I think I have a good understanding of the precomputation design now, so I can move on to implementing Dijkstra next.

---

## Entry 4 – May 9, 2026: Implemented Part 2 Code

Implemented select_sources, run_dijkstra, and precompute_distances. Everything was pretty straightforward. The hardest part was Dijkstra but we have gone over it several times in class so it was relatively easy. select_sources and precompute_distances were simple once the design was already documented in the README.

---

## Entry 5 – May 11, 2026: Part 3 Correctness

Worked through the invariant explanation for Dijkstra. The three phases were initialization, maintenance, and termination. Initialization was straightforward since S is empty at the start so there is nothing to be wrong about. Maintenance took the most thought because you have to argue that the min-heap always pops the globally cheapest unfinalized node, and nonneg edge weights are the reason that holds. If weights could be negative you could always find a cheaper path through an unfinalized node later. Termination follows directly once maintenance is proven since every node eventually gets finalized.

---

## Entry 6 – May 11, 2026: Part 4 Search Design

Worked through why greedy does not work for this problem. The key issue is that greedy only looks at the cost of the next step and ignores what that choice forces you into later. I came up with a counter-example using two relics A and B where greedy picks A first because it is closer to S, but going to A traps you into a 100-cost edge to B. Going to B first costs more upfront but leads to cheap edges to A and then T. Greedy total was 102, optimal was 7. That made the failure mode pretty clear.

---

## Entry 7 – May 11, 2026: Implemented Search Code

Implemented find_optimal_route, _explore, and solve. The structure is a recursive branch and bound over all orderings of the relics. At each step you pick a relic to visit next, recurse, then backtrack by removing it. The base case is when no relics are left, at which point you add the cost to exit and compare against best. The pruning uses dist_table[current_loc][exit_node] as a lower bound on the remaining cost. That value is the shortest possible way to reach exit from here, so if cost_so_far plus that lower bound is already at or above best, no completion of this branch can win. All five provided tests passed, but i still need to finish the README and do some more of my own testing.

---

## Entry 8 – May 11, 2026: Part 6 Pruning Documentation and Typo Fix

Wrote the README for Part 6, the pruning stuff. The main thing I had to think through for 6b was why using dist_table[current_loc][exit_node] as a lower bound is safe. It works because that is just the cost to go straight to exit and ignores any relics left to visit, so the real remaining cost can only be higher. Also noticed and fixed a typo in Part 3a where I had typed "thhe" instead of "the" in both the README and the matching string in dijkstra_invariant_check().

---

## Entry 9 – [Date]: Post-Implementation Reflection

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
