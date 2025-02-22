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

# Initialize WebDriver
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

# Define website configurations
website_configs = {
    "Times of India": {
        "url": "https://timesofindia.indiatimes.com/",
        "article_selector": "div[class*='fewcent-'], div.js_tbl_article",  # Refined selector
        "content_selector": "div._3YYSt.clearfix",  # Selector for article content
    }
}

try:
    for source_name, config in website_configs.items():
        print(f"\nScraping articles from: {source_name}")

        # Open the news website
        driver.get(config["url"])

        # Wait for articles to load
        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, config["article_selector"]))
        )

        # Get the page source
        html = driver.page_source

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # Locate the section containing news articles
        news_articles = soup.select(config["article_selector"])[:10]  # Top 10 news articles

        # Extract and classify articles
        print(f"\nNews Articles from {source_name}:")
        for i, article in enumerate(news_articles, start=1):
            try:
                # Extract article title
                article_title = article.select_one("figcaption").get_text(strip=True)

                # Extract article link
                article_link = article.select_one("a.Hn2z7")["href"]
                if not article_link.startswith("http"):
                    article_link = f"https://timesofindia.indiatimes.com{article_link}"

                # Extract article image
                article_image = article.select_one("img")["src"]

                # Navigate to the article page to fetch the full content
                driver.get(article_link)
                WebDriverWait(driver, 50).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, config["content_selector"]))
                )
                article_html = driver.page_source
                article_soup = BeautifulSoup(article_html, "html.parser")

                # Extract the full article content
                article_content = article_soup.select_one(config["content_selector"])
                if article_content:
                    article_content = article_content.get_text(strip=True)
                else:
                    article_content = "Content not found"

                # Classify article
                broader_topic = "India news"  # Example broader topic
                sub_topic = classify_article(article_content, broader_topics[broader_topic])

                # Print results
                print(f"{i}. Title: {article_title}")
                print(f"   Link: {article_link}")
                print(f"   Image: {article_image}")
                print(f"   Sub-Topic: {sub_topic}")
                print(f"   Content: {article_content}")
                print("-" * 50)
            except Exception as e:
                print(f"Error processing article {i}: {e}")
                continue

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()