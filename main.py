import os
from scripts.utils import getAllEVfromRepo, getCommitsWhereKeywordsAppear, getAllCommitsJSONFormat, getPreviousAndNext, \
    getFilesAndMethodsModified

print("---------------------------------------")
cwd = os.getcwd()
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


REPO = "/home/passport/Repos/tmp/thingsboard"


# Get VE from Project
EVs = getAllEVfromRepo(REPO)
# print(EVs)

# Get all commits in json format
allCommitsJSONFormat = getAllCommitsJSONFormat(REPO, "thingsboard.json")
# print(allCommitsJSONFormat)

# Get commits where EV appears
commitsWhereEVsAppears = getCommitsWhereKeywordsAppear(REPO, ["kafka", "DEVICE_LABEL_PROPERTY"])
# print(commitsWhereEVsAppears)

# Get commits where EV appears
commitsWhereEVsAppears = getCommitsWhereKeywordsAppear(REPO, ["kafka", "DEVICE_LABEL_PROPERTY"])
# print(commitsWhereEVsAppears)

# Get previous and next of each filtered commit
jsonPreviousNextCommit = getPreviousAndNext(allCommitsJSONFormat, commitsWhereEVsAppears)
# print (jsonPreviousNextCommit)

# Get files where EV where touched
filesmodified = getFilesAndMethodsModified(jsonPreviousNextCommit, REPO)
print(filesmodified)

