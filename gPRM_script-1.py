# This is a script to run simulations using the gPRM module for two objectives:
# (1) to gain data of the relative error for simulations by choosing n, D, and
# setting r to be 0.1, and
# (2) to visualize the way PRM works in D=2 by showing the graph and any 
# auxiliary scatterplots.
# Note: throughout this script, D is going to equal 2.

import sys
import numpy as np
import math

from gPRM import gPRM

# input should be D, n, r, simulation_index
# simulation_index starts at 0

D = int(sys.argv[1])
n = int(sys.argv[2])
r = 0.1
s_ix=int(sys.argv[4])

# seeding 
seed = int(D*n) * (s_ix+1)
np.random.seed(seed)      

# filename should be dim-n-s_ix
filename = str(s_ix)+'-dim'+str(D)+'-'+'n'+str(n)

x_init = np.array([0.1] * D)
x_goal = np.array([0.9] * D)
true_distance = np.linalg.norm(x_init - x_goal)

G = gPRM(n, D, x_init, x_goal)

# the actual simulations
i = 0
while i < 1:
    G.sample_points()
    G.run_simulation(r)
    
    # if the algorithm fails to return a path
    if G.get_length() < -0.5:
        # delete the next two lines if you want to "reroll"
        print(float('inf'))
        i += 1
        continue
        
    relative_error = G.get_error() / true_distance
    
    # to stdout
    print(str(relative_error))
    
    # visuals
    G.visualize_graph(r, s_ix, show_edges='relevant', filename='graphs/'+filename)
    #G.visualize_graph(r, s_ix, show_edges='all', filename='graphs/'+filename)
    G.path_angle_scatterplot(s_ix, filename='plots/'+filename)
                
    i += 1