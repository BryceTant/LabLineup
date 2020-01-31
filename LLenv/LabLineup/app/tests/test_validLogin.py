# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestValidLogin():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_validLogin(self):
    self.driver.get("https://lablineup.com")
    self.driver.set_window_size(927, 1053)
    assert self.driver.find_element(By.XPATH, "//p[contains(.,\'Welcome to LabLineup, a free and easy to use queuing system for handling requests for help in your academic labs.\')]").text == "Welcome to LabLineup, a free and easy to use queuing system for handling requests for help in your academic labs."
    elements = self.driver.find_elements(By.XPATH, "//img[contains(@src,\'https://storage.googleapis.com/lablineup-static/Logos/primary_logo.png\')]")
    assert len(elements) > 0
    elements = self.driver.find_elements(By.LINK_TEXT, "Log in")
    assert len(elements) > 0
    self.driver.find_element(By.LINK_TEXT, "Log in").click()
    elements = self.driver.find_elements(By.XPATH, "//section[@id=\'loginForm\']/form")
    assert len(elements) > 0
    self.driver.find_element(By.ID, "id_username").click()
    self.driver.find_element(By.ID, "id_username").send_keys("testUser2")
    self.driver.find_element(By.ID, "id_password").send_keys("LabLineup2")
    self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
    elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, \'/account\')]")
    assert len(elements) > 0
    elements = self.driver.find_elements(By.LINK_TEXT, "Log off")
    assert len(elements) > 0

# _prod -- This test was run on the production environment...not the test server
  
