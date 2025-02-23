import sqlite3

DB_PATH = "newscraper.db"

class SQLitePipeline:
    def open_spider(self, spider):
        """Initialize database connection and table creation."""
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                title TEXT,
                link TEXT UNIQUE,
                content TEXT,
                category TEXT,
                sub_category TEXT
            )
        """)
        self.conn.commit()

    def process_item(self, item, spider):
        """Insert news item into database."""
        try:
            self.cursor.execute("""
                INSERT OR IGNORE INTO news (source, title, link, content, category, sub_category)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (item['source'], item['title'], item['link'], item['content'], item['category'], item['sub_category']))
            self.conn.commit()
        except Exception as e:
            spider.logger.error(f"❌ Database Insert Error: {e}")
        
        return item

    def close_spider(self, spider):
        """Close database connection."""
        self.conn.close()
