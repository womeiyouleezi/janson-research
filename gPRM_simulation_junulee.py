import sys
import numpy as np

from gPRM import gPRM

# r function: (1/n * log n)^(1/d)
def r(num_points, dimension):
    return np.power(np.log(num_points) / num_points, 1 / dimension) 

# input should be D, n, num_simulations, random_seed

D = sys.argv[1]
n = sys.argv[2]
num_simulations = sys.arv[3]
np.random.seed(sys.argv[4])      # seeding

x_init = np.array([0.1] * D)
x_goal = np.array([0.9] * D)
true_distance = np.linalg.norm(x_init - x_goal)

G = gPRM(n, D, x_init, x_goal)

# the actual simulations
while i < (num_simulations):
    G.sample_points()
    G.run_simulation(r(n, D))
    
    # if the algorithm fails to return a path
    if G.get_length() < -0.5:
        continue
        
    relative_error = G.get_error() / true_distance
    print(relative_error)
                
    i += 1


