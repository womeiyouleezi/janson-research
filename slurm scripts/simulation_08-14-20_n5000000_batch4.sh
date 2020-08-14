#!/bin/bash
#SBATCH -n 1
#SBATCH -N 1
#SBATCH -t 0-24:00
#SBATCH -p serial_requeue               # or could be shared
#SBATCH --mem=10000
#SBATCH -o data/08-14-20/asymptotics-dim2_n5000000-4.out                # use %j for jobid
#SBATCH -e data/08-14-20/asymptotics-dim2_n5000000-4.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=junulee@college.harvard.edu
#SBATCH --open-mode=append
i=301
module load Anaconda3/5.0.1-fasrc02
source activate junulee_env1
while [ "$i" -lt "401" ]; do
        python ../asymptotics-4.py 2 5000000 $i
        i=`expr $i + 1`
done

# this is the 4th batch of 100 for D=2, n=5000000