import os
os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = "9222"

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
from src.gui.main_window import MainWindow
from src.utils.theme_manager import ThemeManager
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QPainterPath

def create_rounded_icon(path, size=64):
    # Create source pixmap
    source = QPixmap(path)
    source = source.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, 
                         Qt.TransformationMode.SmoothTransformation)
    
    # Create result pixmap
    result = QPixmap(size, size)
    result.fill(Qt.GlobalColor.transparent)
    
    # Create painter for final image
    painter = QPainter(result)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    # Create circular clip path
    path = QPainterPath()
    path.addEllipse(0, 0, size, size)
    painter.setClipPath(path)
    
    # Draw the image
    painter.drawPixmap(0, 0, source)
    painter.end()
    
    return QIcon(result)

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
                padding: 8px 16px;
                transition: background-color 0.3s;
            }}
            
            QPushButton:hover {{
                background-color: {theme['accent'].name()};
            }}
            
            QPushButton:pressed {{
                background-color: {theme['secondary'].name()};
            }}
            
            /* Style both primary and sidebar buttons the same way */
            QPushButton[class="primary-button"],
            QPushButton[class="sidebar-button"],
            #save_button {{
                background-color: {theme['button_bg'].name()};
                color: {theme['text'].name()};
            }}
            
            QPushButton[class="primary-button"]:hover,
            QPushButton[class="sidebar-button"]:hover,
            #save_button:hover {{
                background-color: {theme['accent'].name()};
            }}
            
            QPushButton[class="primary-button"]:pressed,
            QPushButton[class="sidebar-button"]:pressed,
            #save_button:pressed {{
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

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(script_dir, "Icon", "AntieLogo.png")

def main():
    # Create temporary view to access settings
    temp_view = QWebEngineView()
    settings = temp_view.page().settings()
    
    # Enable WebEngine settings with correct WebAttribute enum
    settings.setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
    
    theme_manager = ThemeManager()
    
    # Create and set rounded icon using relative path
    rounded_icon = create_rounded_icon(icon_path)
    app.setWindowIcon(rounded_icon)
    
    window = MainWindow(theme_manager)
    window.show()
    return app.exec()

if __name__ == "__main__":
    # Set high DPI scaling BEFORE creating QApplication
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QApplication(sys.argv)
    sys.exit(main())