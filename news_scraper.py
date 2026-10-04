#!/usr/bin/env python3
"""
news_scraper.py — Scrapes news from multiple sources.
Supports: Hacker News API, BBC HTML scraping.
"""

import requests
import json
import time
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0"
}


class NewsScraper:
    def __init__(self, output_dir="output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def scrape_hackernews(self, limit=30):
        """Scrape Hacker News via official API."""
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        ids = requests.get(url, timeout=10).json()[:limit]

        articles = []
        for story_id in ids:
            try:
                item = requests.get(
                    f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                    timeout=5
                ).json()
                articles.append({
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "score": item.get("score"),
                    "author": item.get("by"),
                    "comments": item.get("descendants", 0),
                    "time": datetime.fromtimestamp(item.get("time", 0)).isoformat(),
                    "source": "HackerNews"
                })
            except Exception as e:
                logger.warning(f"Failed story {story_id}: {e}")
        return articles

    def scrape_bbc(self, limit=20):
        """Scrape BBC news homepage."""
        url = "https://www.bbc.com/news"
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "lxml")

        articles = []
        for card in soup.select("a[data-testid='internal-link']")[:limit]:
            title = card.get_text(strip=True)
            href = card.get("href", "")
            if title and href:
                articles.append({
                    "title": title,
                    "url": f"https://www.bbc.com{href}" if href.startswith("/") else href,
                    "source": "BBC",
                    "scraped_at": datetime.now().isoformat()
                })
        return articles

    def run(self):
        """Run all sources and save results."""
        all_news = []
        logger.info("Scraping HackerNews...")
        all_news.extend(self.scrape_hackernews(30))

        logger.info("Scraping BBC...")
        all_news.extend(self.scrape_bbc(20))

        out = self.output_dir / f"news_{datetime.now():%Y%m%d_%H%M%S}.json"
        with open(out, "w", encoding="utf-8") as f:
            json.dump(all_news, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(all_news)} articles → {out}")
        return all_news


if __name__ == "__main__":
    NewsScraper().run()
