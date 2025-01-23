import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
from src.gui.main_window import MainWindow
from src.utils.theme_manager import ThemeManager

if __name__ == "__main__":
    # Set HighDPI scaling policy before creating QApplication
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    
    # Create a temporary web view to access settings
    temp_view = QWebEngineView()
    settings = temp_view.page().settings()
    
    # Enable WebEngine features using correct attribute names
    settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.DeveloperExtrasEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
    
    theme_manager = ThemeManager()
    window = MainWindow(theme_manager)
    window.show()
    sys.exit(app.exec())
