from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        self.setFixedWidth(200)
        layout.setSpacing(10)
        
        # Navigation buttons
        buttons = [
            "URL Input",
            "Scraping Options",
            "Results",
            "Settings",
            "Help"
        ]
        
        for button_text in buttons:
            button = QPushButton(button_text)
            button.setFixedHeight(40)
            button.setProperty("class", "sidebar-button")
            layout.addWidget(button)
        
        layout.addStretch()
        self.setLayout(layout)
