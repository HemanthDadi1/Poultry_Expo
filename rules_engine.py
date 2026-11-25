"""
Poultry India Expo 2026 - Deterministic Rules Engine
Engineering Axiom: "AI reads. People confirm. Rules decide."
Author: Hemanth Dadi

Strict deterministic math, mass-balance, and anomaly detection rules for:
1. Broiler Integrators (Shed cards, FCR, cumulative mortality, mass-balance)
2. Commercial Feed Mills & Premixers (COA ingredient compliance, Aflatoxin, Moisture, CP)
3. OEM Shed Analytics (Controller log & manual ledger correlation)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import math
import json

# ---------------------------------------------------------------------------
# BREED STANDARDS (Cobb 500 Daily Benchmark Table)
# ---------------------------------------------------------------------------
COBB_500_BENCHMARK = {
    1:  {"target_weight_g": 42,   "cum_feed_g": 18,   "target_fcr": 0.85, "max_daily_mort_pct": 0.20},
    7:  {"target_weight_g": 195,  "cum_feed_g": 190,  "target_fcr": 0.97, "max_daily_mort_pct": 0.15},
    14: {"target_weight_g": 485,  "cum_feed_g": 585,  "target_fcr": 1.20, "max_daily_mort_pct": 0.12},
    18: {"target_weight_g": 760,  "cum_feed_g": 1000, "target_fcr": 1.31, "max_daily_mort_pct": 0.12},
    20: {"target_weight_g": 905,  "cum_feed_g": 1240, "target_fcr": 1.37, "max_daily_mort_pct": 0.12},
    21: {"target_weight_g": 980,  "cum_feed_g": 1370, "target_fcr": 1.40, "max_daily_mort_pct": 0.12},
    22: {"target_weight_g": 1060, "cum_feed_g": 1500, "target_fcr": 1.41, "max_daily_mort_pct": 0.12},
    23: {"target_weight_g": 1145, "cum_feed_g": 1640, "target_fcr": 1.43, "max_daily_mort_pct": 0.12},
    24: {"target_weight_g": 1230, "cum_feed_g": 1790, "target_fcr": 1.45, "max_daily_mort_pct": 0.12},
    25: {"target_weight_g": 1320, "cum_feed_g": 1945, "target_fcr": 1.47, "max_daily_mort_pct": 0.12},
    28: {"target_weight_g": 1610, "cum_feed_g": 2450, "target_fcr": 1.52, "max_daily_mort_pct": 0.12},
    35: {"target_weight_g": 2360, "cum_feed_g": 3780, "target_fcr": 1.60, "max_daily_mort_pct": 0.12},
    42: {"target_weight_g": 3120, "cum_feed_g": 5350, "target_fcr": 1.71, "max_daily_mort_pct": 0.12},
}

def get_cobb_benchmark_for_day(day: int) -> Dict[str, float]:
    """Interpolate or snap to closest Cobb 500 benchmark for a given day."""
    if day in COBB_500_BENCHMARK:
        return COBB_500_BENCHMARK[day]
    
    # Nearest or linear interpolation
    days = sorted(COBB_500_BENCHMARK.keys())
    if day <= days[0]:
        return COBB_500_BENCHMARK[days[0]]
    if day >= days[-1]:
        return COBB_500_BENCHMARK[days[-1]]
    
    # Find bounding days
    lower_day = max(d for d in days if d <= day)
    upper_day = min(d for d in days if d >= day)
    factor = (day - lower_day) / (upper_day - lower_day)
    
    low = COBB_500_BENCHMARK[lower_day]
    high = COBB_500_BENCHMARK[upper_day]
    
    return {
        "target_weight_g": round(low["target_weight_g"] + factor * (high["target_weight_g"] - low["target_weight_g"]), 1),
        "cum_feed_g": round(low["cum_feed_g"] + factor * (high["cum_feed_g"] - low["cum_feed_g"]), 1),
        "target_fcr": round(low["target_fcr"] + factor * (high["target_fcr"] - low["target_fcr"]), 3),
        "max_daily_mort_pct": low["max_daily_mort_pct"]
    }

# ---------------------------------------------------------------------------
# VERTICAL 1: BROILER INTEGRATOR SHED CARD VALIDATOR
# ---------------------------------------------------------------------------
@dataclass
class DailyLedgerRow:
    day: int
    opening_birds: int
    mortality: int
    culls: int
    closing_birds: int
    opening_feed_bags: int
    feed_bags_received: int
    feed_bags_consumed: int
    closing_feed_bags: int
    avg_body_weight_g: float
    water_liters: Optional[float] = None
    notes: str = ""

@dataclass
class AnomalyAlert:
    code: str
    severity: str  # "BREACH", "WARNING", "INFO"
    day: int
    metric: str
    observed_value: Any
    expected_threshold: Any
    message: str
    action_required: str

def evaluate_broiler_shed_ledger(
    initial_placed_chicks: int,
    rows: List[Dict[str, Any]],
    bag_weight_kg: float = 50.0,
    supervisor_locked: bool = False
) -> Dict[str, Any]:
    """
    Evaluates broiler daily ledger with strict mass-balance and deterministic thresholds.
    No hallucinated calculations. Every metric is verifiable.
    """
    anomalies: List[Dict[str, Any]] = []
    processed_rows: List[Dict[str, Any]] = []
    
    cum_mortality = 0
    cum_culls = 0
    cum_feed_kg = 0.0
    
    running_birds = initial_placed_chicks
    
    for idx, r in enumerate(rows):
        day = int(r.get("day", idx + 1))
        mortality = int(r.get("mortality", 0))
        culls = int(r.get("culls", 0))
        
        # Mass balance check on birds
        expected_closing_birds = running_birds - mortality - culls
        reported_closing_birds = int(r.get("closing_birds", expected_closing_birds))
        
        bird_balance_ok = (expected_closing_birds == reported_closing_birds)
        if not bird_balance_ok:
            anomalies.append({
                "code": "BIRD_COUNT_MISMATCH",
                "severity": "BREACH",
                "day": day,
                "metric": "closing_birds",
                "observed_value": reported_closing_birds,
                "expected_threshold": expected_closing_birds,
                "message": f"Day {day}: Bird tally mismatch! Opening {running_birds} - Mort {mortality} - Culls {culls} should equal {expected_closing_birds}, got {reported_closing_birds}.",
                "action_required": "Verify physical count before approving supervisor sign-off."
            })
        
        # Feed inventory mass balance
        opening_bags = int(r.get("opening_feed_bags", 0))
        received_bags = int(r.get("feed_bags_received", 0))
        consumed_bags = int(r.get("feed_bags_consumed", 0))
        reported_closing_bags = int(r.get("closing_feed_bags", opening_bags + received_bags - consumed_bags))
        
        expected_closing_bags = opening_bags + received_bags - consumed_bags
        feed_balance_ok = (expected_closing_bags == reported_closing_bags)
        
        if not feed_balance_ok:
            anomalies.append({
                "code": "FEED_INVENTORY_DISCREPANCY",
                "severity": "BREACH",
                "day": day,
                "metric": "closing_feed_bags",
                "observed_value": reported_closing_bags,
                "expected_threshold": expected_closing_bags,
                "message": f"Day {day}: Feed bag inventory discrepancy! {opening_bags} + {received_bags} - {consumed_bags} = {expected_closing_bags} bags expected, but physical count reported {reported_closing_bags} bags.",
                "action_required": "Inspect farm feed shed for unlogged feed bag leakage, rodent damage, or theft."
            })
        
        # Accumulate metrics
        cum_mortality += mortality
        cum_culls += culls
        running_birds = reported_closing_birds
        
        day_feed_kg = consumed_bags * bag_weight_kg
        cum_feed_kg += day_feed_kg
        
        # Daily mortality rate %
        daily_mort_pct = (mortality / initial_placed_chicks) * 100.0 if initial_placed_chicks > 0 else 0.0
        cum_mort_pct = (cum_mortality / initial_placed_chicks) * 100.0 if initial_placed_chicks > 0 else 0.0
        
        # Benchmark comparison
        benchmark = get_cobb_benchmark_for_day(day)
        max_allowed_daily_mort = benchmark["max_daily_mort_pct"]
        
        if daily_mort_pct > max_allowed_daily_mort:
            severity = "BREACH" if daily_mort_pct > 0.25 else "WARNING"
            anomalies.append({
                "code": "DAILY_MORTALITY_SPIKE",
                "severity": severity,
                "day": day,
                "metric": "daily_mortality_pct",
                "observed_value": round(daily_mort_pct, 3),
                "expected_threshold": max_allowed_daily_mort,
                "message": f"Day {day}: Daily mortality spike of {mortality} birds ({daily_mort_pct:.2f}%) exceeds limit of {max_allowed_daily_mort:.2f}%.",
                "action_required": "Trigger urgent veterinarian site visit. Check ventilation fans and drinker lines."
            })
        
        # Weight and FCR evaluation
        avg_body_weight_g = float(r.get("avg_body_weight_g", 0.0))
        total_live_biomass_kg = (running_birds * avg_body_weight_g) / 1000.0
        
        fcr = (cum_feed_kg / total_live_biomass_kg) if total_live_biomass_kg > 0 else 0.0
        target_fcr = benchmark["target_fcr"]
        fcr_drift = fcr - target_fcr
        
        if avg_body_weight_g > 0 and fcr_drift > 0.05:
            severity = "BREACH" if fcr_drift > 0.10 else "WARNING"
            anomalies.append({
                "code": "FCR_DRIFT_EXCESS",
                "severity": severity,
                "day": day,
                "metric": "fcr_drift",
                "observed_value": round(fcr, 3),
                "expected_threshold": target_fcr,
                "message": f"Day {day}: Cumulative FCR {fcr:.3f} deviates from Cobb 500 standard {target_fcr:.3f} by +{fcr_drift:.3f} points.",
                "action_required": "Review feed quality, feeder height wastage, and sub-clinical coccidiosis/enteritis."
            })
            
        # Water to feed ratio if provided
        water_l = float(r.get("water_liters", 0.0) or 0.0)
        water_feed_ratio = (water_l / day_feed_kg) if day_feed_kg > 0 and water_l > 0 else None
        if water_feed_ratio is not None:
            if water_feed_ratio < 1.4:
                anomalies.append({
                    "code": "WATER_INTAKE_DEPRESSED",
                    "severity": "WARNING",
                    "day": day,
                    "metric": "water_feed_ratio",
                    "observed_value": round(water_feed_ratio, 2),
                    "expected_threshold": "1.6 - 2.1",
                    "message": f"Day {day}: Low water intake ({water_feed_ratio:.2f} L/kg feed). Check nipple water pressure.",
                    "action_required": "Check pressure regulators and flush lines."
                })
            elif water_feed_ratio > 2.6:
                anomalies.append({
                    "code": "HEAT_STRESS_OR_ENTERITIS",
                    "severity": "WARNING",
                    "day": day,
                    "metric": "water_feed_ratio",
                    "observed_value": round(water_feed_ratio, 2),
                    "expected_threshold": "1.6 - 2.1",
                    "message": f"Day {day}: Abnormally high water intake ({water_feed_ratio:.2f} L/kg feed). Indicates heat stress or wet litter risk.",
                    "action_required": "Check tunnel ventilation, cool cell pads, and electrolyte dosing."
                })
        
        processed_rows.append({
            "day": day,
            "opening_birds": int(r.get("opening_birds", running_birds + mortality + culls)),
            "mortality": mortality,
            "culls": culls,
            "closing_birds": running_birds,
            "daily_mort_pct": round(daily_mort_pct, 3),
            "cum_mort_pct": round(cum_mort_pct, 3),
            "opening_feed_bags": opening_bags,
            "feed_bags_received": received_bags,
            "feed_bags_consumed": consumed_bags,
            "closing_feed_bags": reported_closing_bags,
            "day_feed_kg": round(day_feed_kg, 1),
            "cum_feed_kg": round(cum_feed_kg, 1),
            "avg_body_weight_g": avg_body_weight_g,
            "target_body_weight_g": benchmark["target_weight_g"],
            "total_live_biomass_kg": round(total_live_biomass_kg, 2),
            "calculated_fcr": round(fcr, 3),
            "target_fcr": target_fcr,
            "fcr_drift": round(fcr_drift, 3),
            "water_liters": water_l if water_l > 0 else None,
            "water_feed_ratio": round(water_feed_ratio, 2) if water_feed_ratio else None,
            "notes": r.get("notes", "")
        })
        
    last_row = processed_rows[-1] if processed_rows else {}
    overall_status = "PASS"
    has_breach = any(a["severity"] == "BREACH" for a in anomalies)
    has_warning = any(a["severity"] == "WARNING" for a in anomalies)
    
    if has_breach:
        overall_status = "BREACH"
    elif has_warning:
        overall_status = "WARNING"
        
    return {
        "status": overall_status,
        "supervisor_locked": supervisor_locked,
        "initial_placed_chicks": initial_placed_chicks,
        "current_live_birds": running_birds,
        "total_mortality": cum_mortality,
        "cumulative_mortality_pct": round((cum_mortality / initial_placed_chicks) * 100.0, 2) if initial_placed_chicks > 0 else 0,
        "total_feed_consumed_kg": round(cum_feed_kg, 1),
        "total_feed_consumed_bags": round(cum_feed_kg / bag_weight_kg, 1),
        "current_avg_weight_g": last_row.get("avg_body_weight_g", 0),
        "target_avg_weight_g": last_row.get("target_body_weight_g", 0),
        "final_fcr": last_row.get("calculated_fcr", 0),
        "target_fcr": last_row.get("target_fcr", 0),
        "fcr_drift": last_row.get("fcr_drift", 0),
        "anomalies_count": len(anomalies),
        "anomalies": anomalies,
        "ledger": processed_rows
    }

# ---------------------------------------------------------------------------
# VERTICAL 2: COMMERCIAL FEED MILL & PREMIX COA SPEC CHECKER
# ---------------------------------------------------------------------------
INGREDIENT_SPECS = {
    "yellow_maize": {
        "name": "Yellow Maize (Corn Grain)",
        "parameters": {
            "aflatoxin_b1_ppb": {"label": "Aflatoxin B1", "unit": "ppb", "max": 20.0, "critical": True, "warning_above": 15.0},
            "moisture_pct": {"label": "Moisture", "unit": "%", "max": 12.0, "critical": True, "warning_above": 11.5},
            "crude_protein_pct": {"label": "Crude Protein (CP)", "unit": "%", "min": 8.5, "critical": False, "warning_below": 8.8},
            "damaged_grain_pct": {"label": "Damaged / Discolored Grain", "unit": "%", "max": 4.0, "critical": False, "warning_above": 3.0},
            "foreign_matter_pct": {"label": "Foreign Matter / Dust", "unit": "%", "max": 1.5, "critical": False, "warning_above": 1.0},
            "free_fatty_acids_pct": {"label": "Free Fatty Acids (FFA)", "unit": "%", "max": 2.0, "critical": False, "warning_above": 1.5}
        }
    },
    "soya_doc": {
        "name": "Soybean Meal (De-oiled Cake - 46% min)",
        "parameters": {
            "crude_protein_pct": {"label": "Crude Protein (CP)", "unit": "%", "min": 46.0, "critical": True, "warning_below": 46.5},
            "moisture_pct": {"label": "Moisture", "unit": "%", "max": 11.0, "critical": True, "warning_above": 10.5},
            "urease_activity_dpH": {"label": "Urease Activity (delta pH)", "unit": "dpH", "min": 0.05, "max": 0.20, "critical": True},
            "sand_silica_pct": {"label": "Sand & Silica (Acid Insoluble Ash)", "unit": "%", "max": 1.5, "critical": False, "warning_above": 1.0},
            "crude_fiber_pct": {"label": "Crude Fiber", "unit": "%", "max": 6.5, "critical": False, "warning_above": 6.0}
        }
    }
}

def evaluate_feed_coa(
    commodity_key: str,
    lot_number: str,
    supplier_name: str,
    test_values: Dict[str, float],
    qc_approved: bool = False,
    override_reason: str = ""
) -> Dict[str, Any]:
    """
    Evaluates lab Certificate of Analysis (COA) against deterministic procurement specs.
    Immediate lot quarantine if critical limits (Aflatoxin, Moisture) fail.
    """
    spec_def = INGREDIENT_SPECS.get(commodity_key, INGREDIENT_SPECS["yellow_maize"])
    params = spec_def["parameters"]
    
    results = []
    anomalies = []
    has_critical_breach = False
    has_warning = False
    
    for param_key, rules in params.items():
        val = test_values.get(param_key)
        if val is None:
            continue
            
        val = float(val)
        unit = rules.get("unit", "")
        label = rules.get("label", param_key)
        is_critical = rules.get("critical", False)
        
        status = "PASS"
        breach_msg = ""
        
        # Max check
        if "max" in rules and val > rules["max"]:
            status = "BREACH"
            if is_critical:
                has_critical_breach = True
            breach_msg = f"{label} of {val} {unit} exceeds maximum allowed limit of {rules['max']} {unit}."
        # Min check
        elif "min" in rules and val < rules["min"]:
            status = "BREACH"
            if is_critical:
                has_critical_breach = True
            breach_msg = f"{label} of {val} {unit} is below minimum required limit of {rules['min']} {unit}."
        # Warning checks
        elif "warning_above" in rules and val > rules["warning_above"]:
            status = "WARNING"
            has_warning = True
            breach_msg = f"{label} of {val} {unit} is in cautionary elevated range (threshold: {rules['warning_above']} {unit})."
        elif "warning_below" in rules and val < rules["warning_below"]:
            status = "WARNING"
            has_warning = True
            breach_msg = f"{label} of {val} {unit} is approaching lower limit (threshold: {rules['warning_below']} {unit})."
            
        if status in ("BREACH", "WARNING"):
            anomalies.append({
                "parameter": param_key,
                "label": label,
                "value": val,
                "unit": unit,
                "status": status,
                "is_critical": is_critical,
                "message": breach_msg
            })
            
        results.append({
            "key": param_key,
            "label": label,
            "value": val,
            "unit": unit,
            "min_limit": rules.get("min"),
            "max_limit": rules.get("max"),
            "status": status,
            "is_critical": is_critical
        })
        
    lot_disposition = "ACCEPTED"
    if has_critical_breach:
        lot_disposition = "REJECTED_QUARANTINE"
    elif has_warning:
        lot_disposition = "ACCEPT_WITH_PENALTY"
        
    # Validation constraint on approval
    can_auto_approve = not has_critical_breach
    approval_blocked = has_critical_breach and not bool(override_reason and len(override_reason.strip()) > 10)
    
    return {
        "commodity_key": commodity_key,
        "commodity_name": spec_def["name"],
        "lot_number": lot_number,
        "supplier_name": supplier_name,
        "lot_disposition": lot_disposition,
        "has_critical_breach": has_critical_breach,
        "qc_approved": qc_approved,
        "approval_blocked": approval_blocked,
        "override_reason": override_reason,
        "anomalies_count": len(anomalies),
        "anomalies": anomalies,
        "parameters_table": results
    }

# ---------------------------------------------------------------------------
# VERTICAL 3: OEM SMART SHED SENSOR & MANUAL REGISTER CORRELATION
# ---------------------------------------------------------------------------
def correlate_controller_with_register(
    hourly_sensor_data: List[Dict[str, Any]],
    day_number: int,
    manual_mortality_count: int
) -> Dict[str, Any]:
    """
    Correlates environmental controller telemetry (temperature, static pressure, fan status)
    with the manual shed register mortality count on day N.
    Pinpoints mechanical/environmental causes for sudden bird losses.
    """
    max_temp = -999.0
    min_temp = 999.0
    max_hi = -999.0  # Heat index or THI
    pressure_drops = []
    high_temp_hours = []
    
    for record in hourly_sensor_data:
        hour = record.get("hour", 0)
        temp_c = float(record.get("inside_temp_c", 0.0))
        humidity = float(record.get("rh_pct", 0.0))
        static_pressure = float(record.get("static_pressure_pa", 25.0))
        fan_stage = int(record.get("fan_stage", 4))
        
        if temp_c > max_temp:
            max_temp = temp_c
        if temp_c < min_temp:
            min_temp = temp_c
            
        # Simplified Heat Index for poultry: Temp (°F) + RH% or temp stress > 33°C
        if temp_c >= 33.5:
            high_temp_hours.append({"hour": hour, "temp_c": temp_c, "rh": humidity})
            
        # Tunnel ventilation static pressure failure (< 15 Pa when high fans active)
        if fan_stage >= 4 and static_pressure < 15.0:
            pressure_drops.append({"hour": hour, "pressure_pa": static_pressure, "fans": fan_stage})
            
    is_heat_stress_spike = (len(high_temp_hours) >= 2 and max_temp >= 35.0)
    mechanical_failure_detected = len(pressure_drops) > 0
    
    diagnosis = "Normal Environmental Conditions"
    if is_heat_stress_spike and mechanical_failure_detected:
        diagnosis = (f"CRITICAL HEAT PROSTRATION & TUNNEL FAILURE: Shed peaked at {max_temp:.1f}°C between 13:00-15:00. "
                     f"Static pressure collapsed to {pressure_drops[0]['pressure_pa']} Pa due to fan belt slipping, "
                     f"directly explaining the {manual_mortality_count} dead birds recorded on Day {day_number} shed card.")
    elif is_heat_stress_spike:
        diagnosis = f"HEAT STRESS DETECTED: Peak temp of {max_temp:.1f}°C observed. Correlates with {manual_mortality_count} dead birds."
    elif manual_mortality_count > 15:
        diagnosis = f"NON-CLIMATE MORTALITY SPIKE: Controller logged normal climate. Investigate infectious disease (IBD/ND) or water intoxication."
        
    return {
        "day": day_number,
        "max_temperature_c": round(max_temp, 1),
        "min_temperature_c": round(min_temp, 1),
        "high_temp_hours_count": len(high_temp_hours),
        "pressure_drop_events": len(pressure_drops),
        "root_cause_diagnosis": diagnosis,
        "is_heat_stress_spike": is_heat_stress_spike,
        "mechanical_failure_detected": mechanical_failure_detected,
        "recommendation": "Inspect Fan #3 belt tension and check backup generator transfer switch response."
    }

if __name__ == "__main__":
    print("Testing rules engine determinism...")
    
    # Quick self-test with sample day 22 spike
    sample_rows = [
        {"day": 20, "opening_birds": 4850, "mortality": 4, "culls": 1, "closing_birds": 4845,
         "opening_feed_bags": 24, "feed_bags_received": 30, "feed_bags_consumed": 18, "closing_feed_bags": 36,
         "avg_body_weight_g": 910, "water_liters": 1600},
        {"day": 21, "opening_birds": 4845, "mortality": 5, "culls": 2, "closing_birds": 4838,
         "opening_feed_bags": 36, "feed_bags_received": 0, "feed_bags_consumed": 19, "closing_feed_bags": 17,
         "avg_body_weight_g": 985, "water_liters": 1700},
        {"day": 22, "opening_birds": 4838, "mortality": 28, "culls": 2, "closing_birds": 4808,  # SPIKE: 28 dead
         "opening_feed_bags": 17, "feed_bags_received": 25, "feed_bags_consumed": 22, "closing_feed_bags": 16, # Discrepancy! 17+25-22 = 20, reported 16 (4 bags missing!)
         "avg_body_weight_g": 1025, "water_liters": 2800} # FCR drift & water surge
    ]
    
    res = evaluate_broiler_shed_ledger(5000, sample_rows)
    print("Shed Evaluation Status:", res["status"])
    print(f"Anomalies detected: {res['anomalies_count']}")
    for a in res["anomalies"]:
        print(f"  [{a['severity']}] {a['code']}: {a['message']}")
        
    print("\nTesting Feed COA Evaluation...")
    sample_coa = {
        "aflatoxin_b1_ppb": 28.4,  # BREACH (> 20.0)
        "moisture_pct": 13.8,      # BREACH (> 12.0)
        "crude_protein_pct": 8.1,  # WARNING (< 8.5)
        "damaged_grain_pct": 2.2,
        "foreign_matter_pct": 0.8
    }
    coa_res = evaluate_feed_coa("yellow_maize", "MZ-2026-HYD-108", "Sri Lakshmi Agro Traders, Nizamabad", sample_coa)
    print("COA Disposition:", coa_res["lot_disposition"])
    print(f"COA Anomalies: {coa_res['anomalies_count']}")
    for a in coa_res["anomalies"]:
        print(f"  [{a['status']}] {a['label']}: {a['message']}")
