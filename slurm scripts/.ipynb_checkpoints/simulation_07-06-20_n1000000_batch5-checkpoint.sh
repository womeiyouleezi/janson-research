#!/bin/bash
#SBATCH -n 1
#SBATCH -N 1
#SBATCH -t 0-18:00
#SBATCH -p serial_requeue               # or could be shared
#SBATCH --mem=9000
#SBATCH -o data/07-06-20/asymptotics-dim2_n1000000-5.out                # use %j for jobid
#SBATCH -e data/07-06-20/asymptotics-dim2_n1000000-5.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=junulee@college.harvard.edu
#SBATCH --open-mode=append
i=401
module load Anaconda3/5.0.1-fasrc02
source activate junulee_env1
while [ "$i" -lt "501" ]; do
        python ../asymptotics-2.py 2 1000000 $i
        i=`expr $i + 1`
done

# this is the fifth batch of 100 for D=2, n=1000000