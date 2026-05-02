# thinkfit_engine.py
import json
from .database import  blueprint_library, phase_parameters_kb, macrocycle_kb
import os

# 2. Build the path to the JSON file
# 1. Get the directory where THIS Python file lives (e.g., your_project/api)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Go UP one folder to the main project root (e.g., your_project/)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# 3. Build the exact path to the JSON file
EXERCISE_DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'exercises_enriched.json')

# 3. Load the file into a Python dictionary
try:
    with open(EXERCISE_DATA_PATH, 'r') as f:
        exercise_dataset = json.load(f)
    print(f"Successfully loaded {len(exercise_dataset)} exercises from JSON.")
except FileNotFoundError:
    print(f"CRITICAL ERROR: Could not find {EXERCISE_DATA_PATH}. Make sure the file exists!")
    exercise_dataset = {} # Fallback to prevent immediate crashes

# ==========================================
# 1. HELPERS & SCHEDULERS
# ==========================================

def calculate_next_workout(exercise_name, is_compound, last_week_data, phase_params):
    """
    Calculates progressive overload, using phase-aware logic for baselines.
    """

    # If they've never done the exercise, baseline it
    # --- YOUR PHASE-AWARE LOGIC BECOMES THE BASELINE ---
    if "compound_sets" in phase_params:
        base_sets = phase_params["compound_sets"] if is_compound else phase_params["isolation_sets"]
        base_rep_str = phase_params["compound_reps"] if is_compound else phase_params["isolation_reps"]
    else:
        base_sets = phase_params.get("default_sets", 3)
        base_rep_str = phase_params.get("rep_range", "8-12")
        
    # Convert rep string (e.g., "8-12") to integers
    try:
        min_reps, max_reps = map(int, str(base_rep_str).split("-"))
    except ValueError:
        min_reps, max_reps = 8, 12 # Fallback for AMRAPs

    # --- WEEK 1: NO HISTORY ---
    if not last_week_data:
        return {
            "target_sets": base_sets,
            "target_reps": min_reps, # Start at the bottom of the allowed range
            "target_weight": "Determine 1RM / RPE 7" 
        }

    # --- WEEK 2+: PROGRESSIVE OVERLOAD ---
    last_weight = last_week_data["weight"]
    last_sets = last_week_data["sets"]
    last_reps = last_week_data["reps_achieved"]
    progression_style = phase_params.get("execution_style", "double_progression")

    next_workout = {
        "target_sets": last_sets,
        "target_reps": last_reps,
        "target_weight": last_weight
    }

    # LOGIC 1: DOUBLE PROGRESSION (Recomp / Fat Loss Bias)
    if "recomp" in progression_style or "hypertrophy" in progression_style or "double_progression" in progression_style:
        if last_reps >= max_reps:
            # They hit the ceiling! Increase weight, drop reps back to the floor.
            next_workout["target_weight"] = last_weight + 5 
            next_workout["target_reps"] = min_reps
        else:
            # They haven't hit the ceiling. Push them to get more reps with the same weight.
            next_workout["target_reps"] = min(last_reps + 1, max_reps)

    # LOGIC 2: LINEAR PROGRESSION (Strength Block / Foundation)
    elif "strength" in progression_style or "linear" in progression_style or "barbell" in progression_style:
        # Strength blocks usually force weight up while keeping reps static (e.g., 5x5)
        if last_reps >= min_reps: # As long as they hit the minimum required reps
            next_workout["target_weight"] = last_weight + 5
            next_workout["target_reps"] = min_reps # Keep it at the target
        else:
             # They failed to hit the minimum reps last week. Deload or hold.
            next_workout["target_weight"] = last_weight

    # LOGIC 3: VOLUME ACCUMULATION
    elif "volume" in progression_style:
        # Keep weight and reps the same, but add a set (up to a ceiling, e.g., 5 sets)
        if last_sets < 5:
            next_workout["target_sets"] = last_sets + 1

    return next_workout



