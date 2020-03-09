import json
import statistics

def nb_files(jsonOutputData):
    return len(jsonOutputData['files'])


def getStatisticsFromAllFiles(jsonOutputData):
    nb_files = 0
    metricsMap = {}

    metricsMap['startLine'] = []
    metricsMap['nloc'] = []
    metricsMap['ccn'] = []
    metricsMap['tokens'] = []
    metricsMap['params'] = []
    metricsMap['length'] = []
    metricsMap['fanIn'] = []
    metricsMap['fanOut'] = []
    metricsMap['generalFanOut'] = []
    metricsMap['maxNestingDepth'] = []
    metricsMap['maxNestedStructures'] = []

    #print(jsonOutputData['files'])
    for item in jsonOutputData['files']:
        nb_files += 1
        if item['filetype'] == 'java' or item['filetype'] == 'js':
            for metric in item['functions']:
                metricsMap['startLine'].append(metric['startLine'])
                metricsMap['nloc'].append(metric['nloc'])
                metricsMap['ccn'].append(metric['ccn'])
                metricsMap['tokens'].append(metric['tokens'])
                metricsMap['params'].append(metric['params'])
                metricsMap['length'].append(metric['length'])
                metricsMap['fanIn'].append(metric['fanIn'])
                metricsMap['fanOut'].append(metric['fanOut'])
                metricsMap['generalFanOut'].append(metric['generalFanOut'])
                metricsMap['maxNestingDepth'].append(metric['maxNestingDepth'])
                metricsMap['maxNestedStructures'].append(metric['maxNestedStructures'])

    statisticsMap = {}

    statisticsMap['startLine'] = {}
    statisticsMap['nloc'] = {}
    statisticsMap['ccn'] = {}
    statisticsMap['tokens'] = {}
    statisticsMap['params'] = {}
    statisticsMap['length'] = {}
    statisticsMap['fanIn'] = {}
    statisticsMap['fanOut'] = {}
    statisticsMap['generalFanOut'] = {}
    statisticsMap['maxNestingDepth'] = {}
    statisticsMap['maxNestedStructures'] = {}

    for k, v in metricsMap.items():
        statisticsMap[k] = json.dumps({'avg': statistics.mean(v), 'median': statistics.median(v)})


    return statisticsMap


def plotStatistics(dictStatistics):
    print("todo")


def getDiffPercentages(dictStatistics):
    # must contain only dictStatistics["commit1"] and dictStatistics["commit2"]
    diffMap = {}

    diffMap['startLine'] = []
    diffMap['nloc'] = []
    diffMap['ccn'] = []
    diffMap['tokens'] = []
    diffMap['params'] = []
    diffMap['length'] = []
    diffMap['fanIn'] = []
    diffMap['fanOut'] = []
    diffMap['generalFanOut'] = []
    diffMap['maxNestingDepth'] = []
    diffMap['maxNestedStructures'] = []


    for k, v in dictStatistics['commit1'].items():
        # calculate percentage change .. ((aftervalue–beforevalue)/beforevalue)*100=%change.
        commitOneAvg = json.loads(dictStatistics['commit1'][k])['avg']
        commitTwoAvg = json.loads(dictStatistics['commit2'][k])['avg']
        commitOneMedian = json.loads(dictStatistics['commit1'][k])['median']
        commitTwoMedian = json.loads(dictStatistics['commit2'][k])['median']
        # print(str(commitOneAvg) + " " + str(commitTwoAvg) + " " + str(commitOneMedian) + " " + str(commitTwoMedian))
        diffMap[k] = json.dumps({'avg': (weird_division((commitTwoAvg-commitOneAvg), commitOneAvg)) * 100,
                                 'median': (weird_division((commitTwoMedian-commitOneMedian), commitOneMedian)) * 100 })

    return diffMap

def weird_division(n, d):
    return n / d if d else 0