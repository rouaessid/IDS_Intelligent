import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import numpy as np
import time

# Add src to path to import detector
sys.path.append(os.path.join(os.getcwd(), 'src'))
from detector import IDSDetector

app = FastAPI(title="IDS Next.js API")

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False, # Must be False if origins is ["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Detector
try:
    detector = IDSDetector(models_root='data/trained_models/')
    print("Detector loaded successfully")
except Exception as e:
    print(f"Error loading models: {e}")
    detector = None

# Global simulation data cache
X_sim = None
try:
    X_sim = joblib.load('data/processed/X_unscaled.joblib')
    print("Simulation data loaded")
except Exception as e:
    print(f"Simulation data not found: {e}")

# Global stats tracker
stats = {
    "total_flows": 0,
    "benign_flows": 0,
    "attack_flows": 0,
    "alerts": []
}

class IndexRequest(BaseModel):
    index: int

@app.get("/api/stats")
async def get_stats():
    return {
        "threats": stats["attack_flows"],
        "safe": stats["benign_flows"],
        "total": stats["total_flows"],
        "avgResponse": "5ms"
    }

@app.post("/api/detect-by-index")
async def detect_by_index(req: IndexRequest):
    if detector is None or X_sim is None:
        raise HTTPException(status_code=500, detail="Models or data not loaded")
    
    try:
        if req.index < 0 or req.index >= len(X_sim):
            raise HTTPException(status_code=400, detail="Index out of range")
        
        sample = X_sim.iloc[[req.index]]
        res = detector.detect(sample)
        
        return {
            "result": res,
            "dataset_size": len(X_sim)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/simulate")
async def simulate(num_flows: dict = None):
    if detector is None or X_sim is None:
        raise HTTPException(status_code=500, detail="Models or data not loaded")
    
    n = num_flows.get("num_flows", 50) if num_flows else 50
    
    current_results = []
    current_alerts = []
    
    # Pick random samples and detect
    indices = np.random.randint(0, len(X_sim), n)
    for idx in indices:
        sample = X_sim.iloc[[idx]]
        res = detector.detect(sample)
        
        stats["total_flows"] += 1
        if res['Status'] == 'Danger':
            stats["attack_flows"] += 1
            alert = {
                "index": int(idx),
                "family": res['Level2'],
                "type": res['Level3'],
                "severity": "high"
            }
            stats["alerts"].insert(0, alert)
            current_alerts.append(alert)
        else:
            stats["benign_flows"] += 1
            
        current_results.append(res)
    
    # Keep only last 50 alerts
    stats["alerts"] = stats["alerts"][:50]
    
    return {
        "total_flows": stats["total_flows"],
        "benign_flows": stats["benign_flows"],
        "attack_flows": stats["attack_flows"],
        "alerts": current_alerts, # Alerts from this batch
        "results": current_results
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
