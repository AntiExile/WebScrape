from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QStackedWidget, 
    QLineEdit, QPushButton, QTextEdit, QMessageBox, QTreeWidget, 
    QTreeWidgetItem, QHBoxLayout, QFileDialog, QSplitter)
from PyQt6.QtCore import Qt, QUrl
from src.gui.widgets.browser_view import BrowserView
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
        
        # Browser view
        self.browser_view = BrowserView()
        self.browser_view.recorder.interaction_recorded.connect(self.on_interaction)
        self.browser_view.page().loadFinished.connect(self.enable_interaction_recording)
        
        # Results area
        self.results_tree = QTreeWidget()
        self.results_tree.setHeaderLabels(['Element', 'Details'])
        self.results_tree.setColumnWidth(0, 200)
        
        self.raw_results = QTextEdit()
        self.raw_results.setReadOnly(True)
        
        # Create splitter for browser and results
        results_widget = QWidget()
        results_layout = QVBoxLayout()
        results_layout.addWidget(self.results_tree)
        results_layout.addWidget(self.raw_results)
        results_widget.setLayout(results_layout)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.browser_view)
        splitter.addWidget(results_widget)
        
        # Initialize scraper
        self.scraper = WebScraper()
        self.setup_scraper_connections()
        
        # Add all widgets to main layout
        layout.addWidget(self.url_input)
        layout.addLayout(button_layout)
        layout.addWidget(splitter)
        
        self.setLayout(layout)
        self.current_results = None
        
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
        
        self.browser_view.setUrl(QUrl(url))
        self.start_button.setEnabled(False)
        self.results_tree.clear()
        self.scraper.scrape(url)
        self.enable_interaction_recording()
        
    def toggle_recording(self):
        self.browser_view.recorder.recording = not self.browser_view.recorder.recording
        self.record_button.setText(
            "Stop Recording" if self.browser_view.recorder.recording 
            else "Record Interactions"
        )
        
    def enable_interaction_recording(self):
        self.browser_view.recorder.recording = True
        self.record_button.setText("Stop Recording")
        
    def on_interaction(self, data):
        interaction_item = QTreeWidgetItem(self.results_tree, [
            data['type'],
            f"XPath: {data['xpath']}"
        ])
        if 'value' in data:
            QTreeWidgetItem(interaction_item, ['Value', data['value']])
        if 'text' in data:
            QTreeWidgetItem(interaction_item, ['Text', data['text']])

            js_code = f"""
        let element = document;
        try {{
            element = document.evaluate(
                '{data["xpath"]}', 
                document, 
                null, 
                XPathResult.FIRST_ORDERED_NODE_TYPE, 
                null
            ).singleNodeValue;
            
            if(element) {{
                element.style.outline = '2px solid red';
                setTimeout(() => {{
                    element.style.outline = '';
                }}, 1000);
            }}
        }} catch(e) {{
            console.error('XPath evaluation failed:', e);
        }}
    """
            
    def simulate_interaction(self, item):
    # Get the XPath from the tree item
        xpath = item.text(1).replace('XPath: ', '')
        interaction_type = item.text(0)
    
        js_code = f"""
            let element = document.evaluate(
                '{xpath}',
                document,
                null,
                XPathResult.FIRST_ORDERED_NODE_TYPE,
                null
            ).singleNodeValue;
        
            if(element) {{
                if('{interaction_type}' === 'click') {{
                    element.click();
                }} else if('{interaction_type}' === 'input') {{
                    element.focus();
                }}
            }}
        """
        self.browser_view.page().runJavaScript(js_code)

def setup_ui(self):
    
    self.results_tree.itemDoubleClicked.connect(self.simulate_interaction)

    self.browser_view.page().runJavaScript(js_code)