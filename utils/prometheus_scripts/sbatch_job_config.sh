#!/bin/bash -l

## Grant name
#SBATCH -A plgcholdadyplomy

## Node count, 1 by default
#SBATCH -N 2

##SBATCH --cpus-per-task=24

## Job time
#SBATCH --time=01:00:00

## Partition
#SBATCH -p plgrid-gpu
#SBATCH --gres=gpu:3


module add plgrid/tools/python/3.8
module add plgrid/libs/tensorflow-gpu/2.2.0-python-3.8

cd $SLURM_SUBMIT_DIR
cd ../..

pip install -r requirements.txt

python3 main.py
