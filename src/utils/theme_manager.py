from PyQt6.QtGui import QPalette, QColor, QLinearGradient
from PyQt6.QtCore import Qt

# Update ThemeManager with comprehensive styling
class ThemeManager:
    def __init__(self):
        self.theme = {
            "background_start": QColor(40, 30, 60),
            "background_end": QColor(80, 70, 120),
            "button_bg": QColor(60, 50, 90),
            "text": QColor(255, 255, 255),
            "accent": QColor(180, 160, 220),
            "secondary": QColor(100, 80, 140)
        }
    
    def toggle_theme(self, window):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme(window)
    
    def get_current_theme(self):
        return self.themes[self.current_theme]
    
    def get_contrast_color(self, background_color):
        # Calculate proper contrast color based on background
        return QColor(255, 255, 255) if self.current_theme == "dark" else QColor(0, 0, 0)

    def apply_theme(self, window):
        try:
            theme = self.theme
            
            gradient = f"""
                QMainWindow {{
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 {theme['background_start'].name()},
                        stop: 1 {theme['background_end'].name()}
                    );
                }}
                
                QPushButton {{
                    background-color: {theme['button_bg'].name()};
                    color: {theme['text'].name()};
                    border: none;
                    border-radius: 5px;
                    padding: 8px 16px;
                }}
                
                QPushButton:hover {{
                    background-color: {theme['accent'].name()};
                }}
                
                QPushButton:pressed {{
                    background-color: {theme['secondary'].name()};
                }}
                
                QPushButton[class="primary-button"] {{
                    background-color: {theme['accent'].name()};
                    color: {theme['text'].name()};
                }}
                
                QPushButton[class="primary-button"]:hover {{
                    background-color: {theme['secondary'].name()};
                }}
                
                QLineEdit, QTextEdit {{
                    background-color: {theme['background_start'].name()};
                    color: {theme['text'].name()};
                    border: 1px solid {theme['accent'].name()};
                    border-radius: 5px;
                    selection-background-color: {theme['accent'].name()};
                    padding: 5px;
                }}
                
                QLabel {{
                    color: {theme['text'].name()};
                }}
                
                QProgressBar {{
                    border: 1px solid {theme['accent'].name()};
                    border-radius: 5px;
                    text-align: center;
                }}
                
                QProgressBar::chunk {{
                    background-color: {theme['accent'].name()};
                    border-radius: 5px;
                }}
                
                QTreeWidget {{
                    background-color: {theme['background_start'].name()};
                    color: {theme['text'].name()};
                    border: 1px solid {theme['accent'].name()};
                    border-radius: 5px;
                    padding: 5px;
                    min-height: 100px;
                    max-height: 300px;
                }}
                
                QTreeWidget::item {{
                    padding: 2px;
                    margin: 0px;
                    border-radius: 3px;
                }}
                
                QTreeWidget::item:selected {{
                    background-color: {theme['accent'].name()};
                    color: {theme['text'].name()};
                }}
                
                QTreeWidget::branch {{
                    background: transparent;
                }}
                
                QTreeWidget QHeaderView::section {{
                    background-color: {theme['button_bg'].name()};
                    color: {theme['text'].name()};
                    padding: 5px;
                    border: none;
                    border-radius: 3px;
                }}
                
                QHeaderView::section {{
                    background-color: {theme['background_start'].name()};
                    color: {theme['text'].name()};
                    border: none;
                    border-radius: 0px;
                    padding: 4px;
                }}
                
                QSplitter {{
                    background-color: {theme['background_start'].name()};
                }}
                
                QSplitter::handle {{
                    background-color: {theme['accent'].name()};
                    height: 2px;
                }}
                
                QTextEdit {{
                    background-color: {theme['background_start'].name()};
                    color: {theme['text'].name()};
                    border: 1px solid {theme['accent'].name()};
                    border-radius: 5px;
                    padding: 5px;
                    margin: 0px;
                    min-height: 100px;
                    max-height: 300px;
                }}
            """
            
            window.setStyleSheet(gradient)
        except Exception as e:
            print(f"Error applying theme: {e}")
            return
