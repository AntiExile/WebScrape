from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt6.QtCore import Qt

class Header(QWidget):
    def __init__(self, theme_manager):
        super().__init__()
        self.theme_manager = theme_manager
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.setFixedHeight(160)  # Keep height
        
        # Top row with title only
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(20, 5, 20, 30)  # Reduced top margin to 5
        
        # Title with adjusted positioning
        title = QLabel("WebScrape")
        title.setStyleSheet("""
            font-size: 32px; 
            font-weight: bold; 
            padding: 0px 10px;  /* Removed top padding */
            margin-top: 0px;    /* Removed top margin */
        """)
        title.setFixedHeight(40)  # Reduced height
        
        top_layout.addWidget(title)
        top_layout.addStretch()
        
        # Middle row with URL input
        middle_layout = QHBoxLayout()
        middle_layout.setContentsMargins(20, 20, 20, 10)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL to scrape...")
        self.url_input.setFixedHeight(35)
        middle_layout.addWidget(self.url_input)
        
        # Bottom row with buttons - adjusted margins
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 10, 0, 5)
        
        self.start_button = QPushButton("Start Scraping")
        self.start_button.setFixedHeight(30)
        self.start_button.setProperty("class", "primary-button")
        
        self.save_button = QPushButton("Save Results")
        self.save_button.setFixedHeight(30)
        self.save_button.setEnabled(False)
        self.save_button.setObjectName("save_button")
        
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.start_button)
        bottom_layout.addWidget(self.save_button)
        bottom_layout.addStretch()
        
        # Add all layouts to main layout
        main_layout.addLayout(top_layout)
        main_layout.addLayout(middle_layout)
        main_layout.addLayout(bottom_layout)
        
        self.setLayout(main_layout)
