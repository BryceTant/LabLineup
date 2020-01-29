# test_login.py
# Tests to see if user can login with valid/test credentials
# Generated using Selenium IDE
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

class TestLogin():
  def setup_method(self, method):
    self.driver = webdriver.Chrome() # Specifies Chrome as browser used for testing
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_login(self):
    self.driver.get("https://lablineup.com/")
    self.driver.set_window_size(927, 1053)
    self.driver.find_element(By.LINK_TEXT, "Log in").click()
    self.driver.find_element(By.ID, "id_username").click()
    self.driver.find_element(By.ID, "id_username").send_keys("testUser2")
    self.driver.find_element(By.ID, "id_password").send_keys("LabLineup2")
    self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
  
