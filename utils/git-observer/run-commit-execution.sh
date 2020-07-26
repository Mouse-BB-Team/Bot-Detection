#!/bin/bash

ssh "$PLG_USERNAME"@pro.cyfronet.pl 'cd ~/Bot-Detection && \
git checkout $OBSERVED_BRANCH && \
git pull origin $OBSERVED_BRANCH && \
./utils/git-observer/./run-plgrid-job.sh'