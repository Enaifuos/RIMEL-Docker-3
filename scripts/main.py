# Code Quality Assistant
# input : file or directory to run code analysis on


# output: hmtl website to analyze code analysis results found ./code-quality-assistant directory

from AnalysisScript import runAnalysis
from AnalysisStatistics import nb_files
from AnalysisStatistics import getStatisticsFromAllFiles
from AnalysisStatistics import getDiffPercentages
from release_scripts import get_nb_of_ev
from prepareCommitsToCheckout import getListOfPreviousOrNextSHA

import os
import json
import git

cwd = os.getcwd()
print(cwd)
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
        filteredCommits[key] = (g.log(S=key, pretty="%H")).split('\n')
    return filteredCommits

def getPreviousCommit(allCommits, filteredCommits):
        print(getListOfPreviousOrNextSHA(allCommits, filteredCommits))

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

filteredCommits = getCommitsWhereKeywordsAppear("/home/passport/Repos/tmp/thingsboard", ["DEVICE_LABEL_PROPERTY"])
print(getAllEVfromRepo("/home/passport/Repos/tmp/thingsboard"))
getListOfPreviousOrNextSHA(getAllCommitsJSONFormat("/home/passport/Repos/tmp/thingsboard"), filteredCommits)


#
#
# jsondata = runAnalysis('/home/passport/Repos/tmp/open-location-code/java/src')

# print(jsondata)
# print(getStatisticsFromAllFiles(jsondata))

# statisticsDict = {}
# statisticsDict['commit1'] = getStatisticsFromAllFiles(jsondata)
# statisticsDict['commit2'] = getStatisticsFromAllFiles(jsondata)
# getDiffPercentages(statisticsDict)

