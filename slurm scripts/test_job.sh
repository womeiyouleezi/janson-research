#!/bin/bash
#SBATCH -n 1
#SBATCH -N 1
#SBATCH -t 0-00:15
#SBATCH -p serial_requeue
#SBATCH --mem=200
#SBATCH -o my_test_output_%j.out
#SBATCH -e my_test_errors_%j.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=junulee@college.harvard.edu
module load Anaconda3/5.0.1-fasrc02
source activate junulee_env1
python ../gPRM_simulation_junulee.py 2 100 20 7
 
