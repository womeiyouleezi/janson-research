#!/bin/bash
#SBATCH -n 1
#SBATCH -N 1
#SBATCH -t 0-03:00
#SBATCH -p serial_requeue               # or could be shared
#SBATCH --mem=3000
#SBATCH -o data/06-04-20/path_data-dim2_n1000.out                # use %j for jobid
#SBATCH -e data/06-04-20/path_data-dim2_n1000.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=junulee@college.harvard.edu
#SBATCH --open-mode=append
i=1
module load Anaconda3/5.0.1-fasrc02
source activate junulee_env1
while [ "$i" -lt "101" ]; do
        python ../gPRM_script-3.py 2 1000 $i
        i=`expr $i + 1`
done