from requests import Session
from pprint import pprint
from pprint import pformat
import re
from bs4 import BeautifulSoup
API_HOST='https://api.genius.com'
API_TOKEN='Bearer zRAlYLK229jjN-BXgjBeNiWr90mI0b1uV4ldBzL7m5z2kbfjh_5flXx4XA6BTunx'
session=Session()

def search(q):
	global session
	res=session.get(f'{API_HOST}/search',params={'q':q},headers={'Authorization':API_TOKEN})
	if 200<=res.status_code<300 :
		return res.json()['response']['hits']
	return []

def description(id_of_song):
	global session
	lyrics=session.get(f'{API_HOST}/songs/{id_of_song}',params={'text_format':'plain'},headers={'Authorization':API_TOKEN})
	if 200<=lyrics.status_code<300:
		return lyrics.json()['response']['song']['description']['plain']
	return []

results=search('ed sheeran')
id_of_song=results[0]['result']['id']
pprint(results[0]['result']['url'])
url_lyrics=results[0]['result']['url']
page=session.get(url_lyrics)
soup=BeautifulSoup(page.content,'html.parser')
#soup.findAll(tag = '</a>').replaceWith(tag = '</a><br>')

#soup=soup.replace('<br/>', '\n')
html=list(soup.children)[2]
#body=list(html.children)[3]
#tag=list(body.children)[1]
#dsia=list(tag.children)[2]
#dsia=' '.join([str(elem) for elem in dsia])
#dsia.findAll(tag = '<br>').replaceWith(tag = '\n')
#lyrics=html.find("div", class_=re.compile("^lyrics$|Lyrics__Root"))
for br in soup.find_all("br"):
    br.replace_with("\n")
#lyrics=' '.join([str(elem) for elem in lyrics])
#lyrics = re.sub(r'(\[.*?\])*', '', lyrics)
#lyrics = re.sub('\n{2}', '\n', lyrics)
#lyrics=lyrics.strip("\n")
final=soup.get_text()
lyrics = re.sub(r'(\[.*?\])*', '', final).lower()
lyrics = re.sub('\n{2}', '\n', lyrics)
file=open('output.txt','w',encoding = 'utf-8')
file.write(lyrics)
file.close()
#lyrics=final.split('lyrics')
#print(len(lyrics))
#'https://genius.com/Eminem-rap-god-lyrics'
#name_song='shape of you'
#stripped=re.findall(f'{name_song} lyrics(.*)',lyrics,re.M)
#print(stripped)	
#print(lyrics)
