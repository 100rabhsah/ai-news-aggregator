import streamlit as st
import json
import os
import time
import subprocess
from datetime import datetime, timedelta

# 🌑 Enforce Dark Theme
st.markdown("""
    <style>
        body { background-color: #0e1117; color: white; }
        .stApp { background-color: #0e1117; }
    </style>
""", unsafe_allow_html=True)

SCRAPY_PROJECT_DIR = os.path.abspath("news_scraper")
TEMP_FILE = os.path.join(SCRAPY_PROJECT_DIR, "temp_news.json")
NEWS_FILE = os.path.join(SCRAPY_PROJECT_DIR, "news.json")

def fetch_progress():
    """Fetch scraping progress from temp_news.json."""
    if os.path.exists(TEMP_FILE):
        with open(TEMP_FILE, "r") as f:
            try:
                data = json.load(f)
                return data.get("progress", 100 if data.get("status") == "complete" else 0)
            except json.JSONDecodeError:
                return 0
    return 0

def load_news():
    """Load and sort the latest news from news.json."""
    if os.path.exists(NEWS_FILE):
        with open(NEWS_FILE, "r") as f:
            try:
                articles = json.load(f)
                base_time = datetime.now()
                for i, article in enumerate(articles):
                    if "discovered" not in article:
                        article["discovered"] = (base_time.replace(microsecond=0) - 
                                                 timedelta(seconds=i)).strftime("%Y-%m-%d %H:%M:%S")
                return articles
            except json.JSONDecodeError:
                return []
    return []

st.title("📰 AI News Aggregator")

if st.button("Fetch Latest News"):
    subprocess.Popen(["python", "scraper_runner.py"])
    st.session_state["fetching"] = True
    st.rerun()

# 🏃‍♂️ Display progress bar while scraping
if "fetching" in st.session_state:
    progress_bar = st.progress(0)
    while True:
        progress = fetch_progress()
        progress_bar.progress(progress)
        if progress >= 100:
            del st.session_state["fetching"]
            st.rerun()
        time.sleep(2)

st.write("### 🗞 Latest News Articles")
news_articles = load_news()

# 🔍 Search and Categorization Filters
categories = sorted(set(article.get("category", "Uncategorized") for article in news_articles))
selected_category = st.selectbox("Select Category", ["All"] + categories)
search_query = st.text_input("🔍 Search for news topics...")

# 🏷 Filter articles based on category and search query
filtered_articles = [
    article for article in news_articles
    if (selected_category == "All" or article.get("category") == selected_category) and
       (search_query.lower() in article.get("title", "").lower() or 
        search_query.lower() in article.get("content", "").lower())
]

# 📅 Sorting Options
sort_order = st.radio("Sort by:", ("Newest First", "Oldest First"))
filtered_articles.sort(
    key=lambda article: datetime.strptime(article.get("discovered", "1970-01-01 00:00:00"), "%Y-%m-%d %H:%M:%S"),
    reverse=(sort_order == "Newest First")
)

# 📰 Display Filtered News Articles
if not filtered_articles:
    st.info("No matching news found.")
else:
    for article in filtered_articles:
        st.subheader(article.get("title", "Untitled"))
        st.write(article.get("content", "Content not available."))
        st.write(f"**Category:** {article.get('category', 'Uncategorized')}")
        st.write(f"**Discovered:** {article.get('discovered', 'Unknown')}")
        st.write("---")
