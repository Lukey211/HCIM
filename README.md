Excellent idea. A comprehensive README.md is crucial for the project's clarity and future development. Based on our entire journey and the final state of all the scripts and files you've uploaded, here is a detailed, in-depth README.md that accurately reflects the full scope of what we have accomplished and what each component does.

You can copy and paste this directly into your README.md file.

HCIM Efficiency Guide Generator

Project Overview

This project is a sophisticated, multi-stage data pipeline designed to generate a static, optimal step-by-step guide for Old School RuneScape (OSRS) Hardcore Ironman (HCIM) players. The ultimate goal is to produce the most efficient path from a new account to a Quest Cape, intelligently batching quests, skilling, and item gathering to minimize travel time and risk.

The system is built on a foundation of automated data scraping, processing, and storage, with a clear separation between the data pipeline and the final presentation layer.

Repository Structure

The project is organized into distinct modules for data, scripting logic, final output, and a web application front-end.

/HCIM
|
|-- data/
|   |-- raw/
|   |   |-- items-complete.json
|   |   |-- monsters-complete.json
|   |   |-- prayers-complete.json
|   |   |-- locations-complete.json
|   |
|   |-- osrs_guide.db  (The final SQLite database)
|
|-- scripts/
|   |-- data_importer.py
|   |-- db_loader.py
|   |-- quest_parser.py
|   |-- generate_guide.py
|   |-- (utility scripts like db_checker.py)
|
|-- output/
|   |-- hcim_guide.json
|
|-- app/
|   |-- index.html
|   |-- css/
|   |   |-- style.css
|   |-- js/
|       |-- script.js
|
|-- .gitignore
|-- README.md
|-- requirements.txt

The Data Pipeline Workflow

The project operates as a sequential pipeline. Each script performs a specific task, preparing the data for the next stage.

Stage 1: Raw Data Ingestion (data_importer.py)

This script is the entry point for all external game data. It is a complex, automated tool that:

    Downloads Static Data: Fetches the latest items-complete.json, monsters-complete.json, and prayers-complete.json from the official osrsbox-db repository.

    Automates Map Data Generation:

        Checks if the osrs-wiki-maps repository exists locally. If not, it automatically clones it from GitHub.

        Installs the necessary Python dependencies for the map tools.

        Executes the cache.py script to download the latest OSRS game cache.

        Builds the Java map exporter using Maven (mvn package).

        Executes the compiled Java application (MapExport.java) to process the game cache and generate the worldMapDefinitions.json file.

        Copies the final map data into /data/raw as locations-complete.json.

    User Prompts: Intelligently asks the user if they want to re-download the game cache or regenerate map data if it already exists, saving significant time on subsequent runs.

Stage 2: Database Creation (db_loader.py)

This script transforms the raw, unstructured JSON files into a powerful, queryable database.

    Creates SQLite Database: Generates a single-file SQLite database named osrs_guide.db in the /data directory.

    Defines Schema: Creates the necessary tables (items, monsters, prayers, locations, quests, tasks, task_requirements).

    Loads Data: Parses each of the .json files from /data/raw and loads their contents into the corresponding database tables.

Stage 3: Quest Parsing (quest_parser.py)

This script enriches the database with detailed, step-by-step quest information.

    Scrapes Master List: Fetches the main "Quests/List" page from the OSRS Wiki.

    Identifies All Quests: Intelligently parses the page to find the links to all 173 main quests, using their unique data-rowid attributes to ensure accuracy.

    Follows Links: For each quest, it follows a two-step process:

        Navigates to the main quest page.

        Finds the link to the dedicated /Quick_guide page.

    Parses and Cleans Steps: It scrapes the quick guide page, intelligently locating the "Walkthrough" section and extracting the step-by-step instructions. It also cleans the text to remove unwanted dialogue and fix spacing issues.

    Parses Requirements: It also parses the main quest page's infobox to extract item and skill requirements, storing this critical data in the database.

    Populates Database: Saves all quests, steps, and requirements into the quests, tasks, and task_requirements tables.

Stage 4: Guide Generation (generate_guide.py)

This is the core logic engine of the project. While still under development, its purpose is to:

    Connect to the Database: Reads all the structured data from osrs_guide.db.

    Simulate Player State: Maintains a virtual player profile with current skills, completed quests, and inventory.

    Find Unlocked Tasks: Queries the database to find all available tasks (quests, skilling, etc.) that the player currently meets the requirements for.

    Create Optimal Trips: The main algorithm will select a long-term goal (e.g., a quest) and then use the location data to find and batch together other nearby, efficient tasks into a single "trip".

    Generate Output: Saves the final, ordered list of trips as hcim_guide.json in the /output folder.

Stage 5: Presentation Layer (/app)

A simple, single-page web application for viewing the generated guide.

    index.html: The main HTML structure.

    js/script.js: Contains the JavaScript logic to fetch /output/hcim_guide.json and dynamically render it into a readable, interactive format with checklists.

Setup and Usage

To run the project from scratch, follow these steps:

    Prerequisites:

        Python 3.x

        Git

        Java Development Kit (JDK 11)

        Apache Maven

    Install Python Dependencies:
    Bash

pip install -r requirements.txt

Run the Full Data Pipeline:

    Step 1: Run the data importer to get all raw files. This will automatically clone and build the map data on the first run.
    Bash

python scripts/data_importer.py

Step 2: Run the database loader to create the SQLite database from the raw files.
Bash

python scripts/db_loader.py

Step 3: Run the quest parser to populate the database with all quest steps and requirements. This will take several minutes.
Bash

    python scripts/quest_parser.py

Generate the Guide:
Bash

python scripts/generate_guide.py

View the Guide:

    Start the local web server from the project's root directory (/HCIM).
    Bash

python -m http.server

Open your web browser and navigate to http://localhost:8000/app/.