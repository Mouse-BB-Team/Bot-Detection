#!/bin/bash -l
username=$(whoami)
lastCommitHash=$(git rev-parse --short HEAD)
sbatch --job-name="test:$username|#$lastCommitHash" --output="test_output:$username|#$lastCommitHash.txt" --error="test_error:$username|#$lastCommitHash.txt" --export=username=$username,lastCommitHash=$lastCommitHash batch_test.sh