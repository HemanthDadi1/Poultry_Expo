# Poultry India Expo 2026 — 48-Hour Sprint Demo Script
**Location:** HITEX Exhibition Centre, Hyderabad (Nov 25–27, 2026)  
**Author:** Hemanth Dadi  
**Engineering Axiom:** *"AI reads. People confirm. Rules decide."*

---

## 1. The 30-Second Elevator Pitch (For Integrator CEOs & Mill MDs)
> *"Most poultry AI demos fail on the expo floor because they promise that ChatGPT will calculate your FCR or manage farm accounting. We don't do that.*  
> *Our engineering axiom is simple:*  
> **1. Gemini Vision reads** the messy WhatsApp shed card photo or scanned lab COA.  
> **2. Your supervisor confirms** with one touch, locking the data against edits.  
> **3. Pure deterministic Python rules decide** whether the FCR drifted, bags were stolen, or Aflatoxin breached 20 ppb.  
> *Zero hallucinations, zero Wi-Fi dependency, 100% offline tablet execution."*

---

## 2. Walkthrough Flow 1: Mid-to-Large Broiler Integrators (Halls 4 & 5)
**Target Prospects:** ABIS Exports (IB Group), HMA Agro, Indbro, Sneha Farms, Suguna.

### The Pain Point:
Contract farmers upload daily shed registers via WhatsApp photos at night. Junior data entry operators key them into SAP/Excel days later. By the time someone notices FCR has slipped by +0.08 or that 4 feed bags are missing, the flock has already been harvested at a massive financial loss.

### Demo Steps (60 seconds on tablet):
1. **Show Left Pane (Raw Document):**
   - Point to the handwritten register photo: *"Notice this authentic Indian shed register from Sri Balaji Farms. You see blue ballpoint pen, Telugu/English columns, and coffee smudges."*
   - Toggle **Gemini Grounding**: Highlight the translucent blue bounding boxes over the numbers. *"Gemini extracts every cell with 99%+ mean field confidence."*
2. **Expose the Day 22 Anomaly:**
   - Scroll to Day 22 in both panes:
     - **Mortality:** 28 dead birds (Daily mortality rate 0.56% vs Cobb 500 benchmark limit of 0.12%).
     - **Feed Bag Discrepancy:** `Opening (15) + Received (30) - Consumed (22) = 23 Expected Bags`. But the farmer wrote `19 Bags` (-4 bags unrecorded/stolen).
   - Point to the **Red Breach Banner** and **FCR Drift Card**:
     - FCR jumped to 2.520 (+1.050 above target).
3. **Trigger the Supervisor "Confirm & Lock":**
   - Tap any cell to show real-time re-calculation: change mortality from 28 to 15, and watch FCR recalculate instantly.
   - Now click **"Confirm & Lock Batch"**:
     - Inputs become read-only.
     - A green verified stamp appears: `CONFIRMED & LOCKED • 10:45 AM`.
     - *"Now the data is immutable and ready for ERP synchronization."*

---

## 3. Walkthrough Flow 2: Commercial Feed Mills & Premixers (Halls 5–7 & CLFMA JJ37)
**Target Prospects:** Prodigy Foods, Bentoli AgriNutrition, Godrej Agrovet, KSE.

### The Pain Point:
Maize and Soya DOC trucks sit at the factory gate while 3rd-party lab COAs arrive as scanned PDFs. Delayed manual review leads to unloading high-moisture or high-Aflatoxin grain into bulk silos, contaminating entire batches.

### Demo Steps (60 seconds on tablet):
1. **Switch to Feed Mill Tab (`🌽 Feed Mill COA`):**
   - Point to the scanned NABL Lab Certificate of Analysis from Analytical Testing Services Hyderabad for Maize Lot #108 (42.5 MT).
2. **Review Deterministic Spec Breaches:**
   - **Aflatoxin B1:** Observed 28.4 ppb (BIS & Feed Mill Spec: Max 20.0 ppb) -> **CRITICAL BREACH**.
   - **Moisture:** Observed 13.8% (Spec: Max 12.0%) -> **CRITICAL BREACH (Mold Spoilage Hazard)**.
   - **Crude Protein:** Observed 8.1% (Spec: Min 8.5%) -> **WARNING**.
3. **Demonstrate Supervisory Block:**
   - Point out that **Lot Disposition** is locked to `REJECTED_QUARANTINE`.
   - Tap **"Confirm & Lock Batch"**: The system refuses auto-approval and triggers a mandatory prompt:
     *"Critical Aflatoxin Breach! Enter mandatory QC Escalation Reason and Authorizing Director name to proceed."*
   - *"Your weighbridge discharge cannot happen without deterministic compliance."*

---

## 4. Walkthrough Flow 3: Poultry Equipment & Automation OEMs (Halls 2–4)
**Target Prospects:** Dhumal Industries, Chak Rader, Agrologic, Roxell.

### The Pain Point:
Hardware OEMs manufacture high-quality controllers and fans, but compete on price with imported equipment. They lack a software intelligence layer that connects controller alarms to the farmer's bottom line.

### Demo Steps:
1. **Switch to OEM Tab (`📟 OEM Smart Shed`):**
   - Show the hourly telemetry chart from the Dhumal EC-800 controller on Day 22.
2. **Highlight the Root Cause Correlation:**
   - Between 13:00 and 15:00, outside temperature was 38.2°C.
   - At 13:30, Fan #3 V-belt slipped: Static pressure collapsed from 28 Pa to 11 Pa.
   - Inside shed temperature spiked to 36.8°C.
   - Water meter logged a 65% surge in bird intake due to panting.
3. **Closing Hook:**
   - *"By marrying controller sensor logs with the handwritten shed card, the OEM proves to the integrator that the 28 bird deaths were due to a mechanical fan belt slip rather than feed toxicity. That is how Dhumal or Agrologic sells annual AMC packages."*

---

## 5. Ingesting Live Prospect Files in < 15 Minutes
When a prospect hands over a phone with a WhatsApp shed card photo or a lab PDF at HITEX:
1. Tap **"Quick Field Ingest"** in the top navigation bar.
2. Drag & drop or take a photo with the tablet camera.
3. Or run from terminal:
   ```bash
   python3 quick_import.py --type shed_card --prospect "Suguna Farms" --placed 6000 --image sample.jpg
   ```
4. The prospect's exact farm name, shed number, and numbers are immediately loaded into the demo.
