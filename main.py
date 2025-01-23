import sys
from PyQt6.QtWidgets import QApplication
<<<<<<< HEAD
from PyQt6.QtCore import Qt
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
=======
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
>>>>>>> 371859786f75ce7a502e257f8a8d33ad248d2790
from src.gui.main_window import MainWindow
from src.utils.theme_manager import ThemeManager
from PyQt6.QtGui import QIcon

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
    app.setWindowIcon(QIcon("path/to/your/icon.png"))
    window = MainWindow(theme_manager)
    window.show()
    sys.exit(app.exec())
