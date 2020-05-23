#!/bin/bash
#SBATCH -n 1
#SBATCH -N 1
#SBATCH -t 0-00:20
#SBATCH -p serial_requeue 		#or could be shared
#SBATCH --mem=200
#SBATCH -o my_test_output_%j-1.out
#SBATCH -e my_test_errors_%j-1.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=junulee@college.harvard.edu
#SBATCH --open-mode=append
i=0
seed=1000
module load Anaconda3/5.0.1-fasrc02
source activate junulee_env1
while [ "$i" -lt "5" ]; do
	python ../gPRM_simulation_junulee.py 2 1000 1 $seed
	i=`expr $i + 1`
	seed=`expr $seed + 1000`
done
