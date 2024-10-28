from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,WebDriverException
import pyautogui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import configparser
import random
from selenium.webdriver.common.by import By
import psycopg2
import logging
from sys import exit
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-notifications")
#chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome( options= chrome_options)
driver.maximize_window()
config = configparser.ConfigParser()
config.read('credentials.conf')
email = config.get('DEFAULT','emailkey')
username = config.get('DEFAULT','usernamekey')
password = config.get('DEFAULT','passwordkey')
time.sleep(3)
target_url = 'https://x.com/i/flow/login'
driver.get(target_url) 
time.sleep(3)
username_input = driver.find_element("css selector","input[name='text']")
username_input.send_keys(email)
btton_to_pssword=driver.find_element("css selector","button.css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-ywje51.r-184id4b.r-13qz1uu.r-2yi16.r-1qi8awa.r-3pj75a.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l")
btton_to_pssword.click()
time.sleep(5)
password_input = driver.find_element("css selector", "input[name='password']")
password_input.send_keys(password)
login = driver.find_element("css selector", "button[data-testid='LoginForm_Login_Button']").click()
time.sleep(6)
driver.quit()