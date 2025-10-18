# ui/decryption_tab.py
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QFileDialog, QMessageBox, QLineEdit, QTextEdit, QProgressBar
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from core.steganography import extract_text
from utils import qpixmap_from_path
import os

class DecryptionTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_image = None
        self._setup_ui()

    def _setup_ui(self):
        self.setFixedSize(820, 520)
        self.title = QLabel("Decrypt / Extract Text", self)
        self.title.setFont(QFont("Times New Roman", 18, QFont.Weight.Bold))
        self.title.setGeometry(20, 10, 400, 30)

        self.select_btn = QPushButton("Select Encrypted Image", self)
        self.select_btn.setGeometry(20, 60, 200, 34)
        self.select_btn.clicked.connect(self.select_image)

        self.preview = QLabel(self)
        self.preview.setGeometry(220, 30, 560, 360)
        self.preview.setStyleSheet("background: white; border: 1px solid #222;")
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.pwd_input = QLineEdit(self)
        self.pwd_input.setGeometry(20, 140, 180, 30)
        self.pwd_input.setPlaceholderText("Password (if used)")
        self.pwd_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.decrypt_btn = QPushButton("Extract Message", self)
        self.decrypt_btn.setGeometry(20, 190, 200, 40)
        self.decrypt_btn.clicked.connect(self.perform_decrypt)

        self.result_view = QTextEdit(self)
        self.result_view.setGeometry(20, 260, 180, 200)
        self.result_view.setReadOnly(True)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(20, 470, 760, 20)
        self.progress.setValue(0)

        self.status = QLabel("", self)
        self.status.setGeometry(20, 495, 760, 20)

    def select_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Encrypted Image", os.getcwd(), "Images (*.png *.jpg *.jpeg)")
        if not path:
            return
        self.selected_image = path
        pix = qpixmap_from_path(path, 520, 320)
        self.preview.setPixmap(pix)
        self.status.setText(f"Selected: {os.path.basename(path)}")

    def perform_decrypt(self):
        if not self.selected_image:
            QMessageBox.warning(self, "No Image", "Choose an encrypted image.")
            return
        pwd = self.pwd_input.text()
        try:
            self.progress.setValue(10)
            message = extract_text(self.selected_image, pwd if pwd else "")
            self.progress.setValue(100)
            self.result_view.setPlainText(message)
            QMessageBox.information(self, "Decryption success", "Message extracted and shown in the box.")
            self.status.setText("Decryption successful.")
        except Exception as e:
            QMessageBox.critical(self, "Failed", str(e))
            self.status.setText("Decryption failed.")
        finally:
            self.progress.setValue(0)
