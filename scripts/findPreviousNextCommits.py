import sys
import json

if ( len(sys.argv) < 4 ) :
	print("Give interval size as argument :\n python3 elastic.json sha findPreviousNextCommits.py 1")
else :
	jsonfile = sys.argv[1]
	commitId = sys.argv[2]
	interval_size = sys.argv[3]

	print(jsonfile)
	print(commitId)
	print(interval_size)


	with open(jsonfile, 'r') as f :
		logs_json = json.load(f)
		


