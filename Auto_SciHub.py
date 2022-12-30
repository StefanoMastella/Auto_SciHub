"""
Web Scrape tool created to download dozens of articles from Google Scholar. 
It breaks paywalls using Sci Hub.

Created by Stéfano Mastella
"""
#%% Settings
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pyautogui as pyag
import numpy as np
import re

# Set up Chrome web driver
brow = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Define keywords to search for on Google Scholar
keywords='speech regocnition acoustics machine learning'
# Define number of pages to search through on Google Scholar
scholar_pages = 3

#%% Navigate to Google Scholar and perform search with defined keywords
brow.get('https://scholar.google.com.br/')
brow.find_element('xpath',
                  '/html/body/div/div[7]/div[1]/div[2]/form/div/input').send_keys(keywords)
brow.find_element('xpath',
                  '//*[@id="gs_hdr_tsb"]/span/span[1]').click()

#%% Main loops (run only this cell in case Google Scholar requires Captcha)

# Empty lists for furthe processing
links = []; article_titles = []

# Get the artile titles to be cracked by SciHub in the next loop
for n in range(scholar_pages):
    # Find the h3 elements on the current page
    links = brow.find_elements(By.TAG_NAME,'h3')
    
    # Extract the text from the elements and add it to the titulos_artigos list
    for link in links:
        article_titles.append(link.text)
    
    # Click the next page button
    brow.find_element('xpath',
                      '//*[@id="gs_n"]/center/table/tbody/tr/td[12]/a/b').click()

# Download the articles
for link in range(np.size(article_titles)):
    try:
        title = re.sub("[\(\[].*?[\)\]]", "", article_titles[n])
        # time.sleep(2)
        brow.get('https://sci-hub.se/')
        brow.find_element('xpath',
                          '/html/body/div[2]/div[1]/form/div/textarea').send_keys(title)
        pyag.press('enter')
        brow.find_element('xpath',
                          '/html/body/div[3]/div[1]/button').click()
        n=n+1
        print(f'Article downloaded successfully: {title}\n')
    except:
        n=n+1
        print(f'Unable to download file: {title}\n')
        pass

#%% Close window
input('Press any button to close the browser')
brow.close()
