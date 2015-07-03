#!/bin/bash

printf "\n###############################################\n"
date --iso=s &&
printf "\nunit tests:\n" && nosetests &&
printf "\npep8:\n" && pep8 $(find . -iname '*.py') && printf "\nOK\n"

