#!/bin/bash -l

## Grant name
#SBATCH -A plgcholdadyplomy

## Node count, 1 by default
#SBATCH -N 1

#SBATCH --cpus-per-task=24

#SBATCH --mem=5GB
#SBATCH --mem-per-cpu=5GB

## Job time
#SBATCH --time=01:00:00

## Partition
#SBATCH -p plgrid-testing
##SBATCH --gres=gpu


module add plgrid/tools/python/3.8
module add plgrid/libs/tensorflow-gpu/2.2.0-python-3.8
##module add plgrid/apps/cuda/10.1

cd $SLURM_SUBMIT_DIR
cd ../..

pip install -r requirements.txt

python3 main.py
