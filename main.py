"""
Steganography Pro - Advanced Image Steganography Tool
Main entry point for the application
"""

import sys
from gui.main_window import MainWindow


def main():
    """Initialize and run the application"""
    try:
        app = MainWindow()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
