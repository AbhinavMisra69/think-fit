import csv
import difflib
import json
from exercises import exercise_dataset # Imports your massive dictionary

def enrich_exercises():
    print("Loading CSV data...")
    csv_data = {}
    
    # 1. Read the CSV and map Titles to Descriptions
    try:
        with open('workout/megaGymDataset.csv', mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Store lowercase title for easier matching
                csv_data[row['Title'].lower()] = row['Desc']
    except FileNotFoundError:
        print("Error: Could not find megaGymDataset.csv in this folder.")
        return

    print("Matching exercises and merging descriptions...")
    csv_titles = list(csv_data.keys())
    
    # 2. Iterate through your dataset
    for key, data in exercise_dataset.items():
        name = data['exercise_name'].lower()
        
        # 3. Use fuzzy string matching to find the closest CSV title
        # cutoff=0.6 means it needs to be a 60% match to prevent completely wrong descriptions
        matches = difflib.get_close_matches(name, csv_titles, n=1, cutoff=0.6)
        
        if matches:
            best_match = matches[0]
            description = csv_data[best_match]
            # Clean up empty CSV fields
            data['description'] = description if description.strip() else "Description coming soon."
        else:
            # Fallback if the CSV doesn't have a match for your specific exercise
            data['description'] = "Description coming soon."

    # 4. Save the updated dataset as a JSON file
    # JSON is vastly superior here because you can directly import it into Next.js!
    with open('exercises_enriched.json', 'w', encoding='utf-8') as f:
        json.dump(exercise_dataset, f, indent=4)
        
    print("Success! Created exercises_enriched.json with all descriptions merged.")

if __name__ == "__main__":
    enrich_exercises()