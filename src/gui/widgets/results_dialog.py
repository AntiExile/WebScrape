from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
                            QPushButton, QHBoxLayout, QLabel, QLineEdit, QMessageBox)
from PyQt6.QtCore import Qt, QUrl
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
        
        # Results tree with multiple selection enabled
        self.results_tree = QTreeWidget()
        self.results_tree.setSelectionMode(QTreeWidget.SelectionMode.MultiSelection)  # Enable multiple selection
        self.results_tree.setHeaderLabels(['URL', 'Date', 'Elements Found'])
        self.results_tree.setColumnWidth(0, 300)
        self.results_tree.setColumnWidth(1, 150)
        self.results_tree.itemDoubleClicked.connect(self.load_scrape)
        layout.addWidget(self.results_tree)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Selection info label
        self.selection_label = QLabel("0 items selected")
        button_layout.addWidget(self.selection_label)
        
        button_layout.addStretch()
        
        load_button = QPushButton("Load Selected")
        load_button.clicked.connect(self.load_selected_scrape)
        button_layout.addWidget(load_button)
        
        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_selected_scrapes)
        button_layout.addWidget(delete_button)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        # Connect selection changed signal
        self.results_tree.itemSelectionChanged.connect(self.update_selection_count)

    def update_selection_count(self):
        """Update the selection count label"""
        count = len(self.results_tree.selectedItems())
        self.selection_label.setText(f"{count} item{'s' if count != 1 else ''} selected")

    def delete_selected_scrapes(self):
        """Delete multiple selected scrapes"""
        selected_items = self.results_tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select scrapes to delete.")
            return
            
        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete {len(selected_items)} selected scrape(s)?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            deleted_count = 0
            for item in selected_items:
                date_str = item.text(1)
                try:
                    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    timestamp = dt.strftime("%Y%m%d_%H%M%S")
                    
                    if self.scrape_storage.delete_scrape(timestamp):
                        root = self.results_tree.invisibleRootItem()
                        root.removeChild(item)
                        deleted_count += 1
                except ValueError as e:
                    print(f"Error processing date: {e}")
                    
            if deleted_count > 0:
                QMessageBox.information(self, "Success", 
                    f"Successfully deleted {deleted_count} scrape{'s' if deleted_count != 1 else ''}.")
            else:
                QMessageBox.critical(self, "Error", "Could not delete any scrapes.")
            
            self.update_selection_count()
    
    def load_scrapes(self):
        """Load and display all saved scrapes"""
        self.results_tree.clear()
        scrapes = self.scrape_storage.load_scrapes()
        
        for scrape in scrapes:
            url = scrape.get('url', 'No URL')
            date = datetime.fromisoformat(scrape['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
            
            # Get content from nested data structure
            content = None
            if 'data' in scrape and 'content' in scrape['data']:
                content = scrape['data']['content']
            elif 'content' in scrape:
                content = scrape['content']
            
            # Calculate total elements
            element_count = 0
            if content:
                # Count elements from all categories
                if 'classes' in content:
                    for class_info in content['classes'].values():
                        element_count += class_info.get('count', 0)
                if 'headings' in content:
                    element_count += len(content['headings'])
                if 'links' in content:
                    element_count += len(content['links'])
                if 'images' in content:
                    element_count += len(content['images'])
                if 'forms' in content:
                    element_count += len(content['forms'])
                    # Count form inputs
                    for form in content['forms']:
                        element_count += len(form.get('inputs', []))
            
            item = QTreeWidgetItem(self.results_tree, [
                url,
                date,
                f"{element_count} elements"
            ])
            
            # Store timestamp for loading
            save_timestamp = datetime.fromisoformat(scrape['timestamp']).strftime("%Y%m%d_%H%M%S")
            item.setData(0, Qt.ItemDataRole.UserRole, save_timestamp)
    
    def load_selected_scrape(self):
        """Load the selected scrape into the main window"""
        selected_items = self.results_tree.selectedItems()
        
        # Check if multiple items are selected
        if len(selected_items) > 1:
            QMessageBox.warning(
                self,
                "Multiple Selection",
                "Please select only one scrape to load at a time.",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Check if no items are selected
        if not selected_items:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a scrape to load.",
                QMessageBox.StandardButton.Ok
            )
            return
        
        try:
            # First unload any current scrape
            self.content_area.unload_current_scrape()
            
            # Get the timestamp stored in UserRole
            selected = selected_items[0]  # We know we have exactly one item
            timestamp = selected.data(0, Qt.ItemDataRole.UserRole)
            
            # Load the scrape data
            scrape_data = self.scrape_storage.load_scrape(timestamp)
            
            if scrape_data:
                # Update URL input
                self.content_area.url_input.setText(scrape_data.get('url', ''))
                
                # Get the content from the proper structure
                if 'data' in scrape_data and 'content' in scrape_data['data']:
                    content = scrape_data['data']['content']
                else:
                    content = scrape_data.get('content', {})
                
                # Update current results
                self.content_area.current_results = content
                
                # Update views
                self.content_area.update_results_view(content)
                
                # Load URL in browser if available
                if scrape_data.get('url'):
                    self.content_area.browser_view.setUrl(QUrl(scrape_data['url']))
                
                self.accept()
                QMessageBox.information(self, "Success", "Scrape loaded successfully!")
            else:
                QMessageBox.critical(self, "Error", "Could not find the selected scrape file.")
                
        except Exception as e:
            print(f"Error loading scrape: {e}")  # Debug print
            QMessageBox.critical(self, "Error", f"Failed to load scrape: {str(e)}")
    
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