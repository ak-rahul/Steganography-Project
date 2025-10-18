# ui/decrypt_page.py
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QFileDialog, QMessageBox,
    QLineEdit, QTextEdit, QProgressBar, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from core.stego import extract_text
from utils import qpixmap_from_path
import os

class DecryptPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.img_path = None
        self._build_ui()

    def _build_ui(self):
        self.setStyleSheet("background-color: #0f172a; color: white;")
        outer = QVBoxLayout()
        outer.setContentsMargins(18, 18, 18, 18)
        title = QLabel("Decrypt — Extract hidden text")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        outer.addWidget(title, alignment=Qt.AlignmentFlag.AlignLeft)

        top = QHBoxLayout()
        self.btn_select = QPushButton("Select Encrypted Image")
        self.btn_select.setFixedHeight(36)
        self.btn_select.clicked.connect(self.select_image)
        top.addWidget(self.btn_select)

        self.pwd_input = QLineEdit()
        self.pwd_input.setPlaceholderText("Password (if used)")
        self.pwd_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pwd_input.setFixedHeight(32)
        top.addWidget(self.pwd_input)

        outer.addLayout(top)

        mid = QHBoxLayout()
        self.preview = QLabel("No image")
        self.preview.setFixedSize(520, 360)
        self.preview.setStyleSheet("background: #ffffff;")
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mid.addWidget(self.preview)

        right = QVBoxLayout()
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setPlaceholderText("Decrypted message will appear here.")
        self.result.setFixedSize(300, 360)
        right.addWidget(self.result)

        self.btn_decrypt = QPushButton("Decrypt")
        self.btn_decrypt.setFixedHeight(36)
        self.btn_decrypt.clicked.connect(self.do_decrypt)
        right.addWidget(self.btn_decrypt)

        self.progress = QProgressBar()
        right.addWidget(self.progress)

        mid.addLayout(right)
        outer.addLayout(mid)
        self.setLayout(outer)

        self.setAcceptDrops(True)

    def select_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Encrypted Image", os.getcwd(), "Images (*.png *.jpg *.jpeg *.bmp)")
        if not path:
            return
        self._set_image(path)

    def _set_image(self, path):
        self.img_path = path
        pix = qpixmap_from_path(path, 520, 360)
        self.preview.setPixmap(pix)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            self._set_image(path)

    def do_decrypt(self):
        if not self.img_path:
            QMessageBox.warning(self, "No image", "Select an encrypted image first.")
            return
        pwd = self.pwd_input.text()
        try:
            self.progress.setValue(10)
            text, used_struct = extract_text(self.img_path, pwd if pwd else None)
            self.progress.setValue(100)
            self.result.setPlainText(text)
            QMessageBox.information(self, "Success", "Message extracted and shown in the box.")
        except Exception as e:
            QMessageBox.critical(self, "Failed", str(e))
        finally:
            self.progress.setValue(0)
