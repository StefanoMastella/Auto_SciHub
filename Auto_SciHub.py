"""
Automação web
"""
#%% Settings
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pyautogui as pyag
import numpy as np
import re

brow = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

palavras_chave='speech regocnition acoustics machine learning'
scholar_pages = 3

#%% 

brow.get('https://scholar.google.com.br/')
brow.find_element('xpath',
                  '/html/body/div/div[7]/div[1]/div[2]/form/div/input').send_keys(palavras_chave)
brow.find_element('xpath',
                  '//*[@id="gs_hdr_tsb"]/span/span[1]').click()

links = []

for n in range(scholar_pages):
    if n == 0:
        links = brow.find_elements(By.TAG_NAME,'h3')
    else:
        new_links = brow.find_elements(By.TAG_NAME,'h3')
        for element in new_links:
            links.append(element)
    
    brow.find_element('xpath',
                      '//*[@id="gs_n"]/center/table/tbody/tr/td[12]/a/b').click()

titulos_artigos = []

for n in range(scholar_pages):
    # Find the h3 elements on the current page
    links = brow.find_elements(By.TAG_NAME,'h3')
    
    # Extract the text from the elements and add it to the titulos_artigos list
    for link in links:
        titulos_artigos.append(link.text)
    
    # Click the next page button
    brow.find_element('xpath',
                      '//*[@id="gs_n"]/center/table/tbody/tr/td[12]/a/b').click()

for link in range(np.size(titulos_artigos)):
    try:
        title = re.sub("[\(\[].*?[\)\]]", "", titulos_artigos[n])
        # time.sleep(2)
        brow.get('https://sci-hub.se/')
        brow.find_element('xpath',
                          '/html/body/div[2]/div[1]/form/div/textarea').send_keys(title)
        pyag.press('enter')
        brow.find_element('xpath',
                          '/html/body/div[3]/div[1]/button').click()
        n=n+1
        print(f'Artigo baixado com sucesso: {title}\n')
    except:
        n=n+1
        print(f'Não foi possível baixar o arquivo: {title}\n')
        pass

#%% Close window
input('Aperte qualquer tecla para fechar o navegador')
brow.close()
