import streamlit as st
import json
import os
import time
from datetime import datetime, timedelta

SCRAPY_PROJECT_DIR = os.path.abspath("news_scraper")
NEWS_FILE = os.path.join(SCRAPY_PROJECT_DIR, "news.json")

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

st.write("### 🗢 Latest News Articles")
news_articles = load_news()

# 🔍 Search and Categorization Filters
categories = sorted(set(article.get("category", "Uncategorized") for article in news_articles))
selected_category = st.selectbox("Select Category", ["All"] + categories)

# 🏷 Dynamically get sub-categories based on selected category
if selected_category == "All":
    subcategories = sorted(set(article.get("subcategory", "General") for article in news_articles))
else:
    subcategories = sorted(set(article.get("subcategory", "General") 
                               for article in news_articles if article.get("category") == selected_category))

selected_subcategory = st.selectbox("Select Sub-Category", ["All"] + subcategories)

search_query = st.text_input("🔍 Search for news topics...")

# 🏷 Filter articles based on category, sub-category, and search query
filtered_articles = [
    article for article in news_articles
    if (selected_category == "All" or article.get("category") == selected_category) and
       (selected_subcategory == "All" or article.get("subcategory") == selected_subcategory) and
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
        st.write(f"**Sub-Category:** {article.get('subcategory', 'General')}")
        st.write(f"**Discovered:** {article.get('discovered', 'Unknown')}")
        st.write("---")
