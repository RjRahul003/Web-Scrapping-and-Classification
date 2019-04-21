from selenium import webdriver
from bs4 import BeautifulSoup
from googlesearch import search
from time import sleep
from pyvirtualdisplay import Display
from requests import get
import pandas as pd
import json
import re

# display = Display(visible=0, size=(800,600))
# display.start()

chromeOptions = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images" : 2}
chromeOptions.add_experimental_option("prefs", prefs)

url = 'https://www.youtube.com/'
youtube_list = []

def load_complete_page(driver, clicks):
    for i in range(clicks):
        driver.execute_script("window.scrollBy(0,2500)")
        sleep(2)

try:
    driver = webdriver.Chrome(executable_path='/usr/share/safaridriver', chrome_options=chromeOptions)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    search = driver.find_element_by_css_selector('input#search')
    search.send_keys("travel blog")
    driver.find_element_by_css_selector('#search-icon-legacy').click()
    sleep(5)
    load_complete_page(driver, 300)

    container = driver.find_elements_by_tag_name('ytd-video-renderer')
    for i, each in enumerate(container):
        video_id = each.find_element_by_tag_name('a').get_attribute('href')
        title = each.find_element_by_css_selector('#video-title').text 
        description = each.find_element_by_css_selector('#description-text').text 
        category = 'travel'

        content = {
            'video_id': video_id,
            'title': title,
            'description': description,
            'category': category
        }

        youtube_list.append(content)
        print (i, content)

except Exception as e:
    print ('Some error occured: ', e)
finally:
    driver.close()
    # display.stop()

    df = pd.DataFrame(youtube_list)
    df = df[['video_id', 'title', 'description', 'category']]
    df.to_csv('youtube.csv', index=False)
