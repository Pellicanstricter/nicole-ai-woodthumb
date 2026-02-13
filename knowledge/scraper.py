"""
Wood Thumb Website Scraper
Extracts content from woodthumb.com to build Nicole's knowledge base
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List
import json


class WoodThumbScraper:
    def __init__(self):
        self.base_url = "https://woodthumb.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

    def scrape_page(self, url: str) -> Dict[str, str]:
        """Scrape a single page and extract text content"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()

            # Get text
            text = soup.get_text(separator='\n', strip=True)

            # Get title
            title = soup.find('title')
            title_text = title.string if title else ""

            return {
                'url': url,
                'title': title_text,
                'content': text
            }
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return {'url': url, 'title': '', 'content': ''}

    def scrape_all(self) -> List[Dict[str, str]]:
        """Scrape main pages from Wood Thumb website"""
        pages = [
            self.base_url,
            f"{self.base_url}/workshops",
            f"{self.base_url}/shop-time",
            f"{self.base_url}/team-events",
            f"{self.base_url}/custom-work",
            f"{self.base_url}/about",
            f"{self.base_url}/contact",
        ]

        results = []
        for page in pages:
            print(f"Scraping {page}...")
            data = self.scrape_page(page)
            if data['content']:
                results.append(data)

        return results

    def save_to_file(self, data: List[Dict[str, str]], filename: str = "woodthumb_raw.json"):
        """Save scraped data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Saved to {filename}")


if __name__ == "__main__":
    scraper = WoodThumbScraper()
    data = scraper.scrape_all()
    scraper.save_to_file(data, "knowledge/woodthumb_raw.json")
    print(f"\nScraped {len(data)} pages successfully!")
