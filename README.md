# Poultry India Expo 2026 Sprint (Nov 25–27, HITEX Hyderabad)
**Architecture Axiom:** *"AI reads. People confirm. Rules decide."*  
**Author:** Hemanth Dadi

---

## 1. System Overview
This repository contains the offline tablet application and deterministic validation pipeline built for the Poultry India Expo 2026 sprint at HITEX, Hyderabad. It addresses the 3 core poultry verticals:

1. **Mid-to-Large Broiler Integrators (Halls 4 & 5 — ABIS Exports, HMA Agro, Indbro):**
   - WhatsApp handwritten shed card photo -> Structured daily ledger -> Supervisor "Confirm & Lock" -> Deterministic Cobb 500 FCR, cumulative mortality %, and feed mass-balance discrepancy flags.
2. **Commercial Feed Mills & Premixers (Halls 5–7 & CLFMA JJ37 — Prodigy Foods, Bentoli):**
   - Scanned Lab COA PDF -> Extracted chemical specs -> QC "Approve Lot" lock -> Deterministic compliance checks flagging Aflatoxin B1 (> 20 ppb) and Moisture (> 12%).
3. **Poultry Equipment & Automation OEMs (Halls 2–4 — Dhumal, Chak Rader, Agrologic):**
   - Merged controller CSV telemetry + handwritten shed card image -> Root-cause diagnosis of heat-stress mortality spikes and fan belt slips.

---

## 2. Technical Architecture & Offline Parity
- **Offline-First:** Runs 100% locally in the browser with zero external network dependencies, ensuring flawless operation even when convention hall Wi-Fi drops.
- **Deterministic Math Engine (`rules_engine.py` & `rules_engine.js`):**
  - No hallucinated calculations: LLM (Gemini Vision) is strictly used for multimodal visual grounding and text extraction.
  - All FCR computations, cumulative mortalities, feed bag reconciliation, and COA threshold evaluations are performed by pure mathematical algorithms.
  - Supports Pyodide (WebAssembly Python) in modern browsers, with seamless instant fallback to identical deterministic JavaScript logic.
- **Touch-Friendly Editorial UI:**
  - 50/50 split-screen layout designed specifically for iPad Pro / Samsung Galaxy Tab landscape and portrait viewing.
  - Left pane: Sample raw document viewer with pan, zoom (100% to 220%), and layer toggles (Gemini Grounding Bounding Boxes and Anomaly Focus).
  - Right pane: KPI metric cards, supervisor confirm & lock gate, and interactive editable table with sub-millisecond recalculation.

---

## 3. Directory Structure
```
Poultry_Expo_Brief/
├── index.html                  # Single-page offline tablet demo app
├── app.css                     # Editorial tablet styling (touch targets >= 44px)
├── app.js                      # UI logic, state management, and real-time recalculations
├── rules_engine.py             # Pure Python deterministic rules engine
├── rules_engine.js             # 1-to-1 JavaScript parity implementation (offline engine)
├── pyodide_runner.js           # Pyodide WebAssembly runner
├── test_rules.py               # Python unit tests verifying all rules and benchmarks
├── quick_import.py             # Fast 2-minute CLI prospect ingestion tool
├── EXPO_DEMO_SCRIPT.md         # Step-by-step expo floor sales pitch guide
├── assets/
│   ├── shed_card_mock.svg      # Authentic handwritten Indian broiler shed register
│   └── feed_mill_coa_mock.svg  # Scanned NABL lab Certificate of Analysis PDF simulation
└── data/
    ├── broiler_shed_4_cobb500.json       # 25-day broiler dataset (Day 22 anomaly)
    ├── feed_mill_coa_maize_lot108.json   # Maize Lot #108 (28.4 ppb Aflatoxin breach)
    ├── oem_controller_hourly_day22.json  # Dhumal EC-800 controller hourly log
    └── manifest.json                     # Dynamic preset catalog for expo prospects
```

---

## 4. Running the Demo on a Tablet

### Option A: Open directly in any browser
Double-click `index.html` or open it directly in Safari / Chrome:
```bash
open index.html
```

### Option B: Local Python HTTP server (Recommended for tablet on local hotspot)
```bash
python3 -m http.server 8080
```
Then navigate to `http://<your-laptop-ip>:8080` from your tablet.

---

## 5. Ingesting New Prospect Files on the Expo Floor (< 15 min turnaround)

When an exhibitor provides a WhatsApp shed photo or lab PDF at HITEX:

### Via Tablet UI:
Tap the **"Quick Field Ingest"** button in the top bar to drop or upload the file directly.

### Via Command Line:
```bash
# Ingest broiler shed card
python3 quick_import.py --type shed_card --prospect "Suguna Broilers" --placed 6500 --image /path/to/whatsapp_photo.jpg

# Ingest feed mill COA
python3 quick_import.py --type coa --prospect "Godrej Agrovet" --lot "MZ-902" --aflatoxin 26.5 --moisture 13.5
```
The new prospect preset is immediately available in the demo's preset selector.

---

## 6. Running Verification Tests
```bash
python3 test_rules.py
```
Outputs:
```
....
----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK
```
