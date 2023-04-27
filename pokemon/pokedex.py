from bs4 import BeautifulSoup
data=open('./ht','r')
soup = BeautifulSoup(data, 'html.parser')
pokemon=[]
for links in soup.findAll('div',{'class':'pokemon-info'}):
	link=links.find('h5')
	pokemon.append(link.get_text())
print(pokemon)
textfile = open("pokedex2.txt", "w")
for element in pokemon:
    textfile.write(element + "\n")
textfile.close()