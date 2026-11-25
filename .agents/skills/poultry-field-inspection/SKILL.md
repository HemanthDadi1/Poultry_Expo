---
name: poultry-field-inspection
description: >
  Offline-first poultry field inspection, daily broiler ledger mass-balance verification,
  Cobb 500 FCR evaluation, feed mill lab COA spec checking (Aflatoxin B1 / Moisture),
  and IoT controller environmental correlation. Built on the core engineering axiom:
  "AI reads. People confirm. Rules decide."
metadata:
  publisher: antigravity
  author: Hemanth Dadi
  event: Poultry India Expo 2026 (HITEX Hyderabad)
---

# Poultry Field Inspection & Deterministic Verification Skill

This skill guides the agent in orchestrating multimodal document ingestion, human-in-the-loop supervisor confirmation, and deterministic math/rule execution for commercial poultry operations in India.

## Core Engineering Axiom
> **"AI reads. People confirm. Rules decide."**
> 1. **AI Reads:** Multimodal vision (Gemini Vision) extracts messy handwritten shed cards and scanned laboratory PDFs, returning grounded bounding coordinates and field confidence scores.
> 2. **People Confirm:** Extracted fields remain in an `UNVERIFIED` state until the farm supervisor or QC manager reviews, edits, and taps **Confirm & Lock**.
> 3. **Rules Decide:** Pure deterministic Python or typed mathematical rules evaluate mass-balances, Cobb 500 breed benchmark curves, and toxicological thresholds. **Never compute FCR, mortality %, or toxin thresholds using LLM token generation.**

---

## Target Verticals & Specific Rules

### 1. Mid-to-Large Broiler Integrators (ABIS, HMA, Indbro, Suguna)
- **Flock Sizing:** Standard Indian contract broiler batches range from `10,000` to `25,000` chicks placed.
- **Feed Metric:** Tracked in standard `50 kg` bags.
- **Bird Mass-Balance Formula:**
  $$\text{Closing Birds} = \text{Opening Birds} - \text{Daily Mortality} - \text{Daily Culls}$$
  *Flag `BIRD_COUNT_MISMATCH` if reported closing birds does not equal this value.*
- **Feed Mass-Balance Formula:**
  $$\text{Closing Feed Bags} = \text{Opening Feed Bags} + \text{Received Bags} - \text{Consumed Bags}$$
  *Flag `FEED_INVENTORY_DISCREPANCY` if physical bag count does not reconcile.*
- **FCR (Feed Conversion Ratio):**
  $$\text{Cumulative Feed (kg)} = \sum \text{Consumed Bags} \times 50.0$$
  $$\text{Total Live Biomass (kg)} = \frac{\text{Current Live Birds} \times \text{Avg Body Weight (g)}}{1000}$$
  $$\text{FCR} = \frac{\text{Cumulative Feed (kg)}}{\text{Total Live Biomass (kg)}}$$
- **Threshold Anomaly Flags:**
  - `DAILY_MORTALITY_SPIKE`: Flag `BREACH` if daily mortality exceeds `0.15%` of placed chicks (standard Cobb 500 limit: `0.12%`).
  - `FCR_DRIFT_EXCESS`: Flag `WARNING` if observed FCR drifts $> +0.05$ above breed target; flag `BREACH` if $> +0.10$.

### 2. Commercial Feed Mills & Premixers (Prodigy Foods, Bentoli, Godrej)
- **Commodity Specs (Yellow Maize / Corn Grain):**
  - **Aflatoxin B1:** Max `20.0 ppb` (AOAC 991.31 HPLC). Flag `CRITICAL BREACH` if $> 20.0\text{ ppb}$.
  - **Moisture:** Max `12.0%` (IS 4333 Part II). Flag `CRITICAL BREACH` if $> 12.0\%$ (silo fungal mold hazard).
  - **Crude Protein (CP):** Min `8.5%` (IS 7874 Kjeldahl). Flag `WARNING` if $< 8.5\%$.
- **Lot Release Gate:**
  - If any critical parameter breaches, disposition is `REJECTED_QUARANTINE`.
  - Supervisor approval is strictly blocked unless a formal QC Director written justification note is entered.

### 3. Equipment & Automation OEMs (Dhumal, Chak Rader, Agrologic)
- **Telemetry Fusion:** Merges hourly EC controller CSV logs (Inside Temp, RH %, Static Pressure Pa, Fan Stages) with the manual register.
- **Root Cause Diagnosis:** Detects tunnel ventilation mechanical failures (e.g. static pressure dropping below `15 Pa` during peak fan stages due to belt slippage), correlating climate surges with heat prostration mortality spikes.

---

## Operating Instructions & Script Usage

### Executing Deterministic Rules
To run headless validation or batch test ledgers:
```bash
python3 rules_engine.py
python3 test_rules.py
```

### Rapid 2-Minute Prospect Ingest
When receiving an exhibitor's WhatsApp photo or scanned PDF on the expo floor:
```bash
# Ingest Broiler Register
python3 quick_import.py --type shed_card --prospect "Suguna Broilers" --placed 12500 --image /path/to/whatsapp_photo.jpg

# Ingest Feed Mill COA
python3 quick_import.py --type coa --prospect "Godrej Agrovet" --lot "MH-402" --aflatoxin 28.4 --moisture 13.8
```

### Tablet Demo Launch
Launch the local offline web demo on tablet:
```bash
python3 -m http.server 8080
```
Navigate to `http://<local-ip>:8080` in iPad Safari and tap **"Add to Home Screen"**.
