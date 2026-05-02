import os
import csv
import traceback
from datetime import date, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import pytesseract
import jwt
# Core Module Imports
from core.db import get_db_connection, NutritionDatabase
from core.ml_engine import PhysiqueAnalyzer
from core.tracking import DailyTracker
from core.nutrition import NutritionCalculator
from core.ocr_engine import PackagedFoodEngine
import psycopg2
from psycopg2.extras import RealDictCursor
from core.planning import AdaptiveCoach 
import json


app = Flask(__name__)
CORS(app) # Crucial: Allows Next.js to talk to Flask

# Temporary folder for CV scanner image uploads
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
import os
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS
# Ensure your import matches your folder structure
from core.ml_engine import PhysiqueAnalyzer 

app = Flask(__name__)
CORS(app)

@app.route('/api/calculate_bf', methods=['POST'])
def calculate_bf():
    data = request.json
    try:
        # Cast to float immediately to prevent math errors
        gender = data.get('gender', 'male')
        height = float(data.get('height', 0))
        weight = float(data.get('weight', 0))
        waist = float(data.get('waist', 0))
        neck = float(data.get('neck', 0))
        chest = float(data.get('chest', 0))
        arm = float(data.get('arm', 0))
        hip = float(data.get('hip', 0))
        
        # Debug print to see if numbers are reaching the engine
        print(f"Calculating for: W:{waist} N:{neck} H:{height}")

        bf_percentage = PhysiqueAnalyzer.predict_body_fat(
            gender, weight, height, waist, neck, chest, arm, hip
        )
        
        return jsonify({"body_fat_percentage": bf_percentage}), 200
    except Exception as e:
        print(f"BF Calculation Error: {e}")
        return jsonify({"error": str(e)}), 400

