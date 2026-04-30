import os
import csv
from datetime import date
from core.db import NutritionDatabase

# --- Load Dataset into Memory ---
CSV_PATH = os.path.join(os.path.dirname(__file__), 'indian_food_dataset.csv')
FOOD_DB = {}

try:
    with open(CSV_PATH, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        reader.fieldnames = [name.strip() for name in reader.fieldnames]
        for row in reader:
            dish_name = row.get('Dish Name', '').strip()
            if dish_name:
                FOOD_DB[dish_name] = {
                    "cal": float(row.get('Calories (kcal)', 0) or 0),
                    "pro": float(row.get('Protein (g)', 0) or 0),
                    "carb": float(row.get('Carbohydrates (g)', 0) or 0),
                    "fat": float(row.get('Fats (g)', 0) or 0),
                    "sat": float(row.get('Fats (g)', 0) or 0) * 0.2, 
                    "base_weight": 100.0 
                }
except Exception as e:
    print(f"⚠️ Warning: Could not load food dataset from {CSV_PATH}. Error: {e}")

# Fallback dictionary specifically for Computer Vision outputs
CV_FALLBACK_TABLE = {
    "chicken_tikka_masala": (150, 14.0, 5.0, 8.0, 2.0, 3.0, 100),
    "kofta": (180, 8.0, 12.0, 10.0, 3.0, 4.0, 100),
    "naan": (290, 8.0, 48.0, 5.0, 2.0, 1.0, 100)
}

class DailyTracker:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.today = date.today()
        
        targets = NutritionDatabase.get_user_targets(self.user_id)
        if not targets:
            raise ValueError(f"User {user_id} not found. Please complete onboarding.")
        
        self.daily_targets = {
            "calories": targets["target_calories"],
            "protein_g": targets["target_protein"],
            "carbs_g": targets["target_carbs"],
            "fat_g": targets["target_fat"],
            "sat_fat_limit_g": targets["sat_fat_limit"]
        }

        log = NutritionDatabase.get_daily_log(self.user_id, self.today)
        if log:
            self.consumed_today = {
                "calories": log["consumed_calories"],
                "protein_g": log["consumed_protein"],
                "carbs_g": log["consumed_carbs"],
                "fat_g": log["consumed_fat"],
                "sat_fat_g": log["consumed_sat_fat"]
            }
        else:
            self.consumed_today = {
                "calories": 0, "protein_g": 0.0, "carbs_g": 0.0, 
                "fat_g": 0.0, "sat_fat_g": 0.0
            }

    def log_meal(self, cv_scanner_output: list) -> dict:
        """Processes an array of food items from the CSV or the AI Scanner"""
        if isinstance(cv_scanner_output, dict):
            cv_scanner_output = cv_scanner_output.get("scanned_items", [])

        for item in cv_scanner_output:
            if not isinstance(item, dict): continue
                
            food_id = str(item.get("food_id", ""))
            weight_g = float(item.get("weight_g", 0))

            if not food_id or weight_g <= 0:
                continue

            if food_id in FOOD_DB:
                data = FOOD_DB[food_id]
                mult = weight_g / data["base_weight"]
                
                self.consumed_today["calories"] += int(data.get("cal", 0) * mult)
                self.consumed_today["protein_g"] += round(data.get("pro", 0) * mult, 1)
                self.consumed_today["carbs_g"] += round(data.get("carb", 0) * mult, 1)
                self.consumed_today["fat_g"] += round(data.get("fat", 0) * mult, 1)
                self.consumed_today["sat_fat_g"] += round(data.get("sat", 0) * mult, 1)
            
            elif food_id.lower() in CV_FALLBACK_TABLE:
                base_cal, base_pro, base_carb, base_fat, base_sug, base_sat, base_weight = CV_FALLBACK_TABLE[food_id.lower()]
                mult = weight_g / base_weight
                
                self.consumed_today["calories"] += int(base_cal * mult)
                self.consumed_today["protein_g"] += round(base_pro * mult, 1)
                self.consumed_today["carbs_g"] += round(base_carb * mult, 1)
                self.consumed_today["fat_g"] += round(base_fat * mult, 1)
                self.consumed_today["sat_fat_g"] += round(base_sat * mult, 1)

        NutritionDatabase.upsert_daily_log(self.user_id, self.today, self.consumed_today)
        return self.get_ui_payload()

    def log_manual_macros(self, manual_data: dict) -> dict:
        """Processes raw macros from the OCR Barcode feature"""
        print(f"DEBUG: OCR/Manual payload received: {manual_data}")
        cals = float(manual_data.get("calories") or 0)
        pro = float(manual_data.get("protein") or 0)
        carbs = float(manual_data.get("carbs") or 0)
        fat = float(manual_data.get("fat") or 0)
        
        self.consumed_today["calories"] += int(cals)
        self.consumed_today["protein_g"] += round(pro, 1)
        self.consumed_today["carbs_g"] += round(carbs, 1)
        self.consumed_today["fat_g"] += round(fat, 1)
        self.consumed_today["sat_fat_g"] += round(fat * 0.2, 1) 

        NutritionDatabase.upsert_daily_log(self.user_id, self.today, self.consumed_today)
        print(f"DEBUG: Successfully updated DB with new totals.")
        return self.get_ui_payload()

    def get_ui_payload(self) -> dict:
        return {
            "calories": {
                "current": self.consumed_today["calories"],
                "target": self.daily_targets["calories"]
            },
            "macros": {
                "carbs": { "current": self.consumed_today["carbs_g"], "target": self.daily_targets["carbs_g"], "unit": "g", "colorClass": "bg-[#84cc16]", "bgClass": "bg-[#84cc16]/15" },
                "protein": { "current": self.consumed_today["protein_g"], "target": self.daily_targets["protein_g"], "unit": "g", "colorClass": "bg-[#fbbf24]", "bgClass": "bg-[#fbbf24]/15" },
                "satFat": { "current": self.consumed_today["sat_fat_g"], "target": self.daily_targets["sat_fat_limit_g"], "unit": "g", "colorClass": "bg-[#a855f7]", "bgClass": "bg-[#a855f7]/15" }
            }
        }