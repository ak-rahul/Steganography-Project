# Steganography v2 (PyQt6)

---

Features:
- Embeds compressed payload into image LSBs.
- Optional password (SHA256-derived XOR) for payload.
- Embedded header: allows self-contained decrypt without in-memory maps.
- Fallback attempt for legacy images (best-effort).
- Persistent metadata (files.json).
- Capacity checks and friendly UI.

Run:
1. pip install -r requirements.txt
2. python main.py

Notes:
- Use PNG for lossless storage. JPEG may destroy LSBs (avoid for encrypted images).
- If you encrypted with the older Tkinter app, use "Decrypt" and select that file; app will try legacy fallback.
