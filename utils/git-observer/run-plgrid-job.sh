#!/bin/bash

slackHookURL=$(./json-parser.sh ../../config/slack-config.json hookURL)
lastCommitHash=$(git rev-parse --short HEAD)
currentUser=$(whoami)

# TODO: EXECUTE FUTURE JOB HERE

curl -X POST -H 'Content-type: application/json' --data '{"text":"Pending job: '\#"$lastCommitHash"' ('"$currentUser"')"}' "$slackHookURL"