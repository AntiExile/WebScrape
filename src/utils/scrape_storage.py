import json
import os
from datetime import datetime

class ScrapeStorage:
    def __init__(self):
        self.storage_dir = "saved_scrapes"
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
            
    def save_scrape(self, url, data):
        """Save a scrape result with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scrape_{timestamp}.json"
        filepath = os.path.join(self.storage_dir, filename)
        
        scrape_data = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(scrape_data, f, indent=4)
            
        return filepath
        
    def load_scrapes(self):
        """Load all saved scrapes"""
        scrapes = []
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.storage_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    scrapes.append(json.load(f))
        return sorted(scrapes, key=lambda x: x['timestamp'], reverse=True)
        
    def load_scrape(self, timestamp):
        """Load a specific scrape by timestamp"""
        filename = f"scrape_{timestamp}.json"
        filepath = os.path.join(self.storage_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None