import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
from src.gui.main_window import MainWindow
from src.utils.theme_manager import ThemeManager
from PyQt6.QtGui import QIcon

def main():
    app = QApplication(sys.argv)
    theme_manager = ThemeManager()
    app.setWindowIcon(QIcon("path/to/your/icon.png"))
    window = MainWindow(theme_manager)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
