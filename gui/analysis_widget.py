"""Analysis Widget - Windows 11 Style"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QFrame, QFileDialog, QMessageBox,
                              QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
import os

from core.steganalysis import Steganalysis
from config import *


class AnalysisWidget(QWidget):
    """Steganalysis interface"""
    
    def __init__(self):
        super().__init__()
        self.selected_image = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Left panel
        left_panel = self.create_image_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Right panel
        right_panel = self.create_results_panel()
        main_layout.addWidget(right_panel, 1)
    
    def create_image_panel(self):
        """Create image panel"""
        panel = QFrame()
        panel.setObjectName("card")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("🔍 Steganalysis")
        title.setObjectName("subtitleLabel")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        desc = QLabel("Detect hidden messages in suspicious images")
        desc.setObjectName("bodyLabel")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
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
        self.image_frame.setText("No image selected\n\n📁 Click Browse")
        layout.addWidget(self.image_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Buttons
        browse_btn = QPushButton("📁 Browse Image")
        browse_btn.setObjectName("primaryButton")
        browse_btn.setFixedHeight(45)
        browse_btn.clicked.connect(self.select_image)
        layout.addWidget(browse_btn)
        
        analyze_btn = QPushButton("🔍 Run Full Analysis")
        analyze_btn.setObjectName("successButton")
        analyze_btn.setFixedHeight(45)
        analyze_btn.clicked.connect(self.analyze_image)
        layout.addWidget(analyze_btn)
        
        layout.addStretch()
        return panel
    
    def create_results_panel(self):
        """Create results panel"""
        panel = QFrame()
        panel.setObjectName("card")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("📊 Analysis Results")
        title.setObjectName("subtitleLabel")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Results text
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setFont(QFont("Consolas", 10))
        self.results_text.setPlainText(
            "╔═══════════════════════════════════════════╗\n"
            "║    STEGANOGRAPHY DETECTION SYSTEM         ║\n"
            "╚═══════════════════════════════════════════╝\n\n"
            "Select an image and click 'Run Full Analysis'\n\n"
            "Detection Methods:\n"
            "  • Chi-Square Attack\n"
            "  • LSB Bit Pattern Analysis\n"
            "  • Entropy Analysis\n\n"
            "Ready to analyze..."
        )
        layout.addWidget(self.results_text)
        
        # Clear button
        clear_btn = QPushButton("✕ Clear Results")
        clear_btn.setObjectName("dangerButton")
        clear_btn.setFixedHeight(40)
        clear_btn.clicked.connect(self.clear_results)
        layout.addWidget(clear_btn)
        
        return panel
    
    def select_image(self):
        """Select image"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image to Analyze",
            "",
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
    
    def analyze_image(self):
        """Analyze image"""
        if not self.selected_image:
            QMessageBox.warning(self, "No Image", "Please select an image to analyze!")
            return
        
        try:
            result = Steganalysis.full_analysis(self.selected_image)
            
            import datetime
            report = f"""
╔═══════════════════════════════════════════╗
║         STEGANALYSIS REPORT               ║
╚═══════════════════════════════════════════╝

File: {os.path.basename(self.selected_image)}
Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1] CHI-SQUARE TEST
    Score: {result['chi_square']['score']:.4f}
    Status: {result['chi_square']['message']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[2] LSB BIT PATTERN ANALYSIS
    Randomness: {result['lsb']['randomness']:.2f}%
    Status: {result['lsb']['message']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[3] ENTROPY ANALYSIS
    Entropy: {result['entropy']['entropy']:.4f}
    Expected: {result['entropy']['expected']}
    Status: {result['entropy']['message']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FINAL VERDICT:
{result['verdict']}

Confidence Level: {result['confidence']:.1f}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommendation:
"""
            
            if result['confidence'] >= 66:
                report += "⚠️ HIGH PROBABILITY of hidden data.\nManual inspection recommended."
            elif result['confidence'] >= 33:
                report += "⚠️ MODERATE PROBABILITY.\nSome indicators present."
            else:
                report += "✓ LOW PROBABILITY.\nImage appears clean."
            
            report += "\n\n═══════════════════════════════════════════════"
            
            self.results_text.setPlainText(report)
            
            if result['confidence'] >= 66:
                QMessageBox.warning(
                    self,
                    "⚠️ Hidden Data Detected",
                    f"Analysis indicates {result['confidence']:.0f}% probability\n"
                    f"of hidden data!\n\n"
                    f"Verdict: {result['verdict']}"
                )
            else:
                QMessageBox.information(
                    self,
                    "✓ Analysis Complete",
                    f"Analysis complete.\n\n"
                    f"Confidence: {result['confidence']:.0f}%\n"
                    f"Verdict: {result['verdict']}"
                )
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Analysis failed: {str(e)}")
    
    def clear_results(self):
        """Clear results"""
        self.results_text.setPlainText(
            "╔═══════════════════════════════════════════╗\n"
            "║    STEGANOGRAPHY DETECTION SYSTEM         ║\n"
            "╚═══════════════════════════════════════════╝\n\n"
            "Ready to analyze..."
        )
