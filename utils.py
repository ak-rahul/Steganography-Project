# utils.py
from PIL import Image
from PyQt6.QtGui import QPixmap
import io
import cv2

def qpixmap_from_cv2(img_path: str, max_w: int, max_h: int) -> QPixmap:
    """
    Load image path and return a QPixmap scaled to max_w x max_h preserving aspect ratio.
    """
    img = Image.open(img_path)
    img.thumbnail((max_w, max_h))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    pix = QPixmap()
    pix.loadFromData(buf.read())
    return pix
