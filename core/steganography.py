"""Core steganography module using LSB technique"""

import cv2
import numpy as np
from PIL import Image
import json


class Steganography:
    """LSB Steganography with enhanced features"""
    
    @staticmethod
    def encode_message(image_path: str, message: str, output_path: str) -> dict:
        """
        Encode message into image using LSB steganography
        
        Args:
            image_path: Path to cover image
            message: Message to hide
            output_path: Path to save encoded image
            
        Returns:
            Dictionary with encoding statistics
        """
        try:
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Could not read image")
            
            # Add delimiter to mark end of message
            message = message + "<<<END>>>"
            
            # Convert message to binary
            binary_message = ''.join(format(ord(char), '08b') for char in message)
            message_length = len(binary_message)
            
            # Check capacity
            max_bytes = img.shape[0] * img.shape[1] * 3
            if message_length > max_bytes:
                raise ValueError(f"Message too large. Max {max_bytes // 8} characters")
            
            # Encode message
            data_index = 0
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    for k in range(3):  # RGB channels
                        if data_index < message_length:
                            # Modify LSB
                            img[i, j, k] = (img[i, j, k] & 0xFE) | int(binary_message[data_index])
                            data_index += 1
                        else:
                            break
                    if data_index >= message_length:
                        break
                if data_index >= message_length:
                    break
            
            # Save encoded image
            cv2.imwrite(output_path, img, [cv2.IMWRITE_PNG_COMPRESSION, 0])
            
            return {
                'success': True,
                'message_length': len(message) - 9,  # Exclude delimiter
                'image_size': img.shape,
                'capacity_used': (message_length / max_bytes) * 100
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def decode_message(image_path: str) -> dict:
        """
        Decode message from image
        
        Args:
            image_path: Path to encoded image
            
        Returns:
            Dictionary with decoded message or error
        """
        try:
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Could not read image")
            
            # Extract binary data
            binary_data = ""
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    for k in range(3):
                        binary_data += str(img[i, j, k] & 1)
            
            # Convert binary to text
            message = ""
            for i in range(0, len(binary_data), 8):
                byte = binary_data[i:i+8]
                if len(byte) == 8:
                    char = chr(int(byte, 2))
                    message += char
                    
                    # Check for delimiter
                    if message.endswith("<<<END>>>"):
                        message = message[:-9]  # Remove delimiter
                        return {
                            'success': True,
                            'message': message,
                            'length': len(message)
                        }
            
            raise ValueError("No valid message found or image not encoded")
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_image_capacity(image_path: str) -> dict:
        """Calculate maximum message capacity of image"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Could not read image")
            
            max_bits = img.shape[0] * img.shape[1] * 3
            max_chars = max_bits // 8 - 9  # Account for delimiter
            
            return {
                'success': True,
                'max_characters': max_chars,
                'image_dimensions': f"{img.shape[1]}x{img.shape[0]}"
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
