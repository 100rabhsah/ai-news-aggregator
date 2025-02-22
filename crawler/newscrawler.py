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

# Define broader topics and sub-topics
broader_topics = {
    "Uttar Pradesh news": ["Lucknow news", "Kanpur news", "Varanasi news"],
    "India news": ["Delhi news", "Mumbai news", "Bangalore news"]
}

# Function to classify articles into sub-topics
def classify_article(article_text, sub_topics):
    for sub_topic in sub_topics:
        if sub_topic.lower() in article_text.lower():
            return sub_topic
    return "Other"

try:
    # Use Service to specify the chromedriver path (optional, as it should be in PATH)
    service = Service(executable_path="/usr/bin/chromedriver")
    
    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Open a news website (e.g., Times of India)
    url = "https://timesofindia.indiatimes.com/"
    driver.get(url)
    
    # Wait for the news section to load
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "list9"))
    )
    
    # Get the page source
    html = driver.page_source
    
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    
    # Locate the section containing news articles
    news_articles = soup.find_all('a', class_='w_img')
    
    # Extract and classify articles
    print("News Articles:")
    for i, article in enumerate(news_articles[:10], start=1):  # Limit to top 10 articles
        article_title = article.get('title', '').strip()
        article_link = article.get('href', '').strip()
        
        # Classify the article into sub-topics
        broader_topic = "Uttar Pradesh news"  # Example broader topic
        sub_topic = classify_article(article_title, broader_topics[broader_topic])
        
        # Print the article details
        print(f"{i}. Title: {article_title}")
        print(f"   Link: {article_link}")
        print(f"   Sub-Topic: {sub_topic}")
        print("-" * 50)
    
except Exception as e:
    print(f"An error occurred: {e}")
    
finally:
    # Close the WebDriver if it was successfully initialized
    if driver is not None:
        driver.quit()