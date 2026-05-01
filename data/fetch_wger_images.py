import json
import requests
import difflib

def fetch_wger_data():
    print("1. Fetching exercise list from Wger API...")
    ex_url = "https://wger.de/api/v2/exercise/?language=2&limit=1000"
    exercises_response = requests.get(ex_url).json()
    
    wger_exercises = {}
    for ex in exercises_response.get('results', []):
        # Using .get() safely ignores broken API entries that don't have a name
        name = ex.get('name')
        base_id = ex.get('exercise_base')
        
        # Only map it if both the name and base_id actually exist
        if name and base_id:
            wger_exercises[base_id] = name

    print("2. Fetching image list from Wger API...")
    img_url = "https://wger.de/api/v2/exerciseimage/?is_main=True&limit=1000"
    images_response = requests.get(img_url).json()

    # Create a mapping of Wger Exercise Name -> Image URL
    wger_name_to_image = {}
    for img in images_response.get('results', []):
        base_id = img.get('exercise_base')
        image_url = img.get('image')
        
        # Match the image back to the exercise name we safely grabbed earlier
        if base_id in wger_exercises and image_url:
            ex_name = wger_exercises[base_id]
            wger_name_to_image[ex_name.lower()] = image_url

    return wger_name_to_image

def enrich_your_json_with_images():
    wger_name_to_image = fetch_wger_data()
    wger_titles = list(wger_name_to_image.keys())

    print("3. Loading your exercises_enriched.json...")
    try:
        with open('exercises_enriched.json', 'r', encoding='utf-8') as f:
            your_dataset = json.load(f)
    except FileNotFoundError:
        print("Error: exercises_enriched.json not found in this folder.")
        return

    print("4. Fuzzy matching and merging images...")
    match_count = 0
    
    for key, data in your_dataset.items():
        name = data.get('exercise_name', '').lower()
        
        # Fuzzy match your exercise name to Wger's exercise name
        matches = difflib.get_close_matches(name, wger_titles, n=1, cutoff=0.4)
        
        if matches:
            best_match = matches[0]
            data['card_image'] = wger_name_to_image[best_match]
            match_count += 1
        else:
            # Fallback for highly specific machine exercises Wger might not have
            data['card_image'] = "https://placehold.co/400x400/f8fafc/94a3b8?text=Illustration+Pending"

    print(f"Successfully matched {match_count} out of {len(your_dataset)} exercises!")

    print("5. Saving back to exercises_enriched.json...")
    with open('exercises_enriched.json', 'w', encoding='utf-8') as f:
        json.dump(your_dataset, f, indent=4)
        
    print("Done! Your JSON is now packed with Wger images.")

if __name__ == "__main__":
    enrich_your_json_with_images()