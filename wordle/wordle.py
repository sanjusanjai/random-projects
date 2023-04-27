import re
import collections
import random
def read_words():
	with open("words.txt") as f:
		words=f.read()
	return words.split()

def shortlist_word(word_list):
	combined_word_list = "".join(word_list)
	frequency = collections.Counter(combined_word_list)
	frequencylength=len(frequency.keys())
	N= 2
	#print(N)
	return_list=list()
	for word in word_list:
		flag = 1
		for i in range(N):
			#print(frequency.most_common()[i][0])
			if frequency.most_common()[i][0] not in word:
				flag = 0
				break
		# for i in range(5,9):
		# 	if frequency.most_common()[i][0] not in word:
		# 		flag = 0
		# 		break
		if flag:
			return_list.append(word)
	return return_list
def blacklist(wordlist,black_list):
	returnlist=list()
	for word in wordlist:
		for count,i in enumerate(black_list):
			if i in word:
				break
			elif count+1==len(black_list):
				returnlist.append(word)
			else:
				continue		
	return returnlist


def postional_correction(wordlist,positioncorrect):
	regex=['.' for i in range(5)]
	for pos,letter in positioncorrect:
		regex[pos]=letter
	r=re.compile("".join(regex))
	returnlist=list(filter(r.match,wordlist))
	return returnlist

def position_wrong(wordlist,positionwrong):
	returnlist=list()
	for word in wordlist:
		for count,i in enumerate(positionwrong):
			if i not in word:
				break
			if count+1==len(positionwrong):
				returnlist.append(word)
	return returnlist



def reducelist(wordlist,review,predicted_word):
	reviewlist=[int(i) for i in review]
	predictedlist=[i for i in predicted_word]
	black_list=list()
	positionwrong=list()
	positioncorrect=list()
	for pos,i in enumerate(reviewlist):
		if i==0:
			black_list.append(predictedlist[pos])
		elif i==1:
			positionwrong.append(predictedlist[pos])
		elif i==2:
			positioncorrect.append((pos,predictedlist[pos]))
		else:
			print("Something is wrong. I can feel it ")
			exit(0)
	if blacklist:
		wordlist=blacklist(wordlist,black_list)
	if positioncorrect:
		wordlist=postional_correction(wordlist,positioncorrect)
	if positionwrong:
		wordlist=position_wrong(wordlist,positionwrong)
	#print("wordlist=",wordlist)
	return wordlist
	#print(reviewlist)

def removered(wordlist): ## remove redundant lettered words example: fuzzy, gloss
	returnlist=list()
	for x in wordlist:
		if len(set(x)) == len(x):
			returnlist.append(x)
	return returnlist

word_list=read_words()
word_list.sort()
word_list=removered(word_list)
#combined_word_list = "".join(word_list)
#frequency = collections.Counter(combined_word_list)w
#print(frequency)
review=''
predicted_word=''
for _ in range(6):
	if review!='':
		word_list=reducelist(word_list,review,predicted_word)
	shortlist=shortlist_word(word_list)
	print(f"short listed words = {shortlist}")
	random.shuffle(shortlist)
	predicted_word=shortlist[0]
	print("predicted word= ",predicted_word)
	review=input('review on wordle:')
	if review=='22222':
		print("final word = ",predicted_word)
		print("pogchamp")
		exit(0)
	else:
		continue
print("maybe the word is not in the wordlist")
# print(sorted(frequency.items(), reverse=True, key =
#              lambda kv:(kv[1], kv[0])))
# for word in word_list:
# 	flag = 1
# 	for i in range(5):
# 		if frequency.most_common()[i][0] not in word:
# 			flag = 0
# 			break
# 	if flag:
# 		print(word)


