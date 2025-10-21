"""Main Window - Windows 11 Style"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QStackedWidget, QListWidget, QLabel, QStatusBar, 
                              QFrame, QListWidgetItem)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

from gui.encrypt_widget import EncryptWidget
from gui.decrypt_widget import DecryptWidget
from gui.analysis_widget import AnalysisWidget
from gui.batch_widget import BatchWidget
from config import *


class MainWindow(QMainWindow):
    """Main Application Window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} {APP_VERSION}")
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.center_window()
        self.setup_ui()
    
    def center_window(self):
        """Center window on screen"""
        screen = self.screen().geometry()
        x = (screen.width() - WINDOW_WIDTH) // 2
        y = (screen.height() - WINDOW_HEIGHT) // 2
        self.move(x, y)
    
    def setup_ui(self):
        """Setup the main UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Content area
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = self.create_sidebar()
        content_layout.addWidget(self.sidebar)
        
        # Pages
        self.pages = QStackedWidget()
        self.pages.setStyleSheet("QStackedWidget { background-color: #F3F3F3; }")
        
        self.pages.addWidget(EncryptWidget())
        self.pages.addWidget(DecryptWidget())
        self.pages.addWidget(AnalysisWidget())
        self.pages.addWidget(BatchWidget())
        
        content_layout.addWidget(self.pages, 1)
        main_layout.addLayout(content_layout)
        
        # Status bar
        status_bar = QStatusBar()
        status_bar.showMessage(f"Ready • {APP_NAME} v{APP_VERSION}")
        self.setStatusBar(status_bar)
        
        self.sidebar.currentRowChanged.connect(self.pages.setCurrentIndex)
    
    def create_header(self):
        """Create header"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #FAFAFA;
                border-bottom: 1px solid #E5E5E5;
            }
        """)
        header.setFixedHeight(70)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(30, 10, 30, 10)
        
        title_label = QLabel(f"🔐 {APP_NAME}")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        layout.addStretch()
        
        subtitle = QLabel("Advanced Image Steganography")
        subtitle.setObjectName("bodyLabel")
        subtitle.setFont(QFont("Segoe UI", 12))
        layout.addWidget(subtitle)
        
        return header
    
    def create_sidebar(self):
        """Create sidebar navigation"""
        sidebar = QListWidget()
        sidebar.setFixedWidth(240)
        
        items = [
            "🔒  Encrypt Message",
            "🔓  Decrypt Message",
            "🔍  Steganalysis",
            "📦  Batch Processing"
        ]
        
        for title in items:
            item = QListWidgetItem(title)
            item.setFont(QFont("Segoe UI", 13))
            item.setSizeHint(QSize(220, 50))
            sidebar.addItem(item)
        
        sidebar.setCurrentRow(0)
        return sidebar
