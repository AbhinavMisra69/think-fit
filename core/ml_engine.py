# core/ml_engine.py

class PhysiqueAnalyzer:
    """Wrapper for your custom Machine Learning Body Fat predictor."""
    
    @staticmethod
    def predict_body_fat(weight_kg: float, height_cm: float, waist: float, chest: float, arm: float, thigh: float) -> float:
        # TODO: Import and run your actual .h5 / .onnx / sklearn ML model here.
        # For now, we simulate the ML output so the pipeline works.
        
        # Simulated ML logic based on proportions
        estimated_bf = (waist * 0.4) + (thigh * 0.2) - (arm * 0.1) - (chest * 0.1)
        
        # Keep it within realistic biological bounds
        return max(5.0, min(round(estimated_bf, 1), 45.0))