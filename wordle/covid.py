import re
import collections

def covid_list():
	covid_list = list()
	with open("covid.txt") as f:
		for line in f:
			if line.strip() != '':
				covid_list.append(line.strip()) 
	return covid_list

covid_list=covid_list()
print(covid_list)
##firstnames=[i.split()[0].lower() for i in covid_list]
#print(firstnames)

#combined_word_list = "".join(word_list)
##frequency = collections.Counter(firstnames)
##print(frequency)
# print(covid_list)