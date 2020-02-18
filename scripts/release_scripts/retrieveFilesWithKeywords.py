import os
import sys
import subprocess
from get_nb_of_ev import list_of_EV

print ('This script will retrieve keywords in the current folder')
print ('Format :  python retrieveFilesWithKeywords.py PathToProject keyword1/keyword2/keyword3 bannedWord1/bannedWord2 ')
print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

folder = sys.argv[1]
os.chdir(folder)
print("Now in folder " + subprocess.getoutput("pwd"))


''' TEMP 
os.chdir("../../docker") 
print("Now in folder " + subprocess.getoutput("pwd")) #TEMP

envList = list_of_EV() 
print(envList)
keywords = "'" + '|'.join(envList) + "'" 

os.chdir("../")
print("Now in folder " + subprocess.getoutput("pwd")) #TEMP

TEMP '''

keywordsList = sys.argv[2].split('/')

keywords = "'" + sys.argv[2] + "'"
keywords = keywords.replace('/', '|')
bannedWord = sys.argv[3].split('/')

grepParams = "-Ewnr "

cmd = "grep " + grepParams + keywords + " | sed '"

print(len(bannedWord))
for i in range(0, len(bannedWord)) : 
	cmd += '/' + bannedWord[i] + '/d'
	if i != len(bannedWord) : cmd += ';'

cmd += "'"

print("Commande executee : " + cmd)

#print("Matchs : ")
#os.system(cmd)

output = subprocess.getoutput(cmd)
grepResult = output.split("\n")

keywords_file_map = dict.fromkeys(keywordsList, None) #map with keywords as key
for line in grepResult:
	line_splitted = line.split(":")
	for keyword in keywordsList : 
		result = line_splitted[2].find(keyword)
		if result != -1 :
			if keywords_file_map[keyword] is None : keywords_file_map[keyword] = []
			keywords_file_map[keyword].append(line_splitted[0])

print(keywords_file_map)