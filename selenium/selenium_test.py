# Run the tests: docker start selenium-test && docker exec -it selenium-test bash -c "python selenium_test.py"

import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test import TestCase, Client
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

    def testCreateAccount(self):
        driver = self.driver
        driver.get("http://web:8000/createaccount")
        driver.find_element_by_id("id_username").send_keys("test1")
        driver.find_element_by_id("id_password").send_keys("test1")
        driver.find_element_by_id("id_first_name").send_keys("Jane")
        driver.find_element_by_id("id_last_name").send_keys("Doe")
        driver.find_element_by_id("id_phone_number").send_keys("0909090909")
        driver.find_element_by_id("id_profile_url").send_keys("http://www.reddit.com/")

        driver.find_element_by_name("submit").click()

        self.assertEquals(driver.current_url, "http://localhost:8000/")


    def testLogInFunction(self):
        driver =self.driver
        driver.get("http://web:8000/login")
        username = driver.find_element_by_id("id_username")
        password = driver.find_element_by_id("id_password")

        username.send_keys("A")
        password.send_keys("A")

        driver.find_element_by_name("submit").click()

        self.assertEquals(driver.current_url, "http://localhost:8000/")

    def testRideDetails(self):
        driver =self.driver
        driver.get("http://web:8000/login")
        username = driver.find_element_by_id("id_username")
        password = driver.find_element_by_id("id_password")

        username.send_keys("A")
        password.send_keys("A")

        driver.find_element_by_name("submit").click()
        driver.find_element_by_xpath('/html/body/h7/table[1]/tbody/tr[1]/td[1]/a').click()

        assert "BLACK" in driver.page_source

    def testRideCreation(self):

        # Log in first 
        driver =self.driver
        driver.get("http://web:8000/login")
        username = driver.find_element_by_id("id_username")
        password = driver.find_element_by_id("id_password")

        username.send_keys("A")
        password.send_keys("A")

        driver.find_element_by_id("submit").click()
        driver.find_element_by_name("create_ride").click()
        
        # Fill in the create_ride form 
        driver.find_element_by_id("id_start").send_keys("Start_Point")
        driver.find_element_by_id("id_destination").send_keys("Destination_Point")
        driver.find_element_by_id("id_depart_time").send_keys("2002/01/03/01")
        driver.find_element_by_id("id_seats_offered").send_keys("4")
        driver.find_element_by_id("id_price").send_keys("200")

        driver.find_element_by_name("submit").click()

        assert "Start_Point" in driver.page_source

    def testlogout(self):

        # Log in first
        driver =self.driver
        driver.get("http://web:8000/login")

        username = driver.find_element_by_id("id_username")
        password = driver.find_element_by_id("id_password")

        username.send_keys("A")
        password.send_keys("A")

        driver.find_element_by_name("submit").click()
        driver.find_element_by_xpath('//*[@id="logout"]').click()

        self.assertEquals(driver.current_url, "http://localhost:8000/createaccount")


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()