import os
import csv
import traceback
from datetime import date, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import pytesseract

# Core Module Imports
from core.db import get_db_connection, NutritionDatabase
from core.ml_engine import PhysiqueAnalyzer
from core.tracking import DailyTracker
from core.nutrition import NutritionCalculator
from core.ocr_engine import PackagedFoodEngine

app = Flask(__name__)
CORS(app) # Crucial: Allows Next.js to talk to Flask

# Temporary folder for CV scanner image uploads
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------------------------------------------------
# 1. NUTRITION DASHBOARD ROUTES
# ---------------------------------------------------------
@app.route('/api/nutrition/today', methods=['GET'])
def get_todays_nutrition():
    try:
        tracker = DailyTracker(user_id="user_123")
        return jsonify(tracker.get_ui_payload())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/nutrition/weekly', methods=['GET'])
def get_weekly_progress():
    user_id = "user_123"
    try:
        # 1. Fetch Target Calories
        profile = NutritionDatabase.get_user_targets(user_id)
        target_cals = profile['target_calories'] if profile else 2500
        
        # 2. Get Dates for Current Week (Mon-Sun)
        today = date.today()
        monday = today - timedelta(days=today.weekday())
        sunday = monday + timedelta(days=6)
        
        # 3. Fetch Weekly Logs
        query = """
            SELECT log_date, consumed_calories 
            FROM daily_logs 
            WHERE user_id = %s AND log_date >= %s AND log_date <= %s
        """
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id, monday, sunday))
                logs = cursor.fetchall()
        
        # 4. Format into a dictionary: {"YYYY-MM-DD": 95}
        progress_dict = {}
        for log in logs:
            date_str = log['log_date'].strftime('%Y-%m-%d')
            progress_pct = (log['consumed_calories'] / target_cals) * 100
            progress_dict[date_str] = round(progress_pct)
            
        return jsonify(progress_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------------------
# 2. ONBOARDING & PROFILE ROUTES
# ---------------------------------------------------------
@app.route('/api/onboarding', methods=['POST'])
def complete_onboarding():
    data = request.json
    user_id = data.get("userId", "user_123") 
    
    try:
        weight = float(data["weight"])
        height = float(data["height"])
        
        # Run ML Body Fat Prediction
        bf_pct = PhysiqueAnalyzer.predict_body_fat(
            weight_kg=weight, height_cm=height,
            waist=float(data["waist"]), chest=float(data["chest"]),
            arm=float(data["arm"]), thigh=float(data["thigh"])
        )
        
        # Calculate Targets
        primary_goal = data["primaryGoals"][0].replace("_", " ") 
        bmr = NutritionCalculator.calculate_bmr("male", 25, weight, height)
        
        activity_map = {"2_days": 1.375, "3_4_days": 1.55, "5_plus": 1.725}
        activity_mult = activity_map.get(data["workoutDays"], 1.2)
        tdee = NutritionCalculator.calculate_tdee(bmr, activity_mult)
        
        daily_cals = NutritionCalculator.calculate_daily_calories(tdee, weight, primary_goal, "moderate")
        macros = NutritionCalculator.calculate_macros(weight, daily_cals, primary_goal)
        
        # Save to Neon
        user_profile = {
            "id": user_id, "weight_kg": weight, "height_cm": height, "body_fat_pct": bf_pct,
            "body_type": data["bodyType"], "primary_goals": data["primaryGoals"],
            "workout_days": data["workoutDays"], "soreness_recovery": data["soreness"],
            "medical_conditions": data["medicalConditions"], "workout_location": data["workoutLocation"],
            "available_equipment": data.get("availableEquipment", []),
            "target_calories": daily_cals, "target_protein": macros["protein_g"],
            "target_carbs": macros["carbs_g"], "target_fat": macros["fat_g"], "sat_fat_limit": macros["sat_fat_limit_g"]
        }
        NutritionDatabase.create_user_profile(user_profile)
        
        return jsonify({"status": "success", "targets": macros}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ---------------------------------------------------------
# 3. PHYSIQUE ANALYTICS ROUTES
# ---------------------------------------------------------
@app.route('/api/progress', methods=['GET'])
def get_progress_history():
    user_id = "user_123" 
    query = "SELECT * FROM measurement_logs WHERE user_id = %s ORDER BY log_date ASC;"
    
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id,))
                history = cursor.fetchall()
                
        for entry in history:
            entry['log_date'] = entry['log_date'].strftime('%Y-%m-%d')
            
        return jsonify({"history": history})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/progress/update', methods=['POST'])
