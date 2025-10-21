"""Encrypt Widget - Windows 11 Style"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QLineEdit, QTextEdit, QFrame,
                              QRadioButton, QButtonGroup, QFileDialog,
                              QMessageBox, QCheckBox, QProgressBar, QScrollArea)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap
from pathlib import Path
import os

from core.steganography import Steganography
from core.encryption import PasswordEncryption
from config import *


class EncryptWidget(QWidget):
    """Encryption interface"""
    
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
        
        # Right panel - Controls
        right_panel = self.create_control_panel()
        main_layout.addWidget(right_panel, 1)
    
    def create_image_panel(self):
        """Create image selection panel"""
        panel = QFrame()
        panel.setObjectName("card")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("📷 Cover Image")
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
        self.image_frame.setText("No image selected\n\n📁 Click Browse to select")
        layout.addWidget(self.image_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Browse button
        browse_btn = QPushButton("📁 Browse Image")
        browse_btn.setObjectName("primaryButton")
        browse_btn.setFixedHeight(45)
        browse_btn.clicked.connect(self.select_image)
        layout.addWidget(browse_btn)
        
        # Info label
        self.info_label = QLabel("")
        self.info_label.setObjectName("captionLabel")
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)
        
        layout.addStretch()
        return panel
    
    def create_control_panel(self):
        """Create control panel"""
        # Use scroll area for controls
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
        title = QLabel("🔐 Secret Message")
        title.setObjectName("subtitleLabel")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Algorithm selection
        algo_label = QLabel("Algorithm:")
        algo_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(algo_label)
        
        self.algo_group = QButtonGroup()
        algo_layout = QVBoxLayout()
        algo_layout.setSpacing(8)
        
        for i, (key, desc) in enumerate(STEGO_ALGORITHMS.items()):
            radio = QRadioButton(desc)
            radio.setProperty("algo_key", key)
            if i == 0:
                radio.setChecked(True)
            self.algo_group.addButton(radio)
            algo_layout.addWidget(radio)
        
        layout.addLayout(algo_layout)
        layout.addSpacing(5)  # Small gap after algorithm section
        
        # Password
        pwd_label = QLabel("Password:")
        pwd_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(pwd_label)
        
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_entry.setPlaceholderText("Enter strong password")
        self.password_entry.setFixedHeight(40)
        self.password_entry.textChanged.connect(self.check_password_strength)
        layout.addWidget(self.password_entry)
        
        self.show_pwd_check = QCheckBox("Show password")
        self.show_pwd_check.stateChanged.connect(self.toggle_password)
        layout.addWidget(self.show_pwd_check)
        
        self.pwd_strength_label = QLabel("")
        self.pwd_strength_label.setObjectName("captionLabel")
        layout.addWidget(self.pwd_strength_label)
                
        # Message
        msg_label = QLabel("Secret Message:")
        msg_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(msg_label)
        
        self.message_text = QTextEdit()
        self.message_text.setPlaceholderText("Enter your secret message here...")
        self.message_text.setMinimumHeight(180)
        self.message_text.textChanged.connect(self.update_char_count)
        layout.addWidget(self.message_text)
        
        self.char_label = QLabel("Characters: 0")
        self.char_label.setObjectName("captionLabel")
        self.char_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.char_label)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        encrypt_btn = QPushButton("✓ Encrypt & Save")
        encrypt_btn.setObjectName("successButton")
        encrypt_btn.setFixedHeight(45)
        encrypt_btn.clicked.connect(self.encrypt_message)
        btn_layout.addWidget(encrypt_btn)
        
        clear_btn = QPushButton("✕ Clear All")
        clear_btn.setObjectName("dangerButton")
        clear_btn.setFixedHeight(45)
        clear_btn.clicked.connect(self.clear_fields)
        btn_layout.addWidget(clear_btn)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        scroll.setWidget(panel)
        return scroll

    
    def select_image(self):
        """Select image"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Cover Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)"
        )
        
        if filename:
            self.selected_image = filename
            self.display_image(filename)
            self.show_image_info(filename)
    
    def display_image(self, path):
        """Display image"""
        pixmap = QPixmap(path)
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
    
    def show_image_info(self, path):
        """Show image info"""
        result = Steganography.get_image_capacity(path)
        if result['success']:
            self.info_label.setText(
                f"✓ Image loaded • Capacity: {result['max_characters']:,} chars • "
                f"{result['image_dimensions']} • {result['file_size']}"
            )
    
    def toggle_password(self, state):
        """Toggle password visibility"""
        if state:
            self.password_entry.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
    
    def check_password_strength(self):
        """Check password strength"""
        password = self.password_entry.text()
        score = 0
        
        if len(password) >= 8: score += 1
        if len(password) >= 12: score += 1
        if any(c.isupper() for c in password): score += 1
        if any(c.islower() for c in password): score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password): score += 1
        
        strengths = ["Very Weak", "Weak", "Fair", "Good", "Strong", "Very Strong"]
        colors = ["#D13438", "#FFB900", "#FFB900", "#107C10", "#107C10", "#107C10"]
        
        if password:
            strength = strengths[min(score, 5)]
            color = colors[min(score, 5)]
            self.pwd_strength_label.setText(f"Strength: <b style='color:{color}'>{strength}</b>")
        else:
            self.pwd_strength_label.setText("")
    
    def update_char_count(self):
        """Update character count"""
        count = len(self.message_text.toPlainText())
        self.char_label.setText(f"Characters: {count:,}")
    
    def encrypt_message(self):
        """Encrypt and save"""
        if not self.selected_image:
            QMessageBox.warning(self, "No Image", "Please select a cover image!")
            return
        
        password = self.password_entry.text()
        if len(password) < MIN_PASSWORD_LENGTH:
            QMessageBox.warning(self, "Weak Password", 
                              f"Password must be at least {MIN_PASSWORD_LENGTH} characters!")
            return
        
        message = self.message_text.toPlainText().strip()
        if not message:
            QMessageBox.warning(self, "No Message", "Please enter a message!")
            return
        
        try:
            # Get selected algorithm
            algo = "LSB"
            for button in self.algo_group.buttons():
                if button.isChecked():
                    algo = button.property("algo_key")
                    break
            
            # Encrypt
            encrypted_msg = PasswordEncryption.encrypt_message(message, password)
            
            # Output path
            base_name = Path(self.selected_image).stem
            output_path = os.path.join(
                OUTPUT_DIR,
                f"{base_name}_encrypted_{len(os.listdir(OUTPUT_DIR))}.png"
            )
            
            # Encode
            result = Steganography.encode_message(
                self.selected_image,
                encrypted_msg,
                output_path,
                method=algo
            )
            
            if result['success']:
                psnr = Steganography.calculate_psnr(self.selected_image, output_path)
                
                QMessageBox.information(
                    self,
                    "✓ Success",
                    f"Message encrypted successfully!\n\n"
                    f"📁 File: {os.path.basename(output_path)}\n"
                    f"📝 Length: {len(message):,} characters\n"
                    f"🔐 Algorithm: {STEGO_ALGORITHMS[algo]}\n"
                    f"📊 Capacity: {result['capacity_used']:.2f}%\n"
                    f"📈 PSNR: {psnr:.2f} dB"
                )
                self.clear_fields()
            else:
                QMessageBox.critical(self, "Error", result['error'])
                
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def clear_fields(self):
        """Clear all fields"""
        self.selected_image = None
        self.password_entry.clear()
        self.message_text.clear()
        self.char_label.setText("Characters: 0")
        self.pwd_strength_label.setText("")
        self.info_label.setText("")
        self.image_frame.clear()
        self.image_frame.setText("No image selected\n\n📁 Click Browse to select")
        self.image_frame.setStyleSheet("""
            QLabel {
                background-color: #FAFAFA;
                border: 2px dashed #C8C6C4;
                border-radius: 8px;
                color: #8A8886;
            }
        """)
