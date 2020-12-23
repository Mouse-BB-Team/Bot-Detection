#!/bin/bash -l

## Grant name
#SBATCH -A plgcholdadyplomy

## Node count, 1 by default
#SBATCH -N 1

#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=40GB

## Job time
#SBATCH --time=26:00:00

## Partition
#SBATCH -p plgrid-gpu
#SBATCH --gres=gpu:2


module add plgrid/tools/python/3.8
module add plgrid/libs/tensorflow-gpu/2.3.1-python-3.8
module add plgrid/apps/cuda/10.1

cd $SLURM_SUBMIT_DIR
cd ../..

pip install -r requirements.txt

python3 main.py -d "/net/archive/groups/plggpchdyplo/augmented_data/"
