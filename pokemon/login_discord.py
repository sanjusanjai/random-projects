import time
import os
import re
import random
import string
import secrets
from search import search_pokemon
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
load_dotenv('mydata.env')

class Clock_defined:
	def __init__(self,maxtime):
		self.maxtime=maxtime
		self.currenttime=0
		self.flag=False
	def tick(self):
		self.flag=False
		self.currenttime+=1
		if self.currenttime>=self.maxtime:
			self.flag=True
			self.currenttime=0
driver = webdriver.Chrome()

XPATHS={
	'loginbutton':'//*[@id="app-mount"]/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/button[2]',
	'channeltospam':'//*[@id="app-mount"]/div[2]/div/div[2]/div/div/nav/ul/div[2]/div[3]/div[1]',
	'pokeimages':'//a[@class="anchor-3Z-8Bb anchorUnderlineOnHover-2ESHQB imageWrapper-2p5ogY imageZoom-1n-ADA clickable-3Ya1ho embedWrapper-lXpS3L embedMedia-1guQoW embedImage-2W1cML"]'
}

driver.get("https://discord.com/login")
time.sleep(3)

username_input = driver.find_element_by_name("email")
username_input.send_keys(os.getenv('EMAIL'))


password_input = driver.find_element_by_name("password")
password_input.send_keys(os.getenv('DISCORD_PASSWORD'))


login_button = driver.find_element_by_xpath(XPATHS['loginbutton'])
login_button.click()
time.sleep(5)
#erver=driver.find_element_by_xpath(XPATHS['channeltospam']).click()
#time.sleep(5)


