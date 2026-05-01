exercise_dataset = {
    # ==========================================
    # GLUTES & QUADS
    # ==========================================
    "walking_lunges": {
        "exercise_id": "EX_101",
        "exercise_name": "Walking Lunges",
        "youtube_id": "dlkuCygIEAA",
        "muscle_data": {
            "primary_targets": ["glutes", "quads"],
            "secondary_muscles": ["hamstrings", "core"],
            "movement_pattern": "unilateral_leg",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells"]},
        "biomechanics": {"joint_stress": ["knee_torque"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume", "peak_metabolic"],
            "hypertrophy_tiers": {"glutes": "S_Plus", "quads": "B_Tier"}
        }
    },
    "machine_hip_abduction": {
        "exercise_id": "EX_102",
        "exercise_name": "Machine Hip Abduction",
        "youtube_id": "GpwSQE2F400",
        "muscle_data": {
            "primary_targets": ["glutes"],
            "secondary_muscles": [],
            "movement_pattern": "glute_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "pro_gym", "specific_tools": ["abduction_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"glutes": "S_Tier"}
        }
    },
    "deficit_lunges": {
        "exercise_id": "EX_103",
        "exercise_name": "Deficit Lunges (Front Foot Elevated)",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["glutes", "quads"],
            "secondary_muscles": ["hamstrings"],
            "movement_pattern": "unilateral_leg",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["dumbbells", "step_platform"]},
        "biomechanics": {"joint_stress": ["knee_torque", "hip_flexor_stretch"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "strength_block", "hypertrophy_volume"],
            "hypertrophy_tiers": {"glutes": "S_Tier"}
        }
    },
    "45_degree_back_extension": {
        "exercise_id": "EX_104",
        "exercise_name": "45° Back Extension",
        "youtube_id": "ph3pddpKzzw",
        "muscle_data": {
            "primary_targets": ["glutes", "hamstrings"],
            "secondary_muscles": ["lower_back"],
            "movement_pattern": "hinge_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["back_extension_machine"]},
        "biomechanics": {"joint_stress": ["lumbar_shear"], "pre_hab_for": ["lower_back_strengthening"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"glutes": "S_Tier"}
        }
    },
    "hack_squat": {
        "exercise_id": "EX_105",
        "exercise_name": "Hack Squat",
        "youtube_id": "rYgF8A4RM_E",
        "muscle_data": {
            "primary_targets": ["quads"],
            "secondary_muscles": ["glutes"],
            "movement_pattern": "squat_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "pro_gym", "specific_tools": ["hack_squat_machine"]},
        "biomechanics": {"joint_stress": ["high_knee_torque"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"quads": "S_Tier"}
        }
    },
    "barbell_back_squat": {
        "exercise_id": "EX_106",
        "exercise_name": "Barbell Back Squat (High Bar)",
        "youtube_id": "1kq6r83K3u4",
        "muscle_data": {
            "primary_targets": ["quads", "glutes"],
            "secondary_muscles": ["core", "lower_back"],
            "movement_pattern": "squat_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "squat_rack", "weight_plates"]},
        "biomechanics": {"joint_stress": ["spinal_compression", "high_knee_torque"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "strength_block", "hypertrophy_volume"],
            "hypertrophy_tiers": {"quads": "S_Tier", "glutes": "A_Tier"}
        }
    },
    "bulgarian_split_squat": {
        "exercise_id": "EX_107",
        "exercise_name": "Bulgarian Split Squat",
        "youtube_id": "2C-uNgKwPLE",
        "muscle_data": {
            "primary_targets": ["quads", "glutes"],
            "secondary_muscles": ["hamstrings", "core"],
            "movement_pattern": "unilateral_leg",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": ["high_knee_torque"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "strength_block", "hypertrophy_volume"],
            "hypertrophy_tiers": {"quads": "S_Tier", "glutes": "A_Tier"}
        }
    },
    "pendulum_squat": {
        "exercise_id": "EX_108",
        "exercise_name": "Pendulum Squat",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["quads"],
            "secondary_muscles": ["glutes"],
            "movement_pattern": "squat_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "pro_gym", "specific_tools": ["pendulum_squat_machine"]},
        "biomechanics": {"joint_stress": ["extreme_knee_torque"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"quads": "S_Tier"}
        }
    },
    "smith_machine_squat": {
        "exercise_id": "EX_109",
        "exercise_name": "Smith Machine Squat",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["quads", "glutes"],
            "secondary_muscles": ["core"],
            "movement_pattern": "squat_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["smith_machine", "weight_plates"]},
        "biomechanics": {"joint_stress": ["spinal_compression", "knee_torque"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"quads": "S_Tier", "glutes": "A_Tier"}
        }
    },
    "hip_thrust_machine": {
        "exercise_id": "EX_110",
        "exercise_name": "Hip Thrust Machine",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["glutes"],
            "secondary_muscles": ["hamstrings"],
            "movement_pattern": "glute_isolation",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "pro_gym", "specific_tools": ["hip_thrust_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"glutes": "A_Tier"}
        }
    },
    "single_leg_db_hip_thrust": {
        "exercise_id": "EX_111",
        "exercise_name": "Single Leg Dumbbell Hip Thrust",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["glutes"],
            "secondary_muscles": ["hamstrings"],
            "movement_pattern": "glute_isolation",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"glutes": "A_Tier"}
        }
    },
    "cable_kickback": {
        "exercise_id": "EX_112",
        "exercise_name": "Cable Kickback",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["glutes"],
            "secondary_muscles": [],
            "movement_pattern": "glute_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "ankle_strap"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"glutes": "A_Tier"}
        }
    },
    "step_up": {
        "exercise_id": "EX_113",
        "exercise_name": "Step Up",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["glutes", "quads"],
            "secondary_muscles": ["core"],
            "movement_pattern": "unilateral_leg",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "plyo_box"]},
        "biomechanics": {"joint_stress": ["knee_torque"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "peak_metabolic"],
            "hypertrophy_tiers": {"glutes": "A_Tier"}
        }
    },
    "smith_machine_lunge": {
        "exercise_id": "EX_114",
        "exercise_name": "Smith Machine Lunge",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["glutes", "quads"],
            "secondary_muscles": ["hamstrings"],
            "movement_pattern": "unilateral_leg",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["smith_machine"]},
        "biomechanics": {"joint_stress": ["knee_torque"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"glutes": "A_Tier"}
        }
    },
    "romanian_deadlift": {
        "exercise_id": "EX_115",
        "exercise_name": "Romanian Deadlift (RDL)",
        "youtube_id": "hCDzSR6bW10",
        "muscle_data": {
            "primary_targets": ["glutes", "hamstrings"],
            "secondary_muscles": ["lower_back", "core"],
            "movement_pattern": "hinge_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "weight_plates"]},
        "biomechanics": {"joint_stress": ["spinal_compression", "lumbar_shear"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "strength_block", "hypertrophy_volume"],
            "hypertrophy_tiers": {"glutes": "A_Tier"}
        }
    },
    "leg_extension": {
        "exercise_id": "EX_116",
        "exercise_name": "Leg Extension",
        "youtube_id": "m0FOpMEjcKc",
        "muscle_data": {
            "primary_targets": ["quads"],
            "secondary_muscles": [],
            "movement_pattern": "quad_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["leg_extension_machine"]},
        "biomechanics": {"joint_stress": ["patellar_tendon_stress"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"quads": "A_Tier"}
        }
    },
    "barbell_front_squat": {
        "exercise_id": "EX_117",
        "exercise_name": "Barbell Front Squat",
        "youtube_id": "v-mQsAWEhKc",
        "muscle_data": {
            "primary_targets": ["quads", "core"],
            "secondary_muscles": ["glutes", "upper_back"],
            "movement_pattern": "squat_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "squat_rack", "weight_plates"]},
        "biomechanics": {"joint_stress": ["spinal_compression", "wrist_strain", "knee_torque"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "strength_block"],
            "hypertrophy_tiers": {"quads": "A_Tier"}
        }
    },
    "low_bar_back_squat": {
        "exercise_id": "EX_118",
        "exercise_name": "Low Bar Back Squat",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["quads", "glutes", "lower_back"],
            "secondary_muscles": ["hamstrings", "core"],
            "movement_pattern": "squat_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "squat_rack", "weight_plates"]},
        "biomechanics": {"joint_stress": ["spinal_compression", "shoulder_mobility_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "strength_block"],
            "hypertrophy_tiers": {"quads": "A_Tier"}
        }
    },
    "45_degree_leg_press": {
        "exercise_id": "EX_119",
        "exercise_name": "45° Leg Press",
        "youtube_id": "yZmx_Ac3880",
        "muscle_data": {
            "primary_targets": ["quads", "glutes"],
            "secondary_muscles": ["hamstrings"],
            "movement_pattern": "squat_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["leg_press_machine"]},
        "biomechanics": {"joint_stress": ["lumbar_flexion_if_deep"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"quads": "A_Tier"}
        }
    },
    "reverse_nordic": {
        "exercise_id": "EX_120",
        "exercise_name": "Reverse Nordic",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["quads"],
            "secondary_muscles": ["core"],
            "movement_pattern": "quad_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["mat"]},
        "biomechanics": {"joint_stress": ["high_knee_torque"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition"],
            "hypertrophy_tiers": {"quads": "A_Tier"}
        }
    },
    "barbell_hip_thrust": {
        "exercise_id": "EX_121",
        "exercise_name": "Barbell Hip Thrust",
        "youtube_id": "EF7mHEm4eYI",
        "muscle_data": {
            "primary_targets": ["glutes"],
            "secondary_muscles": ["hamstrings"],
            "movement_pattern": "glute_isolation",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "bench", "bar_pad"]},
        "biomechanics": {"joint_stress": ["pelvic_pressure"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"glutes": "B_Tier"}
        }
    },
    "glute_bridge": {
        "exercise_id": "EX_122",
        "exercise_name": "Glute Bridge",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["glutes"],
            "secondary_muscles": ["lower_back"],
            "movement_pattern": "glute_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["mat"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["lower_back_activation"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "peak_recomposition"],
            "hypertrophy_tiers": {"glutes": "B_Tier"}
        }
    },
    "cable_hip_abduction": {
        "exercise_id": "EX_123",
        "exercise_name": "Cable Hip Abduction",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["glutes"],
            "secondary_muscles": [],
            "movement_pattern": "glute_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "ankle_strap"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"glutes": "B_Tier"}
        }
    },
    "curtsy_lunge": {
        "exercise_id": "EX_124",
        "exercise_name": "Curtsy Lunge",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["glutes", "quads"],
            "secondary_muscles": ["adductors"],
            "movement_pattern": "unilateral_leg",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells"]},
        "biomechanics": {"joint_stress": ["lateral_knee_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "peak_metabolic"],
            "hypertrophy_tiers": {"glutes": "B_Tier"}
        }
    },
    "conventional_deadlift": {
        "exercise_id": "EX_125",
        "exercise_name": "Conventional Deadlift",
        "youtube_id": "wYREQkVtvEc",
        "muscle_data": {
            "primary_targets": ["glutes", "hamstrings", "lower_back"],
            "secondary_muscles": ["lats", "core", "forearms"],
            "movement_pattern": "hinge_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "weight_plates"]},
        "biomechanics": {"joint_stress": ["spinal_compression", "lumbar_shear"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "strength_block"],
            "hypertrophy_tiers": {"glutes": "B_Tier"}
        }
    },
    "sumo_deadlift": {
        "exercise_id": "EX_126",
        "exercise_name": "Sumo Deadlift",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["glutes", "quads", "adductors"],
            "secondary_muscles": ["lower_back", "core"],
            "movement_pattern": "hinge_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "weight_plates"]},
        "biomechanics": {"joint_stress": ["hip_mobility_strain", "lumbar_shear"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "strength_block"],
            "hypertrophy_tiers": {"glutes": "B_Tier"}
        }
    },
    "cable_pull_through": {
        "exercise_id": "EX_127",
        "exercise_name": "Cable Pull-Through",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["glutes", "hamstrings"],
            "secondary_muscles": ["lower_back"],
            "movement_pattern": "hinge_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "rope_attachment"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"glutes": "B_Tier"}
        }
    },
    "lunge": {
        "exercise_id": "EX_128",
        "exercise_name": "Stationary Lunge",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["quads", "glutes"],
            "secondary_muscles": ["core"],
            "movement_pattern": "unilateral_leg",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells"]},
        "biomechanics": {"joint_stress": ["knee_torque"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn"],
            "hypertrophy_tiers": {"quads": "B_Tier"}
        }
    },
    "goblet_squat": {
        "exercise_id": "EX_129",
        "exercise_name": "Goblet Squat",
        "youtube_id": "M_XieR6VvSg",
        "muscle_data": {
            "primary_targets": ["quads"],
            "secondary_muscles": ["core", "glutes"],
            "movement_pattern": "squat_pattern",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["squat_mechanics_training"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "peak_recomposition"],
            "hypertrophy_tiers": {"quads": "B_Tier"}
        }
    },
    "sissy_squat": {
        "exercise_id": "EX_130",
        "exercise_name": "Sissy Squat",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["quads"],
            "secondary_muscles": ["core"],
            "movement_pattern": "quad_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["sissy_squat_bench"]},
        "biomechanics": {"extreme_knee_torque": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"quads": "B_Tier"}
        }
    },

    # ==========================================
    # CHEST
    # ==========================================
    "machine_chest_press": {
        "exercise_id": "EX_201",
        "exercise_name": "Machine Chest Press",
        "youtube_id": "xUm0BiZCWlQ",
        "muscle_data": {
            "primary_targets": ["chest"],
            "secondary_muscles": ["front_delts", "triceps"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["chest_press_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"chest": "S_Plus"}
        }
    },
    "seated_cable_pec_fly": {
        "exercise_id": "EX_202",
        "exercise_name": "Seated Cable Pec Fly",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["chest"],
            "secondary_muscles": [],
            "movement_pattern": "chest_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "bench"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"chest": "S_Tier"}
        }
    },
    "flat_bench_press": {
        "exercise_id": "EX_203",
        "exercise_name": "Flat Bench Press",
        "youtube_id": "vcBig73ojpE",
        "muscle_data": {
            "primary_targets": ["chest"],
            "secondary_muscles": ["front_delts", "triceps"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "bench", "weight_plates"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "strength_block", "hypertrophy_volume"],
            "hypertrophy_tiers": {"chest": "A_Tier"}
        }
    },
    "incline_bench_press": {
        "exercise_id": "EX_204",
        "exercise_name": "Incline Bench Press",
        "youtube_id": "SrqOu55lrOU",
        "muscle_data": {
            "primary_targets": ["upper_chest", "front_delts"],
            "secondary_muscles": ["triceps"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "incline_bench", "weight_plates"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "strength_block", "hypertrophy_volume"],
            "hypertrophy_tiers": {"chest": "A_Tier", "front_delts": "A_Tier"}
        }
    },
    "flat_db_press": {
        "exercise_id": "EX_205",
        "exercise_name": "Flat Dumbbell Press",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["chest"],
            "secondary_muscles": ["front_delts", "triceps"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"chest": "A_Tier"}
        }
    },
    "incline_db_press": {
        "exercise_id": "EX_206",
        "exercise_name": "Incline Dumbbell Press",
        "youtube_id": "8iPEnn-ltC8",
        "muscle_data": {
            "primary_targets": ["upper_chest", "front_delts"],
            "secondary_muscles": ["triceps"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "incline_bench"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"chest": "A_Tier", "front_delts": "A_Tier"}
        }
    },
    "dips": {
        "exercise_id": "EX_207",
        "exercise_name": "Chest Dips (Leaning Forward)",
        "youtube_id": "2z8JmcrW-As",
        "muscle_data": {
            "primary_targets": ["chest", "lower_chest"],
            "secondary_muscles": ["triceps", "front_delts"],
            "movement_pattern": "vertical_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["dip_station"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior", "sternum_pressure"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"chest": "A_Tier"}
        }
    },
    "smith_machine_press_flat_incline": {
        "exercise_id": "EX_208",
        "exercise_name": "Smith Machine Press (Flat & Incline)",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["chest"],
            "secondary_muscles": ["front_delts", "triceps"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["smith_machine", "bench"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"chest": "A_Tier"}
        }
    },
    "cable_crossover": {
        "exercise_id": "EX_209",
        "exercise_name": "Cable Crossover",
        "youtube_id": "taI4XduLpTk",
        "muscle_data": {
            "primary_targets": ["chest"],
            "secondary_muscles": [],
            "movement_pattern": "chest_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior_stretch"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"chest": "A_Tier"}
        }
    },
    "pec_deck_machine": {
        "exercise_id": "EX_210",
        "exercise_name": "Pec Deck Machine",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["chest"],
            "secondary_muscles": [],
            "movement_pattern": "chest_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["pec_deck_machine"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior_stretch"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"chest": "A_Tier"}
        }
    },
    "db_fly": {
        "exercise_id": "EX_211",
        "exercise_name": "Dumbbell Fly",
        "youtube_id": "eozdVDA78K0",
        "muscle_data": {
            "primary_targets": ["chest"],
            "secondary_muscles": [],
            "movement_pattern": "chest_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior_stretch", "bicep_tendon_stretch"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"chest": "A_Tier"}
        }
    },
    "deficit_push_up": {
        "exercise_id": "EX_212",
        "exercise_name": "Deficit Push-Up",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["chest"],
            "secondary_muscles": ["triceps", "front_delts"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["push_up_handles_or_plates"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior_stretch"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "peak_metabolic"],
            "hypertrophy_tiers": {"chest": "A_Tier"}
        }
    },
    "cable_press_around": {
        "exercise_id": "EX_213",
        "exercise_name": "Cable Press Around",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["chest"],
            "secondary_muscles": [],
            "movement_pattern": "chest_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"chest": "A_Tier"}
        }
    },
    "guillotine_press_db": {
        "exercise_id": "EX_214",
        "exercise_name": "Guillotine Press (Dumbbell Version)",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["upper_chest"],
            "secondary_muscles": ["front_delts"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": ["shoulder_impingement"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"chest": "A_Tier"}
        }
    },
    "decline_bench_press": {
        "exercise_id": "EX_215",
        "exercise_name": "Decline Bench Press (Barbell & Dumbbell)",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["lower_chest"],
            "secondary_muscles": ["triceps"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "decline_bench"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"chest": "B_Tier"}
        }
    },
    "banded_push_up": {
        "exercise_id": "EX_216",
        "exercise_name": "Banded Push-Up",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["chest"],
            "secondary_muscles": ["triceps", "core"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["resistance_bands"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition"],
            "hypertrophy_tiers": {"chest": "B_Tier"}
        }
    },

    # ==========================================
    # TRICEPS
    # ==========================================
    "overhead_cable_triceps_extension": {
        "exercise_id": "EX_217",
        "exercise_name": "Overhead Cable Triceps Extension",
        "youtube_id": "1u18yJFLhQ4",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": [],
            "movement_pattern": "tricep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine"]},
        "biomechanics": {"joint_stress": ["elbow_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"triceps": "S_Tier"}
        }
    },
    "skull_crusher": {
        "exercise_id": "EX_218",
        "exercise_name": "Skull Crusher",
        "youtube_id": "d_KZxkY_0cM",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": [],
            "movement_pattern": "tricep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["ez_bar", "bench"]},
        "biomechanics": {"joint_stress": ["elbow_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"triceps": "S_Tier"}
        }
    },
    "bar_press_down": {
        "exercise_id": "EX_219",
        "exercise_name": "Bar Press Down",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": [],
            "movement_pattern": "tricep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "straight_bar"]},
        "biomechanics": {"joint_stress": ["wrist_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"triceps": "A_Tier"}
        }
    },
    "one_arm_db_triceps_extension": {
        "exercise_id": "EX_220",
        "exercise_name": "One-Arm Dumbbell Triceps Extension",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": [],
            "movement_pattern": "tricep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells"]},
        "biomechanics": {"joint_stress": ["elbow_strain", "shoulder_mobility_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"triceps": "A_Tier"}
        }
    },
    "katana_triceps_extension": {
        "exercise_id": "EX_221",
        "exercise_name": "Katana Triceps Extension",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": [],
            "movement_pattern": "tricep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "bench"]},
        "biomechanics": {"joint_stress": ["elbow_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"triceps": "A_Tier"}
        }
    },
    "overhead_cable_extension_rope": {
        "exercise_id": "EX_222",
        "exercise_name": "Overhead Cable Extension (Rope)",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": [],
            "movement_pattern": "tricep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "rope_attachment"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"triceps": "A_Tier"}
        }
    },
    "close_grip_bench_press": {
        "exercise_id": "EX_223",
        "exercise_name": "Close Grip Bench Press",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": ["chest", "front_delts"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "bench", "weight_plates"]},
        "biomechanics": {"joint_stress": ["wrist_strain", "shoulder_anterior"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "strength_block", "hypertrophy_volume"],
            "hypertrophy_tiers": {"triceps": "A_Tier"}
        }
    },
    "cable_triceps_kickback": {
        "exercise_id": "EX_224",
        "exercise_name": "Cable Triceps Kickback",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": [],
            "movement_pattern": "tricep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"triceps": "A_Tier"}
        }
    },
    "smith_machine_jm_press": {
        "exercise_id": "EX_225",
        "exercise_name": "Smith Machine JM Press",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": ["chest"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["smith_machine", "bench"]},
        "biomechanics": {"joint_stress": ["elbow_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"triceps": "A_Tier"}
        }
    },
    "db_skull_crusher": {
        "exercise_id": "EX_226",
        "exercise_name": "Dumbbell Skull Crusher",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": [],
            "movement_pattern": "tricep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": ["elbow_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"triceps": "A_Tier"}
        }
    },
    "rope_press_down": {
        "exercise_id": "EX_227",
        "exercise_name": "Rope Press Down",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": [],
            "movement_pattern": "tricep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "rope_attachment"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"triceps": "B_Tier"}
        }
    },
    "db_french_press": {
        "exercise_id": "EX_228",
        "exercise_name": "Dumbbell French Press",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": [],
            "movement_pattern": "tricep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": ["elbow_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"triceps": "B_Tier"}
        }
    },
    "jm_press_barbell": {
        "exercise_id": "EX_229",
        "exercise_name": "JM Press (Barbell)",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": ["chest"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "bench", "weight_plates"]},
        "biomechanics": {"joint_stress": ["severe_elbow_strain", "wrist_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"triceps": "B_Tier"}
        }
    },
    "close_grip_dip": {
        "exercise_id": "EX_230",
        "exercise_name": "Close Grip Dip (Upright Torso)",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": ["chest", "front_delts"],
            "movement_pattern": "vertical_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["dip_station"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior", "sternum_pressure"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"triceps": "B_Tier"}
        }
    },
    "diamond_push_up": {
        "exercise_id": "EX_231",
        "exercise_name": "Diamond Push-Up",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["triceps"],
            "secondary_muscles": ["chest", "core"],
            "movement_pattern": "horizontal_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": []},
        "biomechanics": {"joint_stress": ["wrist_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "peak_metabolic"],
            "hypertrophy_tiers": {"triceps": "B_Tier"}
        }
    },
    "machine_dip": {
        "exercise_id": "EX_232",
        "exercise_name": "Machine Dip",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["triceps", "chest"],
            "secondary_muscles": ["front_delts"],
            "movement_pattern": "vertical_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["dip_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"triceps": "B_Tier"}
        }
    },

    # ==========================================
    # BACK
    # ==========================================
    "chest_supported_row": {
        "exercise_id": "EX_301",
        "exercise_name": "Chest Supported Row",
        "youtube_id": "0BmV4cbH52Q",
        "muscle_data": {
            "primary_targets": ["back", "rear_delts"],
            "secondary_muscles": ["biceps", "traps"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["dumbbells", "incline_bench"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["posture_correction"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"back": "S_Plus"}
        }
    },
    "wide_grip_lat_pull_down": {
        "exercise_id": "EX_302",
        "exercise_name": "Wide Grip Lat Pull Down",
        "youtube_id": "CAwf7n6Luuc",
        "muscle_data": {
            "primary_targets": ["lats"],
            "secondary_muscles": ["biceps", "rear_delts"],
            "movement_pattern": "vertical_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["lat_pulldown_machine", "wide_bar"]},
        "biomechanics": {"joint_stress": ["shoulder_impingement_if_behind_neck"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"back": "S_Tier"}
        }
    },
    "neutral_grip_pull_down": {
        "exercise_id": "EX_303",
        "exercise_name": "Neutral Grip Pull Down",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["lats", "biceps"],
            "secondary_muscles": ["rhomboids"],
            "movement_pattern": "vertical_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["lat_pulldown_machine", "v_bar_or_neutral_attachment"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"back": "S_Tier"}
        }
    },
    "half_kneeling_one_arm_lat_pull_down": {
        "exercise_id": "EX_304",
        "exercise_name": "Half Kneeling One Arm Lat Pull Down",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["lats"],
            "secondary_muscles": ["core", "biceps"],
            "movement_pattern": "vertical_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "d_handle"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["core_stability"]},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"back": "S_Tier"}
        }
    },
    "meadows_row": {
        "exercise_id": "EX_305",
        "exercise_name": "Meadows Row",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["upper_back", "lats"],
            "secondary_muscles": ["biceps", "rear_delts", "grip"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "landmine_attachment"]},
        "biomechanics": {"joint_stress": ["lumbar_shear_if_unsupported"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"back": "S_Tier"}
        }
    },
    "cable_row": {
        "exercise_id": "EX_306",
        "exercise_name": "Cable Row (Close & Wide Grip)",
        "youtube_id": "UCXxvVItLoM",
        "muscle_data": {
            "primary_targets": ["back", "rhomboids"],
            "secondary_muscles": ["biceps", "rear_delts"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_row_machine"]},
        "biomechanics": {"joint_stress": ["lumbar_flexion_if_rounded"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"back": "S_Tier"}
        }
    },
    "wide_grip_pull_up": {
        "exercise_id": "EX_307",
        "exercise_name": "Wide Grip Pull-Up",
        "youtube_id": "eGo4IYb0OqQ",
        "muscle_data": {
            "primary_targets": ["lats"],
            "secondary_muscles": ["biceps", "core"],
            "movement_pattern": "vertical_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["pull_up_bar"]},
        "biomechanics": {"joint_stress": ["shoulder_impingement_if_poor_mobility"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "strength_block", "hypertrophy_volume"],
            "hypertrophy_tiers": {"back": "A_Tier"}
        }
    },
    "neutral_grip_pull_up": {
        "exercise_id": "EX_308",
        "exercise_name": "Neutral Grip Pull-Up",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["lats", "biceps"],
            "secondary_muscles": ["core", "brachialis"],
            "movement_pattern": "vertical_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["pull_up_bar_with_neutral_grips"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume", "peak_metabolic"],
            "hypertrophy_tiers": {"back": "A_Tier"}
        }
    },
    "cross_body_lat_pull_around": {
        "exercise_id": "EX_309",
        "exercise_name": "Cross Body Lat Pull Around",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["lats"],
            "secondary_muscles": [],
            "movement_pattern": "vertical_pull",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "d_handle"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"back": "A_Tier"}
        }
    },
    "deficit_pendlay_row": {
        "exercise_id": "EX_310",
        "exercise_name": "Deficit Penlay Row",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["back", "rhomboids"],
            "secondary_muscles": ["lower_back", "hamstrings"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "weight_plates", "step_platform"]},
        "biomechanics": {"joint_stress": ["lumbar_shear"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "strength_block"],
            "hypertrophy_tiers": {"back": "A_Tier"}
        }
    },
    "one_arm_db_row": {
        "exercise_id": "EX_311",
        "exercise_name": "One Arm Dumbbell Row",
        "youtube_id": "pYcpY20QaE8",
        "muscle_data": {
            "primary_targets": ["lats", "upper_back"],
            "secondary_muscles": ["biceps", "core"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": ["lumbar_torsion_if_twisted"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"back": "A_Tier"}
        }
    },
    "croc_row": {
        "exercise_id": "EX_312",
        "exercise_name": "Croc Row",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["upper_back", "grip"],
            "secondary_muscles": ["lats", "biceps", "core"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["heavy_dumbbells", "bench_or_rack_for_support"]},
        "biomechanics": {"joint_stress": ["lumbar_shear", "shoulder_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["strength_block", "hypertrophy_volume"],
            "hypertrophy_tiers": {"back": "A_Tier"}
        }
    },
    "lying_or_seated_face_pull": {
        "exercise_id": "EX_313",
        "exercise_name": "Lying or Seated Face Pull",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["rear_delts", "traps"],
            "secondary_muscles": ["rhomboids"],
            "movement_pattern": "rear_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "bench", "rope_attachment"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["shoulder_posture", "rotator_cuff_health"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"back": "A_Tier"}
        }
    },
    "lat_prayer": {
        "exercise_id": "EX_314",
        "exercise_name": "Lat Prayer (Cable Lat Pullover)",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["lats"],
            "secondary_muscles": ["triceps_long_head"],
            "movement_pattern": "vertical_pull",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "straight_bar_or_rope"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"back": "A_Tier"}
        }
    },
    "db_lat_pullover": {
        "exercise_id": "EX_315",
        "exercise_name": "Dumbbell Lat Pullover",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["lats", "chest"],
            "secondary_muscles": ["triceps", "serratus"],
            "movement_pattern": "vertical_pull",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior_stretch"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"back": "A_Tier"}
        }
    },
    "chin_ups": {
        "exercise_id": "EX_316",
        "exercise_name": "Chin-Ups",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["lats", "biceps"],
            "secondary_muscles": ["core"],
            "movement_pattern": "vertical_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["pull_up_bar"]},
        "biomechanics": {"joint_stress": ["elbow_strain", "wrist_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "strength_block", "peak_metabolic"],
            "hypertrophy_tiers": {"back": "B_Tier", "biceps": "B_Tier"}
        }
    },
    "standard_barbell_row": {
        "exercise_id": "EX_317",
        "exercise_name": "Standard Barbell Row",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["back", "rhomboids"],
            "secondary_muscles": ["lower_back", "biceps", "hamstrings"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "weight_plates"]},
        "biomechanics": {"joint_stress": ["lumbar_shear"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "strength_block"],
            "hypertrophy_tiers": {"back": "B_Tier"}
        }
    },
    "pendlay_row": {
        "exercise_id": "EX_318",
        "exercise_name": "Penlay Row",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["back", "rhomboids"],
            "secondary_muscles": ["lower_back", "core"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "weight_plates"]},
        "biomechanics": {"joint_stress": ["lumbar_shear"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "strength_block"],
            "hypertrophy_tiers": {"back": "B_Tier"}
        }
    },
    "freestanding_t_bar_row": {
        "exercise_id": "EX_319",
        "exercise_name": "Freestanding T-Bar Row",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["back"],
            "secondary_muscles": ["lower_back", "biceps"],
            "movement_pattern": "horizontal_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "v_bar_handle"]},
        "biomechanics": {"joint_stress": ["lumbar_shear"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "strength_block"],
            "hypertrophy_tiers": {"back": "B_Tier"}
        }
    },
    "standing_rope_face_pull": {
        "exercise_id": "EX_320",
        "exercise_name": "Standing Rope Face Pull",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["rear_delts", "traps"],
            "secondary_muscles": ["rhomboids"],
            "movement_pattern": "rear_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "rope_attachment"]},
        "biomechanics": {"joint_stress": ["lumbar_shear_if_heavy"], "pre_hab_for": ["posture_correction"]},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition"],
            "hypertrophy_tiers": {"back": "B_Tier"}
        }
    },

    # ==========================================
    # BICEPS
    # ==========================================
    "face_away_bayesian_cable_curl": {
        "exercise_id": "EX_321",
        "exercise_name": "Face-Away Bayesian Cable Curl",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["biceps"],
            "secondary_muscles": [],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "d_handle"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior_stretch"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"biceps": "S_Tier"}
        }
    },
    "45_degree_preacher_curl": {
        "exercise_id": "EX_322",
        "exercise_name": "45° Preacher Curl",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["biceps"],
            "secondary_muscles": [],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["preacher_bench", "ez_bar"]},
        "biomechanics": {"joint_stress": ["elbow_tendon_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"biceps": "S_Tier"}
        }
    },
    "machine_preacher_curl": {
        "exercise_id": "EX_323",
        "exercise_name": "Machine Preacher Curl",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["biceps"],
            "secondary_muscles": [],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["bicep_curl_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"biceps": "S_Tier"}
        }
    },
    "hammer_grip_preacher_curl": {
        "exercise_id": "EX_324",
        "exercise_name": "Hammer Grip Preacher Curl",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["brachialis", "biceps"],
            "secondary_muscles": ["forearms"],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["preacher_bench", "dumbbells"]},
        "biomechanics": {"joint_stress": ["elbow_tendon_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"biceps": "S_Tier"}
        }
    },
    "ez_bar_curl": {
        "exercise_id": "EX_325",
        "exercise_name": "EZ Bar Curl",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["biceps"],
            "secondary_muscles": ["forearms"],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["ez_bar", "weight_plates"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"biceps": "A_Tier"}
        }
    },
    "dumbbell_hammer_curl": {
        "exercise_id": "EX_326",
        "exercise_name": "Dumbbell Hammer Curl",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["brachialis", "biceps"],
            "secondary_muscles": ["forearms"],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["elbow_health"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"biceps": "A_Tier"}
        }
    },
    "incline_dumbbell_curl": {
        "exercise_id": "EX_327",
        "exercise_name": "Incline Dumbbell Curl",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["biceps_long_head"],
            "secondary_muscles": [],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "incline_bench"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior_stretch"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"biceps": "A_Tier"}
        }
    },
    "standing_dumbbell_curl": {
        "exercise_id": "EX_328",
        "exercise_name": "Standing Dumbbell Curl",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["biceps"],
            "secondary_muscles": ["forearms"],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"biceps": "A_Tier"}
        }
    },
    "lying_dumbbell_curl": {
        "exercise_id": "EX_329",
        "exercise_name": "Lying Dumbbell Curl",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["biceps"],
            "secondary_muscles": [],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"biceps": "A_Tier"}
        }
    },
    "cable_curl": {
        "exercise_id": "EX_330",
        "exercise_name": "Cable Curl",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["biceps"],
            "secondary_muscles": [],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "straight_bar_or_rope"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"biceps": "A_Tier"}
        }
    },
    "inverse_zottman_curl": {
        "exercise_id": "EX_331",
        "exercise_name": "Inverse Zottman Curl",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["biceps", "brachioradialis"],
            "secondary_muscles": ["forearms"],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells"]},
        "biomechanics": {"joint_stress": ["wrist_strain_if_heavy"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"biceps": "A_Tier"}
        }
    },
    "strict_curl": {
        "exercise_id": "EX_332",
        "exercise_name": "Strict Curl",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["biceps"],
            "secondary_muscles": [],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "wall_for_support"]},
        "biomechanics": {"joint_stress": ["elbow_tendon_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "strength_block"],
            "hypertrophy_tiers": {"biceps": "A_Tier"}
        }
    },
    "modified_21s": {
        "exercise_id": "EX_333",
        "exercise_name": "Modified 21s",
        "youtube_id": "REPLACE_ME",
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
        "youtube_id": "REPLACE_ME",
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
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["biceps"],
            "secondary_muscles": ["forearms"],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "weight_plates"]},
        "biomechanics": {"joint_stress": ["wrist_strain", "elbow_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "strength_block"],
            "hypertrophy_tiers": {"biceps": "B_Tier"}
        }
    },
    "flat_bench_curl": {
        "exercise_id": "EX_336",
        "exercise_name": "Flat Bench Curl",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["biceps"],
            "secondary_muscles": [],
            "movement_pattern": "bicep_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior_stretch"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"biceps": "B_Tier"}
        }
    },

    # ==========================================
    # SHOULDERS
    # ==========================================
    "cable_lateral_raise": {
        "exercise_id": "EX_401",
        "exercise_name": "Cable Lateral Raise",
        "youtube_id": "PPrzBWZDOhA",
        "muscle_data": {
            "primary_targets": ["side_delts"],
            "secondary_muscles": ["front_delts"],
            "movement_pattern": "side_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "d_handle"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"shoulders": "S_Tier"}
        }
    },
    "reverse_cable_crossover": {
        "exercise_id": "EX_402",
        "exercise_name": "Reverse Cable Crossover",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["rear_delts"],
            "secondary_muscles": ["rhomboids", "traps"],
            "movement_pattern": "rear_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["posture_correction"]},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"shoulders": "S_Tier"}
        }
    },
    "cable_y_raise": {
        "exercise_id": "EX_403",
        "exercise_name": "Cable Y-Raise",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["side_delts", "lower_traps"],
            "secondary_muscles": ["front_delts"],
            "movement_pattern": "side_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine"]},
        "biomechanics": {"joint_stress": ["shoulder_impingement_if_poor_mobility"], "pre_hab_for": ["scapular_stability"]},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"shoulders": "S_Tier"}
        }
    },
    "behind_the_back_cuffed_lateral_raise": {
        "exercise_id": "EX_404",
        "exercise_name": "Behind-the-Back Cuffed Lateral Raise",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["side_delts"],
            "secondary_muscles": [],
            "movement_pattern": "side_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "pro_gym", "specific_tools": ["cable_machine", "cuff_attachment"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"shoulders": "S_Tier"}
        }
    },
    "reverse_pec_deck": {
        "exercise_id": "EX_405",
        "exercise_name": "Reverse Pec Deck (Sideways)",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["rear_delts"],
            "secondary_muscles": ["rhomboids", "traps"],
            "movement_pattern": "rear_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["pec_deck_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"shoulders": "S_Tier"}
        }
    },
    "machine_shoulder_press": {
        "exercise_id": "EX_406",
        "exercise_name": "Machine Shoulder Press",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["front_delts"],
            "secondary_muscles": ["triceps", "upper_chest"],
            "movement_pattern": "vertical_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["shoulder_press_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"shoulders": "A_Tier"}
        }
    },
    "atlantis_standing_machine_lateral_raise": {
        "exercise_id": "EX_407",
        "exercise_name": "Atlantis Standing Machine Lateral Raise",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["side_delts"],
            "secondary_muscles": [],
            "movement_pattern": "side_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "pro_gym", "specific_tools": ["lateral_raise_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"shoulders": "A_Tier"}
        }
    },
    "seated_db_shoulder_press": {
        "exercise_id": "EX_408",
        "exercise_name": "Seated Dumbbell Shoulder Press",
        "youtube_id": "qEwKCR5JCog",
        "muscle_data": {
            "primary_targets": ["front_delts"],
            "secondary_muscles": ["triceps", "upper_chest"],
            "movement_pattern": "vertical_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "bench"]},
        "biomechanics": {"joint_stress": ["shoulder_impingement_if_flared", "lumbar_compression"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "foundation", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"shoulders": "A_Tier"}
        }
    },
    "leaning_in_db_lateral_raise": {
        "exercise_id": "EX_409",
        "exercise_name": "Leaning-In Dumbbell Lateral Raise",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["side_delts"],
            "secondary_muscles": [],
            "movement_pattern": "side_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "pole_or_rack_for_support"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"shoulders": "A_Tier"}
        }
    },
    "arnold_style_side_lying_db_raise": {
        "exercise_id": "EX_410",
        "exercise_name": "Arnold-Style Side Lying Dumbbell Raise",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["side_delts"],
            "secondary_muscles": ["rear_delts"],
            "movement_pattern": "side_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells", "incline_bench"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"shoulders": "A_Tier"}
        }
    },
    "rope_face_pull_shoulders": {
        "exercise_id": "EX_411",
        "exercise_name": "Rope Face Pull",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["rear_delts", "traps"],
            "secondary_muscles": ["rhomboids"],
            "movement_pattern": "rear_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["cable_machine", "rope_attachment"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["shoulder_posture", "rotator_cuff_health"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"shoulders": "A_Tier", "back": "A_Tier"}
        }
    },
    "barbell_overhead_press": {
        "exercise_id": "EX_412",
        "exercise_name": "Barbell Overhead Press",
        "youtube_id": "2yjwXTZAkQ0",
        "muscle_data": {
            "primary_targets": ["front_delts"],
            "secondary_muscles": ["triceps", "core", "upper_chest"],
            "movement_pattern": "vertical_press",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell", "squat_rack", "weight_plates"]},
        "biomechanics": {"joint_stress": ["spinal_compression", "lumbar_shear", "shoulder_impingement"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "recomposition", "strength_block"],
            "hypertrophy_tiers": {"shoulders": "B_Tier"}
        }
    },
    "standing_db_lateral_raise": {
        "exercise_id": "EX_413",
        "exercise_name": "Standing Dumbbell Lateral Raise",
        "youtube_id": "WJm942Nm1KU",
        "muscle_data": {
            "primary_targets": ["side_delts"],
            "secondary_muscles": ["traps"],
            "movement_pattern": "side_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells"]},
        "biomechanics": {"joint_stress": ["shoulder_impingement_if_internally_rotated"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition", "hypertrophy_volume", "peak_metabolic"],
            "hypertrophy_tiers": {"shoulders": "B_Tier"}
        }
    },
    "super_rom_lateral_raise": {
        "exercise_id": "EX_414",
        "exercise_name": "Super ROM Lateral Raise",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["side_delts"],
            "secondary_muscles": ["traps"],
            "movement_pattern": "side_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells"]},
        "biomechanics": {"joint_stress": ["shoulder_impingement_at_top"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"shoulders": "B_Tier"}
        }
    },
    "upright_row": {
        "exercise_id": "EX_415",
        "exercise_name": "Upright Row",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["side_delts", "traps"],
            "secondary_muscles": ["biceps"],
            "movement_pattern": "vertical_pull",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["barbell_or_ez_bar"]},
        "biomechanics": {"joint_stress": ["severe_shoulder_impingement", "wrist_strain"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"shoulders": "B_Tier"}
        }
    },
    "bent_over_reverse_db_fly": {
        "exercise_id": "EX_416",
        "exercise_name": "Bent-Over Reverse Dumbbell Fly",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["rear_delts"],
            "secondary_muscles": ["rhomboids"],
            "movement_pattern": "rear_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["dumbbells"]},
        "biomechanics": {"joint_stress": ["lumbar_shear"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"shoulders": "B_Tier"}
        }
    },
    "seated_machine_lateral_raise": {
        "exercise_id": "EX_417",
        "exercise_name": "Seated Machine Lateral Raise",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["side_delts"],
            "secondary_muscles": [],
            "movement_pattern": "side_delt_isolation",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "basic_gym", "specific_tools": ["lateral_raise_machine"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"shoulders": "B_Tier"}
        }
    },

    # ==========================================
    # CORE
    # ==========================================
    "hollow_body_crunch": {
        "exercise_id": "EX_501",
        "exercise_name": "Hollow Body Crunch",
        "youtube_id": "yRMvUqL_lK4",
        "muscle_data": {
            "primary_targets": ["core"],
            "secondary_muscles": ["hip_flexors"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["mat"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["lumbar_stability"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"core": "S_Tier"}
        }
    },
    "long_lever_plank": {
        "exercise_id": "EX_502",
        "exercise_name": "Long Lever Plank",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["core"],
            "secondary_muscles": ["shoulders", "lats"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["mat"]},
        "biomechanics": {"joint_stress": ["shoulder_anterior_stretch"], "pre_hab_for": ["anti_extension"]},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"core": "A_Tier"}
        }
    },
    "knee_raises": {
        "exercise_id": "EX_503",
        "exercise_name": "Knee Raises",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["core"],
            "secondary_muscles": ["hip_flexors"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["mat"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition"],
            "hypertrophy_tiers": {"core": "A_Tier"}
        }
    },
    "side_plank_raise": {
        "exercise_id": "EX_504",
        "exercise_name": "Side Plank / Side Plank Raise",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["obliques", "core"],
            "secondary_muscles": ["shoulders"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["mat"]},
        "biomechanics": {"joint_stress": ["shoulder_strain_if_weak"], "pre_hab_for": ["lateral_stability"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition", "strength_block"],
            "hypertrophy_tiers": {"core": "A_Tier"}
        }
    },
    "reverse_crunch": {
        "exercise_id": "EX_505",
        "exercise_name": "Reverse Crunch",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["core"],
            "secondary_muscles": ["hip_flexors"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["mat"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["pelvic_control"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"core": "A_Tier"}
        }
    },
    "dead_bug": {
        "exercise_id": "EX_506",
        "exercise_name": "Dead Bug",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["core"],
            "secondary_muscles": ["hip_flexors"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["mat"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["lumbar_stability", "coordination"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition"],
            "hypertrophy_tiers": {"core": "B_Tier"}
        }
    },
    "mountain_climbers": {
        "exercise_id": "EX_507",
        "exercise_name": "Mountain Climbers",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["core"],
            "secondary_muscles": ["shoulders", "cardio_system"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["mat"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "peak_metabolic"],
            "hypertrophy_tiers": {"core": "B_Tier"}
        }
    },
    "basic_plank": {
        "exercise_id": "EX_508",
        "exercise_name": "Basic Plank",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["core"],
            "secondary_muscles": ["shoulders"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["mat"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": ["anti_extension"]},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn"],
            "hypertrophy_tiers": {"core": "B_Tier"}
        }
    },
    "leg_raises": {
        "exercise_id": "EX_509",
        "exercise_name": "Leg Raises",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["core"],
            "secondary_muscles": ["hip_flexors"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["mat"]},
        "biomechanics": {"joint_stress": ["lumbar_shear_if_arched"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"core": "B_Tier"}
        }
    },
    "heel_taps": {
        "exercise_id": "EX_510",
        "exercise_name": "Heel Taps",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["obliques", "core"],
            "secondary_muscles": [],
            "movement_pattern": "core_stabilization",
            "is_compound": False
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["mat"]},
        "biomechanics": {"joint_stress": [], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn"],
            "hypertrophy_tiers": {"core": "B_Tier"}
        }
    },
    "candle_raise": {
        "exercise_id": "EX_511",
        "exercise_name": "Candle Raise",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["core"],
            "secondary_muscles": ["hip_flexors", "lower_back"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["mat"]},
        "biomechanics": {"joint_stress": ["neck_strain_if_unsupported"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume"],
            "hypertrophy_tiers": {"core": "B_Tier"}
        }
    },
    "russian_twist": {
        "exercise_id": "EX_512",
        "exercise_name": "Russian Twist",
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["obliques", "core"],
            "secondary_muscles": ["hip_flexors"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["mat"]},
        "biomechanics": {"joint_stress": ["lumbar_torsion_if_weighted_heavily"], "pre_hab_for": []},
        "periodization_tags": {
            "allowed_phases": ["foundation", "build_and_burn", "recomposition"],
            "hypertrophy_tiers": {"core": "B_Tier"}
        }
    },
    "dragon_flag": {
        "exercise_id": "EX_513",
        "exercise_name": "Dragon Flag",
        "youtube_id": "REPLACE_ME",
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
        "youtube_id": "REPLACE_ME",
        "muscle_data": {
            "primary_targets": ["core"],
            "secondary_muscles": ["lats", "shoulders"],
            "movement_pattern": "core_stabilization",
            "is_compound": True
        },
        "facility_requirements": {"facility_tier": "home", "specific_tools": ["ab_wheel", "mat"]},
        "biomechanics": {"joint_stress": ["lumbar_extension_strain_if_weak"], "pre_hab_for": ["anti_extension"]},
        "periodization_tags": {
            "allowed_phases": ["build_and_burn", "recomposition", "hypertrophy_volume", "strength_block"],
            "hypertrophy_tiers": {"core": "B_Tier"}
        }
    }
}