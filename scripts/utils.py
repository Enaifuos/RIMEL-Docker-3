import os
import json
import git

from scripts.prepareCommitsToCheckout import getListOfPreviousOrNextSHA

cwd = os.getcwd()

# to encapsulate
from scripts.release_scripts import get_nb_of_ev


def getAllCommitsJSONFormat(repoDir, outputJson):
    # get and set all commits of a project
    os.system("./scripts/retrieveCommitsFromRepo.sh " + repoDir + " " + outputJson)
    with open(outputJson, 'r') as f:
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



def filterFilesContainingKeyword(fileList, keyword, repoDir):
    filterFiles = []
    for file in fileList:
        try:
            with open(repoDir + "/" + file, 'r') as myfile:

                data = myfile.read()
                if (keyword in data):
                    filterFiles.append(file)
        except FileNotFoundError:
                pass


    return filterFiles


def getPreviousAndNext(allCommits, CommitsContainsEV):
    output = {}
    for filteredCommit in CommitsContainsEV:
        valueList = []
        listOfCommits = getListOfPreviousOrNextSHA(allCommits, CommitsContainsEV[filteredCommit], True)

        for commit in listOfCommits:
            innerDict = {}
            innerDict["actual"] = commit
            innerDict["previous"] = listOfCommits[commit]
            valueList.append(innerDict)

        output[filteredCommit] = valueList
    return output


def getFilesAndMethodsModified(jsonEntry, repoDir):
    i = 1
    finalList = {}
    for key in jsonEntry:
        finalList[key] = []
        print(key)
        for jsonObject in jsonEntry[key]:
            g = git.cmd.Git(repoDir)
            modifiedFiles = g.diff("--name-only", jsonObject["previous"],  jsonObject["actual"]).split("\n")
            filteredFileList = [el for el in modifiedFiles if ((".java" in el) or (".py" in el) or ((".js" in el) and not (".json" in el)))]
            g.checkout(jsonObject["actual"])

            finalList[key] += filterFilesContainingKeyword(filteredFileList, key, repoDir)


            g.checkout("master")
            i = i +1

    print(finalList)


def getFilesAndMethodsModified(jsonEntry, repoDir):
    i = 1

    finalList = {}
    for key in jsonEntry:
        finalList[key] = []
        print(key)
        for jsonObject in jsonEntry[key]:
            g = git.cmd.Git(repoDir)
            modifiedFiles = g.diff("--name-only", jsonObject["previous"],  jsonObject["actual"]).split("\n")
            filteredFileList = [el for el in modifiedFiles if ((".java" in el) or (".py" in el) or ((".js" in el) and not (".json" in el)))]
            g.checkout(jsonObject["actual"])

            finalList[key] += filterFilesContainingKeyword(filteredFileList, key, repoDir)


            g.checkout("master")
            i = i +1
    return finalList
