#!/bin/bash
#SBATCH -n 1
#SBATCH -N 1
#SBATCH -t 2-00:00
#SBATCH -p shared               # or could be shared
#SBATCH --mem=110000
#SBATCH -o data/5-29-20/path_data-dim2_n100000-1.out                # use %j for jobid
#SBATCH -e data/5-29-20/path_data-dim2_n100000-1.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=junulee@college.harvard.edu
#SBATCH --open-mode=append
i=1
module load Anaconda3/5.0.1-fasrc02
source activate junulee_env1
while [ "$i" -lt "11" ]; do
        python ../gPRM_script-2.py 2 100000 10 $i
        i=`expr $i + 1`
done
# this is the first batch of 10 for D=2, n=100000