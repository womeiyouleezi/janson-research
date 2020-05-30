import numpy as np
from scipy.spatial import KDTree
import matplotlib.pyplot as plt

import math
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
        
    # Visualization of the random graph in two dimensions
    def visualize_graph(self, r, simulation_index, show_edges='relevant', filename=None):
        assert show_edges in {'relevant', 'optimal', 'all'}, "show_edges needs one of the following paramters: 'relevant', 'optimal', 'all'"
        if filename is None:
            filename = str(simulation_index)
        
        # construct points, path points, and init points
        # points = np.array(self.V)
        path_points = np.vstack(self.V[ve] for ve in self.path[1:-1])
        init_points = np.array([self.x_init, self.x_goal])

        x, y = np.array(self.V).T 
        x_pp, y_pp = path_points.T
        x_ip, y_ip = init_points.T
        
        edges = []
        if show_edges=='optimal':
            # actually, do nothing here
            pass
        else:
            for e in self.E:
                # e[0] is the index for the tail, e[1] is the index for the head
                tail = e[0]
                head = e[1]
                if show_edges=='relevant':
                    if (tail not in self.path) and (head not in self.path):
                        continue
                edges.append(np.array([self.V[tail], self.V[head]]))
        edges = np.array(edges)
        
        path_edges = []
        for j in range(len(self.path)-1):
            path_edges.append(np.array([self.V[self.path[j]], self.V[self.path[j+1]]]))
        path_edges = np.array(path_edges)
        
        # plot points here
        plt.figure(figsize=(10,10))
        plt.margins(0)

        plt.scatter(x, y, s=7)
        plt.scatter(x_pp, y_pp, s=7, c='red')
        plt.scatter(x_ip, y_ip, s=20, c='gold')

        for edge in edges:
            xe, ye = edge.T
            plt.plot(xe, ye, 'c-', linewidth=1, alpha=0.075)
        for edge in path_edges:
            xs, ys = edge.T
            plt.plot(xs, ys, 'r-', linewidth=1)
        
        title = 'PRM output for D='+str(self.D)+', n='+str(self.n)+', r='+str(r)\
                  +'; Simulation '+str(simulation_index)+' - '+show_edges\
                  +'; Relative error: '+str(np.abs(self.length - self.true_distance) / self.true_distance)
        plt.title(title)
        plt.savefig(filename+'-'+show_edges+'.png')
        plt.close()
        
    def path_angle_scatterplot(self, simulation_index, filename=None):
        if filename is None:
            filename = 'Scatterplot-'+str(simulation_index)
        
        # construct x and y for scatterplot; x is path length, y is angle displacement
        x_scatter = []
        y_scatter = []
        for ix in range(len(self.path)-1):
            vect_1 = self.V[self.path[ix+1]] - self.V[self.path[ix]]
            vect_2 = self.x_goal - self.V[self.path[ix]]
            angle = math.atan2(vect_1[0]*vect_2[1] - vect_1[1]*vect_2[0], vect_1[0]*vect_2[0] + vect_1[1]*vect_2[1])
            x_scatter.append(np.linalg.norm(vect_1))
            y_scatter.append(angle)
            
        # plot the scatterplot
        plt.figure(figsize=(8,8))
        axes = plt.gca()
        axes.set_xlim([0,0.1])
        #axes.margins(y=0.01)

        plt.scatter(x_scatter, y_scatter, s=20, c='blue')
        plt.title('Signed Angle Displacement x Edge Length; Simulation '+str(simulation_index))
        plt.xlabel('path edge length')
        plt.ylabel('path edge signed angle displacement w.r.t x_goal')
        plt.savefig(filename+'.png')
        plt.close()
        
        return x_scatter, y_scatter
        
    # The following are retrieval methods    
    def get_D(self):
        return self.D
    
    def get_n(self):
        return self.n
    
    def get_init(self):
        return self.x_init, self.x_goal
        
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
        
    
    

