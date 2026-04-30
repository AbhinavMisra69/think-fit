# seed_db.py
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def seed_database():
    if not DATABASE_URL:
        print("❌ Error: DATABASE_URL not found in .env file.")
        return

    print("🔌 Connecting to Neon Database...")
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # 1. Clean Slate (Drops tables if they exist to prevent conflicts)
        print("🧹 Wiping old tables...")
        cursor.execute("DROP TABLE IF EXISTS measurement_logs CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS daily_logs CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS users CASCADE;")

        # 2. Build the Schema
        print("🏗️  Building Schema...")
        schema_sql = """
        CREATE TABLE users (
            id VARCHAR(50) PRIMARY KEY,
            weight_kg FLOAT, height_cm FLOAT, body_fat_pct FLOAT, body_type VARCHAR(50),
            waist_cm FLOAT, chest_cm FLOAT, arm_cm FLOAT, thigh_cm FLOAT,
            primary_goals TEXT[], workout_days VARCHAR(50), soreness_recovery VARCHAR(50),
            medical_conditions TEXT[], workout_location VARCHAR(50), available_equipment TEXT[],
            target_calories INT NOT NULL, target_protein INT NOT NULL, target_carbs INT NOT NULL,
            target_fat INT NOT NULL, sat_fat_limit INT NOT NULL
        );

        CREATE TABLE daily_logs (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(50) REFERENCES users(id) ON DELETE CASCADE,
            log_date DATE NOT NULL DEFAULT CURRENT_DATE,
            consumed_calories INT DEFAULT 0, consumed_protein FLOAT DEFAULT 0,
            consumed_carbs FLOAT DEFAULT 0, consumed_fat FLOAT DEFAULT 0, consumed_sat_fat FLOAT DEFAULT 0,
            UNIQUE(user_id, log_date) 
        );

        CREATE TABLE measurement_logs (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(50) REFERENCES users(id) ON DELETE CASCADE,
            log_date DATE NOT NULL DEFAULT CURRENT_DATE,
            weight_kg FLOAT, body_fat_pct FLOAT,
            waist_cm FLOAT, chest_cm FLOAT, arm_cm FLOAT, thigh_cm FLOAT,
            UNIQUE(user_id, log_date)
        );
        """
        cursor.execute(schema_sql)

        # 3. Insert the Test User Profile
        print("👤 Injecting Test User Profile (user_123)...")
        user_sql = """
        INSERT INTO users (
            id, target_calories, target_protein, target_carbs, target_fat, sat_fat_limit,
            weight_kg, height_cm, body_fat_pct,
            waist_cm, chest_cm, arm_cm, thigh_cm,
            primary_goals, workout_days, soreness_recovery, workout_location
        ) VALUES (
            'user_123', 2103, 115, 298, 50, 23,
            72.0, 175.0, 15.0,
            81.5, 99.0, 35.0, 59.5,
            ARRAY['fat_loss', 'muscle_gain'], '4_days', 'average', 'pro_gym'
        );
        """
        cursor.execute(user_sql)

        # 4. Insert 4 Weeks of Historical Data
        print("📈 Injecting 4 weeks of progress history...")
        history_sql = """
        INSERT INTO measurement_logs (user_id, log_date, weight_kg, body_fat_pct, waist_cm, chest_cm, arm_cm, thigh_cm)
        VALUES
        ('user_123', CURRENT_DATE - INTERVAL '28 days', 75.0, 16.5, 84.0, 98.0, 34.0, 58.0),
        ('user_123', CURRENT_DATE - INTERVAL '21 days', 74.2, 16.0, 83.0, 98.5, 34.5, 58.5),
        ('user_123', CURRENT_DATE - INTERVAL '14 days', 73.1, 15.5, 82.0, 99.0, 35.0, 59.0),
        ('user_123', CURRENT_DATE - INTERVAL '7 days',  72.5, 15.2, 81.5, 99.0, 35.0, 59.5);
        """
        cursor.execute(history_sql)

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Database perfectly seeded! Refresh your Next.js dashboard.")

    except Exception as e:
        print(f"❌ Database seeding failed: {e}")

if __name__ == "__main__":
    seed_database()