from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without GUI
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--log-level=3")  # Suppress warnings
chrome_options.add_argument("--no-sandbox")  # Required for Linux
chrome_options.add_argument("--disable-dev-shm-usage")  # Required for Linux
chrome_options.add_argument("--user-data-dir=/tmp/chrome-profile")  # Unique user data directory
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
)

# Initialize WebDriver with increased timeout
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

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
    # Open a news website
    url = "https://timesofindia.indiatimes.com/"
    driver.get(url)

    # Wait for articles to load (use a more reliable selector)
    WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/city/']"))
    )

    # Get the page source
    html = driver.page_source

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Locate the section containing news articles
    news_articles = soup.select("a[href*='/city/']")[:10]  # Top 10 news links

    # Extract and classify articles
    print("\nNews Articles:")
    for i, article in enumerate(news_articles, start=1):
        article_title = article.get_text(strip=True)
        article_link = article["href"]

        # Ensure full URL
        if not article_link.startswith("http"):
            article_link = f"https://timesofindia.indiatimes.com{article_link}"

        # Classify article
        broader_topic = "Uttar Pradesh news"  # Example broader topic
        sub_topic = classify_article(article_title, broader_topics[broader_topic])

        # Print results
        print(f"{i}. Title: {article_title}")
        print(f"   Link: {article_link}")
        print(f"   Sub-Topic: {sub_topic}")
        print("-" * 50)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()