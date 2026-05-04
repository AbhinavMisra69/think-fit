import os
import csv
import traceback
import json
from datetime import date, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import pytesseract
import psycopg2
from psycopg2.extras import RealDictCursor
import math
import datetime

# Core Module Imports
from core.db import get_db_connection, NutritionDatabase
from core.ml_engine import PhysiqueAnalyzer
from core.tracking import DailyTracker
from core.nutrition import NutritionCalculator
from core.ocr_engine import PackagedFoodEngine
from core.planning import AdaptiveCoach 

from exercise_engine.core_logic import determine_active_phase, determine_weekly_split, schedule_weekly_blueprints, generate_daily_workout, generate_custom_timeline
from exercise_engine.utils import calculate_dynamic_weeks_off
from exercise_engine.database import  blueprint_library, phase_parameters_kb, macrocycle_kb, PHASE_UI_META

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper functions to sanitize incoming React JSON and Database NULLs
def safe_float(val, default=0.0):
    try:
        if val is None or val == "": 
            return float(default)
        return float(val)
    except (ValueError, TypeError):
        return float(default)

def safe_str(val, default=""):
    if val is None or val == "":
        return str(default)
    return str(val).strip()

SEARCH_DB = []
try:
    csv_path = os.path.join('core', 'indian_food_dataset.csv')
    with open(csv_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            dish_name = row.get('Dish Name', '').strip()
            
            if dish_name:
                # 1. Slugify the ID to match your AI scan/search format (e.g. 'aloo-fry')
                food_id = dish_name.lower().replace(" ", "-")
                
                # 2. Extract values using the EXACT headers from your CSV
                cals = row.get('Calories (kcal)')
                prot = row.get('Protein (g)')
                carb = row.get('Carbohydrates (g)')
                fat  = row.get('Fats (g)')
                
                SEARCH_DB.append({
                    "id": food_id, 
                    "name": dish_name,
                    # Safely convert to float, defaulting to 0.0 if the cell is completely empty
                    "calories": float(cals) if cals and cals.strip() else 0.0,
                    "protein": float(prot) if prot and prot.strip() else 0.0,
                    "carbs": float(carb) if carb and carb.strip() else 0.0,
                    "fat": float(fat) if fat and fat.strip() else 0.0,
                    # Your CSV doesn't have a serving size column, so we assume 100g standard
                    "serving_size": 100.0 
                })
                
    print(f"✅ Successfully loaded {len(SEARCH_DB)} items from CSV.")
    print(f"🔍 PEEK: {SEARCH_DB[0]['name']} -> {SEARCH_DB[0]['calories']} kcal, {SEARCH_DB[0]['protein']}g protein")
    
except Exception as e:
    print(f"⚠️ Error loading CSV: {e}")
# ---------------------------------------------------------
# 1. ONBOARDING & BODY FAT CALCULATOR ROUTES
# ---------------------------------------------------------
@app.route('/api/calculate_bf', methods=['POST'])
def calculate_bf():
    data = request.json
    try:
        gender = safe_str(data.get('gender', 'male')).lower()
        height = safe_float(data.get('height'))
        waist = safe_float(data.get('waist'))
        neck = safe_float(data.get('neck'))
        hip = safe_float(data.get('hip'))

        # Safety check to prevent math domain errors (log of 0 or negative)
        if height <= 0 or waist <= 0 or neck <= 0:
            return jsonify({"body_fat_percentage": 15.0}), 200 # Safe fallback

        if gender == 'female':
            # U.S. Navy Formula for Women
            # 495 / (1.29579 - 0.35004 * log10(waist + hip - neck) + 0.22100 * log10(height)) - 450
            if (waist + hip - neck) <= 0: return jsonify({"body_fat_percentage": 25.0}), 200
            
            bf = 495.0 / (1.29579 - 0.35004 * math.log10(waist + hip - neck) + 0.22100 * math.log10(height)) - 450.0
        else:
            # U.S. Navy Formula for Men
            # 495 / (1.0324 - 0.19077 * log10(waist - neck) + 0.15456 * log10(height)) - 450
            if (waist - neck) <= 0: return jsonify({"body_fat_percentage": 15.0}), 200
            
            bf = 495.0 / (1.0324 - 0.19077 * math.log10(waist - neck) + 0.15456 * math.log10(height)) - 450.0

        # Clamp the result so it never returns an impossible number (e.g. -2% or 90%)
        bf_percentage = max(3.0, min(round(bf, 1), 60.0))
        
        print(f"✅ Navy Formula calculated {bf_percentage}% BF for {gender}")
        
        return jsonify({"body_fat_percentage": bf_percentage}), 200

    except Exception as e:
        print(f"🔥 BF Calculation Error: {e}")
        return jsonify({"error": str(e), "body_fat_percentage": 15.0}), 400
    
@app.route('/api/onboarding', methods=['POST'])
def save_onboarding():
    data = request.json
    
    user_id = get_user_id_from_request(request)
    if not user_id:
        return jsonify({"error": "User ID is missing. User not logged in."}), 400

    try:
        gender = safe_str(data.get('gender', 'male'))
        weight = safe_float(data.get('weight'))
        height = safe_float(data.get('height'))
        age = int(safe_float(data.get('age', 25)))
        neck = safe_float(data.get('neck'))
        waist = safe_float(data.get('waist'))
        chest = safe_float(data.get('chest'))
        arm = safe_float(data.get('arm'))
        hip = safe_float(data.get('hip'))
        
        body_type = safe_str(data.get('bodyType'), 'mesomorph')
        activity_level = safe_str(data.get('activityLevel'), 'sedentary')
        experience_level = safe_str(data.get('experienceLevel'), 'beginner')
        
        days_available = int(safe_float(data.get('workoutDays', 4)))
        duration_weeks = int(safe_float(data.get('durationWeeks', 12)))
        print(f"\n\nduration_weeks : {duration_weeks}\n\n")
        
        # --- THE FIX: Keep it as a native Python list! ---
        selected_workout_days = data.get('selectedWorkoutDays', [])
        if not selected_workout_days:
            selected_workout_days = ["Monday", "Wednesday", "Friday"]
        
        facility_type = safe_str(data.get('workoutLocation'), 'gym')
        soreness_recovery = safe_str(data.get('soreness'), 'normal')
        
        medical_conditions = data.get('medicalConditions', [])
        available_equipment = data.get('availableEquipment', [])
        
        primary_goals = data.get('primaryGoals', [])
        goal_main = primary_goals[0] if primary_goals else 'recomposition'
        bf_pct = safe_float(data.get('estimatedBF', 15.0))

        # ---------------------------------------------------------
        # Tap directly into your core.nutrition engine
        # ---------------------------------------------------------
        try:
            nutrition_profile = NutritionCalculator.generate_full_profile(
                sex=gender, age=age, height_cm=height, weight_kg=weight,
                activity_level=activity_level, body_fat_pct=bf_pct, experience_level=experience_level
            )
            
            # Extract EVERYTHING instead of just calories
            target_calories = nutrition_profile["results"]["daily_calories"]
            macs = nutrition_profile["results"]["macros"]
            target_protein = macs["protein_g"]
            target_carbs = macs["carbs_g"]
            target_fat = macs["fat_g"]
            target_sat_fat = macs["sat_fat_limit_g"]
            
        except Exception as e:
            print(f"⚠️ Nutrition Engine Failed: {e}. Falling back to defaults.")
            target_calories, target_protein, target_carbs, target_fat, target_sat_fat = 2000, 150, 200, 65, 20

        # Database Insertion
        # Database Insertion
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cur = conn.cursor()

        insert_query = """
        INSERT INTO users (
            id, gender, weight_kg, height_cm, neck, waist_cm, chest_cm, arm_cm, hip, 
            body_type, activity_level, experience_level, days_available, workout_days, 
            duration_weeks, facility_type, soreness_recovery, medical_conditions, available_equipment, 
            goal, body_fat_pct, target_calories,
            target_protein, target_carbs, target_fat, sat_fat_limit
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            gender = EXCLUDED.gender,
            weight_kg = EXCLUDED.weight_kg,
            height_cm = EXCLUDED.height_cm,
            neck = EXCLUDED.neck,
            waist_cm = EXCLUDED.waist_cm,
            chest_cm = EXCLUDED.chest_cm,
            arm_cm = EXCLUDED.arm_cm,
            hip = EXCLUDED.hip,
            body_type = EXCLUDED.body_type,
            body_fat_pct = EXCLUDED.body_fat_pct,
            activity_level = EXCLUDED.activity_level,
            experience_level = EXCLUDED.experience_level,
            days_available = EXCLUDED.days_available,
            workout_days = EXCLUDED.workout_days,
            duration_weeks = EXCLUDED.duration_weeks,
            facility_type = EXCLUDED.facility_type,
            soreness_recovery = EXCLUDED.soreness_recovery,
            medical_conditions = EXCLUDED.medical_conditions,
            available_equipment = EXCLUDED.available_equipment,
            goal = EXCLUDED.goal,
            target_calories = EXCLUDED.target_calories,
            target_protein = EXCLUDED.target_protein,
            target_carbs = EXCLUDED.target_carbs,
            target_fat = EXCLUDED.target_fat,
            sat_fat_limit = EXCLUDED.sat_fat_limit,
            updated_at = CURRENT_TIMESTAMP;
        """
        
        cur.execute(insert_query, (
            user_id, gender, weight, height, neck, waist, chest, arm, hip,
            body_type, activity_level, experience_level, days_available, selected_workout_days, 
            duration_weeks, facility_type, soreness_recovery, medical_conditions, available_equipment, 
            goal_main, bf_pct, target_calories, 
            target_protein, target_carbs, target_fat, target_sat_fat
        ))

        print(f"\n\nduration_weeks : {duration_weeks}\n\n")

        cur.execute("""
        INSERT INTO measurement_logs 
        (user_id, weight_kg, body_fat_pct, waist_cm, chest_cm, arm_cm, log_date)
        VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE)
        ON CONFLICT (user_id, log_date) DO UPDATE SET
            weight_kg = EXCLUDED.weight_kg,
            body_fat_pct = EXCLUDED.body_fat_pct,
            waist_cm = EXCLUDED.waist_cm,
            chest_cm = EXCLUDED.chest_cm,
            arm_cm = EXCLUDED.arm_cm;
        """, (user_id, weight, bf_pct, waist, chest, arm))
        # ---------------------------------------------------------
        # NEW: Initialize the Exercise Engine State
        # ---------------------------------------------------------
        starting_phases = {
            "build_muscle": "foundation_hypertrophy",
            "lose_fat": "foundation",
            "recomposition": "strength_foundation",
            "general_health": "foundation"
        }
        starting_phase = starting_phases.get(goal_main, "foundation")

        cur.execute("""
        INSERT INTO exercise_state (
            user_id, current_goal, experience_level, 
            preferred_duration_weeks, weeks_in_program, 
            active_phase, last_assigned_split, split_rotation_index
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE SET
            current_goal = EXCLUDED.current_goal,
            experience_level = EXCLUDED.experience_level,
            preferred_duration_weeks = EXCLUDED.preferred_duration_weeks,
            active_phase = EXCLUDED.active_phase,
            updated_at = CURRENT_TIMESTAMP;
        """, (
            user_id, 
            goal_main, 
            experience_level,
            duration_weeks,              
            1,                # Start at week 1
            starting_phase,   # The correct mapped phase!
            'full_body',      # Safe starting split
            0                 # Start at array index 0
        ))
        # ---------------------------------------------------------

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"status": "success", "message": f"Profile synced. Target Cals: {target_calories}"}), 200

    except Exception as e:
        print(f"🔥 Database Error: {e}")
        return jsonify({"error": str(e)}), 500
    
