import streamlit as st
import json
import os
import time
from datetime import datetime, timedelta
import pytz

# 🌑 Enforce Dark Theme
# st.markdown("""
#     <style>
#         body { background-color: #0e1117; color: white; }
#         .stApp { background-color: #0e1117; }
#     </style>
# """, unsafe_allow_html=True)

st.markdown("""
    <style>
        /* Hide Streamlit Branding */
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .viewerBadge_container__1QSob {display: none !important;} 

        /* Hide Profile Picture (Both Sidebar & Main UI) */
        [data-testid="stSidebarUserContent"], 
        [data-testid="stUserAvatar"], 
        [data-testid="stFloatingActionButton"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)


SCRAPY_PROJECT_DIR = os.path.abspath("news_scraper")
NEWS_FILE = os.path.join(SCRAPY_PROJECT_DIR, "news.json")

IST = pytz.timezone("Asia/Kolkata")

def load_news():
    """Load and sort the latest news from news.json."""
    if os.path.exists(NEWS_FILE):
        with open(NEWS_FILE, "r") as f:
            try:
                articles = json.load(f)
                base_time = datetime.now(pytz.utc)  # Ensure it's in UTC
                for i, article in enumerate(articles):
                    if "discovered" not in article:
                        utc_time = base_time.replace(microsecond=0) - timedelta(seconds=i)
                        ist_time = utc_time.astimezone(IST)  # Convert to IST
                        article["discovered"] = ist_time.strftime("%Y-%m-%d %H:%M:%S IST")
                return articles
            except json.JSONDecodeError:
                return []
    return []
message = """
<div style="
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 40px;
    white-space: nowrap;
    overflow: hidden;
    background: linear-gradient(90deg, #ffcc00, #ff9900);
    color: black;
    font-size: 16px;
    font-weight: bold;
    border-radius: 5px;
    animation: scrollText 10s linear infinite;
">
    📰 News articles are updated every 30 minutes! Stay tuned for the latest updates!
</div>

<style>
@keyframes scrollText {
    0% { transform: translateX(100%); }
    100% { transform: translateX(-100%); }
}
</style>
"""

st.markdown(message, unsafe_allow_html=True)

st.title("📰 AI News Aggregator")

# Commented out Fetch Latest News functionality
# if st.button("Fetch Latest News"):
#     subprocess.Popen(["python", "scraper_runner.py"])
#     st.session_state["fetching"] = True
#     st.rerun()

st.write("### 📰 Latest News Articles")
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
    key=lambda article: datetime.strptime(article.get("discovered", "1970-01-01 00:00:00")[:19], "%Y-%m-%d %H:%M:%S"),
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
