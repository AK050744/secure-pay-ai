# utils/Facedetection.py - PRODUCTION VERSION
import base64
import numpy as np
import cv2
import os

def is_real_human(base64_image: str) -> bool:
    """
    Detects if a real human face is present in the image
    Returns True if face detected, False otherwise
    """
    try:
        if not base64_image:
            print("[ERROR] No image data provided")
            return False
            
        # Decode base64 image
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
            
        print(f"[INFO] Image decoded successfully. Shape: {img.shape}")
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Load the face cascade classifier with fallback options
        cascade_paths = [
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml',  # Default path
            './haarcascade_frontalface_default.xml',  # Local file
            'haarcascade_frontalface_default.xml',    # Current directory
        ]
        
        face_cascade = None
        for cascade_path in cascade_paths:
            if os.path.exists(cascade_path):
                face_cascade = cv2.CascadeClassifier(cascade_path)
                if not face_cascade.empty():
                    print(f"[INFO] Using cascade from: {cascade_path}")
                    break
        
        if face_cascade is None or face_cascade.empty():
            print("[ERROR] Could not load face cascade classifier")
            print("Try running the check script to download the cascade file")
            return False
        
        if face_cascade.empty():
            print("[ERROR] Failed to load face cascade classifier")
            return False
        
        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        face_count = len(faces)
        print(f"[INFO] Detected {face_count} face(s)")
        
        # Return True if at least one face is detected
        if face_count > 0:
            print("[INFO] Face detection: SUCCESS")
            return True
        else:
            print("[INFO] Face detection: NO FACES FOUND")
            return False
            
    except Exception as e:
        print(f"[ERROR] Face detection failed: {str(e)}")
        return False

def get_face_details(base64_image: str) -> dict:
    """
    Returns detailed information about detected faces
    """
    try:
        if not base64_image:
            return {"error": "No image data provided"}
            
        # Decode base64 image
        if ',' in base64_image:
            base64_data = base64_image.split(',')[-1]
        else:
            base64_data = base64_image
            
        img_data = base64.b64decode(base64_data)
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return {"error": "Failed to decode image"}
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Load face cascade
        face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(face_cascade_path)
        
        if face_cascade.empty():
            return {"error": "Failed to load face classifier"}
        
        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        return {
            "face_detected": len(faces) > 0,
            "face_count": len(faces),
            "faces": [{"x": int(x), "y": int(y), "width": int(w), "height": int(h)} 
                     for (x, y, w, h) in faces],
            "image_shape": img.shape
        }
        
    except Exception as e:
        return {"error": f"Face detection failed: {str(e)}"}