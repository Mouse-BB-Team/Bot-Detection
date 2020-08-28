#!/bin/bash

ssh "$PLG_USERNAME"@pro.cyfronet.pl 'cd ~/Bot-Detection && \
git checkout $OBSERVED_BRANCH && \
git pull origin $OBSERVED_BRANCH && \
COMMIT_HASH=$(git rev-parse --short HEAD) && \
mkdir $RESULTS_PATH/$COMMIT_HASH && \
cp -r ~/Bot-Detection/ $RESULTS_PATH/$COMMIT_HASH/Bot-Detection/ && \
cd $RESULTS_PATH/$COMMIT_HASH/Bot-Detection/utils/prometheus_scripts && \
./run-plgrid-job.sh $RESULTS_PATH/$COMMIT_HASH'