@app.route('/api/onboarding', methods=['POST'])
def save_onboarding():
    data = request.json
    
    # Grab the user_id straight from the frontend JSON payload
    user_id = data.get('userId')
    
    if not user_id:
        return jsonify({"error": "User ID is missing. User not logged in."}), 400

    try:
        # Define all variables
        gender = data.get('gender')
        weight = float(data.get('weight') or 0)
        height = float(data.get('height') or 0)
        neck = float(data.get('neck') or 0)
        waist = float(data.get('waist') or 0)
        chest = float(data.get('chest') or 0)
        arm = float(data.get('arm') or 0)
        hip = float(data.get('hip') or 0)
        
        body_type = data.get('bodyType')
        activity_level = data.get('activityLevel')
        experience_level = data.get('experienceLevel')
        
        days_available = int(data.get('workoutDays') or 4)
        facility_type = data.get('workoutLocation')
        soreness_recovery = data.get('soreness')
        
        medical_conditions = data.get('medicalConditions', [])
        available_equipment = data.get('availableEquipment', [])
        
        # Get the array from React, but only save the primary choice to the 'goal' column
        primary_goals = data.get('primaryGoals', [])
        goal_main = primary_goals[0] if primary_goals else 'recomposition'
        
        bf_pct = float(data.get('estimatedBF') or 15.0)

        # Connect to Database
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cur = conn.cursor()

        # EXACTLY 19 COLUMNS MATCHING YOUR SCHEMA. NO 'primary_goals' COLUMN.
        insert_query = """
        INSERT INTO users (
            id, gender, weight_kg, height_cm, neck, waist_cm, chest_cm, arm_cm, hip, 
            body_type, activity_level, experience_level, days_available, facility_type, 
            soreness_recovery, medical_conditions, available_equipment, goal, body_fat_pct
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
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
            facility_type = EXCLUDED.facility_type,
            soreness_recovery = EXCLUDED.soreness_recovery,
            medical_conditions = EXCLUDED.medical_conditions,
            available_equipment = EXCLUDED.available_equipment,
            goal = EXCLUDED.goal,
            updated_at = CURRENT_TIMESTAMP;
        """
        
        # EXACTLY 19 VARIABLES.
        cur.execute(insert_query, (
            user_id, gender, weight, height, neck, waist, chest, arm, hip,
            body_type, activity_level, experience_level, days_available, facility_type,
            soreness_recovery, medical_conditions, available_equipment, goal_main, bf_pct
        ))

        cur.execute("""
        INSERT INTO measurement_logs 
        (user_id, weight_kg, body_fat_pct, waist_cm, chest_cm, arm_cm)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (
        user_id, 
        weight, 
        bf_pct, 
        waist, 
        chest, 
        arm, 
        ))

        conn.commit()
        
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"status": "success", "message": "Profile synced successfully"}), 200

    except Exception as e:
        print(f"🔥 Database Error: {e}")
        return jsonify({"error": str(e)}), 500
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

@app.route('/api/progress/update', methods=['POST'])
def update_progress():
    session_str = request.headers.get('X-Session')
    if not session_str:
        return jsonify({"error": "No valid login session found"}), 401

    try:
        session_data = json.loads(session_str)
        user_id = session_data.get('id')
        data = request.json
        
        # 1. Bulletproof the incoming React data
        current_weight = safe_float(data.get('weight'))
        current_waist = safe_float(data.get('waist'))
        current_chest = safe_float(data.get('chest'))
        current_arm = safe_float(data.get('arm'))
        current_thigh = safe_float(data.get('thigh')) # Safely handles the missing thigh data!
        
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute("""
            SELECT gender, height_cm, neck, hip, goal, target_calories, weight_kg, body_fat_pct 
            FROM users WHERE id = %s
        """, (user_id,))
        user_data = cur.fetchone()
        
        if not user_data:
            return jsonify({"error": "User profile not found"}), 404

        # 2. Bulletproof the Database strings (Fixes the .lower() error!)
        db_gender = safe_str(user_data.get('gender'), default="male")
        db_goal = safe_str(user_data.get('goal'), default="maintain")

        # 3. Bulletproof the Database numbers
        db_height = safe_float(user_data.get('height_cm'))
        db_neck = safe_float(user_data.get('neck'))
        db_hip = safe_float(user_data.get('hip'))
        db_weight = safe_float(user_data.get('weight_kg'))
        db_bf_pct = safe_float(user_data.get('body_fat_pct'))

        # Calculate new BF% using the perfectly sanitized data
        current_bf_pct = PhysiqueAnalyzer.predict_body_fat(
            db_gender, current_weight, db_height, 
            current_waist, db_neck, current_chest, current_arm, db_hip
        )

        # Save the new log
        cur.execute("""
            INSERT INTO measurement_logs 
            (user_id, weight_kg, body_fat_pct, waist_cm, chest_cm, arm_cm, thigh_cm)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, log_date
        """, (user_id, current_weight, current_bf_pct, current_waist, current_chest, current_arm, current_thigh))
        
        # Fetch the PREVIOUS log
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
            # Bulletproof the previous measurements (safely handling your NULL onboarding thigh)
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

            # Pass everything cleanly into the Coach
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

            # Apply Coach Adjustments
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
    # Read custom session header
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
        # Assuming you have a get_db_connection() helper defined
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cursor.execute(query, (user_id,))
        history = cursor.fetchall()
        
        # Convert rows to dicts for JSON serialization
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
    

# ---------------------------------------------------------
# WORKOUT EXPERT ROUTES
# ---------------------------------------------------------

# 1. Figure out exactly where we are on the computer
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Build the path to the JSON file
EXERCISE_DATA_PATH = os.path.join(BASE_DIR, 'data', 'exercises_enriched.json')
CORS(app, resources={r"/api/*": {"origins": "*"}})

# 3. Load the file into a Python dictionary
try:
    with open(EXERCISE_DATA_PATH, 'r') as f:
        exercise_dataset = json.load(f)
    print(f"Successfully loaded {len(exercise_dataset)} exercises from JSON.")
except FileNotFoundError:
    print(f"CRITICAL ERROR: Could not find {EXERCISE_DATA_PATH}. Make sure the file exists!")
    exercise_dataset = {} # Fallback to prevent immediate crashes


DATABASE_URL = os.environ.get("DATABASE_URL")


# def get_db_connection():
#     """Helper function to get a database connection."""
#     conn = psycopg2.connect(DATABASE_URL)
#     return conn

def get_db_connection():
    print("\n" + "="*50)
    print("🔄 TEST: Attempting database connection...")
    
    # Check if the URL is even loaded
    url = os.environ.get("DATABASE_URL")
    if not url:
        print("❌ FATAL: Python cannot find DATABASE_URL. It is None.")

    try:
        # The actual connection attempt
        conn = psycopg2.connect(url)
        print("✅ SUCCESS: Connected to the Neon database perfectly!")
        print("="*50 + "\n")
        return conn
        
    except Exception as e:
        # If it crashes, catch it and print the exact reason
        print("❌ FAILED: The connection crashed.")
        print(f"⚠️ Exact Error: {e}")
        print("="*50 + "\n")
        raise e
    
@app.route('/api/debug/both_columns', methods=['GET'])
def debug_both_columns():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("""
        SELECT table_name, column_name 
        FROM information_schema.columns 
        WHERE table_name IN ('users', 'exercise_state')
        ORDER BY table_name, ordinal_position
    """)
    columns = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"columns": columns})



@app.route('/api/workout/generate_week', methods=['POST'])
def generate_week():
    #data = request.json
    data = request.get_json(force=True)  # force=True ignores Content-Type header
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
        # ---------------------------------------------------------
        
        cursor.execute("""
            SELECT u.goal, u.experience_level as user_exp, u.workout_days, u.available_equipment, u.facility_type, u.injuries,
                   e.weeks_in_program, e.active_phase, e.last_assigned_split, e.split_rotation_index, e.last_workout_date
            FROM users u
            JOIN exercise_state e ON u.id = e.user_id
            WHERE u.id = %s
        """, (user_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({"error": "User or exercise state not found."}), 404

        # Convert the VARCHAR schedule "Monday,Tuesday" into a Python list
        raw_schedule = row['workout_days']
        if isinstance(raw_schedule, list):
            user_schedule = raw_schedule
        elif isinstance(raw_schedule, str):
            user_schedule = [d.strip() for d in raw_schedule.split(',')]
        else:
            user_schedule = ["Monday", "Wednesday", "Friday"]  # fallback

        # 2. CONSTRUCT WORKING MEMORY
        working_memory = {
            "user_id": user_id,
            "primary_goal": row['goal'],
            "experience_level": row['user_exp'],
            "facility_type": row['facility_type'],
            "owned_equipment": row['available_equipment'] or [],
            "medical_issues": row['injuries'] or [],
            "schedule": user_schedule,
            "weeks_in_program": row['weeks_in_program'],
            "active_phase": row['active_phase'],
            "last_assigned_split": row['last_assigned_split'],
            "split_rotation_index": row['split_rotation_index'],
            "weeks_off": calculate_dynamic_weeks_off(row['last_workout_date'])
        }
        
        # 3. RUN THE ENGINE PIPELINE EXACTLY AS YOU WROTE IT
        active_phase = determine_active_phase(working_memory, macrocycle_kb)
        working_memory["active_phase"] = active_phase
        
        phase_params = phase_parameters_kb.get(active_phase, phase_parameters_kb["foundation"])
        base_split = phase_params.get("recommended_split", "full_body")
        
        # Adapt split to days available
        assigned_split = determine_weekly_split(working_memory, base_split)
        working_memory["last_assigned_split"] = assigned_split

        
        # Schedule the blueprints (passing the 2 required arguments)
        calendar = schedule_weekly_blueprints(working_memory, assigned_split)
        
        # 4. GENERATE DAILY WORKOUTS
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
            
            # Map "Monday" back to "Day_1" format for your frontend, or use day_name directly
            day_index = {"Sunday":7, "Monday":1, "Tuesday":2, "Wednesday":3, "Thursday":4, "Friday":5, "Saturday":6}.get(day_name, 1)
            weekly_plan[f"Day_{day_index}"] = daily_plan

        # 5. SAVE TO DATABASE
        cursor.execute("""
            INSERT INTO generated_programs (user_id, week_number, workout_json) 
            VALUES (%s, %s, %s::jsonb)
            ON CONFLICT (user_id, week_number) 
            DO UPDATE SET workout_json = EXCLUDED.workout_json, generated_at = CURRENT_TIMESTAMP;
        """, (user_id, working_memory['weeks_in_program'], json.dumps(weekly_plan)))
        
        cursor.execute("""
            UPDATE exercise_state 
            SET active_phase = %s, last_assigned_split = %s, split_rotation_index = %s, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = %s;
        """, (working_memory['active_phase'], working_memory['last_assigned_split'], working_memory['split_rotation_index'], user_id))
        
        conn.commit()
        return jsonify({"status": "success", "program": weekly_plan}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()



import json
from flask import request, jsonify
# Make sure RealDictCursor is imported at the top of your app.py

@app.route('/api/workout/today', methods=['GET'])
def get_today_workout():
    user_id = request.args.get('user_id')
    day_key = request.args.get('day_key') 
    
    if not user_id or not day_key:
        return jsonify({"error": "user_id and day_key are required"}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # 1. Fetch the user's current week
        cursor.execute("SELECT weeks_in_program FROM exercise_state WHERE user_id = %s", (user_id,))
        state_record = cursor.fetchone()
        
        if not state_record:
            return jsonify({"error": "User exercise state not found."}), 404
            
        current_week = state_record['weeks_in_program']
        
        # 2. Fetch the generated program for that week
        cursor.execute("""
            SELECT workout_json FROM generated_programs 
            WHERE user_id = %s AND week_number = %s
        """, (user_id, current_week))
        program_record = cursor.fetchone()
        
        if not program_record:
            return jsonify({"error": "not_generated"}), 404
            
        raw_json = program_record['workout_json']
        
        # 3. SAFETY CHECK: Ensure it is a dictionary, not a string
        if isinstance(raw_json, str):
            workout_json = json.loads(raw_json)
        else:
            workout_json = raw_json
            
        # 4. Check if today is a rest day
        if day_key not in workout_json:
            return jsonify({
                "status": "success", 
                "is_rest_day": True, 
                "today_workout": None
            })
            
        # 5. Return the workout
        return jsonify({
            "status": "success",
            "week_number": current_week,
            "is_rest_day": False,
            "today_workout": workout_json[day_key]
        })
        
    except Exception as e:
        # THE FIX: Catch the error and return it cleanly to React
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
        # 1. Fetch exact same fusion of state
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

        # --- THE MISSING FIX: FETCH HISTORY BEFORE GENERATING ---
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
        # ---------------------------------------------------------
        
        # 3. Generate the single day (NOW WITH ALL 5 ARGUMENTS!)
        new_daily_plan = generate_daily_workout(
            working_memory, 
            exercise_dataset, 
            blueprint, 
            phase_params, 
            user_workout_history
        )
        
        # 4. Fetch, Update, and Save JSONB
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
        # Reset the detraining clock in the dynamic state table
        cursor.execute("""
            UPDATE exercise_state 
            SET last_workout_date = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = %s
        """, (user_id,))
        
        # Save the historical data for the progression engine
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



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)