# ui/main_window.py
from PyQt6.QtWidgets import QMainWindow, QLabel, QTabWidget
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from ui.encryption_tab import EncryptionTab
from ui.decryption_tab import DecryptionTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steganography-Project — SteganoX")
        self.setFixedSize(860, 620)
        self._setup_ui()

    def _setup_ui(self):
        header = QLabel("SteganoX — Steganography", self)
        header.setFont(QFont("Times New Roman", 20, QFont.Weight.Bold))
        header.setGeometry(10, 6, 840, 36)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.tabs = QTabWidget(self)
        self.tabs.setGeometry(10, 46, 840, 560)

        self.encrypt_tab = EncryptionTab(self)
        self.decrypt_tab = DecryptionTab(self)

        self.tabs.addTab(self.encrypt_tab, "Encrypt")
        self.tabs.addTab(self.decrypt_tab, "Decrypt")
