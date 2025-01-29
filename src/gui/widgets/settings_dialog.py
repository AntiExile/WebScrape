from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QCheckBox, QComboBox, QFormLayout)
from PyQt6.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.setWindowTitle("Settings")
        self.setMinimumWidth(400)
        self.setup_ui()
        self.load_current_settings()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Create form layout for settings
        form_layout = QFormLayout()
        
        # Scraping settings
        self.auto_scroll = QCheckBox()
        form_layout.addRow("Auto-scroll during scraping:", self.auto_scroll)
        
        self.save_format = QComboBox()
        self.save_format.addItems(["CSV", "HTML", "JSON"])
        form_layout.addRow("Default save format:", self.save_format)
        
        self.highlight_elements = QCheckBox()
        form_layout.addRow("Highlight interacted elements:", self.highlight_elements)
        
        self.record_screenshots = QCheckBox()
        form_layout.addRow("Record screenshots:", self.record_screenshots)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
    
    def load_current_settings(self):
        settings = self.settings_manager.get_settings()
        self.auto_scroll.setChecked(settings['auto_scroll'])
        self.save_format.setCurrentText(settings['save_format'])
        self.highlight_elements.setChecked(settings['highlight_elements'])
        self.record_screenshots.setChecked(settings['record_screenshots'])
    
    def save_settings(self):
        new_settings = {
            'auto_scroll': self.auto_scroll.isChecked(),
            'save_format': self.save_format.currentText(),
            'highlight_elements': self.highlight_elements.isChecked(),
            'record_screenshots': self.record_screenshots.isChecked()
        }
        self.settings_manager.save_settings(new_settings)
        self.accept()