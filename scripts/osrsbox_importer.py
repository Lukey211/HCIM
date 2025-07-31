import json
import os
import shutil

# --- CONFIGURATION ---
# Define the path to your local clone of the osrsbox-db repository.
# This path points to the folder created by the `git clone` command.
OSRSBOX_REPO_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'osrsbox-db')

# Define the CORRECT source files we want to copy from the cloned repository.
# The files are located in the 'docs' directory, not 'src/data'.
SOURCE_FILES = {
    "items": os.path.join(OSRSBOX_REPO_PATH, 'docs', 'items-complete.json'),
    "monsters": os.path.join(OSRSBOX_REPO_PATH, 'docs', 'monsters-complete.json')
}

# Define the destination directory for our project's raw data.
DESTINATION_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')

def copy_local_data():
    """
    Copies the required data files from the local osrsbox-db repository
    clone to this project's data directory.
    """
    print("Starting local data import...")

    # Ensure the destination directory exists.
    if not os.path.exists(DESTINATION_DIR):
        os.makedirs(DESTINATION_DIR)
        print(f"Created destination directory: {DESTINATION_DIR}")

    # Verify that the source repository path exists.
    if not os.path.exists(OSRSBOX_REPO_PATH):
        print(f"FATAL ERROR: The osrsbox-db repository was not found at the expected path:")
        print(f"'{OSRSBOX_REPO_PATH}'")
        print("Please ensure you have cloned the repository into the correct directory.")
        return

    for name, source_path in SOURCE_FILES.items():
        try:
            # Verify the source file exists before trying to copy.
            if not os.path.exists(source_path):
                print(f"Error: Source file not found for '{name}' at '{source_path}'")
                continue
            
            # Define the final destination path.
            destination_path = os.path.join(DESTINATION_DIR, f"{name}-complete.json")

            # Copy the file.
            shutil.copy2(source_path, destination_path)
            print(f"Successfully copied {name} data to {destination_path}")

        except Exception as e:
            print(f"An error occurred while copying '{name}' data: {e}")

if __name__ == "__main__":
    copy_local_data()