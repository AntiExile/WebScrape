from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
                            QPushButton, QHBoxLayout, QLabel, QLineEdit, QMessageBox)
from PyQt6.QtCore import Qt
from datetime import datetime

class ResultsDialog(QDialog):
    def __init__(self, scrape_storage, content_area, parent=None):
        super().__init__(parent)
        self.scrape_storage = scrape_storage
        self.content_area = content_area
        self.setWindowTitle("Previous Scrapes")
        self.setMinimumSize(800, 600)
        self.setup_ui()
        self.load_scrapes()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search scrapes...")
        self.search_input.textChanged.connect(self.filter_results)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Results tree
        self.results_tree = QTreeWidget()
        self.results_tree.setHeaderLabels(['URL', 'Date', 'Elements Found'])
        self.results_tree.setColumnWidth(0, 300)
        self.results_tree.setColumnWidth(1, 150)
        self.results_tree.itemDoubleClicked.connect(self.load_scrape)
        layout.addWidget(self.results_tree)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        load_button = QPushButton("Load Selected")
        load_button.clicked.connect(self.load_selected_scrape)
        button_layout.addWidget(load_button)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
    
    def load_scrapes(self):
        """Load and display all saved scrapes"""
        self.results_tree.clear()
        scrapes = self.scrape_storage.load_scrapes()
        
        for scrape in scrapes:
            url = scrape['url']
            date = datetime.fromisoformat(scrape['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
            elements = len(scrape['data'].get('classes', {}))
            
            item = QTreeWidgetItem(self.results_tree, [
                url,
                date,
                f"{elements} elements"
            ])
            item.setData(0, Qt.ItemDataRole.UserRole, scrape['timestamp'])
    
    def load_selected_scrape(self):
        """Load the selected scrape into the main window"""
        selected = self.results_tree.currentItem()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select a scrape to load.")
            return
            
        timestamp = selected.data(0, Qt.ItemDataRole.UserRole)
        scrape_data = self.scrape_storage.load_scrape(timestamp)
        
        if scrape_data:
            self.content_area.url_input.setText(scrape_data['url'])
            self.content_area.current_results = scrape_data['data']
            self.content_area.update_results_view(scrape_data['data'])
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Could not load the selected scrape.")
    
    def filter_results(self, text):
        """Filter the results tree based on search text"""
        for i in range(self.results_tree.topLevelItemCount()):
            item = self.results_tree.topLevelItem(i)
            item.setHidden(
                text.lower() not in item.text(0).lower() and
                text.lower() not in item.text(2).lower()
            )
    
    def load_scrape(self, item):
        """Load a scrape when double-clicking an item"""
        # This is essentially the same as load_selected_scrape but for double-click events
        timestamp = item.data(0, Qt.ItemDataRole.UserRole)
        scrape_data = self.scrape_storage.load_scrape(timestamp)
        
        if scrape_data:
            self.content_area.url_input.setText(scrape_data['url'])
            self.content_area.current_results = scrape_data['data']
            self.content_area.update_results_view(scrape_data['data'])
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Could not load the selected scrape.")