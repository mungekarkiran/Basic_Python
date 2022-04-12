import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
from selenium import webdriver
import time

DRIVER_PATH = r'E:\\chromedriver.exe'
url = "https://courses.ineuron.ai/"

# initiating the webdriver.
driver = webdriver.Chrome(DRIVER_PATH) 
driver.get(url) 
  
# this is just to ensure that the page is loaded
time.sleep(5)

print(driver.title, ' || ', driver.current_url)

# # get Xpath 
# myXpath = driver.find_elements_by_xpath('//*[@id="__next"]/div[1]/section[2]/div/div[2]/div')
# xpathList = myXpath[0].text.split('\n') 

# for j in myXpath[0].text.split('\n'):
#     link_by_text = driver.find_element_by_link_text(j)
#     list_of_link = link_by_text.get_attribute('href')
#     print('list_of_link : ', list_of_link)
#     driver.get(list_of_link)
#     time.sleep(5)