# detector.py
import joblib
import pandas as pd
import numpy as np
import os

class IDSDetector:
    def __init__(self, models_root='data/trained_models/'):
        self.models_root = models_root
        self.l3_root = os.path.join(models_root, 'level3/')
        
        # Load Level 1 (Binary)
        self.model_l1 = joblib.load(os.path.join(models_root, 'model_lvl1_binary.joblib'))
        self.scaler_l1 = joblib.load(os.path.join(models_root, 'scaler_lvl1.joblib'))
        
        # Load Level 2 (Multiclass Family)
        self.model_l2 = joblib.load(os.path.join(models_root, 'model_lvl2_multiclass.joblib'))
        self.scaler_l2 = joblib.load(os.path.join(models_root, 'scaler_lvl2.joblib'))
        self.le_l2_secondary = joblib.load(os.path.join(models_root, 'label_encoder_lvl2_final.joblib'))
        self.le_l2_primary = joblib.load('data/processed/label_encoder_lvl2.joblib')
        
        # Load Level 3 Experts (Lazy loading can be done, but we load them now for simplicity)
        self.experts = {
            'DoS': {
                'model': joblib.load(os.path.join(self.l3_root, 'model_lvl3_dos_svm.joblib')),
                'scaler': joblib.load(os.path.join(self.l3_root, 'scaler_lvl3_dos_svm.joblib')),
                'le': joblib.load(os.path.join(self.l3_root, 'le_lvl3_dos_svm.joblib'))
            },
            'BruteForce': {
                'model': joblib.load(os.path.join(self.l3_root, 'model_lvl3_bruteforce.joblib')),
                'scaler': joblib.load(os.path.join(self.l3_root, 'scaler_lvl3_bruteforce.joblib')),
                'le': joblib.load(os.path.join(self.l3_root, 'le_lvl3_bruteforce.joblib'))
            },
            'WebAttack': {
                'model': joblib.load(os.path.join(self.l3_root, 'model_lvl3_webattack.joblib')),
                'scaler': joblib.load(os.path.join(self.l3_root, 'scaler_lvl3_webattack.joblib')),
                'le': joblib.load(os.path.join(self.l3_root, 'le_lvl3_webattack.joblib'))
            },
            'RareAttack': {
                'model': joblib.load(os.path.join(self.l3_root, 'model_lvl3_rare.joblib')),
                'scaler': joblib.load(os.path.join(self.l3_root, 'scaler_lvl3_rare.joblib')),
                'le': joblib.load(os.path.join(self.l3_root, 'le_lvl3_rare.joblib'))
            }
        }
        
        # Features removed for anti-overfitting in L3 (must be removed from raw input before scaling/predicting in L3)
        self.l3_drop_cols = ['Destination Port', 'Init_Win_bytes_forward', 'Init_Win_bytes_backward']

    def detect(self, input_data):
        """
        input_data: pd.DataFrame with raw features (unscaled)
        returns: dict with results at each level
        """
        results = {
            'Level1': 'Pending',
            'Level2': 'None',
            'Level3': 'None',
            'Status': 'Safe'
        }
        
        # 1. Level 1 - Binary Detection
        X_l1 = self.scaler_l1.transform(input_data)
        is_attack = self.model_l1.predict(X_l1)[0]
        
        if is_attack == 0:
            results['Level1'] = 'BENIGN'
            return results
        
        results['Level1'] = 'ATTACK'
        results['Status'] = 'Danger'
        
        # 2. Level 2 - Family Detection
        X_l2 = self.scaler_l2.transform(input_data)
        family_idx = self.model_l2.predict(X_l2)[0]
        # Two-step decoding: model output -> intermediate ID -> string name
        family_id = self.le_l2_secondary.inverse_transform([family_idx])[0]
        family_name = self.le_l2_primary.inverse_transform([family_id])[0]
        results['Level2'] = family_name
        
        # 3. Level 3 - Expert Specialization
        if family_name in self.experts:
            expert = self.experts[family_name]
            
            # Prepare L3 data (drop identity cols)
            X_l3_raw = input_data.drop(columns=[col for col in self.l3_drop_cols if col in input_data.columns])
            
            X_l3 = expert['scaler'].transform(X_l3_raw)
            label_idx = expert['model'].predict(X_l3)[0]
            label_name = expert['le'].inverse_transform([label_idx])[0]
            results['Level3'] = label_name
        else:
            # No expert for this family, display family name as Level 3
            results['Level3'] = f"{family_name}"
            
        return results

if __name__ == "__main__":
    # Test simple init
    print("Testing detector initialization...")
    try:
        detector = IDSDetector()
        print("Detector initialized successfully.")
    except Exception as e:
        print(f"Error during initialization: {e}")
