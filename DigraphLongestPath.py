import sys
from collections import defaultdict

# Loads the file given as the command line argument. Assumes the file is in
# DIMACS graph format. Assumes nodes are indexed increasingly from 1 to n.
f = open(sys.argv[1], 'r')
linez = f.readlines()
numbers = range(1, int(linez.pop(0).split()[2]) + 1)
edges = map(lambda w: map(int, w.split()[1:3]), linez)

# Create dictionaries which contain the outgoing/incoming edged of each node
outgoing, incoming = defaultdict(list), defaultdict(list)
for k, v in map(tuple, edges):
    outgoing[k].append(v)
    incoming[v].append(k)

# Get source nodes (nodes which have only outgoing edges)
sources = filter(lambda x: len(incoming[x]) == 0, numbers)

# Recursively examine the longest paths under each node. TODO: iterative?
def examine(route, number):
    if number in route:
        raise Exception("cyclic")
    route.append(number)
    future_routes = [ route ]
    future_routes.append(map((lambda i: examine(route[:], i)), outgoing[number]))
    return max(future_routes, key=len)

# Examine each source node for the longest path starting from that node and print it
try:
    print max(map((lambda i: examine([], i)), sources), key=len)
except: # TODO: more specific error handling
    print 'cyclic'
