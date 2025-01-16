from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

class Header(QWidget):
    def __init__(self, theme_manager):
        super().__init__()
        self.theme_manager = theme_manager
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout()
        self.setFixedHeight(60)
        
        # Title
        title = QLabel("WebScrape")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        
        # Theme toggle button
        self.theme_button = QPushButton("Toggle Theme")
        self.theme_button.setFixedWidth(120)
        self.theme_button.clicked.connect(lambda: self.theme_manager.toggle_theme(self.window()))
        
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self.theme_button)
        layout.setContentsMargins(20, 0, 20, 0)
        
        self.setLayout(layout)
