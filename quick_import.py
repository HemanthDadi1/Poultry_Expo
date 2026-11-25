#!/usr/bin/env python3
"""
Poultry India Expo 2026 - Quick Import Script
Author: Hemanth Dadi

Allows fast 2-minute ingestion of incoming prospect WhatsApp photos and scanned COA PDFs
collected on Nov 25-27 at HITEX Hyderabad.

Usage:
    python3 quick_import.py --type shed_card --image /path/to/whatsapp_photo.jpg --prospect "Suguna Foods" --placed 6000
    python3 quick_import.py --type coa --pdf /path/to/lab_coa.pdf --prospect "Godrej Agrovet" --lot "MZ-902"
    python3 quick_import.py --list
"""

import argparse
import json
import os
import shutil
import sys
import time

MANIFEST_PATH = "data/manifest.json"
CUSTOM_ASSETS_DIR = "assets/custom_ingest"

def ensure_directories():
    os.makedirs("data", exist_ok=True)
    os.makedirs(CUSTOM_ASSETS_DIR, exist_ok=True)
    if not os.path.exists(MANIFEST_PATH):
        init_manifest = {
            "version": "1.0",
            "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
            "presets": [
                {
                    "id": "broiler_shed_4",
                    "type": "shed_card",
                    "title": "ABIS Exports - Shed #4 (Day 22 Spike & Bag Discrepancy)",
                    "prospect": "ABIS Exports / IB Group",
                    "data_file": "data/broiler_shed_4_cobb500.json",
                    "doc_asset": "assets/shed_card_mock.svg",
                    "is_default": True
                },
                {
                    "id": "maize_coa_108",
                    "type": "coa",
                    "title": "Prodigy Foods / Bentoli - Maize Lot #108 (28.4 ppb Aflatoxin)",
                    "prospect": "Prodigy Foods Pvt Ltd",
                    "data_file": "data/feed_mill_coa_maize_lot108.json",
                    "doc_asset": "assets/feed_mill_coa_mock.svg",
                    "is_default": True
                },
                {
                    "id": "oem_controller_22",
                    "type": "oem_controller",
                    "title": "Dhumal / Agrologic - Day 22 Climate & Telemetry Log",
                    "prospect": "Dhumal Industries / Agrologic",
                    "data_file": "data/oem_controller_hourly_day22.json",
                    "doc_asset": "assets/shed_card_mock.svg",
                    "is_default": False
                }
            ]
        }
        with open(MANIFEST_PATH, "w") as f:
            json.dump(init_manifest, f, indent=2)

def list_presets():
    ensure_directories()
    with open(MANIFEST_PATH, "r") as f:
        m = json.load(f)
    print("\n--- AVAILABLE PROSPECT PRESETS ---")
    for p in m.get("presets", []):
        print(f"[{p['id']}] ({p['type'].upper()}) {p['title']} -> Prospect: {p['prospect']}")
    print("")

