import sys
from PyQt6.QtWidgets import QApplication
from src.gui.main_window import MainWindow
from src.utils.theme_manager import ThemeManager

def main():
    app = QApplication(sys.argv)
    theme_manager = ThemeManager()
    window = MainWindow(theme_manager)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
