import numpy as np
from scipy.spatial import KDTree
import matplotlib

from collections import defaultdict
from heapq import *

##################################################

# Typical implementation (thanks internet)
def dijkstra(edges, init, goal):
    g = defaultdict(list)
    for l,r,c in edges:
        g[l].append((c,r))

    # dist records the min value of each node in heap.
    q, seen, dist = [(0,init,())], set(), {init: 0}
    while q:
        (cost,v1,path) = heappop(q)
        if v1 in seen: continue

        seen.add(v1)
        path += (v1,)
        if v1 == goal: return (cost, path)

        for c, v2 in g.get(v1, ()):
            if v2 in seen: continue

            # Not every edge will be calculated. The edge which can improve the value of node in heap will be useful.
            if v2 not in dist or cost+c < dist[v2]:
                dist[v2] = cost+c
                heappush(q, (cost+c, v2, path))

    return float("inf")


# This will compute X_near for all vertices in V in one go
def Near(V, r_n):
    
    # Create a KD Tree first
    KDT = KDTree(data=V)
    
    # Create the KD Tree to search against
    search_against = KDTree(data=V)

    # run query_ball_tree
    results = KDT.query_ball_tree(other=search_against, r=r_n)
    
    # construct edge set
    edges = []
    for i in range(len(V)):
        for j in results[i]:
            if i == j:
                continue
            # here, i and j are indices in V
            distance = np.linalg.norm(V[i] - V[j], ord=None)
            edges.append((i, j, distance))
            
    return edges


# Creates random sample of n points (not including init and goal)
def SampleFree(n, d, x_init, x_goal, distr=None):
    
    # start with init point (index 0)
    V = [x_init]
    
    for i in range(n):
        
        # for now, only uniform sampling
        V.append(np.random.uniform(size=d))
        
    # add the goal point (index n + 1)
    V.append(x_goal)
    
    return V


# Uses Dijkstra's algorithm with the edges created from Near
def ShortestPath(edges, init, goal):
    output = dijkstra(edges, init, goal)
    #assert not isinstance(output, float)
    try:
        return output[0]
    except:
        if isinstance(output, float):
            print("Shortest path does not exist")
        else:
            print("An error occurred")
