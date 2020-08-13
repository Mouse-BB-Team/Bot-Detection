#!/bin/bash -l

## Grant name
#SBATCH -A plgcholdadyplomy

## Node count, 1 by default
#SBATCH -N 1

#SBATCH --cpus-per-task=24

## Job time
#SBATCH --time=00:10:00

## Partition
#SBATCH -p plgrid-testing
##SBATCH --gres=gpu


module add plgrid/tools/python/3.8
module add plgrid/libs/tensorflow-gpu/2.2.0-python-3.8

cd $SLURM_SUBMIT_DIR
cd ..

pip install -r requirements.txt

python3 main.py