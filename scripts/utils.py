import os
import json
from os import path

import git

from scripts.AnalysisScript import analyze
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
    finalDict = {}
    for key in jsonEntry:
        finalDict[key] = []

        g = git.cmd.Git(repoDir)
        for jsonObject in jsonEntry[key]:
            modifiedFiles = g.diff("--name-only", jsonObject["previous"],  jsonObject["actual"]).split("\n")
            filteredFileList = [el for el in modifiedFiles if ((".java" in el) or (".py" in el) or ((".js" in el) and not (".json" in el)))]
            g.checkout(jsonObject["actual"])

            finalDict[key].append({"files": filterFilesContainingKeyword(filteredFileList, key, repoDir), "previous": jsonObject['previous'], "actual": jsonObject["actual"]})


            g.checkout("master")
            i = i +1

    return finalDict

def filterListByFilesThatExists(filelist, repo):
    print(filelist)
    filtered = []
    for file in filelist:
        if(path.exists(repo + "/" + file)):
            filtered.append(file)
    return filtered


def startAnalysis(jsonEntry, repoDir):
    g = git.cmd.Git(repoDir)
    for key in jsonEntry:
        for jsonBlob in jsonEntry[key]:
            g.checkout(jsonBlob["previous"])
            onlyexistingfiles = filterListByFilesThatExists(jsonBlob["files"], repoDir)
            print(onlyexistingfiles)
            res = analyze(repoDir, onlyexistingfiles)
            print(res)