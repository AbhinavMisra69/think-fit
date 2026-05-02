#  THE EXERCISE DATASET (The Knowledge Base)
exercise_dataset = {
        # ==========================================
    # S+ & S TIER (Glutes & Quads)
    # ==========================================
    "walking_lunges": {
        "exercise_id": "EX_101",
        "exercise_name": "Walking Lunges",
        "muscle_data": {
            "primary_targets": ["glutes", "quads"],
            "secondary_muscles": ["hamstrings", "core"],
            "movement_pattern": "unilateral_leg",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells"]},
        "biomechanics": {"joint_stress": ["knee_torque"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume", "peak_metabolic"],
            "hypertrophy_tiers": {"glutes": "S_Plus", "quads": "B_Tier"}
        }
    },
    "machine_hip_abduction": {
        "exercise_id": "EX_102",
        "exercise_name": "Machine Hip Abduction",
        "muscle_data": {
            "primary_targets": ["glutes"],
            "secondary_muscles": [],
            "movement_pattern": "glute_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "pro_gym", "specific_tools": ["abduction_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"glutes": "S_Tier"}
        }
    },
    "deficit_lunges": {
        "exercise_id": "EX_103",
        "exercise_name": "Deficit Lunges (Front Foot Elevated)",
        "muscle_data": {
            "primary_targets": ["glutes", "quads"],
            "secondary_muscles": ["hamstrings"],
            "movement_pattern": "unilateral_leg",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["dumbbells", "step_platform"]},
        "biomechanics": {"joint_stress": ["knee_torque", "hip_flexor_stretch"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "recomposition", "strength_block", "hypertrophy_volume"],
            "hypertrophy_tiers": {"glutes": "S_Tier"}
        }
    },
    "45_degree_back_extension": {
        "exercise_id": "EX_104",
        "exercise_name": "45° Back Extension",
        "muscle_data": {
            "primary_targets": ["glutes", "hamstrings"],
            "secondary_muscles": ["lower_back"],
            "movement_pattern": "hinge_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["back_extension_machine"]},
        "biomechanics": {"joint_stress": ["lumbar_shear"], "pre_hab_for": ["lower_back_strengthening"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"glutes": "S_Tier"}
        }
    },
    "hack_squat": {
        "exercise_id": "EX_105",
        "exercise_name": "Hack Squat",
        "muscle_data": {
            "primary_targets": ["quads"],
            "secondary_muscles": ["glutes"],
            "movement_pattern": "squat_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "pro_gym", "specific_tools": ["hack_squat_machine"]},
        "biomechanics": {"joint_stress": ["high_knee_torque"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"quads": "S_Tier"}
        }
    },
    "barbell_back_squat": {
        "exercise_id": "EX_106",
        "exercise_name": "Barbell Back Squat (High Bar)",
        "muscle_data": {
            "primary_targets": ["quads", "glutes"],
            "secondary_muscles": ["core", "lower_back"],
            "movement_pattern": "squat_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "squat_rack", "weight_plates"]},
        "biomechanics": {"joint_stress": ["spinal_compression", "high_knee_torque"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "recomposition", "strength_block", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"quads": "S_Tier", "glutes": "A_Tier"}
        }
    },
    "bulgarian_split_squat": {
        "exercise_id": "EX_107",
        "exercise_name": "Bulgarian Split Squat",
        "muscle_data": {
            "primary_targets": ["quads", "glutes"],
            "secondary_muscles": ["hamstrings", "core"],
            "movement_pattern": "unilateral_leg",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": ["high_knee_torque"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "recomposition", "strength_block", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"quads": "S_Tier", "glutes": "A_Tier"}
        }
    },
    "pendulum_squat": {
        "exercise_id": "EX_108",
        "exercise_name": "Pendulum Squat",
        "muscle_data": {
            "primary_targets": ["quads"],
            "secondary_muscles": ["glutes"],
            "movement_pattern": "squat_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "pro_gym", "specific_tools": ["pendulum_squat_machine"]},
        "biomechanics": {"joint_stress": ["extreme_knee_torque"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"quads": "S_Tier"}
        }
    },
    "smith_machine_squat": {
        "exercise_id": "EX_109",
        "exercise_name": "Smith Machine Squat",
        "muscle_data": {
            "primary_targets": ["quads", "glutes"],
            "secondary_muscles": ["core"],
            "movement_pattern": "squat_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["smith_machine", "weight_plates"]},
        "biomechanics": {"joint_stress": ["spinal_compression", "knee_torque"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"quads": "S_Tier", "glutes": "A_Tier"}
        }
    },

    # ==========================================
    # A TIER (Glutes & Quads)
    # ==========================================
    "hip_thrust_machine": {
        "exercise_id": "EX_110",
        "exercise_name": "Hip Thrust Machine",
        "muscle_data": {
            "primary_targets": ["glutes"],
            "secondary_muscles": ["hamstrings"],
            "movement_pattern": "glute_isolation",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "pro_gym", "specific_tools": ["hip_thrust_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"glutes": "A_Tier"}
        }
    },
    "single_leg_db_hip_thrust": {
        "exercise_id": "EX_111",
        "exercise_name": "Single Leg Dumbbell Hip Thrust",
        "muscle_data": {
            "primary_targets": ["glutes"],
            "secondary_muscles": ["hamstrings"],
            "movement_pattern": "glute_isolation",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"glutes": "A_Tier"}
        }
    },
    "cable_kickback": {
        "exercise_id": "EX_112",
        "exercise_name": "Cable Kickback",
        "muscle_data": {
            "primary_targets": ["glutes"],
            "secondary_muscles": [],
            "movement_pattern": "glute_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "ankle_strap"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"glutes": "A_Tier"}
        }
    },
    "step_up": {
        "exercise_id": "EX_113",
        "exercise_name": "Step Up",
        "muscle_data": {
            "primary_targets": ["glutes", "quads"],
            "secondary_muscles": ["core"],
            "movement_pattern": "unilateral_leg",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "plyo_box"]},
        "biomechanics": {"joint_stress": ["knee_torque"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn", "peak_metabolic"],
            "hypertrophy_tiers": {"glutes": "A_Tier"}
        }
    },
    "smith_machine_lunge": {
        "exercise_id": "EX_114",
        "exercise_name": "Smith Machine Lunge",
        "muscle_data": {
            "primary_targets": ["glutes", "quads"],
            "secondary_muscles": ["hamstrings"],
            "movement_pattern": "unilateral_leg",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["smith_machine"]},
        "biomechanics": {"joint_stress": ["knee_torque"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"glutes": "A_Tier"}
        }
    },
    "romanian_deadlift": {
        "exercise_id": "EX_115",
        "exercise_name": "Romanian Deadlift (RDL)",
        "muscle_data": {
            "primary_targets": ["glutes", "hamstrings"],
            "secondary_muscles": ["lower_back", "core"],
            "movement_pattern": "hinge_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "weight_plates"]},
        "biomechanics": {"joint_stress": ["spinal_compression", "lumbar_shear"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "strength_block", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"glutes": "A_Tier"}
        }
    },
    "leg_extension": {
        "exercise_id": "EX_116",
        "exercise_name": "Leg Extension",
        "muscle_data": {
            "primary_targets": ["quads"],
            "secondary_muscles": [],
            "movement_pattern": "quad_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["leg_extension_machine"]},
        "biomechanics": {"joint_stress": ["patellar_tendon_stress"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"quads": "A_Tier"}
        }
    },
    "barbell_front_squat": {
        "exercise_id": "EX_117",
        "exercise_name": "Barbell Front Squat",
        "muscle_data": {
            "primary_targets": ["quads", "core"],
            "secondary_muscles": ["glutes", "upper_back"],
            "movement_pattern": "squat_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "squat_rack", "weight_plates"]},
        "biomechanics": {"joint_stress": ["spinal_compression", "wrist_strain", "knee_torque"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "recomposition", "strength_block", "strength_block"],
            "hypertrophy_tiers": {"quads": "A_Tier"}
        }
    },
    "low_bar_back_squat": {
        "exercise_id": "EX_118",
        "exercise_name": "Low Bar Back Squat",
        "muscle_data": {
            "primary_targets": ["quads", "glutes", "lower_back"],
            "secondary_muscles": ["hamstrings", "core"],
            "movement_pattern": "squat_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "squat_rack", "weight_plates"]},
        "biomechanics": {"joint_stress": ["spinal_compression", "shoulder_mobility_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "strength_block", "strength_block"],
            "hypertrophy_tiers": {"quads": "A_Tier"}
        }
    },
    "45_degree_leg_press": {
        "exercise_id": "EX_119",
        "exercise_name": "45° Leg Press",
        "muscle_data": {
            "primary_targets": ["quads", "glutes"],
            "secondary_muscles": ["hamstrings"],
            "movement_pattern": "squat_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["leg_press_machine"]},
        "biomechanics": {"joint_stress": ["lumbar_flexion_if_deep"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"quads": "A_Tier"}
        }
    },
    "reverse_nordic": {
        "exercise_id": "EX_120",
        "exercise_name": "Reverse Nordic",
        "muscle_data": {
            "primary_targets": ["quads"],
            "secondary_muscles": ["core"],
            "movement_pattern": "quad_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": []},
        "biomechanics": {"joint_stress": ["high_knee_torque"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn", "recomposition"],
            "hypertrophy_tiers": {"quads": "A_Tier"}
        }
    },

    # ==========================================
    # B TIER (Glutes & Quads)
    # ==========================================
    "barbell_hip_thrust": {
        "exercise_id": "EX_121",
        "exercise_name": "Barbell Hip Thrust",
        "muscle_data": {
            "primary_targets": ["glutes"],
            "secondary_muscles": ["hamstrings"],
            "movement_pattern": "glute_isolation",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "bench", "bar_pad"]},
        "biomechanics": {"joint_stress": ["pelvic_pressure"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"glutes": "B_Tier"}
        }
    },
    "glute_bridge": {
        "exercise_id": "EX_122",
        "exercise_name": "Glute Bridge",
        "muscle_data": {
            "primary_targets": ["glutes"],
            "secondary_muscles": ["lower_back"],
            "movement_pattern": "glute_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": []},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["lower_back_activation"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "peak_recomposition"],
            "hypertrophy_tiers": {"glutes": "B_Tier"}
        }
    },
    "cable_hip_abduction": {
        "exercise_id": "EX_123",
        "exercise_name": "Cable Hip Abduction",
        "muscle_data": {
            "primary_targets": ["glutes"],
            "secondary_muscles": [],
            "movement_pattern": "glute_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "ankle_strap"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"glutes": "B_Tier"}
        }
    },
    "curtsy_lunge": {
        "exercise_id": "EX_124",
        "exercise_name": "Curtsy Lunge",
        "muscle_data": {
            "primary_targets": ["glutes", "quads"],
            "secondary_muscles": ["adductors"],
            "movement_pattern": "unilateral_leg",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells"]},
        "biomechanics": {"joint_stress": ["lateral_knee_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "build_and_burn", "peak_metabolic"],
            "hypertrophy_tiers": {"glutes": "B_Tier"}
        }
    },
    "conventional_deadlift": {
        "exercise_id": "EX_125",
        "exercise_name": "Conventional Deadlift",
        "muscle_data": {
            "primary_targets": ["glutes", "hamstrings", "lower_back"],
            "secondary_muscles": ["lats", "core", "forearms"],
            "movement_pattern": "hinge_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "weight_plates"]},
        "biomechanics": {"joint_stress": ["spinal_compression", "lumbar_shear"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "strength_block", "strength_block"],
            "hypertrophy_tiers": {"glutes": "B_Tier"}
        }
    },
    "sumo_deadlift": {
        "exercise_id": "EX_126",
        "exercise_name": "Sumo Deadlift",
        "muscle_data": {
            "primary_targets": ["glutes", "quads", "adductors"],
            "secondary_muscles": ["lower_back", "core"],
            "movement_pattern": "hinge_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "weight_plates"]},
        "biomechanics": {"joint_stress": ["hip_mobility_strain", "lumbar_shear"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "strength_block", "strength_block"],
            "hypertrophy_tiers": {"glutes": "B_Tier"}
        }
    },
    "cable_pull_through": {
        "exercise_id": "EX_127",
        "exercise_name": "Cable Pull-Through",
        "muscle_data": {
            "primary_targets": ["glutes", "hamstrings"],
            "secondary_muscles": ["lower_back"],
            "movement_pattern": "hinge_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "rope_attachment"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"glutes": "B_Tier"}
        }
    },
    "lunge": {
        "exercise_id": "EX_128",
        "exercise_name": "Stationary Lunge",
        "muscle_data": {
            "primary_targets": ["quads", "glutes"],
            "secondary_muscles": ["core"],
            "movement_pattern": "unilateral_leg",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells"]},
        "biomechanics": {"joint_stress": ["knee_torque"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn"],
            "hypertrophy_tiers": {"quads": "B_Tier"}
        }
    },
    "goblet_squat": {
        "exercise_id": "EX_129",
        "exercise_name": "Goblet Squat",
        "muscle_data": {
            "primary_targets": ["quads"],
            "secondary_muscles": ["core", "glutes"],
            "movement_pattern": "squat_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["squat_mechanics_training"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn", "peak_recomposition"],
            "hypertrophy_tiers": {"quads": "B_Tier"}
        }
    },
    "sissy_squat": {
        "exercise_id": "EX_130",
        "exercise_name": "Sissy Squat",
        "muscle_data": {
            "primary_targets": ["quads"],
            "secondary_muscles": ["core"],
            "movement_pattern": "quad_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["sissy_squat_bench"]},
        "biomechanics": {"extreme_knee_torque": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"quads": "B_Tier"}
        }
    },
        # ==========================================
    # CHEST (S+, S, A, B Tiers)
    # ==========================================
    "machine_chest_press": {
        "exercise_id": "EX_201",
        "exercise_name": "Machine Chest Press",
        "muscle_data": {
            "primary_targets": ["chest"],
            "secondary_muscles": ["front_delts", "triceps"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["chest_press_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"chest": "S_Plus"}
        }
    },
    "seated_cable_pec_fly": {
        "exercise_id": "EX_202",
        "exercise_name": "Seated Cable Pec Fly",
        "muscle_data": {
            "primary_targets": ["chest"],
            "secondary_muscles": [],
            "movement_pattern": "chest_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "bench"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"chest": "S_Tier"}
        }
    },
    "flat_bench_press": {
        "exercise_id": "EX_203",
        "exercise_name": "Flat Bench Press",
        "muscle_data": {
            "primary_targets": ["chest"],
            "secondary_muscles": ["front_delts", "triceps"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "bench", "weight_plates"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "recomposition", "strength_block", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"chest": "A_Tier"}
        }
    },
    "incline_bench_press": {
        "exercise_id": "EX_204",
        "exercise_name": "Incline Bench Press",
        "muscle_data": {
            "primary_targets": ["upper_chest", "front_delts"],
            "secondary_muscles": ["triceps"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "incline_bench", "weight_plates"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "recomposition", "strength_block", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"chest": "A_Tier", "front_delts": "A_Tier"}
        }
    },
    "flat_db_press": {
        "exercise_id": "EX_205",
        "exercise_name": "Flat Dumbbell Press",
        "muscle_data": {
            "primary_targets": ["chest"],
            "secondary_muscles": ["front_delts", "triceps"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"chest": "A_Tier"}
        }
    },
    "incline_db_press": {
        "exercise_id": "EX_206",
        "exercise_name": "Incline Dumbbell Press",
        "muscle_data": {
            "primary_targets": ["upper_chest", "front_delts"],
            "secondary_muscles": ["triceps"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "incline_bench"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"chest": "A_Tier", "front_delts": "A_Tier"}
        }
    },
    "dips": {
        "exercise_id": "EX_207",
        "exercise_name": "Chest Dips (Leaning Forward)",
        "muscle_data": {
            "primary_targets": ["chest", "lower_chest"],
            "secondary_muscles": ["triceps", "front_delts"],
            "movement_pattern": "vertical_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["dip_station"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior", "sternum_pressure"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"chest": "A_Tier"}
        }
    },
    "smith_machine_press_flat_incline": {
        "exercise_id": "EX_208",
        "exercise_name": "Smith Machine Press (Flat & Incline)",
        "muscle_data": {
            "primary_targets": ["chest"],
            "secondary_muscles": ["front_delts", "triceps"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["smith_machine", "bench"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"chest": "A_Tier"}
        }
    },
    "cable_crossover": {
        "exercise_id": "EX_209",
        "exercise_name": "Cable Crossover",
        "muscle_data": {
            "primary_targets": ["chest"],
            "secondary_muscles": [],
            "movement_pattern": "chest_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior_stretch"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"chest": "A_Tier"}
        }
    },
    "pec_deck_machine": {
        "exercise_id": "EX_210",
        "exercise_name": "Pec Deck Machine",
        "muscle_data": {
            "primary_targets": ["chest"],
            "secondary_muscles": [],
            "movement_pattern": "chest_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["pec_deck_machine"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior_stretch"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"chest": "A_Tier"}
        }
    },
    "db_fly": {
        "exercise_id": "EX_211",
        "exercise_name": "Dumbbell Fly",
        "muscle_data": {
            "primary_targets": ["chest"],
            "secondary_muscles": [],
            "movement_pattern": "chest_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior_stretch", "bicep_tendon_stretch"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"chest": "A_Tier"}
        }
    },
    "deficit_push_up": {
        "exercise_id": "EX_212",
        "exercise_name": "Deficit Push-Up",
        "muscle_data": {
            "primary_targets": ["chest"],
            "secondary_muscles": ["triceps", "front_delts"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["push_up_handles_or_plates"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior_stretch"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "build_and_burn", "recomposition", "recomposition", "peak_metabolic"],
            "hypertrophy_tiers": {"chest": "A_Tier"}
        }
    },
    "cable_press_around": {
        "exercise_id": "EX_213",
        "exercise_name": "Cable Press Around",
        "muscle_data": {
            "primary_targets": ["chest"],
            "secondary_muscles": [],
            "movement_pattern": "chest_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"chest": "A_Tier"}
        }
    },
    "guillotine_press_db": {
        "exercise_id": "EX_214",
        "exercise_name": "Guillotine Press (Dumbbell Version)",
        "muscle_data": {
            "primary_targets": ["upper_chest"],
            "secondary_muscles": ["front_delts"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": ["shoulder_impingement"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"chest": "A_Tier"}
        }
    },
    "decline_bench_press": {
        "exercise_id": "EX_215",
        "exercise_name": "Decline Bench Press (Barbell & Dumbbell)",
        "muscle_data": {
            "primary_targets": ["lower_chest"],
            "secondary_muscles": ["triceps"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "decline_bench"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"chest": "B_Tier"}
        }
    },
    "banded_push_up": {
        "exercise_id": "EX_216",
        "exercise_name": "Banded Push-Up",
        "muscle_data": {
            "primary_targets": ["chest"],
            "secondary_muscles": ["triceps", "core"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["resistance_bands"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "build_and_burn", "recomposition", "recomposition"],
            "hypertrophy_tiers": {"chest": "B_Tier"}
        }
    },

    # ==========================================
    # TRICEPS (S, A, B Tiers)
    # ==========================================
    "overhead_cable_triceps_extension": {
        "exercise_id": "EX_217",
        "exercise_name": "Overhead Cable Triceps Extension",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": [],
            "movement_pattern": "tricep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine"]},
        "biomechanics": {"joint_stress": ["elbow_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"triceps": "S_Tier"}
        }
    },
    "skull_crusher": {
        "exercise_id": "EX_218",
        "exercise_name": "Skull Crusher",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": [],
            "movement_pattern": "tricep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["ez_bar", "bench"]},
        "biomechanics": {"joint_stress": ["elbow_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"triceps": "S_Tier"}
        }
    },
    "bar_press_down": {
        "exercise_id": "EX_219",
        "exercise_name": "Bar Press Down",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": [],
            "movement_pattern": "tricep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "straight_bar"]},
        "biomechanics": {"joint_stress": ["wrist_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"triceps": "A_Tier"}
        }
    },
    "one_arm_db_triceps_extension": {
        "exercise_id": "EX_220",
        "exercise_name": "One-Arm Dumbbell Triceps Extension",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": [],
            "movement_pattern": "tricep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells"]},
        "biomechanics": {"joint_stress": ["elbow_strain", "shoulder_mobility_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"triceps": "A_Tier"}
        }
    },
    "katana_triceps_extension": {
        "exercise_id": "EX_221",
        "exercise_name": "Katana Triceps Extension",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": [],
            "movement_pattern": "tricep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "bench"]},
        "biomechanics": {"joint_stress": ["elbow_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"triceps": "A_Tier"}
        }
    },
    "overhead_cable_extension_rope": {
        "exercise_id": "EX_222",
        "exercise_name": "Overhead Cable Extension (Rope)",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": [],
            "movement_pattern": "tricep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "rope_attachment"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"triceps": "A_Tier"}
        }
    },
    "close_grip_bench_press": {
        "exercise_id": "EX_223",
        "exercise_name": "Close Grip Bench Press",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": ["chest", "front_delts"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "bench", "weight_plates"]},
        "biomechanics": {"joint_stress": ["wrist_strain", "shoulder_anterior"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "recomposition", "strength_block", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"triceps": "A_Tier"}
        }
    },
    "cable_triceps_kickback": {
        "exercise_id": "EX_224",
        "exercise_name": "Cable Triceps Kickback",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": [],
            "movement_pattern": "tricep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"triceps": "A_Tier"}
        }
    },
    "smith_machine_jm_press": {
        "exercise_id": "EX_225",
        "exercise_name": "Smith Machine JM Press",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": ["chest"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["smith_machine", "bench"]},
        "biomechanics": {"joint_stress": ["elbow_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"triceps": "A_Tier"}
        }
    },
    "db_skull_crusher": {
        "exercise_id": "EX_226",
        "exercise_name": "Dumbbell Skull Crusher",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": [],
            "movement_pattern": "tricep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": ["elbow_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"triceps": "A_Tier"}
        }
    },
    "rope_press_down": {
        "exercise_id": "EX_227",
        "exercise_name": "Rope Press Down",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": [],
            "movement_pattern": "tricep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "rope_attachment"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"triceps": "B_Tier"}
        }
    },
    "db_french_press": {
        "exercise_id": "EX_228",
        "exercise_name": "Dumbbell French Press",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": [],
            "movement_pattern": "tricep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": ["elbow_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"triceps": "B_Tier"}
        }
    },
    "jm_press_barbell": {
        "exercise_id": "EX_229",
        "exercise_name": "JM Press (Barbell)",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": ["chest"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "bench", "weight_plates"]},
        "biomechanics": {"joint_stress": ["severe_elbow_strain", "wrist_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"triceps": "B_Tier"}
        }
    },
    "close_grip_dip": {
        "exercise_id": "EX_230",
        "exercise_name": "Close Grip Dip (Upright Torso)",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": ["chest", "front_delts"],
            "movement_pattern": "vertical_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["dip_station"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior", "sternum_pressure"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"triceps": "B_Tier"}
        }
    },
    "diamond_push_up": {
        "exercise_id": "EX_231",
        "exercise_name": "Diamond Push-Up",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": ["chest", "core"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": []},
        "biomechanics": {"joint_stress": ["wrist_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "build_and_burn", "recomposition", "recomposition", "peak_metabolic"],
            "hypertrophy_tiers": {"triceps": "B_Tier"}
        }
    },
    "machine_dip": {
        "exercise_id": "EX_232",
        "exercise_name": "Machine Dip",
        "muscle_data": {
            "primary_targets": ["triceps", "chest"],
            "secondary_muscles": ["front_delts"],
            "movement_pattern": "vertical_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["dip_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"triceps": "B_Tier"}
        }
    },
    # ==========================================
    # BACK (S+, S, A, B Tiers)
    # ==========================================
    "chest_supported_row": {
        "exercise_id": "EX_301",
        "exercise_name": "Chest Supported Row",
        "muscle_data": {
            "primary_targets": ["back", "rear_delts"],
            "secondary_muscles": ["biceps", "traps"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["dumbbells", "incline_bench"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["posture_correction"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"back": "S_Plus"}
        }
    },
    "wide_grip_lat_pull_down": {
        "exercise_id": "EX_302",
        "exercise_name": "Wide Grip Lat Pull Down",
        "muscle_data": {
            "primary_targets": ["lats"],
            "secondary_muscles": ["biceps", "rear_delts"],
            "movement_pattern": "vertical_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["lat_pulldown_machine", "wide_bar"]},
        "biomechanics": {"joint_stress": ["shoulder_impingement_if_behind_neck"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "foundation", "recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"back": "S_Tier"}
        }
    },
    "neutral_grip_pull_down": {
        "exercise_id": "EX_303",
        "exercise_name": "Neutral Grip Pull Down",
        "muscle_data": {
            "primary_targets": ["lats", "biceps"],
            "secondary_muscles": ["rhomboids"],
            "movement_pattern": "vertical_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["lat_pulldown_machine", "v_bar_or_neutral_attachment"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"back": "S_Tier"}
        }
    },
    "half_kneeling_one_arm_lat_pull_down": {
        "exercise_id": "EX_304",
        "exercise_name": "Half Kneeling One Arm Lat Pull Down",
        "muscle_data": {
            "primary_targets": ["lats"],
            "secondary_muscles": ["core", "biceps"],
            "movement_pattern": "vertical_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "d_handle"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["core_stability"]},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"back": "S_Tier"}
        }
    },
    "meadows_row": {
        "exercise_id": "EX_305",
        "exercise_name": "Meadows Row",
        "muscle_data": {
            "primary_targets": ["upper_back", "lats"],
            "secondary_muscles": ["biceps", "rear_delts", "grip"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "landmine_attachment"]},
        "biomechanics": {"joint_stress": ["lumbar_shear_if_unsupported"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"back": "S_Tier"}
        }
    },
    "cable_row": {
        "exercise_id": "EX_306",
        "exercise_name": "Cable Row (Close & Wide Grip)",
        "muscle_data": {
            "primary_targets": ["back", "rhomboids"],
            "secondary_muscles": ["biceps", "rear_delts"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_row_machine"]},
        "biomechanics": {"joint_stress": ["lumbar_flexion_if_rounded"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"back": "S_Tier"}
        }
    },
    "wide_grip_pull_up": {
        "exercise_id": "EX_307",
        "exercise_name": "Wide Grip Pull-Up",
        "muscle_data": {
            "primary_targets": ["lats"],
            "secondary_muscles": ["biceps", "core"],
            "movement_pattern": "vertical_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["pull_up_bar"]},
        "biomechanics": {"joint_stress": ["shoulder_impingement_if_poor_mobility"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "recomposition", "strength_block", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"back": "A_Tier"}
        }
    },
    "neutral_grip_pull_up": {
        "exercise_id": "EX_308",
        "exercise_name": "Neutral Grip Pull-Up",
        "muscle_data": {
            "primary_targets": ["lats", "biceps"],
            "secondary_muscles": ["core", "brachialis"],
            "movement_pattern": "vertical_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["pull_up_bar_with_neutral_grips"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume", "peak_metabolic"],
            "hypertrophy_tiers": {"back": "A_Tier"}
        }
    },
    "cross_body_lat_pull_around": {
        "exercise_id": "EX_309",
        "exercise_name": "Cross Body Lat Pull Around",
        "muscle_data": {
            "primary_targets": ["lats"],
            "secondary_muscles": [],
            "movement_pattern": "vertical_pull",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "d_handle"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"back": "A_Tier"}
        }
    },
    "deficit_pendlay_row": {
        "exercise_id": "EX_310",
        "exercise_name": "Deficit Penlay Row",
        "muscle_data": {
            "primary_targets": ["back", "rhomboids"],
            "secondary_muscles": ["lower_back", "hamstrings"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "weight_plates", "step_platform"]},
        "biomechanics": {"joint_stress": ["lumbar_shear"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "strength_block", "strength_block"],
            "hypertrophy_tiers": {"back": "A_Tier"}
        }
    },
    "one_arm_db_row": {
        "exercise_id": "EX_311",
        "exercise_name": "One Arm Dumbbell Row",
        "muscle_data": {
            "primary_targets": ["lats", "upper_back"],
            "secondary_muscles": ["biceps", "core"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": ["lumbar_torsion_if_twisted"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"back": "A_Tier"}
        }
    },
    "croc_row": {
        "exercise_id": "EX_312",
        "exercise_name": "Croc Row",
        "muscle_data": {
            "primary_targets": ["upper_back", "grip"],
            "secondary_muscles": ["lats", "biceps", "core"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["heavy_dumbbells", "bench_or_rack_for_support"]},
        "biomechanics": {"joint_stress": ["lumbar_shear", "shoulder_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["strength_block", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"back": "A_Tier"}
        }
    },
    "lying_or_seated_face_pull": {
        "exercise_id": "EX_313",
        "exercise_name": "Lying or Seated Face Pull",
        "muscle_data": {
            "primary_targets": ["rear_delts", "traps"],
            "secondary_muscles": ["rhomboids"],
            "movement_pattern": "rear_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "bench", "rope_attachment"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["shoulder_posture", "rotator_cuff_health"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"back": "A_Tier"}
        }
    },
    "lat_prayer": {
        "exercise_id": "EX_314",
        "exercise_name": "Lat Prayer (Cable Lat Pullover)",
        "muscle_data": {
            "primary_targets": ["lats"],
            "secondary_muscles": ["triceps_long_head"],
            "movement_pattern": "vertical_pull",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "straight_bar_or_rope"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"back": "A_Tier"}
        }
    },
    "db_lat_pullover": {
        "exercise_id": "EX_315",
        "exercise_name": "Dumbbell Lat Pullover",
        "muscle_data": {
            "primary_targets": ["lats", "chest"],
            "secondary_muscles": ["triceps", "serratus"],
            "movement_pattern": "vertical_pull",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior_stretch"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"back": "A_Tier"}
        }
    },
    "chin_ups": {
        "exercise_id": "EX_316",
        "exercise_name": "Chin-Ups",
        "muscle_data": {
            "primary_targets": ["lats", "biceps"],
            "secondary_muscles": ["core"],
            "movement_pattern": "vertical_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["pull_up_bar"]},
        "biomechanics": {"joint_stress": ["elbow_strain", "wrist_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "build_and_burn", "recomposition", "recomposition", "strength_block", "peak_metabolic"],
            "hypertrophy_tiers": {"back": "B_Tier", "biceps": "B_Tier"}
        }
    },
    "standard_barbell_row": {
        "exercise_id": "EX_317",
        "exercise_name": "Standard Barbell Row",
        "muscle_data": {
            "primary_targets": ["back", "rhomboids"],
            "secondary_muscles": ["lower_back", "biceps", "hamstrings"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "weight_plates"]},
        "biomechanics": {"joint_stress": ["lumbar_shear"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "recomposition", "strength_block", "strength_block"],
            "hypertrophy_tiers": {"back": "B_Tier"}
        }
    },
    "pendlay_row": {
        "exercise_id": "EX_318",
        "exercise_name": "Penlay Row",
        "muscle_data": {
            "primary_targets": ["back", "rhomboids"],
            "secondary_muscles": ["lower_back", "core"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "weight_plates"]},
        "biomechanics": {"joint_stress": ["lumbar_shear"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "strength_block", "strength_block"],
            "hypertrophy_tiers": {"back": "B_Tier"}
        }
    },
    "freestanding_t_bar_row": {
        "exercise_id": "EX_319",
        "exercise_name": "Freestanding T-Bar Row",
        "muscle_data": {
            "primary_targets": ["back"],
            "secondary_muscles": ["lower_back", "biceps"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "v_bar_handle"]},
        "biomechanics": {"joint_stress": ["lumbar_shear"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "recomposition", "strength_block"],
            "hypertrophy_tiers": {"back": "B_Tier"}
        }
    },
    "standing_rope_face_pull": {
        "exercise_id": "EX_320",
        "exercise_name": "Standing Rope Face Pull",
        "muscle_data": {
            "primary_targets": ["rear_delts", "traps"],
            "secondary_muscles": ["rhomboids"],
            "movement_pattern": "rear_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "rope_attachment"]},
        "biomechanics": {"joint_stress": ["lumbar_shear_if_heavy"], "pre_hab_for": ["posture_correction"]},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "build_and_burn", "recomposition", "recomposition"],
            "hypertrophy_tiers": {"back": "B_Tier"}
        }
    },

    # ==========================================
    # BICEPS (S, A, B Tiers)
    # ==========================================
    "face_away_bayesian_cable_curl": {
        "exercise_id": "EX_321",
        "exercise_name": "Face-Away Bayesian Cable Curl",
        "muscle_data": {
            "primary_targets": ["biceps"],
            "secondary_muscles": [],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "d_handle"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior_stretch"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"biceps": "S_Tier"}
        }
    },
    "45_degree_preacher_curl": {
        "exercise_id": "EX_322",
        "exercise_name": "45° Preacher Curl",
        "muscle_data": {
            "primary_targets": ["biceps"],
            "secondary_muscles": [],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["preacher_bench", "ez_bar"]},
        "biomechanics": {"joint_stress": ["elbow_tendon_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"biceps": "S_Tier"}
        }
    },
    "machine_preacher_curl": {
        "exercise_id": "EX_323",
        "exercise_name": "Machine Preacher Curl",
        "muscle_data": {
            "primary_targets": ["biceps"],
            "secondary_muscles": [],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["bicep_curl_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"biceps": "S_Tier"}
        }
    },
    "hammer_grip_preacher_curl": {
        "exercise_id": "EX_324",
        "exercise_name": "Hammer Grip Preacher Curl",
        "muscle_data": {
            "primary_targets": ["brachialis", "biceps"],
            "secondary_muscles": ["forearms"],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["preacher_bench", "dumbbells"]},
        "biomechanics": {"joint_stress": ["elbow_tendon_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"biceps": "S_Tier"}
        }
    },
    "ez_bar_curl": {
        "exercise_id": "EX_325",
        "exercise_name": "EZ Bar Curl",
        "muscle_data": {
            "primary_targets": ["biceps"],
            "secondary_muscles": ["forearms"],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["ez_bar", "weight_plates"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"biceps": "A_Tier"}
        }
    },
    "dumbbell_hammer_curl": {
        "exercise_id": "EX_326",
        "exercise_name": "Dumbbell Hammer Curl",
        "muscle_data": {
            "primary_targets": ["brachialis", "biceps"],
            "secondary_muscles": ["forearms"],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["elbow_health"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"biceps": "A_Tier"}
        }
    },
    "incline_dumbbell_curl": {
        "exercise_id": "EX_327",
        "exercise_name": "Incline Dumbbell Curl",
        "muscle_data": {
            "primary_targets": ["biceps_long_head"],
            "secondary_muscles": [],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "incline_bench"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior_stretch"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"biceps": "A_Tier"}
        }
    },
    "standing_dumbbell_curl": {
        "exercise_id": "EX_328",
        "exercise_name": "Standing Dumbbell Curl",
        "muscle_data": {
            "primary_targets": ["biceps"],
            "secondary_muscles": ["forearms"],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"biceps": "A_Tier"}
        }
    },
    "lying_dumbbell_curl": {
        "exercise_id": "EX_329",
        "exercise_name": "Lying Dumbbell Curl",
        "muscle_data": {
            "primary_targets": ["biceps"],
            "secondary_muscles": [],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"biceps": "A_Tier"}
        }
    },
    "cable_curl": {
        "exercise_id": "EX_330",
        "exercise_name": "Cable Curl",
        "muscle_data": {
            "primary_targets": ["biceps"],
            "secondary_muscles": [],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "straight_bar_or_rope"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"biceps": "A_Tier"}
        }
    },
    "inverse_zottman_curl": {
        "exercise_id": "EX_331",
        "exercise_name": "Inverse Zottman Curl",
        "muscle_data": {
            "primary_targets": ["biceps", "brachioradialis"],
            "secondary_muscles": ["forearms"],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells"]},
        "biomechanics": {"joint_stress": ["wrist_strain_if_heavy"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"biceps": "A_Tier"}
        }
    },
    "strict_curl": {
        "exercise_id": "EX_332",
        "exercise_name": "Strict Curl",
        "muscle_data": {
            "primary_targets": ["biceps"],
            "secondary_muscles": [],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "wall_for_support"]},
        "biomechanics": {"joint_stress": ["elbow_tendon_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "recomposition", "strength_block"],
            "hypertrophy_tiers": {"biceps": "A_Tier"}
        }
    },
    "modified_21s": {
        "exercise_id": "EX_333",
        "exercise_name": "Modified 21s",
        "muscle_data": {
            "primary_targets": ["biceps"],
            "secondary_muscles": ["forearms"],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell_or_dumbbells"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "hypertrophy_volume"],
            "hypertrophy_tiers": {"biceps": "A_Tier"}
        }
    },
    "cheat_curl": {
        "exercise_id": "EX_334",
        "exercise_name": "Cheat Curl",
        "muscle_data": {
            "primary_targets": ["biceps"],
            "secondary_muscles": ["forearms", "core"],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "weight_plates"]},
        "biomechanics": {"joint_stress": ["lumbar_shear"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["strength_block"],
            "hypertrophy_tiers": {"biceps": "A_Tier"}
        }
    },
    "barbell_curl": {
        "exercise_id": "EX_335",
        "exercise_name": "Barbell Curl",
        "muscle_data": {
            "primary_targets": ["biceps"],
            "secondary_muscles": ["forearms"],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "weight_plates"]},
        "biomechanics": {"joint_stress": ["wrist_strain", "elbow_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "recomposition", "strength_block"],
            "hypertrophy_tiers": {"biceps": "B_Tier"}
        }
    },
    "flat_bench_curl": {
        "exercise_id": "EX_336",
        "exercise_name": "Flat Bench Curl",
        "muscle_data": {
            "primary_targets": ["biceps"],
            "secondary_muscles": [],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior_stretch"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"biceps": "B_Tier"}
        }
    },
    # ==========================================
    # S TIER (Shoulders)
    # ==========================================
    "cable_lateral_raise": {
        "exercise_id": "EX_401",
        "exercise_name": "Cable Lateral Raise",
        "muscle_data": {
            "primary_targets": ["side_delts"],
            "secondary_muscles": ["front_delts"],
            "movement_pattern": "side_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "d_handle"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"shoulders": "S_Tier"}
        }
    },
    "reverse_cable_crossover": {
        "exercise_id": "EX_402",
        "exercise_name": "Reverse Cable Crossover",
        "muscle_data": {
            "primary_targets": ["rear_delts"],
            "secondary_muscles": ["rhomboids", "traps"],
            "movement_pattern": "rear_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["posture_correction"]},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"shoulders": "S_Tier"}
        }
    },
    "cable_y_raise": {
        "exercise_id": "EX_403",
        "exercise_name": "Cable Y-Raise",
        "muscle_data": {
            "primary_targets": ["side_delts", "lower_traps"],
            "secondary_muscles": ["front_delts"],
            "movement_pattern": "side_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine"]},
        "biomechanics": {"joint_stress": ["shoulder_impingement_if_poor_mobility"], "pre_hab_for": ["scapular_stability"]},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"shoulders": "S_Tier"}
        }
    },
    "behind_the_back_cuffed_lateral_raise": {
        "exercise_id": "EX_404",
        "exercise_name": "Behind-the-Back Cuffed Lateral Raise",
        "muscle_data": {
            "primary_targets": ["side_delts"],
            "secondary_muscles": [],
            "movement_pattern": "side_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "pro_gym", "specific_tools": ["cable_machine", "cuff_attachment"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"shoulders": "S_Tier"}
        }
    },
    "reverse_pec_deck": {
        "exercise_id": "EX_405",
        "exercise_name": "Reverse Pec Deck (Sideways)",
        "muscle_data": {
            "primary_targets": ["rear_delts"],
            "secondary_muscles": ["rhomboids", "traps"],
            "movement_pattern": "rear_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["pec_deck_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"shoulders": "S_Tier"}
        }
    },

    # ==========================================
    # A TIER (Shoulders)
    # ==========================================
    "machine_shoulder_press": {
        "exercise_id": "EX_406",
        "exercise_name": "Machine Shoulder Press",
        "muscle_data": {
            "primary_targets": ["front_delts"],
            "secondary_muscles": ["triceps", "upper_chest"],
            "movement_pattern": "vertical_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["shoulder_press_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"shoulders": "A_Tier"}
        }
    },
    "atlantis_standing_machine_lateral_raise": {
        "exercise_id": "EX_407",
        "exercise_name": "Atlantis Standing Machine Lateral Raise",
        "muscle_data": {
            "primary_targets": ["side_delts"],
            "secondary_muscles": [],
            "movement_pattern": "side_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "pro_gym", "specific_tools": ["lateral_raise_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"shoulders": "A_Tier"}
        }
    },
    "seated_db_shoulder_press": {
        "exercise_id": "EX_408",
        "exercise_name": "Seated Dumbbell Shoulder Press",
        "muscle_data": {
            "primary_targets": ["front_delts"],
            "secondary_muscles": ["triceps", "upper_chest"],
            "movement_pattern": "vertical_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": ["shoulder_impingement_if_flared", "lumbar_compression"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "build_and_burn", "foundation", "recomposition", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"shoulders": "A_Tier"}
        }
    },
    "leaning_in_db_lateral_raise": {
        "exercise_id": "EX_409",
        "exercise_name": "Leaning-In Dumbbell Lateral Raise",
        "muscle_data": {
            "primary_targets": ["side_delts"],
            "secondary_muscles": [],
            "movement_pattern": "side_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "pole_or_rack_for_support"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"shoulders": "A_Tier"}
        }
    },
    "arnold_style_side_lying_db_raise": {
        "exercise_id": "EX_410",
        "exercise_name": "Arnold-Style Side Lying Dumbbell Raise",
        "muscle_data": {
            "primary_targets": ["side_delts"],
            "secondary_muscles": ["rear_delts"],
            "movement_pattern": "side_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "incline_bench"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"shoulders": "A_Tier"}
        }
    },
    "rope_face_pull_shoulders": {
        "exercise_id": "EX_411",
        "exercise_name": "Rope Face Pull",
        "muscle_data": {
            "primary_targets": ["rear_delts", "traps"],
            "secondary_muscles": ["rhomboids"],
            "movement_pattern": "rear_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "rope_attachment"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["shoulder_posture", "rotator_cuff_health"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"shoulders": "A_Tier", "back": "A_Tier"}
        }
    },

    # ==========================================
    # B TIER (Shoulders)
    # ==========================================
    "barbell_overhead_press": {
        "exercise_id": "EX_412",
        "exercise_name": "Barbell Overhead Press",
        "muscle_data": {
            "primary_targets": ["front_delts"],
            "secondary_muscles": ["triceps", "core", "upper_chest"],
            "movement_pattern": "vertical_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "squat_rack", "weight_plates"]},
        "biomechanics": {"joint_stress": ["spinal_compression", "lumbar_shear", "shoulder_impingement"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "recomposition", "strength_block", "strength_block"],
            "hypertrophy_tiers": {"shoulders": "B_Tier"}
        }
    },
    "standing_db_lateral_raise": {
        "exercise_id": "EX_413",
        "exercise_name": "Standing Dumbbell Lateral Raise",
        "muscle_data": {
            "primary_targets": ["side_delts"],
            "secondary_muscles": ["traps"],
            "movement_pattern": "side_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells"]},
        "biomechanics": {"joint_stress": ["shoulder_impingement_if_internally_rotated"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume", "peak_metabolic"],
            "hypertrophy_tiers": {"shoulders": "B_Tier"}
        }
    },
    "super_rom_lateral_raise": {
        "exercise_id": "EX_414",
        "exercise_name": "Super ROM Lateral Raise",
        "muscle_data": {
            "primary_targets": ["side_delts"],
            "secondary_muscles": ["traps"],
            "movement_pattern": "side_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells"]},
        "biomechanics": {"joint_stress": ["shoulder_impingement_at_top"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"shoulders": "B_Tier"}
        }
    },
    "upright_row": {
        "exercise_id": "EX_415",
        "exercise_name": "Upright Row",
        "muscle_data": {
            "primary_targets": ["side_delts", "traps"],
            "secondary_muscles": ["biceps"],
            "movement_pattern": "vertical_pull", 
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell_or_ez_bar"]},
        "biomechanics": {"joint_stress": ["severe_shoulder_impingement", "wrist_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"shoulders": "B_Tier"}
        }
    },
    "bent_over_reverse_db_fly": {
        "exercise_id": "EX_416",
        "exercise_name": "Bent-Over Reverse Dumbbell Fly",
        "muscle_data": {
            "primary_targets": ["rear_delts"],
            "secondary_muscles": ["rhomboids"],
            "movement_pattern": "rear_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells"]},
        "biomechanics": {"joint_stress": ["lumbar_shear"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"shoulders": "B_Tier"}
        }
    },
    "seated_machine_lateral_raise": {
        "exercise_id": "EX_417",
        "exercise_name": "Seated Machine Lateral Raise",
        "muscle_data": {
            "primary_targets": ["side_delts"],
            "secondary_muscles": [],
            "movement_pattern": "side_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["lateral_raise_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"shoulders": "B_Tier"}
        }
    },
    # batch_5_core

    # ==========================================
    # S TIER (Core)
    # ==========================================
    "hollow_body_crunch": {
        "exercise_id": "EX_501",
        "exercise_name": "Hollow Body Crunch",
        "muscle_data": {
            "primary_targets": ["core"],
            "secondary_muscles": ["hip_flexors"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": []},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["lumbar_stability"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"core": "S_Tier"}
        }
    },

    # ==========================================
    # A TIER (Core)
    # ==========================================
    "long_lever_plank": {
        "exercise_id": "EX_502",
        "exercise_name": "Long Lever Plank",
        "muscle_data": {
            "primary_targets": ["core"],
            "secondary_muscles": ["shoulders", "lats"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": []},
        "biomechanics": {"joint_stress": ["shoulder_anterior_stretch"], "pre_hab_for": ["anti_extension"]},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "build_and_burn", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"core": "A_Tier"}
        }
    },
    "knee_raises": {
        "exercise_id": "EX_503",
        "exercise_name": "Knee Raises",
        "muscle_data": {
            "primary_targets": ["core"],
            "secondary_muscles": ["hip_flexors"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": []},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn", "recomposition"],
            "hypertrophy_tiers": {"core": "A_Tier"}
        }
    },
    "side_plank_raise": {
        "exercise_id": "EX_504",
        "exercise_name": "Side Plank / Side Plank Raise",
        "muscle_data": {
            "primary_targets": ["obliques", "core"],
            "secondary_muscles": ["shoulders"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": []},
        "biomechanics": {"joint_stress": ["shoulder_strain_if_weak"], "pre_hab_for": ["lateral_stability"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn", "recomposition", "strength_block"],
            "hypertrophy_tiers": {"core": "A_Tier"}
        }
    },
    "reverse_crunch": {
        "exercise_id": "EX_505",
        "exercise_name": "Reverse Crunch",
        "muscle_data": {
            "primary_targets": ["core"],
            "secondary_muscles": ["hip_flexors"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": []},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["pelvic_control"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"core": "A_Tier"}
        }
    },

    # ==========================================
    # B TIER (Core)
    # ==========================================
    "dead_bug": {
        "exercise_id": "EX_506",
        "exercise_name": "Dead Bug",
        "muscle_data": {
            "primary_targets": ["core"],
            "secondary_muscles": ["hip_flexors"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": []},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["lumbar_stability", "coordination"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn", "recomposition"],
            "hypertrophy_tiers": {"core": "B_Tier"}
        }
    },
    "mountain_climbers": {
        "exercise_id": "EX_507",
        "exercise_name": "Mountain Climbers",
        "muscle_data": {
            "primary_targets": ["core"],
            "secondary_muscles": ["shoulders", "cardio_system"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": []},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "build_and_burn", "peak_metabolic"],
            "hypertrophy_tiers": {"core": "B_Tier"}
        }
    },
    "basic_plank": {
        "exercise_id": "EX_508",
        "exercise_name": "Basic Plank",
        "muscle_data": {
            "primary_targets": ["core"],
            "secondary_muscles": ["shoulders"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": []},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["anti_extension"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn"],
            "hypertrophy_tiers": {"core": "B_Tier"}
        }
    },
    "leg_raises": {
        "exercise_id": "EX_509",
        "exercise_name": "Leg Raises",
        "muscle_data": {
            "primary_targets": ["core"],
            "secondary_muscles": ["hip_flexors"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": []},
        "biomechanics": {"joint_stress": ["lumbar_shear_if_arched"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"core": "B_Tier"}
        }
    },
    "heel_taps": {
        "exercise_id": "EX_510",
        "exercise_name": "Heel Taps",
        "muscle_data": {
            "primary_targets": ["obliques", "core"],
            "secondary_muscles": [],
            "movement_pattern": "core_stabilization",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": []},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn"],
            "hypertrophy_tiers": {"core": "B_Tier"}
        }
    },
    "candle_raise": {
        "exercise_id": "EX_511",
        "exercise_name": "Candle Raise",
        "muscle_data": {
            "primary_targets": ["core"],
            "secondary_muscles": ["hip_flexors", "lower_back"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": []},
        "biomechanics": {"joint_stress": ["neck_strain_if_unsupported"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"core": "B_Tier"}
        }
    },
    "russian_twist": {
        "exercise_id": "EX_512",
        "exercise_name": "Russian Twist",
        "muscle_data": {
            "primary_targets": ["obliques", "core"],
            "secondary_muscles": ["hip_flexors"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": []},
        "biomechanics": {"joint_stress": ["lumbar_torsion_if_weighted_heavily"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "build_and_burn", "recomposition"],
            "hypertrophy_tiers": {"core": "B_Tier"}
        }
    },
    "dragon_flag": {
        "exercise_id": "EX_513",
        "exercise_name": "Dragon Flag",
        "muscle_data": {
            "primary_targets": ["core"],
            "secondary_muscles": ["lats", "hip_flexors"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["bench"]},
        "biomechanics": {"joint_stress": ["cervical_spine_pressure"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"core": "B_Tier"}
        }
    },
    "rollout": {
        "exercise_id": "EX_514",
        "exercise_name": "Rollout",
        "muscle_data": {
            "primary_targets": ["core"],
            "secondary_muscles": ["lats", "shoulders"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["ab_wheel", ]},
        "biomechanics": {"joint_stress": ["lumbar_extension_strain_if_weak"], "pre_hab_for": ["anti_extension"]},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"core": "B_Tier"}
        }
    },
    #----------------------------------------------------------
    #NO EQUIPMENT EXERCISES
    # ---------------------------------------------------------
    # PUSH EXERCISES
    # ---------------------------------------------------------
    "standard_push_ups": {
        "exercise_id": "EX_BW_101",
        "exercise_name": "Push-ups (Standard)",
        "muscle_data": {
            "primary_targets": ["chest", "front_delt", "triceps"],
            "secondary_muscles": ["core_stabilization"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "bodyweight_only", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["wrists"], 
            "pre_hab_for": ["serratus_anterior_activation"]
        },
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition_1", "recomposition_2", "hypertrophy_volume", "peak_metabolic", "active_lifestyle"],
            "hypertrophy_tiers": {"chest": "A_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", "reps": "8-20 (to RPE 8-9)", 
            "tempo": "3 seconds down, explosive up"
        }
    },
    "incline_push_ups": {
        "exercise_id": "EX_BW_102",
        "exercise_name": "Incline Push-ups",
        "muscle_data": {
            "primary_targets": ["lower_chest", "front_delt", "triceps"],
            "secondary_muscles": ["core_stabilization"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "household_items", 
            "specific_tools": [] # We leave this empty so it passes the equipment filter seamlessly
        },
        "biomechanics": {
            "joint_stress": ["wrists"], 
            "pre_hab_for": ["shoulder_stability"]
        },
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition_1", "recomposition_2", "active_lifestyle"],
            "hypertrophy_tiers": {"lower_chest": "B_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", "reps": "8-20 (to RPE 8-9)", 
            "tempo": "3 seconds down, explosive up"
        }
    },
    "decline_push_ups": {
        "exercise_id": "EX_BW_103",
        "exercise_name": "Decline Push-ups",
        "muscle_data": {
            "primary_targets": ["upper_chest", "front_delt", "triceps"],
            "secondary_muscles": ["core_stabilization"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "household_items", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["wrists", "anterior_shoulder"], 
            "pre_hab_for": ["upper_chest_activation"]
        },
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition_1", "recomposition_2", "hypertrophy_volume", "peak_metabolic"],
            "hypertrophy_tiers": {"upper_chest": "A_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", "reps": "8-20 (to RPE 8-9)", 
            "tempo": "3 seconds down, explosive up"
        }
    },
    "diamond_push_ups": {
        "exercise_id": "EX_BW_104",
        "exercise_name": "Diamond Push-ups",
        "muscle_data": {
            "primary_targets": ["triceps", "inner_chest"],
            "secondary_muscles": ["front_delt", "core_stabilization"],
            "movement_pattern": "tricep_isolation",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "bodyweight_only", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["elbows", "wrists"], 
            "pre_hab_for": ["triceps_tendon_conditioning"]
        },
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition_1", "recomposition_2", "hypertrophy_volume", "peak_metabolic"],
            "hypertrophy_tiers": {"triceps": "S_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", "reps": "8-20 (to RPE 8-9)", 
            "tempo": "3 seconds down, explosive up"
        }
    },
    "pike_push_ups": {
        "exercise_id": "EX_BW_105",
        "exercise_name": "Pike Push-ups",
        "muscle_data": {
            "primary_targets": ["front_delt", "side_delt", "triceps"],
            "secondary_muscles": ["upper_chest", "core_stabilization"],
            "movement_pattern": "vertical_press",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "bodyweight_only", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["shoulders", "wrists"], 
            "pre_hab_for": ["overhead_mobility"]
        },
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition_1", "recomposition_2", "hypertrophy_volume"],
            "hypertrophy_tiers": {"front_delt": "A_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", "reps": "8-20 (to RPE 8-9)", 
            "tempo": "3 seconds down, explosive up",
            "notes": "Keep hips high and shift weight forward onto the shoulders."
        }
    },
    "pseudo_planche_push_ups": {
        "exercise_id": "EX_BW_106",
        "exercise_name": "Pseudo Planche Push-ups",
        "muscle_data": {
            "primary_targets": ["front_delt", "chest", "triceps"],
            "secondary_muscles": ["core_stabilization", "biceps"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "bodyweight_only", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["wrists", "biceps_tendon"], 
            "pre_hab_for": ["straight_arm_scapular_strength"]
        },
        "periodization_tags": {
            "allowed_phases": ["recomposition_2", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"front_delt": "S_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", "reps": "8-20 (to RPE 8-9)", 
            "tempo": "3 seconds down, explosive up",
            "notes": "Lean shoulders far over the wrists. Very advanced."
        }
    },

    # ---------------------------------------------------------
    # PULL & HINGE EXERCISES
    # ---------------------------------------------------------
    "inverted_table_rows": {
        "exercise_id": "EX_BW_201",
        "exercise_name": "Inverted Table Rows",
        "muscle_data": {
            "primary_targets": ["lats", "rhomboids", "biceps"],
            "secondary_muscles": ["core_stabilization", "rear_delts"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "household_items", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["none"], 
            "pre_hab_for": ["thoracic_extension", "posture_correction"]
        },
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition_1", "recomposition_2", "hypertrophy_volume"],
            "hypertrophy_tiers": {"mid_back": "A_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", "reps": "8-15 (to RPE 8-9)", 
            "tempo": "3 seconds down, explosive up",
            "notes": "Lie under a sturdy table, grip the edge, and pull your chest to the wood."
        }
    },
    "towel_doorway_rows": {
        "exercise_id": "EX_BW_202",
        "exercise_name": "Towel Doorway Rows",
        "muscle_data": {
            "primary_targets": ["lats", "mid_back", "biceps"],
            "secondary_muscles": ["forearms", "rear_delts"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "household_items", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["none"], 
            "pre_hab_for": ["grip_strength"]
        },
        "periodization_tags": {
            "allowed_phases": ["foundation", "active_lifestyle", "build_and_burn"],
            "hypertrophy_tiers": {"lats": "B_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", "reps": "8-15 (to RPE 8-9)", 
            "tempo": "3 seconds down, squeeze at the top",
            "notes": "Wrap a thick towel around a sturdy door handle. Lean back and pull."
        }
    },
    "wall_pull_holds": {
        "exercise_id": "EX_BW_203",
        "exercise_name": "Wall Pull Holds (Isometric)",
        "muscle_data": {
            "primary_targets": ["lats", "teres_major"],
            "secondary_muscles": ["core_stabilization"],
            "movement_pattern": "vertical_pull",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "bodyweight_only", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["none"], 
            "pre_hab_for": ["lat_activation", "mind_muscle_connection"]
        },
        "periodization_tags": {
            "allowed_phases": ["foundation", "active_lifestyle", "recomposition_1"],
            "hypertrophy_tiers": {"lats": "B_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", "reps": "20-40 second max-effort holds", 
            "tempo": "Isometric",
            "notes": "Stand with your back to a wall, drive your elbows back into the wall as hard as possible to contract the lats."
        }
    },
    "reverse_snow_angels": {
        "exercise_id": "EX_BW_204",
        "exercise_name": "Reverse Snow Angels",
        "muscle_data": {
            "primary_targets": ["rear_delts", "rhomboids", "lower_traps"],
            "secondary_muscles": ["lower_back"],
            "movement_pattern": "rear_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {
            "facility_tier": "bodyweight_only", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["none"], 
            "pre_hab_for": ["scapular_retraction", "rotator_cuff"]
        },
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition_1", "recomposition_2", "hypertrophy_volume"],
            "hypertrophy_tiers": {"rear_delts": "A_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", "reps": "10-15 (to RPE 8-9)", 
            "tempo": "Slow and controlled",
            "notes": "Lie face down. Keep arms straight and sweep them from your hips to above your head without touching the floor."
        }
    },
    "superman_holds": {
        "exercise_id": "EX_BW_205",
        "exercise_name": "Superman Holds",
        "muscle_data": {
            "primary_targets": ["erector_spinae", "glutes"],
            "secondary_muscles": ["hamstrings", "rhomboids"],
            "movement_pattern": "hinge_pattern",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "bodyweight_only", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["lumbar_compression"], 
            "pre_hab_for": ["lower_back_endurance"]
        },
        "periodization_tags": {
            "allowed_phases": ["foundation", "active_lifestyle", "build_and_burn", "recomposition_1"],
            "hypertrophy_tiers": {"lower_back": "B_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", "reps": "20-40 second holds (or 10-15 slow reps)", 
            "tempo": "Hold at the top contraction",
            "notes": "Lie face down, squeeze glutes, and lift chest and thighs off the floor."
        }
    },
    "pull_ups_standard": {
        "exercise_id": "EX_BW_206",
        "exercise_name": "Pull-ups (Standard)",
        "muscle_data": {
            "primary_targets": ["lats", "biceps", "upper_back"],
            "secondary_muscles": ["core_stabilization", "forearms"],
            "movement_pattern": "vertical_pull",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "home_minimal", 
            "specific_tools": ["pullup_bar"] # The only specific tool required
        },
        "biomechanics": {
            "joint_stress": ["shoulders", "elbows"], 
            "pre_hab_for": ["spinal_decompression"]
        },
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition_1", "recomposition_2", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"lats": "S_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", "reps": "AMRAP (As Many Reps As Possible)", 
            "tempo": "Controlled descent",
            "notes": "If you cannot perform a full pull-up, do slow negative descents."
        }
    },
    "wide_grip_inverted_rows": {
        "exercise_id": "EX_BW_207",
        "exercise_name": "Wide-Grip Inverted Rows",
        "muscle_data": {
            "primary_targets": ["upper_back", "rear_delts"],
            "secondary_muscles": ["lats", "biceps", "core_stabilization"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "household_items", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["shoulders"], 
            "pre_hab_for": ["postural_alignment"]
        },
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition_1", "recomposition_2", "hypertrophy_volume"],
            "hypertrophy_tiers": {"upper_back": "A_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", 
            "reps": "8-15 (to RPE 8-9)", 
            "tempo": "5-second slow negative, explosive up",
            "notes": "Use a wider grip to shift focus to the upper back. Establish a strong mind-muscle connection."
        }
    },
    "close_grip_inverted_rows": {
        "exercise_id": "EX_BW_208",
        "exercise_name": "Close-Grip Inverted Rows",
        "muscle_data": {
            "primary_targets": ["lats", "biceps"],
            "secondary_muscles": ["mid_back", "core_stabilization"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "household_items", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["elbows"], 
            "pre_hab_for": ["lat_activation"]
        },
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition_1", "recomposition_2", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"lats": "A_Tier", "biceps": "B_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", 
            "reps": "15-25 (High Rep Protocol)", 
            "tempo": "Controlled tempo",
            "notes": "Keep elbows tucked tight to your sides to maximize lat and bicep engagement."
        }
    },
    "single_arm_assisted_rows": {
        "exercise_id": "EX_BW_209",
        "exercise_name": "Single-Arm Assisted Rows",
        "muscle_data": {
            "primary_targets": ["lats", "unilateral_back"],
            "secondary_muscles": ["biceps", "core_stabilization", "obliques"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True 
        },
        "facility_requirements": {
            "facility_tier": "household_items", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["none"], 
            "pre_hab_for": ["anti_rotation_core", "unilateral_strength"]
        },
        "periodization_tags": {
            "allowed_phases": ["recomposition_2", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"lats": "S_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", 
            "reps": "8-12 per arm (to RPE 8-9)", 
            "tempo": "3 seconds down, 2-3 sec pause at the top",
            "notes": "Use one arm primarily, assisting with the other only when necessary. Squeeze hard at the top."
        }
    },
    "feet_elevated_inverted_rows": {
        "exercise_id": "EX_BW_210",
        "exercise_name": "Feet-Elevated Inverted Rows",
        "muscle_data": {
            "primary_targets": ["lats", "mid_back", "biceps"],
            "secondary_muscles": ["rear_delts", "core_stabilization"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "household_items", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["none"], 
            "pre_hab_for": ["scapular_retraction"]
        },
        "periodization_tags": {
            "allowed_phases": ["recomposition_1", "recomposition_2", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"mid_back": "S_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", 
            "reps": "8-15 (to RPE 8-9)", 
            "tempo": "5-second slow negative, explosive up",
            "notes": "Elevate feet on a chair to increase load and difficulty."
        }
    },
    "doorframe_rows": {
        "exercise_id": "EX_BW_211",
        "exercise_name": "Doorframe Rows",
        "muscle_data": {
            "primary_targets": ["mid_back", "biceps"],
            "secondary_muscles": ["forearms", "lats"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "household_items", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["fingers", "wrists"], 
            "pre_hab_for": ["grip_strength"]
        },
        "periodization_tags": {
            "allowed_phases": ["foundation", "active_lifestyle", "build_and_burn", "peak_metabolic"],
            "hypertrophy_tiers": {"biceps": "B_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", 
            "reps": "15-25 (High Rep Protocol)", 
            "tempo": "2-3 sec pause at full contraction",
            "notes": "Lean back holding the doorframe and pull yourself in. Move feet closer to the door to increase difficulty."
        }
    },
    "isometric_row_hold_top": {
        "exercise_id": "EX_BW_212",
        "exercise_name": "Top Hold (Row Position)",
        "muscle_data": {
            "primary_targets": ["rhomboids", "mid_back", "lats"],
            "secondary_muscles": ["biceps", "core_stabilization"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "household_items", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["none"], 
            "pre_hab_for": ["scapular_endurance", "postural_correction"]
        },
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition_1", "peak_metabolic", "active_lifestyle"],
            "hypertrophy_tiers": {"mid_back": "B_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", 
            "reps": "20-40 sec holds (to RPE 8-9)", 
            "tempo": "Maximum Isometric Tension",
            "notes": "Hold your chest as close to the bar/table as possible and actively squeeze the back."
        }
    },
    "towel_curl_isometric": {
        "exercise_id": "EX_BW_213",
        "exercise_name": "Towel Curl Hold",
        "muscle_data": {
            "primary_targets": ["biceps", "brachialis"],
            "secondary_muscles": ["forearms", "front_delt"],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {
            "facility_tier": "household_items", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["none"], 
            "pre_hab_for": ["tendon_stiffness", "bicep_activation"]
        },
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition_1", "recomposition_2", "hypertrophy_volume"],
            "hypertrophy_tiers": {"biceps": "A_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", 
            "reps": "15-30 sec max-effort holds", 
            "tempo": "Maximum Isometric Tension",
            "notes": "Step on a towel, grab the ends, and pull up as hard as possible as if curling it. Do not let up tension."
        }
    },
    "prone_y_t_raises": {
        "exercise_id": "EX_BW_214",
        "exercise_name": "Prone Y-T Raises",
        "muscle_data": {
            "primary_targets": ["rear_delts", "lower_traps"],
            "secondary_muscles": ["rhomboids", "lower_back"],
            "movement_pattern": "rear_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {
            "facility_tier": "bodyweight_only", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["none"], 
            "pre_hab_for": ["scapular_health", "shoulder_impingement_prevention"]
        },
        "periodization_tags": {
            "allowed_phases": ["foundation", "active_lifestyle", "build_and_burn", "recomposition_1", "hypertrophy_volume"],
            "hypertrophy_tiers": {"rear_delts": "A_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", 
            "reps": "12-20 (to RPE 8-9)", 
            "tempo": "2-3 sec pause at the top, slow negative",
            "notes": "Lie face down. Raise arms in a 'Y' shape, lower, then a 'T' shape. Focus entirely on mind-muscle connection."
        }
    },
    "cobra_hold": {
        "exercise_id": "EX_BW_215",
        "exercise_name": "Cobra Hold",
        "muscle_data": {
            "primary_targets": ["lower_back", "erector_spinae"],
            "secondary_muscles": ["glutes", "rhomboids"],
            "movement_pattern": "hinge_pattern",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "bodyweight_only", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["lumbar_compression"], 
            "pre_hab_for": ["posture_correction", "spinal_extension"]
        },
        "periodization_tags": {
            "allowed_phases": ["foundation", "active_lifestyle", "build_and_burn", "recomposition_1"],
            "hypertrophy_tiers": {"lower_back": "B_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", 
            "reps": "20-40 sec holds", 
            "tempo": "Isometric",
            "notes": "Lie face down, lift chest, and pull hands back towards your hips, rotating palms outward to engage the back."
        }
    },
    # ---------------------------------------------------------
    # LEG EXERCISES
    # ---------------------------------------------------------
    "bodyweight_squats": {
        "exercise_id": "EX_BW_301",
        "exercise_name": "Bodyweight Squats",
        "muscle_data": {
            "primary_targets": ["quads", "glutes"],
            "secondary_muscles": ["hamstrings", "core_stabilization"],
            "movement_pattern": "squat_pattern",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "bodyweight_only", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["knees", "hips"], 
            "pre_hab_for": ["hip_mobility", "ankle_mobility"]
        },
        "periodization_tags": {
            "allowed_phases": ["foundation", "active_lifestyle", "build_and_burn", "recomposition_1", "peak_metabolic"],
            "hypertrophy_tiers": {"quads": "A_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", "reps": "12-25 (to RPE 8-9)", 
            "tempo": "3 seconds down, explosive up, add pauses at bottom for intensity"
        }
    },
    "jump_squats": {
        "exercise_id": "EX_BW_302",
        "exercise_name": "Jump Squats",
        "muscle_data": {
            "primary_targets": ["quads", "glutes", "calves"],
            "secondary_muscles": ["hamstrings", "core_stabilization"],
            "movement_pattern": "squat_pattern",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "bodyweight_only", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["knees", "ankles", "lumbar_compression"], 
            "pre_hab_for": ["explosive_power", "landing_mechanics"]
        },
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "peak_metabolic", "active_lifestyle"],
            "hypertrophy_tiers": {"quads": "B_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", "reps": "12-25 (to RPE 8-9)", 
            "tempo": "Explosive jump, soft and controlled landing"
        }
    },
    "walking_lunges": {
        "exercise_id": "EX_BW_303",
        "exercise_name": "Walking Lunges",
        "muscle_data": {
            "primary_targets": ["quads", "glutes"],
            "secondary_muscles": ["hamstrings", "core_stabilization"],
            "movement_pattern": "unilateral_leg",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "bodyweight_only", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["knees", "hips"], 
            "pre_hab_for": ["unilateral_stability", "knee_tracking"]
        },
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition_1", "recomposition_2", "hypertrophy_volume", "peak_metabolic"],
            "hypertrophy_tiers": {"quads": "A_Tier", "glutes": "A_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", "reps": "12-25 per leg (to RPE 8-9)", 
            "tempo": "3 seconds down, explosive up, add pauses at bottom for intensity"
        }
    },
    "bulgarian_split_squats": {
        "exercise_id": "EX_BW_304",
        "exercise_name": "Bulgarian Split Squats",
        "muscle_data": {
            "primary_targets": ["quads", "glutes"],
            "secondary_muscles": ["hamstrings", "core_stabilization"],
            "movement_pattern": "unilateral_leg",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "household_items", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["knees", "hips"], 
            "pre_hab_for": ["unilateral_strength", "hip_flexor_stretch"]
        },
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition_1", "recomposition_2", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"quads": "S_Tier", "glutes": "S_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", "reps": "12-25 per leg (to RPE 8-9)", 
            "tempo": "3 seconds down, explosive up, add pauses at bottom for intensity",
            "notes": "Elevate rear foot on a chair or bench."
        }
    },
    "glute_bridges": {
        "exercise_id": "EX_BW_305",
        "exercise_name": "Glute Bridges",
        "muscle_data": {
            "primary_targets": ["glutes"],
            "secondary_muscles": ["hamstrings", "lower_back"],
            "movement_pattern": "glute_isolation",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "bodyweight_only", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["none"], 
            "pre_hab_for": ["glute_activation", "pelvic_control"]
        },
        "periodization_tags": {
            "allowed_phases": ["foundation", "active_lifestyle", "build_and_burn", "recomposition_1"],
            "hypertrophy_tiers": {"glutes": "A_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", "reps": "12-25 (to RPE 8-9)", 
            "tempo": "Explosive up, squeeze for 2 seconds, slow down",
            "notes": "Add pauses at top contraction for intensity."
        }
    },
    "wall_sit": {
        "exercise_id": "EX_BW_306",
        "exercise_name": "Wall Sit",
        "muscle_data": {
            "primary_targets": ["quads"],
            "secondary_muscles": ["glutes", "calves"],
            "movement_pattern": "quad_isolation",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "bodyweight_only", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["knees"], 
            "pre_hab_for": ["isometric_endurance", "patellar_tendon_conditioning"]
        },
        "periodization_tags": {
            "allowed_phases": ["foundation", "active_lifestyle", "build_and_burn", "peak_metabolic"],
            "hypertrophy_tiers": {"quads": "B_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", "reps": "Isometric Hold (to RPE 8-9)", 
            "tempo": "Isometric hold",
            "notes": "Hold until failure or near failure."
        }
    },
    # ---------------------------------------------------------
    # HAMSTRINGS & GLUTES
    # ---------------------------------------------------------
    "single_leg_glute_bridges": {
        "exercise_id": "EX_BW_307",
        "exercise_name": "Single-Leg Glute Bridges",
        "muscle_data": {
            "primary_targets": ["glutes", "hamstrings"],
            "secondary_muscles": ["lower_back", "core_stabilization"],
            "movement_pattern": "unilateral_leg",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "bodyweight_only", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["none"], 
            "pre_hab_for": ["pelvic_stability", "glute_medius_activation"]
        },
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition_1", "recomposition_2", "hypertrophy_volume", "peak_metabolic"],
            "hypertrophy_tiers": {"glutes": "A_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", 
            "reps": "12-20 per leg (to RPE 8-9)", 
            "tempo": "Explosive up, 2-second squeeze, slow down",
            "notes": "Keep the non-working leg straight or bent at 90 degrees. Drive through the heel."
        }
    },
    "bed_hip_thrusts": {
        "exercise_id": "EX_BW_308",
        "exercise_name": "Hip Thrusts (Bed/Chair)",
        "muscle_data": {
            "primary_targets": ["glutes"],
            "secondary_muscles": ["hamstrings", "quads"],
            "movement_pattern": "glute_isolation",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "household_items", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["none"], 
            "pre_hab_for": ["hip_extension_power"]
        },
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition_1", "recomposition_2", "hypertrophy_volume"],
            "hypertrophy_tiers": {"glutes": "S_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", 
            "reps": "15-25 (to RPE 8-9)", 
            "tempo": "Explosive up, hard pause at the top",
            "notes": "Rest your upper back on a sturdy bed or couch. Add pauses at the top for maximum intensity."
        }
    },
    "hamstring_walkouts": {
        "exercise_id": "EX_BW_309",
        "exercise_name": "Hamstring Walkouts",
        "muscle_data": {
            "primary_targets": ["hamstrings"],
            "secondary_muscles": ["glutes", "core_stabilization"],
            "movement_pattern": "hamstring_isolation",
            "is_compound": False
        },
        "facility_requirements": {
            "facility_tier": "bodyweight_only", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["none"], 
            "pre_hab_for": ["hamstring_tendon_health", "knee_flexion_strength"]
        },
        "periodization_tags": {
            "allowed_phases": ["foundation", "active_lifestyle", "recomposition_1", "recomposition_2", "hypertrophy_volume"],
            "hypertrophy_tiers": {"hamstrings": "A_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", 
            "reps": "8-15 (to RPE 8-9)", 
            "tempo": "Slow and controlled steps",
            "notes": "Start in a glute bridge position. Slowly walk your feet out on your heels until legs are almost straight, then walk them back in. Keep hips high the entire time."
        }
    },

    # ---------------------------------------------------------
    # CALVES
    # ---------------------------------------------------------
    "standing_calf_raises": {
        "exercise_id": "EX_BW_310",
        "exercise_name": "Standing Calf Raises",
        "muscle_data": {
            "primary_targets": ["calves"],
            "secondary_muscles": ["ankles"],
            "movement_pattern": "calf_isolation",
            "is_compound": False
        },
        "facility_requirements": {
            "facility_tier": "bodyweight_only", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["ankles"], 
            "pre_hab_for": ["achilles_tendon_stiffness"]
        },
        "periodization_tags": {
            "allowed_phases": ["foundation", "active_lifestyle", "build_and_burn", "peak_metabolic"],
            "hypertrophy_tiers": {"calves": "B_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", 
            "reps": "20-30 (to RPE 8-9)", 
            "tempo": "3 seconds down, explosive up, 1-second pause at the top",
            "notes": "Do these on a stair edge or thick book if available for a deeper stretch."
        }
    },
    "single_leg_calf_raises": {
        "exercise_id": "EX_BW_311",
        "exercise_name": "Single-Leg Calf Raises",
        "muscle_data": {
            "primary_targets": ["calves"],
            "secondary_muscles": ["ankles", "core_stabilization"],
            "movement_pattern": "calf_isolation",
            "is_compound": False
        },
        "facility_requirements": {
            "facility_tier": "bodyweight_only", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["ankles"], 
            "pre_hab_for": ["ankle_stability", "unilateral_balance"]
        },
        "periodization_tags": {
            "allowed_phases": ["recomposition_1", "recomposition_2", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"calves": "A_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", 
            "reps": "12-20 per leg (to RPE 8-9)", 
            "tempo": "3 seconds down, explosive up",
            "notes": "Hold onto a wall or chair for balance so you can focus entirely on the calf muscle."
        }
    },
    "explosive_calf_jumps": {
        "exercise_id": "EX_BW_312",
        "exercise_name": "Explosive Calf Jumps",
        "muscle_data": {
            "primary_targets": ["calves"],
            "secondary_muscles": ["quads", "ankles"],
            "movement_pattern": "calf_isolation",
            "is_compound": True
        },
        "facility_requirements": {
            "facility_tier": "bodyweight_only", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["ankles", "knees"], 
            "pre_hab_for": ["plyometric_elasticity"]
        },
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "peak_metabolic", "active_lifestyle"],
            "hypertrophy_tiers": {"calves": "B_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", 
            "reps": "15-25", 
            "tempo": "Rapid, pogo-stick style jumps",
            "notes": "Keep knees mostly straight. Generate all the jumping power from your ankles and calves."
        }
    },
    "wall_supported_calf_holds": {
        "exercise_id": "EX_BW_313",
        "exercise_name": "Wall-Supported Calf Holds",
        "muscle_data": {
            "primary_targets": ["calves"],
            "secondary_muscles": ["ankles"],
            "movement_pattern": "calf_isolation",
            "is_compound": False
        },
        "facility_requirements": {
            "facility_tier": "bodyweight_only", 
            "specific_tools": []
        },
        "biomechanics": {
            "joint_stress": ["none"], 
            "pre_hab_for": ["isometric_endurance", "achilles_health"]
        },
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition_1", "active_lifestyle"],
            "hypertrophy_tiers": {"calves": "B_Tier"}
        },
        "execution_guidelines": {
            "sets": "3-5", 
            "reps": "30-60 sec holds", 
            "tempo": "Maximum Isometric Tension",
            "notes": "Press high onto your toes while leaning against a wall. Squeeze and hold until failure."
        }
    }
}