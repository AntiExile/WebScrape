from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout)
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
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        self.setup_ui()
        self.theme_manager.apply_theme(self)
    
    def setup_ui(self):
        # Add header
        self.header = Header(self.theme_manager)
        self.layout.addWidget(self.header)
        
        # Main content area with sidebar
        content_layout = QHBoxLayout()
        
        self.sidebar = Sidebar()
        content_layout.addWidget(self.sidebar)
        
        self.content_area = ContentArea()
        content_layout.addWidget(self.content_area)
        
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        self.layout.addWidget(content_widget)
        
        # Add status bar
        self.status_bar = StatusBar()
        self.layout.addWidget(self.status_bar)
        
        # Connect signals
        self.sidebar.record_clicked.connect(self.content_area.toggle_recording)
