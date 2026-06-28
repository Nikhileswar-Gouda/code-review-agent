import json
import os
import datetime

# Storage file configuration
MEMORY_FILE = "fixes_memory.json"

# Function to save a successful fix to the memory file.
def save_fix(bug_description: str, fix_code: str):
    """
    Saves a bug description and its associated fix code with a timestamp to a JSON file.
    
    Parameters:
        bug_description (str): Description of the bug.
        fix_code (str): The code that fixed the bug.
    """
    print(f"[DEBUG] Saving fix for bug: '{bug_description}'...")
    try:
        memory = {}
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                memory = json.load(f)
                
        now = datetime.datetime.now().isoformat()
        memory[bug_description] = {
            "fix": fix_code,
            "timestamp": now
        }
        
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=4)
            
        print(f"Confirmation: Successfully saved fix for '{bug_description}' to {MEMORY_FILE}.")
    except Exception as e:
        print(f"[DEBUG] Error saving fix: {e}")

# Function to recall a similar fix based on a bug description.
def recall_similar_fix(bug_description: str) -> str or None:
    """
    Recalls a stored fix if the given bug description shares 3 or more words with a stored one.
    
    Parameters:
        bug_description (str): The description of the bug to query.
        
    Returns:
        str or None: The recalled fix code if a match is found, otherwise None.
    """
    print(f"[DEBUG] Querying memory for bug: '{bug_description}'...")
    try:
        if not os.path.exists(MEMORY_FILE):
            print(f"[DEBUG] Memory file '{MEMORY_FILE}' not found.")
            return None
            
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            memory = json.load(f)
            
        query_words = set(bug_description.lower().split())
        
        for stored_desc, data in memory.items():
            stored_words = set(stored_desc.lower().split())
            matching_words = query_words.intersection(stored_words)
            
            if len(matching_words) >= 3:
                print(f"[DEBUG] Found matching bug in memory with {len(matching_words)} common words.")
                return data.get("fix")
                
        print("[DEBUG] No similar bug found in memory.")
        return None
    except Exception as e:
        print(f"[DEBUG] Error recalling fix: {e}")
        return None
