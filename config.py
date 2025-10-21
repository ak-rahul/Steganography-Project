"""Configuration file for steganography application"""

import os

# Application settings
APP_NAME = "Steganography Pro"
APP_VERSION = "2.0.0"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

# File settings
SUPPORTED_FORMATS = [
    ("PNG files", "*.png"),
    ("JPEG files", "*.jpg *.jpeg"),
    ("BMP files", "*.bmp"),
    ("All files", "*.*")
]

OUTPUT_DIR = "encrypted_images"
HISTORY_FILE = "encryption_history.json"

# Image settings
MAX_IMAGE_SIZE = (400, 400)
THUMBNAIL_SIZE = (150, 150)

# Security settings
MIN_PASSWORD_LENGTH = 4
MAX_MESSAGE_LENGTH = 10000

# UI Theme colors (Dark mode)
THEME_DARK = {
    'bg': '#1e1e2e',
    'fg': '#cdd6f4',
    'primary': '#89b4fa',
    'secondary': '#a6e3a1',
    'accent': '#f38ba8',
    'surface': '#313244',
    'border': '#45475a'
}

# UI Theme colors (Light mode)
THEME_LIGHT = {
    'bg': '#eff1f5',
    'fg': '#4c4f69',
    'primary': '#1e66f5',
    'secondary': '#40a02b',
    'accent': '#d20f39',
    'surface': '#e6e9ef',
    'border': '#9ca0b0'
}

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)
