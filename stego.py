# stego.py
import cv2
import math
import os
import zlib
import hashlib
from typing import Optional, Tuple

MAGIC = b"STEGGY"          # 6 bytes magic
VERSION = b"\x02"          # version 2
HEADER_LEN = len(MAGIC) + 1 + 4  # magic + version + 4-byte length

def _derive_key(password: str) -> bytes:
    """Derive a 32-byte key from password using SHA256."""
    if password is None:
        password = ""
    return hashlib.sha256(password.encode("utf-8")).digest()

def _xor_data(data: bytes, key: bytes) -> bytes:
    """XOR data with repeating key."""
    if not key:
        return data
    out = bytearray(len(data))
    klen = len(key)
    for i, b in enumerate(data):
        out[i] = b ^ key[i % klen]
    return bytes(out)

def _bytes_to_bits(b: bytes) -> list:
    """Return list of '0'/'1' chars representing bits of byte array."""
    bits = []
    for byte in b:
        bits.extend([ (byte >> i) & 1 for i in reversed(range(8)) ])
    return bits

def _bits_to_bytes(bits: list) -> bytes:
    """Convert list of bits (0/1 ints) into bytes."""
    byts = bytearray()
    for i in range(0, len(bits), 8):
        chunk = bits[i:i+8]
        if len(chunk) < 8:
            break
        val = 0
        for bit in chunk:
            val = (val << 1) | (bit & 1)
        byts.append(val)
    return bytes(byts)

def capacity_bits_for_image(img) -> int:
    """Return total number of bits available (one bit per channel LSB)."""
    h, w, c = img.shape
    return h * w * c  # 3 channels usually -> three bits per pixel

def pack_payload(message: str, password: Optional[str]) -> bytes:
    """
    Compress and optionally encrypt the message, and return full header+payload bytes.
    Format: MAGIC + VERSION + payload_len(4 big-endian) + payload_bytes
    Payload is zlib-compressed message bytes optionally XORed by derived key.
    """
    msg_bytes = message.encode("utf-8")
    compressed = zlib.compress(msg_bytes)
    if password:
        key = _derive_key(password)
        compressed = _xor_data(compressed, key)
    payload_len = len(compressed).to_bytes(4, "big")
    return MAGIC + VERSION + payload_len + compressed

def unpack_payload(payload_bytes: bytes, password: Optional[str]) -> str:
    """Given payload_bytes (compressed +/- encrypted), return decoded utf-8 message."""
    if password:
        key = _derive_key(password)
        payload_bytes = _xor_data(payload_bytes, key)
    decompressed = zlib.decompress(payload_bytes)
    return decompressed.decode("utf-8")

def hide_text(input_path: str, message: str, password: Optional[str], output_path: Optional[str] = None) -> str:
    """
    Encode message into input_path image. Writes PNG to output_path (or current dir).
    Raises ValueError if message too large for image capacity.
    Returns output file path.
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError("Input image not found.")

    img = cv2.imread(input_path)
    if img is None:
        raise ValueError("Failed to read input image.")
    total_bits = capacity_bits_for_image(img)

    full_payload = pack_payload(message, password)
    bits = _bytes_to_bits(full_payload)
    needed = len(bits)
    if needed + 16 > total_bits:
        # leave small slack; raise a helpful error
        raise ValueError(f"Message too large to embed. Required bits: {needed}, available: {total_bits}")

    # write bits into LSB of image channels (row-major)
    h, w, c = img.shape
    bit_idx = 0
    for y in range(h):
        for x in range(w):
            for ch in range(c):
                if bit_idx >= needed:
                    break
                # set LSB to bits[bit_idx]
                img[y, x, ch] = (int(img[y, x, ch]) & ~1) | bits[bit_idx]
                bit_idx += 1
            if bit_idx >= needed:
                break
        if bit_idx >= needed:
            break

    # save output
    if output_path is None:
        base = os.path.basename(input_path)
        output_path = os.path.join(os.getcwd(), f"encrypted_v2_{base}")
    cv2.imwrite(output_path, img)
    return output_path

def extract_text(image_path: str, password: Optional[str]) -> Tuple[str, bool]:
    """
    Extract message from image_path. Returns (message, used_new_format_flag).
    Will try new embedded header format first; if not present, attempt legacy decoding fallback.
    Raises ValueError on wrong password or no message found.
    """
    if not os.path.isfile(image_path):
        raise FileNotFoundError("Image not found.")

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read image.")

    h, w, c = img.shape
    total_bits = h * w * c

    # read first HEADER_LEN bytes worth of bits to detect magic
    header_bits_needed = HEADER_LEN * 8
    header_bits = []
    bit_count = 0
    for y in range(h):
        for x in range(w):
            for ch in range(c):
                header_bits.append(int(img[y, x, ch]) & 1)
                bit_count += 1
                if bit_count >= header_bits_needed:
                    break
            if bit_count >= header_bits_needed:
                break
        if bit_count >= header_bits_needed:
            break
    header_bytes = _bits_to_bytes(header_bits)
    if header_bytes[:len(MAGIC)] == MAGIC and header_bytes[len(MAGIC)] == VERSION[0]:
        # parse length
        payload_len = int.from_bytes(header_bytes[len(MAGIC)+1:len(MAGIC)+1+4], "big")
        # compute how many bits total to read (payload only)
        payload_bits_needed = payload_len * 8
        # read remaining bits after header
        bits = []
        # skip header_bits_needed bits first
        skip = header_bits_needed
        idx = 0
        for y in range(h):
            for x in range(w):
                for ch in range(c):
                    if idx >= skip:
                        bits.append(int(img[y, x, ch]) & 1)
                        if len(bits) >= payload_bits_needed:
                            break
                    idx += 1
                if len(bits) >= payload_bits_needed:
                    break
            if len(bits) >= payload_bits_needed:
                break
        payload_bytes = _bits_to_bytes(bits)
        # attempt unpack
        try:
            message = unpack_payload(payload_bytes, password)
            return message, True
        except zlib.error as ze:
            raise ValueError("Failed to decompress payload. Possibly wrong password or corrupted data.") from ze
        except Exception as e:
            raise ValueError("Failed to decode payload.") from e
    else:
        # fallback: try legacy extraction (attempt to be compatible with your old code)
        # Old algorithm used per-character binary and stop bit marker (non structured). We'll implement a permissive fallback:
        bits = []
        stop = False
        for y in range(h):
            for x in range(w):
                pixel = img[y, x]
                # append LSB of each channel
                bits.extend([int(pixel[0]) & 1, int(pixel[1]) & 1, int(pixel[2]) & 1])
        # convert into bytes and then to chars until a null-like stop or we exhaust
        bytes_data = _bits_to_bytes(bits)
        # try to decode as ASCII until non-printable / garbage; return as legacy
        try:
            # remove trailing zeros
            decoded = bytes_data.rstrip(b'\x00').decode('utf-8', errors='ignore')
            if not decoded:
                raise ValueError("No legacy message found.")
            return decoded, False
        except Exception as e:
            raise ValueError("No embedded stego header found, and legacy decode failed.") from e
