from PyQt6.QtGui import QPalette, QColor, QLinearGradient
from PyQt6.QtCore import Qt

# Update ThemeManager with comprehensive styling
class ThemeManager:
    def __init__(self):
        self.current_theme = "light"
        self.themes = {
            "light": {
                "background_start": QColor(255, 255, 255),
                "background_end": QColor(230, 220, 255),
                "text": QColor(0, 0, 0),
                "accent": QColor(100, 50, 150),
                "secondary": QColor(180, 160, 220),
                "button_bg": QColor(240, 235, 255)},
            "dark": {
                "background_start": QColor(40, 30, 60),
                "background_end": QColor(80, 70, 120),
                "button_bg": QColor(60, 50, 90),
                "text": QColor(255, 255, 255),
                "accent": QColor(180, 160, 220),
                "secondary": QColor(100, 80, 140)
            }
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
            theme = self.themes[self.current_theme]
            
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
                    padding: 8px 15px;
                    font-weight: bold;
                    transition: background-color 0.2s;
                }}
                
                QPushButton:hover {{
                    background-color: {theme['accent'].name()};
                    color: white;
                    transition: background-color 0.2s;
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
                }}
                
                QTreeWidget::item {{
                    padding: 5px;
                }}
                
                QTreeWidget::item:selected {{
                    background-color: {theme['accent'].name()};
                    color: white;
                }}
                
                QTreeWidget::branch {{
                    background: {theme['background_start'].name()};
                    border: none;
                    padding: 2px;
                }}
            """
            
            window.setStyleSheet(gradient)
        except Exception as e:
            print(f"Error applying theme: {e}")
            return
