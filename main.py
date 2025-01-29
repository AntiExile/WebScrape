import os
os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = "9222"

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
from src.gui.main_window import MainWindow
from src.utils.theme_manager import ThemeManager
from PyQt6.QtGui import QIcon

# Move QApplication creation and high DPI setting to top level
QApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
)
app = QApplication(sys.argv)

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
    app.setWindowIcon(QIcon(r"E:\WebScrapeOG\Icon\AntieLogo.png"))
    window = MainWindow(theme_manager)
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())