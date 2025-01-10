import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from PyQt6.QtCore import QObject, pyqtSignal

class WebScraper(QObject):
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    scraping_completed = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.session = requests.Session()
    
    def validate_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def scrape(self, url):
        try:
            if not self.validate_url(url):
                self.error_occurred.emit("Invalid URL format")
                return
                
            self.status_updated.emit("Starting scraping...")
            self.progress_updated.emit(10)
            
            response = self.session.get(url)
            response.raise_for_status()
            
            self.progress_updated.emit(30)
            self.status_updated.emit("Parsing content...")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get all unique classes and their elements
            class_data = {}
            for element in soup.find_all(class_=True):
                classes = element.get('class')
                for class_name in classes:
                    if class_name not in class_data:
                        class_data[class_name] = {
                            'count': 0,
                            'tag_types': set(),
                            'sample_content': []
                        }
                    class_data[class_name]['count'] += 1
                    class_data[class_name]['tag_types'].add(element.name)
                    if len(class_data[class_name]['sample_content']) < 3:
                        sample = element.get_text().strip()
                        if sample:
                            class_data[class_name]['sample_content'].append(sample)
            
            data = {
                'title': soup.title.string if soup.title else 'No title',
                'links': [{'text': a.text, 'href': a.get('href')} 
                          for a in soup.find_all('a', href=True)],
                'headings': [h.text for h in soup.find_all(['h1', 'h2', 'h3'])],
                'paragraphs': [p.text for p in soup.find_all('p')],
                'classes': {
                    class_name: {
                        'count': info['count'],
                        'tag_types': list(info['tag_types']),
                        'sample_content': info['sample_content']
                    }
                    for class_name, info in class_data.items()
                }
            }
            
            self.progress_updated.emit(90)
            self.status_updated.emit("Finalizing results...")
            self.scraping_completed.emit(data)
            self.progress_updated.emit(100)
            self.status_updated.emit("Scraping completed!")
            
        except requests.RequestException as e:
            self.error_occurred.emit(f"Network error: {str(e)}")
        except Exception as e:
            self.error_occurred.emit(f"Scraping error: {str(e)}")
