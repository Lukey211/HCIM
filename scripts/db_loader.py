import sqlite3
import json
import os

# --- DATABASE AND FILE PATHS ---
# The script will automatically find the correct paths based on its location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, '..')
DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw')
DB_PATH = os.path.join(PROJECT_ROOT, 'data', 'osrs_guide.db') # The single-file database

def create_database(conn):
    """Creates the database tables if they don't already exist."""
    cursor = conn.cursor()
    print("Creating database schema...")

    # Items Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        item_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        members BOOLEAN,
        tradeable BOOLEAN,
        stackable BOOLEAN,
        examine_text TEXT,
        low_alch INTEGER,
        high_alch INTEGER,
        quest_item BOOLEAN
    );
    """)

    # Monsters Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS monsters (
        monster_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        combat_level INTEGER,
        hitpoints INTEGER,
        is_aggressive BOOLEAN,
        is_poisonous BOOLEAN,
        attack_type TEXT,
        max_hit INTEGER
    );
    """)

    # Prayers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prayers (
        prayer_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        level_required INTEGER,
        description TEXT
    );
    """)
    
    # Locations Table (using simple integer coordinates)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations (
        location_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        region_id INTEGER,
        x INTEGER,
        y INTEGER,
        plane INTEGER
    );
    """)

    conn.commit()
    print("✅ Schema created successfully.")


def load_items(conn):
    """Loads item data from items-complete.json into the database."""
    print("Loading items...")
    file_path = os.path.join(DATA_DIR, 'items-complete.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cursor = conn.cursor()
    items_to_insert = []
    for item_id, item_data in data.items():
        items_to_insert.append((
            item_data.get('id'), item_data.get('name'), item_data.get('members'),
            item_data.get('tradeable_on_ge'), item_data.get('stackable'),
            item_data.get('examine'), item_data.get('lowalch'), item_data.get('highalch'),
            item_data.get('quest_item')
        ))

    cursor.executemany("""
        INSERT OR IGNORE INTO items (item_id, name, members, tradeable, stackable, examine_text, low_alch, high_alch, quest_item)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, items_to_insert)
    conn.commit()
    print(f"✅ Items loaded: {len(items_to_insert)} records.")


def load_monsters(conn):
    """Loads monster data from monsters-complete.json into the database."""
    print("Loading monsters...")
    file_path = os.path.join(DATA_DIR, 'monsters-complete.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cursor = conn.cursor()
    monsters_to_insert = []
    for monster_id, monster_data in data.items():
        # The attack_type is a list, so we'll join it into a string
        attack_type = ', '.join(monster_data.get('attack_type', []))
        monsters_to_insert.append((
            monster_data.get('id'), monster_data.get('name'), monster_data.get('combat_level'),
            monster_data.get('hitpoints'), monster_data.get('aggressive'),
            monster_data.get('poisonous'), attack_type, monster_data.get('max_hit')
        ))

    cursor.executemany("""
        INSERT OR IGNORE INTO monsters (monster_id, name, combat_level, hitpoints, is_aggressive, is_poisonous, attack_type, max_hit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, monsters_to_insert)
    conn.commit()
    print(f"✅ Monsters loaded: {len(monsters_to_insert)} records.")


def load_prayers(conn):
    """Loads prayer data from prayers-complete.json into the database."""
    print("Loading prayers...")
    file_path = os.path.join(DATA_DIR, 'prayers-complete.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cursor = conn.cursor()
    prayers_to_insert = []
    for prayer_id, prayer_data in data.items():
        prayers_to_insert.append((
            # Assuming the key is the ID for prayers, as there's no 'id' field
            int(prayer_id), prayer_data.get('name'), prayer_data.get('level'),
            prayer_data.get('description')
        ))
        
    cursor.executemany("""
        INSERT OR IGNORE INTO prayers (prayer_id, name, level_required, description)
        VALUES (?, ?, ?, ?);
    """, prayers_to_insert)
    conn.commit()
    print(f"✅ Prayers loaded: {len(prayers_to_insert)} records.")


def load_locations(conn):
    """Loads location data from locations-complete.json into the database."""
    print("Loading locations...")
    file_path = os.path.join(DATA_DIR, 'locations-complete.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        # The locations file is a list of dictionaries
        data = json.load(f)
    
    cursor = conn.cursor()
    locations_to_insert = []
    for location_data in data:
        # The coordinates are nested in a 'position' dictionary
        pos = location_data.get('position', {})
        if pos: # Only insert if there is a position
            locations_to_insert.append((
                location_data.get('name'), location_data.get('id'),
                pos.get('x'), pos.get('y'), pos.get('z')
            ))

    cursor.executemany("""
        INSERT INTO locations (name, region_id, x, y, plane)
        VALUES (?, ?, ?, ?, ?);
    """, locations_to_insert)
    conn.commit()
    print(f"✅ Locations loaded: {len(locations_to_insert)} records.")


if __name__ == "__main__":
    # Remove old database file for a clean import, if it exists
    if os.path.exists(DB_PATH):
        print(f"Removing existing database file at {DB_PATH}")
        os.remove(DB_PATH)

    # This will create the DB file if it doesn't exist
    connection = sqlite3.connect(DB_PATH)
    
    # Create the tables
    create_database(connection)
    
    # Load all the data
    load_items(connection)
    load_monsters(connection)
    load_prayers(connection)
    load_locations(connection)
    
    connection.close()
    print("\n🎉 Database setup and loading process complete.")
    print(f"Database file created at: {DB_PATH}")