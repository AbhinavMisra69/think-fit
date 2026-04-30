# core/db.py
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load variables from your .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Opens a secure connection to the Neon database."""
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is missing from the .env file!")
    
    # RealDictCursor ensures SQL rows come back as standard Python dictionaries
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

class NutritionDatabase:
    """Handles all SQL interactions to keep your business logic perfectly clean."""
    
    @staticmethod
    def create_user_profile(profile: dict):
        """Inserts or updates the massive onboarding payload from Next.js + Zod."""
        query = """
            INSERT INTO users (
                id, weight_kg, height_cm, body_fat_pct, body_type,
                waist_cm, chest_cm, arm_cm, thigh_cm,
                primary_goals, workout_days, soreness_recovery, medical_conditions,
                workout_location, available_equipment,
                target_calories, target_protein, target_carbs, target_fat, sat_fat_limit
            ) VALUES (
                %(id)s, %(weight_kg)s, %(height_cm)s, %(body_fat_pct)s, %(body_type)s,
                %(waist_cm)s, %(chest_cm)s, %(arm_cm)s, %(thigh_cm)s,
                %(primary_goals)s, %(workout_days)s, %(soreness_recovery)s, %(medical_conditions)s,
                %(workout_location)s, %(available_equipment)s,
                %(target_calories)s, %(target_protein)s, %(target_carbs)s, %(target_fat)s, %(sat_fat_limit)s
            )
            ON CONFLICT (id) DO UPDATE SET
                weight_kg = EXCLUDED.weight_kg,
                body_fat_pct = EXCLUDED.body_fat_pct,
                target_calories = EXCLUDED.target_calories,
                target_protein = EXCLUDED.target_protein,
                target_carbs = EXCLUDED.target_carbs,
                target_fat = EXCLUDED.target_fat;
        """
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, profile)
            conn.commit()

    @staticmethod
    def get_user_targets(user_id: str) -> dict:
        """Fetches the user's customized macro goals."""
        query = "SELECT * FROM users WHERE id = %s;"
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id,))
                return cursor.fetchone()

    @staticmethod
    def get_daily_log(user_id: str, log_date) -> dict:
        """Fetches what the user has eaten today."""
        query = "SELECT * FROM daily_logs WHERE user_id = %s AND log_date = %s;"
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id, log_date))
                return cursor.fetchone()

    @staticmethod
    def upsert_daily_log(user_id: str, log_date, consumed: dict):
        """Creates a new daily log if it doesn't exist, or updates it if it does."""
        query = """
            INSERT INTO daily_logs 
                (user_id, log_date, consumed_calories, consumed_protein, consumed_carbs, consumed_fat, consumed_sat_fat)
            VALUES 
                (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id, log_date) 
            DO UPDATE SET 
                consumed_calories = EXCLUDED.consumed_calories,
                consumed_protein = EXCLUDED.consumed_protein,
                consumed_carbs = EXCLUDED.consumed_carbs,
                consumed_fat = EXCLUDED.consumed_fat,
                consumed_sat_fat = EXCLUDED.consumed_sat_fat;
        """
        values = (
            user_id, log_date, 
            consumed["calories"], consumed["protein_g"], 
            consumed["carbs_g"], consumed["fat_g"], consumed["sat_fat_g"]
        )
        
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
            conn.commit()