driver.get("https://discord.com/channels/719913121392885802/839458671284191232")
time.sleep(5)
#when xpath fails uncomment above
#message_class_regex="/^message-2qnXI6/"
#messages=driver.find_element_by_class_name(message_class_regex)
clock1=Clock_defined(4)
clock2=Clock_defined(5)
#=False
#before_length=0
before_len_list=0
before_message=''
before_pokemon_found=''
new_bot_message_length_before=0
new_bot_message_before=[]
latest_image=''
before_pokemon_href=''
while True:
	try:
		textbox=driver.find_element_by_xpath('//div[@aria-label="Message #exp-spam"]')
	except:
		continue
	N=random.randint(3,8)
	spam=''.join(secrets.choice(string.ascii_uppercase + string.digits+ string.ascii_lowercase)for i in range(N))
	textbox.send_keys(spam)
	textbox.send_keys(Keys.ENTER)
	#messages=driver.find_elements_by_class_name('groupStart-23k01U')
	time.sleep(1.1)
	#print((messages))
	#print(x.text for x in messages)
	new_bot_message=driver.find_elements_by_class_name('embedTitle-3OXDkz')
	now_messages=[x.text for x in new_bot_message]
	#print(now_messages)
	#print(new_bot_message_before)
	#print(len(new_bot_message),new_bot_message_length_before)
	#if((not new_bot_message_length_before) or ((new_bot_message_length_before!=len(new_bot_message)))):#and(len(new_bot_message)>1))):
	#print(new_bot_message_before!=now_messages)
	images=driver.find_elements_by_xpath(XPATHS['pokeimages'])
	print('nani',images)
	print([x.get_attribute('href') for x in images])
	if len(images)>0:
		imgsrc=images[-1].get_attribute('href')
		number_of_pokemon=re.sub(r'.*attachments\/(.*?)\/(.*?)\/.*',r'\1 \2',imgsrc).split()
		print(number_of_pokemon)
	
	#print(imgsrc)
	#print([x.text for x in imgsrc])

	#WebElement small = browser.findElement(new ByChained(By.xpath("""//div[contains(@class,'anchor-3Z-8Bb anchorUnderlineOnHover-2ESHQB imageWrapper-2p5ogY imageZoom-1n-ADA clickable-3Ya1ho embedWrapper-lXpS3L embedMedia-1guQoW embedImage-2W1cML')]"""),By.xpath("//div[contains(@class,'Medium')]"),By.xpath("//div[contains(@class,'Small')]")));
	#elems = images.find_elements_by_css_selector(".anchor-3Z-8Bb anchorUnderlineOnHover-2ESHQB imageWrapper-2p5ogY imageZoom-1n-ADA clickable-3Ya1ho embedWrapper-lXpS3L embedMedia-1guQoW embedImage-2W1cML [href]")
	#links = [elem.get_attribute('href') for elem in elems]
	#print(elems,links,sep='\n')
	#hr=driver.find_element_by_css_selector("p.sc-eYdvao.kvdWiq > a").get_attribute('href')
	#print('hr is',hr)
	if before_pokemon_href!=number_of_pokemon:
		before_pokemon_href=number_of_pokemon
		textbox.send_keys("p!hint")
		textbox.send_keys(Keys.ENTER)
		time.sleep(5)
		#new_bot_message_length_before=len(new_bot_message)
		new_bot_message_before=now_messages
		hint_response=driver.find_elements_by_class_name('messageContent-2qWWxC')
		list_of_hints=[]
		for x in hint_response:
			try:
				if re.match('^The pokémon is .+',x.text): # text of pokebot for hint
					list_of_hints.append(x.text)
			except:
				continue
		print(list_of_hints)
		latest_hint=list_of_hints[-1]
		print(latest_hint)
		latest_hint=latest_hint[15:-1]
		print(latest_hint)
		pokemon=search_pokemon(latest_hint)
		print(pokemon)
		textbox.send_keys(f"p!c {pokemon}")
		textbox.send_keys(Keys.ENTER)
		time.sleep(3)
	
	'''
	if new_bot_message_before!=now_messages:
		#print('enter',len(new_bot_message),new_bot_message_length_before,sep=' ')
		print('enter',re.match('^.+wild.+',now_messages[-1]))
		if(re.match('^.+wild.+',now_messages[-1])): #or (re.match('^.+A new wild.+',new_bot_message[-2].text) and re.match('^.+Congragulations.+',new_bot_message[-1].text))):
			print('asking hint')
			textbox.send_keys("p!hint")
			textbox.send_keys(Keys.ENTER)
			time.sleep(5)
			#new_bot_message_length_before=len(new_bot_message)
			new_bot_message_before=now_messages
			hint_response=driver.find_elements_by_class_name('messageContent-2qWWxC')
			list_of_hints=[]
			for x in hint_response:
				try:
					if re.match('^The pokémon is .+',x.text): # text of pokebot for hint
						list_of_hints.append(x.text)
				except:
					continue
			print(list_of_hints)
			latest_hint=list_of_hints[-1]
			print(latest_hint)
			latest_hint=latest_hint[15:-1]
			print(latest_hint)
			pokemon=search_pokemon(latest_hint)
			print(pokemon)
			textbox.send_keys(f"p!c {pokemon}")
			textbox.send_keys(Keys.ENTER)
			time.sleep(3)
			#print(search_pokemon(latest_hint))
			'''
	'''
	hint_response=driver.find_elements_by_class_name('messageContent-2qWWxC')#get hint of poke
	#print(hint_response)
	#print(x.text for x in hint_response)
	lists=[]
	for x in hint_response:
		try:
			if re.match('^The pokémon is .+',x.text): # text of pokebot for hint
				lists.append(x.text)
		except:
			continue
	#print(lists)
	
	#hint_response=[x for x in hint_response if re.match('^The pokémon is .+',x.text)]
	print(lists)
	

	if clock2.flag: 
		response=lists[-1]
		response=response[15:-1]
		pokemon_found=search_pokemon(response).lower()
		if before_pokemon_found!=pokemon_found:
			print(pokemon_found)
			textbox.send_keys(f"p!c {pokemon_found}")
			textbox.send_keys(Keys.ENTER)
		#flag_hint=True
		#before_len_list=len(lists)

	new_bot_message=driver.find_elements_by_class_name('embedTitle-3OXDkz')
	print(len(new_bot_message))
	#if before_length<len(new_bot_message): #and re.match('^.+A new wild.+',new_bot_message[-1].text):
	if before_message!=new_bot_message[-1].text:
		textbox.send_keys("p!hint")
		textbox.send_keys(Keys.ENTER)
		#before_length=len(new_bot_message)
		before_message=new_bot_message[-1].text
	print(new_bot_message[-1].text)
	# if((#) and (clock1.flag) and (re.match('^.+A new wild.+',new_bot_message[-1].text))): #or re.match('^.+A new wild.+',new_bot_message[-2].text))):
	# 	#t#extbox=driver.find_element_by_xpath('//div[@aria-label="Message #xp-spam"]')
	# 	textbox.send_keys("p!hint")
	# 	textbox.send_keys(Keys.ENTER)
	# 	#=False
	#pri#nt([x.text for x in new_bot_message])
	time.sleep(1)
	clock1.tick()
	clock2.tick()

#server= driver.find_element_by_xpath('//*[@id="app-mount"]/div[2]/div/div[2]/div/div/nav/ul/div[2]/div[3]/div[1]/div[2]/div/div/svg/foreignObject/div')
#server.click()
'''