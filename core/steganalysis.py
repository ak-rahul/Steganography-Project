"""Steganalysis - Detect steganography in images"""

import cv2
import numpy as np
from scipy import stats


class Steganalysis:
    """Detect hidden messages in images"""
    
    @staticmethod
    def chi_square_test(image_path: str) -> dict:
        """Chi-square attack detection"""
        img = cv2.imread(image_path)
        flat = img.flatten()
        
        # Count frequency of pixel values
        observed = np.bincount(flat, minlength=256)
        expected = np.full(256, np.mean(observed))
        
        # Chi-square statistic
        chi_square = np.sum((observed - expected) ** 2 / (expected + 1e-10))
        normalized_score = chi_square / 255
        
        return {
            'score': normalized_score,
            'suspicious': normalized_score > 50,
            'message': '⚠️ SUSPICIOUS - Likely contains hidden data' if normalized_score > 50 else '✓ Clean'
        }
    
    @staticmethod
    def lsb_analysis(image_path: str) -> dict:
        """Analyze LSB bit patterns"""
        img = cv2.imread(image_path)
        lsb_layer = img & 1
        
        # Calculate randomness
        unique_patterns = len(np.unique(lsb_layer))
        total_pixels = lsb_layer.size
        randomness = (unique_patterns / total_pixels) * 100
        
        return {
            'randomness': randomness,
            'suspicious': randomness > 45,
            'message': '⚠️ SUSPICIOUS - High LSB randomness' if randomness > 45 else '✓ Normal LSB pattern'
        }
    
    @staticmethod
    def entropy_analysis(image_path: str) -> dict:
        """Calculate image entropy"""
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        hist = cv2.calcHist([img], [0], None, [256], [0, 256])
        hist = hist.flatten() / hist.sum()
        
        entropy = -np.sum(hist * np.log2(hist + 1e-10))
        
        # Normal images have entropy 7.3-7.9
        expected_range = (7.3, 7.9)
        suspicious = entropy < expected_range[0] or entropy > expected_range[1]
        
        return {
            'entropy': entropy,
            'expected': f"{expected_range[0]} - {expected_range[1]}",
            'suspicious': suspicious,
            'message': '⚠️ SUSPICIOUS - Abnormal entropy' if suspicious else '✓ Normal entropy'
        }
    
    @staticmethod
    def full_analysis(image_path: str) -> dict:
        """Perform complete steganalysis"""
        chi = Steganalysis.chi_square_test(image_path)
        lsb = Steganalysis.lsb_analysis(image_path)
        entropy = Steganalysis.entropy_analysis(image_path)
        
        suspicious_count = sum([chi['suspicious'], lsb['suspicious'], entropy['suspicious']])
        
        return {
            'chi_square': chi,
            'lsb': lsb,
            'entropy': entropy,
            'verdict': 'LIKELY CONTAINS HIDDEN DATA' if suspicious_count >= 2 else 'NO OBVIOUS STEGANOGRAPHY DETECTED',
            'confidence': (suspicious_count / 3) * 100
        }
