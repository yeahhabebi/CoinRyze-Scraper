import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import json
from datetime import datetime

class CoinRyzeScraper:
    def __init__(self):
        self.base_url = "https://coinryze.org"
        self.session = requests.Session()
        self.setup_headers()
        self.scraping_log = {
            'requests_made': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'start_time': datetime.now()
        }

    def setup_headers(self):
        self.headers = {
            'User-Agent': 'EducationalScraper/1.0 (+http://github.com/yourusername/coinryze-scraper)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

    def respectful_request(self, url, delay=3):
        """Make request with rate limiting"""
        try:
            # Respectful delay
            time.sleep(delay + random.uniform(0.5, 1.5))
            
            response = self.session.get(url, headers=self.headers, timeout=10)
            self.scraping_log['requests_made'] += 1
            
            if response.status_code == 200:
                self.scraping_log['successful_requests'] += 1
                return response
            elif response.status_code == 429:
                print("Rate limited. Waiting 60 seconds...")
                time.sleep(60)
                return self.respectful_request(url, delay*2)
            else:
                self.scraping_log['failed_requests'] += 1
                print(f"Request failed with status: {response.status_code}")
                return None
                
        except Exception as e:
            self.scraping_log['failed_requests'] += 1
            print(f"Request error: {e}")
            return None

    def check_robots_txt(self):
        """Check robots.txt before scraping"""
        robots_url = f"{self.base_url}/robots.txt"
        response = self.respectful_request(robots_url, delay=1)
        if response:
            print("Robots.txt content:")
            print(response.text[:500])  # First 500 chars
        return response

    def scrape_crypto_listings(self):
        """Scrape cryptocurrency listings (example implementation)"""
        # This is a template - you'll need to inspect actual site structure
        url = f"{self.base_url}/cryptocurrencies"
        response = self.respectful_request(url)
        
        if not response:
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Example selectors - you need to inspect actual site
        crypto_data = []
        
        # Hypothetical card structure - UPDATE THESE SELECTORS
        crypto_cards = soup.find_all('div', class_='crypto-item')  # Update with actual selector
        
        for card in crypto_cards:
            try:
                # Extract data - update selectors based on actual site inspection
                name_elem = card.find('h3') or card.find('span', class_='name')
                price_elem = card.find('span', class_='price') or card.find('div', class_='value')
                
                if name_elem and price_elem:
                    crypto_data.append({
                        'name': name_elem.get_text(strip=True),
                        'price': price_elem.get_text(strip=True),
                        'timestamp': datetime.now().isoformat()
                    })
            except Exception as e:
                print(f"Error extracting data: {e}")
                continue
        
        return crypto_data

    def save_to_csv(self, data, filename):
        """Save data to CSV file"""
        if data:
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False)
            print(f"Data saved to {filename}")
        else:
            print("No data to save")

    def save_to_json(self, data, filename):
        """Save data to JSON file"""
        if data:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Data saved to {filename}")
        else:
            print("No data to save")

    def print_stats(self):
        """Print scraping statistics"""
        duration = datetime.now() - self.scraping_log['start_time']
        print(f"\n--- Scraping Statistics ---")
        print(f"Total requests: {self.scraping_log['requests_made']}")
        print(f"Successful: {self.scraping_log['successful_requests']}")
        print(f"Failed: {self.scraping_log['failed_requests']}")
        print(f"Duration: {duration}")

def main():
    print("Starting CoinRyze.org educational scraper...")
    print("NOTE: This is a template. You need to inspect the actual website structure.")
    
    scraper = CoinRyzeScraper()
    
    # Check robots.txt first
    print("1. Checking robots.txt...")
    scraper.check_robots_txt()
    
    # Scrape cryptocurrency data
    print("2. Scraping cryptocurrency listings...")
    crypto_data = scraper.scrape_crypto_listings()
    
    if crypto_data:
        print(f"Successfully scraped {len(crypto_data)} cryptocurrencies")
        
        # Save data
        scraper.save_to_csv(crypto_data, 'crypto_data.csv')
        scraper.save_to_json(crypto_data, 'crypto_data.json')
        
        # Display first few results
        print("\nFirst 3 results:")
        for i, crypto in enumerate(crypto_data[:3]):
            print(f"{i+1}. {crypto['name']}: {crypto['price']}")
    else:
        print("No data scraped. The site structure may have changed.")
        print("You need to inspect the actual website and update the CSS selectors.")
    
    # Print statistics
    scraper.print_stats()

if __name__ == "__main__":
    main()
