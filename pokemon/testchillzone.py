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
	'pokeimages':'//a[@class="anchor-3Z-8Bb anchorUnderlineOnHover-2ESHQB imageWrapper-2p5ogY imageZoom-1n-ADA clickable-3Ya1ho embedWrapper-lXpS3L embedMedia-1guQoW embedImage-2W1cML"]',

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
driver.get("https://discord.com/channels/719913121392885802/839458671284191232")
time.sleep(5)

while True:
	try:
		textbox=driver.find_element_by_xpath('//div[@aria-label="Message #exp-spam"]')
	except:
		continue
	spam="dajksd"
	textbox.send_keys(spam)
	textbox.send_keys(Keys.ENTER)
	time.sleep(0.5)
	try:
		login_button = driver.find_element_by_xpath(XPATHS['loginbutton'])
		login_button.click()
		print("chiloled")
	except:
		continue