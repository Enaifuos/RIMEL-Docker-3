import json

methodIndicators = ['public', 'protected', 'private']
undesirableIndicators = ['class']



'''
	Arguments : 
		- a list of files that contain each one some environment variables.
		- a list of environment variables.
	Returns :
		Dictionary : {VE_1 : [method name 1, method name 2], VE_2 : [method name 3]}
	Note :
		- if a method M contains two differents EV, only the first EV detected will have it in the value list !
		- it works only for java files
'''
def get_dictonary_ve_method(files, environmentVariablesList) :
	method = None
	methodEVdict = {}

	for ev in environmentVariablesList :
		methodEVdict[ev] = []

	for filepath in files :
		file = open(filepath, 'r') 
		for line in file:
			l = line.strip()
			if any(word in l for word in methodIndicators) and (not l.endswith(';')) :
				if not any(undesirable in l for undesirable in undesirableIndicators) :
					method = l

			elif any(ev in l for ev in environmentVariablesList) :
				if method is not None :
					for ev in environmentVariablesList :
						if ev in l :
							fileMethodTuple = {'file':filepath, 'method':getMethodName(method)}
							methodEVdict[ev].append(fileMethodTuple)
							#methodEVdict[ev].append(getMethodName(method))
							method=None
							break
		file.close() 
	outputJSON = json.dumps(methodEVdict)
	return outputJSON



def getMethodName(line) :
	javaKeyWords = ['public', 'private', 'protected', 'static', 'final']
	count = 0
	#return line.split(' ')[0]
	for word in line.split(' ') :
		if word not in javaKeyWords :
			count += 1
		if count == 2 :
			count = 0
			return word.split("(")[0]
	return None



'''
	Arguments :
		- a method to get body
		- a file that contains the given method
	Returns :
		- String containing the method prototype and body
	Note :
		- we consider that in a file, there is only one method with the given name
		- IF THE METHOD COMES AT THE END OF THE CLASS, THIS METHOD MAY STUCKS !
'''
def get_method_body(filepath, method) :
	file = open(filepath, 'r')
	method_format1 = method
	method_format2 = method

	method_format1 += " ("
	method_format2 += "("

	inWantedMethod = False

	output = ""

	for line in file :
		l = line.strip()
		if not inWantedMethod :
			if (method_format1 in l or method_format2 in l) : 
				if any(word in l for word in methodIndicators) and (not l.endswith(';')) :
					if not any(undesirable in l for undesirable in undesirableIndicators) :
						inWantedMethod = True
						output += l
		else :
			if any(word in l for word in methodIndicators) and (not l.endswith(';')) :
				inWantedMethod = False
			elif (l and not l.startswith('//')) :
				output += l

	file.close()
	return output


x = get_dictonary_ve_method(['test.js', 'test2.js'], ["SIZE", "count"])
print(x)
#json.loads("{'SIZE': [{'file': 'test.js', 'method': 'copyLarge'}, {'file': 'test2.js', 'method': 'copyLarge5'}], 'count': [{'file': 'test.js', 'method': 'copy'}, {'file': 'test.js', 'method': 'copy'}, {'file': 'test2.js', 'method': 'copy33'}, {'file': 'test2.js', 'method': 'copy3'}]}")
#print(get_method_body('test.js', 'copy'))

