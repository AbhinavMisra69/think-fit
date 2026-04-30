class NutritionCalculator:
    ACTIVITY_MULTIPLIERS = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "extremely active": 1.9,
    }

    RATE_PERCENTAGES = {
        "slow": 0.005,
        "moderate": 0.007,
        "fast": 0.01,
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
    def calculate_daily_calories(cls, tdee: float, weight_kg: float, goal: str, rate: str) -> float:
        goal = goal.lower()
        if goal == "maintenance":
            return tdee

        rate_pct = cls.RATE_PERCENTAGES.get(rate.lower(), 0.005)
        kg_per_week = weight_kg * rate_pct
        caloric_adjustment = (kg_per_week * 7700) / 7

        return tdee - caloric_adjustment if goal == "fat loss" else tdee + caloric_adjustment

    @classmethod
   
    def calculate_macros(weight_kg: float, daily_calories: float, goal: str) -> dict:
        """Calculates macro distribution with dynamic carbohydrate limits."""
        
        # 1. Protein Target
        protein_g = round(weight_kg * 1.6) # Standard 1.6g per kg for muscle retention
        protein_cals = protein_g * 4
        
        # 2. Carbohydrate Target
        # You can change 4.0 to 2.5 here if your goal is cutting!
        multiplier = 4.0 
        target_carbs_g = round(weight_kg * multiplier)
        
        # Apply strict limits
        lower_limit_carbs = round(weight_kg * 4.0)
        upper_limit_carbs = round(weight_kg * 6.0)
        
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
        # Saturated Fat: Max 10% of total daily calories
        sat_fat_cals = daily_calories * 0.10
        sat_fat_g_limit = round(sat_fat_cals / 9)

        # Added Sugar: Hard AHA limits based on biological sex
        sugar_g_limit = 36 if sex.lower() == 'male' else 25

        return {
            "saturated_fat_g_max": sat_fat_g_limit,
            "added_sugar_g_max": sugar_g_limit
        }

    @classmethod
    def generate_full_profile(cls, sex: str, age: int, height_cm: float, weight_kg: float, 
                              goal: str, activity_level: str, rate: str) -> dict:
        
        bmr = cls.calculate_bmr(sex, age, weight_kg, height_cm)
        tdee = cls.calculate_tdee(bmr, activity_level)
        daily_cals = cls.calculate_daily_calories(tdee, weight_kg, goal, rate)
        macros = cls.calculate_macros(weight_kg, daily_cals, goal)
        health_limits = cls.calculate_health_limits(sex, daily_cals)

        return {
            "results": {
                "bmr": round(bmr),
                "tdee": round(tdee),
                "daily_calories": round(daily_cals),
                "macros": macros,
                "limits": health_limits
            }
        }