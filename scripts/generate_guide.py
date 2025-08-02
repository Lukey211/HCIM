import sqlite3
import json
import os

# --- DATABASE PATH ---
# The script will automatically find the database file in the data directory
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
        try:
            conn = sqlite3.connect(DB_PATH)
            # This allows us to access columns by name
            conn.row_factory = sqlite3.Row
            print("✅ Successfully connected to the SQLite database.")
            return conn
        except sqlite3.Error as e:
            print(f"❌ Database connection error: {e}")
            return None

    def initialize_player_state(self):
        """Sets up the initial state for a new level 3 account."""
        # In a more advanced version, this could be a more detailed dictionary or class
        return {
            "skills": {
                "attack": 1, "strength": 1, "defence": 1, "hitpoints": 10,
                "ranged": 1, "magic": 1, "prayer": 1, "cooking": 1,
                "woodcutting": 1, "fletching": 1, "fishing": 1, "firemaking": 1,
                "crafting": 1, "smithing": 1, "mining": 1, "herblore": 1,
                "agility": 1, "thieving": 1, "slayer": 1, "farming": 1,
                "runecraft": 1, "hunter": 1, "construction": 1
            },
            "completed_quests": [],
            "inventory": [],
            "bank": [],
            "current_location": {"x": 3222, "y": 3218, "plane": 0} # Lumbridge
        }

    def load_all_tasks_from_db(self):
        """
        Placeholder function. This will eventually query the database for all
        parsed quest steps, skilling actions, item pickups, etc.
        For now, it returns a hardcoded example.
        """
        print("Loading all tasks from database...")
        cursor = self.conn.cursor()
        
        # --- PSEUDOCODE for future database queries ---
        # cursor.execute("SELECT * FROM quests")
        # all_quests = cursor.fetchall()
        #
        # cursor.execute("SELECT * FROM skilling_actions")
        # all_skilling = cursor.fetchall()
        
        # For now, we'll return an empty list as we haven't defined tasks yet
        tasks = []
        print("✅ Tasks loaded (currently empty).")
        return tasks

    def find_unlocked_tasks(self):
        """
        Filters the master task list to find tasks whose dependencies
        (skill levels, quest points, items) are met by the current player_state.
        """
        unlocked_tasks = []
        for task in self.all_tasks:
            # --- PSEUDOCODE for dependency checking ---
            # requirements_met = True
            # if task.required_skills:
            #     for skill, level in task.required_skills.items():
            #         if self.player_state['skills'][skill] < level:
            #             requirements_met = False
            #             break
            # if requirements_met:
            #     unlocked_tasks.append(task)
            pass
        return unlocked_tasks

    def create_trip(self):
        """
        This is the core logic engine. It will:
        1. Identify a major goal (e.g., complete a quest).
        2. Select a "seed task" for that goal (e.g., the first step of the quest).
        3. Query the database for nearby, zero-risk tasks and required item spawns using coordinate math.
        4. Generate a step-by-step plan for the trip.
        5. Return a "trip" object.
        """
        print("Creating a new trip...")
        # This is a hardcoded example trip for demonstration purposes.
        # The real logic will be much more complex.
        trip = {
            "title": "Starting Out in Lumbridge",
            "goal": "Prepare for Cook's Assistant and gather initial supplies.",
            "inventory_setup": ["A small fishing net", "An axe", "A tinderbox"],
            "steps": [
                {"text": "Talk to the Lumbridge Guide to get your initial tools."},
                {"text": "Walk to the pond north of the castle and catch 5 Shrimp."},
                {"text": "Walk west to the trees and chop 5 logs."},
                {"text": "Light the logs and cook the shrimp on the fire."},
                {"text": "Walk to the Lumbridge Castle kitchen to start Cook's Assistant."}
            ]
        }
        return trip

    def run(self):
        """Generates the full guide until the end goal is met."""
        print("\nStarting guide generation...")
        
        # This loop will eventually be the core of the program.
        # For now, it just runs once to generate our example trip.
        while len(self.player_state["completed_quests"]) < 1: # Loop just once for now
            new_trip = self.create_trip()
            self.guide.append(new_trip)
            
            # --- PSEUDOCODE for updating player state ---
            # self.update_player_state(new_trip)
            
            # We'll just break to prevent an infinite loop in this skeleton version
            break

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