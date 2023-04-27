def search_pokemon(word):
	import re
	word=word.replace("_",".")
	length=len(word)
	index = 0
	with open("database.txt", "r") as file1:
		for line in file1:
			index+=1
			if re.search(word, line) and length==len(line)-1: 
				return line[:-1]