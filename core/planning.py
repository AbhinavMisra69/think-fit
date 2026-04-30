from .nutrition import NutritionCalculator

class DietProjector:
    """Maps out the long-term timeline from current weight to target weight."""
    
    @classmethod
    def generate_roadmap(cls, user_profile: dict, target_weight_kg: float, max_weeks: int = 52) -> dict:
        """
        Simulates the diet week-by-week, showing how TDEE and targets 
        shrink as the user loses weight.
        """
        timeline = []
        current_weight = user_profile["inputs"]["weight_kg"]
        goal = user_profile["inputs"]["goal"]
        rate = user_profile["inputs"]["rate"]
        
        # We need these constants from the user's initial setup
        sex = user_profile["inputs"]["sex"]
        age = user_profile["inputs"]["age"]
        height_cm = user_profile["inputs"]["height_cm"]
        activity_level = user_profile["inputs"]["activity_level"]

        week = 1
        while week <= max_weeks:
            # 1. Recalculate everything for the CURRENT weight
            bmr = NutritionCalculator.calculate_bmr(sex, age, current_weight, height_cm)
            tdee = NutritionCalculator.calculate_tdee(bmr, activity_level)
            daily_cals = NutritionCalculator.calculate_daily_calories(tdee, current_weight, goal, rate)
            macros = NutritionCalculator.calculate_macros(current_weight, daily_cals, goal)

            # 2. Record the week's stats
            timeline.append({
                "week": week,
                "projected_weight_kg": round(current_weight, 2),
                "tdee": round(tdee),
                "target_calories": round(daily_cals),
                "macros": macros
            })

            # 3. Simulate the weight change for next week
            # 1 kg of fat is roughly 7700 kcal
            daily_deficit = tdee - daily_cals
            weekly_deficit = daily_deficit * 7
            weight_lost = weekly_deficit / 7700
            
            if goal == "fat loss":
                current_weight -= weight_lost
                if current_weight <= target_weight_kg:
                    break
            elif goal == "muscle gain":
                # Assuming surplus leads to gain (simplified: 1kg tissue ~ 7700 surplus)
                current_weight += abs(weight_lost) 
                if current_weight >= target_weight_kg:
                    break

            week += 1

        return {
            "target_hit": current_weight <= target_weight_kg if goal == "fat loss" else current_weight >= target_weight_kg,
            "weeks_required": week,
            "timeline": timeline
        }


