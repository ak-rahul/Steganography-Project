"""Core steganography module"""

import cv2
import numpy as np
import random


class Steganography:
    """LSB Steganography with multiple algorithms"""
    
    @staticmethod
    def encode_message(image_path: str, message: str, output_path: str, method='LSB') -> dict:
        """Encode message into image"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Could not read image")
            
            message = message + "<<<END>>>"
            binary_message = ''.join(format(ord(char), '08b') for char in message)
            message_length = len(binary_message)
            
            max_bytes = img.shape[0] * img.shape[1] * 3
            if message_length > max_bytes:
                raise ValueError(f"Message too large. Max {max_bytes // 8} characters")
            
            if method == 'LSB':
                img = Steganography._encode_lsb(img, binary_message)
            elif method == 'LSB_MATCH':
                img = Steganography._encode_lsb_match(img, binary_message)
            elif method == 'PVD':
                img = Steganography._encode_pvd(img, binary_message)
            
            cv2.imwrite(output_path, img, [cv2.IMWRITE_PNG_COMPRESSION, 0])
            
            return {
                'success': True,
                'message_length': len(message) - 9,
                'image_size': img.shape,
                'capacity_used': (message_length / max_bytes) * 100,
                'method': method
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def _encode_lsb(img, binary_message):
        """Standard LSB encoding"""
        data_index = 0
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                for k in range(3):
                    if data_index < len(binary_message):
                        img[i, j, k] = (img[i, j, k] & 0xFE) | int(binary_message[data_index])
                        data_index += 1
                    else:
                        return img
        return img
    
    @staticmethod
    def _encode_lsb_match(img, binary_message):
        """LSB Matching"""
        data_index = 0
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                for k in range(3):
                    if data_index < len(binary_message):
                        pixel_val = int(img[i, j, k])
                        bit = int(binary_message[data_index])
                        
                        if pixel_val % 2 != bit:
                            change = random.choice([-1, 1])
                            new_val = max(0, min(255, pixel_val + change))
                            img[i, j, k] = new_val
                        
                        data_index += 1
                    else:
                        return img
        return img
    
    @staticmethod
    def _encode_pvd(img, binary_message):
        """Pixel Value Differencing"""
        data_index = 0
        for i in range(0, img.shape[0] - 1, 2):
            for j in range(0, img.shape[1] - 1, 2):
                if data_index >= len(binary_message):
                    return img
                
                diff = abs(int(img[i, j, 0]) - int(img[i+1, j, 0]))
                
                if diff >= 8:
                    bits_to_embed = min(3, len(binary_message) - data_index)
                    embed_value = int(binary_message[data_index:data_index+bits_to_embed], 2)
                    img[i, j, 0] = (img[i, j, 0] & 0xF8) | embed_value
                    data_index += bits_to_embed
        return img
    
    @staticmethod
    def decode_message(image_path: str) -> dict:
        """Decode message from image"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Could not read image")
            
            binary_data = ""
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    for k in range(3):
                        binary_data += str(img[i, j, k] & 1)
            
            message = ""
            for i in range(0, len(binary_data), 8):
                byte = binary_data[i:i+8]
                if len(byte) == 8:
                    char = chr(int(byte, 2))
                    message += char
                    
                    if message.endswith("<<<END>>>"):
                        message = message[:-9]
                        return {
                            'success': True,
                            'message': message,
                            'length': len(message)
                        }
            
            raise ValueError("No valid message found")
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_image_capacity(image_path: str) -> dict:
        """Calculate maximum message capacity"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Could not read image")
            
            max_bits = img.shape[0] * img.shape[1] * 3
            max_chars = max_bits // 8 - 9
            
            return {
                'success': True,
                'max_characters': max_chars,
                'image_dimensions': f"{img.shape[1]}x{img.shape[0]}",
                'file_size': f"{img.nbytes / 1024:.2f} KB"
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def calculate_psnr(original_path: str, stego_path: str) -> float:
        """Calculate Peak Signal-to-Noise Ratio"""
        original = cv2.imread(original_path)
        stego = cv2.imread(stego_path)
        
        mse = np.mean((original - stego) ** 2)
        if mse == 0:
            return float('inf')
        
        psnr = 20 * np.log10(255.0 / np.sqrt(mse))
        return psnr
