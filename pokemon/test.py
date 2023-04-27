import re
word=input()
word=word.replace("_",".")
length=len(word)
file1 = open("F:\pokemon\database.txt", "r")
flag = 0
index = 0

for line in file1:
    index+=1

    if re.search(word, line) and length==len(line)-1: 
    	print(line)
file1.close()