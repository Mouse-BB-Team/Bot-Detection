#!/bin/bash
lastCommitHash=$(git rev-parse --short HEAD)
username=$(whoami)

## Task titled: username + Commit Hash
#SBATCH -J "$username|#$lastCommitHash"

## Grant name
#SBATCH -A plgcholdadyplomy

## /** TODO: 

## Node count, 1 by default
#SBATCH -N 1

## Task per node – since for now I think we would go into multithreaded approach, I suggest making it default 1
#SBATCH --ntasks-per-node=1

## Here we would allocate number of cores for our threads
#SBATCH --cpus-per-task=5

## TODO */

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

#python3 main_script.py
