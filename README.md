# AI News Aggregator

An autonomous AI agent that crawls, summarizes, and publishes news articles.

## Overview

The AI News Aggregator is designed to autonomously gather news articles from various sources, generate concise summaries using advanced natural language processing techniques, and publish these summaries on a user-friendly web interface.

## Features

- **Automated Web Crawling**: Collects the latest news articles from multiple sources.
- **AI-Powered Summarization**: Utilizes state-of-the-art models to generate concise summaries.
- **Seamless Publishing**: Automatically updates the frontend with the latest summaries.

## Team Members

- **Sourabh Sah**: Web Crawling and Data Extraction
- **Ravi Prakash Srivastava**: Summarization and Blog Generation
- **Nainika Anand**: Publishing and Frontend Integration

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/100rabhsah/ai-news-aggregator.git
   cd ai-news-aggregator
   ```


2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```


3. **Configure Environment Variables**:
   - Create a `.env` file in the root directory.
   - Add necessary environment variables (e.g., API keys, database credentials).

4. **Run the Application**:
   ```bash
   python main.py
   ```


## Directory Structure


```
ai-news-aggregator/
├── crawler/          # Contains web crawling scripts
├── summarizer/       # Modules for article summarization
├── database/         # Database models and connectors
├── frontend/         # Frontend application code
├── main.py           # Entry point of the application
├── requirements.txt  # List of dependencies
└── README.md         # Project documentation
```


## Contributing

We welcome contributions from the community. To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

