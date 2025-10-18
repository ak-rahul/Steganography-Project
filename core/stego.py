# core/stego.py
import os
import enum
import zlib
import secrets
import hashlib
from typing import Tuple, Optional

import cv2
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Format:
# MAGIC (6 bytes) | VERSION (1 byte) | KDF_SALT_LEN(1) | kdf_salt | nonce(12) | payload_len(4 BE) | ciphertext (payload_len bytes)
# We choose: MAGIC=b"STEGX3", VERSION=0x03, kdf_salt len = 16
MAGIC = b"STEGX3"
VERSION = b"\x03"
KDF_SALT_LEN = 16
NONCE_LEN = 12
LEN_BYTES = 4  # payload length storage

# legacy compatibility: older algorithm was unstructured LSB marking with stop bits.
# We'll implement a permissive fallback.

def _derive_key(password: str, salt: bytes, iterations: int = 200000) -> bytes:
    """
    Derive a 32-byte AES key using PBKDF2-HMAC-SHA256.
    """
    if password is None:
        password = ""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return kdf.derive(password.encode("utf-8"))

def _bytes_to_bits(data: bytes):
    bits = []
    for b in data:
        for i in reversed(range(8)):
            bits.append((b >> i) & 1)
    return bits

def _bits_to_bytes(bits):
    b = bytearray()
    for i in range(0, len(bits), 8):
        chunk = bits[i:i+8]
        if len(chunk) < 8:
            break
        val = 0
        for bit in chunk:
            val = (val << 1) | (bit & 1)
        b.append(val)
    return bytes(b)

def capacity_bits(img) -> int:
    h, w, ch = img.shape
    return h * w * ch

def pack_payload(message: str, password: Optional[str]) -> bytes:
    """
    Compress and encrypt message, return full payload (excluding any outer header fields).
    We'll return: kdf_salt + nonce + payload_len(4) + ciphertext
    But higher-level code will add MAGIC + VERSION at front.
    """
    raw = message.encode("utf-8")
    compressed = zlib.compress(raw)
    # derive key if password provided, else use zeros key with random salt
    salt = secrets.token_bytes(KDF_SALT_LEN)
    key = _derive_key(password if password else "", salt)
    aes = AESGCM(key)
    nonce = secrets.token_bytes(NONCE_LEN)
    ct = aes.encrypt(nonce, compressed, None)  # ciphertext includes auth tag appended
    payload_len = len(ct).to_bytes(LEN_BYTES, "big")
    return salt + nonce + payload_len + ct

def build_full_blob(message: str, password: Optional[str]) -> bytes:
    """
    Returns bytes to embed: MAGIC + VERSION + payload_blob
    where payload_blob = salt + nonce + len + ct
    """
    payload = pack_payload(message, password)
    return MAGIC + VERSION + payload

def unpackage_and_decrypt(blob: bytes, password: Optional[str]) -> str:
    """
    Given blob starting with MAGIC+VERSION, try to decrypt and decompress.
    Raises ValueError on issues.
    """
    if len(blob) < (len(MAGIC) + 1 + KDF_SALT_LEN + NONCE_LEN + LEN_BYTES):
        raise ValueError("Blob too short/corrupted.")
    if blob[:len(MAGIC)] != MAGIC:
        raise ValueError("Invalid MAGIC header.")
    version = blob[len(MAGIC)]
    if version != VERSION[0]:
        raise ValueError("Unsupported version.")
    offset = len(MAGIC) + 1
    salt = blob[offset:offset + KDF_SALT_LEN]; offset += KDF_SALT_LEN
    nonce = blob[offset:offset + NONCE_LEN]; offset += NONCE_LEN
    payload_len = int.from_bytes(blob[offset:offset + LEN_BYTES], "big"); offset += LEN_BYTES
    ct = blob[offset: offset + payload_len]
    if len(ct) != payload_len:
        raise ValueError("Payload length mismatch.")
    key = _derive_key(password if password else "", salt)
    aes = AESGCM(key)
    try:
        decompressed = aes.decrypt(nonce, ct, None)
    except Exception as e:
        raise ValueError("Decryption failed. Wrong password or corrupted data.") from e
    try:
        raw = zlib.decompress(decompressed)
    except Exception as e:
        raise ValueError("Decompression failed.") from e
    return raw.decode("utf-8")

