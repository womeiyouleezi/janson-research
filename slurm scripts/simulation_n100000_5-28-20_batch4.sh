#!/bin/bash
#SBATCH -n 1
#SBATCH -N 1
#SBATCH -t 2-00:00
#SBATCH -p serial_requeue               # or could be shared
#SBATCH --mem=15000
#SBATCH -o data/dim2_n100000-4.out                # use %j for jobid
#SBATCH -e data/dim2_n100000-4.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=junulee@college.harvard.edu
#SBATCH --open-mode=append
i=31
module load Anaconda3/5.0.1-fasrc02
source activate junulee_env1
while [ "$i" -lt "41" ]; do
        python ../gPRM_script-1.py 2 100000 10 $i
        i=`expr $i + 1`
done
# this is the fourth batch of 10 for D=2, n=100000
