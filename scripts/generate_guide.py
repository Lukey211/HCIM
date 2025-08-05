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
        self.all_tasks = self.load_all_tasks_from_db()
        self.guide = []

    def get_db_connection(self):
        """Establishes a connection to the SQLite database."""
        if not os.path.exists(DB_PATH):
            print(f"❌ Database file not found at {DB_PATH}. Please run quest_parser.py first.")
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
        if not self.conn: return []
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT
                q.name AS quest_name,
                t.step_number,
                t.description
            FROM tasks t
            JOIN quests q ON t.quest_id = q.quest_id
            ORDER BY q.quest_id, t.step_number;
        """)
        tasks = [dict(row) for row in cursor.fetchall()]
        print(f"✅ Loaded {len(tasks)} tasks from the database.")
        return tasks

    def find_unlocked_tasks(self):
        """
        (Placeholder) Filters tasks based on player_state.
        In the future, this will check skill/quest requirements from the database.
        """
        return self.all_tasks # For now, we assume all tasks are unlocked

    def create_trip(self):
        """
        Creates a trip based on the first available quest in our task list.
        """
        print("Creating a new trip...")
        
        unlocked_tasks = self.find_unlocked_tasks()
        if not unlocked_tasks:
            print("No more unlocked tasks available.")
            return None

        # Get the name of the first quest in our database
        first_quest_name = unlocked_tasks[0]['quest_name']
        
        # Collect all steps for this specific quest
        quest_steps = [task for task in unlocked_tasks if task['quest_name'] == first_quest_name]

        trip = {
            "title": f"Quest: {first_quest_name}",
            "goal": f"Complete {first_quest_name}.",
            "inventory_setup": ["Quest-specific items will go here"],
            "steps": [
                # Format each step with its number and description from the database
                {"text": f"Step {s['step_number']}: {s['description']}"} for s in quest_steps
            ]
        }
        return trip

    def run(self):
        """Generates the full guide."""
        print("\nStarting guide generation...")
        if not self.all_tasks:
            print("No tasks loaded from the database. Cannot generate a guide.")
            return

        # For now, just generate one trip for the first quest to prove it works
        new_trip = self.create_trip()
        if new_trip:
            self.guide.append(new_trip)
            # Mark the quest as "completed" in our simulation
            self.player_state["completed_quests"].append(new_trip["title"])

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