import sqlite3
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, '..')
DB_PATH = os.path.join(PROJECT_ROOT, 'data', 'osrs_guide.db')

def check_database():
    """Connects to the DB and prints some sample data."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check quests table
        cursor.execute("SELECT COUNT(*) FROM quests;")
        quest_count = cursor.fetchone()[0]
        print(f"✅ Found {quest_count} quests in the database.")

        # Check tasks table
        cursor.execute("SELECT COUNT(*) FROM tasks;")
        task_count = cursor.fetchone()[0]
        print(f"✅ Found {task_count} quest descriptions in the database.")

        # Print the first 5 quests as a sample
        print("\n--- Sample Quests ---")
        cursor.execute("SELECT name FROM quests LIMIT 5;")
        for row in cursor.fetchall():
            print(row[0])

        conn.close()

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    check_database()