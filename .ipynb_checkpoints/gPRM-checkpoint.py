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
        self.E = Near(self.V, self.r_function(self.n, self.D))
        self.length = ShortestPath(self.E, 0, 1+self.n)
        
    def get_V(self):
        return self.V
    
    def get_E(self):
        return self.E
        
    def get_length(self):
        return self.length
    
    def get_error(self):
        return np.abs(self.length - self.true_distance)
        
    
    