def generate_custom_timeline(goal, preferred_duration_weeks, macro_kb):
    """
    Dynamically scales a periodization model using a linear round-robin algorithm,
    enforcing a strict minimum of 3 weeks for core adaptable phases.
    """
    if preferred_duration_weeks < 6:
        return {
            "status": "rejected", 
            "message": "Unrealistic timeline. A minimum of 6 weeks is required."
        }
        
   # RULE 2: Baseline Selection
    # If they want 12 weeks or less, base it on the 2-month (8-week) model.
    # If they want 13 weeks or more, base it on the 4-month (16-week) model.
    baseline_key = "2_months" if preferred_duration_weeks < 12 else "4_months"
    
    baseline_model = [dict(phase) for phase in macro_kb.get(goal, macro_kb["recomposition"])[baseline_key]]
    
    current_total_weeks = sum(p["base_weeks"] for p in baseline_model)
    delta_weeks = preferred_duration_weeks - current_total_weeks

    step = 1 if delta_weeks > 0 else -1
    phases_adjusted = 0
    
    # THE ROUND-ROBIN DISTRIBUTION LOOP
    while phases_adjusted < abs(delta_weeks):
        made_an_adjustment = False
        
        # Iterate FORWARD through the phases (Phase 1, then Phase 2, then Phase 3...)
        for i in range(len(baseline_model)):
            if phases_adjusted == abs(delta_weeks):
                break
                
            if step == -1: # IF WE ARE SHRINKING
                # YOUR NEW RULE: Cannot decrease a phase if it is 3 weeks or less
                if baseline_model[i]["base_weeks"] <= 3:
                    continue
            else: # IF WE ARE STRETCHING
                # Safety constraint: don't let a single phase stretch past 8 weeks
                if baseline_model[i]["base_weeks"] >= 8:
                    continue
                    
            # Apply the adjustment
            baseline_model[i]["base_weeks"] += step
            phases_adjusted += 1
            made_an_adjustment = True
            
        # If we loop through all phases and can't adjust anything safely, reject it.
        if not made_an_adjustment:
            return {
                "status": "rejected",
                "message": f"Timeline constrained. Cannot compress to {preferred_duration_weeks} weeks without violating the 3-week phase minimum."
            }

    # Rebuild the final timeline with the new calculated end_weeks
    running_total = 0
    custom_timeline = []
    
    for phase_data in baseline_model:
        running_total += phase_data["base_weeks"]
        custom_timeline.append({
            "phase": phase_data["phase"],
            "end_week": running_total
        })

    return {"status": "success", "timeline": custom_timeline}

def determine_active_phase(working_memory, macrocycle_kb):
    goal = working_memory.get("primary_goal", "recomposition")
    weeks_in = working_memory.get("weeks_in_program", 1)
    target_duration = working_memory.get("preferred_duration_weeks", 16) # User inputs this
    
    # Generate the perfectly scaled timeline
    timeline_response = generate_custom_timeline(goal, target_duration, macrocycle_kb)
    
    if timeline_response["status"] == "rejected":
        # Handle the rejection (in your frontend, you would show the message to the user)
        print(f"WARNING: {timeline_response['message']}")
        # Fallback to the standard 16-week model
        timeline_response = generate_custom_timeline(goal, 16, macrocycle_kb)
        
    custom_timeline = timeline_response["timeline"]
    
    # Modulo loops them if they decide to keep going after their target duration ends
    cycle_week = ((weeks_in - 1) % target_duration) + 1 
    
    for block in custom_timeline:
        if cycle_week <= block["end_week"]:
            return block["phase"]
            
    return custom_timeline[-1]["phase"]



#trigger if i. the user didn't login for 2 weeks or more ii. the goal has be acheived 
def handle_transitions_and_detraining(working_memory, macrocycle_kb):
    """
    Executes the post-program routing and detraining decision tree.
    """
    current_goal = working_memory.get("primary_goal", "recomposition")
    current_phase = working_memory.get("active_phase")
    weeks_off = working_memory.get("weeks_off", 0)
    
    progression_track = macrocycle_kb.get(current_goal, macrocycle_kb["recomposition"])["4_months"]
    
    current_idx = 0
    for i, block in enumerate(progression_track):
        if block["phase"] == current_phase:
            current_idx = i
            break

    # ==========================================
    # BRANCH 1: THE DETRAINING PROTOCOL
    # ==========================================
    if weeks_off > 0:
        if weeks_off < 2:
            return current_phase 
            
        elif 2 <= weeks_off <= 4:
            new_idx = max(0, current_idx - 1)
            return progression_track[new_idx]["phase"]
            
        else:
            new_idx = max(0, current_idx - 2)
            experience = working_memory.get("experience_level", "beginner")
            if experience != "beginner" and progression_track[new_idx]["phase"] in ["foundation", "strength_foundation"]:
                new_idx = 1 
                
            return progression_track[new_idx]["phase"]


    # ==========================================
    # BRANCH 2: PROGRAM DURATION ENDS
    # ==========================================
    program_ended = working_memory.get("program_ended", False)
    
    if program_ended:
        goal_achieved = working_memory.get("goal_achieved", False)
        
        if goal_achieved:
            new_goal = working_memory.get("new_goal")
            
            if new_goal and new_goal != current_goal:
                new_track = macrocycle_kb.get(new_goal)["4_months"]
                working_memory["primary_goal"] = new_goal 
                return new_track[1]["phase"] 
                
            else:
                if current_goal == "general_health":
                    return "sustain"
                else:
                    return progression_track[-1]["phase"] 
                    
        else:
            # THE UPGRADE: Goal NOT achieved -> Extend program dynamically
            current_duration = working_memory.get("preferred_duration_weeks", 16)
            working_memory["preferred_duration_weeks"] = current_duration + 4
            
            # Reset the program_ended flag so the loop can continue naturally
            working_memory["program_ended"] = False 
            
            return current_phase

    # Default fallback
    return current_phase



