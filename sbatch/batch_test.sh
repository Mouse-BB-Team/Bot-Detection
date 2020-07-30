#!/bin/bash

lastCommit=$(git rev-parse --short HEAD)
userName=$(whoami)

echo "$userName|#$lastCommit"
