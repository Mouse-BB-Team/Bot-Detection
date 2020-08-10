#!/bin/bash -l
lastCommitHash=$(git rev-parse --short HEAD)
username=$(whoami)

## Task titled: username + Commit Hash
#SBATCH -J "test:$username|#$lastCommitHash"

## Grant name
#SBATCH -A plgkamilkalis2020a

## Node count, 1 by default
#SBATCH -N 1

#SBATCH -ntasks-per-node=30

#SBATCH --cpus-per-task=24

## Job time
#SBATCH --time=00:10:00

## Partition
#SBATCH -p plgrid-testing

## Output files
#SBATCH --output="test_output_$username_#$lastCommitHash.txt"
#SBATCH --error="test_error_$username_#$lastCommitHash.txt"


module add plgrid/tools/python/3.8
module add plgrid/libs/tensorflow-gpu/2.2.0-python-3.8

cd $SLURM_SUBMIT_DIR
cd ..

pip install -r requirements.txt

python3 main.py
