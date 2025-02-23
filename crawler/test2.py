from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

try:
    service = Service(executable_path="/usr/bin/chromedriver")
    service.start()
    print("ChromeDriver started successfully.")
except Exception as e:
    print(f"Failed to start ChromeDriver: {e}")