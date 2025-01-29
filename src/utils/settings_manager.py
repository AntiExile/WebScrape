class SettingsManager:
    def __init__(self):
        self.settings = {
            'auto_scroll': True,
            'save_format': 'CSV',
            'highlight_elements': True,
            'record_screenshots': False
        }
    
    def save_settings(self, new_settings):
        self.settings.update(new_settings)
    
    def get_settings(self):
        return self.settings.copy()