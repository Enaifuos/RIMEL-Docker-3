#!/bin/bash

USAGE='''
	This script is used to retrieve all commits from a repository.
	It uses gitjson script.

	The output JSON file containing commits will be stored in a JSON file given in argument.
	
	Example :

	RUN : ./retrieveCommitsFromRepo.sh ~/Desktop/repositories/repository/to/analyse outputFileName.json
	OUTPUT : analyse.json

'''
if [ $# -eq 2 ]
then
	echo "Retrieving commits from the repository $1"
	echo "Output will be stored in $2"

	./scripts/gitjson log --json=haeds --repo=$1 > $2
else
	echo "Give repository path as argument :\n RUN : ./retrieveCommitsFromRepo.sh ~/Desktop/repositories/repository/to/analyse outputFileName.json"
fi