def get_highest_tier_score(exercise_details):
    tier_weights = {"S_Plus": 5, "S_Tier": 4, "A_Tier": 3, "B_Tier": 2}
    best_score = 0
    tiers_dict = exercise_details.get("periodization_tags", {}).get("hypertrophy_tiers", {})
    
    for muscle, tier_string in tiers_dict.items():
        score = tier_weights.get(tier_string, 1)
        if score > best_score:
            best_score = score
            
    return best_score


def check_consecutive_days(schedule_array):
    """Checks if the user trains 3 or more days in a row to prevent CNS burnout."""
    day_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
    days = sorted([day_map[day] for day in schedule_array])
    
    # Check for 3 days in a row (e.g., 0, 1, 2)
    for i in range(len(days) - 2):
        if days[i+1] == days[i] + 1 and days[i+2] == days[i] + 2:
            return True
            
    # Wrap-around check (Saturday, Sunday, Monday -> 5, 6, 0)
    if 5 in days and 6 in days and 0 in days:
        return True
        
    return False

def determine_weekly_split(working_memory, phase_base_split):
    """
    Takes the ideal split required by the periodization phase, and intelligently 
    adapts it to fit the user's actual available days, overriding dangerous setups.
    """
    schedule = working_memory.get("schedule", ["Monday", "Thursday"])
    days_count = len(schedule)
    
    # Initialize a warnings array in memory so the frontend app can display alerts
    if "system_warnings" not in working_memory:
        working_memory["system_warnings"] = []
    
    # 1. Full Body & Circuits 
    if phase_base_split in ["full_body", "full_body_circuit", "mixed_modal_circuit"]:
        return phase_base_split
        
    # 2. Adapting Upper/Lower Blocks
    if phase_base_split == "upper_lower":
        if days_count <= 2:
            # THE OVERRIDE
            working_memory["system_warnings"].append(
                "This phase is optimized for at least 3 days. To ensure you hit every muscle twice a week for better results, we have temporarily switched your 2 days to Full Body."
            )
            return "full_body"
        elif days_count == 3:
            return "upper_lower_full" 
        elif days_count == 4:
            return "upper_lower_repeated" 
        elif days_count >= 5:
            return "upper_lower_upper_lower_full" 
            
    # 3. Adapting Push/Pull/Legs Blocks
    if phase_base_split == "push_pull_legs":
        if days_count <= 2:
            # THE OVERRIDE
            working_memory["system_warnings"].append(
                "This phase requires at least 3 days to complete a full Push/Pull/Legs cycle. To prevent muscle imbalances, we have temporarily switched your 2 days to Full Body."
            )
            return "full_body"
        elif days_count == 3:
            return "push_pull_legs" 
        elif days_count == 4:
            return "push_pull_repeated" 
        elif days_count == 5:
            return "upper_lower_push_pull_legs" 
        elif days_count == 6:
            return "push_pull_legs_repeated" 

    # Fallback safety
    return "full_body"


