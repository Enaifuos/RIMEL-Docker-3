import os
import time


from scripts.utils import getAllEVfromRepo, getCommitsWhereKeywordsAppear, getAllCommitsJSONFormat, getPreviousAndNext, \
    getFilesAndMethodsModified

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


REPO = "/home/passport/Repos/tmp/thingsboard"

print(" 1/6  -  Get VE from Project")
EVs = getAllEVfromRepo(REPO)
print("--- %s seconds ---" % (time.time() - start_time))
# print(EVs)

print(" 2/6  -  Get all commits in json format")
allCommitsJSONFormat = getAllCommitsJSONFormat(REPO, "thingsboard.json")
print("--- %s seconds ---" % (time.time() - start_time))
# print(allCommitsJSONFormat)

print(" 3/6  -  Get commits where EV appears")
commitsWhereEVsAppears = getCommitsWhereKeywordsAppear(REPO, EVs)
print("--- %s seconds ---" % (time.time() - start_time))
# print(commitsWhereEVsAppears)

print(" 4/6  -  Get previous and next of each filtered commit")
jsonPreviousNextCommit = getPreviousAndNext(allCommitsJSONFormat, commitsWhereEVsAppears)
print("--- %s seconds ---" % (time.time() - start_time))
# print (jsonPreviousNextCommit)

print(" 5/6  -  Get files where EV where touched")
filesmodified = getFilesAndMethodsModified(jsonPreviousNextCommit, REPO)
print(filesmodified)
print("--- %s TOTAL TIME ---" % (time.time() - start_time))


