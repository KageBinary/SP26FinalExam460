# The Torchbearer

**Student Name:** Ian Hock
**Student ID:** 129868450
**Course:** CS 460 – Algorithms | Spring 2026

---

## Part 1: Problem Analysis

- **Why a single shortest-path run from S is not enough:**
  A single Dijkstra from S only gives cheapest costs from S to each node. Once you leave S and reach a relic, you need costs from that relic to the next one, which a single run from S cannot provide.

- **What decision remains after all inter-location costs are known:**
  The order to visit the relics. Knowing every cost between locations still leaves you with multiple possible orderings, each with a different total fuel cost.

- **Why this requires a search over orders (one sentence):**
  Every possible ordering of the relics produces a different total fuel cost, so you have to search over all orderings to find the minimum.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

| Source Node Type | Why it is a source                                                                                                     |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Entrance         | The Torchbearer starts here, so you need costs from S to every relic and to T                                          |
| Relic chamber    | After visiting a relic, the next jump could be to any other relic or exit, so you need costs from each relic to others |

### Part 2b: Distance Storage

| Property                    | Your answer                                                                     |
| --------------------------- | ------------------------------------------------------------------------------- |
| Data structure name         | a dictionary of dictionaries                                                    |
| What the keys represent     | The keys represent the source nodes and the destination nodes                   |
| What the values represent   | The values represent the minimum distances from each source to each destination |
| Lookup time complexity      | O(1)                                                                            |
| Why O(1) lookup is possible | Dictionary lookups are O(1) in the average case because of hashing              |

### Part 2c: Precomputation Complexity

- **Number of Dijkstra runs:** You run Dijkstra once from S and once from each relic. If there are k relics, then it is 1 + k runs.
- **Cost per run:** ASSIGNMENT.md states Dijkstra runs in O(m log n) time, where n = |V| and m = |E|.
- **Total complexity:** (1 + k) * O(m log n) = O(k m log n)
- **Justification (one line):** You run one Dijkstra for each source node. There are k + 1 source nodes, and each run takes O(m log n) time.

---

## Part 3: Algorithm Correctness

### Part 3a: Invariant Explanation

- **For nodes already finalized (in S):**
  When a node gets popped and added to visited, the distance we have for it is guaranteed to be the true shortest distance. It is locked in and we will never find a cheaper one.

- **For nodes not yet finalized (not in S):**
  The distance we have here is the best so far, but only using paths that go through already finalized nodes. There could be a cheaper path that goes through non-finalized nodes.

### Part 3b: Invariant Maintenance

- **Initialization : why the invariant holds before iteration 1:**
  S is empty at the start, so there are no finalized nodes to check. That part holds trivially. dist[source] = 0, which is correct since the cost to reach yourself is zero. Every other node starts at infinity because no paths have been discovered yet.

- **Maintenance : why finalizing the min-dist node is always correct:**
  When you pop node u with distance d, that is the smallest tentative distance of any unfinalized node. Any other path to u would have to pass through some unfinalized node w first, and dist[w] >= d. Because edge weights are nonnegative, going from w to u can only add more cost, so nothing can reach u cheaper than d. It is safe to finalize it.

- **Termination : what the invariant guarantees when the algorithm ends:**
  When the heap is empty, every reachable node has been finalized. The invariant guarantees that dist[v] is the true shortest distance from the source to every node v. Anything still at infinity was never reachable.

### Part 3c: Why Correctness Matters

If any entry in dist_table were wrong, the search would be comparing bad costs and could pick an ordering that looks optimal but actually burns more fuel than necessary.

---

## Part 4: Search Design

### Why Greedy Fails

- **The failure mode:** Greedy always picks the cheapest next relic from the current position. This can lock you into a path that is cheap upfront but forces expensive jumps later.
- **Counter-example setup:** Nodes S, A, B, T. Relics are A and B. dist[S][A] = 1, dist[S][B] = 5, dist[A][B] = 100, dist[B][A] = 1, dist[A][T] = 1, dist[B][T] = 1.
- **What greedy picks:** Greedy picks A first since dist[S][A] = 1 is cheaper than dist[S][B] = 5. Then it goes A to B for 100, then B to T for 1. Total cost = 102.
- **What optimal picks:** Optimal picks B first (cost 5 from S), then A (cost 1 from B), then T (cost 1 from A). Total cost = 7.
- **Why greedy loses:** Visiting A first is cheap upfront but A connects to B at cost 100. Visiting B first costs more upfront but B connects cheaply to A (cost 1), and A connects cheaply to T (cost 1). Greedy does not account for what each choice costs downstream.

### What the Algorithm Must Explore

- The algorithm must search every possible order of visiting the relics because the total fuel cost depends on the full sequence of jumps, not just the cost of each individual step.

---

## Part 5: State and Search Space

### Part 5a: State Representation

| Component                | Variable name in code  | Data type | Description                                              |
| ------------------------ | ---------------------- | --------- | -------------------------------------------------------- |
| Current location         | `current_loc`          | node      | The node the Torchbearer is at right now                 |
| Relics already collected | `relics_remaining`     | set       | The relics not yet visited (removed as each is visited)  |
| Fuel cost so far         | `cost_so_far`          | float     | Total fuel spent to reach the current state              |

### Part 5b: Data Structure for Visited Relics

| Property                                    | Your answer                                                                  |
| ------------------------------------------- | ---------------------------------------------------------------------------- |
| Data structure chosen                       | set                                                                          |
| Operation: check if relic already collected | Time complexity: O(1)                                                        |
| Operation: mark a relic as collected        | Time complexity: O(1)                                                        |
| Operation: unmark a relic (backtrack)       | Time complexity: O(1)                                                        |
| Why this structure fits                     | All three operations needed during the search run in O(1) using a Python set |

### Part 5c: Worst-Case Search Space

- **Worst-case number of orders considered:** k! where k is the number of relics.
- **Why:** The first relic can be any of k choices, the second any of k-1, and so on, giving k * (k-1) * ... * 1 = k! total orderings in the worst case with no pruning.

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

- **What is tracked:** The minimum total fuel cost found so far and the relic ordering that achieved it, stored together in `best` as a mutable list so it can be updated in place across all recursive calls.
- **When it is used:** Checked at the start of every recursive call before exploring further, and updated in the base case whenever a complete route with a lower total cost is found.
- **What it allows the algorithm to skip:** Any path where the cost already spent plus the shortest possible remaining distance to exit is already at or above the current best — those paths cannot improve the answer so they are abandoned early.

### Part 6b: Lower Bound Estimation

- **What information is available at the current state:** The current location, the fuel cost spent so far, and the precomputed shortest distances between all important nodes in dist_table.
- **What the lower bound accounts for:** The minimum possible cost to reach the exit from the current location, which is dist_table[current_loc][exit_node].
- **Why it never overestimates:** It is the shortest possible path from the current location to the exit, ignoring any relics still to visit. The actual remaining cost must be at least this value since the Torchbearer still has to visit more relics before reaching exit.

### Part 6c: Pruning Correctness

- If cost_so_far + dist_table[current_loc][exit_node] >= best[0], then even finishing this route in the cheapest possible way cannot beat the current best. Since the lower bound never overestimates the remaining cost, cutting this branch cannot throw away the optimal solution.

---

## References

- Lecture notes only.
