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
from core.planning import AdaptiveCoach 


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

@app.route('/api/progress/update', methods=['POST'])
def update_progress():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "No valid login token found"}), 401
    
    token = auth_header.split(" ")[1]

    try:
        # 1. Authenticate User
        decoded = jwt.decode(token, os.environ.get("JWT_SECRET"), algorithms=["HS256"])
        user_id = decoded.get('id')
        data = request.json
        
        # 2. Extract incoming measurements
        current_weight = float(data.get('weight') or 0)
        current_waist = float(data.get('waist') or 0)
        current_chest = float(data.get('chest') or 0)
        current_arm = float(data.get('arm') or 0)
        current_thigh = float(data.get('thigh') or 0)
        
        # Calculate new body fat % using the ML engine
        # We need gender, height, neck, hip from the users table first!
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute("""
            SELECT gender, height_cm, neck, hip, goal, target_calories, weight_kg, body_fat_pct 
            FROM users WHERE id = %s
        """, (user_id,))
        user_data = cur.fetchone()
        
        if not user_data:
            return jsonify({"error": "User profile not found"}), 404

        # Calculate new BF%
        current_bf_pct = PhysiqueAnalyzer.predict_body_fat(
            user_data['gender'], current_weight, user_data['height_cm'], 
            current_waist, user_data['neck'], current_chest, current_arm, user_data['hip']
        )

        # 3. Save the new log to the database
        cur.execute("""
            INSERT INTO measurement_logs 
            (user_id, weight_kg, body_fat_pct, waist_cm, chest_cm, arm_cm, thigh_cm)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, log_date
        """, (user_id, current_weight, current_bf_pct, current_waist, current_chest, current_arm, current_thigh))
        
        # 4. Fetch the PREVIOUS log (the one right before this new one)
        cur.execute("""
            SELECT weight_kg, body_fat_pct, waist_cm, chest_cm, arm_cm, thigh_cm 
            FROM measurement_logs 
            WHERE user_id = %s 
            ORDER BY log_date DESC 
            OFFSET 1 LIMIT 1
        """, (user_id,))
        prev_log = cur.fetchone()

        coach_result = None

        # 5. Run the Adaptive Coach (ONLY if we have a previous log to compare against)
        if prev_log:
            prev_measurements = {
                "waist_cm": prev_log['waist_cm'] or 0,
                "chest_cm": prev_log['chest_cm'] or 0,
                "arm_cm": prev_log['arm_cm'] or 0,
                "thigh_cm": prev_log['thigh_cm'] or 0
            }
            
            curr_measurements = {
                "waist_cm": current_waist,
                "chest_cm": current_chest,
                "arm_cm": current_arm,
                "thigh_cm": current_thigh
            }

            coach_result = AdaptiveCoach.weekly_check_in(
                previous_weight=prev_log['weight_kg'] or user_data['weight_kg'], 
                current_weight=current_weight, 
                previous_bf_pct=prev_log['body_fat_pct'] or user_data['body_fat_pct'], 
                current_bf_pct=current_bf_pct,
                previous_measurements=prev_measurements, 
                current_measurements=curr_measurements,
                current_daily_cals=user_data['target_calories'], 
                goal=user_data['goal'], 
                expected_loss_rate="moderate" # You can make this dynamic later
            )

            # 6. Apply Coach Adjustments to the Users Table
            if coach_result['adjustment_made']:
                new_cals = coach_result['new_daily_calories']
                # Recalculate macros based on new calories (assuming you have this function)
                # For now, we will just update the calories
                cur.execute("""
                    UPDATE users 
                    SET target_calories = %s,
                        weight_kg = %s,
                        body_fat_pct = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (new_cals, current_weight, current_bf_pct, user_id))
            else:
                # Just update the latest stats
                cur.execute("""
                    UPDATE users 
                    SET weight_kg = %s,
                        body_fat_pct = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (current_weight, current_bf_pct, user_id))
                
        else:
            # First log ever, just update users table with latest weight/bf
            cur.execute("""
                UPDATE users 
                SET weight_kg = %s, body_fat_pct = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (current_weight, current_bf_pct, user_id))

        conn.commit()
        cur.close()
        conn.close()

        # 7. Return the data, including the coach's feedback so React can show it!
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
    app.run(host='0.0.0.0', port=5001, debug=True)