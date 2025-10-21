"""Batch Widget - Windows 11 Style"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QFrame, QFileDialog, QMessageBox,
                              QTextEdit, QListWidget, QProgressBar, QRadioButton,
                              QButtonGroup, QLineEdit)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from pathlib import Path
import os

from core.steganography import Steganography
from core.encryption import PasswordEncryption
from config import *


class BatchProcessThread(QThread):
    """Background thread for batch processing"""
    progress = pyqtSignal(int, int, str)  # current, total, status
    finished = pyqtSignal(int, int)  # success, total
    
    def __init__(self, files, message, password, algorithm):
        super().__init__()
        self.files = files
        self.message = message
        self.password = password
        self.algorithm = algorithm
    
    def run(self):
        """Process files"""
        success = 0
        for idx, file_path in enumerate(self.files):
            try:
                encrypted_msg = PasswordEncryption.encrypt_message(self.message, self.password)
                output_path = os.path.join(
                    OUTPUT_DIR,
                    f"batch_{Path(file_path).stem}_{idx}.png"
                )
                
                result = Steganography.encode_message(
                    file_path,
                    encrypted_msg,
                    output_path,
                    method=self.algorithm
                )
                
                if result['success']:
                    success += 1
                    self.progress.emit(idx + 1, len(self.files), "✓ Success")
                else:
                    self.progress.emit(idx + 1, len(self.files), "✗ Failed")
            except Exception:
                self.progress.emit(idx + 1, len(self.files), "✗ Error")
        
        self.finished.emit(success, len(self.files))


class BatchWidget(QWidget):
    """Batch processing interface"""
    
    def __init__(self):
        super().__init__()
        self.file_list = []
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header
        header = QFrame()
        header_layout = QHBoxLayout(header)
        
        title = QLabel("📦 Batch Processing")
        title.setObjectName("subtitleLabel")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        header_layout.addWidget(title)
        
        desc = QLabel("Encrypt multiple images with the same message")
        desc.setObjectName("bodyLabel")
        header_layout.addWidget(desc)
        header_layout.addStretch()
        
        main_layout.addWidget(header)
        
        # File list card
        list_card = QFrame()
        list_card.setObjectName("card")
        list_layout = QVBoxLayout(list_card)
        list_layout.setContentsMargins(15, 15, 15, 15)
        
        list_header = QLabel("Selected Images:")
        list_header.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        list_layout.addWidget(list_header)
        
        self.file_listbox = QListWidget()
        self.file_listbox.setMinimumHeight(150)
        list_layout.addWidget(self.file_listbox)
        
        # File buttons
        file_btn_layout = QHBoxLayout()
        
        add_btn = QPushButton("📁 Add Images")
        add_btn.setObjectName("primaryButton")
        add_btn.clicked.connect(self.add_files)
        file_btn_layout.addWidget(add_btn)
        
        clear_btn = QPushButton("🗑️ Clear All")
        clear_btn.setObjectName("dangerButton")
        clear_btn.clicked.connect(self.clear_files)
        file_btn_layout.addWidget(clear_btn)
        
        self.count_label = QLabel("Files: 0")
        self.count_label.setObjectName("bodyLabel")
        file_btn_layout.addStretch()
        file_btn_layout.addWidget(self.count_label)
        
        list_layout.addLayout(file_btn_layout)
        main_layout.addWidget(list_card)
        
        # Settings card
        settings_card = QFrame()
        settings_card.setObjectName("card")
        settings_layout = QVBoxLayout(settings_card)
        settings_layout.setContentsMargins(15, 15, 15, 15)
        
        settings_label = QLabel("Settings:")
        settings_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        settings_layout.addWidget(settings_label)
        
        # Algorithm
        algo_label = QLabel("Algorithm:")
        algo_label.setObjectName("bodyLabel")
        settings_layout.addWidget(algo_label)
        
        self.algo_group = QButtonGroup()
        algo_layout = QHBoxLayout()
        for i, (key, desc) in enumerate(STEGO_ALGORITHMS.items()):
            radio = QRadioButton(key)
            radio.setProperty("algo_key", key)
            if i == 0:
                radio.setChecked(True)
            self.algo_group.addButton(radio)
            algo_layout.addWidget(radio)
        algo_layout.addStretch()
        settings_layout.addLayout(algo_layout)
        
        # Password
        pwd_label = QLabel("Password (same for all):")
        pwd_label.setObjectName("bodyLabel")
        settings_layout.addWidget(pwd_label)
        
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_entry.setPlaceholderText("Enter password")
        self.password_entry.setFixedHeight(35)
        settings_layout.addWidget(self.password_entry)
        
        # Message
        msg_label = QLabel("Message (same for all):")
        msg_label.setObjectName("bodyLabel")
        settings_layout.addWidget(msg_label)
        
        self.message_text = QTextEdit()
        self.message_text.setPlaceholderText("Enter message...")
        self.message_text.setMaximumHeight(100)
        settings_layout.addWidget(self.message_text)
        
        main_layout.addWidget(settings_card)
        
        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        main_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("")
        self.status_label.setObjectName("captionLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # Process button
        process_btn = QPushButton("⚡ Process All Images")
        process_btn.setObjectName("successButton")
        process_btn.setFixedHeight(50)
        process_btn.clicked.connect(self.process_batch)
        main_layout.addWidget(process_btn)
    
    def add_files(self):
        """Add files"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Images",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)"
        )
        
        for file in files:
            if file not in self.file_list:
                self.file_list.append(file)
                self.file_listbox.addItem(f"📄 {os.path.basename(file)}")
        
        self.count_label.setText(f"Files: {len(self.file_list)}")
    
    def clear_files(self):
        """Clear files"""
        self.file_list = []
        self.file_listbox.clear()
        self.count_label.setText("Files: 0")
        self.progress_bar.setValue(0)
        self.status_label.setText("")
    
    def process_batch(self):
        """Process all files"""
        if not self.file_list:
            QMessageBox.warning(self, "No Files", "Please add images first!")
            return
        
        password = self.password_entry.text()
        if len(password) < MIN_PASSWORD_LENGTH:
            QMessageBox.warning(
                self,
                "Weak Password",
                f"Password must be at least {MIN_PASSWORD_LENGTH} characters!"
            )
            return
        
        message = self.message_text.toPlainText().strip()
        if not message:
            QMessageBox.warning(self, "No Message", "Please enter a message!")
            return
        
        # Get algorithm
        algo = "LSB"
        for button in self.algo_group.buttons():
            if button.isChecked():
                algo = button.property("algo_key")
                break
        
        # Start processing thread
        self.thread = BatchProcessThread(self.file_list, message, password, algo)
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.processing_finished)
        self.thread.start()
        
        self.status_label.setText("Processing...")
    
    def update_progress(self, current, total, status):
        """Update progress"""
        progress = int((current / total) * 100)
        self.progress_bar.setValue(progress)
        self.status_label.setText(f"Processing {current}/{total}...")
    
    def processing_finished(self, success, total):
        """Processing complete"""
        self.status_label.setText(f"Complete! {success}/{total} successful")
        
        QMessageBox.information(
            self,
            "✓ Batch Complete",
            f"Processing finished!\n\n"
            f"Successful: {success}/{total}\n"
            f"Failed: {total - success}\n\n"
            f"Files saved to: {OUTPUT_DIR}"
        )
