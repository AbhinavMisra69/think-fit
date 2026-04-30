# update_db.py
import os
import psycopg2
from dotenv import load_dotenv

# Load the connection string
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def update_database():
    print("🔌 Connecting to Neon Database...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # 1. Create the History Table
        create_history_table = """
        CREATE TABLE IF NOT EXISTS measurement_logs (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(50) REFERENCES users(id) ON DELETE CASCADE,
            log_date DATE NOT NULL DEFAULT CURRENT_DATE,
            weight_kg FLOAT,
            body_fat_pct FLOAT,
            waist_cm FLOAT,
            chest_cm FLOAT,
            arm_cm FLOAT,
            thigh_cm FLOAT,
            UNIQUE(user_id, log_date)
        );
        """

        # 2. Inject 4 weeks of test data so your charts look amazing immediately
        seed_data = """
        INSERT INTO measurement_logs (user_id, log_date, weight_kg, body_fat_pct, waist_cm, chest_cm, arm_cm, thigh_cm)
        VALUES
        ('user_123', CURRENT_DATE - INTERVAL '28 days', 75.0, 16.5, 84.0, 98.0, 34.0, 58.0),
        ('user_123', CURRENT_DATE - INTERVAL '21 days', 74.2, 16.0, 83.0, 98.5, 34.5, 58.5),
        ('user_123', CURRENT_DATE - INTERVAL '14 days', 73.1, 15.5, 82.0, 99.0, 35.0, 59.0),
        ('user_123', CURRENT_DATE - INTERVAL '7 days',  72.5, 15.2, 81.5, 99.0, 35.0, 59.5)
        ON CONFLICT (user_id, log_date) DO NOTHING;
        """

        print("🏗️  Building measurement_logs table...")
        cursor.execute(create_history_table)
        
        print("📈 Injecting 4 weeks of historical test data...")
        cursor.execute(seed_data)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Database successfully upgraded! You are ready for charts.")

    except Exception as e:
        print(f"❌ Database update failed: {e}")

if __name__ == "__main__":
    update_database()