# ui/encryption_tab.py
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QFileDialog, QMessageBox, QTextEdit, QLineEdit, QProgressBar
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from core.steganography import hide_text, capacity_bits, pack_payload
from utils import qpixmap_from_path
from storage import add_entry
import os

class EncryptionTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_image = None
        self._setup_ui()

    def _setup_ui(self):
        self.setFixedSize(820, 520)
        self.title = QLabel("Encrypt / Hide Text", self)
        self.title.setFont(QFont("Times New Roman", 18, QFont.Weight.Bold))
        self.title.setGeometry(20, 10, 400, 30)

        self.select_btn = QPushButton("Select Image", self)
        self.select_btn.setGeometry(20, 60, 160, 34)
        self.select_btn.clicked.connect(self.select_image)

        self.preview = QLabel(self)
        self.preview.setGeometry(220, 30, 560, 360)
        self.preview.setStyleSheet("background: white; border: 1px solid #222;")
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.pwd_input = QLineEdit(self)
        self.pwd_input.setGeometry(20, 120, 180, 30)
        self.pwd_input.setPlaceholderText("Password (optional)")
        self.pwd_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.msg_input = QTextEdit(self)
        self.msg_input.setGeometry(20, 180, 180, 160)
        self.msg_input.setPlaceholderText("Message to hide (text)")

        self.encrypt_btn = QPushButton("Embed & Save", self)
        self.encrypt_btn.setGeometry(20, 360, 160, 40)
        self.encrypt_btn.clicked.connect(self.perform_encrypt)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(20, 420, 760, 20)
        self.progress.setValue(0)

        self.status = QLabel("", self)
        self.status.setGeometry(20, 450, 760, 20)

    def select_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Image", os.getcwd(), "Images (*.png *.jpg *.jpeg)")
        if not path:
            return
        self.selected_image = path
        pix = qpixmap_from_path(path, 520, 320)
        self.preview.setPixmap(pix)
        try:
            import cv2
            img = cv2.imread(path)
            cap = capacity_bits(img)
            self.status.setText(f"Selected: {os.path.basename(path)} — capacity: {cap//8} bytes")
        except Exception:
            self.status.setText(f"Selected: {os.path.basename(path)}")

    def perform_encrypt(self):
        if not self.selected_image:
            QMessageBox.warning(self, "No Image", "Please choose an image first.")
            return
        message = self.msg_input.toPlainText()
        if not message:
            QMessageBox.warning(self, "No Message", "Please enter the message to hide.")
            return
        pwd = self.pwd_input.text()
        # quick payload check
        try:
            payload = pack_payload(message, pwd if pwd else "")
            needed = len(payload) * 8
            import cv2
            img = cv2.imread(self.selected_image)
            avail = capacity_bits(img)
            if needed + 16 > avail:
                QMessageBox.critical(self, "Too large", f"Message too large. Needs {needed} bits, avail {avail}.")
                return
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return
        # ask save path
        suggested = os.path.join(os.getcwd(), f"stego_{os.path.basename(self.selected_image)}")
        out, _ = QFileDialog.getSaveFileName(self, "Save encrypted image", suggested, "PNG Image (*.png);;All files (*)")
        if not out:
            return
        try:
            self.progress.setValue(10)
            out_path = hide_text(self.selected_image, message, pwd if pwd else "", output_path=out)
            self.progress.setValue(100)
            add_entry(os.path.basename(out_path), self.selected_image, bool(pwd))
            QMessageBox.information(self, "Success", f"Saved: {out_path}")
            pix = qpixmap_from_path(out_path, 520, 320)
            self.preview.setPixmap(pix)
            self.status.setText(f"Saved: {os.path.basename(out_path)}")
        except Exception as e:
            QMessageBox.critical(self, "Failed", str(e))
            self.progress.setValue(0)
