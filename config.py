"""Configuration file"""

import os

APP_NAME = "Steganography-Project"
APP_VERSION = "3.0.0"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800

SUPPORTED_FORMATS = [
    ("PNG files", "*.png"),
    ("JPEG files", "*.jpg *.jpeg"),
    ("BMP files", "*.bmp"),
    ("All files", "*.*")
]

OUTPUT_DIR = "encrypted_images"
MAX_IMAGE_SIZE = (450, 450)
MIN_PASSWORD_LENGTH = 4

STEGO_ALGORITHMS = {
    'LSB': 'Least Significant Bit (Standard)',
    'PVD': 'Pixel Value Differencing (Advanced)',
    'LSB_MATCH': 'LSB Matching (Histogram Preserved)'
}

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Windows 11 Fluent Design Colors
WINDOWS_COLORS = {
    'bg': '#F3F3F3',
    'surface': '#FFFFFF',
    'surface_hover': '#F9F9F9',
    'border': '#E5E5E5',
    'accent': '#0078D4',
    'accent_hover': '#106EBE',
    'accent_pressed': '#005A9E',
    'text': '#000000',
    'text_secondary': '#605E5C',
    'text_disabled': '#A19F9D',
    'success': '#107C10',
    'warning': '#FFB900',
    'error': '#D13438',
    'card_shadow': 'rgba(0, 0, 0, 0.05)'
}
