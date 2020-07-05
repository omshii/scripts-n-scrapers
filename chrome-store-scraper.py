#A slow script to scrape the chrome extensions store

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import urllib.parse
import time
import math
import os

options = Options()
options.headless = True
gecko_path=os.path.abspath("gecko/geckodriver")
driver = webdriver.Firefox(options=options, executable_path=gecko_path)

search_term=input("Enter search_term: ")
results_number=int(input("Enter number of results: "))
search_url='https://chrome.google.com/webstore/search/'+urllib.parse.quote(search_term)+'?_category=extensions'
driver.get(search_url)

scroll_count=int(math.ceil(results_number/40))

last_height = driver.execute_script("return document.body.scrollHeight")
for i in range(0,scroll_count):
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
	time.sleep(5)
	new_height = driver.execute_script("return document.body.scrollHeight")
	if new_height == last_height:
		try:
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
			time.sleep(5)	
			driver.find_element_by_class_name('h-a-Hd-mb').click()
			new_height = driver.execute_script("return document.body.scrollHeight")
		except:
			break
	last_height = new_height

results_url_list=[]
results = driver.find_elements_by_class_name('h-Ja-d-Ac')
for result in results:
	result_url = result.get_attribute("href");
	results_url_list.append(result_url)

datafile = open("data.csv","a")
datafile.write("Name;Number of users;Number of reviews;Developer"+"\n")

print(len(results_url_list))

for url in results_url_list:
	try:	
		driver.get(url)
		time.sleep(5)
		name=driver.find_element_by_class_name('e-f-w').text
		try:	
			dev=driver.find_element_by_xpath("//div[@class='e-f-Me e-f-Xi-oc']/a[@class='e-f-y']").text	
		except:
			dev=driver.find_element_by_xpath("//span[@class='e-f-Me']/span[@class='oc']").text
		users=driver.find_element_by_class_name('e-f-ih').get_attribute("title")
		reviews=driver.find_element_by_class_name('KnRoYd-N-nd').text
		datafile.write(name+";"+users+";"+reviews+";"+dev+'\n')
	except Exception as error:
		print(error)		
		print(url)
		continue

	


