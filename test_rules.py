import json
import unittest
from rules_engine import (
    evaluate_broiler_shed_ledger,
    evaluate_feed_coa,
    correlate_controller_with_register,
    get_cobb_benchmark_for_day
)

class TestPoultryExpoRulesEngine(unittest.TestCase):
    
    def test_cobb_benchmark_lookup(self):
        day_1 = get_cobb_benchmark_for_day(1)
        self.assertEqual(day_1["target_weight_g"], 42)
        
        day_22 = get_cobb_benchmark_for_day(22)
        self.assertEqual(day_22["target_weight_g"], 1060)
        self.assertEqual(day_22["target_fcr"], 1.41)
        
    def test_shed_card_anomaly_detection(self):
        # 3 day test with Day 22 anomaly
        rows = [
            {"day": 20, "opening_birds": 4850, "mortality": 3, "culls": 1, "closing_birds": 4846,
             "opening_feed_bags": 20, "feed_bags_received": 30, "feed_bags_consumed": 18, "closing_feed_bags": 32,
             "avg_body_weight_g": 910},
            {"day": 21, "opening_birds": 4846, "mortality": 4, "culls": 2, "closing_birds": 4840,
             "opening_feed_bags": 32, "feed_bags_received": 0, "feed_bags_consumed": 19, "closing_feed_bags": 13,
             "avg_body_weight_g": 985},
            {"day": 22, "opening_birds": 4840, "mortality": 28, "culls": 2, "closing_birds": 4810,
             "opening_feed_bags": 13, "feed_bags_received": 25, "feed_bags_consumed": 22, "closing_feed_bags": 12, # 13+25-22 = 16 expected, 12 reported (-4 bags discrepancy)
             "avg_body_weight_g": 1025, "water_liters": 2900}
        ]
        
        result = evaluate_broiler_shed_ledger(4850, rows, bag_weight_kg=50.0)
        self.assertEqual(result["status"], "BREACH")
        
        anomaly_codes = [a["code"] for a in result["anomalies"]]
        self.assertIn("DAILY_MORTALITY_SPIKE", anomaly_codes)
        self.assertIn("FEED_INVENTORY_DISCREPANCY", anomaly_codes)
        
    def test_feed_mill_coa_aflatoxin_breach(self):
        test_values = {
            "aflatoxin_b1_ppb": 28.4,
            "moisture_pct": 13.8,
            "crude_protein_pct": 8.1
        }
        res = evaluate_feed_coa("yellow_maize", "MZ-108", "Sri Lakshmi Agro", test_values)
        self.assertEqual(res["lot_disposition"], "REJECTED_QUARANTINE")
        self.assertTrue(res["has_critical_breach"])
        self.assertTrue(res["approval_blocked"])
        
    def test_controller_shed_correlation(self):
        sample_hourly = [
            {"hour": 11, "inside_temp_c": 28.5, "rh_pct": 65, "static_pressure_pa": 27.0, "fan_stage": 4},
            {"hour": 12, "inside_temp_c": 31.0, "rh_pct": 62, "static_pressure_pa": 26.5, "fan_stage": 4},
            {"hour": 13, "inside_temp_c": 35.8, "rh_pct": 72, "static_pressure_pa": 12.0, "fan_stage": 5}, # fan belt slip
            {"hour": 14, "inside_temp_c": 36.8, "rh_pct": 74, "static_pressure_pa": 11.5, "fan_stage": 5}, # high heat
            {"hour": 15, "inside_temp_c": 34.2, "rh_pct": 70, "static_pressure_pa": 14.0, "fan_stage": 4},
            {"hour": 16, "inside_temp_c": 29.5, "rh_pct": 68, "static_pressure_pa": 26.0, "fan_stage": 4}
        ]
        
        diag = correlate_controller_with_register(sample_hourly, 22, 28)
        self.assertTrue(diag["is_heat_stress_spike"])
        self.assertTrue(diag["mechanical_failure_detected"])
        self.assertIn("CRITICAL HEAT PROSTRATION", diag["root_cause_diagnosis"])

if __name__ == "__main__":
    unittest.main()
