import numpy as np
from scipy.spatial import KDTree
import matplotlib

from collections import defaultdict
from heapq import *

from gPRM_utils import SampleFree, Near, ShortestPath

##################################################

# Given relevant parameters, creates a class that can run gPRM over and 
# over, randomizing the V every time.
class gPRM:
    def __init__(self, n, D, x_init, x_goal):
        self.n = n
        self.D = D
        
        self.x_init = x_init
        self.x_goal = x_goal
        self.true_distance = np.linalg.norm(x_init - x_goal)
        
        self.V = None
        self.KD_array = []
        self.E = None
        
        self.length = 0
        self.path = None
        
    # Gets sample V from free space and constructs two KD trees for querying    
    def sample_points(self):
        
        # clear memory
        del(self.V)
        del(self.KD_array)
        
        self.V = SampleFree(self.n, self.D, self.x_init, self.x_goal)
        
        # construct KD trees
        KDT = KDTree(data=self.V)
        search_against = KDTree(data=self.V)
        
        self.KD_array = [KDT, search_against]
        
    # With constructed KD trees, query for a given radius, construct edge set,
    # and run a shortest path algorithm
    def run_simulation(self, r_n):
        
        # clear memory
        del(self.E)
        
        # run query_ball_tree
        results = self.KD_array[0].query_ball_tree(other=self.KD_array[1], r=r_n)

        # construct edge set
        self.E = []
        for i in range(len(self.V)):
            for j in results[i]:
                if i == j:
                    continue
                # here, i and j are indices in V
                distance = np.linalg.norm(self.V[i] - self.V[j], ord=None)
                (self.E).append((i, j, distance))
        
        # shortest path algorithm
        self.length, self.path = ShortestPath(self.E, 0, 1+self.n)
        
    # The following are retrieval methods    
    def get_V(self):
        return self.V
    
    def get_KDTrees(self):
        return self.KD_array
    
    def get_E(self):
        return self.E
        
    def get_length(self):
        return self.length
    
    def get_true_distance(self):
        return self.true_distance
    
    def get_error(self):
        return np.abs(self.length - self.true_distance)
    
    def get_path(self):
        return self.path
        
    
    

