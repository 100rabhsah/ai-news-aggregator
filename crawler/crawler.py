import requests
from bs4 import BeautifulSoup
import sqlite3
import time

# Step 1: Fetch and parse news articles
def fetch_articles(url, category, num_pages=10):  # Fetch 10 pages per source
    articles = []
    try:
        for page in range(1, num_pages + 1):
            print(f"Fetching page {page} of {url}...")
            if "bbc.com" in url:
                # BBC News
                response = requests.get(f"{url}?page={page}")
            elif "indiatimes.com" in url:
                # Times of India
                response = requests.get(f"{url}?page={page}")
            elif "thehindu.com" in url:
                # The Hindu
                response = requests.get(f"{url}?page={page}")
            elif "techcrunch.com" in url:
                # TechCrunch
                response = requests.get(f"{url}/page/{page}")
            
            response.raise_for_status()  # Raise an error for bad status codes
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Debug: Print the HTML content of the page
            # print(soup.prettify())
            
            # Adjust the following selectors based on the website's structure
            if "bbc.com" in url:
                # BBC News
                for article in soup.find_all("div", class_="gs-c-promo"):
                    title = article.find("h3", class_="gs-c-promo-heading__title")
                    content = article.find("p", class_="gs-c-promo-summary")
                    if title and content:
                        articles.append({
                            "title": title.text.strip(),
                            "content": content.text.strip(),
                            "source": url,
                            "category": category
                        })
                        print(f"Found article: {title.text.strip()}")
            elif "indiatimes.com" in url:
                # Times of India
                for article in soup.find_all("div", class_="article"):
                    title = article.find("span", class_="w_tle")
                    content = article.find("p", class_="w_desc")
                    if title and content:
                        articles.append({
                            "title": title.text.strip(),
                            "content": content.text.strip(),
                            "source": url,
                            "category": category
                        })
                        print(f"Found article: {title.text.strip()}")
            elif "thehindu.com" in url:
                # The Hindu
                for article in soup.find_all("div", class_="story-card"):
                    title = article.find("h2", class_="title")
                    content = article.find("p", class_="intro")
                    if title and content:
                        articles.append({
                            "title": title.text.strip(),
                            "content": content.text.strip(),
                            "source": url,
                            "category": category
                        })
                        print(f"Found article: {title.text.strip()}")
            elif "techcrunch.com" in url:
                # TechCrunch
                for article in soup.find_all("div", class_="post-block"):
                    title = article.find("h2", class_="post-block__title")
                    content = article.find("div", class_="post-block__content")
                    if title and content:
                        articles.append({
                            "title": title.text.strip(),
                            "content": content.text.strip(),
                            "source": url,
                            "category": category
                        })
                        print(f"Found article: {title.text.strip()}")
            
            # Add a delay to avoid overwhelming the server
            time.sleep(2)
        
        return articles
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

# Step 2: Classify and store articles
def store_articles():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("news_articles.db")
    cursor = conn.cursor()

    # Create a table to store articles
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                source TEXT,
                category TEXT,
                subtopic TEXT
            )
        """)
        conn.commit()
        print("Table 'articles' created or already exists.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

    # Hardcoded topics and subtopics
    broader_topic = "Technology News"
    subtopics = ["Artificial Intelligence", "Cybersecurity"]

    # Fetch and store articles
    sources = [
        ("https://www.bbc.com/news/technology", broader_topic),  # BBC for technology news
        ("https://timesofindia.indiatimes.com/technology", broader_topic),  # Times of India for technology news
        ("https://www.thehindu.com/sci-tech/technology", broader_topic),  # The Hindu for technology news
        ("https://techcrunch.com/category/artificial-intelligence", subtopics[0]),  # TechCrunch for AI news
        ("https://techcrunch.com/category/security", subtopics[1])  # TechCrunch for cybersecurity news
    ]

    for url, category in sources:
        articles = fetch_articles(url, category, num_pages=10)  # Fetch 10 pages per source
        for article in articles:
            try:
                cursor.execute("""
                    INSERT INTO articles (title, content, source, category, subtopic)
                    VALUES (?, ?, ?, ?, ?)
                """, (article["title"], article["content"], article["source"], article["category"], category))
                conn.commit()
                print(f"Inserted article: {article['title']}")
            except sqlite3.Error as e:
                print(f"Error inserting article: {e}")

    # Close the database connection
    conn.close()

# Run the crawler
if __name__ == "__main__":
    store_articles()
    print("Crawling completed. Data stored in 'news_articles.db'.")