
# -*- coding: utf-8 -*-
import datetime
import json
import time

import scrapy
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
from scrapy.utils.response import open_in_browser




class LinkExcSpider(scrapy.Spider):
    name = 'page'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']



    def start_requests(self):

        try:

            current_url = 'https://quotes.toscrape.com/login'
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            # chrome_options.add_argument("--headless")

            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.get(current_url)
            time.sleep(5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.find_element_by_xpath("//input[@id='username']").send_keys("temp@gmail.com")
            driver.find_element_by_xpath("//input[@id='password']").send_keys("temp123")
            driver.find_element_by_xpath("//input[@value='Login']").click()


            links = ['']


            current_url = 'https://quotes.toscrape.com/login'
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            # chrome_options.add_argument("--headless")

            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.get(current_url)
            time.sleep(5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.find_element_by_xpath("//input[@id='username']").send_keys("temp@gmail.com")
            driver.find_element_by_xpath("//input[@id='password']").send_keys("temp123")
            driver.find_element_by_xpath("//input[@value='Login']").click()


            link = 'https://quotes.toscrape.com/page/2/'
            driver.get(link)

            # res = HtmlResponse(url=current_url, body=driver.page_source.encode('utf8'))
            res = HtmlResponse(url=driver.current_url, body=driver.page_source.encode('utf8'))
            driver.quit()
        except Exception as e:
            print(e)


    def parse(self, response):
       ab = response.text



if __name__ == '__main__':
    execute("scrapy crawl page".split())