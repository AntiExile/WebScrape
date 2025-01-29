from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QStackedWidget, 
    QLineEdit, QPushButton, QTextEdit, QMessageBox, QTreeWidget, 
    QTreeWidgetItem, QHBoxLayout, QFileDialog, QSplitter)
from PyQt6.QtCore import Qt, QUrl
from src.gui.widgets.browser_view import BrowserView
import json

class ContentArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.recording = False  # Add recording state
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        self.browser_view = BrowserView()
        layout.addWidget(self.browser_view)
        layout.setContentsMargins(0, 0, 0, 0)

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
        
        # Results area
        self.results_tree = QTreeWidget()
        self.results_tree.setHeaderLabels(['Element', 'Details'])
        self.results_tree.setColumnWidth(0, 200)
        self.results_tree.itemDoubleClicked.connect(self.simulate_interaction)
        
        # Layout setup
        layout.addWidget(self.url_input)
        layout.addLayout(button_layout)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.browser_view)
        
        results_widget = QWidget()
        results_layout = QVBoxLayout()
        results_layout.addWidget(self.results_tree)
        results_widget.setLayout(results_layout)
        splitter.addWidget(results_widget)
        
        layout.addWidget(splitter)
        self.setLayout(layout)

    def toggle_recording(self):
        self._is_recording = not self._is_recording
        if self._is_recording:
            self.browser_view.recorder
        else:
            self.browser_view.recorder.stop_recording()

    def save_results(self):
        if not self.current_results:
            QMessageBox.warning(
                self,
                "No Results",
                "No scraping results to save."
            )
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Results",
            "",
            "CSV Files (*.csv);;HTML Files (*.html);;All Files (*.*)"
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.current_results, f, indent=4)
            QMessageBox.information(
                self,
                "Success",
                "Results saved successfully!"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to save results: {str(e)}"
            )

    def start_scraping(self):
        url = self.url_input.text().strip()
        
        if not url:
            QMessageBox.warning(
                self,
                "Invalid URL",
                "Please enter a URL to scrape."
            )
            return
            
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        try:
            self.start_button.setEnabled(False)
            self.url_input.setEnabled(False)
            self.save_button.setEnabled(False)
            self.browser_view.setUrl(QUrl(url))
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to start scraping: {str(e)}"
            )
            self.start_button.setEnabled(True)
            self.url_input.setEnabled(True)

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
        self.browser_view.page().runJavaScript(js_code)

    def simulate_interaction(self, item):
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
        
    # Add toggle_recording method
    def toggle_recording(self):
        """Toggle the recording state of the browser view."""
        self.recording = not self.recording
        self.browser_view.recorder.recording = self.recording
        
        # Update UI to show recording state
        if self.recording:
            self.start_button.setText("Stop Recording")
            self.results_tree.clear()  # Clear previous recordings
        else:
            self.start_button.setText("Start Recording")