def update_progress():
    data = request.json
    user_id = "user_123"
    today = date.today()
    
    try:
        weight = float(data["weight"])
        waist = float(data["waist"])
        chest = float(data["chest"])
        arm = float(data["arm"])
        thigh = float(data["thigh"])
        
        # Get baseline height from DB to feed into ML model
        profile = NutritionDatabase.get_user_targets(user_id)
        height_cm = profile["height_cm"] if profile and "height_cm" in profile else 175.0

        new_bf_pct = PhysiqueAnalyzer.predict_body_fat(
            weight_kg=weight, height_cm=height_cm, 
            waist=waist, chest=chest, arm=arm, thigh=thigh
        )
        
        query = """
            INSERT INTO measurement_logs 
            (user_id, log_date, weight_kg, body_fat_pct, waist_cm, chest_cm, arm_cm, thigh_cm)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id, log_date) 
            DO UPDATE SET 
                weight_kg = EXCLUDED.weight_kg, body_fat_pct = EXCLUDED.body_fat_pct,
                waist_cm = EXCLUDED.waist_cm, chest_cm = EXCLUDED.chest_cm,
                arm_cm = EXCLUDED.arm_cm, thigh_cm = EXCLUDED.thigh_cm;
        """
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id, today, weight, new_bf_pct, waist, chest, arm, thigh))
            conn.commit()
            
        return jsonify({"status": "success", "new_bf_pct": new_bf_pct})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ---------------------------------------------------------
# 4. NUTRITION DATABASE & SEARCH
# ---------------------------------------------------------
SEARCH_DB = []
try:
    csv_path = os.path.join('core', 'indian_food_dataset.csv')
    with open(csv_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dish_name = row.get('Dish Name', '').strip()
            if dish_name:
                SEARCH_DB.append({
                    "id": dish_name, 
                    "name": dish_name,
                })
    print(f"✅ Successfully loaded {len(SEARCH_DB)} items from Indian Food Database.")
except Exception as e:
    print(f"⚠️ Warning: Could not load indian_food_dataset.csv. Ensure it is in the core folder. Error: {e}")

@app.route('/api/food/search', methods=['GET'])
def search_food():
    """Filters the loaded CSV dataset based on the Next.js query."""
    query = request.args.get('q', '').lower().strip()
    if not query or not SEARCH_DB:
        return jsonify([])
        
    results = [food for food in SEARCH_DB if query in food['name'].lower()]
    return jsonify(results[:15])

# ---------------------------------------------------------
# 5. SCANNER & LOGGING ROUTES
# ---------------------------------------------------------
@app.route('/api/scan/packaged', methods=['POST'])
def scan_packaged_food():
    if 'image' not in request.files:
        return jsonify({"error": "No image"}), 400
    
    file = request.files['image']
    filepath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(filepath)

    try:
        processed_img = PackagedFoodEngine.preprocess_image(filepath)
        
        # Use psm 4 to maintain table column structures
        raw_text = pytesseract.image_to_string(processed_img, config=r'--oem 3 --psm 4')
        clean_text = PackagedFoodEngine.normalize_text(raw_text)
        
        # --- THE X-RAY LOGS ---
        print("\n" + "="*40)
        print("🔍 RAW OCR OUTPUT:")
        print(raw_text)
        print("-" * 40)
        print("🧼 CLEANED TEXT:")
        print(clean_text)
        print("="*40 + "\n")
        
        nutrition = PackagedFoodEngine.extract_nutrition(clean_text)
        base = PackagedFoodEngine.detect_base(clean_text)
        
        os.remove(filepath)
        
        return jsonify({
            "success": True,
            "nutrition": nutrition, 
            "base": base
        })
    except Exception as e:
        print(f"🔥 OCR ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/scan/log', methods=['POST'])
def log_scanned_meal():
    """Logs meals sourced from the CSV search or CV Scanner"""
    try:
        data = request.json
        print(f"DEBUG [Scan Log]: Received payload: {data}")
        
        # Safely extract the list
        items_to_log = data.get('scanned_items', []) if isinstance(data, dict) else data
        
        if not items_to_log:
            return jsonify({"error": "No items provided"}), 400

        # --- THE FIX: Normalize the dictionary keys ---
        # Map Colab's 'protein_g' to the 'protein' key your database expects
        normalized_items = []
        for item in items_to_log:
            normalized_items.append({
                'food_id': item.get('food_id', 'unknown-item'),
                'weight_g': item.get('weight_g', 0),
                'calories': item.get('calories', 0),
                
                # If 'protein_g' exists, use it. Otherwise, look for 'protein'. Default to 0.
                'protein': item.get('protein_g', item.get('protein', 0)),
                'carbs': item.get('carbs_g', item.get('carbs', 0)),
                'fat': item.get('fat_g', item.get('fat', 0))
            })

        # Initialize tracker and pass the freshly normalized list
        tracker = DailyTracker(user_id="user_123")
        updated_payload = tracker.log_meal(normalized_items)
        
        return jsonify(updated_payload)
        
    except Exception as e:
        print(f"🔥 CRASH IN /api/scan/log: {str(e)}")
        traceback.print_exc() 
        return jsonify({"error": str(e)}), 500


@app.route('/api/manual/log', methods=['POST'])
def log_manual_meal():
    """Logs raw macros derived from the OCR Barcode Scanner"""
    data = request.json
    print(f"DEBUG [Manual Log]: Received payload: {data}")
    try:
        tracker = DailyTracker(user_id="user_123")
        updated_ui_payload = tracker.log_manual_macros(data)
        return jsonify(updated_ui_payload)
    except Exception as e:
        print(f"🔥 CRASH IN MANUAL LOG: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)