@echo off
:: This script creates the complete directory and file structure for the
:: OSRS HCIM Guide Generator project.

:: Set the root directory for the project
set "PROJECT_DIR=C:\Users\g\Desktop\Code Projects\HCIM"

echo #################################################
echo # OSRS HCIM Guide Generator Project Setup       #
echo #################################################
echo.
echo Target directory: %PROJECT_DIR%
echo.

:: Check if the directory exists, if not, create it.
if not exist "%PROJECT_DIR%" (
    echo Directory does not exist. Creating it now...
    mkdir "%PROJECT_DIR%"
)

:: Change to the project directory
cd /d "%PROJECT_DIR%"

:: --- 1. Create Directory Structure ---
echo Creating sub-directories...
mkdir "data"
mkdir "data\raw"
mkdir "data\processed"
mkdir "scripts"
mkdir "output"
mkdir "app"
mkdir "app\css"
mkdir "app\js"
echo ...Directory structure created.
echo.

:: --- 2. Create Project Files ---
echo Creating project files...

:: Create .gitignore
(
    echo # Ignore Python's cache files
    echo __pycache__/
    echo *.pyc
    echo.
    echo # Ignore virtual environment folders
    echo venv/
    echo .venv/
    echo.
    echo # Ignore all raw and processed data files
    echo data/raw/*
    echo data/processed/*
    echo.
    echo # You can temporarily comment out the line below to commit the final guide
    echo # output/*
) > .gitignore
echo ... .gitignore created.

:: Create requirements.txt
(
    echo requests
    echo psycopg2-binary  # For connecting to PostgreSQL
) > requirements.txt
echo ... requirements.txt created.

:: Create README.md
(
    echo # OSRS HCIM Guide Generator
    echo.
    echo This project is designed to generate a static, step-by-step guide for Hardcore Ironman players aiming for a Quest Cape in Old School RuneScape.
) > README.md
echo ... README.md created.

:: --- 3. Create Script Files ---

:: Create empty __init__.py
type NUL > scripts\__init__.py

:: Create osrsbox_importer.py
(
    echo import requests
    echo import json
    echo import os
    echo.
    echo # Define the URLs for the data we need from the osrsbox-db repository
    echo DATA_SOURCES = {
    echo     "items": "https://raw.githubusercontent.com/osrsbox/osrsbox-db/master/data/items/items-complete.json",
    echo     "monsters": "https://raw.githubusercontent.com/osrsbox/osrsbox-db/master/data/monsters/monsters-complete.json"
    echo }
    echo.
    echo # Define the output directory for our raw data
    echo OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
    echo.
    echo def download_data():
    echo     """
    echo     Downloads the latest data files from osrsbox-db and saves them locally.
    echo     """
    echo     print("Starting data download from osrsbox-db...")
    echo.
    echo     # Ensure the output directory exists
    echo     if not os.path.exists(OUTPUT_DIR):
    echo         os.makedirs(OUTPUT_DIR)
    echo         print(f"Created directory: {OUTPUT_DIR}")
    echo.
    echo     for name, url in DATA_SOURCES.items():
    echo         try:
    echo             print(f"Downloading {name} data from {url}...")
    echo             response = requests.get(url, timeout=30)
    echo             response.raise_for_status()  # This will raise an error for bad responses (4xx or 5xx)
    echo.
    echo             # Define the local file path
    echo             file_path = os.path.join(OUTPUT_DIR, f"{name}-complete.json")
    echo.
    echo             # Save the content to a file
    echo             with open(file_path, 'w', encoding='utf-8') as f:
    echo                 json.dump(response.json(), f, indent=4)
    echo.
    echo             print(f"Successfully saved {name} data to {file_path}")
    echo.
    echo         except requests.exceptions.RequestException as e:
    echo             print(f"Error downloading {name} data: {e}")
    echo         except json.JSONDecodeError as e:
    echo             print(f"Error decoding JSON for {name}: {e}")
    echo.
    echo if __name__ == "__main__":
    echo     # This block allows the script to be run directly from the command line
    echo     download_data()
    echo     # In the future, you would add a function call here to load the data into your PostgreSQL database.
    echo     # e.g., load_items_to_db()
) > scripts\osrsbox_importer.py
echo ... scripts/osrsbox_importer.py created.

:: Create placeholder map_data_importer.py
(
    echo # This script will handle importing map, NPC, and object location data.
    echo # It will likely parse data from the osrs-wiki-maps repository.
    echo pass
) > scripts\map_data_importer.py
echo ... scripts/map_data_importer.py created.

:: Create placeholder quest_guide_parser.py
(
    echo # This script will use the MediaWiki API to parse quest guides.
    echo # It will extract requirements, steps, and rewards into a structured format.
    echo pass
) > scripts\quest_guide_parser.py
echo ... scripts/quest_guide_parser.py created.

:: Create generate_guide.py
(
    echo import json
    echo import os
    echo.
    echo # Define the output path for the final guide
    echo OUTPUT_PATH = os.path.join(os.path.dirname(__file__), '..', 'output', 'hcim_guide.json')
    echo.
    echo class GuideGenerator:
    echo     def __init__(self):
    echo         # In the future, this is where you'd connect to your PostgreSQL database
    echo         # self.db_connection = connect_to_db()
    echo         self.player_state = self.initialize_player_state()
    echo         self.all_tasks = self.load_all_tasks_from_db()
    echo         self.guide = []
    echo.
    echo     def initialize_player_state(self):
    echo         """Sets up the initial state for a level 3 account."""
    echo         return {
    echo             "skills": {"attack": 1, "strength": 1, "defence": 1, "hitpoints": 10},
    echo             "completed_quests": [],
    echo             "inventory": [],
    echo             "bank": [],
    echo             "current_location": "Lumbridge"
    echo         }
    echo.
    echo     def load_all_tasks_from_db(self):
    echo         """
    echo         Placeholder function. This will eventually query your database
    echo         for all parsed quest steps, skilling actions, etc.
    echo         """
    echo         print("Loading all tasks from database...")
    echo         # Pseudocode: SELECT * FROM tasks;
    echo         return [] # Return a list of Task objects
    echo.
    echo     def find_unlocked_tasks(self):
    echo         """
    echo         Filters the master task list to find tasks whose dependencies are met
    echo         by the current player_state.
    echo         """
    echo         unlocked = []
    echo         for task in self.all_tasks:
    echo             # Pseudocode: check_dependencies(task, self.player_state)
    echo             pass
    echo         return unlocked
    echo.
    echo     def create_trip(self):
    echo         """
    echo         The core logic. Selects a goal, finds a seed task, and batches
    echo         nearby tasks and item pickups into a single trip.
    echo         """
    echo         print("Creating a new trip...")
    echo         # 1. Identify major goal (e.g., unlock Ardougne Cloak 1)
    echo         # 2. Select a seed task for that goal (e.g., start 'Plague City')
    echo         # 3. Use PostGIS to find nearby, zero-risk tasks and required item spawns.
    echo         # 4. Generate a step-by-step plan for the trip.
    echo         # 5. Return the trip object.
    echo         trip = {
    echo             "title": "The Varrock & Canifis Run",
    echo             "goal": "Complete Priest in Peril to unlock Morytania.",
    echo             "inventory_setup": ["1x Bucket", "50x Essence", "1x Tinderbox"],
    echo             "steps": [
    echo                 {"text": "Walk east. Enter Varrock Palace library and talk to `Reldo` to start `Shield of Arrav`."},
    echo                 {"text": "Walk north-east. Pick up the `Cadava berries` behind the fence. **(For a future quest)**"},
    echo                 {"text": "Return to Varrock West Bank."}
    echo             ]
    echo         }
    echo         return trip
    echo.
    echo     def run(self):
    echo         """Generates the full guide until the end goal is met."""
    echo         print("Starting guide generation...")
    echo         # Loop until Quest Cape is achieved (or all quests are marked complete)
    echo         while len(self.player_state["completed_quests"]) ^< 150: # Example number
    echo             new_trip = self.create_trip()
    echo             self.guide.append(new_trip)
    echo             # Pseudocode: update_player_state(self.player_state, new_trip.rewards)
    echo             # For now, we'll just break to prevent an infinite loop
    echo             break
    echo.
    echo         print("Guide generation complete.")
    echo         self.save_guide()
    echo.
    echo     def save_guide(self):
    echo         """Saves the generated guide to a JSON file."""
    echo         with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    echo             json.dump(self.guide, f, indent=4)
    echo         print(f"Guide saved to {OUTPUT_PATH}")
    echo.
    echo.
    echo if __name__ == "__main__":
    echo     generator = GuideGenerator()
    echo     generator.run()
) > scripts\generate_guide.py
echo ... scripts/generate_guide.py created.

:: --- 4. Create Web App Files ---

:: Create index.html
(
    echo ^<!DOCTYPE html^>
    echo ^<html lang="en"^>
    echo ^<head^>
    echo     ^<meta charset="UTF-8"^>
    echo     ^<meta name="viewport" content="width=device-width, initial-scale=1.0"^>
    echo     ^<title^>HCIM Quest Cape Guide^</title^>
    echo     ^<link rel="stylesheet" href="css/style.css"^>
    echo ^</head^>
    echo ^<body^>
    echo     ^<header^>
    echo         ^<h1^>HCIM Quest Cape Efficiency Guide^</h1^>
    echo     ^</header^>
    echo     ^<main id="guide-container"^>
    echo         ^!-- Guide content will be loaded here by JavaScript --^>
    echo         ^<p class="loading"^>Loading guide...^</p^>
    echo     ^</main^>
    echo     ^<script src="js/script.js"^>^</script^>
    echo ^</body^>
    echo ^</html^>
) > app\index.html
echo ... app/index.html created.

:: Create style.css
(
    echo body {
    echo     font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    echo     line-height: 1.6;
    echo     background-color: #f4f4f4;
    echo     color: #333;
    echo     margin: 0;
    echo     padding: 20px;
    echo }
    echo header {
    echo     text-align: center;
    echo     margin-bottom: 2rem;
    echo }
    echo main {
    echo     max-width: 800px;
    echo     margin: auto;
    echo     background: #fff;
    echo     padding: 2rem;
    echo     border-radius: 8px;
    echo     box-shadow: 0 0 10px rgba(0,0,0,0.1);
    echo }
) > app\css\style.css
echo ... app/css/style.css created.

:: Create script.js
(
    echo document.addEventListener('DOMContentLoaded', () => {
    echo     const guideContainer = document.getElementById('guide-container');
    echo.
    echo     // Fetch the generated guide from the output folder
    echo     // Note: This requires you to run a local server.
    echo     // You can use `python -m http.server` in the root directory.
    echo     fetch('../output/hcim_guide.json')
    echo         .then(response => {
    echo             if (!response.ok) {
    echo                 throw new Error('Network response was not ok');
    echo             }
    echo             return response.json();
    echo         })
    echo         .then(guideData => {
    echo             guideContainer.innerHTML = ''; // Clear loading message
    echo             renderGuide(guideData, guideContainer);
    echo         })
    echo         .catch(error => {
    echo             console.error('Error fetching the guide:', error);
    echo             guideContainer.innerHTML = `^<p class="error"^>Could not load the guide. Make sure the file exists and you are running a local server.^</p^>`;
    echo         });
    echo });
    echo.
    echo function renderGuide(guide, container) {
    echo     guide.forEach((trip, index) => {
    echo         const tripElement = document.createElement('div');
    echo         tripElement.className = 'trip';
    echo.
    echo         tripElement.innerHTML = `
    echo             ^<h2^>Chapter ${index + 1}: ${trip.title}^</h2^>
    echo             ^<p^>^<strong^>Goal:^</strong^> ${trip.goal}^</p^>
    echo             ^<h3^>Inventory Setup:^</h3^>
    echo             ^<ul^>
    echo                 ${trip.inventory_setup.map(item => `^<li^>${item}^</li^>`).join('')}
    echo             ^</ul^>
    echo             ^<h3^>Steps:^</h3^>
    echo             ^<ol^>
    echo                 ${trip.steps.map(step => `^<li^>^<input type="checkbox"^> ${step.text}^</li^>`).join('')}
    echo             ^</ol^>
    echo         `;
    echo         container.appendChild(tripElement);
    echo     });
    echo }
) > app\js\script.js
echo ... app/js/script.js created.

echo.
echo --- All files created successfully! ---
echo.
echo Next steps:
echo 1. Open the project in your favorite code editor.
echo 2. Install dependencies: pip install -r requirements.txt
echo 3. Run the first script: python scripts/osrsbox_importer.py
echo.
pause
