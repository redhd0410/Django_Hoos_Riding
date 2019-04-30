# Run the tests: docker start selenium-test && docker exec -it selenium-test bash -c "python selenium_test.py"

import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from django.test import TestCase
import time

class TestSelenium(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote(
        command_executor='http://selenium-chrome:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME)

    def testCreateAccount(self):
        driver = self.driver
        driver.get("http://web:8000/createaccount")
        assert "Create Your Account" in driver.page_source

    def testLogInPage(self):
        driver = self.driver
        driver.get("http://web:8000/login")
        assert "Log In" in driver.page_source

    def testLogInFunction(self):
        driver =self.driver
        driver.get("http://web:8000/login")
        username = driver.find_element_by_id("id_username")
        password = driver.find_element_by_id("id_password")

        username.send_keys("A")
        password.send_keys("A")

        driver.find_element_by_name("submit").click()

        print(driver.current_url)

        pass

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()