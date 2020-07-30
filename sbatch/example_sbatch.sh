
#!/bin/bash
#SBATCH -J
#SBATCH --time=1:00:00
#SBATCH --gres=gpu:1
#SBATCH -A grant012gpu
#SBATCH -p plgrid-gpu
#SBATCH --output=\"_output.txt\"
#SBATCH --error=\"_error.txt\"
date
module add plgrid/apps/mumax/3.9.3
mumax3
date