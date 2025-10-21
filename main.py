"""
Steganography Pro - Windows 11 Fluent Design
Main entry point
"""

import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow
from gui.styles import apply_windows_theme


def main():
    """Initialize and run application"""
    app = QApplication(sys.argv)
    
    # Set app name
    app.setApplicationName("Steganography Pro")
    app.setOrganizationName("SteganoPro")
    
    # Apply Windows 11 theme
    apply_windows_theme(app)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
