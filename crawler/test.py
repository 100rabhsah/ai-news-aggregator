from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without GUI
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
)

# Initialize WebDriver
driver = None  # Initialize driver variable

try:
    # Use Service to specify the chromedriver path (optional, as it should be in PATH)
    service = Service(executable_path="/usr/bin/chromedriver")
    
    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Open the Naukri Gulf "Top Jobs by Designation" page
    url = "https://www.naukrigulf.com/top-jobs-by-designation"
    driver.get(url)
    
    # Wait for the required section to load (with the correct class name)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "soft-link"))
    )
    
    # Get the page source
    html = driver.page_source
    
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    
    # Locate the section containing job titles
    job_profiles_section = soup.find_all('a', class_='soft-link darker')
    
    # Extract and print top job profiles
    print("Top Job Profiles:")
    for i, job in enumerate(job_profiles_section[:10], start=1):  # Limit to top 10
        print(f"{i}. {job.text.strip()}")
    
except Exception as e:
    print(f"An error occurred: {e}")
    
finally:
    # Close the WebDriver if it was successfully initialized
    if driver is not None:
        driver.quit()