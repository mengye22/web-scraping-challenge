from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    import os
    if os.name=="nt":
        executable_path = {'executable_path': './chromedriver.exe'}
    else:
        executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
    

def scrape():
    browser = init_browser()
    # Visit NASA Mars News
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    time.sleep(2)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # title and body is in the div with the class list_text
    article = soup.find('div',class_='list_text')
    # with in the class list_text, then find the title and body text
    news_title = article.find('div',class_='content_title').text
    news_para = article.find('div',class_='article_teaser_body').text

    # connect with JPL Mars space images website
    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)
    time.sleep(2)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # link of the image is in img with class thumb and under src
    image = soup.find('a',class_='button')['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov/'+image

    # connect with Mars twitter account to see the weather information
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    time.sleep(4)
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    # access the span class for all tweets
    all_tweets = soup.find_all("span",class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    for item in all_tweets:
        # access the text for the span
        current_weather = item.text
        # find the current weather twitter by matching InSight
        if 'InSight' in current_weather:
            break
        else:
            continue

    # connect with Mars facts to print out table information
    fact_url = "https://space-facts.com/mars/"
    browser.visit(fact_url)
    time.sleep(2)
    # access the first table(which is what we need) info
    mars_table = pd.read_html(fact_url)[0]
    mars_df = pd.DataFrame(mars_table)
    mars_df.columns = ["Description","Value"]
    mars_df = mars_df.set_index("Description")
    mars_fact = mars_df.to_html(header = True, index = True)

    # connect with Mars hemispheres to print out links
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    time.sleep(2)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    hemisphere_image_urls = []
    results = soup.find('div',class_='results')
    items = results.find_all('div',class_='item')

    for item in items:
        title = item.find('h3').text
        link = item.find('a')['href']
        web_link = "https://astrogeology.usgs.gov/" + link
        browser.visit(web_link)
        html = browser.html
        soup = bs(html, 'html.parser')
        img_download = soup.find('div',class_='downloads')
        img_url = img_download.find('a')['href']
        hemisphere_image_urls.append({"title":title,"img_url":img_url})
    
    browser.quit()

     # Store data in a dictionary
    mars_data = {
        "mars_title":news_title,
        "mars_para":news_para,
        "mars_fimg":featured_image_url,
        "mars_weather":current_weather,
        "marsFact":mars_fact,
        "mars_hemi":hemisphere_image_urls
    }

    # Return results
    return mars_data


