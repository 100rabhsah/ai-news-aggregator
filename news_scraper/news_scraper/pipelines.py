import json
import os

class NewsScraperPipeline:
    def open_spider(self, spider):
        # Ensure the file is created and opened in write mode
        self.file_path = "news.json"
        if os.path.exists(self.file_path):
            os.remove(self.file_path)  # Remove existing file to avoid duplicate entries
        
        self.file = open(self.file_path, "w", encoding="utf-8")
        self.file.write("[\n")  # Start JSON array
        self.first_item = True

    def close_spider(self, spider):
        self.file.write("\n]")  # Close JSON array
        self.file.close()

    def process_item(self, item, spider):
        # Add a comma before adding a new JSON object (except for the first one)
        if not self.first_item:
            self.file.write(",\n")
        self.first_item = False
        
        # Write item as JSON
        json.dump(dict(item), self.file, ensure_ascii=False, indent=4)
        return item
