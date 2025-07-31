HCIM Efficiency Guide Generator

This project is a data pipeline designed to generate a static, efficient questing and skilling guide for Old School RuneScape (OSRS) Hardcore Iron Man (HCIM) accounts. The primary goal is to produce an optimal step-by-step guide that minimizes risk and travel time, batching tasks together geospatially to achieve a Quest Cape.

Repository Structure

The project is organized to separate data, logic, and presentation into distinct modules.

/osrs-hcim-guide-generator
|
|-- data/
|   |-- raw/
|   |   |-- items-complete.json
|   |   |-- monsters-complete.json
|   |   |-- (other downloaded files...)
|   |
|   |-- processed/
|       |-- (files for your database, if needed)
|
|-- scripts/
|   |-- __init__.py
|   |-- osrsbox_importer.py
|   |-- map_data_importer.py
|   |-- quest_guide_parser.py
|   |-- generate_guide.py
|
|-- output/
|   |-- hcim_guide.json
|   |-- hcim_guide.md
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

Directory Purpose

    data/: Stores all game data.

        raw/: Contains unmodified files downloaded directly from external sources.

        processed/: Holds cleaned, structured data ready to be loaded into the database.

    scripts/: Contains all Python logic for fetching data, parsing information, and generating the final guide.

    output/: The destination for the final generated guide files (e.g., hcim_guide.json).

    app/: A simple, single-page web application that fetches and displays the generated guide from the output/ directory.

How It Works: The Data Pipeline

The project follows a multi-stage data pipeline approach:

    📥 Ingestion: The scripts in scripts/ are run to download the latest game data (items, monsters, maps, etc.) from public APIs and repositories into the data/raw/ directory.

    ⚙️ Processing & Storage: This raw data is then parsed, validated, and loaded into a PostgreSQL database. This structured data forms the "single source of truth" for the guide generator.

    🧠 Generation: The main generate_guide.py script executes the core logic. It simulates a player's state (skills, quests completed, inventory) and queries the database to find all currently achievable tasks. It uses geospatial analysis (PostGIS) to find nearby tasks and batches them into efficient "trips".

    📄 Output: Once the generator has plotted a course to the end goal (e.g., Quest Cape), it saves the complete, ordered list of trips as a structured JSON file in the output/ directory.

    🖥️ Presentation: A user can view the guide by running a local web server. The simple web app in the app/ folder fetches the generated JSON file and renders it in a readable, interactive format.

Setup & Usage

    Clone the repository:
    Bash

git clone <your-repository-url>
cd osrs-hcim-guide-generator

Install dependencies:
Bash

pip install -r requirements.txt

Set up the database:

    Install PostgreSQL and the PostGIS extension.

    Create a database and configure your connection details (you may need to add a config file for this).

Run the pipeline:

    Run the data ingestion and processing scripts.

    Run the main guide generator: python scripts/generate_guide.py

View the guide:

    Start a local server from the project root: python -m http.server

    Open your browser and go to http://localhost:8000/app/.