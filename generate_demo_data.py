"""
Generates realistic Indian poultry datasets and visual mock documents
for the Poultry India Expo 2026 Sprint tablet demo.
"""

import json
import os

os.makedirs("data", exist_ok=True)
os.makedirs("assets", exist_ok=True)

# ---------------------------------------------------------------------------
# 1. BROILER SHED #4 DATASET (Day 1 to 25 with Day 22 Anomaly)
# ---------------------------------------------------------------------------
broiler_days = [
    # Days 1 to 25
    {"day": 1,  "opening_birds": 5000, "mortality": 8, "culls": 0, "closing_birds": 4992, "opening_feed_bags": 50, "feed_bags_received": 0,  "feed_bags_consumed": 2,  "closing_feed_bags": 48, "avg_body_weight_g": 42,   "water_liters": 180,  "notes": "Chicks placed 03-Nov 6am, brooding temp 33C, good vigor."},
    {"day": 2,  "opening_birds": 4992, "mortality": 5, "culls": 0, "closing_birds": 4987, "opening_feed_bags": 48, "feed_bags_received": 0,  "feed_bags_consumed": 3,  "closing_feed_bags": 45, "avg_body_weight_g": 56,   "water_liters": 240,  "notes": "Pre-starter crumble, active feeding."},
    {"day": 3,  "opening_birds": 4987, "mortality": 4, "culls": 1, "closing_birds": 4982, "opening_feed_bags": 45, "feed_bags_received": 0,  "feed_bags_consumed": 3,  "closing_feed_bags": 42, "avg_body_weight_g": 74,   "water_liters": 310,  "notes": "Normal brooding."},
    {"day": 4,  "opening_birds": 4982, "mortality": 3, "culls": 0, "closing_birds": 4979, "opening_feed_bags": 42, "feed_bags_received": 0,  "feed_bags_consumed": 4,  "closing_feed_bags": 38, "avg_body_weight_g": 95,   "water_liters": 380,  "notes": "Crop check 98% full."},
    {"day": 5,  "opening_birds": 4979, "mortality": 3, "culls": 0, "closing_birds": 4976, "opening_feed_bags": 38, "feed_bags_received": 0,  "feed_bags_consumed": 5,  "closing_feed_bags": 33, "avg_body_weight_g": 122,  "water_liters": 450,  "notes": "B complex in water."},
    {"day": 6,  "opening_birds": 4976, "mortality": 2, "culls": 1, "closing_birds": 4973, "opening_feed_bags": 33, "feed_bags_received": 0,  "feed_bags_consumed": 5,  "closing_feed_bags": 28, "avg_body_weight_g": 155,  "water_liters": 520,  "notes": "Ventilation adjustment."},
    {"day": 7,  "opening_birds": 4973, "mortality": 3, "culls": 0, "closing_birds": 4970, "opening_feed_bags": 28, "feed_bags_received": 60, "feed_bags_consumed": 6,  "closing_feed_bags": 82, "avg_body_weight_g": 195,  "water_liters": 610,  "notes": "Day 7 sample weighment. Target 195g met."},
    {"day": 8,  "opening_birds": 4970, "mortality": 2, "culls": 0, "closing_birds": 4968, "opening_feed_bags": 82, "feed_bags_received": 0,  "feed_bags_consumed": 7,  "closing_feed_bags": 75, "avg_body_weight_g": 235,  "water_liters": 710,  "notes": "Switched to starter crumb."},
    {"day": 9,  "opening_birds": 4968, "mortality": 2, "culls": 0, "closing_birds": 4966, "opening_feed_bags": 75, "feed_bags_received": 0,  "feed_bags_consumed": 8,  "closing_feed_bags": 67, "avg_body_weight_g": 278,  "water_liters": 820,  "notes": "IBD Gumboro vaccination eye-drop."},
    {"day": 10, "opening_birds": 4966, "mortality": 3, "culls": 1, "closing_birds": 4962, "opening_feed_bags": 67, "feed_bags_received": 0,  "feed_bags_consumed": 9,  "closing_feed_bags": 58, "avg_body_weight_g": 325,  "water_liters": 940,  "notes": "Post vacc stress care."},
    {"day": 11, "opening_birds": 4962, "mortality": 2, "culls": 0, "closing_birds": 4960, "opening_feed_bags": 58, "feed_bags_received": 0,  "feed_bags_consumed": 10, "closing_feed_bags": 48, "avg_body_weight_g": 372,  "water_liters": 1020, "notes": "Tunnel fans stage 2 running."},
    {"day": 12, "opening_birds": 4960, "mortality": 3, "culls": 0, "closing_birds": 4957, "opening_feed_bags": 48, "feed_bags_received": 0,  "feed_bags_consumed": 11, "closing_feed_bags": 37, "avg_body_weight_g": 420,  "water_liters": 1100, "notes": "Litter dry and friable."},
    {"day": 13, "opening_birds": 4957, "mortality": 2, "culls": 0, "closing_birds": 4955, "opening_feed_bags": 37, "feed_bags_received": 0,  "feed_bags_consumed": 12, "closing_feed_bags": 25, "avg_body_weight_g": 455,  "water_liters": 1180, "notes": "Feeder line height raised."},
    {"day": 14, "opening_birds": 4955, "mortality": 3, "culls": 1, "closing_birds": 4951, "opening_feed_bags": 25, "feed_bags_received": 70, "feed_bags_consumed": 13, "closing_feed_bags": 82, "avg_body_weight_g": 490,  "water_liters": 1260, "notes": "Day 14 test weight 490g (benchmark 485g)."},
    {"day": 15, "opening_birds": 4951, "mortality": 2, "culls": 0, "closing_birds": 4949, "opening_feed_bags": 82, "feed_bags_received": 0,  "feed_bags_consumed": 14, "closing_feed_bags": 68, "avg_body_weight_g": 545,  "water_liters": 1340, "notes": "Good uniformity 86%."},
    {"day": 16, "opening_birds": 4949, "mortality": 3, "culls": 0, "closing_birds": 4946, "opening_feed_bags": 68, "feed_bags_received": 0,  "feed_bags_consumed": 15, "closing_feed_bags": 53, "avg_body_weight_g": 610,  "water_liters": 1420, "notes": "ND Lasota booster drinking water."},
    {"day": 17, "opening_birds": 4946, "mortality": 2, "culls": 0, "closing_birds": 4944, "opening_feed_bags": 53, "feed_bags_received": 0,  "feed_bags_consumed": 16, "closing_feed_bags": 37, "avg_body_weight_g": 680,  "water_liters": 1500, "notes": "Starter to finisher transition."},
    {"day": 18, "opening_birds": 4944, "mortality": 3, "culls": 1, "closing_birds": 4940, "opening_feed_bags": 37, "feed_bags_received": 0,  "feed_bags_consumed": 17, "closing_feed_bags": 20, "avg_body_weight_g": 760,  "water_liters": 1560, "notes": "Static pressure 28 Pa."},
    {"day": 19, "opening_birds": 4940, "mortality": 2, "culls": 0, "closing_birds": 4938, "opening_feed_bags": 20, "feed_bags_received": 50, "feed_bags_consumed": 18, "closing_feed_bags": 52, "avg_body_weight_g": 840,  "water_liters": 1620, "notes": "Finisher pellet delivery 50 bags."},
    {"day": 20, "opening_birds": 4938, "mortality": 3, "culls": 1, "closing_birds": 4934, "opening_feed_bags": 52, "feed_bags_received": 0,  "feed_bags_consumed": 18, "closing_feed_bags": 34, "avg_body_weight_g": 915,  "water_liters": 1680, "notes": "Routine supervisor inspection."},
    {"day": 21, "opening_birds": 4934, "mortality": 4, "culls": 1, "closing_birds": 4929, "opening_feed_bags": 34, "feed_bags_received": 0,  "feed_bags_consumed": 19, "closing_feed_bags": 15, "avg_body_weight_g": 985,  "water_liters": 1720, "notes": "Day 21 weight 985g, FCR on track 1.39."},
    # --- DAY 22 ANOMALIES (Mortality spike + Missing feed bags + Water surge) ---
    {"day": 22, "opening_birds": 4929, "mortality": 28, "culls": 3, "closing_birds": 4898, "opening_feed_bags": 15, "feed_bags_received": 30, "feed_bags_consumed": 22, "closing_feed_bags": 19, "avg_body_weight_g": 1025, "water_liters": 2850, "notes": "URGENT: Fan #3 tripped at 1:30pm, shed heated up to 37C! 28 dead birds near south cool pad. Physical bag audit found 19 bags on floor vs 23 expected (-4 missing bags)."},
    {"day": 23, "opening_birds": 4898, "mortality": 8, "culls": 1, "closing_birds": 4889, "opening_feed_bags": 19, "feed_bags_received": 0,  "feed_bags_consumed": 20, "closing_feed_bags": 19, "avg_body_weight_g": 1090, "water_liters": 2100, "notes": "Technician replaced fan V-belt. Electrolyte given. Mortality subduing."},
    {"day": 24, "opening_birds": 4889, "mortality": 4, "culls": 0, "closing_birds": 4885, "opening_feed_bags": 19, "feed_bags_received": 40, "feed_bags_consumed": 21, "closing_feed_bags": 38, "avg_body_weight_g": 1175, "water_liters": 1900, "notes": "Recovery ongoing."},
    {"day": 25, "opening_birds": 4885, "mortality": 3, "culls": 0, "closing_birds": 4882, "opening_feed_bags": 38, "feed_bags_received": 0,  "feed_bags_consumed": 22, "closing_feed_bags": 16, "avg_body_weight_g": 1260, "water_liters": 1950, "notes": "Day 25 weight 1260g (Cobb std 1320g - 60g deficit from Day 22 stress)."}
]

