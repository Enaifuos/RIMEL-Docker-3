import json

tokens = ['environment', 'variable', 'env', 'var']

with open('../jsons/thinksBoard.json', 'r') as f:
    logs_json = json.load(f)

for log in logs_json :
	if any(token in log['subject'] for token in tokens) :
		print(log['subject']+ "   :   " + log['sha'])