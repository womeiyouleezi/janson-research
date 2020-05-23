#!/bin/bash
#SBATCH -n 1
#SBATCH -N 1
#SBATCH -t 0-21:00
#SBATCH -p serial_requeue               #or could be shared
#SBATCH --mem=2000
#SBATCH -o dim4_n10000_output-1.txt	# use %j for jobid
#SBATCH -e dim4_n10000_errors-1.txt
#SBATCH --mail-type=ALL
#SBATCH --mail-user=junulee@college.harvard.edu
#SBATCH --open-mode=append
i=0
seed=1000
module load Anaconda3/5.0.1-fasrc02
source activate junulee_env1
while [ "$i" -lt "25" ]; do
        python ../gPRM_simulation_junulee.py 4 10000 1 $seed
        i=`expr $i + 1`
        seed=`expr $seed + 400`
done
# this is the 1st job for D=4, n=10000
