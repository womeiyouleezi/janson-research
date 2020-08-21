import numpy as np
from scipy.spatial import KDTree
from scipy.stats import uniform, expon, poisson

import sys
import math
from collections import defaultdict
from heapq import *

import pickle

##################################################

# We compare the PRM algorithm in two dimensions to
# three heuristics we have previously worked with:
# (1) the angle minimizer, (2) the edge length
# maximizer within a given angle range, and (3) the
# length cos angle maximizer.

# r_n function
def r(n, D):
    return (n ** (-1/(2*D))) / 5
    # designed for n = 5 * 10^6
    
# theta_max function    
def theta_max(n, D):
    return math.pi / (0.5 * n ** (1/4))
    # designed for n = 5 * 10^6
    
########## auxiliary functions ##########    
    
# Typical Dijkstra implementation (thanks internet)
def dijkstra(edges, init, goal):
    
    # builds a adjacency list with edge weights (c)
    
    #g = defaultdict(list)
    #for l,r,c in edges:
    #    g[l].append((c,r))
    
    # jk edges is an adjacency list (see Near_PRM)
    g = edges

    # dist records the min value of each node in heap
    q, seen, dist = [(0,init,())], set(), {init: 0}
    while q:
        (cost,v1,path) = heappop(q)
        if v1 in seen: continue

        seen.add(v1)
        path += (v1,)
        if v1 == goal: return (cost, path)

        for v2, c in g.get(v1, ()):
            if v2 in seen: continue

            # not every edge will be calculated. The edge which can improve the value of node in heap will be useful
            if v2 not in dist or cost+c < dist[v2]:
                dist[v2] = cost+c
                heappush(q, (cost+c, v2, path))

    return (float('inf'), path)

# Creates random sample of n points (not including init and goal) -- poisson functionality added
def SampleFree(n, d, x_init, x_goal, distr='unif'):
    assert distr in {'unif', 'pois'}, "distr parameter must be one of the following: 'unif', 'pois'"
    
    # start with init point (index 0)
    V = [x_init]
    
    if distr is 'pois':
        num_points = np.random.poisson(lam=n)
    else:
        num_points = n
    
    for i in range(num_points):
        point = np.random.uniform(size=d)
        if (point[0]-0.5)**2 - 1.997 * (point[0]-0.5) * (point[1]-0.5) + (point[1]-0.5)**2 > 1/1800:
            continue
        V.append(point)
        
    # add the goal point (index n + 1)
    V.append(x_goal)
    
    return V

# For PRM, an adjacency list with distances is required
def Near_PRM(V, r_n):
    
    # Create a KD Tree first
    KDT = KDTree(data=V)
    
    # Create the KD Tree to search against
    search_against = KDTree(data=V)

    # run query_ball_tree
    results = KDT.query_ball_tree(other=search_against, r=r_n)
    
    # construct edge set
    
    #edges = []
    #for i in range(len(V)):
    #    for j in results[i]:
    #        if i == j:
    #            continue
    #        # here, i and j are indices in V
    #        distance = np.linalg.norm(V[i] - V[j], ord=None)
    #        edges.append((i, j, distance))
            
    edges = defaultdict(list)
    for i in range(len(V)):
        for j in results[i]:
            if i == j:
                continue
            else:
                edges[i].append((j, np.linalg.norm(V[i] - V[j])))
    
    return edges

########## graph traversal algorithms ##########

# PRM
def run_PRM(V, E):

    # shortest path algorithm
    distance, path_idxs = dijkstra(E, 0, len(V)-1)
    
    path_nodes = []
    for v in path_idxs:
        path_nodes.append(V[v])
    
    return path_nodes, distance

# Heuristic 1
def run_heuristic_1(V, E):
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
        candidates = np.take(V, np.array(E[piece]).T[0].astype(int), axis=0) 
        angles = []
        for p in candidates:
            vect_1 = p - V[piece]
            vect_2 = x_goal - V[piece]
            angle = math.atan2( vect_1[0]*vect_2[1] - vect_1[1]*vect_2[0], vect_1[0]*vect_2[0] + vect_1[1]*vect_2[1])
            angles.append(np.abs(angle))             # absolute angle in radians
        next_piece = np.array(E[piece]).T[0].astype(int)[np.array(angles).argmin()]
        if next_piece in visited:
            #print('failed')
            #print(next_piece)
            #print(visited)
            failure = True            # means we have already been to this node
        else:
            distance += np.linalg.norm(V[next_piece] - V[piece])
            visited.append(next_piece)
            piece = next_piece
            
    path_nodes = []
    for v in visited:
        path_nodes.append(V[v])
    
    if failure:
        return path_nodes, float('inf')
    
    else:
        return path_nodes, distance
    
