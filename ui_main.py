# ui_main.py
import os
from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QFileDialog, QMessageBox, QTextEdit,
    QLineEdit, QApplication, QFrame, QProgressBar, QWidget, QHBoxLayout, QVBoxLayout
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt

from stego import hide_text, extract_text, capacity_bits_for_image, pack_payload
from storage import add_entry, load_store
from utils import qpixmap_from_cv2

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steganography v2 — PyQt6")
        self.setFixedSize(900, 700)
        self.setStyleSheet("background-color: #263238; color: white;")
        self._setup_ui()
        self.chosen_image = None
        self.store = load_store()

    def _setup_ui(self):
        # header
        header = QLabel("Steganography — Next Gen", self)
        header.setFont(QFont("Times New Roman", 26, QFont.Weight.Bold))
        header.setGeometry(220, 10, 500, 40)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # left controls
        left_widget = QWidget(self)
        left_widget.setGeometry(20, 70, 260, 600)
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)

        self.btn_select = QPushButton("Select Image", left_widget)
        self.btn_select.setFixedHeight(40)
        self.btn_select.clicked.connect(self.select_image)
        left_layout.addWidget(self.btn_select)

        self.btn_encrypt = QPushButton("Encrypt & Save", left_widget)
        self.btn_encrypt.setFixedHeight(40)
        self.btn_encrypt.clicked.connect(self.start_encrypt_ui)
        left_layout.addWidget(self.btn_encrypt)

        self.btn_decrypt = QPushButton("Decrypt", left_widget)
        self.btn_decrypt.setFixedHeight(40)
        self.btn_decrypt.clicked.connect(self.start_decrypt_ui)
        left_layout.addWidget(self.btn_decrypt)

        left_layout.addSpacing(20)
        lbl_hint = QLabel("Hints:\n• Use .png for lossless embedding\n• Use a short password to protect\n• Messages are compressed & optionally encrypted", left_widget)
        lbl_hint.setWordWrap(True)
        left_layout.addWidget(lbl_hint)
        left_layout.addStretch(1)

        # image preview area
        preview_frame = QFrame(self)
        preview_frame.setGeometry(300, 70, 560, 360)
        preview_frame.setStyleSheet("background-color: #37474f; border-radius: 6px;")
        self.preview_label = QLabel(preview_frame)
        self.preview_label.setGeometry(130, 20, 300, 320)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("background: white;")

        # bottom input area
        self.input_frame = QFrame(self)
        self.input_frame.setGeometry(300, 450, 560, 220)
        self.input_frame.setStyleSheet("background-color: #455a64; border-radius: 6px;")

        # place inputs inside input_frame using absolute positions for simplicity
        lbl_pwd = QLabel("Password (optional):", self.input_frame)
        lbl_pwd.setGeometry(16, 10, 180, 25)
        lbl_pwd.setStyleSheet("color: white;")
        self.pwd_input = QLineEdit(self.input_frame)
        self.pwd_input.setGeometry(200, 10, 320, 28)
        self.pwd_input.setStyleSheet("background: white; color: black;")

        lbl_message = QLabel("Message to hide:", self.input_frame)
        lbl_message.setGeometry(16, 50, 180, 25)
        lbl_message.setStyleSheet("color: white;")

        self.message_input = QTextEdit(self.input_frame)
        self.message_input.setGeometry(16, 80, 504, 90)
        self.message_input.setStyleSheet("background: white; color: black;")

        self.submit_encrypt_button = QPushButton("Encrypt Now", self.input_frame)
        self.submit_encrypt_button.setGeometry(16, 175, 140, 34)
        self.submit_encrypt_button.clicked.connect(self.do_encrypt)
        self.submit_encrypt_button.setStyleSheet("background: #1e88e5; color: white;")

        self.submit_decrypt_button = QPushButton("Decrypt Now", self.input_frame)
        self.submit_decrypt_button.setGeometry(180, 175, 140, 34)
        self.submit_decrypt_button.clicked.connect(self.do_decrypt)
        self.submit_decrypt_button.setStyleSheet("background: #43a047; color: white;")
        self.submit_decrypt_button.hide()

        # progress & status bar
        self.progress = QProgressBar(self)
        self.progress.setGeometry(20, 660, 860, 20)
        self.progress.setValue(0)
        self.status = QLabel("", self)
        self.status.setGeometry(20, 635, 860, 20)
        self.status.setStyleSheet("color: #cfd8dc;")

    def select_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Image", os.getcwd(), "Images (*.png *.jpg *.jpeg);;All files (*)")
        if not path:
            return
        self.chosen_image = path
        pix = qpixmap_from_cv2(path, 300, 300)
        self.preview_label.setPixmap(pix)
        self.status.setText(f"Selected: {os.path.basename(path)}")
        # check capacity and show approx limits
        import cv2
        img = cv2.imread(path)
        bits = capacity_bits_for_image(img)
        self.status.setText(f"Selected: {os.path.basename(path)} — capacity: {bits//8} bytes ({bits} bits)")

    def start_encrypt_ui(self):
        # show encryption inputs
        self.submit_encrypt_button.show()
        self.submit_decrypt_button.hide()
        self.message_input.show()
        self.pwd_input.show()

    def start_decrypt_ui(self):
        # prepare for decrypt mode: pick image
        path, _ = QFileDialog.getOpenFileName(self, "Select Encrypted Image", os.getcwd(), "Images (*.png *.jpg *.jpeg);;All files (*)")
        if not path:
            return
        self.chosen_image = path
        pix = qpixmap_from_cv2(path, 300, 300)
        self.preview_label.setPixmap(pix)
        # switch buttons
        self.submit_encrypt_button.hide()
        self.submit_decrypt_button.show()
        self.message_input.hide()
        self.pwd_input.show()
        self.status.setText(f"Selected encrypted: {os.path.basename(path)}")

    def do_encrypt(self):
        if not self.chosen_image:
            QMessageBox.warning(self, "No Image", "Select an image first.")
            return
        message = self.message_input.toPlainText()
        if not message:
            QMessageBox.warning(self, "No Message", "Type a message to hide.")
            return
        pwd = self.pwd_input.text()
        # quick capacity check by building payload bytes (without writing)
        try:
            payload = pack_payload(message, pwd)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Payload build failed: {str(e)}")
            return
        # compute bits needed and compare to capacity
        import cv2
        img = cv2.imread(self.chosen_image)
        needed_bits = len(payload) * 8
        available_bits = capacity_bits_for_image(img)
        if needed_bits + 16 > available_bits:
            QMessageBox.critical(self, "Too big", f"Message too large to embed. Need ~{needed_bits} bits, available {available_bits}. Try shorter message or larger image.")
            return
        # ask for save location
        suggested = os.path.join(os.getcwd(), f"encrypted_v2_{os.path.basename(self.chosen_image)}")
        out_path, _ = QFileDialog.getSaveFileName(self, "Save encrypted image as", suggested, "PNG Image (*.png);;All files (*)")
        if not out_path:
            return
        # perform embedding
        try:
            self.progress.setValue(10)
            out = hide_text(self.chosen_image, message, pwd if pwd else None, output_path=out_path)
            self.progress.setValue(100)
            add_entry(os.path.basename(out), self.chosen_image, bool(pwd))
            QMessageBox.information(self, "Success", f"Encryption saved to:\n{out}")
            self.status.setText(f"Saved: {os.path.basename(out)}")
            pix = qpixmap_from_cv2(out, 300, 300)
            self.preview_label.setPixmap(pix)
        except Exception as e:
            QMessageBox.critical(self, "Encryption failed", str(e))
            self.progress.setValue(0)

    def do_decrypt(self):
        if not self.chosen_image:
            QMessageBox.warning(self, "No Image", "Select an image first.")
            return
        pwd = self.pwd_input.text()
        try:
            self.progress.setValue(10)
            message, used_new = extract_text(self.chosen_image, pwd if pwd else None)
            self.progress.setValue(100)
            if used_new:
                QMessageBox.information(self, "Decrypted (v2)", message)
            else:
                QMessageBox.information(self, "Decrypted (legacy/fallback)", message)
            self.status.setText("Decryption successful.")
        except Exception as e:
            QMessageBox.critical(self, "Decryption failed", str(e))
            self.status.setText("Decryption failed.")
        finally:
            self.progress.setValue(0)
