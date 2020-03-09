import json

from scripts.AnalysisStatistics import getStatisticsFromAllFiles

def deleteEntriesWithEmptyPreviousAnalysisKey(json) :
	keysToDelete=[]
	for key in json :
		i = 0
		for item in json[key] :
			if len(item['previousAnalysis']) == 0 :
				del json[key][i]
				if len(json[key]) == 0 :
					#del json[key]
					keysToDelete.append(key)
			i += 1

	for key in keysToDelete :
		del json[key]


jsonDataFile="analysis.json"

with open(jsonDataFile) as jsonfile :
	data=json.load(jsonfile)

# delete entries where there is no previousAnalysis AND delete entries with size equals to 0
deleteEntriesWithEmptyPreviousAnalysisKey(data)

dictAnalysis={}
for key in data :
	#dictAnalysis[key] = {"nlocTotalPrevious":{}, "nlocTotalActual":{}}
	nlocTotalActual=0
	nlocTotalPrevious=0
	ccnTotalActual=0
	ccnTotalPrevious=0
	i = 0
	for item in data[key] :
		previousAnalysisData=getStatisticsFromAllFiles(item['previousAnalysis'])
		actualAnalysisData=getStatisticsFromAllFiles(item['actualAnalysis'])

		nlocTotalPrevious += eval(previousAnalysisData['nloc'])['avg']
		nlocTotalActual += eval(actualAnalysisData['nloc'])['avg']
		ccnTotalPrevious += eval(previousAnalysisData['ccn'])['avg']
		ccnTotalActual += eval(actualAnalysisData['ccn'])['avg']
		i += 1

	dictAnalysis[key] = {"nlocTotalPrevious":(nlocTotalPrevious/i), "nlocTotalActual":(nlocTotalActual/i), "ccnTotalPrevious":(ccnTotalPrevious/i), "ccnTotalActual":(ccnTotalActual/i)}

print(json.dumps(dictAnalysis))


dictFinalCompute={}
for key in dictAnalysis :
	dictFinalCompute[key] = {}
	dictFinalCompute[key]["nloc"] = dictAnalysis[key]["nlocTotalActual"] - dictAnalysis[key]["nlocTotalPrevious"]
	dictFinalCompute[key]["ccn"] = dictAnalysis[key]["ccnTotalActual"] - dictAnalysis[key]["ccnTotalPrevious"]
 	


print(json.dumps(dictFinalCompute))