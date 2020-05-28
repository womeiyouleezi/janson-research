#!/bin/bash
#SBATCH -n 1
#SBATCH -N 1
#SBATCH -t 0-03:00
#SBATCH -p serial_requeue               # or could be shared
#SBATCH --mem=2000
#SBATCH -o dim2_n100.out                # use %j for jobid
#SBATCH -e dim2_n100.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=junulee@college.harvard.edu
#SBATCH --open-mode=append
i=0
module load Anaconda3/5.0.1-fasrc02
source activate junulee_env1
while [ "$i" -lt "5" ]; do
        python ../gPRM_script-1.py 2 100 10 $i
        i=`expr $i + 1`
done