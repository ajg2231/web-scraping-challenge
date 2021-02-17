#!/usr/bin/env python
# coding: utf-8

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