broiler_meta = {
    "metadata": {
        "title": "Broiler Shed Register - Batch #4 (Cobb 500)",
        "farm_name": "Sri Balaji Broiler Farm (Contract Farm #142)",
        "integrator": "ABIS Exports / IB Group Hyderabad Division",
        "location": "Choutuppal Mandal, Yadadri Bhuvanagiri, Telangana",
        "farmer_name": "K. Venkat Reddy",
        "supervisor_name": "M. Ramesh (Area Tech Officer)",
        "flock_id": "ABIS-TG-2026-SH4-B4",
        "shed_no": "04 (Environmentally Controlled Tunnel)",
        "chicks_placed": 5000,
        "placement_date": "2026-11-03",
        "current_evaluation_day": 25,
        "hatchery_source": "Venkateshwara Hatcheries (VH), Hyderabad",
        "feed_type": "ABIS High-Energy Broiler Crumb / Pellets (50kg bags)",
        "supervisor_locked": False,
        "supervisor_lock_timestamp": None,
        "supervisor_notes": "Pending resolution of Day 22 mortality spike (28 birds) and 4-bag physical inventory variance."
    },
    "rows": broiler_days
}

with open("data/broiler_shed_4_cobb500.json", "w") as f:
    json.dump(broiler_meta, f, indent=2)

