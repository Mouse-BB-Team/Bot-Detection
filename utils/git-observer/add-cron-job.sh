#!/bin/bash

echo 0-59/$1 '* * * *' $2/git-observer-cron-job.sh $3 $2/$4 | crontab -