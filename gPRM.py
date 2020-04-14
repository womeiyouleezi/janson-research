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
    def __init__(self, n, D, r_function, x_init, x_goal):
        self.n = n
        self.D = D
        self.r_function = r_function
        
        self.x_init = x_init
        self.x_goal = x_goal
        self.true_distance = np.linalg.norm(x_init - x_goal)
        
        self.V = None
        self.E = None
        self.length = 0
        self.path = None
        
    def run_iteration(self):
        
        # clear memory
        del(self.V)
        del(self.E)
        
        self.V = SampleFree(self.n, self.D, self.x_init, self.x_goal)
        self.E = Near(self.V, self.r_function(n))
        self.length = ShortestPath(self.E, 0, n+1)
        
    def return_V(self):
        return self.V
    
    def return_E(self):
        return self.E
        
    def return_length(self):
        return self.length
        
    
    

