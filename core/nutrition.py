class NutritionCalculator:
    ACTIVITY_MULTIPLIERS = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "extremely active": 1.9,
    }

    @staticmethod
    def convert_height_to_cm(feet: int, inches: int) -> float:
        return (feet * 30.48) + (inches * 2.54)

    @classmethod
    def calculate_bmr(cls, sex: str, age: int, weight_kg: float, height_cm: float) -> float:
        base_bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age)
        return base_bmr + 5 if sex.lower() == 'male' else base_bmr - 161

    @classmethod
    def calculate_tdee(cls, bmr: float, activity_level: str) -> float:
        multiplier = cls.ACTIVITY_MULTIPLIERS.get(activity_level.lower(), 1.2)
        return bmr * multiplier

    @classmethod
    def calculate_optimized_calories(cls, tdee: float, sex: str, weight_kg: float, body_fat_pct: float, experience_level: str) -> tuple[float, str]:
        """
        Calculates daily calories based on body fat percentage and training experience.
        Returns a tuple of (target_calories, phase_name).
        """
        sex = sex.lower()
        experience_level = experience_level.lower()

        # 1. Determine if the user needs a Body Recomp phase
        needs_recomp = False
        if sex == 'male' and body_fat_pct >= 20.0:
            needs_recomp = True
        elif sex == 'female' and body_fat_pct >= 30.0:
            needs_recomp = True

        if needs_recomp:
            # BODY RECOMP: Lose max 0.5% bodyweight/week (~250-500 below maintenance)
            kg_loss_per_week = weight_kg * 0.005
            daily_deficit = (kg_loss_per_week * 7700) / 7
            
            # Clamp the deficit between 250 and 500 to adhere strictly to the guidelines
            daily_deficit = max(250, min(daily_deficit, 500))
            return tdee - daily_deficit, "recomp"
            
        else:
            # BUILDING PHASE: Calorie surplus based on training experience
            if experience_level == "beginner":
                surplus = 400  # Middle of +300-500 range
            elif experience_level == "intermediate":
                surplus = 250  # Middle of +200-300 range
            elif experience_level == "advanced":
                surplus = 150  # Middle of +100-200 range
            else:
                surplus = 300  # Fallback
                
            return tdee + surplus, "build"

    @classmethod
    def calculate_macros(cls, weight_kg: float, daily_calories: float, phase: str) -> dict:
        """Calculates macro distribution dynamically based on the current phase."""
        
        # 1. Protein Target
        protein_g = round(weight_kg * 1.6) # Standard 1.6g per kg for muscle retention/growth
        protein_cals = protein_g * 4
        
        # 2. Carbohydrate Target
        # Dynamically adjust carbs based on whether we are cutting (recomp) or bulking (build)
        multiplier = 2.5 if phase == "recomp" else 4.0 
        target_carbs_g = round(weight_kg * multiplier)
        
        # Apply strict limits depending on the phase
        lower_limit_carbs = round(weight_kg * 2.5) if phase == "recomp" else round(weight_kg * 4.0)
        upper_limit_carbs = round(weight_kg * 4.0) if phase == "recomp" else round(weight_kg * 6.0)
        
        # Ensure the calculated carbs fall within the limits
        carbs_g = max(lower_limit_carbs, min(target_carbs_g, upper_limit_carbs))
        carb_cals = carbs_g * 4
        
        # 3. Fat Target (Whatever calories are leftover)
        remaining_cals = daily_calories - (protein_cals + carb_cals)
        fat_g = max(round(remaining_cals / 9), 30) # Absolute minimum 30g for hormonal health
        
        # 4. Saturated Fat Limit
        sat_fat_limit_g = round(fat_g * 0.3) # Max 30% of total fat

        return {
            "protein_g": int(protein_g),
            "carbs_g": int(carbs_g),
            "fat_g": int(fat_g),
            "sat_fat_limit_g": int(sat_fat_limit_g)
        }

    @classmethod
    def calculate_health_limits(cls, sex: str, daily_calories: float) -> dict:
        """
        Calculates maximum daily thresholds for Saturated Fat and Added Sugar 
        based on the American Heart Association (AHA) guidelines.
        """
        sat_fat_cals = daily_calories * 0.10
        sat_fat_g_limit = round(sat_fat_cals / 9)
        sugar_g_limit = 36 if sex.lower() == 'male' else 25

        return {
            "saturated_fat_g_max": sat_fat_g_limit,
            "added_sugar_g_max": sugar_g_limit
        }

    @classmethod
    def generate_full_profile(cls, sex: str, age: int, height_cm: float, weight_kg: float, 
                              activity_level: str, body_fat_pct: float, experience_level: str) -> dict:
        
        bmr = cls.calculate_bmr(sex, age, weight_kg, height_cm)
        tdee = cls.calculate_tdee(bmr, activity_level)
        
        # Retrieve the newly optimized calories and the determined phase
        daily_cals, phase = cls.calculate_optimized_calories(tdee, sex, weight_kg, body_fat_pct, experience_level)
        
        macros = cls.calculate_macros(weight_kg, daily_cals, phase)
        health_limits = cls.calculate_health_limits(sex, daily_cals)

        return {
            "results": {
                "phase_assigned": phase,
                "bmr": round(bmr),
                "tdee": round(tdee),
                "daily_calories": round(daily_cals),
                "macros": macros,
                "limits": health_limits
            }
        }