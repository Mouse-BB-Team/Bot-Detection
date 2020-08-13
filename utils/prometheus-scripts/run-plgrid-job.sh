#!/bin/bash

slackHookURL=$(./json-parser.sh ../../config/slack-config.json hookURL)
lastCommitHash=$(git rev-parse --short HEAD)
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

python3 ../slack_notifier/pending_job.py currentUser lastCommitHash
