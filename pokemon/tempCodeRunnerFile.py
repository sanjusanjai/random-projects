import time
import os
import re
import random
import string
import secrets
from new_search import search_pokemon
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
load_dotenv('mydata.env')
driver = webdriver.Chrome()
XPATHS={
	'loginbutton':'//*[@type="submit"]',
	'channeltospam':'//*[@id="app-mount"]/div[2]/div/div[2]/div/div/nav/ul/div[2]/div[3]/div[1]',
	'pokeimages':'//a[@class="anchor-3Z-8Bb anchorUnderlineOnHover-2ESHQB imageWrapper-2p5ogY imageZoom-1n-ADA clickable-3Ya1ho embedWrapper-lXpS3L embedMedia-1guQoW embedImage-2W1cML"]'
}

driver.get("https://discord.com/login")
time.sleep(3)

username_input = driver.find_element_by_name("email")
#username_input.send_keys(os.getenv('EMAIL'))
username_input.send_keys("npbarath02@gmail.com")

password_input = driver.find_element_by_name("password")
#password_input.send_keys(os.getenv('DISCORD_PASSWORD'))
password_input.send_keys("barathnp02")

login_button = driver.find_element_by_xpath(XPATHS['loginbutton'])
login_button.click()
time.sleep(5)
number_of_pokemon=0
driver.get("https://discord.com/channels/689826408243265609/689826409090383918")
time.sleep(5)
before_pokemon_href=''
pokemon_caught=0
while True:
	try:
		textbox=driver.find_element_by_xpath('//div[@aria-label="Message #xp-spam"]')
	except:
		continue
	N=random.randint(3,8)
	spam=''.join(secrets.choice(string.ascii_uppercase + string.digits+ string.ascii_lowercase)for i in range(N))
	textbox.send_keys(spam)
	textbox.send_keys(Keys.ENTER)
	time.sleep(2)
	images=driver.find_elements_by_xpath(XPATHS['pokeimages']) # pokemon images not dp
	if len(images)>0:
		imgsrc=images[-1].get_attribute('href')
		number_of_pokemon=re.sub(r'.*attachments\/(.*?)\/(.*?)\/.*',r'\1 \2',imgsrc).split()

	if before_pokemon_href!=number_of_pokemon:
		before_pokemon_href=number_of_pokemon
		textbox.send_keys("p!hint")
		textbox.send_keys(Keys.ENTER)
		time.sleep(5)
		hint_response=driver.find_elements_by_class_name('messageContent-2qWWxC')
		list_of_hints=[]
		for x in hint_response:
			try:
				if re.match('^The pokémon is .+',x.text): # text of pokebot for hint
					list_of_hints.append(x.text)
			except:
				continue
		try:
			latest_hint=list_of_hints[-1]
			latest_hint=latest_hint[15:-1]
		except:
			continue
		pokemon=search_pokemon(latest_hint)
		if len(pokemon)==0:
			textbox.send_keys(f"p!c {x}")
			textbox.send_keys(Keys.ENTER)
			time.sleep(10)
		for x in pokemon:
			textbox.send_keys(f"p!c {x}")
			textbox.send_keys(Keys.ENTER)
			time.sleep(10)
			check=driver.find_elements_by_class_name('markup-2BOw-j')
			allmessages='\n'.join([y.text for y in check])
			#print(allmessages)
			match=re.findall(f'Congratulations.*?{x}',allmessages,re.M)
			#print(match)
			if len(match):
				#print('breaking')
				if pokemon_caught==10:
					pokemon_caught=0
					time.sleep(60)
				else:
					pokemon_caught+=1
				break
			else:
				continue