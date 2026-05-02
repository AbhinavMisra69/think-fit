from datetime import datetime, timezone

def calculate_dynamic_weeks_off(last_workout_date):
    """
    Takes the PostgreSQL timestamp and calculates how many full weeks 
    have passed since the user last worked out.
    """
    if not last_workout_date:
        return 0 # Brand new user, no weeks off
        
    # Ensure we are using UTC to match the database timezone
    now = datetime.now(timezone.utc)
    
    # Calculate the time difference
    time_delta = now - last_workout_date
    
    # Convert total days to full weeks (using floor division)
    weeks_off = time_delta.days // 7
    
    # We only trigger detraining protocols if it's been 2 or more weeks
    # (1 week off is just a normal deload/rest week)
    return weeks_off if weeks_off >= 2 else 0
