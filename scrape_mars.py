#!/usr/bin/env python
# coding: utf-8

# In[6]:


import bs4
import requests as rq

url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

data = rq.get(url)

pull = bs4.BeautifulSoup(data.text, 'html.parser')

print(pull.prettify())


# In[13]:


res1 = pull.find_all('div', class_='image_and_description_container')

for i in res1:
    link1 = i.a['href']
    break
    
link2 = 'https://mars.nasa.gov'
link3 = link2+link1
tray = rq.get(link3)
soup = bs4.BeautifulSoup(tray.text, 'html.parser')
news_title=soup.find("title").text
news_p=soup.body.find_all('p')[0]

print(news_title)
print(news_p)


# In[15]:


import webdriver_manager.chrome as wmc
import splinter as spl

expath = {"executable_path" : wmc.ChromeDriverManager().install()}
brow = spl.Browser('chrome', **expath, headless=False)


# In[16]:


a = brow.visit('https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html')
b = bs4.BeautifulSoup(brow.html, 'html.parser')

for i in b:
    c = i.find('a', class_='showimg fancybox-thumbs')['href']
    break

url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'

curl = url+c
print(curl)    


# In[3]:


import pandas as pd

df1 = pd.read_html('https://space-facts.com/mars/')
print(len(df1))


# In[4]:


df2 = pd.DataFrame(df1[0])
df3 = pd.DataFrame(df1[1])
df4 = pd.DataFrame(df1[2])

df5 = [df2, df3, df4]
df6 = pd.concat(df5)
df7 = pd.DataFrame.to_html(df6)

print(df7)


# In[17]:


hemispheres=[{"title" : "Cerberus", "img_url" : "/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg"},
             {"title" : "Schiaparelli", "img_url" : "/cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg"}, 
             {"title" : "Syrtis Major", "img_url" : "/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg"},
             {"title" : "Valles Marineris", "img_url" : "/cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg"}]


# In[18]:


print(news_title)
print(news_p)
print(curl)
print(df7)
print(hemispheres)


# In[ ]:


import flask as fl
from flask_pymongo import PyMongo
import scrape_mars

app = fl.Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/scraper")

@app.route('/')
def first():
    data = mongo.db.collection.find_one()
    return fl.render_template('index2.html', record1=data)

@app.route('/scrape')
def scrapemaster():
    purpan=scrape_mars.scrape_info()
    mongo.db.collection.update({}, purpan, upsert=True)
    return redirect("/")
    

if __name__ == "__main__":
    app.run(debug=True)

