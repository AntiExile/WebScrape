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
    
    # Create and set rounded icon
    rounded_icon = create_rounded_icon(r"E:\WebScrapeOG\Icon\AntieLogo.png")
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