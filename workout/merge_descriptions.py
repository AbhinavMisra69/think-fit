import csv
import difflib
import json
import time
import urllib.request
import urllib.parse
import re
from exercises import exercise_dataset

def get_youtube_id(query):
    """Scrapes the first YouTube search result ID using built-in Python."""
    query = urllib.parse.quote(query)
    url = f"https://www.youtube.com/results?search_query={query}"
    try:
        html = urllib.request.urlopen(url)
        # Search the raw HTML for the first instance of a video ID
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        if video_ids:
            return video_ids[0]
        return None
    except Exception as e:
        print(f"Error fetching {query}: {e}")
        return None

def enrich_exercises():
    print("Loading CSV data...")
    csv_data = {}
    
    try:
        with open('workout/megaGymDataset.csv', mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                csv_data[row['Title'].lower()] = row['Desc']
    except FileNotFoundError:
        print("Error: Could not find megaGymDataset.csv in this folder.")
        return

    print("Matching exercises, merging descriptions, and fetching videos...")
    csv_titles = list(csv_data.keys())
    
    for key, data in exercise_dataset.items():
        name = data['exercise_name'].lower()
        
        # --- A. DESCRIPTION MATCHING ---
        matches = difflib.get_close_matches(name, csv_titles, n=1, cutoff=0.6)
        if matches:
            best_match = matches[0]
            description = csv_data[best_match]
            data['description'] = description if description.strip() else "Description coming soon."
        else:
            data['description'] = "Description coming soon."

        # --- B. YOUTUBE VIDEO FETCHING (NATIVE SCRAPING) ---
        print(f"Fetching video for: {data['exercise_name']}...")
        search_query = f"{data['exercise_name']} exercise tutorial"
        
        video_id = get_youtube_id(search_query)
        data['youtube_id'] = video_id

        # Pause to prevent YouTube from blocking your IP
        time.sleep(1) 

    # Save the updated dataset
    with open('exercises_enriched.json', 'w', encoding='utf-8') as f:
        json.dump(exercise_dataset, f, indent=4)
        
    print("Success! Created exercises_enriched.json with all descriptions and YouTube IDs merged.")

if __name__ == "__main__":
    enrich_exercises()