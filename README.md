# The Torchbearer

**Student Name:** Ian Hock
**Student ID:** 129868450
**Course:** CS 460 – Algorithms | Spring 2026

> This README is your project documentation. Write it the way a developer would document
> their design decisions , bullet points, brief justifications, and concrete examples where
> required. You are not writing an essay. You are explaining what you built and why you built
> it that way. Delete all blockquotes like this one before submitting.

---

## Part 1: Problem Analysis

> Document why this problem is not just a shortest-path problem. Three bullet points, one
> per question. Each bullet should be 1-2 sentences max.

- **Why a single shortest-path run from S is not enough:**
  A single Dijkstra from S only gives cheapest costs from S to each node. Once you leave S and reach a relic, you need costs from that relic to the next one, which a single run from S cannot provide.

- **What decision remains after all inter-location costs are known:**
  The order to visit the relics. Knowing every cost between locations still leaves you with multiple possible orderings, each with a different total fuel cost.

- **Why this requires a search over orders (one sentence):**
  Every possible ordering of the relics produces a different total fuel cost, so you have to search over all orderings to find the minimum.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

> List the source node types as a bullet list. For each, one-line reason.

| Source Node Type | Why it is a source                                                                                                     |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Entrance         | The Torchbearer starts here, so you need costs from S to every relic and to T                                          |
| Relic chamber    | After visiting a relic, the next jump could be to any other relic or exit, so you need costs from each relic to others |

### Part 2b: Distance Storage

> Fill in the table. No prose required.

| Property                    | Your answer                                                                     |
| --------------------------- | ------------------------------------------------------------------------------- |
| Data structure name         | a dictionary of dictionaries                                                    |
| What the keys represent     | The keys represent the source nodes and the destination nodes                   |
| What the values represent   | The values represent the minimum distances from each source to each destination |
| Lookup time complexity      | O(1)                                                                            |
| Why O(1) lookup is possible | Dictionary lookups are O(1) in the average case because of hashing              |

### Part 2c: Precomputation Complexity

> State the total complexity and show the arithmetic. Two to three lines max.

- **Number of Dijkstra runs:** You run Dijkstra once from S and once from each relic. If there are k relics, then it is 1 + k runs.
- **Cost per run:** ASSIGNMENT.md states Dijkstra runs in O(m log n) time, where n = |V| and m = |E|.
- **Total complexity:** (1 + k) * O(m log n) = O(k m log n)
- **Justification (one line):** You run one Dijkstra for each source node. There are k + 1 source nodes, and each run takes O(m log n) time.

---

## Part 3: Algorithm Correctness

> Document your understanding of why Dijkstra produces correct distances.
> Bullet points and short sentences throughout. No paragraphs.

### Part 3a: What the Invariant Means

> Two bullets: one for finalized nodes, one for non-finalized nodes.
> Do not copy the invariant text from the spec.

- **For nodes already finalized (in S):**
  _Your answer here._

- **For nodes not yet finalized (not in S):**
  _Your answer here._

### Part 3b: Why Each Phase Holds

> One to two bullets per phase. Maintenance must mention nonnegative edge weights.

- **Initialization : why the invariant holds before iteration 1:**
  _Your answer here._

- **Maintenance : why finalizing the min-dist node is always correct:**
  _Your answer here._

- **Termination : what the invariant guarantees when the algorithm ends:**
  _Your answer here._

### Part 3c: Why This Matters for the Route Planner

> One sentence connecting correct distances to correct routing decisions.

_Your answer here._

---

## Part 4: Search Design

### Why Greedy Fails

> State the failure mode. Then give a concrete counter-example using specific node names
> or costs (you may use the illustration example from the spec). Three to five bullets.

- **The failure mode:** _Your answer here._
- **Counter-example setup:** _Your answer here._
- **What greedy picks:** _Your answer here._
- **What optimal picks:** _Your answer here._
- **Why greedy loses:** _Your answer here._

### What the Algorithm Must Explore

> One bullet. Must use the word "order."

- _Your answer here._

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component                | Variable name in code | Data type | Description |
| ------------------------ | --------------------- | --------- | ----------- |
| Current location         |                       |           |             |
| Relics already collected |                       |           |             |
| Fuel cost so far         |                       |           |             |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property                                    | Your answer      |
| ------------------------------------------- | ---------------- |
| Data structure chosen                       |                  |
| Operation: check if relic already collected | Time complexity: |
| Operation: mark a relic as collected        | Time complexity: |
| Operation: unmark a relic (backtrack)       | Time complexity: |
| Why this structure fits                     |                  |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** _Your answer (in terms of k)._
- **Why:** _One-line justification._

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** _Your answer here._
- **When it is used:** _Your answer here._
- **What it allows the algorithm to skip:** _Your answer here._

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** _Your answer here._
- **What the lower bound accounts for:** _Your answer here._
- **Why it never overestimates:** _Your answer here._

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- _Your answer here._

---

## References

> Bullet list. If none beyond lecture notes, write that.

- _Your references here._