def hide_text(input_path: str, message: str, password: Optional[str], output_path: Optional[str] = None) -> str:
    """
    Embed structured blob into image LSBs and write PNG.
    Returns output_path.
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError("Input image not found.")
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError("Failed to read input image.")
    blob = build_full_blob(message, password)
    bits = _bytes_to_bits(blob)
    available = capacity_bits(img)
    if len(bits) + 16 > available:
        raise ValueError(f"Message too large to embed. Need {len(bits)} bits, available {available} bits.")
    h, w, ch = img.shape
    bit_idx = 0
    for y in range(h):
        for x in range(w):
            for c in range(ch):
                if bit_idx >= len(bits):
                    break
                img[y, x, c] = (int(img[y, x, c]) & ~1) | bits[bit_idx]
                bit_idx += 1
            if bit_idx >= len(bits):
                break
        if bit_idx >= len(bits):
            break
    if output_path is None:
        base = os.path.basename(input_path)
        output_path = os.path.join(os.getcwd(), f"stego_{base}")
    # force PNG to avoid compression issues
    cv2.imwrite(output_path, img)
    return output_path

def extract_text(image_path: str, password: Optional[str]) -> Tuple[str, bool]:
    """
    Extract and return (message, used_structured_blob_flag).
    If structured header not found, attempt legacy fallback and return (message, False).
    """
    if not os.path.isfile(image_path):
        raise FileNotFoundError("Image not found.")
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not open image.")
    h, w, ch = img.shape
    total_bits = h * w * ch
    # Read at least enough bits to include header minimal
    header_bits_needed = (len(MAGIC) + 1 + KDF_SALT_LEN + NONCE_LEN + LEN_BYTES) * 8
    header_bits = []
    bit_count = 0
    for y in range(h):
        for x in range(w):
            for c in range(ch):
                header_bits.append(int(img[y, x, c]) & 1)
                bit_count += 1
                if bit_count >= header_bits_needed:
                    break
            if bit_count >= header_bits_needed:
                break
        if bit_count >= header_bits_needed:
            break
    header_bytes = _bits_to_bytes(header_bits)
    # check MAGIC
    if header_bytes[:len(MAGIC)] == MAGIC and header_bytes[len(MAGIC)] == VERSION[0]:
        # we have structured blob; parse payload_len to know how many bits to fetch
        # Reconstruct enough bits for the whole blob: salt + nonce + len + ciphertext
        # We need to read LEN_BYTES to know ciphertext length: bytes are located after magic+ver+salt+nonce
        # For simplicity, read large chunk: header + max payload limited by capacity
        # We'll extract all bits up to total_bits and then slice bytes.
        all_bits = []
        idx = 0
        for y in range(h):
            for x in range(w):
                for c in range(ch):
                    all_bits.append(int(img[y, x, c]) & 1)
                    idx += 1
                    if idx >= total_bits:
                        break
                if idx >= total_bits:
                    break
            if idx >= total_bits:
                break
        all_bytes = _bits_to_bytes(all_bits)
        try:
            message = unpackage_and_decrypt(all_bytes, password if password else "")
            return message, True
        except Exception as e:
            # bubble up descriptive error
            raise
    # Legacy fallback (best-effort): same technique as your original Tkinter app
    bits = []
    stop = False
    for row in img:
        for pixel in row:
            # append LSBs of all three channels
            bits.append(int(pixel[0]) & 1)
            bits.append(int(pixel[1]) & 1)
            bits.append(int(pixel[2]) & 1)
    bytes_data = _bits_to_bytes(bits)
    # Try to convert bytes until you find a likely stop (e.g., many zeros trailing)
    try:
        text = bytes_data.rstrip(b'\x00').decode('utf-8', errors='ignore')
        if not text:
            raise ValueError("Legacy decode produced empty string.")
        return text, False
    except Exception as e:
        raise ValueError("No structured stego header found and legacy decode failed.") from e
