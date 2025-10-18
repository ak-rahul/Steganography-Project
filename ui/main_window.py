# ui/main_window.py (corrected with QLabel import)
from PyQt6.QtWidgets import QMainWindow, QWidget, QTabWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from ui.encrypt_page import EncryptPage
from ui.decrypt_page import DecryptPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SteganoX — Next-Gen Steganography")
        self.setFixedSize(880, 680)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        layout = QVBoxLayout()
        central.setLayout(layout)

        header = QLabel("SteganoX")
        header.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setMovable(False)

        self.encrypt = EncryptPage()
        self.decrypt = DecryptPage()

        tabs.addTab(self.encrypt, "Encrypt")
        tabs.addTab(self.decrypt, "Decrypt")
        layout.addWidget(tabs)
        self.setCentralWidget(central)
