# ui/encrypt_page.py
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QFileDialog, QMessageBox,
    QTextEdit, QLineEdit, QProgressBar, QCheckBox, QHBoxLayout, QVBoxLayout, QGridLayout
)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from core.stego import hide_text, build_full_blob, capacity_bits
from utils import qpixmap_from_path, human_size
from storage import add_entry
import os
import cv2

class EncryptPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.img_path = None
        self._build_ui()

    def _build_ui(self):
        self.setStyleSheet("background-color: #0f172a; color: white;")
        main_layout = QGridLayout()
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setHorizontalSpacing(16)
        main_layout.setVerticalSpacing(12)

        title = QLabel("Encrypt — Hide text in an image")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        main_layout.addWidget(title, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        # Left side: controls
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(10)

        self.btn_select = QPushButton("Select Image")
        self.btn_select.setFixedHeight(36)
        self.btn_select.clicked.connect(self.select_image)
        controls_layout.addWidget(self.btn_select)

        self.lbl_capacity = QLabel("Capacity: -")
        controls_layout.addWidget(self.lbl_capacity)

        self.pwd_input = QLineEdit()
        self.pwd_input.setPlaceholderText("Password (optional)")
        self.pwd_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pwd_input.setFixedHeight(32)
        controls_layout.addWidget(self.pwd_input)

        self.show_pwd_cb = QCheckBox("Show password")
        self.show_pwd_cb.stateChanged.connect(self._toggle_pwd)
        controls_layout.addWidget(self.show_pwd_cb)

        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Enter message to hide (text). Compression used automatically.")
        self.message_input.setFixedHeight(160)
        controls_layout.addWidget(self.message_input)

        self.btn_save = QPushButton("Embed & Save (PNG recommended)")
        self.btn_save.setFixedHeight(40)
        self.btn_save.clicked.connect(self.embed_and_save)
        controls_layout.addWidget(self.btn_save)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        controls_layout.addWidget(self.progress)

        self.status = QLabel("")
        controls_layout.addWidget(self.status)

        main_layout.addLayout(controls_layout, 1, 0)

        # Right side: preview
        preview_layout = QVBoxLayout()
        self.preview_label = QLabel("No image selected")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("background: #ffffff; border-radius: 8px;")
        self.preview_label.setFixedSize(560, 360)
        preview_layout.addWidget(self.preview_label, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addLayout(preview_layout, 1, 1)

        self.setLayout(main_layout)

        # Enable drag & drop
        self.setAcceptDrops(True)

    def _toggle_pwd(self, state):
        if state:
            self.pwd_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.pwd_input.setEchoMode(QLineEdit.EchoMode.Password)

    def select_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Image", os.getcwd(), "Images (*.png *.jpg *.jpeg *.bmp)")
        if not path:
            return
        self._set_image(path)

    def _set_image(self, path):
        self.img_path = path
        pix = qpixmap_from_path(path, 520, 360)
        self.preview_label.setPixmap(pix)
        # capacity check
        try:
            img = cv2.imread(path)
            cap = capacity_bits(img)
            self.lbl_capacity.setText(f"Capacity: {cap} bits ≈ {cap//8} bytes")
            size = os.path.getsize(path)
            self.status.setText(f"File: {os.path.basename(path)} — {human_size(size)}")
        except Exception:
            self.lbl_capacity.setText("Capacity: -")
            self.status.setText(f"File: {os.path.basename(path)}")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if not urls:
            return
        path = urls[0].toLocalFile()
        self._set_image(path)

    def embed_and_save(self):
        if not self.img_path:
            QMessageBox.warning(self, "No image", "Please select an image first.")
            return
        text = self.message_input.toPlainText()
        if not text:
            QMessageBox.warning(self, "No message", "Please enter message text to hide.")
            return
        pwd = self.pwd_input.text()
        # quick build blob to check size without repeated heavy ops
        try:
            blob = build_full_blob(text, pwd if pwd else None)
            needed_bits = len(blob) * 8
            import cv2
            img = cv2.imread(self.img_path)
            available = capacity_bits(img)
            if needed_bits + 16 > available:
                QMessageBox.critical(self, "Too big", f"Message too large. Need {needed_bits} bits, available {available} bits.")
                return
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to prepare message: {e}")
            return
        suggested = os.path.join(os.getcwd(), f"stego_{os.path.basename(self.img_path)}")
        out, _ = QFileDialog.getSaveFileName(self, "Save encrypted image (use .png to avoid loss)", suggested, "PNG Image (*.png);;All files (*)")
        if not out:
            return
        # ensure .png for lossless
        if not out.lower().endswith(".png"):
            out = out + ".png"
        try:
            self.progress.setValue(10)
            saved = hide_text(self.img_path, text, pwd if pwd else None, output_path=out)
            self.progress.setValue(100)
            add_entry(os.path.basename(saved), self.img_path, bool(pwd))
            QMessageBox.information(self, "Success", f"Saved encrypted image:\n{saved}")
            self._set_image(saved)
        except Exception as e:
            QMessageBox.critical(self, "Embed failed", str(e))
            self.progress.setValue(0)
