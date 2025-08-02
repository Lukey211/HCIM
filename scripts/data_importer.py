import requests
import json
import os
import sys
import shutil
import subprocess

# --- Static Data Sources ---
STATIC_DATA_SOURCES = {
    "items": "https://raw.githubusercontent.com/osrsbox/osrsbox-db/master/docs/items-complete.json",
    "monsters": "https://raw.githubusercontent.com/osrsbox/osrsbox-db/master/docs/monsters-complete.json",
    "prayers": "https://raw.githubusercontent.com/osrsbox/osrsbox-db/master/docs/prayers-complete.json"
}

# --- Project Directory and Tool Paths Setup ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw')
CODE_PROJECTS_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, '..'))
MAPS_REPO_DIR = os.path.join(CODE_PROJECTS_DIR, 'osrs-wiki-maps')
MAPS_REPO_URL = "https://github.com/osrs-wiki/osrs-wiki-maps.git"
MAVEN_EXECUTABLE = r"C:\Program Files\JetBrains\IntelliJ IDEA 2025.1.1.1\plugins\maven\lib\maven3\bin\mvn.cmd"


def download_static_data():
    """Downloads the static osrsbox data files."""
    print("--- Step 1: Downloading Static Data (Items, Monsters, & Prayers) ---")
    for name, url in STATIC_DATA_SOURCES.items():
        try:
            file_name = f"{name}-complete.json"
            file_path = os.path.join(OUTPUT_DIR, file_name)
            print(f"Downloading {name} data from {url}...")

            response = requests.get(url, timeout=60)
            response.raise_for_status()
            data = json.loads(response.text)

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            print(f"✅ Successfully saved {name} data to {file_path}")
        except Exception as e:
            print(f"❌ An error occurred downloading {name}: {e}")
            return False
    return True

def run_command(command, working_dir):
    """Helper function to run a command and handle errors."""
    try:
        result = subprocess.run(
            command,
            cwd=working_dir,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        return True
    except FileNotFoundError:
        print(f"❌ ERROR: Command not found: '{command[0]}'. Is it installed and in your PATH?")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: Command failed: '{' '.join(command)}'")
        print(f"   Return Code: {e.returncode}")
        print(f"   --- STDOUT ---:\n{e.stdout}")
        print(f"   --- STDERR ---:\n{e.stderr}")
        return False
    except Exception as e:
        print(f"❌ An unexpected error occurred while running command: {e}")
        return False

def generate_and_import_map_data():
    """Automates the process of building and importing the osrs-wiki-maps data."""
    print("\n--- Step 2: Generating Map Data (Locations) ---")

    if not all(shutil.which(cmd) for cmd in ["git"]):
        print("❌ ERROR: Git is not found. Please install it and ensure it is in your system's PATH.")
        return False
    if not os.path.exists(MAVEN_EXECUTABLE):
        print(f"❌ ERROR: Maven executable not found at the specified path: {MAVEN_EXECUTABLE}")
        return False
    print("✅ Prerequisites found.")

    if not os.path.isdir(MAPS_REPO_DIR):
        print(f"Cloning '{MAPS_REPO_URL}' into '{CODE_PROJECTS_DIR}'...")
        if not run_command(["git", "clone", MAPS_REPO_URL], CODE_PROJECTS_DIR):
            return False
        print("✅ Repository cloned successfully.")
    else:
        print(f"✅ 'osrs-wiki-maps' repository found.")

    version_file = os.path.join(MAPS_REPO_DIR, 'data', 'versions', 'version.txt')
    should_download_cache = True
    if os.path.exists(version_file):
        with open(version_file, 'r') as f:
            existing_version = f.read().strip()
        print(f"\nFound existing cache version: {existing_version}")
        answer = input("Do you want to download a fresh game cache? (y/n, default is n): ").lower()
        if answer != 'y':
            should_download_cache = False
    
    if should_download_cache:
        print("\nRunning 'cache.py' to download game data. This may take several minutes...")
        if not run_command([sys.executable, os.path.join('scripts', 'cache.py')], MAPS_REPO_DIR):
            return False
        print("✅ Game cache downloaded successfully.")

    with open(version_file, 'r') as f:
        version = f.read().strip()
    print(f"Using cache version: {version}")

    print("\nBuilding Java map exporter with Maven... This will download dependencies on the first run.")
    if not run_command([MAVEN_EXECUTABLE, "package"], MAPS_REPO_DIR):
        return False
    print("✅ Java application built successfully.")

    target_dir = os.path.join(MAPS_REPO_DIR, 'osrs-wiki-maps', 'target')
    jar_files = [f for f in os.listdir(target_dir) if f.endswith('-shaded.jar')]
    if not jar_files:
        print(f"❌ ERROR: Could not find the shaded JAR file in '{target_dir}'.")
        return False
    jar_file_path = os.path.join(target_dir, jar_files[0])
    print(f"Found executable JAR: {jar_file_path}")

    print("\nRunning Java map exporter. This is a long process, please be patient...")
    if not run_command(["java", "-jar", jar_file_path], MAPS_REPO_DIR):
        return False
    print("✅ Java map exporter finished successfully.")
    
    source_file = os.path.join(MAPS_REPO_DIR, 'out', 'mapgen', 'versions', version, 'worldMapDefinitions.json')
    dest_file = os.path.join(OUTPUT_DIR, 'locations-complete.json')
    
    print(f"\nCopying generated map data...")
    print(f"   FROM: {source_file}")
    print(f"   TO:   {dest_file}")
    
    try:
        shutil.copyfile(source_file, dest_file)
        print("✅ Successfully copied and renamed map data.")
    except FileNotFoundError:
        print(f"❌ ERROR: Could not find the generated file at '{source_file}'.")
        return False
        
    return True

def main():
    """Runs the full data import process."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    if not download_static_data():
        print("\n⚠️ Data import process failed during static data download.")
        return

    # --- NEW: Check if map data should be generated ---
    locations_file = os.path.join(OUTPUT_DIR, 'locations-complete.json')
    run_map_generator = True
    if os.path.exists(locations_file):
        print("\n--- Map Data Check ---")
        print(f"✅ 'locations-complete.json' already exists.")
        answer = input("Do you want to regenerate it? This will take several minutes. (y/n, default is n): ").lower()
        if answer != 'y':
            run_map_generator = False
            print("Skipping map generation.")

    if run_map_generator:
        if not generate_and_import_map_data():
            print("\n⚠️ Data import process failed during map generation.")
            return
    
    print("\n🎉 Data import process complete. All raw data files are in data/raw/")


if __name__ == "__main__":
    main()