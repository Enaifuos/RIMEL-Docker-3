import sys
import json


if ( len(sys.argv) < 2 ) :
	print("Give JSON data file as argument !")
else :
	tokens = ['environment', 'variable', 'env', 'var']
	with open(sys.argv[1], 'r') as f :
		logs_json = json.load(f)

	for log in logs_json :
		if any(token in log['subject'] for token in tokens) :
			print(log['subject']+ "   :   " + log['sha'])