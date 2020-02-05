# Code Quality Assistant
# input : file or directory to run code analysis on


# output: hmtl website to analyze code analysis results found ./code-quality-assistant directory

from AnalysisScript import runAnalysis
from AnalysisStatistics import nb_files
from AnalysisStatistics import getStatisticsFromAllFiles
from AnalysisStatistics import getDiffPercentages


jsondata = runAnalysis('/home/passport/Repos/tmp/open-location-code/java/src')

# print(nb_files(jsondata))
# print(getStatisticsFromAllFiles(jsondata))

statisticsDict = {}
statisticsDict['commit1'] = getStatisticsFromAllFiles(jsondata)
statisticsDict['commit2'] = getStatisticsFromAllFiles(jsondata)
getDiffPercentages(statisticsDict)

