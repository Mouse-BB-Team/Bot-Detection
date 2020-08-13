#!/bin/bash -l
username=$(whoami)
lastCommitHash=$(git rev-parse --short HEAD)
currDate=$(date "+%d.%m.%y|%H:%M:%S")
output_path="outputs"

if [ ! -d $output_path ]
then
	mkdir $output_path
fi

sbatch \
	--job-name="$username|#$lastCommitHash|$currDate" \
	--output="$output_path/out:$username|#$lastCommitHash|$currDate.txt" \
	--error="$output_path/err:$username|#$lastCommitHash|$currDate.txt" \
	--export=username=$username,lastCommitHash=$lastCommitHash,output_path=$output_path,currDate=$currDate \
	sbatch_job_config.sh

