from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class UntitledTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
    
    def test_untitled_test_case(self):
        driver = self.driver
        driver.get("https://www.gamer.com.tw/")
        driver.find_element_by_link_text("我要登入").click()
        driver.find_element_by_id("uidh").click()
        driver.find_element_by_name("uidh").clear()
        driver.find_element_by_name("uidh").send_keys("tedkao")
        driver.find_element_by_name("passwdh").click()
        driver.find_element_by_name("passwdh").clear()
        driver.find_element_by_name("passwdh").send_keys("darkness")
        # ERROR: Caught exception [ERROR: Unsupported command [selectFrame | index=0 | ]]
        driver.switch_to.frame(0)
        driver.find_element_by_xpath("//span[@id='recaptcha-anchor']/div").click()
        # ERROR: Caught exception [ERROR: Unsupported command [selectFrame | relative=parent | ]]
        driver.switch_to.parent_frame()
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("哈啦區").click()
        driver.find_element_by_link_text("遊戲王 決鬥聯盟").click()
        driver.find_element_by_xpath("//img[contains(@src,'https://p2.bahamut.com.tw/FORUM/welcome/29618_2_1600140598.JPG')]").click()
        driver.find_element_by_xpath("//a[@id='topBar_member']/i").click()
        driver.find_element_by_link_text("登出").click()
        driver.find_element_by_xpath("//button[@type='button']").click()
    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()