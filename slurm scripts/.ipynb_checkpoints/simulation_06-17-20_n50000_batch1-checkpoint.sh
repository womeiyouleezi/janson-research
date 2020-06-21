#!/bin/bash
#SBATCH -n 1
#SBATCH -N 1
#SBATCH -t 0-18:00
#SBATCH -p serial_requeue               # or could be shared
#SBATCH --mem=7000
#SBATCH -o data/06-20-20/asymptotics-dim2_n50000-1.out                # use %j for jobid
#SBATCH -e data/06-20-20/asymptotics-dim2_n50000-1.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=junulee@college.harvard.edu
#SBATCH --open-mode=append
i=1
module load Anaconda3/5.0.1-fasrc02
source activate junulee_env1
while [ "$i" -lt "51" ]; do
        python ../asymptotics-1.py 2 50000 $i
        i=`expr $i + 1`
done

# this is the first batch of 100 for D=2, n=50000