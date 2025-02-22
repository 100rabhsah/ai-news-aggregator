import requests
import json

def fetch_news(api_key, topic, sub_topics):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": topic,  # Main topic (e.g., "technology")
        "apiKey": api_key,  # Your NewsAPI key
        "language": "en",  # Language of articles
        "sortBy": "publishedAt",  # Sort by publication date
        "pageSize": 10  # Number of articles to fetch
    }
    
    # Make the API request
    response = requests.get(url, params=params)
    
    # Print the full API response for debugging
    print("API Response:", response.json())
    
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        
        # Filter articles based on sub-topics
        filtered_articles = []
        for article in articles:
            for sub_topic in sub_topics:
                # Check if sub-topic exists in title or content (case-insensitive)
                if (sub_topic.lower() in article["title"].lower() or 
                    sub_topic.lower() in article["content"].lower()):
                    filtered_articles.append({
                        "topic": topic,
                        "sub_topic": sub_topic,
                        "title": article["title"],
                        "content": article["content"],
                        "url": article["url"]
                    })
                    break  # Avoid duplicate entries
        
        return filtered_articles
    else:
        print(f"Error fetching news: {response.status_code}")
        return []

def save_to_json(data, filename):
    # Save the data to a JSON file
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data saved to {filename}")

# Example usage
api_key = "530dec48a9ac4ae5907570f2acf3433a"  # Replace with your actual NewsAPI key
topic = "technology"

# Define global and local sub-topics
global_sub_topics = ["artificial intelligence", "tech", "innovation", "cybersecurity"]
local_sub_topics = ["startups", "local tech", "regional", "city-based"]

# Fetch global technology news
global_articles = fetch_news(api_key, topic, global_sub_topics)
save_to_json(global_articles, "global_technology_news.json")

# Fetch local technology news
local_articles = fetch_news(api_key, topic, local_sub_topics)
save_to_json(local_articles, "local_technology_news.json")