# heuristic 2
def run_heuristic_2(V, E, theta_max):
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
        points_in_ball = np.array(E[piece]).T[0].astype(int)     # indices of all points in the ball around (X_t, Y_t)
        points_in_slice = []   # indices of all points such that angle displacement does not exceed theta_max
        
        if len(V)-1 in points_in_ball:
            next_piece = len(V)-1
            distance += np.linalg.norm(V[next_piece] - V[piece])
            visited.append(next_piece)
            piece = next_piece
            continue
        
        for p_idx in points_in_ball:
            vect_1 = V[p_idx] - V[piece]
            vect_2 = x_goal - V[piece]
            if np.arccos(np.dot(vect_1, vect_2) / (np.linalg.norm(vect_1) * np.linalg.norm(vect_2))) < theta_max:
                points_in_slice.append(p_idx)
                
        if len(points_in_slice) < 1:
            failure = True
            continue
        
        candidates = np.take(V, points_in_slice, axis=0)
        #print(len(candidates))
        edge_lengths = []
        for p in candidates:
            edge_lengths.append(np.linalg.norm(p - V[piece]))
        next_piece = points_in_slice[np.argmax(edge_lengths)]
        if next_piece in visited:
            #print('failed')
            #print(next_piece)
            #print(visited)
            failure = True            # means we have already been to this node
        else:
            distance += np.linalg.norm(V[next_piece] - V[piece])
            visited.append(next_piece)
            piece = next_piece
            
    path_nodes = []
    for v in visited:
        path_nodes.append(V[v])
    
    if failure:
        return path_nodes, float('inf')
    
    else:
        return path_nodes, distance
    
# heuristic 3
def run_heuristic_3(V, E):
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
        points_in_ball = np.array(E[piece]).T[0].astype(int)     # indices of all points in the ball around (X_t, Y_t)
        #costs_in_ball = (np.array(E[piece]).T)[1]      # costs of all edges starting from V[piece]
        
        if len(V)-1 in points_in_ball:
            next_piece = len(V)-1
            distance += np.linalg.norm(V[next_piece] - V[piece])
            visited.append(next_piece)
            piece = next_piece
            continue
        
        candidates = np.take(V, points_in_ball, axis=0)
        
        # optimizing term = R cos theta
        opt = []
        for p in candidates:
            vect_1 = p - V[piece]
            vect_2 = x_goal - V[piece]
            cos_theta = np.dot(vect_1, vect_2) / (np.linalg.norm(vect_1) * np.linalg.norm(vect_2))
            opt.append(np.linalg.norm(vect_1) * cos_theta)
            
        next_piece = points_in_ball[np.argmax(opt)]
        if next_piece in visited:
            #print('failed')
            #print(next_piece)
            #print(visited)
            failure = True            # means we have already been to this node
        else:
            distance += np.linalg.norm(V[next_piece] - V[piece])
            visited.append(next_piece)
            piece = next_piece
            
    path_nodes = []
    for v in visited:
        path_nodes.append(V[v])
    
    if failure:
        return path_nodes, float('inf')
    
    else:
        return path_nodes, distance       

########## script to run ##########

# probably will require < 18 hours to run

D = int(sys.argv[1])        # should be 2
n = int(sys.argv[2])        # should be 5 * 10^6
#radius = r(n, D)
s_ix=int(sys.argv[3])       # goes from 1 to 500

# seeding 
seed = int(D*n/5000) * (s_ix+1) + 1
np.random.seed(seed) 
    
# filename
date_string = '08-20-20/'
folder_name = 'path_points/'
filename = date_string+folder_name+str(s_ix)+'-dim'+str(D)+'-'+'n'+str(n)

# graph computation

x_init = np.array([0.1] * D)
x_goal = np.array([0.9] * D)

V = SampleFree(n, D, x_init, x_goal)
E = Near_PRM(V, r(n, D))

nodes_dijk, distance_dijk = run_PRM(V, E)
nodes_1, distance_1 = run_heuristic_1(V, E)
nodes_2, distance_2 = run_heuristic_2(V, E, theta_max(n, D))
nodes_3, distance_3 = run_heuristic_3(V, E)

# print distances in order, separated by spaces
print(distance_dijk, distance_1, distance_2, distance_3)

# pickle each set of nodes
f = open("data/"+filename+"_pathpoints.pkl","wb")
data = {0: nodes_dijk, 1: nodes_1, 2: nodes_2, 3: nodes_3}
pickle.dump(data, f)
f.close()