# Notice we added working_memory as the first parameter
def schedule_weekly_blueprints(working_memory, assigned_split):
    """
    Maps days of the week to the correct anatomical blueprint using an infinite rolling queue.
    Prevents restarting the split at the beginning of every week.
    """
    # Pull the schedule directly from the passed memory
    schedule_array = working_memory.get("schedule", ["Monday", "Wednesday", "Friday"])
    
    split_sequences = {
        "full_body": ["full_body_A", "full_body_B", "full_body_C"],
        "upper_lower": ["upper_day", "lower_day"],
        "push_pull_legs": ["push_day", "pull_day", "leg_day"],
        "upper_lower_full": ["upper_day", "lower_day", "full_body_A"],
        "upper_lower_repeated": ["upper_day", "lower_day"],
        "push_pull_repeated": ["push_day", "pull_day"], 
        "upper_lower_upper_lower_full": ["upper_day", "lower_day", "upper_day", "lower_day", "full_body_A"],
        "upper_lower_push_pull_legs": ["upper_day", "lower_day", "push_day", "pull_day", "leg_day"],
        "push_pull_legs_repeated": ["push_day", "pull_day", "leg_day"],
    }
    
    sequence = split_sequences.get(assigned_split, ["full_body_A"])
    
    # Safely reference the local working_memory
    if working_memory.get("last_assigned_split") != assigned_split:
        working_memory["split_rotation_index"] = 0
        working_memory["last_assigned_split"] = assigned_split
        
    current_index = working_memory.get("split_rotation_index", 0)
    
    calendar = {}
    for day in schedule_array:
        day_type = sequence[current_index % len(sequence)]
        calendar[day] = day_type
        current_index += 1
        
    # Lock the pointer into the local memory dictionary
    working_memory["split_rotation_index"] = current_index
    
    return calendar




# ==========================================
# 2. THE ELIMINATION FILTERS
# ==========================================
def apply_rule_W1_equipment(memory, raw_dataset):
    tier_hierarchy = {"home": 1, "basic_gym": 2, "pro_gym": 3}
    user_tier = tier_hierarchy.get(memory.get("facility_type", "home"), 1)
    user_tools = set(memory.get("owned_equipment", []))
    
    safe_db = {}
    for ex_name, details in raw_dataset.items():
        req_tier = tier_hierarchy.get(details.get("facility_requirements", {}).get("facility_tier", "home"), 1)
        req_tools = set(details.get("facility_requirements", {}).get("specific_tools", []))
        
        if user_tier >= req_tier and req_tools.issubset(user_tools):
            safe_db[ex_name] = details
    return safe_db

def apply_rule_W2_injuries(user_injuries, safe_db):
    injury_stress_map = {
        "lower_back": ["spinal_compression", "lumbar_shear"],
        "knee": ["extreme_knee_torque", "high_knee_torque"]
    }
    tags_to_avoid = set()
    for injury in user_injuries:
        if injury in injury_stress_map:
            tags_to_avoid.update(injury_stress_map[injury])
            
    completely_safe_db = {}
    for ex_name, details in safe_db.items():
        exercise_stress = set(details.get("biomechanics", {}).get("joint_stress", []))
        if not exercise_stress.intersection(tags_to_avoid):
            completely_safe_db[ex_name] = details
    return completely_safe_db

def apply_rule_W8_phase(current_phase, safe_db):
    """
    Translates the highly specific programming phases into the broader 
    database tags so the AI doesn't accidentally delete valid exercises.
    """
    # The Translation Dictionary
    phase_aliases = {
        # Programming Phase  ->  [Accepted Database Tags]
        "foundation":            ["foundation"],
        "strength_foundation":   ["foundation"],     # Maps to the broad tag
        "recomposition_1":       ["recomposition"],  # Maps to the broad tag
        "recomposition_2":       ["recomposition"],  # Maps to the broad tag
        "peak_recomposition":    ["recomposition"],  # Maps to the broad tag
        
        # Ensure your other phases map correctly based on your find/replace
        "foundation_hypertrophy":["foundation", "hypertrophy_volume"],
        "volume_surge":          ["hypertrophy_volume"],
        "peak_volume":           ["hypertrophy_volume"],
        "strength_block":        ["strength_block"],
        "active_lifestyle":      ["active_lifestyle", "build_and_burn"],
        "build_and_burn":        ["build_and_burn"],
        "intensify":             ["intensify", "strength_block"],
        "metabolic_conditioning":["peak_metabolic"],
        "endurance_and_strength":["strength_block", "active_lifestyle"],
        "sustain":               ["active_lifestyle"]
    }
    
    # Get the list of allowed database tags for the current programming phase
    valid_tags = phase_aliases.get(current_phase, [current_phase])
    
    phase_accurate_db = {}
    for ex_name, details in safe_db.items():
        # Safely extract the allowed phases from the exercise entry
        tags_dict = details.get("periodization_tags", {})
        allowed_phases = tags_dict.get("allowed_phases", [])
        
        # If any of the translated tags match the exercise's tags, let it pass
        if any(tag in allowed_phases for tag in valid_tags) or "all" in allowed_phases:
            phase_accurate_db[ex_name] = details
            
    return phase_accurate_db

