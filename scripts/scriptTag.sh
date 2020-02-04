#!/bin/sh

#Ce script récupère l identifiant de commits par tag
#Il produit un fichier json {"tag":"id du commit du tag"}
#RUN : Il prend en paramètre le path vers le repository github à analyser
#Example RUN : ./scriptTag.sh ~/Desktop/repositories/repository/to/analyse

if [ $# -eq 1 ]
then
	
	rimelScriptsPath=$(pwd)	
	echo "moving to $1"
	cd $1

	jsonContent="{"
	for i in $(git tag); do
		jsonContent+="\""
		jsonContent+="$i"
		jsonContent+="\":\""
		jsonContent+=$(git show $i | grep commit | cut -d " " -f2)
		jsonContent+="\""
		jsonContent+=",\n"
	done
	jsonContent=${jsonContent%",\n"};
	jsonContent+="}"
	
	echo "moving back to $rimelScriptsPath"
	cd $rimelScriptsPath

	echo "creating empty json file.."
	touch tags.json
	echo $jsonContent > tags.json
	echo "file tags.json has been created"

else
	echo "Give repository path as argument :\n ./scriptTag ~/Desktop/repositories/myRepo"
fi