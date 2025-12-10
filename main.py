from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# Load trained pipeline model
model = joblib.load("intrusion_model.pkl")

# Define request schema
class SessionData(BaseModel):
    session_id: str
    network_packet_size: int
    protocol_type: str
    login_attempts: int
    session_duration: float
    encryption_used: str = None # type: ignore
    ip_reputation_score: float
    failed_logins: int
    browser_type: str
    unusual_time_access: int

@app.post("/predict")
def predict(data: SessionData):
    # Convert input to a DataFrame (needed for scikit-learn pipeline)
    df = pd.DataFrame([{
        "network_packet_size": data.network_packet_size,
        "protocol_type": data.protocol_type,
        "login_attempts": data.login_attempts,
        "session_duration": data.session_duration,
        "encryption_used": data.encryption_used,
        "ip_reputation_score": data.ip_reputation_score,
        "failed_logins": data.failed_logins,
        "browser_type": data.browser_type,
        "unusual_time_access": data.unusual_time_access
    }])

    # Make prediction
    prediction = model.predict(df)[0]

    return {"session_id": data.session_id, "attack_detected": int(prediction)}
