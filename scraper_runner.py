import subprocess
import time
import json
import os

# Set timeout (None means no timeout)
SCRAPY_TIMEOUT = 120
progress_file = "progress.json"
temp_news_file = "temp_news.json"
news_file = "news.json"

progress = {"progress": 0, "status": "idle"}

def save_progress():
    """Save progress to progress.json"""
    with open(progress_file, "w") as file:
        json.dump(progress, file, indent=4)

def run_scrapy():
    """Run the Scrapy crawler with progress tracking"""
    global progress

    progress["progress"] = 0
    progress["status"] = "starting"
    save_progress()

    process = subprocess.Popen(
        ["scrapy", "crawl", "news_scraper"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Update progress in real-time
    progress_intervals = 20  # Adjust for smoother updates
    sleep_time = 5 if SCRAPY_TIMEOUT is None else SCRAPY_TIMEOUT / progress_intervals

    for i in range(1, progress_intervals + 1):
        if process.poll() is not None:  # Exit if Scrapy process finishes early
            break
        time.sleep(sleep_time)
        progress["progress"] = int((i / progress_intervals) * 100)
        save_progress()

    process.wait()

    progress["progress"] = 100
    progress["status"] = "done"
    save_progress()

    append_news()

def append_news():
    """Append temp_news.json to news.json and remove temp file"""
    if os.path.exists(temp_news_file):
        with open(temp_news_file, "r") as temp_file:
            try:
                temp_data = json.load(temp_file)
            except json.JSONDecodeError:
                temp_data = []

        if os.path.exists(news_file):
            with open(news_file, "r") as news_file_obj:
                try:
                    existing_data = json.load(news_file_obj)
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []

        if isinstance(temp_data, list):
            existing_data.extend(temp_data)
        else:
            existing_data.append(temp_data)

        with open(news_file, "w") as news_file_obj:
            json.dump(existing_data, news_file_obj, indent=4)

        os.remove(temp_news_file)  # Remove temp file after appending

if __name__ == "__main__":
    run_scrapy()
