from base64 import encode
import requests
from bs4 import BeautifulSoup
import string
from concurrent.futures import ThreadPoolExecutor


textfile = open("wordlist.txt", "w",encoding="utf-8")
THREADS=1000
#url=https://www.dictionary.com/list/A/3

URLS={
	"base":"https://www.dictionary.com",
	"list":"/list"
}

def geturl(alphabet,pagenumber):
	url=URLS["base"]+URLS["list"]+"/"+alphabet+"/"+str(pagenumber)
	r=requests.get(url)
	if r.status_code==200:
		return r
	else:
		return None

def execute(alphabet,pagenumber):
	pagenumber=0
	
	#while True:
	r=geturl(alphabet,pagenumber)
	print("hidasoda",r)
	if r.status_code==200:
		soup = BeautifulSoup(r.content,features="lxml")
		print("debug")
		table = soup.find('ul', attrs = {'class':'css-dy629s'}) 
		for element in table:
			textfile.write(element.text.split(" |")[0] + "\n")
	print("done")
		#pagenumber+=1


# alphabet="i"
# pagenumber="10"
# textfile = open("wordlist.txt", "w",encoding="utf-8")
print("hell")
with ThreadPoolExecutor(max_workers=THREADS) as pool:

	for alphabet in string.ascii_uppercase:
		print("hi")
		for pagenumber in range(1,50):
			textfile.write("1")
			pool.submit(execute,alphabet,pagenumber)



textfile.close()
# textfile.close()
# for alphabet in string.ascii_uppercase:
# 	pagenumber=0
# 	while True:
# 		r=geturl(alphabet,pagenumber)
# 		if r==None:
# 			break
# 		soup = BeautifulSoup(r.content)
# 		table = soup.find('ul', attrs = {'class':'css-dy629s'}) 
# 		for element in table:
# 			textfile.write(element.text.split(" |")[0] + "\n")
# 		pagenumber+=1
# textfile.close()
#print(table.prettify())
#print(soup.prettify())
#print(url)
# for pagenumber in range(1,25):
# 	r=geturl(alphabet,pagenumber)
# 	soup = BeautifulSoup(r.content, from_encoding="utf-8")
# 	table = soup.find('ul', attrs = {'class':'css-dy629s'}) 
# 	for element in table:
# 		#print(element.text.split(" |")[0] + "\n")
# 		print(element.text.encode("utf-8"))