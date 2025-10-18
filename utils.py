# utils.py
from PyQt6.QtGui import QPixmap
from PIL import Image
import io
import os

def qpixmap_from_path(img_path: str, max_w: int = 520, max_h: int = 360) -> QPixmap:
    img = Image.open(img_path)
    img.thumbnail((max_w, max_h))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    pix = QPixmap()
    pix.loadFromData(buf.read())
    return pix

def human_size(bytes_num: int) -> str:
    for unit in ['B','KB','MB','GB']:
        if bytes_num < 1024.0:
            return f"{bytes_num:3.1f}{unit}"
        bytes_num /= 1024.0
    return f"{bytes_num:.1f}TB"
