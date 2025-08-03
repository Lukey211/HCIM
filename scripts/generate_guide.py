import sqlite3
import json
import os

# --- DATABASE PATH ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, '..')
DB_PATH = os.path.join(PROJECT_ROOT, 'data', 'osrs_guide.db')
OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'output', 'hcim_guide.json')


class GuideGenerator:
    def __init__(self):
        """Initializes the Guide Generator, connecting to the database."""
        self.conn = self.get_db_connection()
        self.player_state = self.initialize_player_state()
        self.all_tasks = self.load_all_tasks_from_db() # This will now be populated
        self.guide = []

    def get_db_connection(self):
        """Establishes a connection to the SQLite database."""
        if not os.path.exists(DB_PATH):
            print(f"❌ Database file not found at {DB_PATH}. Please run db_loader.py first.")
            return None
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            print("✅ Successfully connected to the SQLite database.")
            return conn
        except sqlite3.Error as e:
            print(f"❌ Database connection error: {e}")
            return None

    def initialize_player_state(self):
        """Sets up the initial state for a new level 3 account."""
        return {
            "skills": { "attack": 1, "strength": 1, "defence": 1, "hitpoints": 10, "ranged": 1, "magic": 1, "prayer": 1, "cooking": 1, "woodcutting": 1, "fletching": 1, "fishing": 1, "firemaking": 1, "crafting": 1, "smithing": 1, "mining": 1, "herblore": 1, "agility": 1, "thieving": 1, "slayer": 1, "farming": 1, "runecraft": 1, "hunter": 1, "construction": 1 },
            "completed_quests": [],
            "inventory": [],
            "bank": [],
            "current_location": {"x": 3222, "y": 3218, "plane": 0}
        }

    def load_all_tasks_from_db(self):
        """
        Loads all quest steps from the database into a list of task dictionaries.
        """
        print("Loading all tasks from the database...")
        if not self.conn:
            return []
            
        cursor = self.conn.cursor()
        
        # Query to join quests and tasks to get all data
        cursor.execute("""
            SELECT
                t.task_id,
                q.name AS quest_name,
                t.step_number,
                t.description
            FROM tasks t
            JOIN quests q ON t.quest_id = q.quest_id
            ORDER BY q.name, t.step_number;
        """)
        
        tasks_from_db = cursor.fetchall()
        
        # Convert the database rows into a list of dictionaries for easier use
        tasks = [dict(row) for row in tasks_from_db]
        
        print(f"✅ Loaded {len(tasks)} tasks from the database.")
        
        # --- PROOF OF CONCEPT ---
        # Let's print the first task we loaded to prove it's working.
        if tasks:
            print("\n--- Sample Task Loaded ---")
            print(f"Quest: {tasks[0]['quest_name']}")
            print(f"Step {tasks[0]['step_number']}: {tasks[0]['description']}")
            print("------------------------\n")

        return tasks

    def find_unlocked_tasks(self):
        """
        (Placeholder) Filters tasks based on player_state.
        """
        # This is where the logic to check skill requirements, etc., will go.
        return self.all_tasks # For now, return all tasks

    def create_trip(self):
        """
        (Placeholder) The core logic engine.
        For now, it just creates one trip based on the first available task.
        """
        print("Creating a new trip...")
        
        unlocked_tasks = self.find_unlocked_tasks()
        if not unlocked_tasks:
            print("No more unlocked tasks available.")
            return None

        # Let's build a trip around the first unlocked task
        seed_task = unlocked_tasks[0]
        
        trip = {
            "title": f"Quest: {seed_task['quest_name']}",
            "goal": f"Complete the first step of {seed_task['quest_name']}.",
            "inventory_setup": ["Coins", "Stamina potion"], # Example items
            "steps": [
                {"text": seed_task['description']}
            ]
        }
        return trip

    def run(self):
        """Generates the full guide."""
        print("\nStarting guide generation...")
        
        if not self.all_tasks:
            print("No tasks loaded from the database. Cannot generate a guide.")
            return

        # For now, just generate one trip to demonstrate
        new_trip = self.create_trip()
        if new_trip:
            self.guide.append(new_trip)

        print("Guide generation complete.")
        self.save_guide()

    def save_guide(self):
        """Saves the generated guide to a JSON file."""
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.guide, f, indent=4)
        print(f"✅ Guide saved to {OUTPUT_PATH}")

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    generator = GuideGenerator()
    if generator.conn:
        generator.run()
        generator.close()