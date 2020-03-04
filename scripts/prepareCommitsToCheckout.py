import sys
import json
import copy

'''
	this method returns a list of filtered commits SHA
	loadedJSON is a JSON file loaded from filtered commits
'''
def getAllFilteredSHA(loadedJSON) :
	filteredSHA=[]
	for key in loadedJSON:
		filteredSHA.append(loadedJSON[key])

	return filteredSHA

'''
	this method returns a dictionary that associate to each commit from the filtered commits, 
	the previous (or the next) one in order to checkout it to compare complexity.
	It associates only one previous commit to each filtered commit.
	The number of previous commits to save should be passed in argument, in a next version of this method.


	There is a commented line (elif) which replaced by (if) : the elif statement will prevent associating a filtered commit to another filtered commit.
	So the filtered commits list may not be empty at the end.
	The if statement allows us to evenutally associate a filtered commit to another filtered one.

	This method raises an Exception if there is at least one filtered commit which is not associated to another commit.

	EVENTUAL BUG : IF THE FIRST COMMIT BELONGS TO THE FILTERED COMMITS, THIS METHOD SUCKS !!!
'''
def getListOfPreviousOrNextSHA(allCommits, filteredSHA, previous=True) :

	takePreviousBoolean = False
	result = {}
	print("$$$$$previous", previous)
	for key in allCommits:
		if len(filteredSHA) > 0 :

			if takePreviousBoolean :
				if previous :  # we want the previous commits
					result[filteredSHA[0]] = key["sha"]
				else : # we want the next commits
					result[filteredSHA[0]] = allCommits[allCommits.index(key)-2]["sha"]

				filteredSHA.remove(filteredSHA[0])
				takePreviousBoolean = False

			#elif key["sha"] == filteredSHA[0] :
			if len(filteredSHA) > 0 and key["sha"] == filteredSHA[0] :
				takePreviousBoolean = True
		else :
			break

	print(filteredSHA)


	return result
	

'''
	this method creates a list of tuples. A tuple is (sha, previousSHA, nextSHA)
'''
def createDictionaryOfPreviousAndNextCommits(previousList, nextList) :
	# we suppose that previous and next list have the same keys (same length)
	if previousList.keys() != nextList.keys() :
		raise Exception("ERROR IN createTupleOfPreviousAndNextCommits() : previous and next lists have not the same keys length !")

	shaDictionary = {}
	for sha in previousList :
		shaDictionary[sha] = (previousList[sha], nextList[sha])

	return shaDictionary


if ( len(sys.argv) < 4 ) :
	print("Give commits JSON file and Output file to store :\n python3 prepareCommitsToCheckout.py ../jsons/allCommits ../jsons/filteredCommits.json outputFileName.JSON")
else :
	allCommitsFile = sys.argv[1]
	filteredCommitsFile = sys.argv[2]
	outputFile = sys.argv[3]

	# read filtered commits file 
	with open(filteredCommitsFile, 'r') as f :
		filteredJSON = json.load(f)

	# read all commits file 
	with open(allCommitsFile, 'r') as f :
		allCommitsJSON = json.load(f)

	# extract a list of SHA from filtered commits
	filteredSHA=getAllFilteredSHA(filteredJSON)

	# deep copy of filteredSHA in order to use it to retrieve previous and next commits
	filteredSHA_deepCopy = copy.deepcopy(filteredSHA)

	# associate to each filtered commit SHA, the previous and the next commit's SHA
	previousCommits = getListOfPreviousOrNextSHA(allCommitsJSON, filteredSHA, False)
	nextCommits = getListOfPreviousOrNextSHA(allCommitsJSON, filteredSHA_deepCopy, True)

	# create dictionary {SHA : (previousSHA, nextSHA)}
	dictionary = createDictionaryOfPreviousAndNextCommits(previousCommits, nextCommits)

	# write output in JSON file
	with open(outputFile, 'w') as outputFileName:
		json.dump(dictionary, outputFileName)

	