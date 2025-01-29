from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                            QMessageBox, QDialog)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl

class Sidebar(QWidget):
    record_clicked = pyqtSignal()
    settings_clicked = pyqtSignal()
    results_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        self.setFixedWidth(200)
        layout.setSpacing(10)
        
        # Record button
        self.record_button = QPushButton("Record Interactions")
        self.record_button.setFixedHeight(40)
        self.record_button.setProperty("class", "sidebar-button")
        self.record_button.clicked.connect(self.record_clicked.emit)
        layout.addWidget(self.record_button)
        
        # Results button
        self.results_button = QPushButton("Results")
        self.results_button.setFixedHeight(40)
        self.results_button.setProperty("class", "sidebar-button")
        self.results_button.clicked.connect(self.results_clicked.emit)
        layout.addWidget(self.results_button)
        
        # Settings button
        self.settings_button = QPushButton("Settings")
        self.settings_button.setFixedHeight(40)
        self.settings_button.setProperty("class", "sidebar-button")
        self.settings_button.clicked.connect(self.settings_clicked.emit)
        layout.addWidget(self.settings_button)
        
        # Help button
        help_button = QPushButton("Help")
        help_button.setFixedHeight(40)
        help_button.setProperty("class", "sidebar-button")
        help_button.clicked.connect(self.show_help_dialog)
        layout.addWidget(help_button)
        
        layout.addStretch()
        self.setLayout(layout)

    def show_help_dialog(self):
        reply = QMessageBox.question(
            self,
            "Open Help Page",
            "Would you like to open the WebScrape documentation in your browser?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            QDesktopServices.openUrl(QUrl("https://github.com/AntiExile/WebScrape"))
