import os
import time


from scripts.utils import getAllEVfromRepo, getCommitsWhereKeywordsAppear, getAllCommitsJSONFormat, getPreviousAndNext, \
    getFilesAndMethodsModified, startAnalysis

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

print(" 1/8  -  Get VE from Project")
EVs = getAllEVfromRepo(REPO)
print("--- %s seconds ---" % (time.time() - start_time))

EVs = ["ZOOKEEPER_URL"]

print(" 2/8  -  Get all commits in json format")
allCommitsJSONFormat = getAllCommitsJSONFormat(REPO, "thingsboard.json")
print("--- %s seconds ---" % (time.time() - start_time))


print(" 3/8  -  Get commits where EV appears")
commitsWhereEVsAppears = getCommitsWhereKeywordsAppear(REPO, EVs)
print("--- %s seconds ---" % (time.time() - start_time))


print(" 4/8  -  Get previous and next of each filtered commit")
jsonPreviousNextCommit = getPreviousAndNext(allCommitsJSONFormat, commitsWhereEVsAppears)
print("--- %s seconds ---" % (time.time() - start_time))


print(" 5/8 -  Get files where EV where touched")
filesToAnalyze = getFilesAndMethodsModified(jsonPreviousNextCommit, REPO)
print(filesToAnalyze)
print("--- %s seconds ---" % (time.time() - start_time))


print(" 6/8  -  Analysing code (complexity, nloc..)")
print("not implemented")
analysis = startAnalysis(filesToAnalyze, REPO)
print(analysis)
print("--- %s seconds ---" % (time.time() - start_time))


print(" 7/8  -  Generating statistics")
print("not implemented")
print("--- %s seconds ---" % (time.time() - start_time))



print(" 8/8  -  Plotting")
print("not implemented")
print("--- %s seconds ---" % (time.time() - start_time))


print("\n---------------------------------------------------")
print("--- %s total time ---" % (time.time() - start_time))
print("---------------------------------------------------")
