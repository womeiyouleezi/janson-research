#!/bin/bash
#SBATCH -n 1
#SBATCH -N 1
#SBATCH -t 0-20:00
#SBATCH -p serial_requeue               # or could be shared
#SBATCH --mem=10000
#SBATCH -o data/08-20-20/asymptotics-dim2_n5000000-3.out                # use %j for jobid
#SBATCH -e data/08-20-20/asymptotics-dim2_n5000000-3.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=junulee@college.harvard.edu
#SBATCH --open-mode=append
i=151
module load Anaconda3/5.0.1-fasrc02
source activate junulee_env1
while [ "$i" -lt "201" ]; do
        python ../heuristic_comparison-v1.py 2 5000000 $i
        i=`expr $i + 1`
done

# this is the 4th batch of 50 for D=2, n=5000000