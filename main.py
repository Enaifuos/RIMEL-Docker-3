import json
import os
import time

import git
import lizard

from scripts.AnalysisScript import runAnalysisFiles, runLizard
from scripts.AnalysisStatistics import getStatisticsFromAllFiles
from scripts.utils import getAllEVfromRepo, getCommitsWhereKeywordsAppear, getAllCommitsJSONFormat, getPreviousAndNext, \
    getFilesAndMethodsModified, startAnalysis, deleteEntriesWithEmptyFilesList, filterListByFilesThatExistsWithoutRepo, \
    getNlocNCCStats

print("---------------------------------------")
cwd = os.getcwd()
start_time = time.time()
print("initial cwd : \n" + cwd)
print("---------------------------------------")


#########################" ALGORITHME ###############################
# iterate over repos

    # for each repo in list of repo
        # checkout repo
        # get and set list of EV

    # for each EV
        # find : (usageCommit, previousCommit, [(file, method),...])

    # for each EV
        # checkout previousCommit and getAnalysis of methods before
        # checkout usageCommit and get Analysis of methods now
        # fill results in array

        # statistics?
#######################################################################


#REPO = "/Users/soufiane/Desktop/magma"
name = "openmrs-sdk.json"
REPO = "/home/passport/Repos/tmp/openmrs-sdk"


print(" 1/8  -  Get VE from Project")
EVs = getAllEVfromRepo(REPO)
print(EVs)
print("--- %s seconds ---" % (time.time() - start_time))

#EVs = ["ZOOKEEPER_URL"]

print(" 2/8  -  Get all commits in json format")
allCommitsJSONFormat = getAllCommitsJSONFormat(REPO, name)
print("--- %s seconds ---" % (time.time() - start_time))


print(" 3/8  -  Get commits where EV appears")
commitsWhereEVsAppears = getCommitsWhereKeywordsAppear(REPO, EVs)
print("--- %s seconds ---" % (time.time() - start_time))


print(" 4/8  -  Get previous and next of each filtered commit")
jsonPreviousNextCommit = getPreviousAndNext(allCommitsJSONFormat, commitsWhereEVsAppears)
print("--- %s seconds ---" % (time.time() - start_time))


print(" 5/8 -  Get files where EV where touched")
filesToAnalyze = getFilesAndMethodsModified(jsonPreviousNextCommit, REPO)
filteredFilesToAnalyze = deleteEntriesWithEmptyFilesList(filesToAnalyze)
print("--- %s seconds ---" % (time.time() - start_time))

with open("step5_"+name, 'w') as outfile:
    json.dump(filteredFilesToAnalyze, outfile)


print(" 6/8  -  Analysing code (complexity, nloc..)")

g = git.cmd.Git(REPO)


for key in filteredFilesToAnalyze:
    for jsonEntry in filteredFilesToAnalyze[key]:

        # checkout actual, recuperer les analyses de tout les fichiers en actual
        g.checkout(jsonEntry["actual"])
        fileListToAnalyze = []

        for file in jsonEntry["files"]:
            fileListToAnalyze.append(REPO + "/" +file)
            jsonEntry["actualAnalysis"] = runAnalysisFiles(REPO, fileListToAnalyze)

        # checkout actual, recuperer les analyses de tout les fichiers en actual
        g.checkout(jsonEntry["previous"])
        fileListToAnalyze = []
        existingFileList = filterListByFilesThatExistsWithoutRepo(REPO, jsonEntry["files"])

        jsonEntry["previousAnalysis"] = {}
        for file in existingFileList:
            fileListToAnalyze.append(REPO + "/" +file)
            jsonEntry["previousAnalysis"] = runAnalysisFiles(REPO, fileListToAnalyze)
        g.checkout(jsonEntry["previous"])

with open(name, 'w') as outfile:
    json.dump(filteredFilesToAnalyze, outfile)


print(" 7/8  -  Generating statistics")
print(filteredFilesToAnalyze)
print("zebi")
print(getNlocNCCStats(json.dumps(filteredFilesToAnalyze)))
print("--- %s seconds ---" % (time.time() - start_time))



'''
print(" 8/8  -  Plotting")
print("not implemented")
print("--- %s seconds ---" % (time.time() - start_time))


print("\n---------------------------------------------------")
print("--- %s total time ---" % (time.time() - start_time))
print("---------------------------------------------------")
'''