class AdaptiveCoach:
    """The algorithm that runs every week when the user logs their comprehensive check-in data."""
    
    @classmethod
    def weekly_check_in(cls, 
                        previous_weight: float, current_weight: float, 
                        previous_bf_pct: float, current_bf_pct: float,
                        previous_measurements: dict, current_measurements: dict,
                        current_daily_cals: float, goal: str, expected_loss_rate: str) -> dict:
        
        # 1. Calculate General Deltas (Negative means a decrease)
        weight_diff = current_weight - previous_weight
        bf_diff = current_bf_pct - previous_bf_pct
        
        # 2. Calculate Specific Measurement Deltas
        # Defaults to 0 if the user skipped a measurement that week
        waist_diff = current_measurements.get("waist_cm", 0) - previous_measurements.get("waist_cm", 0)
        chest_diff = current_measurements.get("chest_cm", 0) - previous_measurements.get("chest_cm", 0)
        arm_diff = current_measurements.get("arm_cm", 0) - previous_measurements.get("arm_cm", 0)
        thigh_diff = current_measurements.get("thigh_cm", 0) - previous_measurements.get("thigh_cm", 0)

        # Aggregate muscle indicator metrics (Chest + Arms + Thighs)
        muscle_indicator_diff = chest_diff + arm_diff + thigh_diff

        # Base calculations for expected weight drop
        rate_percentages = {"slow": 0.005, "moderate": 0.007, "fast": 0.01}
        rate_pct = rate_percentages.get(expected_loss_rate.lower(), 0.007)
        expected_weekly_loss = previous_weight * rate_pct

        adjustment_needed = False
        new_calories = current_daily_cals
        message = "Metrics look great. Keep executing the plan."
        status = "PROGRESSING"

        # --- GOAL: FAT LOSS ---
        if goal == "fat loss":
            
            # SCENARIO A: Body Recomposition (Weight stalled, but dropping fat / gaining muscle)
            # Trigger: Weight loss is slow, BUT body fat dropped OR waist dropped while limbs grew/maintained.
            if abs(weight_diff) < (expected_weekly_loss * 0.5) and (bf_diff < -0.2 or (waist_diff < -0.5 and muscle_indicator_diff >= 0)):
                adjustment_needed = False
                status = "RECOMPOSITION"
                message = "The scale is moving slowly, but your body fat and waist are dropping while your muscle measurements are holding strong. You are experiencing body recomposition. Do NOT drop calories."
            
            # SCENARIO B: Crashing / Muscle Loss Alert
            # Trigger: Losing weight rapidly, BUT limbs/chest are shrinking fast while waist/BF% barely moves.
            elif weight_diff < -(expected_weekly_loss * 1.5) and muscle_indicator_diff < -1.5 and bf_diff > -0.1:
                adjustment_needed = True
                new_calories = current_daily_cals + 150 
                status = "MUSCLE_LOSS_ALERT"
                message = "You are dropping weight too fast, and your limb measurements are shrinking without a drop in body fat. Adding 150 calories to protect your muscle tissue."

            # SCENARIO C: True Plateau
            # Trigger: Weight stalled, BF% stalled, all measurements stalled.
            elif abs(weight_diff) < (expected_weekly_loss * 0.3) and bf_diff >= 0 and waist_diff >= 0:
                adjustment_needed = True
                new_calories = current_daily_cals - 100 
                status = "PLATEAU"
                message = "True plateau detected across the scale, body fat, and tape measurements. Dropping calories slightly to break the metabolic adaptation."

        # --- GOAL: MUSCLE GAIN ---
        elif goal == "muscle gain":
            
            # SCENARIO D: Lean Bulk (The Ideal)
            # Trigger: Gaining weight, muscle measurements going up, waist and BF% stable.
            if weight_diff > 0 and muscle_indicator_diff > 0 and waist_diff <= 0.5 and bf_diff <= 0.2:
                adjustment_needed = False
                status = "LEAN_BULK"
                message = "Textbook lean bulk. Your limbs and chest are growing, but your waist and body fat are stable. Perfect surplus."

            # SCENARIO E: Dirty Bulk / Fat Spike
            # Trigger: Gaining weight, but waist and BF% are spiking.
            elif weight_diff > 0 and (bf_diff > 0.5 or waist_diff > 1.0):
                adjustment_needed = True
                new_calories = current_daily_cals - 150
                status = "FAT_SPIKE"
                message = "You are gaining mass, but your waist and body fat are rising too quickly. Dialing back the surplus to keep the gains lean."
                
            # SCENARIO F: Hardgainer Plateau
            # Trigger: Weight and all measurements are completely flat.
            elif weight_diff <= 0 and muscle_indicator_diff <= 0:
                adjustment_needed = True
                new_calories = current_daily_cals + 150
                status = "PLATEAU"
                message = "No growth detected. Your body has adapted to the current calories. Bumping the fuel up to force new tissue growth."

        # Safety Net: Never let calories drop below a basal metabolic floor
        minimum_safe_cals = 1500 
        if new_calories < minimum_safe_cals:
            new_calories = minimum_safe_cals
            if status == "PLATEAU":
                message = "Plateau detected, but calories are at the absolute safe floor. Do not eat less. We recommend increasing your daily step count by 2,000 steps instead of cutting food."

        return {
            "status": status,
            "adjustment_made": adjustment_needed,
            "new_daily_calories": round(new_calories),
            "coach_feedback": message,
            "metrics_logged": {
                "weight_change_kg": round(weight_diff, 2),
                "bf_pct_change": round(bf_diff, 2),
                "waist_cm_change": round(waist_diff, 2),
                "muscle_indicator_change_cm": round(muscle_indicator_diff, 2)
            }
        }