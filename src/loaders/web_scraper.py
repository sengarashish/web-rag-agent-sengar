import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict

class WebScraper:
    def __init__(self, delay: float = 2.0):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_url(self, url: str) -> Dict[str, str]:
        print(f"Fetching: {url}")
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # remove script and style elements
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()
            
            text = soup.get_text(separator=' ', strip=True)
            # basic cleanup
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            text = ' '.join(lines)
            
            return {
                'url': url,
                'content': text,
                'title': soup.title.string if soup.title else url
            }
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return {'url': url, 'content': '', 'title': url}
    
    def scrape_urls(self, urls: List[str]) -> List[Dict[str, str]]:
        results = []
        for idx, url in enumerate(urls):
            result = self.scrape_url(url)
            results.append(result)
            
            # rate limiting between requests
            if idx < len(urls) - 1:
                print(f"Waiting {self.delay}s before next request...")
                time.sleep(self.delay)
        
        return results
