"""Decrypt Widget - Windows 11 Style"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QLineEdit, QTextEdit, QFrame,
                              QFileDialog, QMessageBox, QCheckBox, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
import os

from core.steganography import Steganography
from core.encryption import PasswordEncryption
from config import *


class DecryptWidget(QWidget):
    """Decryption interface"""
    
    def __init__(self):
        super().__init__()
        self.selected_image = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Left panel - Image
        left_panel = self.create_image_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Right panel - Decryption
        right_panel = self.create_decrypt_panel()
        main_layout.addWidget(right_panel, 1)
    
    def create_image_panel(self):
        """Create image panel"""
        panel = QFrame()
        panel.setObjectName("card")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("🔒 Encrypted Image")
        title.setObjectName("subtitleLabel")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Image display
        self.image_frame = QLabel()
        self.image_frame.setFixedSize(400, 400)
        self.image_frame.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_frame.setStyleSheet("""
            QLabel {
                background-color: #FAFAFA;
                border: 2px dashed #C8C6C4;
                border-radius: 8px;
                color: #8A8886;
            }
        """)
        self.image_frame.setText("No encrypted image\n\n📁 Click Browse")
        layout.addWidget(self.image_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Browse button
        browse_btn = QPushButton("📁 Browse Encrypted Image")
        browse_btn.setObjectName("primaryButton")
        browse_btn.setFixedHeight(45)
        browse_btn.clicked.connect(self.select_image)
        layout.addWidget(browse_btn)
        
        # Info
        info = QLabel("💡 Tip: Select images from 'encrypted_images' folder")
        info.setObjectName("captionLabel")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        layout.addStretch()
        return panel
    
    def create_decrypt_panel(self):
        """Create decrypt panel"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        panel = QFrame()
        panel.setObjectName("card")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🔓 Decrypt Secret Message")
        title.setObjectName("subtitleLabel")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Password
        pwd_label = QLabel("Enter Password:")
        pwd_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(pwd_label)
        
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_entry.setPlaceholderText("Enter decryption password")
        self.password_entry.setFixedHeight(40)
        layout.addWidget(self.password_entry)
        
        self.show_pwd_check = QCheckBox("Show password")
        self.show_pwd_check.stateChanged.connect(self.toggle_password)
        layout.addWidget(self.show_pwd_check)
        
        # Decrypt button
        decrypt_btn = QPushButton("🔓 Decrypt Message")
        decrypt_btn.setObjectName("successButton")
        decrypt_btn.setFixedHeight(45)
        decrypt_btn.clicked.connect(self.decrypt_message)
        layout.addWidget(decrypt_btn)
        
        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("QFrame { background-color: #E5E5E5; max-height: 1px; }")
        layout.addWidget(divider)
        
        # Message display
        msg_label = QLabel("Decrypted Message:")
        msg_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(msg_label)
        
        self.message_text = QTextEdit()
        self.message_text.setReadOnly(True)
        self.message_text.setPlaceholderText("Decrypted message will appear here...")
        self.message_text.setMinimumHeight(200)
        layout.addWidget(self.message_text)
        
        self.stats_label = QLabel("")
        self.stats_label.setObjectName("captionLabel")
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.stats_label)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        copy_btn = QPushButton("📋 Copy")
        copy_btn.setObjectName("secondaryButton")
        copy_btn.setFixedHeight(40)
        copy_btn.clicked.connect(self.copy_message)
        btn_layout.addWidget(copy_btn)
        
        save_btn = QPushButton("💾 Save to File")
        save_btn.setObjectName("secondaryButton")
        save_btn.setFixedHeight(40)
        save_btn.clicked.connect(self.save_to_file)
        btn_layout.addWidget(save_btn)
        
        clear_btn = QPushButton("✕ Clear")
        clear_btn.setObjectName("dangerButton")
        clear_btn.setFixedHeight(40)
        clear_btn.clicked.connect(self.clear_fields)
        btn_layout.addWidget(clear_btn)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        scroll.setWidget(panel)
        return scroll
    
    def select_image(self):
        """Select image"""
        start_dir = OUTPUT_DIR if os.path.exists(OUTPUT_DIR) else ""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Encrypted Image",
            start_dir,
            "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)"
        )
        
        if filename:
            self.selected_image = filename
            pixmap = QPixmap(filename)
            scaled = pixmap.scaled(380, 380, Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
            self.image_frame.setPixmap(scaled)
            self.image_frame.setStyleSheet("""
                QLabel {
                    background-color: #FAFAFA;
                    border: 1px solid #E5E5E5;
                    border-radius: 8px;
                }
            """)
    
    def toggle_password(self, state):
        """Toggle password visibility"""
        if state:
            self.password_entry.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
    
    def decrypt_message(self):
        """Decrypt message"""
        if not self.selected_image:
            QMessageBox.warning(self, "No Image", "Please select an encrypted image!")
            return
        
        password = self.password_entry.text()
        if not password:
            QMessageBox.warning(self, "No Password", "Please enter the password!")
            return
        
        try:
            # Extract
            result = Steganography.decode_message(self.selected_image)
            
            if not result['success']:
                QMessageBox.critical(self, "Error", result['error'])
                return
            
            encrypted_msg = result['message']
            
            # Decrypt
            try:
                decrypted_msg = PasswordEncryption.decrypt_message(encrypted_msg, password)
                
                self.message_text.setPlainText(decrypted_msg)
                
                word_count = len(decrypted_msg.split())
                self.stats_label.setText(
                    f"Length: {len(decrypted_msg):,} characters • {word_count:,} words"
                )
                
                QMessageBox.information(
                    self,
                    "✓ Success",
                    f"Message decrypted successfully!\n\n"
                    f"📝 Length: {len(decrypted_msg):,} characters\n"
                    f"📄 Words: {word_count:,}"
                )
                
            except ValueError:
                QMessageBox.critical(
                    self,
                    "❌ Decryption Failed",
                    "Incorrect password or corrupted data!\n\n"
                    "Please verify:\n"
                    "• Password is correct\n"
                    "• Image hasn't been modified\n"
                    "• Image was encrypted with this tool"
                )
                
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def copy_message(self):
        """Copy to clipboard"""
        message = self.message_text.toPlainText()
        if message:
            from PyQt6.QtWidgets import QApplication
            QApplication.clipboard().setText(message)
            QMessageBox.information(self, "✓ Copied", "Message copied to clipboard!")
        else:
            QMessageBox.warning(self, "No Message", "No message to copy!")
    
    def save_to_file(self):
        """Save to file"""
        message = self.message_text.toPlainText()
        if not message:
            QMessageBox.warning(self, "No Message", "No message to save!")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Message",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(message)
                QMessageBox.information(self, "✓ Saved", f"Message saved to {os.path.basename(filename)}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save: {str(e)}")
    
    def clear_fields(self):
        """Clear fields"""
        self.selected_image = None
        self.password_entry.clear()
        self.message_text.clear()
        self.stats_label.clear()
        self.image_frame.clear()
        self.image_frame.setText("No encrypted image\n\n📁 Click Browse")
        self.image_frame.setStyleSheet("""
            QLabel {
                background-color: #FAFAFA;
                border: 2px dashed #C8C6C4;
                border-radius: 8px;
                color: #8A8886;
            }
        """)
