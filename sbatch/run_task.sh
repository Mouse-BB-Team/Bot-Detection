#!/bin/bash -l
lastCommitHash=$(git rev-parse --short HEAD)
username=$(whoami)

## Task titled: username + Commit Hash
#SBATCH -J "$username|#$lastCommitHash"

## Grant name
#SBATCH -A plgcholdadyplomy

## Node count, 1 by default
#SBATCH -N 1

#SBATCH -ntasks-per-node=30

#SBATCH --cpus-per-task=24

## Job time
#SBATCH --time=1:00:00

## Partition
#SBATCH -p plgrid-gpu
#SBATCH --gres=gpu

## Output files
#SBATCH --output="output_$username_#$lastCommitHash.txt"
#SBATCH --error="error_$username_#$lastCommitHash.txt"


module add plgrid/tools/python/3.8
module add plgrid/libs/tensorflow-gpu/2.2.0-python-3.8

#python3 ../main_script.py
