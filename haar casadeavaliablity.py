# check_haar_cascade.py
import cv2
import os

def check_haar_cascade():
    """Check if Haar cascade files are available"""
    
    print("Checking Haar cascade availability...")
    print(f"OpenCV Version: {cv2.__version__}")
    
    # Method 1: Check cv2.data path
    try:
        haar_path = cv2.data.haarcascades
        print(f"Haar cascades directory: {haar_path}")
        
        if os.path.exists(haar_path):
            print("✅ Haar cascades directory exists")
            
            # List all available cascade files
            files = os.listdir(haar_path)
            haar_files = [f for f in files if f.endswith('.xml')]
            
            print(f"Available cascade files ({len(haar_files)}):")
            for file in haar_files:
                print(f"  - {file}")
                
            # Check specifically for face detection file
            face_cascade_file = 'haarcascade_frontalface_default.xml'
            face_cascade_path = os.path.join(haar_path, face_cascade_file)
            
            if os.path.exists(face_cascade_path):
                print(f"✅ Face cascade file found: {face_cascade_path}")
                
                # Test loading the classifier
                face_cascade = cv2.CascadeClassifier(face_cascade_path)
                if not face_cascade.empty():
                    print("✅ Face cascade classifier loads successfully")
                    return face_cascade_path
                else:
                    print("❌ Face cascade classifier failed to load")
            else:
                print(f"❌ Face cascade file NOT found: {face_cascade_path}")
        else:
            print("❌ Haar cascades directory does not exist")
            
    except Exception as e:
        print(f"❌ Error checking cv2.data.haarcascades: {e}")
    
    # Method 2: Try alternative paths
    print("\nTrying alternative paths...")
    
    alternative_paths = [
        # Common installation paths
        "/usr/share/opencv4/haarcascades/",
        "/usr/local/share/opencv4/haarcascades/",
        "/opt/homebrew/share/opencv4/haarcascades/",  # macOS Homebrew
        "C:\\opencv\\build\\etc\\haarcascades\\",      # Windows
        # Python package paths
        f"{cv2.__path__[0]}/data/",
    ]
    
    for alt_path in alternative_paths:
        face_file = os.path.join(alt_path, 'haarcascade_frontalface_default.xml')
        if os.path.exists(face_file):
            print(f"✅ Found alternative path: {face_file}")
            return face_file
    
    print("❌ No Haar cascade files found in alternative paths")
    return None

def download_haar_cascade():
    """Download Haar cascade file if not available"""
    import urllib.request
    
    print("\nDownloading Haar cascade file...")
    
    url = "https://raw.githubusercontent.com/opencv/opencv/4.x/data/haarcascades/haarcascade_frontalface_default.xml"
    local_filename = "haarcascade_frontalface_default.xml"
    
    try:
        urllib.request.urlretrieve(url, local_filename)
        print(f"✅ Downloaded: {local_filename}")
        print(f"File saved to: {os.path.abspath(local_filename)}")
        return os.path.abspath(local_filename)
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return None

def test_face_detection(cascade_path):
    """Test the face detection with a simple example"""
    print(f"\nTesting face detection with: {cascade_path}")
    
    try:
        face_cascade = cv2.CascadeClassifier(cascade_path)
        
        if face_cascade.empty():
            print("❌ Classifier is empty")
            return False
            
        # Create a simple test image (just for testing the classifier)
        import numpy as np
        test_img = np.zeros((200, 200, 3), dtype=np.uint8)
        gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
        
        # This should return empty array for blank image
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        print(f"✅ Face detection test successful. Detected {len(faces)} faces in blank image (should be 0)")
        return True
        
    except Exception as e:
        print(f"❌ Face detection test failed: {e}")
        return False

if __name__ == "__main__":
    cascade_path = check_haar_cascade()
    
    if cascade_path:
        test_face_detection(cascade_path)
    else:
        print("\n🔄 Attempting to download Haar cascade file...")
        downloaded_path = download_haar_cascade()
        if downloaded_path:
            test_face_detection(downloaded_path)
        else:
            print("\n❌ Could not obtain Haar cascade file")
            print("\n💡 Solutions:")
            print("1. Reinstall OpenCV: pip uninstall opencv-python && pip install opencv-python")
            print("2. Install opencv-contrib-python: pip install opencv-contrib-python")
            print("3. Download manually from: https://github.com/opencv/opencv/tree/4.x/data/haarcascades")