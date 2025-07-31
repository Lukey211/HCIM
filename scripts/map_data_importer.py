import requests
import json
import os

# --- CONFIGURATION ---
# Define the stable, direct URL for the pre-generated locations.json file.
DATA_URL = "https://maps.runescape.wiki/osrs/locations.json"

# Define the destination directory for our project's raw data.
DESTINATION_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')

def download_map_data():
    """
    Downloads the locations.json file directly from the wiki's map CDN.
    """
    print("Starting map data download from the official wiki CDN...")

    # Ensure the destination directory exists.
    if not os.path.exists(DESTINATION_DIR):
        os.makedirs(DESTINATION_DIR)
        print(f"Created destination directory: {DESTINATION_DIR}")

    try:
        print(f"Downloading map data from {DATA_URL}...")
        # Increased timeout for a potentially large file
        response = requests.get(DATA_URL, timeout=60)
        # Raise an error for bad responses (like 404 Not Found)
        response.raise_for_status()

        # Define the final destination path.
        destination_path = os.path.join(DESTINATION_DIR, 'locations.json')

        # Save the content to the file.
        with open(destination_path, 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, indent=4)

        print(f"Successfully saved map data to {destination_path}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading map data: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON. The downloaded file may be corrupt or not valid JSON: {e}")

if __name__ == "__main__":
    download_map_data()