from selenium import webdriver
import urllib.parse as up

import_searchs = [
    'HarvardBiz Ray Wang',
    'The Wall Street Journal Jason Zweig',
    'BankingUX Jim Bruene',
    'TMA agency James Ashton',
    'Gartner Stessa Cohen',
]


browser = webdriver.Chrome()

for i in import_searchs:
    browser.get('https://www.google.com.tw/search?q=' + up.quote_plus(i) + '&oq=' + up.quote_plus(i) + '&aqs=chrome..69i57j69i60l3.632j0j1&sourceid=chrome&ie=UTF-8')
    links = browser.find_elements_by_xpath('//div[@class="rc"]/div/a')
    
    for link in links:
        print(link.get_attribute("href"))


browser.close()