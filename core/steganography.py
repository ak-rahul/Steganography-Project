# core/steganography.py
"""
Steganography core:
- AES-256-GCM encryption (cryptography)
- zlib compression
- self-contained header format: MAGIC(6) | VERSION(1) | payload_len(4 BE) | nonce(12) | tag(16) | ciphertext
- LSB embedding into image channels (one bit per channel)
- Functions: hide_text, extract_text, capacity_bits
"""

import cv2
import zlib
import os
import secrets
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from typing import Tuple

MAGIC = b"STEGX2"   # 6 bytes
VERSION = b"\x01"   # 1 byte
HEADER_FIXED_LEN = 6 + 1 + 4 + 12 + 16  # magic + version + len + nonce + tag

def _derive_key(password: str) -> bytes:
    if password is None:
        password = ""
    return hashlib.sha256(password.encode("utf-8")).digest()

def _bytes_to_bits(data: bytes):
    bits = []
    for byte in data:
        for i in reversed(range(8)):
            bits.append((byte >> i) & 1)
    return bits

def _bits_to_bytes(bits):
    out = bytearray()
    for i in range(0, len(bits), 8):
        chunk = bits[i:i+8]
        if len(chunk) < 8:
            break
        val = 0
        for b in chunk:
            val = (val << 1) | (b & 1)
        out.append(val)
    return bytes(out)

def capacity_bits(img) -> int:
    """Number of LSB bits available = height * width * channels"""
    h, w, c = img.shape
    return h * w * c

def pack_payload(message: str, password: str) -> bytes:
    """Compress and encrypt message, return header+ciphertext bytes."""
    raw = message.encode("utf-8")
    compressed = zlib.compress(raw)
    key = _derive_key(password)
    aes = AESGCM(key)
    nonce = secrets.token_bytes(12)
    ciphertext = aes.encrypt(nonce, compressed, None)  # ciphertext includes tag at end (AESGCM returns ciphertext+tag)
    # AESGCM returns ciphertext+tag; tag is last 16 bytes. We'll split for clarity.
    tag = ciphertext[-16:]
    ct = ciphertext[:-16]
    length = len(ct).to_bytes(4, "big")
    payload = MAGIC + VERSION + length + nonce + tag + ct
    return payload

def unpack_payload(payload: bytes, password: str) -> str:
    """Given raw payload bytes (header + ct), decrypt and return message string."""
    if len(payload) < HEADER_FIXED_LEN:
        raise ValueError("Payload too small/corrupted.")
    if payload[:6] != MAGIC:
        raise ValueError("Invalid magic header.")
    # version = payload[6]
    payload_len = int.from_bytes(payload[7:11], "big")
    nonce = payload[11:23]
    tag = payload[23:39]
    ct = payload[39:]
    if len(ct) != payload_len:
        # we allow mismatch but raise to indicate possible corruption
        raise ValueError("Payload length mismatch.")
    key = _derive_key(password)
    aes = AESGCM(key)
    combined = ct + tag
    try:
        decompressed = aes.decrypt(nonce, combined, None)
    except Exception as e:
        raise ValueError("Decryption failed (wrong password or corrupted data).") from e
    message = zlib.decompress(decompressed).decode("utf-8")
    return message

def hide_text(input_path: str, message: str, password: str, output_path: str = None) -> str:
    """
    Embed message into input image and save as output_path.
    Returns output file path.
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError("Input image not found.")
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError("Cannot read input image.")
    payload = pack_payload(message, password if password else "")
    bits = _bytes_to_bits(payload)
    available = capacity_bits(img)
    if len(bits) + 16 > available:  # small slack
        raise ValueError(f"Message too large for this image. Required bits {len(bits)}, available {available}.")
    h, w, c = img.shape
    bit_idx = 0
    for y in range(h):
        for x in range(w):
            for ch in range(c):
                if bit_idx >= len(bits):
                    break
                # set LSB
                img[y, x, ch] = (int(img[y, x, ch]) & ~1) | bits[bit_idx]
                bit_idx += 1
            if bit_idx >= len(bits):
                break
        if bit_idx >= len(bits):
            break
    if not output_path:
        base = os.path.basename(input_path)
        output_path = os.path.join(os.getcwd(), f"stego_{base}")
    cv2.imwrite(output_path, img)
    return output_path

def extract_text(image_path: str, password: str) -> str:
    """
    Extract embedded message from image. Returns the message string.
    Raises ValueError if no message or wrong password.
    """
    if not os.path.isfile(image_path):
        raise FileNotFoundError("Image not found.")
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Cannot open image.")
    h, w, c = img.shape
    total_bits = h * w * c
    # read header bits first
    header_bits_needed = HEADER_FIXED_LEN * 8
    header_bits = []
    idx = 0
    for y in range(h):
        for x in range(w):
            for ch in range(c):
                header_bits.append(int(img[y, x, ch]) & 1)
                idx += 1
                if idx >= header_bits_needed:
                    break
            if idx >= header_bits_needed:
                break
        if idx >= header_bits_needed:
            break
    header_bytes = _bits_to_bytes(header_bits)
    if header_bytes[:6] != MAGIC:
        raise ValueError("No valid embedded stego header found.")
    payload_len = int.from_bytes(header_bytes[7:11], "big")
    total_payload_bits = (HEADER_FIXED_LEN + payload_len) * 8
    # now read full payload bits
    bits = []
    idx = 0
    for y in range(h):
        for x in range(w):
            for ch in range(c):
                bits.append(int(img[y, x, ch]) & 1)
                idx += 1
                if idx >= total_payload_bits:
                    break
            if idx >= total_payload_bits:
                break
        if idx >= total_payload_bits:
            break
    payload_bytes = _bits_to_bytes(bits)
    try:
        message = unpack_payload(payload_bytes, password if password else "")
    except Exception as e:
        # bubble up informative message
        raise
    return message