# ==========================================
# 3. THE ASSEMBLY ENGINE
# ==========================================
def apply_rule_W3_prehab(user_injuries, safe_db):
    prehab_routine = []
    for ex_name, details in safe_db.items():
        if any(injury in details.get("biomechanics", {}).get("pre_hab_for", []) for injury in user_injuries):
            prehab_routine.append({
                "exercise": details["exercise_name"],
                "type": "pre_hab_warmup",
                "sets": 2, "reps": "12-15"
            })
    return prehab_routine[:2]

# Added user_workout_history as the 4th parameter
def apply_rule_W6_assembly(safe_db, blueprint, phase_params, user_workout_history):
    main_routine = []
    muscles_hit_today = set() 
    
    for required_pattern, required_amount in blueprint.items():
        matching = [(k, v) for k, v in safe_db.items() if v.get("muscle_data", {}).get("movement_pattern") == required_pattern]
        
        if not matching:
            main_routine.append({
                "exercise": f"System Notice: No safe exercises found for {required_pattern}",
                "pattern": required_pattern,
                "sets": 0, "reps": "N/A"
            })
            continue 
            
        def dynamic_score(ex_tuple):
            base_score = get_highest_tier_score(ex_tuple[1])
            primary_targets = set(ex_tuple[1].get("muscle_data", {}).get("primary_targets", []))
            primary_overlap = primary_targets.intersection(muscles_hit_today)
            secondary_targets = set(ex_tuple[1].get("muscle_data", {}).get("secondary_muscles", []))
            secondary_overlap = secondary_targets.intersection(muscles_hit_today)
            penalty = (len(primary_overlap) * 2) + (len(secondary_overlap) * 1)
            return base_score - penalty

        matching.sort(key=dynamic_score, reverse=True)
        
        selected_count = 0
        for ex_name, details in matching:
            if selected_count >= required_amount: break
            
            is_compound = details.get("muscle_data", {}).get("is_compound", False)
            
            # Now we use the dictionary passed into the function!
            past_data = user_workout_history.get(details["exercise_name"], None)
            
            next_targets = calculate_next_workout(
                details["exercise_name"], 
                is_compound, 
                past_data, 
                phase_params
            )
            
        
            main_routine.append({
                "exercise_name": details["exercise_name"], # Fixed name!
                "pattern": required_pattern,
                "sets": next_targets["target_sets"],
                "reps": next_targets["target_reps"],
                "target_weight": next_targets["target_weight"],
                "rest_sec": phase_params.get("rest_seconds", 90),
                "style": phase_params.get("execution_style", "straight_sets"),
                
                # --- ADD THE RICH DATA FOR REACT ---
                "muscle_data": details.get("muscle_data", {"primary_targets": [], "movement_pattern": required_pattern}),
                "youtube_id": details.get("youtube_id", ""),
                "description": details.get("description", ""),
                "biomechanics": details.get("biomechanics", {"joint_stress": []}),
                "facility_requirements": details.get("facility_requirements", {"specific_tools": []}),
                "periodization_tags": details.get("periodization_tags", {})
            })
            
            muscles_hit_today.update(details.get("muscle_data", {}).get("primary_targets", []))
            selected_count += 1
            
    return main_routine

# ==========================================
# 4. THE MASTER ORCHESTRATOR
# ==========================================
# Added user_workout_history as the 5th parameter
def generate_daily_workout(memory, dataset, blueprint, params, user_workout_history):
    user_injuries = memory.get("medical_issues", [])
    active_phase = memory.get("active_phase", "foundation")
    
    db_w1 = apply_rule_W1_equipment(memory, dataset)
    db_w2 = apply_rule_W2_injuries(user_injuries, db_w1)
    final_db = apply_rule_W8_phase(active_phase, db_w2)
    
    warmup = apply_rule_W3_prehab(user_injuries, final_db)
    
    for warmup_exercise in warmup:
        keys_to_remove = [k for k, v in final_db.items() if v["exercise_name"] == warmup_exercise["exercise"]]
        for k in keys_to_remove:
            del final_db[k]
    
    # Pass it into the assembly engine
    main_workout = apply_rule_W6_assembly(final_db, blueprint, params, user_workout_history)
    
    return warmup + main_workout