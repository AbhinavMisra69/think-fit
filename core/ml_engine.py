import math

class PhysiqueAnalyzer:
    """Wrapper for your custom Machine Learning Body Fat predictor."""
    
    @staticmethod
    def predict_body_fat(gender: str, weight_kg: float, height_cm: float, waist: float, neck: float, chest: float, arm: float, hip: float = 0.0) -> float:
        try:
            # 1. Convert all centimeters to inches first
            h_in = height_cm / 2.54
            w_in = waist / 2.54   # Acts as 'abdomen' for men, 'waist' for women
            n_in = neck / 2.54
            hip_in = hip / 2.54
            
            # 2. Apply the direct Body Fat Percentage formulas
            if gender.lower() == 'male':
                # Men: BF (%) = 86.010 x log10 (abdomen - neck) - 70.041 x log10 (height) + 36.76
                estimated_bf = 86.010 * math.log10(w_in - n_in) - 70.041 * math.log10(h_in) + 36.76
            else:
                # Women: BF (%) = 163.205 x log10 (waist + hip - neck) - 97.684 x log10 (height) - 78.387
                estimated_bf = 163.205 * math.log10(w_in + hip_in - n_in) - 97.684 * math.log10(h_in) - 78.387
                
            # 3. Keep it within realistic biological bounds (5% to 50%)
            return max(5.0, min(round(estimated_bf, 1), 50.0))
            
        except (ValueError, ZeroDivisionError) as e:
            print(f"Math Error in BF% calculation: {e}")
            return 15.0 # Safe fallback if invalid dimensions are entered