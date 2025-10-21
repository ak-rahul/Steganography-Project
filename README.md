# 🔐 Steganography-Project

![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20|%20Linux%20|%20macOS-lightgrey.svg)


**Advanced Image Steganography Tool with Windows 11 Fluent Design**

Hide secret messages inside images with military-grade encryption

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Troubleshooting](#-troubleshooting)


---

## 📖 Overview

**Steganography-Project** is a modern, feature-rich desktop application for hiding secret messages inside images using advanced steganographic techniques. Built with Python and PyQt6, it features a beautiful Windows 11 Fluent Design interface and implements multiple steganography algorithms with AES-256 encryption for maximum security.

### What is Steganography?

Steganography is the practice of concealing information within another file, message, or image. Unlike encryption, which makes data unreadable, steganography hides the existence of the data itself, making it perfect for covert communication.

---

## ✨ Features

### 🔒 **Encryption & Security**
- **Multiple Steganography Algorithms**
  - LSB (Least Significant Bit) - Standard, fast and efficient
  - PVD (Pixel Value Differencing) - Advanced, more secure against detection
  - LSB-Match - Histogram-preserving, resistant to Chi-square attacks
- **AES-256 Encryption** with PBKDF2 key derivation (100,000 iterations)
- **Password Strength Meter** with real-time feedback
- **Secure Password Hashing** with random salt generation

### 🔍 **Advanced Analysis**
- **Built-in Steganalysis Detection**
  - Chi-Square Attack Detection
  - LSB Bit Pattern Analysis
  - Entropy Analysis
  - Confidence scoring system
- **PSNR Quality Metrics** to measure image degradation
- **Image Capacity Calculator** to check maximum message size

### 📦 **Batch Processing**
- Process multiple images simultaneously
- Multi-threaded background processing
- Progress tracking with status updates
- Same message and password for all files

### 🎨 **Modern UI/UX**
- **Windows 11 Fluent Design** aesthetic
- Sidebar navigation with 4 main sections
- Rounded corners, proper shadows, and spacing
- Responsive layout with smooth transitions
- Dark-themed cards and surfaces
- Real-time character counter
- Drag-and-drop support (planned)

### 💾 **File Management**
- Support for PNG, JPEG, BMP formats
- Auto-save encrypted images
- Export decrypted messages to text files
- Copy to clipboard functionality
- Organized output directory structure

---

## 🚀 Installation

### Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package manager)
- **Windows 10/11, Linux, or macOS**

### Quick Install

#### Clone the repository
```
git clone https://github.com/ak-rahul/Steganography-Project.git
cd Steganography-Project
```

#### Install dependencies
```
pip install -r requirements.txt
```

#### Run the application
```
python main.py
```

### Dependencies

- PyQt6==6.6.1
- opencv-python==4.8.1.78
- Pillow==10.1.0
- numpy==1.24.3
- cryptography==41.0.7
- scipy==1.11.4

### Manual Installation
```
pip install PyQt6 opencv-python Pillow numpy cryptography scipy
```

---

## 📂 Project Structure
```
Steganography-Project/
│
├── main.py 
├── config.py 
├── requirements.txt
├── README.md
├── LICENSE.md
│
├── core/ # Core functionality
│ ├── init.py
│ ├── steganography.py 
│ ├── encryption.py 
│ └── steganalysis.py 
│
├── gui/ # User interface
│ ├── init.py
│ ├── main_window.py 
│ ├── encrypt_widget.py 
│ ├── decrypt_widget.py 
│ ├── analysis_widget.py 
│ ├── batch_widget.py 
│ └── styles.py 
│
└── encrypted_images/ # Output directory (auto-created)
```

---

## 🎯 Usage

### 1. Encrypting a Message

1. **Launch the application**: `python main.py`
2. **Navigate to "Encrypt Message"** (default tab)
3. **Select Algorithm**: Choose LSB, PVD, or LSB-Match
4. **Browse Image**: Click "📁 Browse Image" and select your cover image
5. **Enter Password**: Type a strong password (minimum 4 characters)
6. **Type Message**: Enter your secret message in the text area
7. **Click "✓ Encrypt & Save"**: Your encrypted image will be saved to `encrypted_images/`

### 2. Decrypting a Message

1. **Navigate to "Decrypt Message"** tab
2. **Browse Encrypted Image**: Select the image containing hidden data
3. **Enter Password**: Type the correct decryption password
4. **Click "🔓 Decrypt Message"**: View the hidden message
5. **Copy or Save**: Use "📋 Copy" or "💾 Save to File" buttons

### 3. Analyzing Suspicious Images

1. **Navigate to "Steganalysis"** tab
2. **Browse Image**: Select any image to analyze
3. **Click "🔍 Run Full Analysis"**: View detailed detection report
4. **Review Results**: Check confidence score and verdict

### 4. Batch Processing

1. **Navigate to "Batch Processing"** tab
2. **Add Images**: Click "📁 Add Images" and select multiple files
3. **Configure Settings**: Choose algorithm, password, and message
4. **Click "⚡ Process All Images"**: Watch progress in real-time
5. **Check Output**: Find all encrypted images in `encrypted_images/`

---

---

## 💡 Tips & Best Practices

### For Maximum Security:
- ✅ Use **PNG format** (lossless compression)
- ✅ Choose **PVD or LSB-Match** algorithms
- ✅ Use **strong passwords** (12+ chars, mixed case, symbols)
- ✅ Use **large cover images** for better stealth
- ✅ Test decryption immediately after encryption
- ❌ Avoid JPEG for encrypted images (lossy compression destroys data)
- ❌ Don't reuse the same cover image multiple times

### Password Strength Guidelines:
- **Weak**: < 8 characters
- **Fair**: 8-11 characters, mixed case
- **Good**: 12+ characters, mixed case + numbers
- **Strong**: 12+ characters, mixed case + numbers + symbols

---

## 🐛 Troubleshooting

### Issue: "No module named 'PyQt6'"
**Solution**: Install PyQt6: `pip install PyQt6`

### Issue: "Could not read image"
**Solution**: 
- Ensure image file is not corrupted
- Use supported formats (PNG, JPEG, BMP)
- Check file permissions

### Issue: "Message too large"
**Solution**: 
- Use a larger cover image
- Shorten your message
- Check capacity with info display

### Issue: "Incorrect password or corrupted data"
**Solution**: 
- Verify password is correct (case-sensitive)
- Ensure image hasn't been modified/compressed
- Check if image was encrypted with this tool

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE.md) file for details.