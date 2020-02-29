import os
import sys
import subprocess

print ('This script will retrieve keywords in the current folder')
print ('Format :  python retrieveFilesWithKeywords.py PathToProject keyword1/keyword2/keyword3 bannedWord1/bannedWord2 ')
print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))


folder = sys.argv[1]
os.chdir(folder)
print("Now in folder " + subprocess.getoutput("pwd"))

keywords = "'" + sys.argv[2] + "'"
keywords = keywords.replace('/', '|')
bannedWord = sys.argv[3].split('/')

grepParams = "-Ewnr -m1 "

cmd = "grep " + grepParams + keywords + " | sed '"

print(len(bannedWord))
for i in range(0, len(bannedWord)) : 
	cmd += '/' + bannedWord[i] + '/d'
	if i != len(bannedWord) : cmd += ';'

cmd += "'"

print("Commande executee : " + cmd)

print("Matchs : ")
os.system(cmd)



cmdMin = cmd.replace(grepParams, "-lEwnr -m1 ")
print("Commande executee : " + cmdMin)
print("File concerned : ")
output = subprocess.getoutput(cmdMin)

files = output.split("\n")
print (files)
