# setup_db.py
import os
import psycopg2
from dotenv import load_dotenv

# 1. Load the connection string from your .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def setup_database():
    if not DATABASE_URL:
        print("❌ Error: DATABASE_URL not found in .env file.")
        return

    print("🔌 Connecting to Neon Database...")
    
    try:
        # 2. Connect to the database
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # 3. Write the SQL Commands
        create_tables_sql = """
        -- Create Users Table with the ML and Zod Form Fields
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(50) PRIMARY KEY,
            weight_kg FLOAT,
            height_cm FLOAT,
            body_fat_pct FLOAT,
            body_type VARCHAR(50),
            
            -- Tape Measurements
            waist_cm FLOAT,
            chest_cm FLOAT,
            arm_cm FLOAT,
            thigh_cm FLOAT,
            
            -- Zod Form Arrays and Preferences
            primary_goals TEXT[],
            workout_days VARCHAR(50),
            soreness_recovery VARCHAR(50),
            medical_conditions TEXT[],
            workout_location VARCHAR(50),
            available_equipment TEXT[],
            
            -- Calculated Targets
            target_calories INT NOT NULL,
            target_protein INT NOT NULL,
            target_carbs INT NOT NULL,
            target_fat INT NOT NULL,
            sat_fat_limit INT NOT NULL
        );

        -- Create Daily Logs Table
        CREATE TABLE IF NOT EXISTS daily_logs (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(50) REFERENCES users(id) ON DELETE CASCADE,
            log_date DATE NOT NULL,
            consumed_calories INT DEFAULT 0,
            consumed_protein FLOAT DEFAULT 0,
            consumed_carbs FLOAT DEFAULT 0,
            consumed_fat FLOAT DEFAULT 0,
            consumed_sat_fat FLOAT DEFAULT 0,
            UNIQUE(user_id, log_date) 
        );
        """

        # 4. Insert the test user
        insert_test_user_sql = """
        INSERT INTO users (
            id, target_calories, target_protein, target_carbs, target_fat, sat_fat_limit,
            weight_kg, height_cm, body_fat_pct
        )
        VALUES (
            'user_123', 2103, 115, 298, 50, 23,
            72.0, 175.0, 15.0
        )
        ON CONFLICT (id) DO NOTHING;
        """

        # 5. Execute and Commit
        print("🏗️  Building Tables...")
        cursor.execute(create_tables_sql)
        
        print("👤 Injecting Test User (user_123)...")
        cursor.execute(insert_test_user_sql)
        
        conn.commit()
        
        cursor.close()
        conn.close()
        print("✅ Database setup complete! Neon is officially connected and ready.")

    except Exception as e:
        print(f"❌ Database connection failed: {e}")

if __name__ == "__main__":
    setup_database()