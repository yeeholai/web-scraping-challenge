# Import dependencies

import pandas as pd
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser=init_browser()

    # NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    news_title = soup.find_all("div", class_="content_title")[0].text.strip()
    news_title

    news_paragraph = soup.find_all("div", class_="rollover_description_inner")[0].text.strip()
    news_paragraph


    # ### JPL Mars Space Images
    
    jpl = 'https://spaceimages-mars.com/'
    browser.visit(jpl)
    html = browser.html
    soup=bs(html,"html.parser")
    img_url = soup.find("a", class_="showimg fancybox-thumbs")["href"]
    featured_img_url = jpl + img_url
    featured_img_url


    # ### Mars Facts
    url = "https://galaxyfacts-mars.com/"
    mars_table=pd.read_html(url)[0]
    mars_table.rename(columns={0:"Description",1:"Mars",2:"Earth"},inplace=True)
    mars_table.set_index("Description", inplace=True)

    mars_table = mars_table.to_html()
    mars_table = mars_table.replace('\n','')

    # ### Mars Hemispheres
    url="https://marshemispheres.com/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    hemisphere_dict = []
    container = soup.find_all("div", class_="item")

    for item in container:
    #     Title
        hemisphere = item.find("div",class_="description")
        title = hemisphere.h3.text
        
    #     Image url
        h_url = hemisphere.a['href']
        browser.visit(url+h_url)
        html=browser.html
        soup = bs(html, "html.parser")
        image_url = soup.find_all("img")[4]["src"]
        image_url = url+image_url
        dictionary = {"title":title,
                     "image_url":image_url}
        hemisphere_dict.append(dictionary)

    # ### One dictionary to bind them all

    one_dictionary={
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_img_url": featured_img_url,
        "mars_table": mars_table,
        "hemisphere_info": hemisphere_dict
    }
    browser.quit()
    
    return one_dictionary