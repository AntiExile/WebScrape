from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout)
from PyQt6.QtCore import Qt
from .widgets.sidebar import Sidebar
from .widgets.header import Header
from .widgets.content_area import ContentArea
from .widgets.status_bar import StatusBar
from .widgets.settings_dialog import SettingsDialog  # Add this import
from src.utils.settings_manager import SettingsManager  # Add this import
from .widgets.results_dialog import ResultsDialog  # Add this import
from src.utils.scrape_storage import ScrapeStorage  # Add this import

class MainWindow(QMainWindow):
    def __init__(self, theme_manager):
        super().__init__()
        self.theme_manager = theme_manager
        self.settings_manager = SettingsManager()  # Add settings manager
        self.scrape_storage = ScrapeStorage()  # Add this line
        self.setWindowTitle("WebScrape")
        self.setMinimumSize(1200, 800)
        
        # Add this line to make the window fullscreen by default
        self.showMaximized()
        
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
        self.sidebar.settings_clicked.connect(self.show_settings)  # Add this line
        self.sidebar.results_clicked.connect(self.show_results)  # Add this line
        self.sidebar.unload_clicked.connect(self.content_area.unload_current_scrape)  # Add this line
        
    def show_settings(self):
        settings_dialog = SettingsDialog(self.settings_manager, self)
        if settings_dialog.exec():
            # Settings were saved, update any necessary components
            settings = self.settings_manager.get_settings()
            self.content_area.update_settings(settings)
            
    def show_results(self):
        """Show the results dialog"""
        results_dialog = ResultsDialog(self.scrape_storage, self.content_area, self)
        results_dialog.exec()
