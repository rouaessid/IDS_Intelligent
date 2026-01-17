# Backend API for IDS detector
# Place your detector.py in the same directory or adjust the import path
from detector import IDSDetector
import pandas as pd
import json

class IDSAPI:
    def __init__(self):
        self.detector = IDSDetector()
    
    def analyze(self, data):
        """Analyze network data and return threat classification"""
        try:
            df = pd.DataFrame(data)
            results = self.detector.detect(df)
            return results
        except Exception as e:
            return {'error': str(e)}

# Flask/FastAPI wrapper can be added to expose this as HTTP endpoint
