from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

def scrape():
    
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url1="https://mars.nasa.gov/news/"
    url2="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    url3="https://twitter.com/search?q=%23Marsweather&src=typed_query&f=live"
    url4="https://space-facts.com/mars/"
    url5="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # NASA Mars News
    content=requests.get(url1)
    soup = BeautifulSoup(content.text,"html.parser")

    news_title = soup.find(class_="content_title").get_text().replace('\n','').strip()
    news_p = soup.find("div",class_="rollover_description_inner").get_text().replace('\n','').strip()

    # JPL Mars Space Images - Featured Image
    browser.visit(url2)
    browser.find_by_id('full_image').click()
    html = browser.html
    soup = BeautifulSoup(html,"html.parser")

    featured_image = soup.find('article').find("a").get("data-fancybox-href")
    # featured_image = soup.find('div', {"class": "fancybox-inner fancybox-skin fancybox-dark-skin fancybox-dark-skin-open"}).img['src']
    featured_image_url = (f"https://www.jpl.nasa.gov{featured_image}")
    
    #Mars Weather
    browser.visit(url3)
    html = browser.html
    soup = BeautifulSoup(html,"html.parser")
    insight = soup.find(text=re.compile('InSight'))

    #Mars Facts
    browser.visit(url4)
    html = browser.html
    soup = BeautifulSoup(html,"html.parser")

    mars_facts = soup.find("table",class_="tablepress tablepress-id-p-mars")
    mars_facts_df=pd.read_html(str(mars_facts))[0]
    mars_facts_df = mars_facts_df.rename(columns={0:'Parameter',1:"Values"})
    mars_facts_df = mars_facts_df.set_index('Parameter')
    mars_facts_df.to_html("templates/table.html")

    #Mars Hemispheres
    browser.visit(url5)
    browser.find_by_tag('h3')[0].click()
    html = browser.html
    soup = BeautifulSoup(html,"html.parser")
    value=soup.find_all("li")
    img1_url=value[0].a["href"]
    img1_title=soup.find('h2', class_='title').text
    print(img1_title)
    print(img1_url)

    browser.visit(url5)
    browser.find_by_tag('h3')[1].click()
    html = browser.html
    soup = BeautifulSoup(html,"html.parser")
    value=soup.find_all("li")
    img2_url=value[0].a["href"]
    img2_title=soup.find('h2', class_='title').text
    print(img2_title)
    print(img2_url)

    browser.visit(url5)
    browser.find_by_tag('h3')[2].click()
    html = browser.html
    soup = BeautifulSoup(html,"html.parser")
    value=soup.find_all("li")
    img3_url=value[0].a["href"]
    img3_title=soup.find('h2', class_='title').text
    print(img3_title)
    print(img3_url)

    browser.visit(url5)
    browser.find_by_tag('h3')[3].click()
    html = browser.html
    soup = BeautifulSoup(html,"html.parser")
    value=soup.find_all("li")
    img4_url=value[0].a["href"]
    img4_title=soup.find('h2', class_='title').text
    print(img4_title)
    print(img4_url) 

    mars_data = { 
        "News_Title": news_title,
        "News_Paragraph": news_p,
        "Featured_Image": featured_image_url,
        "Weather": insight}
        
    browser.quit()
    
    return mars_data