print("Saved data/broiler_shed_4_cobb500.json")

# ---------------------------------------------------------------------------
# 2. FEED MILL COA DATASET (Maize Lot #108 - Aflatoxin Breach)
# ---------------------------------------------------------------------------
feed_coa_data = {
    "metadata": {
        "title": "Certificate of Analysis (COA) - Inward Raw Material",
        "feed_mill": "Prodigy Foods Pvt Ltd / Bentoli Formulation Hub",
        "plant_location": "Cherlapally Industrial Estate, Hyderabad, Telangana",
        "testing_laboratory": "Analytical Testing Services (NABL Accredited TC-8492)",
        "lab_address": "Plot 18/A, IDA Nacharam, Hyderabad 500076",
        "coa_number": "ATS/HYD/2026/COA-MZ-108",
        "sample_received_date": "2026-11-24",
        "testing_completed_date": "2026-11-25",
        "commodity": "yellow_maize",
        "commodity_display": "Yellow Maize (Poultry Feed Grade Corn)",
        "supplier_name": "Sri Lakshmi Agro Traders & Commission Agents",
        "supplier_location": "Nizamabad Agricultural Market Yard (Mandi)",
        "lot_number": "MZ-2026-HYD-108",
        "vehicle_numbers": ["TS-08-UB-4412", "TS-08-UB-4413"],
        "consignment_qty_mt": 42.50,
        "qc_manager": "Dr. S. K. Mukherjee, Chief Nutritionist",
        "qc_status": "LOCKED_BREACH",
        "qc_approved": False,
        "override_reason": ""
    },
    "parameters": {
        "aflatoxin_b1_ppb": 28.4,
        "moisture_pct": 13.8,
        "crude_protein_pct": 8.1,
        "damaged_grain_pct": 2.2,
        "foreign_matter_pct": 1.4,
        "free_fatty_acids_pct": 1.6
    },
    "standard_specifications": {
        "aflatoxin_b1_ppb": {"max": 20.0, "unit": "ppb", "critical": True, "method": "AOAC 991.31 (HPLC / Immunoaffinity)"},
        "moisture_pct": {"max": 12.0, "unit": "%", "critical": True, "method": "IS: 4333 (Part II) 105C Oven"},
        "crude_protein_pct": {"min": 8.5, "unit": "%", "critical": False, "method": "IS: 7874 (Part I) Kjeldahl (N x 6.25)"},
        "damaged_grain_pct": {"max": 4.0, "unit": "%", "critical": False, "method": "Visual Sorting IS: 4333 (Part I)"},
        "foreign_matter_pct": {"max": 1.5, "unit": "%", "critical": False, "method": "IS: 4333 (Part I) Sieve"},
        "free_fatty_acids_pct": {"max": 2.0, "unit": "%", "critical": False, "method": "Titration as Oleic Acid"}
    },
    "commercial_impact": {
        "risk_summary": "CRITICAL TOXICOSIS HAZARD: High Aflatoxin B1 (28.4 ppb) combined with high moisture (13.8%) creates active fungal proliferation risk in bulk silo. Will cause immunosuppression, poor FCR, and liver lesions in broilers if compounded into pre-starter or starter diets.",
        "recommended_action": "REJECT ENTIRE CONSIGNMENT (42.5 MT). Do not allow weighbridge discharge. If diverted to commercial layer feed or older birds, mandatory binder dosage of 2.5 kg/MT hydrated sodium calcium aluminosilicate (HSCAS) + organic acid mold inhibitor required with written GM approval."
    }
}

