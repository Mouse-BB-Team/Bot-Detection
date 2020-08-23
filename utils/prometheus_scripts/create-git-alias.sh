#!/bin/bash

create_alias()
{
  echo '[alias]
        deploy = "!f() { git push \"$1\" \"$2\"; utils/prometheus_scripts/./run-commit-execution.sh; }; f"' >> .git/config
}

while true; do
    read -p "Do you want to make git alias \"git deploy <remote> <branch>\" to pushing and running plgrid job in one commend? (y/n): " yn
    case $yn in
        [Yy]* ) create_alias; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done