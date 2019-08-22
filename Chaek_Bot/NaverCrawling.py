# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 10:19:37 2019

"""

# 네이버 책 베스트셀러 크롤링

#%%
import requests
from bs4 import BeautifulSoup

#%%

res = requests.get('https://book.naver.com/bestsell/bestseller_list.nhn')
html = res.text
soup = BeautifulSoup(html, "html.parser")

#%%
print(soup.prettify())

#%%
s1 = find('ol', {'class':'basic})

#%%
print(s1)

#%%
s2 = s1.find_all('li')

#%%
for i in s2:
    print(s2)

#%%
titles=[]
authors = []
intros = []

for i in s2:
    
    # book title
    s3 = i.find('dt').text
    titles.append(s3)
    
    # book author
    s3 = i.find('dd', 'txt_block')
    s4 = s3.find('a').text
    authors.append(s4)
    
    # book intro
    s3 = i.find_all('dd')
    s4 = s3[2].text
    intros.append(s4)
    
#%%
for i in titles:
    print(i)

#%%
for i in authors:
    print(i)
    
#%%
for i in intros:
    print(i)
    
#%%
books = {'book_name' : titles, 'author' : authors, 'intro' : intros }


#%%
import pandas as pd

df = pd.DataFrame(books)
df.to_csv('best_sellers2.csv', encoding='ms949')

#%%
# 여러 페이지의 베스트셀러를 가져올 때

from selenium import webdriver
from bs4 import BeautifulSoup
import time

#%%
driver = webdriver.Chrome('C:/Users/hsh01/python_class/class_01/chromedriver.exe')

### 3초간의 시간 주기
driver.implicitly_wait(3)

### 네이버 책 - 베스트 탭에 들어가기
driver.get('https://book.naver.com/bestsell/bestseller_list.nhn')

### 네이버 책 - 베스트 탭 - 1~6page의 페이지소스 가져오기
htmls = [] 
htmls.append(driver.page_source)
'''
time.sleep(3)
n_button = driver.find_element_by_xpath('//*[@id="section_bestseller"]/div[4]/a[1]').click() #1->2page
htmls.append(driver.page_source)

time.sleep(3)
n_button = driver.find_element_by_xpath('//*[@id="section_bestseller"]/div[4]/a[2]').click() #2->3page
htmls.append(driver.page_source)

time.sleep(3)
n_button = driver.find_element_by_xpath('//*[@id="section_bestseller"]/div[4]/a[3]').click() #3->4page
htmls.append(driver.page_source)

time.sleep(3)
n_button = driver.find_element_by_xpath('//*[@id="section_bestseller"]/div[4]/a[4]').click() #4->5page
htmls.append(driver.page_source)

time.sleep(3)
n_button = driver.find_element_by_xpath('//*[@id="section_bestseller"]/div[4]/a[5]').click() #5->6page
htmls.append(driver.page_source)
'''

for i in range(5):
    ### 4초간의 시간 주기(시간을 너무 짧게 주면 페이지를 넘기질 못함)
    time.sleep(4)
    num=i+1
    n_button = driver.find_element_by_xpath('//*[@id="section_bestseller"]/div[4]/a'+'[{}]'.format(num)).click()
    htmls.append(driver.page_source)


#%%
titles=[]
authors = []
intros = []

for html in htmls:
    soup = BeautifulSoup(html, "html.parser")
    s1 = soup.find('ol', {'class':'basic'})
    s2 = s1.find_all('li')
    
    for i in s2:
    
        # book title
        s3 = i.find('dt').text
        titles.append(s3)
    
        # book author
        s3 = i.find('dd', 'txt_block')
        s4 = s3.find('a').text
        authors.append(s4)
    
        # book intro
        s3 = i.find_all('dd')
        s4 = s3[2].text
        intros.append(s4)
    
books = {'book_name' : titles, 'author' : authors, 'intro' : intros }

#%%
import pandas as pd

df = pd.DataFrame(books)

print(len(df))
#%%
df.to_csv('best_sellers150.csv', encoding='ms949')

