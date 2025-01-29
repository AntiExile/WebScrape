from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QStackedWidget, 
    QLineEdit, QPushButton, QTextEdit, QMessageBox, QTreeWidget, 
    QTreeWidgetItem, QHBoxLayout, QFileDialog, QSplitter)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QTextCharFormat, QSyntaxHighlighter, QColor, QFont
from src.gui.widgets.browser_view import BrowserView
import json
import re

class HTMLHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tag_format = QTextCharFormat()
        self.tag_format.setForeground(QColor("#2980b9"))  # Blue for tags
        
        self.attr_format = QTextCharFormat()
        self.attr_format.setForeground(QColor("#16a085"))  # Green for attributes
        
        self.value_format = QTextCharFormat()
        self.value_format.setForeground(QColor("#c0392b"))  # Red for values
        
        self.text_format = QTextCharFormat()
        self.text_format.setForeground(QColor("#2c3e50"))  # Dark gray for text

    def highlightBlock(self, text):
        # Highlight tags
        import re
        # Match opening and closing tags
        tag_pattern = r'<[^>]+>'
        for match in re.finditer(tag_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), self.tag_format)

        # Match attributes and their values
        attr_pattern = r'\w+="[^"]*"'
        for match in re.finditer(attr_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), self.attr_format)

        # Match text between tags
        text_pattern = r'>[^<]+<'
        for match in re.finditer(text_pattern, text):
            # Don't format the brackets
            self.setFormat(match.start() + 1, match.end() - match.start() - 2, self.text_format)

class ContentArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.recording = False  # Add recording state
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 0, 0, 0)

        # Control section (URL input and buttons)
        control_layout = QHBoxLayout()
        
        # URL input
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL to scrape...")
        self.url_input.setFixedHeight(40)
        control_layout.addWidget(self.url_input)
        
        # Buttons
        self.start_button = QPushButton("Start Scraping")
        self.start_button.setFixedHeight(40)
        self.start_button.setProperty("class", "primary-button")
        self.start_button.clicked.connect(self.start_scraping)
        control_layout.addWidget(self.start_button)
        
        self.save_button = QPushButton("Save Results")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_results)
        control_layout.addWidget(self.save_button)
        
        # Main content area
        content_layout = QHBoxLayout()
        
        # Browser view on the left
        self.browser_view = BrowserView()
        self.browser_view.recorder.interaction_recorded.connect(self.on_interaction)
        self.browser_view.loadFinished.connect(self.update_html_view)
        content_layout.addWidget(self.browser_view, stretch=2)
        
        # Right side splitter
        right_splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Results tree in top half
        self.results_tree = QTreeWidget()
        self.results_tree.setHeaderLabels(['Element', 'Details'])
        self.results_tree.setColumnWidth(0, 200)
        self.results_tree.itemDoubleClicked.connect(self.simulate_interaction)
        right_splitter.addWidget(self.results_tree)
        
        # HTML viewer in bottom half
        self.html_viewer = QTextEdit()
        self.html_viewer.setReadOnly(True)
        self.html_viewer.setPlaceholderText("HTML content will appear here")
        right_splitter.addWidget(self.html_viewer)
        
        content_layout.addWidget(right_splitter, stretch=1)
        
        # Add layouts to main layout
        layout.addLayout(control_layout)
        layout.addLayout(content_layout)
        
        self.setLayout(layout)

    def toggle_recording(self):
        self._is_recording = not self._is_recording
        if self._is_recording:
            self.browser_view.recorder
        else:
            self.browser_view.recorder.stop_recording()

    def save_results(self):
        if not self.current_results:
            QMessageBox.warning(self, "No Results", "No scraping results to save.")
            return
            
        try:
            # Save to storage
            filepath = self.window().scrape_storage.save_scrape(
                self.url_input.text(),
                self.current_results
            )
            
            # Also allow saving to file if needed
            save_to_file = QMessageBox.question(
                self,
                "Save to File",
                "Results saved to history. Would you also like to save to a file?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if save_to_file == QMessageBox.StandardButton.Yes:
                file_path, _ = QFileDialog.getSaveFileName(
                    self,
                    "Save Results",
                    "",
                    "CSV Files (*.csv);;HTML Files (*.html);;All Files (*.*)"
                )
                
                if file_path:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(self.current_results, f, indent=4)
                    
            QMessageBox.information(self, "Success", "Results saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save results: {str(e)}")

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

    def update_settings(self, settings):
        """Update content area based on new settings"""
        self.auto_scroll = settings['auto_scroll']
        self.default_save_format = settings['save_format']
        self.highlight_elements = settings['highlight_elements']
        self.record_screenshots = settings['record_screenshots']

    def update_html_view(self):
        """Update the HTML viewer with formatted content"""
        self.browser_view.page().toHtml(self.format_and_set_html)

    def format_and_set_html(self, html_content):
        """Format HTML content into categorized sections"""
        # Remove scripts and style tags
        html_content = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', html_content)
        html_content = re.sub(r'<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>', '', html_content)
        
        # Define categories and their patterns
        categories = {
            'Page Title': {
                'pattern': r'<title[^>]*>(.*?)</title>',
                'prefix': '📄 '
            },
            'Navigation Links': {
                'pattern': r'<a[^>]*?href="([^"]*)"[^>]*>(.*?)</a>',
                'prefix': '🔗 '
            },
            'Main Headings': {
                'pattern': r'<h1[^>]*>(.*?)</h1>',
                'prefix': '📌 '
            },
            'Sub Headings': {
                'pattern': r'<h[2-6][^>]*>(.*?)</h[2-6]>',
                'prefix': '📎 '
            },
            'Forms': {
                'pattern': r'<form[^>]*?action="([^"]*)"[^>]*>.*?</form>',
                'prefix': '📝 '
            },
            'Input Fields': {
                'pattern': r'<input[^>]*?(?:type="([^"]*)")?[^>]*>',
                'prefix': '⌨️ '
            },
            'Images': {
                'pattern': r'<img[^>]*?src="([^"]*)"[^>]*?(?:alt="([^"]*)")?[^>]*>',
                'prefix': '🖼️ '
            },
            'Lists': {
                'pattern': r'<(?:ul|ol)[^>]*>.*?</(?:ul|ol)>',
                'prefix': '📋 '
            },
            'Tables': {
                'pattern': r'<table[^>]*>.*?</table>',
                'prefix': '📊 '
            },
            'Meta Information': {
                'pattern': r'<meta[^>]*?(?:name|property)="([^"]*)"[^>]*?content="([^"]*)"[^>]*>',
                'prefix': 'ℹ️ '
            }
        }
        
        # Create formatted output
        formatted_output = "=== Page Structure Overview ===\n\n"
        
        for category, config in categories.items():
            matches = re.finditer(config['pattern'], html_content, re.DOTALL)
            items = list(matches)
            
            if items:
                formatted_output += f"\n{'-' * 40}\n"
                formatted_output += f"{category}\n"
                formatted_output += f"{'-' * 40}\n"
                
                for item in items:
                    if category == 'Navigation Links':
                        url, text = item.groups()
                        formatted_output += f"{config['prefix']}Link: {text.strip()} -> {url}\n"
                    elif category == 'Images':
                        src = item.group(1)
                        alt = item.group(2) if item.group(2) else 'No alt text'
                        formatted_output += f"{config['prefix']}Image: {alt} ({src})\n"
                    elif category == 'Meta Information':
                        name, content = item.groups()
                        formatted_output += f"{config['prefix']}{name}: {content}\n"
                    elif category == 'Input Fields':
                        input_type = item.group(1) if item.group(1) else 'text'
                        formatted_output += f"{config['prefix']}Type: {input_type}\n"
                    else:
                        content = item.group(1) if item.groups() else item.group(0)
                        formatted_output += f"{config['prefix']}{content.strip()}\n"
                
                formatted_output += "\n"
        
        # Set up HTML viewer with formatting
        self.html_viewer.setFont(QFont("Consolas", 10))
        highlighter = HTMLHighlighter(self.html_viewer.document())
        self.html_viewer.setPlainText(formatted_output)

    def set_html_content(self, html_content):
        """Set the HTML content in the viewer"""
        self.html_viewer.setPlainText(html_content)