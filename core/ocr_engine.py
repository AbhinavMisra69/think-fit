import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
import re
from rapidfuzz import fuzz

class PackagedFoodEngine:
    @staticmethod
    def preprocess_image(image_path):
        img = cv2.imread(image_path)
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Slightly lighter denoising to preserve thin fonts
        gray = cv2.bilateralFilter(gray, 9, 15, 15) 
        
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        return thresh

    @staticmethod
    def normalize_text(text):
        text = text.lower()
        text = re.sub(r'(\d)([a-z])', r'\1 \2', text)
        text = re.sub(r'([a-z])(\d)', r'\1 \2', text)
        text = re.sub(r'(\d)(g|mg|kcal)', r'\1 \2', text)
        text = re.sub(r'[^a-z0-9.\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        replacements = {
            "carbohydrates": "carbs", "carbohydrate": "carbs",
            "proteins": "protein", "sugars": "sugar",
            "energy": "calories", "kcal": "calories"
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        return text.strip()

    # DROPPED THRESHOLD TO 70
    @staticmethod
    def match_keyword_sequence(words, i, phrase, threshold=70): 
        phrase_words = phrase.split()
        if i + len(phrase_words) > len(words): return False 
        extracted = " ".join(words[i:i+len(phrase_words)])
        return fuzz.ratio(extracted, phrase) >= threshold

    @classmethod
    def extract_nutrition(cls, text):
        nutrition = {}
        words = text.split()
        
        keywords = {
            "sat_fat": ["saturated fat", "sat fat"],
            "calories": ["calories"],
            "protein": ["protein", "protien", "pro tein"], 
            "carbs": ["carbs"],
            "sugar": ["sugar"]
        }

        for i in range(len(words)):
            for key, variants in keywords.items():
                for phrase in variants:
                    if cls.match_keyword_sequence(words, i, phrase):
                        for j in range(i+1, min(i+7, len(words))): # Look a little further ahead
                            if words[j] == '6.25': # Skip nitrogen multiplier
                                continue
                            if re.match(r'\d+\.?\d*', words[j]):
                                if key not in nutrition:
                                    nutrition[key] = float(words[j])
                                break

        if "fat" not in nutrition:
            for i, word in enumerate(words):
                if cls.match_keyword_sequence(words, i, "total fat") or cls.match_keyword_sequence(words, i, "fat"):
                    context = " ".join(words[max(0, i-1):i+2])
                    if "trans" in context or "saturated" in context or "sat" in context:
                        continue
                    for j in range(i+1, min(i+7, len(words))):
                        if re.match(r'\d+\.?\d*', words[j]):
                            nutrition["fat"] = float(words[j])
                            break

        return nutrition

    @staticmethod
    def detect_base(text):
        if "per 100g" in text or "per 100 g" in text:
            return "per 100g"
        return "per serving"