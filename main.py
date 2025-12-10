from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
import joblib
import pandas as pd
import os
from typing import Optional

app = FastAPI(title="PacketWatch API", version="1.0.0")

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Load trained pipeline model
try:
    model = joblib.load("intrusion_model.pkl")
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None


# Define request schema with validation
class SessionData(BaseModel):
    session_id: str = Field(..., min_length=1, description="Unique session identifier")
    network_packet_size: int = Field(..., ge=0, le=65535, description="Network packet size in bytes")
    protocol_type: str = Field(..., description="Protocol type (TCP, UDP, ICMP, HTTPS)")
    login_attempts: int = Field(..., ge=0, description="Number of login attempts")
    session_duration: float = Field(..., ge=0, description="Session duration in seconds")
    encryption_used: Optional[str] = Field(None, description="Encryption type (AES, DES, SSL/TLS)")
    ip_reputation_score: float = Field(..., ge=0, le=100, description="IP reputation score")
    failed_logins: int = Field(..., ge=0, description="Number of failed logins")
    browser_type: str = Field(..., description="Browser type")
    unusual_time_access: int = Field(..., ge=0, le=1, description="Unusual time access flag (0 or 1)")

    @validator('protocol_type')
    def validate_protocol(cls, v):
        valid_protocols = ['TCP', 'UDP', 'ICMP', 'HTTPS']
        if v not in valid_protocols:
            raise ValueError(f'Protocol must be one of {valid_protocols}')
        return v

    @validator('browser_type')
    def validate_browser(cls, v):
        valid_browsers = ['Chrome', 'Firefox', 'Safari', 'Edge', 'Other']
        if v not in valid_browsers:
            raise ValueError(f'Browser must be one of {valid_browsers}')
        return v

    @validator('encryption_used')
    def validate_encryption(cls, v):
        if v is not None and v != "":
            valid_encryptions = ['AES', 'DES', 'SSL/TLS']
            if v not in valid_encryptions:
                raise ValueError(f'Encryption must be one of {valid_encryptions}')
        return v

    class Config:
        schema_extra = {
            "example": {
                "session_id": "sess_12345",
                "network_packet_size": 512,
                "protocol_type": "TCP",
                "login_attempts": 3,
                "session_duration": 120.5,
                "encryption_used": "AES",
                "ip_reputation_score": 75.5,
                "failed_logins": 2,
                "browser_type": "Chrome",
                "unusual_time_access": 0
            }
        }


@app.get("/")
def root():
    """Serve the main UI page"""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Welcome to PacketWatch API", "docs": "/docs"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "version": "1.0.0"
    }


@app.post("/predict")
def predict(data: SessionData):
    """
    Predict if a network session is an attack or normal traffic
    
    Returns:
        dict: Contains session_id and attack_detected (0 = normal, 1 = attack)
    """
    
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please ensure intrusion_model.pkl exists."
        )
    
    try:
        # Convert input to DataFrame for scikit-learn pipeline
        df = pd.DataFrame([{
            "network_packet_size": data.network_packet_size,
            "protocol_type": data.protocol_type,
            "login_attempts": data.login_attempts,
            "session_duration": data.session_duration,
            "encryption_used": data.encryption_used if data.encryption_used else None,
            "ip_reputation_score": data.ip_reputation_score,
            "failed_logins": data.failed_logins,
            "browser_type": data.browser_type,
            "unusual_time_access": data.unusual_time_access
        }])
        
        print(f"📊 Processing prediction for session: {data.session_id}")
        print(f"   Data shape: {df.shape}")
        print(f"   Features: {df.columns.tolist()}")
        
        # Make prediction
        prediction = model.predict(df)[0]
        prediction_int = int(prediction)
        
        print(f"✅ Prediction result: {prediction_int} ({'ATTACK' if prediction_int == 1 else 'NORMAL'})")
        
        return {
            "session_id": data.session_id,
            "attack_detected": prediction_int
        }
        
    except Exception as e:
        print(f"❌ Prediction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting PacketWatch API server...")
    print(f"📁 Static directory: {static_dir}")
    print(f"🔧 Model loaded: {model is not None}")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)