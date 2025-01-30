import json
import os
from datetime import datetime
from pathlib import Path

class ScrapeStorage:
    def __init__(self):
        # Get user's documents folder
        self.storage_dir = os.path.join(
            str(Path.home()), 
            "Documents", 
            "WebScrape",
            "saved_scrapes"
        )
        print(f"Storage directory path: {self.storage_dir}")  # Debug print
        
        # Create directories if they don't exist
        if not os.path.exists(self.storage_dir):
            print(f"Creating directory: {self.storage_dir}")  # Debug print
            os.makedirs(self.storage_dir, exist_ok=True)  # Added exist_ok=True for safety
            
    def save_scrape(self, url, data):
        """Save a scrape result with timestamp to user's documents"""
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

    def delete_scrape(self, timestamp):
        """Delete a specific scrape by timestamp"""
        try:
            # List all files in the directory
            for filename in os.listdir(self.storage_dir):
                if filename.endswith('.json') and timestamp in filename:
                    filepath = os.path.join(self.storage_dir, filename)
                    os.remove(filepath)
                    return True
            return False
        except Exception as e:
            print(f"Error deleting scrape: {e}")
            return False