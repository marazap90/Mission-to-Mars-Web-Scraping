# import dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import time


def scrape():
    
    # start empty dictionary to store all upcoming mars data
    mars_data = {}
    
    # writting chromedriver path and creating browser object
    executable_path = {"executable_path": "/Users/marekz/Desktop/Data_Analytics_Bootcamp/chromedriver"}
    browser = Browser("chrome", headless=False)
    
    
    ##===============
    ## NASA Mars News
    ##===============
    
    url_news = "https://mars.nasa.gov/news/"
    browser.visit(url_news)
    time.sleep(1)
    
    # creating html object using BeautifulSoup
    nasa_html = browser.html
    soup = bs(nasa_html, "html.parser")
    
    # find first article
    article = soup.find("div", class_='list_text')
    
    # getting news title and paragraph from first article
    news_title = article.find('div', class_="content_title").text
    news_p = article.find('div', class_ ="article_teaser_body").text
    
    # store title and paragraph into dictionary
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p
    
    
    ##===============
    ## JPL Mars Space Images - Featured Image
    ##===============
    
    url_img = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_img)
    time.sleep(1)
    
    # navigating to image
    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(2)
    
    # navigating to more info to get large picture
    browser.click_link_by_partial_text("more info")
    time.sleep(2)
    
    # creating html object of current page using BeautifulSoup
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, "html.parser")
    time.sleep(1)
    
    # find image src path from page html 
    image_path = jpl_soup.find("img", class_='main_image')["src"]
    
    # create featured_image_url from source url plus image src path
    featured_image_url = "https://www.jpl.nasa.gov{}".format(image_path)
    
    # store featured image into dictionary
    mars_data["featured_image_url"] = featured_image_url
    
    
    ##===============
    ## Mars Weather
    ##===============
    
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    time.sleep(1)
    
    # creating html object of current page using BeautifulSoup
    twitter_html = browser.html
    twitter_soup = bs(twitter_html, "html.parser")
    time.sleep(1)
    
    # find first weather tweet
    mars_weather = twitter_soup.find("div", class_='js-tweet-text-container').text.strip()
    
    # store featured image into dictionary
    mars_data["mars_weather"] = mars_weather
    
    
    ##===============    
    ## Mars Facts
    ##===============
    
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    time.sleep(1)
    
    # using pandas to get table from site
    facts = pd.read_html(facts_url)
    facts_table = facts[0]
    facts_table.columns = ['Property', 'Mars', 'Earth']
    facts_table = facts_table.set_index(['Property'])
    facts_html_table = facts_table.to_html()
    
    
    ##===============
    ## Mars Hemispheres
    ##===============
    
    hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hem_url)
    time.sleep(1)
    
    # creating html object of current page using BeautifulSoup
    hem_html = browser.html
    hem_soup = bs(hem_html, "html.parser")
    time.sleep(1)
    
    # using for loop and bs to get url and title data, and storing into separated lists 
    hem_titles = []
    hem_urls = []
    
    for item in hem_soup.find_all("div",class_="item"):
        hem_title = item.find("h3").text[:-9]
        browser.click_link_by_partial_text("Enhanced")
        time.sleep(1)
        hem_img_url = browser.find_by_text('Sample')['href']
        hem_titles.append(hem_title)
        hem_urls.append(hem_img_url)
        
    # creating a list of dicts from the two separated lists created above
    hem_images_urls = [{'title': hem_titles[x],'img_url': hem_urls[x]} for x in range(len(hem_titles))]
    
    mars_data["hem_images_urls"] = hem_images_urls
    
    browser.quit()
return mars_data
    
    
    
    
    