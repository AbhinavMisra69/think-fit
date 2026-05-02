import json
import requests
import difflib
import os
import re  # <-- NEW: We need Regex to detect and delete brackets

# 1. Advanced text cleaner
def clean_name(name):
    if not name: return ""
    
    # NEW: Find any opening bracket '(', any text inside, and the closing bracket ')', and delete it all.
    c = re.sub(r'\(.*?\)', '', str(name))
    
    c = c.lower().replace('-', ' ').replace('_', ' ').replace('/', ' ').strip()
    c = ' '.join(c.split())
    
    # Strip trailing 's' to normalize plurals
    words = c.split()
    cleaned_words = []
    for w in words:
        if w.endswith('s') and not w.endswith('ss'):
            cleaned_words.append(w[:-1])
        else:
            cleaned_words.append(w)
    return ' '.join(cleaned_words)

# Smart Name Extractor
def get_exercise_name(ex):
    possible_keys = ['name', 'Exercise', 'title', 'Title', 'exercise_name', 'Exercise_Name', 'exercise', 'Name']
    for key in possible_keys:
        if key in ex and ex[key]:
            return str(ex[key])
    return ""

def update_exercise_animations():
    local_file_path = 'data/exercises_enriched.json' 
    
    print("1. Fetching open-source database from GitHub...")
    url = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/dist/exercises.json"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to fetch external database.")
        return
        
    external_db = response.json()
    external_dict = {}
    base_url = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/"
    
    for ex in external_db:
        c_name = clean_name(ex.get('name', ''))
        images = ex.get('images', [])
        if c_name and images and len(images) == 2:
            external_dict[c_name] = [base_url + images[0], base_url + images[1]]

    external_names = list(external_dict.keys())
    print(f"   -> Loaded {len(external_names)} exercises from GitHub.\n")

    print("2. Loading local database...")
    if not os.path.exists(local_file_path):
        print(f"Error: Could not find {local_file_path}")
        return

    with open(local_file_path, 'r', encoding='utf-8') as f:
        local_db = json.load(f)

    # Determine shape of JSON
    if isinstance(local_db, dict):
        if 'exercises' in local_db: exercise_list = local_db['exercises']
        elif 'results' in local_db: exercise_list = local_db['results']
        else: exercise_list = list(local_db.values())
    else:
        exercise_list = local_db

    print(f"   -> Found {len(exercise_list)} exercises in local database.\n")
    print("3. Starting Multi-Tier matching process...")

    updated_count = 0
    missed = []

    if len(exercise_list) > 0 and not get_exercise_name(exercise_list[0]):
        print("\n🚨 CRITICAL ERROR: Could not find the name key in your JSON.")
        return

    for ex in exercise_list:
        if not isinstance(ex, dict): continue
            
        raw_local_name = get_exercise_name(ex)
        c_local_name = clean_name(raw_local_name)
        
        # Clean up old keys
        for old_key in ['card_image', 'image_url', 'gif_url']:
            if old_key in ex: del ex[old_key]
        
        # TIER 1: Exact match
        if c_local_name in external_dict:
            ex['animation_frames'] = external_dict[c_local_name]
            updated_count += 1
            print(f" [EXACT] {raw_local_name} --> mapped to --> {c_local_name.title()}")
            continue

        # TIER 2: Substring / Containment Match
        subset_matches = [en for en in external_names if c_local_name in en or en in c_local_name]
        if subset_matches:
            best_subset = difflib.get_close_matches(c_local_name, subset_matches, n=1, cutoff=0.1)
            best_match = best_subset[0] if best_subset else subset_matches[0]
            
            ex['animation_frames'] = external_dict[best_match]
            updated_count += 1
            print(f" [SUBSTRING] {raw_local_name}  --> mapped to -->  {best_match.title()}")
            continue

        # TIER 3: Stricter Fuzzy Match
        matches = difflib.get_close_matches(c_local_name, external_names, n=1, cutoff=0.72)
        if matches:
            ex['animation_frames'] = external_dict[matches[0]]
            updated_count += 1
            print(f" [FUZZY] {raw_local_name}  --> mapped to -->  {matches[0].title()}")
        else:
            ex['animation_frames'] = []
            missed.append(raw_local_name)

    # Save
    with open(local_file_path, 'w', encoding='utf-8') as f:
        json.dump(local_db, f, indent=4)

    print("\n========================================")
    print(f"✅ Successfully added highly-accurate animations to {updated_count} exercises!")
    if missed:
        print(f"⚠️ Could not safely match {len(missed)} exercises:")
        for m in missed[:10]: print(f"   - {m}")
    print("========================================")

if __name__ == "__main__":
    update_exercise_animations()