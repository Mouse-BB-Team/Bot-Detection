#!/bin/bash

git fetch

branchName=$1
scriptToRun=$2

pullResult=$(git pull origin $branchName)

if [[ $? -ne 0 ]]; then
    echo "fatal error"
    exit 127
fi

isAlreadyUpToDate=$(echo $pullResult | grep "Already up to date." | wc -l )

if [[ $isAlreadyUpToDate -eq 1 ]]; then
    echo "no new commits"
    exit 0
else
    echo "found new commit"
    sh $scriptToRun
fi