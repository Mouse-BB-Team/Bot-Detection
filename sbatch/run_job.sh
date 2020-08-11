#!/bin/bash -l
username=$(whoami)
lastCommitHash=$(git rev-parse --short HEAD)
output_path="outputs"
if [ ! -d $output_path ]
then
  mkdir $output_path
fi
sbatch --job-name="$username|job:#$lastCommitHash" --output="$output_path/out:$username|#$lastCommitHash.txt" --error="$output_path/err:$username|#$lastCommitHash.txt" --export=username=$username,lastCommitHash=$lastCommitHash,output_path=$output_path sbatch_job_config.sh