#Script to upload word documents to wordpress blog

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import os
import time
import mammoth

options = Options()
options.headless = True
gecko_path=os.path.abspath("gecko/geckodriver")
driver = webdriver.Firefox(options=options, executable_path=gecko_path)

#Replace the wordpress userid, password, and website url (for eg. www.example.com)
userid = "INSERT_WORDPRESS_USERID"
password = "INSERT_WORDPRESS_PASSWORD"
website = "INSERT_WEBSITE_URL"

url = website+"/wp-admin/post-new.php"
driver.get(url)		
time.sleep(30)
driver.find_element_by_id("user_login").send_keys(userid)
driver.find_element_by_id("user_pass").send_keys(password)
driver.find_element_by_id("wp-submit").click()
time.sleep(30)

permalinks = ""

#'blog' ... is the directory with all the blog posts
for file in os.listdir('blog'):
	filepath = 'blog/'+file
	result = mammoth.convert_to_html(filepath)
	html = result.value
	messages = result.messages
	title = file[:-5]
	driver.find_element_by_id("title").send_keys(title)
	driver.find_element_by_id("content-html").click()
	driver.find_element_by_id("content").send_keys(html)
	driver.find_element_by_id("in-category-14").click()
	driver.execute_script("window.scrollTo(0, 0)")
	time.sleep(10)
	driver.find_element_by_id("publish").click()
	time.sleep(10)
	link = driver.find_element_by_xpath("//span[@id='sample-permalink']/a[1]").get_attribute('href')
	permalinks = permalinks+ link + '\n'	
	time.sleep(30)
	print("Uploaded ",file)
	driver.get(url)

#Writes the blog posts permalinks to a file if you need 'em
with open('links', 'w') as outfile:
	outfile.write(permalinks)
