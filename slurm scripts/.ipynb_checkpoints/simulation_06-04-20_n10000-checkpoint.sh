#!/bin/bash
#SBATCH -n 1
#SBATCH -N 1
#SBATCH -t 0-18:00
#SBATCH -p serial_requeue               # or could be shared
#SBATCH --mem=4000
#SBATCH -o data/06-04-20/path_data-dim2_n10000.out                # use %j for jobid
#SBATCH -e data/06-04-20/path_data-dim2_n10000.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=junulee@college.harvard.edu
#SBATCH --open-mode=append
i=1
module load Anaconda3/5.0.1-fasrc02
source activate junulee_env1
while [ "$i" -lt "101" ]; do
        python ../gPRM_script-3.py 2 10000 $i
        i=`expr $i + 1`
done