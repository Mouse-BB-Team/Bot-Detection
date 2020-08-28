#!/bin/bash

projectDir="$(dirname "$(dirname "$(pwd)")")"
export PYTHONPATH=$PYTHONPATH:"$projectDir"

lastCommitHash=$(git rev-parse --short HEAD)
commitMsg=$(git log -1 --pretty=%B)
currentUser=$(whoami)
currDate=$(date "+%d.%m.%y|%H:%M:%S")
output_path="outputs"

if [ ! -d $output_path ]
then
	mkdir $output_path
fi

sbatch \
	--job-name="#$lastCommitHash" \
	--output="$output_path/out#$lastCommitHash|$currDate.txt" \
	--error="$output_path/err#$lastCommitHash|$currDate.txt" \
	--export=lastCommitHash="$lastCommitHash",output_path=$output_path,currDate="$currDate" \
	sbatch_job_config.sh

python3 ../notification_jobs/pending_job.py "$currentUser" "$lastCommitHash" "$commitMsg"
