macrocycle_kb = {
    "recomposition": {
        "2_months": [
            {"phase": "strength_foundation", "base_weeks": 3},
            {"phase": "recomposition", "base_weeks": 5}
        ],
        "4_months": [
            {"phase": "strength_foundation", "base_weeks": 5},
            {"phase": "recomposition_1", "base_weeks": 5},
            {"phase": "recomposition_2", "base_weeks": 4},
            {"phase": "peak_recomposition", "base_weeks": 2}
        ]
    },
    "build_muscle": {
        "2_months": [
            {"phase": "foundation_hypertrophy", "base_weeks": 4},
            {"phase": "volume_surge", "base_weeks": 4}
        ],
        "4_months": [
            {"phase": "foundation_hypertrophy", "base_weeks": 4},
            {"phase": "volume_surge", "base_weeks": 5},
            {"phase": "strength_block", "base_weeks": 4},
            {"phase": "peak_volume", "base_weeks": 3}
        ]
    },
    "lose_fat": {
        "2_months": [
            {"phase": "foundation", "base_weeks": 3},
            {"phase": "build_and_burn", "base_weeks": 5}
        ],
        "4_months": [
            {"phase": "foundation", "base_weeks": 4},
            {"phase": "build_and_burn", "base_weeks": 6},
            {"phase": "intensify", "base_weeks": 4},
            {"phase": "metabolic_conditioning", "base_weeks": 2}
        ]
    },
    "general_health": {
        "2_months": [
            {"phase": "foundation", "base_weeks": 3},
            {"phase": "active_lifestyle", "base_weeks": 5}
        ],
        "4_months": [
            {"phase": "foundation", "base_weeks": 4},
            {"phase": "active_lifestyle", "base_weeks": 6},
            {"phase": "endurance_and_strength", "base_weeks": 4},
            {"phase": "sustain", "base_weeks": 2}
        ]
    }
}

blueprint_library = {
    # ---------------------------------------------------------
    # 1. FULL BODY SPLITS (Used in Foundation & Active Lifestyle)
    # ---------------------------------------------------------
    "full_body": {
        "full_body_A": {
            "squat_pattern": 1,
            "horizontal_press": 1,
            "horizontal_pull": 1,
            "bicep_isolation": 1,
            "core_stabilization": 1
        },
        "full_body_B": {
            "hinge_pattern": 1,
            "vertical_press": 1,
            "vertical_pull": 1,
            "tricep_isolation": 1,
            "core_stabilization": 1
        },
        "full_body_C": {
            "unilateral_leg": 1,
            "horizontal_press": 1,
            "vertical_pull": 1,
            "side_delt_isolation": 1,
            "core_stabilization": 1
        }
    },

    # ---------------------------------------------------------
    # 2. UPPER / LOWER SPLITS (Used in Recomposition & Volume Surge)
    # ---------------------------------------------------------
    "upper_lower": {
        "upper_day": {
            "horizontal_press": 1,
            "vertical_pull": 1,
            "vertical_press": 1,
            "horizontal_pull": 1,
            "chest_isolation": 1,
            "bicep_isolation": 1,
            "tricep_isolation": 1
        },
        "lower_day": {
            "squat_pattern": 1,
            "hinge_pattern": 1,
            "unilateral_leg": 1,
            "quad_isolation": 1,
            "glute_isolation": 1,
            "core_stabilization": 1
        }
    },

    # ---------------------------------------------------------
    # 3. PUSH / PULL / LEGS (Used in Strength Block & Advanced Users)
    # ---------------------------------------------------------
    "push_pull_legs": {
        "push_day": {
            "horizontal_press": 2, # E.g., Bench Press AND Incline DB Press
            "vertical_press": 1,
            "chest_isolation": 1,
            "side_delt_isolation": 1,
            "tricep_isolation": 2
        },
        "pull_day": {
            "vertical_pull": 2,
            "horizontal_pull": 1,
            "rear_delt_isolation": 1,
            "bicep_isolation": 2
        },
        "leg_day": {
            "squat_pattern": 1,
            "hinge_pattern": 1,
            "unilateral_leg": 1,
            "quad_isolation": 1,
            "glute_isolation": 1
        }
    }
}

phase_parameters_kb = {
    # ---------------------------------------------------------
    # THE FOUNDATION & HEALTH ARC
    # ---------------------------------------------------------
    "foundation": {
        "recommended_split": "full_body",
        "ideal_frequency": 3,
        "default_sets": 3,
        "rep_range": "10-12",
        "rest_seconds": 90,
        "execution_style": "form_mastery" # Keeps weight light, focuses on rep completion
    },
    "strength_foundation": {
        "recommended_split": "full_body",
        "ideal_frequency": 3,
        "default_sets": 4, 
        "rep_range": "8-12",
        "rest_seconds": 120, 
        "execution_style": "barbell_linear" # Triggers linear weight increases
    },
    "active_lifestyle": {
        "recommended_split": "full_body",
        "ideal_frequency": 3,
        "default_sets": 3,
        "rep_range": "10-12",
        "rest_seconds": 90,
        "execution_style": "double_progression"
    },

    # ---------------------------------------------------------
    # THE RECOMPOSITION ARC
    # ---------------------------------------------------------
    "recomposition_1": {
        "recommended_split": "upper_lower",
        "ideal_frequency": 4,
        "compound_sets": 4, "compound_reps": "8-12",
        "isolation_sets": 3, "isolation_reps": "12-15",
        "rest_seconds": 75, 
        "execution_style": "recomp_fat_loss_bias" # Triggers double progression
    },
    "recomposition_2": {
        "recommended_split": "push_pull_legs",
        "ideal_frequency": 5,
        "compound_sets": 4, "compound_reps": "6-10",
        "isolation_sets": 4, "isolation_reps": "10-12",
        "rest_seconds": 90, 
        "execution_style": "recomp_muscle_bias" # Triggers double progression
    },

    # ---------------------------------------------------------
    # THE MUSCLE BUILDING ARC
    # ---------------------------------------------------------
    "hypertrophy_volume": {
        "recommended_split": "upper_lower", # Or PPL depending on frequency
        "ideal_frequency": 4,
        "compound_sets": 4, "compound_reps": "8-12",
        "isolation_sets": 3, "isolation_reps": "12-15",
        "rest_seconds": 90,
        "execution_style": "volume_accumulation" # Triggers adding sets week over week
    },
    "strength_block": {
        "recommended_split": "push_pull_legs",
        "ideal_frequency": 5,
        "default_sets": 5,
        "rep_range": "5-8",
        "rest_seconds": 180, #3 minutes for heavy CNS recovery
        "execution_style": "heavy_strength_linear" # Triggers forced weight jumps
    },

    # ---------------------------------------------------------
    # THE FAT LOSS ARC
    # ---------------------------------------------------------
    "build_and_burn": {
        "recommended_split": "full_body_circuit",
        "ideal_frequency": 4,
        "default_sets": 4, 
        "rep_range": "8-12",
        "rest_seconds": 45,
        "execution_style": "double_progression" 
    },
    "peak_metabolic": {
        "recommended_split": "mixed_modal_circuit",
        "ideal_frequency": 4,
        "default_sets": "AMRAP", # As Many Reps As Possible
        "rep_range": "timed_45_seconds",
        "rest_seconds": 30,
        "execution_style": "circuit_style" # Bypasses heavy lifting algorithms
    }
}