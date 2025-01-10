from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QStackedWidget)
from PyQt6.QtCore import Qt
from .widgets.sidebar import Sidebar
from .widgets.header import Header
from .widgets.content_area import ContentArea
from .widgets.status_bar import StatusBar

class MainWindow(QMainWindow):
    def __init__(self, theme_manager):
        super().__init__()
        self.theme_manager = theme_manager
        self.setWindowTitle("WebScrape")
        self.setMinimumSize(1200, 800)
        
        # Create main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setStyleSheet("QWidget { font-family: Arial; }")
        
        # Initialize UI components
        self.setup_ui()
        
        # Apply initial theme
        self.theme_manager.apply_theme(self)
    
    def setup_ui(self):
        # Add header
        self.header = Header(self.theme_manager)
        self.layout.addWidget(self.header)
        
        # Create main content layout
        content_layout = QHBoxLayout()
        
        # Add sidebar
        self.sidebar = Sidebar()
        content_layout.addWidget(self.sidebar)
        
        # Add main content area
        self.content_area = ContentArea()
        content_layout.addWidget(self.content_area)
        
        # Add content layout to main layout
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        self.layout.addWidget(content_widget)
        
        # Add status bar
        self.status_bar = StatusBar()
        self.layout.addWidget(self.status_bar)
