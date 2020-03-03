# Code Quality Assistant
# input : file or directory to run code analysis on


# output: hmtl website to analyze code analysis results found ./code-quality-assistant directory

#from AnalysisScript import runAnalysis
#from AnalysisStatistics import nb_files
#from AnalysisStatistics import getStatisticsFromAllFiles
#from AnalysisStatistics import getDiffPercentages
from release_scripts import get_nb_of_ev
from prepareCommitsToCheckout import getListOfPreviousOrNextSHA

import os
import json
import git

print("---------------------------------------")
cwd = os.getcwd()
print("initial cwd : \n" + cwd)
print("---------------------------------------")



# to encapsulate
def getAllCommitsJSONFormat(repoDir):
    # get and set all commits of a project
    os.system("./retrieveCommitsFromRepo.sh " + repoDir + " thingsboardAllCommits.json")
    with open("thingsboardAllCommits.json", 'r') as f:
        return json.load(f)


def getAllEVfromRepo(repoDir):
    os.chdir(repoDir)
    allEV =  get_nb_of_ev.list_of_EV()
    os.chdir(cwd)
    return allEV

def getCommitsWhereKeywordsAppear(repoDir, keywordList):
    filteredCommits = {}
    for key in keywordList :
        g = git.cmd.Git(repoDir)
        filteredCommits[key] = (g.log(S=key, pretty="%h")).split('\n')
    return filteredCommits

def getPreviousCommit(allCommits, filteredCommits):
        print(getListOfPreviousOrNextSHA(allCommits, filteredCommits))

def filterFilesContainingKeyword(fileList, keyword, repoDir):
    filterFiles = []
    for file in fileList:
        with open(repoDir + "/" + file, 'r') as myfile:
            data = myfile.read()
            if (keyword in data):
                filterFiles.append(file)

    return filterFiles

# os.system("git log -S '"+key+"'")

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




# allcommits = getAllCommitsJSONFormat("/home/passport/Repos/tmp/thingsboard")
# print(allcommits)

filteredCommits = getCommitsWhereKeywordsAppear("/home/passport/Repos/tmp/thingsboard", ["KAFKA", "DEVICE_LABEL_PROPERTY"])

print("-----------------------------------------------")
print("filtered commits where keywords appear  : \n" + str(filteredCommits))
print("-----------------------------------------------")


output = {}
#print(getAllEVfromRepo("~/Desktop/thingsboard/"))
for filteredCommit in filteredCommits :
    valueList = []
    listOfCommits = getListOfPreviousOrNextSHA(getAllCommitsJSONFormat("/home/passport/Repos/tmp/thingsboard"), filteredCommits[filteredCommit])

    for commit in listOfCommits :
        innerDict = {}
        innerDict["actual"] = commit
        innerDict["previous"] = listOfCommits[commit]
        valueList.append(innerDict)

    output[filteredCommit] = valueList

print("-----------------------------------------------")
print("printing output  : \n" + str(output))
print("-----------------------------------------------")




def getFilesAndMethodsModified(jsonEntry, repoDir):
    print("-----------------------------------------------")
    print("getFilesAndMethodsModified")
    print("repoDir : " + repoDir)
    print("-----------------------------------------------")
    for key in jsonEntry:
        print(key)
        for jsonObject in jsonEntry[key]:
            g = git.cmd.Git(repoDir)
            modifiedFiles = g.diff("--name-only",  jsonObject["previous"], jsonObject["actual"]).split("\n")
            print("modified files: " + str(modifiedFiles))
            filteredFileList = [el for el in modifiedFiles if ((".java" in el) or (".py" in el) or ((".js" in el) and not (".json" in el)))]
            g.checkout(jsonObject["actual"])
            filteredFileList2 = filterFilesContainingKeyword(filteredFileList, key, repoDir)
            print(filteredFileList2)
            g.checkout("master")

getFilesAndMethodsModified(output, "/home/passport/Repos/tmp/thingsboard")




#
#
# jsondata = runAnalysis('/home/passport/Repos/tmp/open-location-code/java/src')

# print(jsondata)
# print(getStatisticsFromAllFiles(jsondata))

# statisticsDict = {}
# statisticsDict['commit1'] = getStatisticsFromAllFiles(jsondata)
# statisticsDict['commit2'] = getStatisticsFromAllFiles(jsondata)
# getDiffPercentages(statisticsDict)

