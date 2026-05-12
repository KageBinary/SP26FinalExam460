"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Ian Hock
Student ID:   129868450

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.

    """
    return """
Why a single shortest-path run from S is not enough:
A single Dijkstra from S only gives cheapest costs from S to each node. Once you leave S and reach a relic, you need costs from that relic to the next one, which a single run from S cannot provide.

What decision remains after all inter-location costs are known:
The order to visit the relics. Knowing every cost between locations still leaves you with multiple possible orderings, each with a different total fuel cost.

Why this requires a search over orders:
Every possible ordering of the relics produces a different total fuel cost, so you have to search over all orderings to find the minimum.
"""


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.

    
    """
    #used dict.fromkeys to remove duplicates while preserving order despite order not mattering it makes life easier.
    return list(dict.fromkeys([spawn] + relics))


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').

    
    """
    # start every node at infinity, source at 0
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    heap = [(0, source)]
    visited = set()

    while heap:
        current_dist, u = heapq.heappop(heap)

        # skip if already finalized
        if u in visited:
            continue
        visited.add(u)

        # relax neighbors
        for v, cost in graph[u]:
            new_dist = current_dist + cost
            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(heap, (new_dist, v))

    return dist


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.

    
    """
    sources = select_sources(spawn, relics, exit_node)
    dist_table = {}
    # run dijkstra from each source and store results in dist_table
    for source in sources:
        dist_table[source] = run_dijkstra(graph, source)
    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.


    """
    return """
For nodes already finalized (in S):
When a node gets popped and added to visited, thhe distance we have for it is guaranteed to be the true shortest distance. It is locked in and we will never find a cheaper one.

For nodes not yet finalized (not in S):
The distance we have here is the best so far, but only using paths that go through already finalized nodes. There could be a cheaper path that goes through non-finalized nodes.

Initialization: S is empty at the start, so there are no finalized nodes to check. That part holds trivially. dist[source] = 0, which is correct since the cost to reach yourself is zero. Every other node starts at infinity because no paths have been discovered yet.

Maintenance: When you pop node u with distance d, that is the smallest tentative distance of any unfinalized node. Any other path to u would have to pass through some unfinalized node w first, and dist[w] >= d. Because edge weights are nonnegative, going from w to u can only add more cost, so nothing can reach u cheaper than d. It is safe to finalize it.

Termination: When the heap is empty, every reachable node has been finalized. The invariant guarantees that dist[v] is the true shortest distance from the source to every node v. Anything still at infinity was never reachable.

If any entry in dist_table were wrong, the search would be comparing bad costs and could pick an ordering that looks optimal but actually burns more fuel than necessary.
"""


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.


    """
    return """
The failure mode: Greedy always picks the cheapest next relic from the current position. This can lock you into a path that is cheap upfront but forces expensive jumps later.

Counter-example setup: Nodes S, A, B, T. Relics are A and B. dist[S][A] = 1, dist[S][B] = 5, dist[A][B] = 100, dist[B][A] = 1, dist[A][T] = 1, dist[B][T] = 1.

What greedy picks: Greedy picks A first since dist[S][A] = 1 is cheaper than dist[S][B] = 5. Then it goes A to B for 100, then B to T for 1. Total cost = 102.

What optimal picks: Optimal picks B first (cost 5 from S), then A (cost 1 from B), then T (cost 1 from A). Total cost = 7.

Why greedy loses: Visiting A first is cheap upfront but A connects to B at cost 100. Visiting B first costs more upfront but B connects cheaply to A (cost 1), and A connects cheaply to T (cost 1). Greedy does not account for what each choice costs downstream.

What the algorithm must explore: The algorithm must search every possible order of visiting the relics because the total fuel cost depends on the full sequence of jumps, not just the cost of each individual step.
"""


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.


    """
    best = [float('inf'), []]
    relics_remaining = set(relics)
    relics_visited_order = []
    _explore(dist_table, spawn, relics_remaining, relics_visited_order, 0, exit_node, best)
    return (best[0], best[1])


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.

    """
    # dist_table[current_loc][exit_node] is the shortest possible cost to reach the exit
    # from here, so cost_so_far + that value is a lower bound on any completion of this
    # route. If it already meets or exceeds best, no completion can improve on best.
    if cost_so_far + dist_table[current_loc][exit_node] >= best[0]:
        return

    if not relics_remaining:
        total = cost_so_far + dist_table[current_loc][exit_node]
        if total < best[0]:
            best[0] = total
            best[1] = list(relics_visited_order)
        return

    for relic in list(relics_remaining):
        relics_remaining.remove(relic)
        relics_visited_order.append(relic)
        _explore(dist_table, relic, relics_remaining, relics_visited_order,
                 cost_so_far + dist_table[current_loc][relic], exit_node, best)
        relics_remaining.add(relic)
        relics_visited_order.pop()


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.


    """
    dist_table = precompute_distances(graph, spawn, relics, exit_node)
    return find_optimal_route(dist_table, spawn, relics, exit_node)


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
