#!/usr/bin/env python3
import requests
import csv
import re
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

class ProductScraper:
    HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PriceMonitor/1.0)"}

    def __init__(self, output_dir="output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def scrape_books_to_scrape(self, pages=5):
        base = "https://books.toscrape.com/catalogue/page-{}.html"
        products = []
        for page in range(1, pages + 1):
            r = requests.get(base.format(page), headers=self.HEADERS, timeout=15)
            soup = BeautifulSoup(r.text, "lxml")
            for card in soup.select("article.product_pod"):
                title_el = card.select_one("h3 a")
                price_el = card.select_one("p.price_color")
                stock_el = card.select_one("p.instock.availability")
                products.append({
                    "title": title_el.get("title") if title_el else None,
                    "price": self._parse_price(price_el.get_text() if price_el else ""),
                    "currency": "GBP",
                    "in_stock": "In stock" in (stock_el.get_text() if stock_el else ""),
                    "scraped_at": datetime.now().isoformat()
                })
        return products

    def _parse_price(self, text):
        m = re.search(r"[\d.]+", text)
        return float(m.group()) if m else None

    def run(self):
        products = self.scrape_books_to_scrape()
        out = self.output_dir / f"products_{datetime.now():%Y%m%d}.csv"
        with open(out, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=products[0].keys())
            writer.writeheader()
            writer.writerows(products)
        print(f"[+] Saved {len(products)} products -> {out}")
        return products

if __name__ == "__main__":
    ProductScraper().run()
