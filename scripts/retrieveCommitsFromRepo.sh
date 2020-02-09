#!/bin/bash

USAGE='''
	This script is used to retrieve all commits from a repository.
	It uses gitjson script.

	The output JSON file containing commits will be stored in a JSON file with the name of the repository
	
	Example :

	RUN : ./retrieveCommitsFromRepo.sh ~/Desktop/repositories/repository/to/analyse
	OUTPUT : analyse.json

'''
if [ $# -eq 1 ]
then
	echo "Retrieving commits from the repository $1"
	output_file_name=$(basename "$1")
	output_file_name+=".json"

	echo "Output will be stored in $output_file_name"

	./gitjson log --json=haeds --repo=$1 > $output_file_name
else
	echo "Give repository path as argument :\n RUN : ./retrieveCommitsFromRepo.sh ~/Desktop/repositories/repository/to/analyse"
fi
