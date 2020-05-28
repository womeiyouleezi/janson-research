import sys
import numpy as np

from gPRM import gPRM

# r function: (1/n * log n)^(1/d)
def r(num_points, dimension):
    return np.power(np.log(num_points) / num_points, 1 / dimension) 

# input should be D, n, r, random_seed

D = int(sys.argv[1])
n = int(sys.argv[2])
r = float(sys.arv[3])
#num_simulations = int(sys.argv[4])
seed=int(sys.argv[4])
np.random.seed(seed)      # seeding

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
        i += 1
        continue
        
    relative_error = G.get_error() / true_distance
    
    # to stdout
    print('Seed: '+str(seed))
    print(str(relative_error))
    
    # visuals
                
    i += 1


