#!/bin/bash
#SBATCH -n 1
#SBATCH -N 1
#SBATCH -t 0-18:00
#SBATCH -p serial_requeue               # or could be shared
#SBATCH --mem=3500
#SBATCH -o data/dim2_n10000.out                # use %j for jobid
#SBATCH -e data/dim2_n10000.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=junulee@college.harvard.edu
#SBATCH --open-mode=append
i=0
module load Anaconda3/5.0.1-fasrc02
source activate junulee_env1
while [ "$i" -lt "50" ]; do
        python ../gPRM_script-1.py 2 10000 10 $i
        i=`expr $i + 1`
done
