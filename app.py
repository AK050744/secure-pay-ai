from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils.Facedetection import is_real_human
from fraud_model import calculate_fraud_score
import uvicorn
import cv2

app = FastAPI()

# Add CORS middleware to handle frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=False,  # Set to False when using allow_origins=["*"]
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.post("/verify_transaction/")
async def verify_transaction(request: Request):
    try:
        data = await request.json()
        
        # Validate required fields
        required_fields = ["device_id", "location", "purchase_amount", "account_age_days", "category", "session_duration"]
        for field in required_fields:
            if field not in data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")

        # Check for face image
        if not data.get("face_image"):
            return {
                "status": "blocked",
                "score": "N/A",
                "message": "Face image is required for verification"
            }
        
        if not is_real_human(data["face_image"]):
            return {
                "status": "blocked",
                "score": "N/A",
                "message": "No human face detected"
            }

        # Calculate fraud score with proper data structure
        fraud_data = {
            "device_id_known": data.get("device_id_known", False),
            "location_change": data.get("location_change", False),
            "amount_usd": float(data["purchase_amount"]),
            "purchase_hour": data.get("purchase_hour", 12),
            "is_new_account": int(data["account_age_days"]) < 30,
            "is_sale_event": data.get("is_sale_event", False)
        }
        
        score = calculate_fraud_score(fraud_data)

        # Determine transaction status
        if score > 80:
            return {"status": "blocked", "score": score, "message": "High risk transaction blocked"}
        elif score > 50:
            return {"status": "challenge", "score": score, "message": "Transaction requires additional verification"}
        else:
            return {"status": "approved", "score": score, "message": "Transaction approved"}
            
    except Exception as e:
        return {
            "status": "error",
            "score": "N/A",
            "message": f"Error processing transaction: {str(e)}"
        }

@app.post("/debug_face/")
async def debug_face(request: Request):
    """Debug endpoint to test face detection separately"""
    try:
        data = await request.json()
        
        if not data.get("face_image"):
            return {"error": "No face image provided"}
        
        # Test face detection
        result = is_real_human(data["face_image"])
        
        return {
            "face_detected": result,
            "image_data_length": len(data["face_image"]),
            "has_data_prefix": "data:" in data["face_image"],
            "opencv_version": cv2.__version__ if 'cv2' in globals() else "Not imported"
        }
        
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def root():
    return {"message": "Secure Pay AI - Transaction Risk API"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)