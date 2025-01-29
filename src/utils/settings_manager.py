import json
import os

class SettingsManager:
    def __init__(self):
        self.settings_file = "app_settings.json"
        self.default_settings = {
            'auto_scroll': True,
            'save_format': 'CSV',
            'highlight_elements': True,
            'record_screenshots': False
        }
        self.settings = self.load_settings()
    
    def save_settings(self, new_settings):
        self.settings.update(new_settings)
        with open(self.settings_file, 'w') as file:
            json.dump(self.settings, file)
    
    def get_settings(self):
        return self.settings.copy()
    
    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as file:
                return json.load(file)
        else:
            return self.default_settings.copy()