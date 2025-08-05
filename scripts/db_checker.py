import sqlite3
import os

# --- DATABASE PATH (should match your main script) ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, '..')
DB_PATH = os.path.join(PROJECT_ROOT, 'data', 'osrs_guide.db')

def view_quest_data(quest_name):
    """Connects to the database and prints all data for a specific quest."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Fetch the main quest details
        cursor.execute("SELECT * FROM quests WHERE name = ?", (quest_name,))
        quest_details = cursor.fetchone()

        if not quest_details:
            print(f"No data found for quest: '{quest_name}'")
            return

        print("\n" + "="*40)
        print(f"Data for: {quest_details[1]}")
        print("="*40)
        print(f"URL: {quest_details[2]}")
        print(f"Requirements: {quest_details[3]}")
        print(f"Items Required: {quest_details[4]}")
        print(f"Items Recommended: {quest_details[5]}")

        # Fetch the quest steps (tasks)
        print("\n--- Walkthrough Steps ---")
        cursor.execute("""
            SELECT step_number, description
            FROM tasks
            WHERE quest_id = ?
            ORDER BY step_number
        """, (quest_details[0],))
        tasks = cursor.fetchall()

        if tasks:
            for task in tasks:
                print(f"{task[0]}. {task[1]}")
        else:
            print("No walkthrough steps found for this quest.")

        conn.close()

    except sqlite3.OperationalError as e:
        print(f"An error occurred: {e}")
        print("Please ensure the main quest_parser.py script has been run successfully first.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # You can change this to any quest name you saw successfully parse
    view_quest_data("Cook's Assistant")
    view_quest_data("The Restless Ghost")
    view_quest_data("Dragon Slayer I")