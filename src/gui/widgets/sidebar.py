from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, pyqtSignal

class Sidebar(QWidget):
    
    record_clicked = pyqtSignal()
    settings_clicked = pyqtSignal()  # Add new signal

    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        self.setFixedWidth(200)
        layout.setSpacing(10)
        
        url_button = QPushButton("URL Input")
        url_button.setFixedHeight(40)
        url_button.setProperty("class", "sidebar-button")
        layout.addWidget(url_button)
        
        # Record button - added right after URL Input
        self.record_button = QPushButton("Record Interactions")
        self.record_button.setFixedHeight(40)
        self.record_button.setProperty("class", "sidebar-button")
        self.record_button.clicked.connect(self.record_clicked.emit)
        layout.addWidget(self.record_button)

        # Navigation buttons
        other_buttons = [
            "Scraping Options",
            "Results"
        ]
        
        for button_text in other_buttons:
            button = QPushButton(button_text)
            button.setFixedHeight(40)
            button.setProperty("class", "sidebar-button")
            layout.addWidget(button)
            
        # Settings button
        self.settings_button = QPushButton("Settings")
        self.settings_button.setFixedHeight(40)
        self.settings_button.setProperty("class", "sidebar-button")
        self.settings_button.clicked.connect(self.settings_clicked.emit)
        layout.addWidget(self.settings_button)
        
        # Help button
        help_button = QPushButton("Help")
        help_button.setFixedHeight(40)
        help_button.setProperty("class", "sidebar-button")
        layout.addWidget(help_button)
        
        layout.addStretch()
        self.setLayout(layout)
