def search_pokemon(word):
	import re
	word=word.replace("_",".")
	length=len(word)
	index = 0
	ans=[]
	with open("pokedex.txt", "r") as file1:
		for line in file1:
			index+=1
			if re.search(word, line) and length==len(line)-1: 
				ans.append(line[:-1])
	return ans