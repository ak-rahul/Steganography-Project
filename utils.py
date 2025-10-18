# utils.py
from PIL import Image
from PyQt6.QtGui import QPixmap
import io

def qpixmap_from_path(img_path: str, max_w: int, max_h: int) -> QPixmap:
    """
    Load an image path and return a scaled QPixmap (keeps aspect ratio).
    """
    img = Image.open(img_path)
    img.thumbnail((max_w, max_h))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    pix = QPixmap()
    pix.loadFromData(buf.getvalue())
    return pix
