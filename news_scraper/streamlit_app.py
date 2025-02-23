import streamlit as st
import json
import os

def load_articles():
    """Load articles from news.json file."""
    try:
        file_path = os.path.join(os.path.dirname(__file__), ".", "news.json")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"Error loading news data: {e}")
        return []

# Load articles from JSON
articles = load_articles()

# Categorize articles into Global & Local
global_news = [article for article in articles if article["category"] == "Global"]
local_news = [article for article in articles if article["category"] == "Local"]

# Streamlit UI
st.title("📰 AI-Powered News Aggregator")

# Dropdown to select Global or Local News
category_selection = st.selectbox("Select News Category:", ["All", "Global", "Local"])

# Search Bar
search_query = st.text_input("🔍 Search News:", "").lower().strip()

# Function to filter news based on search
def filter_news(news_list, query):
    if not query:
        return news_list  # If no search query, return all news
    return [
        article for article in news_list
        if query in article["title"].lower() or query in article["content"].lower()
    ]

# Filter news based on category and search
if category_selection == "Global":
    filtered_news = filter_news(global_news, search_query)
elif category_selection == "Local":
    filtered_news = filter_news(local_news, search_query)
else:
    filtered_news = filter_news(articles, search_query)

# Display news articles
if filtered_news:
    for article in filtered_news:
        st.markdown(f"### [{article['title']}]({article['link']})")
        st.write(article["content"])
        st.write(f"**Category:** {article['category']} > {article['sub_category']}")
        st.divider()
else:
    st.warning("No news articles found matching your search.")

