from torchbearer import solve



# no relics, should go straight to exit
test1 = {'S': [('T', 4)], 'T': []}
cost, order = solve(test1, 'S', [], 'T')
print("no relics")
print(f"  got: {cost} {order}  expected: 4 []")



# single relic sitting on the only path to exit
test2 = {'S': [('R', 3)], 'R': [('T', 3)], 'T': []}
cost, order = solve(test2, 'S', ['R'], 'T')
print("single relic on only path")
print(f"  got: {cost} {order}  expected: 6 ['R']")



# two relics where picking the wrong one first is way more expensive
test3 = {
    'S': [('A', 1), ('B', 10)],
    'A': [('B', 1), ('T', 50)],
    'B': [('A', 20), ('T', 1)],
    'T': []
}
cost, order = solve(test3, 'S', ['A', 'B'], 'T')
print("ordering matters")
print(f"  got: {cost} {order}  expected: 3 ['A', 'B']")



# relic is reachable but exit is not
test4 = {'S': [('R', 1)], 'R': [], 'T': []}
cost, order = solve(test4, 'S', ['R'], 'T')
print("no path to exit")
print(f"  got: {cost} {order}  expected: inf []")



# relic is completely disconnected from spawn
test5 = {'S': [('T', 2)], 'R': [('T', 1)], 'T': []}
cost, order = solve(test5, 'S', ['R'], 'T')
print("unreachable relic")
print(f"  got: {cost} {order}  expected: inf []")



# 4 relics in a chain, only one cheap ordering exists
test6 = {
    'S': [('D', 1), ('A', 10), ('B', 10), ('C', 10)],
    'D': [('C', 1), ('T', 100)],
    'C': [('A', 1), ('T', 100)],
    'A': [('B', 1), ('T', 100)],
    'B': [('T', 1)],
    'T': []
}
cost, order = solve(test6, 'S', ['A', 'B', 'C', 'D'], 'T')
print("4 relics chain")
print(f"  got: {cost} {order}  expected: 5 ['D', 'C', 'A', 'B']")
