import requests
from bs4 import BeautifulSoup
import sqlite3
import os
import re
import time

# --- DATABASE AND FILE PATHS ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, '..')
DB_PATH = os.path.join(PROJECT_ROOT, 'data', 'osrs_guide.db')

# --- WIKI URLS ---
BASE_WIKI_URL = "https://oldschool.runescape.wiki"
QUEST_LIST_URL = f"{BASE_WIKI_URL}/w/Quests/List"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)

def create_quest_tables(conn):
    """Creates the necessary tables for storing quest and task data."""
    cursor = conn.cursor()
    print("Ensuring quest and task tables exist...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quests (
        quest_id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE, wiki_url TEXT
    );""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT, quest_id INTEGER, step_number INTEGER,
        description TEXT NOT NULL,
        FOREIGN KEY (quest_id) REFERENCES quests (quest_id)
    );""")
    conn.commit()
    print("✅ Tables are ready.")

def fetch_all_quest_links():
    """
    Scrapes the main quest list page by finding all rows with a 'data-rowid'
    attribute to get the URL for every quest's main page.
    """
    print(f"Fetching master quest list from: {QUEST_LIST_URL}")
    headers = {'User-Agent': 'HCIM Guide Generator Bot'}
    response = requests.get(QUEST_LIST_URL, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    quest_links = {}
    quest_rows = soup.find_all('tr', attrs={'data-rowid': True})
    
    if not quest_rows:
        print("❌ Could not find any quest rows with the 'data-rowid' attribute.")
        return {}

    for row in quest_rows:
        link_tag = row.select_one('td:nth-of-type(2) a')
        if link_tag and link_tag.has_attr('href'):
            quest_name = link_tag.get_text(strip=True)
            if "Recipe for Disaster/" not in link_tag.get('title', ''):
                quest_links[quest_name] = f"{BASE_WIKI_URL}{link_tag['href']}"
                
    print(f"✅ Found {len(quest_links)} quests.")
    return quest_links

def parse_quest(conn, quest_name, quest_url):
    """
    Parses a single quest, finding its quick guide and scraping the cleaned steps.
    """
    print(f"  -> Processing '{quest_name}'...")
    headers = {'User-Agent': 'HCIM Guide Generator Bot'}
    
    try:
        main_page_response = requests.get(quest_url, headers=headers, timeout=10)
        main_page_response.raise_for_status()
        main_soup = BeautifulSoup(main_page_response.content, 'html.parser')

        quick_guide_link = main_soup.find('a', href=re.compile(r'/Quick_guide$'))
        if not quick_guide_link:
            print(f"    ⚠️ No quick guide link found for '{quest_name}'. Skipping.")
            return

        quick_guide_url = f"{BASE_WIKI_URL}{quick_guide_link['href']}"
        
        quick_guide_response = requests.get(quick_guide_url, headers=headers, timeout=10)
        quick_guide_response.raise_for_status()
        quick_guide_soup = BeautifulSoup(quick_guide_response.content, 'html.parser')

        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO quests (name, wiki_url) VALUES (?, ?)", (quest_name, quick_guide_url))
        quest_id = cursor.execute("SELECT quest_id FROM quests WHERE name = ?", (quest_name,)).fetchone()[0]

        walkthrough_header = quick_guide_soup.find('span', id='Walkthrough')
        if not walkthrough_header:
            print(f"    ❌ No 'Walkthrough' section found for '{quest_name}'. Skipping.")
            return

        steps_list = walkthrough_header.find_parent('h2').find_next(['ol', 'ul'])
        if not steps_list:
            print(f"    ❌ No list found after 'Walkthrough' for '{quest_name}'. Skipping.")
            return
        
        step_count = 0
        for i, step in enumerate(steps_list.find_all('li', recursive=False)):
            # --- REFINED TEXT CLEANING ---
            # 1. Remove only the dialogue explanation boxes ('dl' tags)
            for dialogue in step.find_all('dl'):
                dialogue.decompose()
            
            # 2. Get the text, using a space as a separator to prevent joined words,
            #    which preserves the chat option numbers inside their <span> tags.
            step_text = step.get_text(separator=' ', strip=True)

            cursor.execute("""
                INSERT INTO tasks (quest_id, step_number, description)
                VALUES (?, ?, ?);
            """, (quest_id, i + 1, step_text))
            step_count += 1
        
        conn.commit()
        if step_count > 0:
            print(f"    ✅ Parsed and loaded {step_count} cleaned steps for '{quest_name}'.")
        else:
            print(f"    ⚠️ Found quick guide for '{quest_name}', but no steps were parsed.")
            
    except requests.exceptions.RequestException as e:
        print(f"    ❌ An error occurred while processing '{quest_name}': {e}")

if __name__ == "__main__":
    connection = get_db_connection()
    if connection:
        create_quest_tables(connection)
        
        print("\nClearing all existing quest and task data from the database...")
        cur = connection.cursor()
        cur.execute("DELETE FROM tasks;")
        cur.execute("DELETE FROM quests;")
        cur.execute("DELETE FROM sqlite_sequence WHERE name IN ('tasks', 'quests');")
        connection.commit()
        print("✅ Existing data cleared.")
        
        all_quests = fetch_all_quest_links()
        if all_quests:
            print("\n--- Starting Quest Parsing ---")
            for quest_name, url in all_quests.items():
                parse_quest(connection, quest_name, url)
                time.sleep(0.5)
            print("--- Quest Parsing Finished ---")

        connection.close()
        print("\nQuest parsing process complete.")