def import_shed_card(image_path: str, prospect: str, placed_chicks: int, shed_no: str = "01"):
    ensure_directories()
    timestamp_slug = time.strftime("%Y%m%d_%H%M%S")
    target_id = f"shed_card_{prospect.lower().replace(' ', '_')}_{timestamp_slug}"
    
    # Copy source image if given
    dest_asset = f"{CUSTOM_ASSETS_DIR}/{target_id}.svg"
    if image_path and os.path.exists(image_path):
        ext = os.path.splitext(image_path)[1]
        dest_img = f"{CUSTOM_ASSETS_DIR}/{target_id}{ext}"
        shutil.copyfile(image_path, dest_img)
        dest_asset = dest_img
    else:
        # Link default shed card asset
        dest_asset = "assets/shed_card_mock.svg"

    # Generate realistic template rows (Days 1 to 21)
    rows = []
    birds = placed_chicks
    feed_bags_bal = 40
    for day in range(1, 22):
        mort = 2 if day < 10 else 3
        culls = 1 if day in (7, 14, 21) else 0
        birds_close = birds - mort - culls
        feed_consumed = int(day * 0.9) + 2
        received = 30 if day in (1, 8, 15) else 0
        feed_bags_bal = feed_bags_bal + received - feed_consumed
        
        # Approximate body weight
        wt = int(42 + (day * 45))
        
        rows.append({
            "day": day,
            "opening_birds": birds,
            "mortality": mort,
            "culls": culls,
            "closing_birds": birds_close,
            "opening_feed_bags": feed_bags_bal + feed_consumed - received,
            "feed_bags_received": received,
            "feed_bags_consumed": feed_consumed,
            "closing_feed_bags": feed_bags_bal,
            "avg_body_weight_g": wt,
            "water_liters": int(feed_consumed * 50 * 1.8),
            "notes": f"Field inspection Day {day}"
        })
        birds = birds_close

    data_payload = {
        "metadata": {
            "title": f"Broiler Shed Register - {prospect}",
            "farm_name": f"{prospect} Contract Farm",
            "integrator": prospect,
            "location": "Telangana Region",
            "farmer_name": "Sample Contract Farmer",
            "supervisor_name": "Field Tech Officer",
            "flock_id": f"{prospect[:4].upper()}-BATCH-2026",
            "shed_no": shed_no,
            "chicks_placed": placed_chicks,
            "placement_date": time.strftime("%Y-%m-%d"),
            "current_evaluation_day": 21,
            "hatchery_source": "VH Group",
            "feed_type": "50kg Pellets",
            "supervisor_locked": False
        },
        "rows": rows
    }

    data_file_path = f"data/{target_id}.json"
    with open(data_file_path, "w") as f:
        json.dump(data_payload, f, indent=2)

    # Register in manifest
    with open(MANIFEST_PATH, "r") as f:
        manifest = json.load(f)

    manifest["presets"].append({
        "id": target_id,
        "type": "shed_card",
        "title": f"{prospect} - Shed #{shed_no} ({placed_chicks} Birds)",
        "prospect": prospect,
        "data_file": data_file_path,
        "doc_asset": dest_asset,
        "is_default": False
    })
    manifest["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"SUCCESS: Ingested shed card for '{prospect}' into '{data_file_path}'.")
    print(f"New preset ID: {target_id}. Available in tablet app immediately.")

def import_coa(pdf_path: str, prospect: str, lot_number: str, commodity: str = "yellow_maize", aflatoxin: float = 24.5, moisture: float = 13.2):
    ensure_directories()
    timestamp_slug = time.strftime("%Y%m%d_%H%M%S")
    target_id = f"coa_{prospect.lower().replace(' ', '_')}_{timestamp_slug}"

    dest_asset = f"{CUSTOM_ASSETS_DIR}/{target_id}.pdf"
    if pdf_path and os.path.exists(pdf_path):
        ext = os.path.splitext(pdf_path)[1]
        dest_pdf = f"{CUSTOM_ASSETS_DIR}/{target_id}{ext}"
        shutil.copyfile(pdf_path, dest_pdf)
        dest_asset = dest_pdf
    else:
        dest_asset = "assets/feed_mill_coa_mock.svg"

    data_payload = {
        "metadata": {
            "title": f"COA Inward Inspection - {prospect}",
            "feed_mill": prospect,
            "plant_location": "Hyderabad Region",
            "testing_laboratory": "Analytical Testing Services (NABL)",
            "coa_number": f"COA-{lot_number}",
            "sample_received_date": time.strftime("%Y-%m-%d"),
            "commodity": commodity,
            "commodity_display": "Yellow Maize (Feed Grade Corn)",
            "supplier_name": "Agro Commodity Supplier",
            "lot_number": lot_number,
            "consignment_qty_mt": 40.0,
            "qc_status": "PENDING_CHECK",
            "qc_approved": False,
            "override_reason": ""
        },
        "parameters": {
            "aflatoxin_b1_ppb": aflatoxin,
            "moisture_pct": moisture,
            "crude_protein_pct": 8.2,
            "damaged_grain_pct": 2.0,
            "foreign_matter_pct": 1.2,
            "free_fatty_acids_pct": 1.5
        }
    }

    data_file_path = f"data/{target_id}.json"
    with open(data_file_path, "w") as f:
        json.dump(data_payload, f, indent=2)

    with open(MANIFEST_PATH, "r") as f:
        manifest = json.load(f)

    manifest["presets"].append({
        "id": target_id,
        "type": "coa",
        "title": f"{prospect} - Lot #{lot_number} ({aflatoxin} ppb Afla)",
        "prospect": prospect,
        "data_file": data_file_path,
        "doc_asset": dest_asset,
        "is_default": False
    })
    manifest["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"SUCCESS: Ingested COA for '{prospect}' into '{data_file_path}'.")
    print(f"New preset ID: {target_id}. Ready for demo!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Poultry India Expo Quick Ingestion Tool")
    parser.add_argument("--type", choices=["shed_card", "coa"], help="Type of document to ingest")
    parser.add_argument("--image", help="Path to WhatsApp photo / image")
    parser.add_argument("--pdf", help="Path to COA PDF file")
    parser.add_argument("--prospect", default="Prospect Exhibitor", help="Name of prospect or company")
    parser.add_argument("--placed", type=int, default=5000, help="Initial placed chicks for shed card")
    parser.add_argument("--lot", default="LOT-EXPO-2026", help="Lot number for COA")
    parser.add_argument("--aflatoxin", type=float, default=24.5, help="Aflatoxin B1 level (ppb)")
    parser.add_argument("--moisture", type=float, default=13.2, help="Moisture level (pct)")
    parser.add_argument("--list", action="store_true", help="List all active presets in manifest")

    args = parser.parse_args()

    if args.list:
        list_presets()
    elif args.type == "shed_card":
        import_shed_card(args.image, args.prospect, args.placed)
    elif args.type == "coa":
        import_coa(args.pdf, args.prospect, args.lot, aflatoxin=args.aflatoxin, moisture=args.moisture)
    else:
        parser.print_help()