# 2. NUTRITION DASHBOARD ROUTES
# ---------------------------------------------------------
@app.route('/api/scan/log', methods=['POST'])
def log_scanned_meal():
    try:
        data = request.json
        # 1. Identity Check
        session_data = data.get('thinkfit_session', {})
        user_id = session_data.get('id')
        
        if not user_id:
            return jsonify({"error": "User ID is missing."}), 400
        
        items_to_log = data.get('scanned_items', [])
        if not items_to_log:
            return jsonify({"error": "No items provided"}), 400

        total_cals, total_prot, total_carb, total_fat, total_sat = 0, 0, 0, 0, 0

        for item in items_to_log:
            f_id = item.get('food_id', 'unknown').lower().strip().replace(" ", "-")
            w = float(item.get('weight_g') or 0)
            
            # 1. Try to find the item in our rich SEARCH_DB
            food_info = next((x for x in SEARCH_DB if x['id'] == f_id), None)

            # 👇 ADD THIS PRINT STATEMENT 👇
            print(f"🔍 DEBUG: Searched for ID '{f_id}'. Found match: {food_info is not None}")

            if food_info:
                # Math: Calculate based on the weight
                mult = w / food_info.get('serving_size', 100.0)
                
                total_cals += (food_info.get('calories', 0) * mult)
                # ... (rest of the math)

        # 👇 ADD THIS PRINT STATEMENT RIGHT BEFORE THE SQL QUERY 👇
        print(f"🛑 ABOUT TO SAVE TO DB -> Cals: {total_cals}, Prot: {total_prot}")

        # 3. Database UPSERT to daily_logs
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cur = conn.cursor()

        # REMOVED the 'updated_at' column to perfectly match your schema
        upsert_query = """
        INSERT INTO daily_logs (
            user_id, consumed_calories, consumed_protein, 
            consumed_carbs, consumed_fat, consumed_sat_fat
        ) 
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id, log_date) 
        DO UPDATE SET
            consumed_calories = daily_logs.consumed_calories + EXCLUDED.consumed_calories,
            consumed_protein = daily_logs.consumed_protein + EXCLUDED.consumed_protein,
            consumed_carbs = daily_logs.consumed_carbs + EXCLUDED.consumed_carbs,
            consumed_fat = daily_logs.consumed_fat + EXCLUDED.consumed_fat,
            consumed_sat_fat = daily_logs.consumed_sat_fat + EXCLUDED.consumed_sat_fat;
        """

        cur.execute(upsert_query, (
            user_id, 
            int(total_cals), 
            round(total_prot, 1), 
            round(total_carb, 1), 
            round(total_fat, 1),
            round(total_sat, 1)
        ))
        
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "status": "success", 
            "added_calories": int(total_cals),
            "added_protein": round(total_prot, 1)
        }), 200
        
    except Exception as e:
        print(f"🔥 Final Logging Error: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/progress/update', methods=['POST'])
def update_progress():
    session_str = request.headers.get('X-Session')
    if not session_str:
        return jsonify({"error": "No valid login session found"}), 401

    try:
        session_data = json.loads(session_str)
        user_id = session_data.get('id')
        data = request.json
        
        current_weight = safe_float(data.get('weight'))
        current_waist = safe_float(data.get('waist'))
        current_chest = safe_float(data.get('chest'))
        current_arm = safe_float(data.get('arm'))
        current_thigh = safe_float(data.get('thigh')) 
        
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute("""
            SELECT gender, height_cm, neck, hip, goal, target_calories, weight_kg, body_fat_pct 
            FROM users WHERE id = %s
        """, (user_id,))
        user_data = cur.fetchone()
        
        if not user_data:
            return jsonify({"error": "User profile not found"}), 404

        db_gender = safe_str(user_data.get('gender'), default="male")
        db_goal = safe_str(user_data.get('goal'), default="maintain")
        db_height = safe_float(user_data.get('height_cm'))
        db_neck = safe_float(user_data.get('neck'))
        db_hip = safe_float(user_data.get('hip'))
        db_weight = safe_float(user_data.get('weight_kg'))
        db_bf_pct = safe_float(user_data.get('body_fat_pct'))

        current_bf_pct = PhysiqueAnalyzer.predict_body_fat(
            db_gender, current_weight, db_height, 
            current_waist, db_neck, current_chest, current_arm, db_hip
        )

        cur.execute("""
            INSERT INTO measurement_logs 
            (user_id, weight_kg, body_fat_pct, waist_cm, chest_cm, arm_cm, thigh_cm)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, log_date
        """, (user_id, current_weight, current_bf_pct, current_waist, current_chest, current_arm, current_thigh))
        
        cur.execute("""
            SELECT weight_kg, body_fat_pct, waist_cm, chest_cm, arm_cm, thigh_cm 
            FROM measurement_logs 
            WHERE user_id = %s 
            ORDER BY log_date DESC 
            OFFSET 1 LIMIT 1
        """, (user_id,))
        prev_log = cur.fetchone()

        coach_result = None

        if prev_log:
            prev_measurements = {
                "waist_cm": safe_float(prev_log.get('waist_cm')),
                "chest_cm": safe_float(prev_log.get('chest_cm')),
                "arm_cm": safe_float(prev_log.get('arm_cm')),
                "thigh_cm": safe_float(prev_log.get('thigh_cm'))
            }
            
            curr_measurements = {
                "waist_cm": current_waist,
                "chest_cm": current_chest,
                "arm_cm": current_arm,
                "thigh_cm": current_thigh
            }

            prev_weight = safe_float(prev_log.get('weight_kg'), default=db_weight)
            prev_bf = safe_float(prev_log.get('body_fat_pct'), default=db_bf_pct)
            current_cals = safe_float(user_data.get('target_calories'), default=2000.0)

            # AdaptiveCoach logic dynamically handles feedback and target adjustments
            coach_result = AdaptiveCoach.weekly_check_in(
                previous_weight=prev_weight, 
                current_weight=current_weight, 
                previous_bf_pct=prev_bf, 
                current_bf_pct=current_bf_pct,
                previous_measurements=prev_measurements, 
                current_measurements=curr_measurements,
                current_daily_cals=current_cals, 
                goal=db_goal, 
                expected_loss_rate="moderate"
            )

            if coach_result and coach_result.get('adjustment_made'):
                new_cals = safe_float(coach_result.get('new_daily_calories'), default=current_cals)
                cur.execute("""
                    UPDATE users 
                    SET target_calories = %s, weight_kg = %s, body_fat_pct = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (new_cals, current_weight, current_bf_pct, user_id))
            else:
                cur.execute("""
                    UPDATE users 
                    SET weight_kg = %s, body_fat_pct = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (current_weight, current_bf_pct, user_id))
        else:
            cur.execute("""
                UPDATE users 
                SET weight_kg = %s, body_fat_pct = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (current_weight, current_bf_pct, user_id))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "status": "success", 
            "message": "Progress logged successfully",
            "coach_insights": coach_result
        }), 200

    except Exception as e:
        print(f"Progress Update Error: {e}")
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------------------
# 3. PHYSIQUE ANALYTICS ROUTES
# ---------------------------------------------------------
@app.route('/api/progress', methods=['GET'])
def get_progress_history():
    session_str = request.headers.get('X-Session')
    if not session_str:
        return jsonify({"error": "Unauthorized"}), 401
        
    try:
        session_data = json.loads(session_str)
        user_id = session_data.get('id')
    except Exception:
        return jsonify({"error": "Invalid session"}), 401

    query = "SELECT * FROM measurement_logs WHERE user_id = %s ORDER BY log_date ASC;"
    
    try:
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cursor.execute(query, (user_id,))
        history = cursor.fetchall()
        
        history_list = []
        for entry in history:
            entry_dict = dict(entry)
            entry_dict['log_date'] = entry_dict['log_date'].strftime('%Y-%m-%d')
            history_list.append(entry_dict)
            
        cursor.close()
        conn.close()
            
        return jsonify({"history": history_list})
    except Exception as e:
        print(f"Fetch Error: {e}")
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------------------
# 4. NUTRITION DATABASE & SEARCH
# ---------------------------------------------------------

@app.route('/api/food/search', methods=['GET'])
def search_food():
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
        raw_text = pytesseract.image_to_string(processed_img, config=r'--oem 3 --psm 6')
        clean_text = PackagedFoodEngine.normalize_text(raw_text)
        
        print("\n" + "="*40)
        print("🔍 RAW OCR OUTPUT:\n", raw_text)
        print("-" * 40)
        print("🧼 CLEANED TEXT:\n", clean_text)
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
# Helper to reliably grab the user_id from either the JSON body or the X-Session header
# Helper to reliably grab the user_id from the thinkfit_session key
@app.route('/api/manual/log', methods=['POST', 'OPTIONS'])
def log_manual_meal():
    # --- CORS PREFLIGHT CATCH ---
    # The browser sends an 'OPTIONS' request first to check permissions. 
    # We must say "Yes, go ahead" (200 OK) before it will send the actual POST data.
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.json
        print(f"DEBUG [Manual Log]: Received payload: {data}")
        
        # 1. The Identity Check
        session_data = data.get('thinkfit_session', {})
        user_id = session_data.get('id')
        
        if not user_id:
            return jsonify({"error": "User ID is missing. Cannot log meal."}), 400

        # 2. Extract Macros
        cals = int(float(data.get('calories') or 0))
        prot = float(data.get('protein') or 0)
        carb = float(data.get('carbs') or 0)
        fat  = float(data.get('fat') or 0)
        sat_fat = float(data.get('sat_fat') or 0)

        # 3. Database UPSERT
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cur = conn.cursor()

        upsert_query = """
        INSERT INTO daily_logs (
            user_id, consumed_calories, consumed_protein, 
            consumed_carbs, consumed_fat, consumed_sat_fat
        ) 
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id, log_date) 
        DO UPDATE SET
            consumed_calories = daily_logs.consumed_calories + EXCLUDED.consumed_calories,
            consumed_protein = daily_logs.consumed_protein + EXCLUDED.consumed_protein,
            consumed_carbs = daily_logs.consumed_carbs + EXCLUDED.consumed_carbs,
            consumed_fat = daily_logs.consumed_fat + EXCLUDED.consumed_fat,
            consumed_sat_fat = daily_logs.consumed_sat_fat + EXCLUDED.consumed_sat_fat;
        """

        cur.execute(upsert_query, (user_id, cals, prot, carb, fat, sat_fat))
        
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "status": "success", 
            "message": "Manual macros added to daily log",
            "added": {"calories": cals, "protein": prot, "carbs": carb, "fat": fat}
        }), 200

    except Exception as e:
        print(f"🔥 CRASH IN MANUAL LOG: {str(e)}")
        return jsonify({"error": str(e)}), 500
    

def get_user_id_from_request(req):
    import json
    import urllib.parse
    
    # 0. Check Query Parameters FIRST (Best for GET requests)
    query_id = req.args.get('userId') or req.args.get('user_id')
    if query_id: 
        return query_id

    # 1. Try checking the JSON Body (For POST requests)
    data = req.get_json(silent=True) or {}
    session_data = data.get('thinkfit_session')
    
    if isinstance(session_data, str):
        try: session_data = json.loads(session_data)
        except: session_data = {}
            
    if session_data and isinstance(session_data, dict) and session_data.get('id'):
        return session_data.get('id')
        
    user_id = data.get('userId') or data.get('user_id')
    if user_id: return user_id

    # 2. Check the Cookies
    cookie_str = req.cookies.get('thinkfit_session')
    if cookie_str:
        try:
            decoded_cookie = urllib.parse.unquote(cookie_str)
            return json.loads(decoded_cookie).get('id')
        except: pass

    # 3. Check Headers
    header_str = req.headers.get('X-Session') or req.headers.get('Authorization')
    if header_str:
        try:
            header_data = json.loads(header_str)
            if isinstance(header_data, dict) and 'thinkfit_session' in header_data:
                return header_data['thinkfit_session'].get('id')
            elif isinstance(header_data, dict) and header_data.get('id'):
                return header_data.get('id')
        except:
            if "{" in header_str:
                try: return json.loads(header_str[header_str.find('{'):]).get('id')
                except: pass
                    
    return None

# ---------------------------------------------------------
# 2. NUTRITION DASHBOARD ROUTES
# ---------------------------------------------------------
import psycopg2
@app.route('/api/nutrition/today', methods=['GET'])
def get_today_nutrition():
    user_id = request.args.get('userId')
    if not user_id: return jsonify({"error": "User ID is required"}), 400

    try:
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cur = conn.cursor()

        # 1. FIXED: Explicitly asking for 'sat_fat_limit' instead of 'target_sat_fat'
        cur.execute("""
            SELECT target_calories, target_protein, target_carbs, sat_fat_limit 
            FROM users WHERE id = %s
        """, (user_id,))
        target_row = cur.fetchone()
        
        # Fallback values just in case onboarding failed
        t_cal = target_row[0] if target_row and target_row[0] else 2000
        t_prot = target_row[1] if target_row and target_row[1] else 150
        t_carb = target_row[2] if target_row and target_row[2] else 250
        t_sat = target_row[3] if target_row and target_row[3] else 25

        # 2. Fetch today's consumed totals from daily_logs
        cur.execute("""
            SELECT consumed_calories, consumed_protein, consumed_carbs, consumed_sat_fat 
            FROM daily_logs 
            WHERE user_id = %s AND log_date = CURRENT_DATE
        """, (user_id,))
        log_row = cur.fetchone()

        cals_current = float(log_row[0]) if log_row and log_row[0] else 0
        prot_current = float(log_row[1]) if log_row and log_row[1] else 0
        carb_current = float(log_row[2]) if log_row and log_row[2] else 0
        sat_current  = float(log_row[3]) if log_row and log_row[3] else 0

        cur.close()
        conn.close()

        # 3. Build the React Payload using the dynamic targets
        payload = {
            "calories": {
                "current": cals_current,
                "target": t_cal
            },
            "macros": {
                "carbs": {
                    "current": carb_current,
                    "target": t_carb,
                    "unit": "g",
                    "colorClass": "bg-indigo-500",
                    "bgClass": "bg-indigo-50"
                },
                "protein": {
                    "current": prot_current,
                    "target": t_prot,
                    "unit": "g",
                    "colorClass": "bg-emerald-500",
                    "bgClass": "bg-emerald-50"
                },
                "satFat": {
                    "current": sat_current,
                    "target": t_sat,
                    "unit": "g",
                    "colorClass": "bg-red-500",
                    "bgClass": "bg-red-50"
                }
            }
        }

        return jsonify(payload), 200

    except Exception as e:
        print(f"🔥 GET Today Nutrition Error: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/nutrition/weekly', methods=['GET'])
def get_weekly_progress():
    user_id = get_user_id_from_request(request)
    if not user_id:
        return jsonify({"error": "Unauthorized. Missing User ID."}), 401
        
    try:
        from datetime import date, timedelta
        import psycopg2
        from psycopg2.extras import RealDictCursor
        
        today = date.today()
        # Calculate Monday and Sunday of the current week
        monday = today - timedelta(days=today.weekday())
        sunday = monday + timedelta(days=6)
        
        # 1. Connect directly and safely
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # 2. Fetch the user's custom target calories directly
        cursor.execute("SELECT target_calories FROM users WHERE id = %s", (user_id,))
        user_row = cursor.fetchone()
        target_cals = user_row['target_calories'] if user_row and user_row['target_calories'] else 2000
        
        # 3. Fetch all logs for this week
        query = """
            SELECT log_date, consumed_calories 
            FROM daily_logs 
            WHERE user_id = %s AND log_date >= %s AND log_date <= %s
        """
        cursor.execute(query, (user_id, monday, sunday))
        logs = cursor.fetchall()
        
        # 4. Process the data into the {"YYYY-MM-DD": 85} format
        progress_dict = {}
        for log in logs:
            # Handle date formatting safely
            date_val = log['log_date']
            date_str = date_val.strftime('%Y-%m-%d') if hasattr(date_val, 'strftime') else str(date_val)
            
            # Calculate completion percentage
            progress_pct = (log['consumed_calories'] / target_cals) * 100
            progress_dict[date_str] = round(progress_pct)
            
        cursor.close()
        conn.close()
            
        return jsonify(progress_dict)
        
    except Exception as e:
        print(f"🔥 WEEKLY PROGRESS CRASH: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    

# ---------------------------------------------------------
# 6. WORKOUT EXPERT ROUTES
# ---------------------------------------------------------

import json
import os

# 1. Get the directory where THIS Python file lives (which is the think-fit folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Look directly into the 'data' folder right next to it
EXERCISE_DATA_PATH = os.path.join(BASE_DIR, 'data', 'exercises_enriched.json')
print(f"exercise data path is: {EXERCISE_DATA_PATH}")

# 3. Load the file into a Python dictionary
try:
    with open(EXERCISE_DATA_PATH, 'r') as f:
        exercise_dataset = json.load(f)
    print(f"Successfully loaded {len(exercise_dataset)} exercises from JSON.")
except FileNotFoundError:
    print(f"CRITICAL ERROR: Could not find {EXERCISE_DATA_PATH}. Make sure the file exists!")
    exercise_dataset = {} # Fallback to prevent immediate crashes

try:
    with open(EXERCISE_DATA_PATH, 'r') as f:
        exercise_dataset = json.load(f)
    print(f"Successfully loaded {len(exercise_dataset)} exercises from JSON.")
except FileNotFoundError:
    print(f"CRITICAL ERROR: Could not find {EXERCISE_DATA_PATH}. Make sure the file exists!")
    exercise_dataset = {} 

def get_db_connection():
    print("\n" + "="*50)
    print("🔄 TEST: Attempting database connection...")
    url = os.environ.get("DATABASE_URL")
    if not url:
        print("❌ FATAL: Python cannot find DATABASE_URL. It is None.")

    try:
        conn = psycopg2.connect(url)
        print("✅ SUCCESS: Connected to the Neon database perfectly!")
        print("="*50 + "\n")
        return conn
    except Exception as e:
        print("❌ FAILED: The connection crashed.")
        print(f"⚠️ Exact Error: {e}")
        print("="*50 + "\n")
        raise e
    
@app.route('/api/workout/macrocycle', methods=['GET'])
def get_macrocycle_overview():
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # 1. Fetch user data
        cursor.execute("""
            SELECT u.goal, e.weeks_in_program, u.duration_weeks
            FROM users u 
            JOIN exercise_state e ON u.id = e.user_id 
            WHERE u.id = %s
        """, (user_id,))
        user_data = cursor.fetchone()
        
        if not user_data:
            return jsonify({"error": "User not found"}), 404
            
        goal = user_data['goal']
        current_week = user_data['weeks_in_program']
        preferred_duration = user_data['duration_weeks']
        
        # 2. Call your custom algorithm!
        timeline_result = generate_custom_timeline(goal, preferred_duration, macrocycle_kb)
        
        # Safety check if the algorithm rejected the timeline
        if timeline_result["status"] == "rejected":
            return jsonify({"error": timeline_result["message"]}), 400
            
        # 3. Transform the algorithm's output into the rich UI format
        macrocycle_ui = []
        rolling_start_week = 1
        
        for phase_data in timeline_result["timeline"]:
            raw_name = phase_data["phase"]
            end_week = phase_data["end_week"]
            
            # Map the raw backend name to the UI metadata
            meta = PHASE_UI_META.get(raw_name, {
                "name": raw_name.replace('_', ' ').title(), 
                "focus": "Continuing progression.", 
                "theme": "blue"
            })
            
            macrocycle_ui.append({
                "phase": meta["name"],
                "start_week": rolling_start_week,
                "end_week": end_week,
                "focus": meta["focus"],
                "theme": meta["theme"]
            })
            
            # The next phase starts the week after this one ends
            rolling_start_week = end_week + 1
            
        # 4. Return the fully computed payload to React
        return jsonify({
            "status": "success",
            "total_weeks": preferred_duration,
            "current_week": current_week,
            "goal": goal,
            "phases": macrocycle_ui
        })
        
    except Exception as e:
        print(f"Error in macrocycle: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        cursor.close()
        conn.close()



@app.route('/api/workout/edit_week', methods=['POST'])
def edit_week():
    import json
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    new_days_names = data.get('new_days', []) 
    new_frequency = len(new_days_names)
    
    # 1. Hard API Validation (Backup for the React frontend)
    if new_frequency < 2 or new_frequency > 7:
        return jsonify({"status": "error", "message": "You must select between 2 and 7 workout days."})

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Map string days to numbers
        day_map = { "Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7 }
        new_day_indices = sorted([day_map[d] for d in new_days_names])
        
        # Get current state
        cursor.execute("SELECT active_phase, weeks_in_program FROM exercise_state WHERE user_id = %s", (user_id,))
        state = cursor.fetchone()
        current_week = state['weeks_in_program']
        active_phase = state['active_phase']
        
        cursor.execute("SELECT workout_json FROM generated_programs WHERE user_id = %s AND week_number = %s", (user_id, current_week))
        workout_json = cursor.fetchone()['workout_json']
        
        # Extract chronological existing workouts
        occupied_keys = sorted([k for k, v in workout_json.items() if k.startswith('Day_') and len(v) > 0], key=lambda x: int(x.split('_')[1]))
        current_workouts = [workout_json[k] for k in occupied_keys]
        
        # ---------------------------------------------------------
        # 🔄 THE SMART SWITCH (Rearrange vs. Regenerate)
        # ---------------------------------------------------------
        # ---------------------------------------------------------
        # 🔄 THE SMART SWITCH (Rearrange vs. Regenerate)
        # ---------------------------------------------------------
        proposed_json = {f"Day_{i}": [] for i in range(1, 8)} # Blank slate for BOTH paths

        if new_frequency == len(current_workouts):
            # NO FREQUENCY CHANGE: Just shift the existing workouts around
            for i, target_day_idx in enumerate(new_day_indices):
                proposed_json[f"Day_{target_day_idx}"] = current_workouts[i]
        
        else:
            # FREQUENCY CHANGE: Regenerate the program using the Core Pipeline!
            
            # 1. Fetch deep user data
            cursor.execute("""
                SELECT u.goal, u.experience_level as user_exp, u.workout_days, u.available_equipment, u.facility_type, u.injuries, u.duration_weeks,
                       e.weeks_in_program, e.active_phase as active_phase, e.last_assigned_split, e.split_rotation_index, e.last_workout_date
                FROM users u
                JOIN exercise_state e ON u.id = e.user_id
                WHERE u.id = %s
            """, (user_id,))
            row = cursor.fetchone()
            
            if not row:
                return jsonify({"error": "User or exercise state not found."}), 404

            # 2. Build Working Memory with the NEW schedule
            working_memory = {
                "user_id": user_id,
                "primary_goal": row['goal'],
                "experience_level": row['user_exp'],
                "facility_type": row['facility_type'],
                "owned_equipment": row['available_equipment'] or [],
                "medical_issues": row['injuries'] or [],
                "schedule": new_days_names, # <-- THIS TRIGGER THE NEW AI CALENDAR
                "preferred_duration_weeks": row['duration_weeks'], 
                "weeks_in_program": row['weeks_in_program'],
                "active_phase": row['active_phase'],
                "last_assigned_split": row['last_assigned_split'],
                "split_rotation_index": row['split_rotation_index'],
                "weeks_off": calculate_dynamic_weeks_off(row['last_workout_date'])
            }
            
            # 3. Determine Parameters
            active_phase = determine_active_phase(working_memory, macrocycle_kb)
            working_memory["active_phase"] = active_phase
            
            phase_params = phase_parameters_kb.get(active_phase, phase_parameters_kb["foundation"])
            base_split = phase_params.get("recommended_split", "full_body")
            
            assigned_split = determine_weekly_split(working_memory, base_split)
            working_memory["last_assigned_split"] = assigned_split

            calendar = schedule_weekly_blueprints(working_memory, assigned_split)
            
            # 4. Fetch history for the generator (Assuming you have a function or query for this)
            cursor.execute("""
                SELECT exercise_name, sets_completed, reps_achieved, weight_used
                FROM (
                    SELECT exercise_name, sets_completed, reps_achieved, weight_used,
                        ROW_NUMBER() OVER(PARTITION BY exercise_name ORDER BY log_date DESC) as rn
                    FROM workout_history
                    WHERE user_id = %s
                ) tmp 
                WHERE rn = 1;
            """, (user_id,))
            
            history_rows = cursor.fetchall()
            user_workout_history = {}
            for r in history_rows:
                user_workout_history[r['exercise_name']] = {
                    "sets": r['sets_completed'],
                    "reps_achieved": r['reps_achieved'],
                    "weight": r['weight_used']
                }
            
            # 5. Generate and assign the daily workouts directly into proposed_json
            for day_name, day_type in calendar.items():
                if day_type == "rest_day":
                    continue # Skip empty days
                    
                library_category = assigned_split.replace("_repeated", "").replace("_full", "")
                if day_type in ["upper_day", "lower_day"]: library_category = "upper_lower"
                elif day_type in ["push_day", "pull_day", "leg_day"]: library_category = "push_pull_legs"
                elif "full_body" in day_type: library_category = "full_body"
                
                blueprint = blueprint_library[library_category][day_type]
                
                daily_plan = generate_daily_workout(
                    working_memory, 
                    exercise_dataset, 
                    blueprint, 
                    phase_params, 
                    user_workout_history # Make sure this variable is defined!
                )
                
                day_index = {"Sunday":7, "Monday":1, "Tuesday":2, "Wednesday":3, "Thursday":4, "Friday":5, "Saturday":6}.get(day_name, 1)
                
                # Assign it directly to the master output
                proposed_json[f"Day_{day_index}"] = daily_plan
                
        # ---------------------------------------------------------
        # ---------------------------------------------------------

        # ---------------------------------------------------------
        # 🧠 FULL-WEEK CNS SAFETY AUDIT (Runs on BOTH cases!)
        # ---------------------------------------------------------
        def get_workout_category(workout):
            if not workout: return None
            upper = {'chest', 'lats', 'back', 'triceps', 'biceps', 'front_delts', 'side_delts', 'rear_delts', 'traps', 'shoulders'}
            lower = {'quads', 'hamstrings', 'glutes', 'calves'}
            has_u = has_l = False
            for ex in workout:
                targets = ex.get('muscle_data', {}).get('primary_targets', [])
                for t in targets:
                    if t in upper: has_u = True
                    if t in lower: has_l = True
            if has_u and has_l: return 'full_body'
            if has_u: return 'upper'
            if has_l: return 'lower'
            return 'core'

        for day_idx in new_day_indices:
            cat = get_workout_category(proposed_json[f"Day_{day_idx}"])
            if not cat or cat == 'core': continue
            
            for adj in [((day_idx - 2) % 7) + 1, (day_idx % 7) + 1]:
                adj_cat = get_workout_category(proposed_json[f"Day_{adj}"])
                if adj_cat and (adj_cat == cat or adj_cat == 'full_body' or cat == 'full_body'):
                    return jsonify({
                        "status": "conflict", 
                        "message": "This layout violates the 48-hour recovery rule. Heavy/Full-body days cannot be back-to-back."
                    })
        # ---------------------------------------------------------

        # Update the Database
        cursor.execute("""
            UPDATE generated_programs 
            SET workout_json = %s::jsonb 
            WHERE user_id = %s AND week_number = %s
        """, (json.dumps(proposed_json), user_id, current_week))
        
        conn.commit()
        return jsonify({"status": "success", "message": "Schedule optimized and safely saved!", "updated_program": proposed_json})

    except Exception as e:
        import traceback
        print("\n" + "="*50)
        print("🚨 CRASH IN EDIT_WEEK 🚨")
        traceback.print_exc() # This prints the exact line number and variable that failed!
        print("="*50 + "\n")
        
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/api/workout/check_status', methods=['GET'])
def check_workout_status():
    user_id = request.args.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # 1. Figure out exactly what day it is
        today_idx = datetime.datetime.today().weekday() + 1 # Monday=1, Sunday=7
        yesterday_idx = (today_idx - 2) % 7 + 1
        day_key = f"Day_{yesterday_idx}"
        
        #TESTING
        # day_key = "Day_1"     # Force it to look at Monday's JSON
        # planned_count_override = 5 
        # logged_count_override = 2
        
        # 2. Get the current week number from the user's state
        cursor.execute("SELECT weeks_in_program FROM exercise_state WHERE user_id = %s", (user_id,))
        state_record = cursor.fetchone()
        
        if not state_record:
            return jsonify({"status": "clear", "message": "No active program."})
            
        current_week = state_record['weeks_in_program']

        # =========================================================
        # 🛡️ THE WRAP-AROUND PROTECTOR 🛡️
        # =========================================================
        week_to_check = current_week
        
        if today_idx == 1: 
            # If today is Monday, yesterday was Sunday of LAST week!
            week_to_check = current_week - 1
            
        if week_to_check < 1:
            # If they just started Week 1 today (or changed schedules on Day 1), 
            # it is biologically impossible to have missed a workout yesterday.
            return jsonify({"status": "clear", "message": "Brand new program timeline. Clean slate!"})
        # =========================================================

        # 3. Fetch the program for the CORRECT week
        cursor.execute("""
            SELECT workout_json 
            FROM generated_programs 
            WHERE user_id = %s AND week_number = %s
        """, (user_id, week_to_check))
        record = cursor.fetchone()
        
        if not record or day_key not in record['workout_json']:
            return jsonify({"status": "clear", "message": "Yesterday was a rest day or no program found."})
            
        planned_workout = record['workout_json'][day_key]

        if len(planned_workout) == 0:
            return jsonify({"status": "clear", "message": "Missed workout was successfully resolved."})
        
        # 4. Check if they logged anything yesterday
        cursor.execute("""
            SELECT COUNT(*) as exercises_logged 
            FROM workout_history 
            WHERE user_id = %s AND log_date = CURRENT_DATE - INTERVAL '1 day'
        """, (user_id,))

        history = cursor.fetchone()
        logged_count = history['exercises_logged']
        planned_count = len(planned_workout)

        # 5. Determine the Intervention State
        if logged_count == 0:
            return jsonify({
                "status": "intervention_needed",
                "type": "missed_completely",
                "missed_day_key": day_key
            })
        elif logged_count < planned_count:
            return jsonify({
                "status": "intervention_needed",
                "type": "partial_completion",
                "missed_day_key": day_key
            })
            
        return jsonify({"status": "clear", "message": "Workout completed successfully."})

        #TESTING
        # if logged_count_override == 0:
        #     return jsonify({
        #         "status": "intervention_needed",
        #         "type": "missed_completely",
        #         "missed_day_key": day_key
        #     })
        # elif logged_count_override < planned_count_override:
        #     return jsonify({
        #         "status": "intervention_needed",
        #         "type": "partial_completion",
        #         "missed_day_key": day_key
        #     })  
        # return jsonify({"status": "clear", "message": "Workout completed successfully."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/workout/generate_week', methods=['POST'])
def generate_week():
    data = request.get_json(force=True)
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute("""
            SELECT exercise_name, sets_completed, reps_achieved, weight_used
            FROM (
                SELECT exercise_name, sets_completed, reps_achieved, weight_used,
                       ROW_NUMBER() OVER(PARTITION BY exercise_name ORDER BY log_date DESC) as rn
                FROM workout_history
                WHERE user_id = %s
            ) tmp 
            WHERE rn = 1;
        """, (user_id,))
        
        history_rows = cursor.fetchall()
        user_workout_history = {}
        for r in history_rows:
            user_workout_history[r['exercise_name']] = {
                "sets": r['sets_completed'],
                "reps_achieved": r['reps_achieved'],
                "weight": r['weight_used']
            }
        
        cursor.execute("""
            SELECT u.goal, u.experience_level as user_exp, u.workout_days, u.available_equipment, u.facility_type, u.injuries, u.duration_weeks,
                   e.weeks_in_program, e.active_phase, e.last_assigned_split, e.split_rotation_index, e.last_workout_date
            FROM users u
            JOIN exercise_state e ON u.id = e.user_id
            WHERE u.id = %s
        """, (user_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({"error": "User or exercise state not found."}), 404

        raw_schedule = row['workout_days']
        if isinstance(raw_schedule, list):
            user_schedule = raw_schedule
        elif isinstance(raw_schedule, str):
            user_schedule = [d.strip() for d in raw_schedule.split(',')]
        else:
            user_schedule = ["Monday", "Wednesday", "Friday"]

        working_memory = {
            "user_id": user_id,
            "primary_goal": row['goal'],
            "experience_level": row['user_exp'],
            "facility_type": row['facility_type'],
            "owned_equipment": row['available_equipment'] or [],
            "medical_issues": row['injuries'] or [],
            "schedule": user_schedule,
            "preferred_duration_weeks": row['duration_weeks'], # <-- THE MISSING LINK!
            "weeks_in_program": row['weeks_in_program'],
            "active_phase": row['active_phase'],
            "last_assigned_split": row['last_assigned_split'],
            "split_rotation_index": row['split_rotation_index'],
            "weeks_off": calculate_dynamic_weeks_off(row['last_workout_date'])
        }
        
        active_phase = determine_active_phase(working_memory, macrocycle_kb)
        working_memory["active_phase"] = active_phase
        
        phase_params = phase_parameters_kb.get(active_phase, phase_parameters_kb["foundation"])
        base_split = phase_params.get("recommended_split", "full_body")
        
        assigned_split = determine_weekly_split(working_memory, base_split)
        working_memory["last_assigned_split"] = assigned_split

        calendar = schedule_weekly_blueprints(working_memory, assigned_split)
        
        weekly_plan = {}
        for day_name, day_type in calendar.items():
            library_category = assigned_split.replace("_repeated", "").replace("_full", "")
            if day_type in ["upper_day", "lower_day"]: library_category = "upper_lower"
            elif day_type in ["push_day", "pull_day", "leg_day"]: library_category = "push_pull_legs"
            elif "full_body" in day_type: library_category = "full_body"
            
            blueprint = blueprint_library[library_category][day_type]
            
            daily_plan = generate_daily_workout(
                working_memory, 
                exercise_dataset, 
                blueprint, 
                phase_params, 
                user_workout_history
            )
            
            day_index = {"Sunday":7, "Monday":1, "Tuesday":2, "Wednesday":3, "Thursday":4, "Friday":5, "Saturday":6}.get(day_name, 1)
            weekly_plan[f"Day_{day_index}"] = daily_plan

        cursor.execute("""
            INSERT INTO generated_programs (user_id, week_number, workout_json) 
            VALUES (%s, %s, %s::jsonb)
            ON CONFLICT (user_id, week_number) 
            DO UPDATE SET workout_json = EXCLUDED.workout_json, generated_at = CURRENT_TIMESTAMP;
        """, (user_id, working_memory['weeks_in_program'], json.dumps(weekly_plan)))
        
        cursor.execute("""
            UPDATE exercise_state 
            SET 
                active_phase = %s, 
                last_assigned_split = %s, 
                split_rotation_index = %s, 
                current_goal = %s,
                preferred_duration_weeks = %s,
                program_ended = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = %s;
        """, (
            working_memory.get('active_phase'), 
            working_memory.get('last_assigned_split'), 
            working_memory.get('split_rotation_index'),
            working_memory.get('primary_goal'),             # <-- NEW: Handles Goal changes
            working_memory.get('preferred_duration_weeks'), # <-- NEW: Handles 4-week extensions
            working_memory.get('program_ended', False),     # <-- NEW: Resets the end flag
            user_id
        ))

        # Optional but highly recommended: Keep the `users` table synced if the engine changes their goal or duration
       # Optional but highly recommended: Keep the `users` table synced safely
        updated_goal = working_memory.get('primary_goal')
        updated_duration = working_memory.get('preferred_duration_weeks')
        
        if updated_goal and updated_duration:
            cursor.execute("""
                UPDATE users 
                SET goal = %s, duration_weeks = %s 
                WHERE id = %s
            """, (updated_goal, updated_duration, user_id))

        conn.commit()
        return jsonify({"status": "success", "program": weekly_plan}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()



@app.route('/api/workout/resolve_intervention', methods=['POST'])
def resolve_intervention():
    import json 
    
    data = request.json
    user_id = data.get('user_id')
    intervention_type = data.get('type') 
    missed_day_key = data.get('missed_day_key')
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        message = "No schedule changes were required."
        
        cursor.execute("SELECT weeks_in_program FROM exercise_state WHERE user_id = %s", (user_id,))
        current_week = cursor.fetchone()['weeks_in_program']
        
        cursor.execute("SELECT workout_json FROM generated_programs WHERE user_id = %s AND week_number = %s", (user_id, current_week))
        workout_json = cursor.fetchone()['workout_json']
        
        missed_workout = workout_json.get(missed_day_key, [])

        today_idx = datetime.datetime.today().weekday() + 1
        #TESTING
        # today_idx = 2
        
        occupied_days = sorted([
            int(k.split('_')[1]) for k, v in workout_json.items() 
            if k.startswith('Day_') and len(v) > 0 and k != missed_day_key
        ])

        # =========================================================
        # 🧠 THE AI COACHING BRAIN (CNS & MUSCLE OVERLAP CHECKER)
        # =========================================================
        def get_workout_category(workout):
            if not workout: return None
            upper_muscles = {'chest', 'lats', 'back', 'triceps', 'biceps', 'front_delts', 'side_delts', 'rear_delts', 'traps', 'lower_chest', 'shoulders'}
            lower_muscles = {'quads', 'hamstrings', 'glutes', 'calves'}
            has_upper = has_lower = False
            
            for ex in workout:
                targets = ex.get('muscle_data', {}).get('primary_targets', [])
                for t in targets:
                    if t in upper_muscles: has_upper = True
                    if t in lower_muscles: has_lower = True
                    
            if has_upper and has_lower: return 'full_body'
            if has_upper: return 'upper'
            if has_lower: return 'lower'
            return 'core'

        def is_safe_day(target_day_idx, workout_to_check, check_target_day=False):
            cat_to_check = get_workout_category(workout_to_check)
            if not cat_to_check or cat_to_check == 'core': return True 
            
            prev_day = ((target_day_idx - 2) % 7) + 1
            next_day = (target_day_idx % 7) + 1
            
            workouts_to_evaluate = [
                workout_json.get(f"Day_{prev_day}", []),
                workout_json.get(f"Day_{next_day}", [])
            ]
            
            if check_target_day:
                workouts_to_evaluate.append(workout_json.get(f"Day_{target_day_idx}", []))
                
            for w in workouts_to_evaluate:
                adj_cat = get_workout_category(w)
                if not adj_cat: continue
                if adj_cat == cat_to_check or adj_cat == 'full_body' or cat_to_check == 'full_body':
                    return False
            return True
        # =========================================================

        # ---------------------------------------------------------
        # SCENARIO 1: THE REST DAY SLIDE
        # ---------------------------------------------------------
        if intervention_type == 'slide':
            rest_days = [d for d in range(1, 8) if d >= today_idx and d not in occupied_days]
            safe_target_day = next((d for d in rest_days if is_safe_day(d, missed_workout, False)), None)
                    
            if safe_target_day:
                workout_json[f"Day_{safe_target_day}"] = missed_workout
                message = f"Workout safely moved to Day {safe_target_day}."
            else:
                return jsonify({"status": "conflict", "message": "Cannot shift safely without violating 48-hour muscle recovery rules."})

        # ---------------------------------------------------------
        # SCENARIO 2: CONSOLIDATE HEAVY LIFTS (UPGRADED)
        # ---------------------------------------------------------
        elif intervention_type == 'consolidate':
            primary_compounds = [
                ex for ex in missed_workout 
                if ex.get('muscle_data', {}).get('is_compound') == True
            ]
            
            if not primary_compounds:
                message = "No primary compounds found. Missed workout cleared."
            else:
                safe_target_day = None
                is_rest_day = False
                
                # Phase 1: Try to append to future EXISTING workout days safely
                future_occupied = [d for d in occupied_days if d >= today_idx]
                for o_day in future_occupied:
                    if is_safe_day(o_day, primary_compounds, check_target_day=True):
                        safe_target_day = o_day
                        break
                        
                # Phase 2: Fallback to scanning empty REST DAYS
                if not safe_target_day:
                    rest_days = [d for d in range(1, 8) if d >= today_idx and d not in occupied_days]
                    for r_day in rest_days:
                        if is_safe_day(r_day, primary_compounds, check_target_day=False):
                            safe_target_day = r_day
                            is_rest_day = True
                            break
                            
                # Execution
                if safe_target_day:
                    target_key = f"Day_{safe_target_day}"
                    if is_rest_day:
                        workout_json[target_key] = primary_compounds
                        message = f"Compounds successfully rescued to a safe rest day (Day {safe_target_day})."
                    else:
                        workout_json[target_key] = primary_compounds + workout_json[target_key]
                        message = f"Heavy lifts safely consolidated into your Day {safe_target_day} session."
                else:
                    return jsonify({"status": "conflict", "message": "Cannot consolidate safely without violating 48-hour muscle recovery rules."})

        # ---------------------------------------------------------
        # SCENARIO 3: SILENT TRIAGE (PARTIAL COMPLETION)
        # ---------------------------------------------------------
        elif intervention_type == 'triage_partial':
            cursor.execute("SELECT exercise_name FROM workout_history WHERE user_id = %s AND log_date = CURRENT_DATE - INTERVAL '1 day'", (user_id,))
            done_exercises = [row['exercise_name'] for row in cursor.fetchall()]
            
            skipped_exercises = [ex for ex in missed_workout if ex.get('exercise_name', ex.get('name')) not in done_exercises]
            rescued_compounds = [ex for ex in skipped_exercises if ex.get('muscle_data', {}).get('is_compound') == True]
            
            if not rescued_compounds:
                message = "No primary compounds were missed. Partial workout resolved."
            else:
                safe_target_day = None
                is_rest_day = False
                
                # Phase 1: Try to append to future EXISTING workout days safely
                future_occupied = [d for d in occupied_days if d >= today_idx]
                for o_day in future_occupied:
                    if is_safe_day(o_day, rescued_compounds, check_target_day=True):
                        safe_target_day = o_day
                        break
                        
                # Phase 2: Fallback to scanning empty REST DAYS
                if not safe_target_day:
                    rest_days = [d for d in range(1, 8) if d >= today_idx and d not in occupied_days]
                    for r_day in rest_days:
                        if is_safe_day(r_day, rescued_compounds, check_target_day=False):
                            safe_target_day = r_day
                            is_rest_day = True
                            break
                            
                # Execution
                if safe_target_day:
                    target_key = f"Day_{safe_target_day}"
                    if is_rest_day:
                        workout_json[target_key] = rescued_compounds
                        message = f"Partial workout triaged. Compounds safely moved to a rest day (Day {safe_target_day})."
                    else:
                        workout_json[target_key] = rescued_compounds + workout_json[target_key]
                        message = f"Partial workout triaged. Compounds safely added to Day {safe_target_day}."
                else:
                    # IMPORTANT: For automatic triage, we drop the volume but return SUCCESS, not CONFLICT.
                    message = "Could not safely shift missed compounds without violating recovery rules. Volume dropped."

        # ---------------------------------------------------------
        # THE LOOP BREAKER
        # ---------------------------------------------------------
        if missed_day_key in workout_json:
            workout_json[missed_day_key] = []

        cursor.execute("""
            UPDATE generated_programs 
            SET workout_json = %s::jsonb 
            WHERE user_id = %s AND week_number = %s
        """, (json.dumps(workout_json), user_id, current_week))
        
        conn.commit()
        return jsonify({"status": "success", "message": message, "updated_program": workout_json})

    except Exception as e:
        conn.rollback()
        print(f"🔥 FATAL RESOLUTION ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()



@app.route('/api/dashboard/user_data', methods=['GET'])
def get_dashboard_data():
    user_id = request.args.get('user_id')
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # 1. Fetch the user's current phase and their current week's workout plan
        cursor.execute("""
            SELECT e.active_phase, g.workout_json 
            FROM exercise_state e
            JOIN generated_programs g ON e.user_id = g.user_id AND e.weeks_in_program = g.week_number
            WHERE e.user_id = %s
        """, (user_id,))
        
        record = cursor.fetchone()
        
        if not record:
            return jsonify({"error": "User data not found"}), 404
            
        workout_json = record['workout_json']
        active_phase = record['active_phase'] 

        # 2. Map the "Day_X" keys to actual day names, ONLY if the day has exercises
        day_map = {
            1: "Monday", 2: "Tuesday", 3: "Wednesday", 
            4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"
        }
        
        current_week_days = []
        for key, exercises in workout_json.items():
            # Check if it's a day key and the array isn't empty (meaning it's not a rest day)
            if key.startswith('Day_') and isinstance(exercises, list) and len(exercises) > 0:
                day_num = int(key.split('_')[1])
                current_week_days.append(day_map[day_num])
                
        return jsonify({
            "status": "success",
            "active_phase": active_phase,
            "current_week_days": current_week_days
        })

    except Exception as e:
        print(f"Error fetching dashboard data: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/workout/today', methods=['GET'])
def get_today_workout():
    user_id = request.args.get('user_id')
    day_key = request.args.get('day_key') 
    
    if not user_id or not day_key:
        return jsonify({"error": "user_id and day_key are required"}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute("SELECT weeks_in_program FROM exercise_state WHERE user_id = %s", (user_id,))
        state_record = cursor.fetchone()
        
        if not state_record:
            return jsonify({"error": "User exercise state not found."}), 404
            
        current_week = state_record['weeks_in_program']
        
        cursor.execute("""
            SELECT workout_json FROM generated_programs 
            WHERE user_id = %s AND week_number = %s
        """, (user_id, current_week))
        program_record = cursor.fetchone()
        
        if not program_record:
            return jsonify({"error": "not_generated"}), 404
            
        raw_json = program_record['workout_json']
        
        if isinstance(raw_json, str):
            workout_json = json.loads(raw_json)
        else:
            workout_json = raw_json
            
        if day_key not in workout_json:
            return jsonify({
                "status": "success", 
                "is_rest_day": True, 
                "today_workout": None
            })
            
        return jsonify({
            "status": "success",
            "week_number": current_week,
            "is_rest_day": False,
            "today_workout": workout_json[day_key]
        })
        
    except Exception as e:
        print(f"Error in /api/workout/today: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/workout/regenerate_day', methods=['POST'])
def regenerate_day():
    data = request.json
    user_id = data.get('user_id')
    day_key = data.get('day_key') 
    day_name = data.get('day_name') 
    day_type = data.get('day_type') 
    temporary_equipment = data.get('temporary_equipment', [])
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute("""
            SELECT u.goal, u.experience_level, u.injuries, e.weeks_in_program, e.active_phase 
            FROM users u JOIN exercise_state e ON u.id = e.user_id WHERE u.id = %s
        """, (user_id,))
        row = cursor.fetchone()
        
        working_memory = {
            "primary_goal": row['goal'],
            "experience_level": row['experience_level'],
            "medical_issues": row['injuries'] or [],
            "weeks_in_program": row['weeks_in_program'],
            "active_phase": row['active_phase'],
            "available_equipment": temporary_equipment 
        }
        
        phase_params = phase_parameters_kb.get(row['active_phase'])
        
        library_category = "full_body"
        if day_type in ["upper_day", "lower_day"]: library_category = "upper_lower"
        elif day_type in ["push_day", "pull_day", "leg_day"]: library_category = "push_pull_legs"
        
        blueprint = blueprint_library[library_category][day_type]

        cursor.execute("""
            SELECT exercise_name, sets_completed, reps_achieved, weight_used
            FROM (
                SELECT exercise_name, sets_completed, reps_achieved, weight_used,
                       ROW_NUMBER() OVER(PARTITION BY exercise_name ORDER BY log_date DESC) as rn
                FROM workout_history
                WHERE user_id = %s
            ) tmp 
            WHERE rn = 1;
        """, (user_id,))
        
        history_rows = cursor.fetchall()
        user_workout_history = {}
        for r in history_rows:
            user_workout_history[r['exercise_name']] = {
                "sets": r['sets_completed'],
                "reps_achieved": r['reps_achieved'],
                "weight": r['weight_used']
            }
        
        new_daily_plan = generate_daily_workout(
            working_memory, 
            exercise_dataset, 
            blueprint, 
            phase_params, 
            user_workout_history
        )
        
        cursor.execute("SELECT workout_json FROM generated_programs WHERE user_id = %s AND week_number = %s", (user_id, row['weeks_in_program']))
        workout_json = cursor.fetchone()['workout_json']
        
        workout_json[day_key] = new_daily_plan
        
        cursor.execute("""
            UPDATE generated_programs SET workout_json = %s::jsonb, generated_at = CURRENT_TIMESTAMP
            WHERE user_id = %s AND week_number = %s
        """, (json.dumps(workout_json), user_id, row['weeks_in_program']))
        
        conn.commit()
        return jsonify({"status": "success", "updated_day": new_daily_plan})

    except Exception as e:
        conn.rollback()
        print(f"Error in regenerate_day: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/workout/complete', methods=['POST'])
def complete_workout():
    data = request.json
    user_id = data.get('user_id')
    exercises_completed = data.get('exercises', []) 
    
    conn = get_db_connection()
    cursor = conn.cursor() 
    
    try:
        cursor.execute("""
            UPDATE exercise_state 
            SET last_workout_date = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = %s
        """, (user_id,))
        
        insert_history_query = """
            INSERT INTO workout_history (user_id, exercise_name, sets_completed, reps_achieved, weight_used) 
            VALUES (%s, %s, %s, %s, %s)
        """
        history_records = [
            (user_id, ex.get('name'), ex.get('sets'), ex.get('reps'), ex.get('weight', 0.0))
            for ex in exercises_completed
        ]
        
        cursor.executemany(insert_history_query, history_records)
        conn.commit()
        
        return jsonify({"status": "success"})

    except Exception as e:
        conn.rollback() 
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ---------------------------------------------------------
# STRENGTH ANALYTICS ROUTE
# ---------------------------------------------------------
@app.route('/api/progress/strength', methods=['GET'])
def get_strength_progression():
    user_id = get_user_id_from_request(request)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
        
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get workout history ordered by date
        cursor.execute("""
            SELECT log_date, exercise_name, weight_used, reps_achieved
            FROM workout_history
            WHERE user_id = %s
            ORDER BY log_date ASC
        """, (user_id,))
        
        history = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # --- Advanced Benchmark Proxy Engine ---
        # Formula: Proxy 1RM * Multiplier = Benchmark 1RM
        PROXY_MAP = {
            "bench": {
                "barbell bench": 1.0, "bench press": 1.0, "machine chest press": 1.0,
                "dumbbell bench press": 2.2, "incline bench": 1.2, "chest press": 1.0,
            },
            "squat": {
                "barbell squat": 1.0, "hack squat": 0.8, "leg press": 0.5,
                "goblet squat": 1.5, "split squat": 2.0, "lunges": 2.2
            },
            "deadlift": {
                "deadlift": 1.0, "romanian deadlift": 1.1, "rdl": 1.1,
                "rack pull": 0.9, "back extension": 2.5, "good morning": 2.0
            },
            "ohp": {
                "overhead press": 1.0, "military press": 1.0,
                "dumbbell shoulder press": 2.2, "machine shoulder press": 1.0,
                "shoulder press": 1.0, "arnold press": 2.2
            }
        }
        
        daily_strength = {}
        for entry in history:
            # Safely handle dates
            log_date = entry['log_date']
            date_str = log_date.strftime('%Y-%m-%d') if hasattr(log_date, 'strftime') else str(log_date)[:10]
            
            ex_name = str(entry['exercise_name']).lower()
            weight = float(entry['weight_used'] or 0)
            reps = float(entry['reps_achieved'] or 0)
            
            if weight <= 0 or reps <= 0:
                continue
                
            # Brzycki / Epley 1RM formula
            calc_1rm = weight * (1 + reps / 30.0)
            
            if date_str not in daily_strength:
                daily_strength[date_str] = {"bench": None, "squat": None, "deadlift": None, "ohp": None}
                
            for benchmark, proxies in PROXY_MAP.items():
                for proxy_name, multiplier in proxies.items():
                    if proxy_name in ex_name:
                        est_benchmark_1rm = calc_1rm * multiplier
                        curr_est = daily_strength[date_str][benchmark]
                        # Save the highest estimate for the day
                        if curr_est is None or est_benchmark_1rm > curr_est:
                            daily_strength[date_str][benchmark] = round(est_benchmark_1rm, 1)
                        break 
        
        formatted_data = []
        last_known = {"bench": 0, "squat": 0, "deadlift": 0, "ohp": 0}
        
        for date_str in sorted(daily_strength.keys()):
            day_data = daily_strength[date_str]
            
            # Forward Fill missing data so the line charts don't break visually
            for bench_key in last_known.keys():
                if day_data[bench_key] is not None:
                    last_known[bench_key] = day_data[bench_key]
                else:
                    day_data[bench_key] = last_known[bench_key] if last_known[bench_key] > 0 else None
                    
            from datetime import datetime
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            
            formatted_data.append({
                "short_date": date_obj.strftime('%d %b'),
                "bench": day_data["bench"],
                "squat": day_data["squat"],
                "deadlift": day_data["deadlift"],
                "ohp": day_data["ohp"]
            })
            
        return jsonify({"strength_history": formatted_data})
        
    except Exception as e:
        print(f"🔥 STRENGTH PROGRESSION CRASH: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
