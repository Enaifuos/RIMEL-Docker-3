import sys
import json
import os
import subprocess

def getDiffAddedLinesByCommit(SHA) :
	cmd = "git diff "
	cmd += SHA
	cmd += " | grep '^+'"
	output = subprocess.check_output(cmd, shell=True)

	return output


def createMapFileLines(listDiffString) :
	for 
			
	


def containsKeyword(diffLines, keywordsList) :
	addition = []
	usage = []
	for string in diffLines :
		for keyword in keywordsList :
			if string.find(keyword) > -1 :
				addition.append(string)
	return addition


if __name__ == '__main__':

	if ( len(sys.argv) < 2 ) :
		print("Give commits JSON file and Output file to store :\n python3 myscript.py keyword1,keyword2")
	else :
		#print(getFileAndLines('446e3ddf945b9be5c04f954f97408faac2d22336'))	
#		keywords = sys.argv[1].split(',')

#		print("__keywords", keywords)


		diff = getDiffAddedLinesByCommit('2209ecdc4452b7f9fc4e350b8f1b08fd5e24afb7')
		print(diff)


#		print("\n\n___________\n\n")

#		print(containsKeyword(diff, keywords))
