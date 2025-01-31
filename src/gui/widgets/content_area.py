from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QStackedWidget, 
    QLineEdit, QPushButton, QTextEdit, QMessageBox, QTreeWidget, 
    QTreeWidgetItem, QHBoxLayout, QFileDialog, QSplitter)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QTextCharFormat, QSyntaxHighlighter, QColor, QFont
from src.gui.widgets.browser_view import BrowserView
from datetime import datetime
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
        # Define categories and their patterns for HTML parsing
        self.categories = {
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
            }
        }
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
        self.save_button.setObjectName("save_button")  # Add this line
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
        """Save the current scraping results"""
        if not self.current_results:
            QMessageBox.warning(self, "No Results", "No scraping results to save.")
            return
            
        try:
            # Count total elements found
            total_elements = 0
            if 'classes' in self.current_results:
                for class_info in self.current_results['classes'].values():
                    total_elements += class_info['count']
            
            # Save to storage with proper element count
            filepath = self.window().scrape_storage.save_scrape(
                self.url_input.text(),
                {
                    'url': self.url_input.text(),
                    'timestamp': datetime.now().isoformat(),
                    'total_elements': total_elements,
                    'content': self.current_results
                }
            )
            
            # Show success message with element count
            save_to_file = QMessageBox.question(
                self,
                "Save to File",
                f"Results saved to history ({total_elements} elements found). Would you also like to save to a file?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if save_to_file == QMessageBox.StandardButton.Yes:
                file_path, _ = QFileDialog.getSaveFileName(
                    self,
                    "Save Results",
                    "",
                    "CSV Files (*.csv);;HTML Files (*.html);;JSON Files (*.json)"
                )
                
                if file_path:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(self.current_results, f, indent=4)
                    
            QMessageBox.information(self, "Success", f"Results saved successfully! {total_elements} elements found.")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save results: {str(e)}")

    def start_scraping(self):
        """Start the scraping process"""
        url = self.url_input.text().strip()
        
        if not url:
            QMessageBox.warning(self, "Invalid URL", "Please enter a URL to scrape.")
            return
            
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        try:
            self.start_button.setEnabled(False)
            self.url_input.setEnabled(False)
            self.save_button.setEnabled(False)
            self.browser_view.setUrl(QUrl(url))
            
            # Enable save button when page is loaded
            self.browser_view.loadFinished.connect(self._on_page_load_finished)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start scraping: {str(e)}")
            self.start_button.setEnabled(True)
            self.url_input.setEnabled(True)

    def _on_page_load_finished(self, success):
        """Handle page load completion"""
        if success:
            self.browser_view.page().toHtml(self._process_html_content)
            self.start_button.setEnabled(True)
            self.url_input.setEnabled(True)
            self.save_button.setEnabled(True)
        else:
            QMessageBox.critical(self, "Error", "Failed to load page")
            self.start_button.setEnabled(True)
            self.url_input.setEnabled(True)

    def _process_html_content(self, html_content):
        """Process the HTML content and store results"""
        # Parse the HTML
        parsed_data = self._parse_html_content(html_content)
        self.current_results = parsed_data
        
        # Clear existing items
        self.results_tree.clear()
        
        # Add parsed data to tree
        # Title
        title_item = QTreeWidgetItem(self.results_tree, ['Page Title', parsed_data['title']])
        
        # Classes
        if parsed_data['classes']:
            classes_item = QTreeWidgetItem(self.results_tree, ['Classes', f"{len(parsed_data['classes'])} found"])
            for class_name, info in parsed_data['classes'].items():
                class_item = QTreeWidgetItem(classes_item, [
                    class_name,
                    f"Used {info['count']} times"
                ])
                # Add tag types
                QTreeWidgetItem(class_item, ['Tag Types', ', '.join(info['tag_types'])])
                # Add samples
                if info['sample_content']:
                    samples_item = QTreeWidgetItem(class_item, ['Sample Content', ''])
                    for sample in info['sample_content']:
                        QTreeWidgetItem(samples_item, ['Sample', sample[:100]])
        
        # Headings
        if parsed_data['headings']:
            headings_item = QTreeWidgetItem(self.results_tree, ['Headings', f"{len(parsed_data['headings'])} found"])
            for heading in parsed_data['headings']:
                QTreeWidgetItem(headings_item, [
                    f"H{heading['level']}", 
                    heading['text']
                ])
        
        # Links
        if parsed_data['links']:
            links_item = QTreeWidgetItem(self.results_tree, ['Links', f"{len(parsed_data['links'])} found"])
            for link in parsed_data['links']:
                QTreeWidgetItem(links_item, [
                    link['text'] or 'No text',
                    link['href']
                ])
        
        # Images
        if parsed_data['images']:
            images_item = QTreeWidgetItem(self.results_tree, ['Images', f"{len(parsed_data['images'])} found"])
            for img in parsed_data['images']:
                QTreeWidgetItem(images_item, [
                    img['alt'] or 'No alt text',
                    img['src']
                ])
        
        # Forms
        if parsed_data['forms']:
            forms_item = QTreeWidgetItem(self.results_tree, ['Forms', f"{len(parsed_data['forms'])} found"])
            for form in parsed_data['forms']:
                form_item = QTreeWidgetItem(forms_item, [
                    'Form',
                    f"Action: {form['action']}, Method: {form['method']}"
                ])
                inputs_item = QTreeWidgetItem(form_item, ['Inputs', f"{len(form['inputs'])} found"])
                for input_field in form['inputs']:
                    QTreeWidgetItem(inputs_item, [
                        input_field['type'],
                        f"name: {input_field['name']}, id: {input_field['id']}"
                    ])
        
        # Expand top-level items
        for i in range(self.results_tree.topLevelItemCount()):
            self.results_tree.topLevelItem(i).setExpanded(True)

    def _parse_html_content(self, html_content):
        """Parse HTML content and extract structured data"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Create a dictionary to store the parsed data
        parsed_data = {
            'title': soup.title.string if soup.title else 'No title',
            'classes': {},
            'headings': [],
            'links': [],
            'images': [],
            'forms': []
        }
        
        # Parse HTML classes and their elements
        for element in soup.find_all(class_=True):
            classes = element.get('class')
            for class_name in classes:
                if (class_name not in parsed_data['classes']):
                    parsed_data['classes'][class_name] = {
                        'count': 0,
                        'tag_types': set(),
                        'sample_content': []
                    }
                parsed_data['classes'][class_name]['count'] += 1
                parsed_data['classes'][class_name]['tag_types'].add(element.name)
                
                # Store a sample of the content (up to 3 samples)
                if len(parsed_data['classes'][class_name]['sample_content']) < 3:
                    content = element.get_text().strip()
                    if content:
                        parsed_data['classes'][class_name]['sample_content'].append(content)
        
        # Convert sets to lists for JSON serialization
        for class_info in parsed_data['classes'].values():
            class_info['tag_types'] = list(class_info['tag_types'])
        
        # Extract headings
        parsed_data['headings'] = [
            {'level': int(h.name[1]), 'text': h.get_text().strip()}
            for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        ]
        
        # Extract links
        parsed_data['links'] = [
            {'text': a.get_text().strip(), 'href': a.get('href')}
            for a in soup.find_all('a', href=True)
        ]
        
        # Extract images
        parsed_data['images'] = [
            {'src': img.get('src'), 'alt': img.get('alt', '')}
            for img in soup.find_all('img', src=True)
        ]
        
        # Extract forms
        parsed_data['forms'] = [
            {
                'action': form.get('action', ''),
                'method': form.get('method', 'get'),
                'inputs': [
                    {
                        'type': input_tag.get('type', 'text'),
                        'name': input_tag.get('name', ''),
                        'id': input_tag.get('id', '')
                    }
                    for input_tag in form.find_all('input')
                ]
            }
            for form in soup.find_all('form')
        ]
        
        return parsed_data

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
        
        # Store elements and their XPaths for highlighting
        self.element_positions = {}
        current_position = 0
        
        formatted_output = "=== Page Structure Overview ===\n\n"
        
        for category, config in self.categories.items():
            matches = re.finditer(config['pattern'], html_content, re.DOTALL)
            items = list(matches)
            
            if items:
                formatted_output += f"\n{'-' * 40}\n"
                formatted_output += f"{category}\n"
                formatted_output += f"{'-' * 40}\n"
                
                for item in items:
                    line = ""
                    try:
                        if category == 'Navigation Links':
                            url, text = item.groups()
                            if url and text:  # Check if values exist
                                line = f"{config['prefix']}Link: {text.strip()} -> {url}\n"
                                xpath = f"//a[@href='{url}']"
                        elif category == 'Images':
                            src = item.group(1)
                            alt = item.group(2) if item.group(2) else 'No alt text'
                            if src:  # Check if src exists
                                line = f"{config['prefix']}Image: {alt} ({src})\n"
                                xpath = f"//img[@src='{src}']"
                        else:
                            content = item.group(1) if item.groups() else item.group(0)
                            if content:  # Check if content exists
                                line = f"{config['prefix']}{content.strip()}\n"
                                # Create appropriate XPath based on category
                                if category == 'Page Title':
                                    xpath = "//title"
                                elif category == 'Main Headings':
                                    xpath = f"//h1[contains(text(), '{content.strip()}')]"
                                elif category == 'Sub Headings':
                                    xpath = f"//h2[contains(text(), '{content.strip()}')]|//h3[contains(text(), '{content.strip()}')]"
                                else:
                                    continue
                        
                        # Only store position and add line if we have content
                        if line:
                            self.element_positions[current_position] = xpath
                            current_position += len(line)
                            formatted_output += line
                    except (AttributeError, IndexError) as e:
                        print(f"Error processing {category} item: {e}")
                        continue
        
        # Set up HTML viewer with formatting
        self.html_viewer.setFont(QFont("Consolas", 10))
        self.html_viewer.mouseMoveEvent = self.on_html_viewer_mouse_move
        self.html_viewer.leaveEvent = self.on_html_viewer_leave
        highlighter = HTMLHighlighter(self.html_viewer.document())
        self.html_viewer.setPlainText(formatted_output)

    def on_html_viewer_mouse_move(self, event):
        """Handle mouse movement over the HTML viewer"""
        cursor = self.html_viewer.cursorForPosition(event.pos())
        position = cursor.position()
        
        # Find the closest element position
        closest_pos = None
        for pos in self.element_positions:
            if pos <= position:
                if closest_pos is None or pos > closest_pos:
                    closest_pos = pos
        
        if closest_pos is not None:
            xpath = self.element_positions[closest_pos]
            self.highlight_element_in_browser(xpath)

    def on_html_viewer_leave(self, event):
        """Handle mouse leaving the HTML viewer"""
        # Remove any existing highlights
        self.browser_view.page().runJavaScript("""
            document.querySelectorAll('.webscrape-highlight').forEach(el => {
                el.style.outline = '';
                el.classList.remove('webscrape-highlight');
            });
        """)

    def highlight_element_in_browser(self, xpath):
        """Highlight the element in the browser view"""
        # Escape special characters in xpath
        def escape_xpath_string(xpath_str):
            if not xpath_str:
                return "''"
            if '"' not in xpath_str:
                return f'"{xpath_str}"'
            if "'" not in xpath_str:
                return f"'{xpath_str}'"
            return f"concat('{xpath_str.replace("'", "',\"'\",'")}','')"

        try:
            # Clean the XPath expression
            if 'contains' in xpath:
                # Handle contains() function
                base, text = xpath.split('contains(text(), ', 1)
                text = text.rsplit(')', 1)[0].strip("'\"")
                xpath = f"{base}contains(text(), {escape_xpath_string(text)})"
            
            # Escape single quotes in the entire xpath
            xpath = xpath.replace("'", "\\'")
            
            js_code = """
            (function() {
                // Remove previous highlights
                document.querySelectorAll('.webscrape-highlight').forEach((el) => {
                    el.style.outline = '';
                    el.classList.remove('webscrape-highlight');
                });
                
                try {
                    const evaluator = new XPathEvaluator();
                    const result = evaluator.evaluate(
                        `%s`,
                        document,
                        null,
                        XPathResult.FIRST_ORDERED_NODE_TYPE,
                        null
                    );
                    
                    const element = result.singleNodeValue;
                    if(element) {
                        element.classList.add('webscrape-highlight');
                        element.style.outline = '2px solid #ff4444';
                        element.style.outlineOffset = '2px';
                        element.scrollIntoView({behavior: 'smooth', block: 'center'});
                        
                        // Add highlight effect
                        element.style.transition = 'all 0.3s';
                        element.style.backgroundColor = 'rgba(255, 68, 68, 0.1)';
                    }
                } catch(e) {
                    // Silently handle XPath errors
                    console.debug('XPath evaluation:', e);
                }
            })();
            """ % xpath
            
            self.browser_view.page().runJavaScript(js_code)
        except Exception as e:
            print(f"Error in highlight_element_in_browser: {e}")

    def set_html_content(self, html_content):
        """Set the HTML content in the viewer"""
        self.html_viewer.setPlainText(html_content)

    def update_results_view(self, data):
        """Update both tree view and HTML view with loaded data"""
        try:
            # Update tree view
            self.results_tree.clear()
            
            # Add title
            title_item = QTreeWidgetItem(self.results_tree, ['Page Title', data.get('title', 'No title')])
            
            # Add classes
            if 'classes' in data:
                classes_item = QTreeWidgetItem(self.results_tree, ['Classes', f"{len(data['classes'])} found"])
                for class_name, info in data['classes'].items():
                    class_item = QTreeWidgetItem(classes_item, [
                        class_name,
                        f"Used {info['count']} times"
                    ])
                    # Add tag types
                    QTreeWidgetItem(class_item, ['Tag Types', ', '.join(info['tag_types'])])
                    # Add samples
                    if info['sample_content']:
                        samples_item = QTreeWidgetItem(class_item, ['Sample Content', ''])
                        for sample in info['sample_content']:
                            QTreeWidgetItem(samples_item, ['Sample', sample[:100]])
            
            # Expand top-level items
            for i in range(self.results_tree.topLevelItemCount()):
                self.results_tree.topLevelItem(i).setExpanded(True)
                
            # Format and update HTML view
            formatted_html = self.format_loaded_data(data)
            self.html_viewer.setPlainText(formatted_html)
            
            # Enable save button
            self.save_button.setEnabled(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error updating results view: {str(e)}")

    def format_loaded_data(self, data):
        """Format loaded data for HTML viewer"""
        formatted_output = "=== Page Structure Overview ===\n\n"
        
        # Add title
        formatted_output += f"Title: {data.get('title', 'No title')}\n\n"
        
        # Add classes
        if 'classes' in data:
            formatted_output += f"{'-' * 40}\nClasses\n{'-' * 40}\n"
            for class_name, info in data['classes'].items():
                formatted_output += f"\nClass: {class_name}\n"
                formatted_output += f"Used {info['count']} times\n"
                formatted_output += f"Tag types: {', '.join(info['tag_types'])}\n"
                if info['sample_content']:
                    formatted_output += "Sample content:\n"
                    for sample in info['sample_content']:
                        formatted_output += f"  - {sample[:100]}\n"
        
        return formatted_output

    def unload_current_scrape(self):
        """Clear current scrape data and views"""
        # Clear current results
        self.current_results = None
        
        # Clear URL input
        self.url_input.setText("")
        
        # Clear tree view
        self.results_tree.clear()
        
        # Clear HTML viewer
        self.html_viewer.clear()
        
        # Reset browser view
        self.browser_view.setUrl(QUrl("about:blank"))
        
        # Disable save button
        self.save_button.setEnabled(False)