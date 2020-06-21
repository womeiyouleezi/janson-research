import numpy as np
from scipy.spatial import KDTree
import sys
import math

##################################################

# Using the graph heuristic of choosing the next node as the 
# vertex with the smallest (signed) cosine distance from the 
# straight-line path, we revise our graph utility functions.

# r_n function
def r(n, D):
    return n ** (-1/(2*D))

# Creates random sample of n points (not including init and goal)
def SampleFree(n, d, x_init, x_goal, distr='unif'):
    assert distr in {'unif', 'pois'}, "distr parameter must be one of the following: 'unif', 'pois'"
    
    # start with init point (index 0)
    V = [x_init]
    
    for i in range(n):
        
        if distr is 'unif':
            V.append(np.random.uniform(size=d))
        else:
            pass       # later functionality for poisson process sampling
        
    # add the goal point (index n + 1)
    V.append(x_goal)
    
    return V

# Creates adjacency list, no need for also storing their distances
def Near(V, r_n):
    
    # Create a KD Tree first
    KDT = KDTree(data=V)
    
    # Create the KD Tree to search against
    search_against = KDTree(data=V)

    # run query_ball_tree; returns list of lists
    results = KDT.query_ball_tree(other=search_against, r=r_n)
    
    # for vertex indexed by i, results[i] contains all indices j such that dist(v[i],v[j]) < r
    edges = [None] * len(V)
    for i in range(len(V)):
        edges[i] = []
        for j in results[i]:
            if i != j:
                edges[i].append(j)
            
    return edges

# Afore-mentioned graph heuristic
def path_algorithm(V, E):
    # V is the vertex set, E is the output of the KDT function (both numpy arrays)
    x_init = V[0]
    x_goal = V[-1]
    
    # tracks where we've been (array of indices)
    piece = 0
    visited = [0]
    distance = 0
    
    # boolean indicator of something going wrong, e.g. no further point or repeat node
    failure = False
    #print((failure is False) and (piece != len(V)-1))
    
    while (failure is False) and (piece != len(V)-1):
        candidates = np.take(V, np.array(E[piece]), axis=0)
        angles = []
        for p in candidates:
            vect_1 = p - V[piece]
            vect_2 = x_goal - V[piece]
            angle = math.atan2( vect_1[0]*vect_2[1] - vect_1[1]*vect_2[0], vect_1[0]*vect_2[0] + vect_1[1]*vect_2[1])
            angles.append(np.abs(angle))             # absolute angle in radians
        next_piece = E[piece][np.array(angles).argmin()]
        if next_piece in visited:
            #print('failed')
            #print(next_piece)
            #print(visited)
            failure = True            # means we have already been to this node
        else:
            distance += np.linalg.norm(V[next_piece] - V[piece])
            visited.append(next_piece)
            piece = next_piece
            
    if failure:
        return float('inf'), None
    
    else:
        distance -= np.linalg.norm(V[visited[-1]] - V[visited[-2]])
        return distance, visited
    
# start of script

D = int(sys.argv[1])
n = int(sys.argv[2])
radius = r(n, D)
s_ix=int(sys.argv[3])

# seeding 
seed = int(D*n) * (s_ix+1)
np.random.seed(seed) 

x_init = np.array([0.1] * D)
x_goal = np.array([0.9] * D)
true_distance = np.linalg.norm(x_init - x_goal)

V = np.array(SampleFree(n, D, x_init, x_goal))
E = np.array(Near(V, r(n, D)))

d, path = path_algorithm(V, E)

print(str(d)+' '+str(len(path)-1))
# prints the distance (excluding the last edge to goal) and the number of edges (T_n + 1)
