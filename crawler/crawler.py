from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize WebDriver
driver = webdriver.Firefox()
driver.get("https://www.google.com")

# Search for a query
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Selenium Python")
search_box.send_keys(Keys.RETURN)

# Wait for results to load
time.sleep(2)

# Extract search result titles
results = driver.find_elements(By.CSS_SELECTOR, "h3")
for result in results:
    print(result.text)

# Close the driver
driver.quit()
