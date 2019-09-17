from bs4 import BeautifulSoup
import urllib.request
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pandas as pd
import time

OUTPUT_FILE = 'output.txt'
URL = 'https://www.youtube.com/watch?v=67Xd44rF4Nk'

def get_text(URL):
    driver = webdriver.Chrome('D:/Tools/chromedriver.exe')
    driver.get(URL)
    body = driver.find_element_by_tag_name('body')

    num_page_down = 1
    while num_page_down:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        num_page_down -= 1

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    text = ''
    body = soup.find('body')
    temp = body.find_all('yt-formatted-string', attrs={'class':'style-scope ytd-video-primary-info-renderer'})
    title = temp[0].get_text()
    print(title)
    thread = body.find_all('ytd-comment-renderer', attrs={'class':'style-scope ytd-comment-thread-renderer'})
    comments = []
    for items in thread:
        div = items.find_all('yt-formatted-string', attrs={'id':'content-text'})
        div2 = items.select('yt-formatted-string > a')[0].get_text()
        for lists in div:
            print(lists)
            if lists != None:
                try:
                    cmt = lists.string
                    textcmt = re.sub(r'[^\w]',' ',cmt)
                    comments.append([textcmt, div2])    
                    print(textcmt)
                except TypeError as e:
                    print(e)
                    pass
            else:
                pass
        print(div2)
    return text

def clear_text(text):
    cleared = re.sub('[a-zA-Z]', '', text)
    cleared = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]', '', cleared)
    return cleared

def main():
    output_file = open(OUTPUT_FILE, 'w')
    result_text = get_text(URL)
    result_text = clear_text(result_text)
    print(result_text)
    output_file.write(result_text)
    output_file.close()

if __name__ == '__main__':
    main()
