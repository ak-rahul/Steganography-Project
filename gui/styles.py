"""Windows 11 Fluent Design Stylesheet"""

WINDOWS_STYLE = """
/* Main Window */
QMainWindow {
    background-color: #F3F3F3;
}

/* Sidebar Navigation */
QListWidget {
    background-color: #FAFAFA;
    border: none;
    border-right: 1px solid #E5E5E5;
    outline: none;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
    padding: 8px 0px;
}

QListWidget::item {
    padding: 14px 20px;
    margin: 3px 8px;
    border-radius: 6px;
    color: #323130;
}

QListWidget::item:hover {
    background-color: #F3F3F3;
}

QListWidget::item:selected {
    background-color: #E6F3FF;
    color: #0078D4;
    font-weight: 600;
}

/* Cards */
QWidget#cardWidget {
    background-color: #FFFFFF;
    border: 1px solid #E5E5E5;
    border-radius: 8px;
}

QFrame#card {
    background-color: #FFFFFF;
    border: 1px solid #E5E5E5;
    border-radius: 8px;
}

/* Buttons - Primary */
QPushButton#primaryButton {
    background-color: #0078D4;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 11px 24px;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
    font-weight: 600;
}

QPushButton#primaryButton:hover {
    background-color: #106EBE;
}

QPushButton#primaryButton:pressed {
    background-color: #005A9E;
}

/* Buttons - Secondary */
QPushButton#secondaryButton {
    background-color: transparent;
    color: #323130;
    border: 1px solid #8A8886;
    border-radius: 6px;
    padding: 11px 24px;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
    font-weight: 600;
}

QPushButton#secondaryButton:hover {
    background-color: #F3F3F3;
}

/* Buttons - Success */
QPushButton#successButton {
    background-color: #107C10;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 11px 24px;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
    font-weight: 600;
}

QPushButton#successButton:hover {
    background-color: #0E6B0E;
}

/* Buttons - Danger */
QPushButton#dangerButton {
    background-color: #D13438;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 11px 24px;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
    font-weight: 600;
}

QPushButton#dangerButton:hover {
    background-color: #A72C2F;
}

/* Text Inputs */
QLineEdit {
    background-color: #FFFFFF;
    border: 1px solid #8A8886;
    border-bottom: 2px solid #8A8886;
    border-radius: 4px;
    padding: 10px 12px;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
    color: #323130;
}

QLineEdit:focus {
    border-bottom: 2px solid #0078D4;
}

QTextEdit, QPlainTextEdit {
    background-color: #FFFFFF;
    border: 1px solid #8A8886;
    border-radius: 6px;
    padding: 10px;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
    color: #323130;
}

QTextEdit:focus, QPlainTextEdit:focus {
    border: 2px solid #0078D4;
}

/* Labels */
QLabel {
    font-family: 'Segoe UI', sans-serif;
    color: #323130;
    background-color: transparent;
}

QLabel#titleLabel {
    font-size: 20px;
    font-weight: 600;
    color: #323130;
}

QLabel#subtitleLabel {
    font-size: 16px;
    font-weight: 600;
    color: #323130;
}

QLabel#bodyLabel {
    font-size: 14px;
    color: #605E5C;
}

QLabel#captionLabel {
    font-size: 12px;
    color: #8A8886;
}

/* Scrollbars */
QScrollBar:vertical {
    background: #F3F3F3;
    width: 14px;
    border-radius: 7px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #C8C6C4;
    border-radius: 7px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #A19F9D;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Radio Buttons */
QRadioButton {
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
    color: #323130;
    spacing: 10px;
}

QRadioButton::indicator {
    width: 20px;
    height: 20px;
    border: 2px solid #8A8886;
    border-radius: 10px;
    background-color: #FFFFFF;
}

QRadioButton::indicator:hover {
    border-color: #0078D4;
}

QRadioButton::indicator:checked {
    background-color: #FFFFFF;
    border-color: #0078D4;
    border-width: 6px;
}

/* Checkboxes */
QCheckBox {
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
    color: #323130;
    spacing: 10px;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border: 2px solid #8A8886;
    border-radius: 4px;
    background-color: #FFFFFF;
}

QCheckBox::indicator:hover {
    border-color: #0078D4;
}

QCheckBox::indicator:checked {
    background-color: #0078D4;
    border-color: #0078D4;
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTAiIHZpZXdCb3g9IjAgMCAxMiAxMCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEgNUw0LjUgOC41TDExIDEiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+Cjwvc3ZnPgo=);
}

/* Progress Bar */
QProgressBar {
    background-color: #E1E1E1;
    border: none;
    border-radius: 4px;
    height: 8px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #0078D4;
    border-radius: 4px;
}

/* Status Bar */
QStatusBar {
    background-color: #FAFAFA;
    border-top: 1px solid #E5E5E5;
    font-family: 'Segoe UI', sans-serif;
    font-size: 12px;
    color: #605E5C;
    padding: 5px;
}

/* ComboBox */
QComboBox {
    background-color: #FFFFFF;
    border: 1px solid #8A8886;
    border-radius: 4px;
    padding: 8px 12px;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
    color: #323130;
    min-width: 150px;
}

QComboBox:hover {
    border-color: #0078D4;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #605E5C;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1px solid #E5E5E5;
    border-radius: 6px;
    selection-background-color: #F3F3F3;
    selection-color: #323130;
    outline: none;
}
"""


def apply_windows_theme(app):
    """Apply Windows 11 Fluent Design theme"""
    if app:
        app.setStyle('Fusion')
        app.setStyleSheet(WINDOWS_STYLE)
