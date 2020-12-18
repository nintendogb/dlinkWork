import time
from selenium import webdriver
from typing import Union
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

HEADLESS = False

Browser = Union[
    webdriver.chrome.webdriver.WebDriver,
	webdriver.firefox.webdriver.WebDriver,
	webdriver.edge.webdriver.WebDriver,
]
ACCOUNT = 'nintendogb@gmail.com'
PASSWORD = 'dark1129'
EMAIL_VAL = '//*[@class="account-group email"]/input'
USER_VAL = '//*[@class="account-group"]/input'
SIGN_OUT = '//*[@class="d-md"]/a[2]'

def get_driver(bw_type: str) -> Browser:
    if bw_type == 'firefox':
        '''
        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True
        return webdriver.Firefox(firefox_profile=profile)
        '''
        options = webdriver.FirefoxOptions()
        if HEADLESS:
            options.add_argument('--headless')
        options.add_argument('ignore-certificate-errors')
        return webdriver.Firefox(executable_path='./geckodriver', options=options)
    elif bw_type == 'edge':
        return webdriver.Edge()
    elif bw_type == 'chrome':
        options = webdriver.ChromeOptions()
        if HEADLESS:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        return webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)
	

def test_page() -> None:
    for browser_type in ('firefox', 'edge', 'chrome'):
        if browser_type in ('edge'):
            continue
        print(f'START {browser_type} testing')
        driver = get_driver(browser_type)
        driver.get("https://sso.dlink.com/")
        
        
        banner_btn = driver.find_element_by_class_name('banner_btn')
        banner_btn.click()
        
        driver.implicitly_wait(30)
        email_col = driver.find_element_by_id('email')
        email_col.send_keys(ACCOUNT)
        password_col = driver.find_element_by_id('password')
        password_col.send_keys(PASSWORD)
        signin_btn = driver.find_element_by_id('signbtn')
        signin_btn.click()

        WebDriverWait(driver, 30).until(lambda d: d.find_element_by_xpath(EMAIL_VAL).get_attribute("value") != '')
        WebDriverWait(driver, 30).until(lambda d: d.find_element_by_xpath(USER_VAL).get_attribute("value") != '')
        cur_email = driver.find_element_by_xpath(EMAIL_VAL)
        cur_user = driver.find_element_by_xpath(USER_VAL)
        print(f'CUR_ACCOUNT[{cur_email.get_attribute("value")}]  CUR_USER[{cur_user.get_attribute("value")}]')
        
        sign_out = driver.find_element_by_xpath(SIGN_OUT)
        sign_out.click()
        
        banner_btn = driver.find_element_by_class_name('banner_btn')
        if banner_btn:
            print('SIGNOUT SUCCESSFULLY')
        else:
            print('SIGNOUT FAIL')
        
        driver.quit()

test_page()