with open("data/feed_mill_coa_maize_lot108.json", "w") as f:
    json.dump(feed_coa_data, f, indent=2)

print("Saved data/feed_mill_coa_maize_lot108.json")

# ---------------------------------------------------------------------------
# 3. OEM SHED CONTROLLER HOURLY TELEMETRY (Day 22 Hourly Log)
# ---------------------------------------------------------------------------
hourly_telemetry = []
# 24 hours of Day 22
base_temps = [23.5, 23.0, 22.8, 22.5, 23.2, 24.5, 26.2, 28.0, 30.5, 32.8, 34.2, 35.5, 36.5, 37.8, 38.2, 37.0, 35.2, 32.8, 30.2, 28.0, 26.5, 25.4, 24.5, 24.0]
inside_temps = [24.0, 23.8, 23.5, 23.4, 23.8, 24.6, 25.5, 26.5, 27.5, 28.8, 30.2, 32.5, 35.8, 36.8, 36.2, 33.5, 30.8, 28.5, 27.2, 26.0, 25.2, 24.8, 24.5, 24.2]
static_pressures = [26, 26, 25, 25, 26, 27, 28, 28, 28, 28, 29, 27, 12, 11, 14, 26, 27, 27, 26, 26, 25, 25, 25, 25]
fan_stages = [2, 2, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 4, 4, 4, 3, 3, 3, 2, 2, 2, 2]
water_pulses = [15, 12, 10, 8, 15, 35, 60, 85, 110, 140, 180, 230, 340, 380, 320, 240, 180, 140, 110, 85, 60, 40, 25, 20]

for h in range(24):
    alarm = None
    if h == 12:
        alarm = "STATIC_PRESS_WARN: Fan #3 rpm drop"
    elif h == 13:
        alarm = "HIGH_TEMP_ALARM: 35.8C (Belt Slip Fan #3)"
    elif h == 14:
        alarm = "CRITICAL_HEAT_ALARM: 36.8C Inside Temp Peak"
    elif h == 15:
        alarm = "MANUAL_REPAIR: Technician tensioned Fan #3 V-belt"
        
    hourly_telemetry.append({
        "hour": h,
        "time_str": f"{h:02d}:00",
        "outside_temp_c": base_temps[h],
        "inside_temp_c": inside_temps[h],
        "target_temp_c": 24.0,
        "rh_pct": 74 if h in (12, 13, 14) else 65,
        "static_pressure_pa": static_pressures[h],
        "fan_stage": fan_stages[h],
        "water_liters_hour": water_pulses[h],
        "alarm": alarm
    })

oem_controller_data = {
    "device_info": {
        "controller_model": "Dhumal SmartVent EC-800 / Agrologic TC-5",
        "firmware_version": "v4.2.1-HYD",
        "farm_id": "SRI_BALAJI_SHED_04",
        "date": "2026-11-24",
        "flock_day": 22,
        "total_water_liters": sum(water_pulses),
        "peak_inside_temp": max(inside_temps),
        "min_static_pressure": min(static_pressures),
        "fan_failure_duration_min": 115
    },
    "hourly_telemetry": hourly_telemetry
}

with open("data/oem_controller_hourly_day22.json", "w") as f:
    json.dump(oem_controller_data, f, indent=2)

print("Saved data/oem_controller_hourly_day22.json")
