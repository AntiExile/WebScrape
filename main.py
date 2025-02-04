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

def create_rounded_icon(path, size=32):  # Reduced size from 64 to 32
    # Create source pixmap
    source = QPixmap(path)
    source = source.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, 
                         Qt.TransformationMode.SmoothTransformation)
    
    # Create result pixmap with transparent background
    result = QPixmap(size, size)
    result.fill(Qt.GlobalColor.transparent)
    
    # Create painter and set render hints
    painter = QPainter(result)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
    
    # Create rounded path
    path = QPainterPath()
    path.addRoundedRect(0, 0, size, size, size/2, size/2)
    
    # Draw source pixmap with rounded path
    painter.setClipPath(path)
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
    
    # Enhanced browser emulation with better permissions handling
    profile = QWebEngineProfile.defaultProfile()
    
    # Set modern browser user agent
    profile.setHttpUserAgent(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36 "
        "Edg/120.0.0.0"  # Add Edge identifier to help with compatibility
    )
    
    # Core settings
    settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.DnsPrefetchEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadImages, True)
    
    # Privacy settings
    settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, False)
    settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, False)
    settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, False)
    
    # Cookie and storage settings
    profile.setPersistentCookiesPolicy(
        QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies
    )
    profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
    profile.setHttpCacheMaximumSize(100 * 1024 * 1024)  # Reduced to 100MB
    
    # Headers and language
    profile.setHttpAcceptLanguage("en-US,en;q=0.9")
    
    # Set storage path
    storage_path = os.path.join(script_dir, "browser_data")
    profile.setPersistentStoragePath(storage_path)
    profile.setCachePath(os.path.join(storage_path, "cache"))
    
    theme_manager = ThemeManager()
    
    app = QApplication(sys.argv)
    
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
    
    # Set the application icon here
    rounded_icon = create_rounded_icon(icon_path)
    app.setWindowIcon(rounded_icon)
    
    sys.exit(main())