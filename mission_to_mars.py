# Import libraries
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd


# Define scrape function
def scrape():

    executable_path = {"executable_path": "chromedriver.exe"}    
    browser = Browser("chrome", **executable_path, headless=False)

    # Open the site
    browser.visit('https://mars.nasa.gov/news')
    # Get the heml
    html = browser.html
    # Use Beautiful soup to parse the html
    soup = bs(html, 'html.parser')

    # Define final empty dictionary
    mars_all = {}

    # Get title and paragraph
    news_title = soup.find('div', class_="content_title").text
    news_paragraph = soup.find('div', class_="article_teaser_body").text

    # Add to dictionary
    mars_all['news_title'] = news_title
    mars_all['news_paragraph'] = news_paragraph

    # Get latest weather from twitter
    weather_data = requests.get('https://twitter.com/MarsWxReport').text
    weather_soup = bs(weather_data, 'lxml')
    weather_tweet = weather_soup.find_all('div', class_="js-tweet-text-container")
    mars_weather = ''

    for result in weather_tweet:
        try:
            tweet = result.find('p', class_="TweetTextSize").text
            if 'InSight' in tweet:
                mars_weather = tweet
                break
        except AttributeError as e:
            print(e)   

    # Add to dictionary
    mars_all['mars_weather'] = mars_weather

    # jpl featured image
    jpl_data = requests.get('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars').text
    jpl_soup = bs(jpl_data, 'lxml')
    jpl_image_url = jpl_soup.find('div', class_="carousel_items").find('article')
    jpl_image_url = jpl_image_url['style']
    jpl_image_url = jpl_image_url.replace('background-image: url(', '').replace(');','').replace('\'', '')
    jpl_image_url = 'https://www.jpl.nasa.gov' + jpl_image_url

    # Add to dictionary
    mars_all['jpl_image_url'] = jpl_image_url

    # mars fact
    mars_fact_url = requests.get('https://space-facts.com/mars/').text
    mars_soup = bs(mars_fact_url, 'lxml')
    mars_fact = mars_soup.find('table', class_="tablepress-id-p-mars")

    mars_fact_final = {}

    for result in mars_fact.find_all('tr'):
        col1 = result.find('td', class_="column-1").text
        col2 = result.find('td', class_="column-2").text
        col1 = col1.replace(":", "")
        mars_fact_final[col1] =col2
        
    # Add to dictionary
    mars_all['mars_fact'] = mars_fact_final

    # Hemisphere images
    hemis_url = requests.get('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars').text
    hemis_soup = bs(hemis_url, 'lxml')
    hemis_fact = hemis_soup.find_all('div', class_="item")

    hemisphere_image_urls = []

    for result in hemis_fact:
        hemis_url = 'http://astrogeology.usgs.gov' + result.find('a')['href']
        hemis_title = result.find('h3').text
        hemis_title = hemis_title.replace(' Enhanced', '')

        browser.visit(hemis_url)
        img_html = browser.html        
        img_url = 'http://astrogeology.usgs.gov' + bs(img_html, 'lxml').find('img', class_='wide-image')['src']

        hemis = {}
        hemis["title"] = hemis_title
        hemis["img_url"] = img_url
        
        hemisphere_image_urls.append(hemis)
        
    # Add to dictionary
    mars_all['hemisphere'] = hemisphere_image_urls

    return mars_all

if __name__ == "__main__":
    myscrape = scrape()
    print(myscrape)