#!/usr/bin/env python3
"""
Simple test script to debug face detection issues
"""

import base64
import numpy as np
import cv2
import os

def test_opencv_installation():
    """Test if OpenCV is properly installed"""
    print("Testing OpenCV installation...")
    print(f"OpenCV version: {cv2.__version__}")
    
    # Test Haar cascade availability
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    print(f"Haar cascade path: {cascade_path}")
    print(f"Haar cascade exists: {os.path.exists(cascade_path)}")
    
    if os.path.exists(cascade_path):
        face_cascade = cv2.CascadeClassifier(cascade_path)
        print(f"Haar cascade loaded successfully: {not face_cascade.empty()}")
    
    return os.path.exists(cascade_path)

def create_test_face_detection():
    """Create a temporary face detection that always returns True for testing"""
    
    # Create utils directory if it doesn't exist
    os.makedirs('utils', exist_ok=True)
    
    test_content = '''# utils/Facedetection.py - TEST VERSION
import base64
import numpy as np
import cv2
import os

def is_real_human(base64_image: str) -> bool:
    """
    TEST VERSION - Always returns True for debugging
    """
    try:
        if not base64_image:
            print("[ERROR] No image data provided")
            return False
            
        # Just check if we can decode the image
        if ',' in base64_image:
            base64_data = base64_image.split(',')[-1]
        else:
            base64_data = base64_image
            
        img_data = base64.b64decode(base64_data)
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            print("[ERROR] Failed to decode image")
            return False
            
        print(f"[TEST] Image decoded successfully. Shape: {img.shape}")
        print("[TEST] Returning True for testing purposes")
        
        # For testing - always return True if image decodes
        return True
        
    except Exception as e:
        print(f"[ERROR] Test face detection failed: {str(e)}")
        return False
'''
    
    with open('utils/Facedetection.py', 'w') as f:
        f.write(test_content)
    
    print("Created test version of Facedetection.py")

if __name__ == "__main__":
    print("=== Face Detection Debug Tool ===")
    
    if not test_opencv_installation():
        print("\n❌ OpenCV Haar cascades not found!")
        print("Try installing opencv-contrib-python instead of opencv-python:")
        print("pip uninstall opencv-python")
        print("pip install opencv-contrib-python")
    else:
        print("\n✅ OpenCV installation looks good!")
    
    create_test = input("\nCreate test version that always returns True? (y/n): ")
    if create_test.lower() == 'y':
        create_test_face_detection()
        print("\n✅ Test version created. Restart your backend and try again.")
        print("This will help determine if the issue is with face detection or other parts.")