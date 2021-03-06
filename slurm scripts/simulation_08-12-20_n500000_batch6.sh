#!/bin/bash
#SBATCH -n 1
#SBATCH -N 1
#SBATCH -t 0-18:00
#SBATCH -p serial_requeue               # or could be shared
#SBATCH --mem=9000
#SBATCH -o data/07-06-20/asymptotics-dim2_n500000-6.out                # use %j for jobid
#SBATCH -e data/07-06-20/asymptotics-dim2_n500000-6.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=junulee@college.harvard.edu
#SBATCH --open-mode=append
i=501
module load Anaconda3/5.0.1-fasrc02
source activate junulee_env1
while [ "$i" -lt "601" ]; do
        python ../asymptotics-3.py 2 500000 $i
        i=`expr $i + 1`
done

# this is the sixth batch of 100 for D=2, n=500000