from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QStackedWidget, 
    QLineEdit, QPushButton, QTextEdit, QMessageBox, QTreeWidget, QTreeWidgetItem, QHBoxLayout, QFileDialog)
from PyQt6.QtCore import Qt
from src.scraping.scraper import WebScraper
import json

class ContentArea(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # URL input section
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL to scrape...")
        self.url_input.setFixedHeight(40)
        
        # Start button
        self.start_button = QPushButton("Start Scraping")
        self.start_button.setFixedHeight(40)
        self.start_button.setProperty("class", "primary-button")
        self.start_button.clicked.connect(self.start_scraping)
        
        # Button container
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        
        # Save button
        self.save_button = QPushButton("Save Results")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_results)
        button_layout.addWidget(self.save_button)
        
        # Results area
        self.results_tree = QTreeWidget()
        self.results_tree.setHeaderLabels(['Element', 'Details'])
        self.results_tree.setColumnWidth(0, 200)
        
        self.raw_results = QTextEdit()
        self.raw_results.setReadOnly(True)
        
        # Initialize scraper
        self.scraper = WebScraper()
        self.setup_scraper_connections()
        
        layout.addWidget(self.url_input)
        layout.addLayout(button_layout)
        layout.addWidget(self.results_tree)
        layout.addWidget(self.raw_results)
        
        self.setLayout(layout)
        self.current_results = None  # Store current results

    def setup_scraper_connections(self):
        self.scraper.progress_updated.connect(self.update_progress)
        self.scraper.status_updated.connect(self.update_status)
        self.scraper.scraping_completed.connect(self.display_results)
        self.scraper.error_occurred.connect(self.show_error)

    def start_scraping(self):
        url = self.url_input.text().strip()
        if not url:
            self.show_error("Please enter a URL")
            return

        self.start_button.setEnabled(False)
        self.results_tree.clear()
        self.raw_results.clear()
        self.scraper.scrape(url)

    def update_progress(self, value):
        status_bar = self.window().status_bar
        status_bar.progress_bar.setVisible(True)
        status_bar.progress_bar.setValue(value)

    def update_status(self, message):
        self.window().status_bar.status_label.setText(message)

    def display_results(self, data):
        self.start_button.setEnabled(True)
        self.save_button.setEnabled(True)
        self.current_results = data
        
        # Display raw JSON data
        formatted_results = json.dumps(data, indent=2)
        self.raw_results.setText(formatted_results)
        
        # Clear and populate the tree widget
        self.results_tree.clear()
        
        # Add basic information
        basic_info = QTreeWidgetItem(self.results_tree, ['Basic Information'])
        QTreeWidgetItem(basic_info, ['Title', data.get('title', 'No title')])
        
        # Add classes information
        classes_root = QTreeWidgetItem(self.results_tree, ['HTML Classes'])
        classes = data.get('classes', {})
        
        for class_name, info in classes.items():
            class_item = QTreeWidgetItem(classes_root, [
                class_name,
                f"Used {info['count']} times"
            ])
            
            # Add tag types
            tags_item = QTreeWidgetItem(class_item, [
                'Tag Types',
                ', '.join(info['tag_types'])
            ])
            
            # Add sample content
            if info['sample_content']:
                samples_item = QTreeWidgetItem(class_item, ['Sample Content'])
                for sample in info['sample_content']:
                    QTreeWidgetItem(samples_item, ['Sample', sample[:100]])
        
        self.results_tree.expandToDepth(1)
        
        self.window().status_bar.progress_bar.setVisible(False)

    def show_error(self, message):
        self.start_button.setEnabled(True)
        self.save_button.setEnabled(False)
        QMessageBox.critical(self, "Error", message)
        self.window().status_bar.status_label.setText("Ready")
        self.window().status_bar.progress_bar.setVisible(False)

    def save_results(self):
        if not self.current_results:
            return
            
        file_dialog = QFileDialog(self)
        file_dialog.setDefaultSuffix('json')
        file_dialog.setNameFilter('JSON Files (*.json);;CSV Files (*.csv);;HTML Files (*.html)')
        
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if not selected_files:
                return
                
            file_path = selected_files[0]
            file_format = file_path.split('.')[-1].lower()
            
            try:
                if file_format == 'json':
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(self.current_results, f, indent=2)
                elif file_format == 'csv':
                    self.save_as_csv(file_path)
                elif file_format == 'html':
                    self.save_as_html(file_path)
                    
                self.window().status_bar.status_label.setText(f"Results saved to {file_path}")
            except Exception as e:
                self.show_error(f"Error saving file: {str(e)}")
