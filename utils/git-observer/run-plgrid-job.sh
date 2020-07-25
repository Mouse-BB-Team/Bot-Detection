#!/bin/bash

lastCommitHash=$(git rev-parse --short HEAD)

curl -X POST -H 'Content-type: application/json' --data '{"text":"Starting job for: '\#$lastCommitHash'"}' https://hooks.slack.com/services/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
