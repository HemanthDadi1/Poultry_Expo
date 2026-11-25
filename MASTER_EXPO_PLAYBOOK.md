# Poultry India Expo 2026 — FDE Field Discovery Playbook
**Event:** Poultry India Expo 2026, HITEX Exhibition Centre, Hyderabad (Nov 25–27, 2026)  
**Approach:** Forward Deployed Engineering (Diagnose Bottlenecks $\to$ Map Workflow & Data $\to$ Propose Scoped PoV)  
**Reference Prototype:** [index.html](file:///Users/hemanthdadi/Downloads/Poultry_Expo_Brief/index.html)

---

## PART 1: The Mindset Shift (Stop Selling, Start Diagnosing)

If you walk up to a booth pitching a product, people put up a wall immediately. At an expo, everyone is trying to sell them something.

Your edge is **not** being a software salesperson—it's being a **Forward Deployed Engineer (FDE)** doing field discovery:
* **You are not pushing a pre-packaged app.** You are there to understand how their operations actually run, find where manual work, messy documents, or system gaps cost them time/money, and figure out *if* a custom AI + rules workflow is worth building for them.
* **How to treat your tablet ([index.html](file:///Users/hemanthdadi/Downloads/Poultry_Expo_Brief/index.html)):** Keep it in your bag or at your side at first. **Do not open with a demo.** Only pull it out *after* they describe a real bottleneck, and frame it honestly: *"We built a quick working prototype for a similar workflow just to test how vision + deterministic rules behave offline—want to see what that looks like?"*
* **Your Goal at the Expo:** Not to close a software deal on the floor. Your goal is to have **10–15 honest operational conversations**, uncover **3–5 real, quantified bottlenecks**, and leave with permission to do a **1-page Discovery Brief / Proof of Value (PoV)** on their actual sample data.

---

## PART 2: Understand Their World Before You Talk

Before walking into HITEX, understand the daily reality of the three groups you'll meet so you can ask smart, grounded questions:

### 1. Broiler Integrators (Suguna, Sneha, ABIS/IB Group, Venky's, Indbro)
* **How it works:** They place day-old chicks, **50 kg feed bags**, and medicines with contract farmers. At Day 35–40, birds are weighed and farmers are paid **Growing Charges** based on **FCR** ($\text{Feed kg} \div \text{Live Weight kg}$) and **Mortality %**.
* **Where friction usually hides:** Line supervisors visit 8–12 farms a day, snap WhatsApp photos of handwritten shed cards, and someone in the regional office types them into Excel/SAP days later. By the time a +0.05 FCR drift (~₹3/bird loss) or missing feed bags show up, the flock is already harvested.

### 2. Commercial Feed Mills (Godrej Agrovet, Prodigy Foods, Bentoli, KSE, Japfa)
* **How it works:** Yellow Maize is ~55–60% of feed cost. Incoming trucks must pass QC specs before unloading into silos—especially **Aflatoxin B1 ($\le 20\text{ ppb}$)** and **Moisture ($\le 12\%$)**.
* **Where friction usually hides:** At 5:00 PM when 15 maize trucks are queued at the weighbridge, 3rd-party lab Certificates of Analysis (COAs) arrive as scanned PDFs or WhatsApp images in inconsistent formats. Under pressure to clear trucks, manual checks slip.

### 3. Equipment & EC Automation OEMs (Dhumal, Chak Rader, AgroLogic, Big Dutchman)
* **How it works:** They sell Environmentally Controlled (EC) tunnel sheds, fans, and controllers (tracking Static Pressure Pa, Temp, RH%, Fan Stages).
* **Where friction usually hides:** When summer heat spikes kill birds, integrators blame the OEM's equipment. The OEM has controller CSV logs, while the farm has paper mortality logs—and nobody connects the two to prove whether a fan belt slipped (< 15 Pa) or the farmer's generator failed.

---

## PART 3: Who to Meet & How to Start a Natural Conversation

### Target Map at HITEX
| Group | Where | Target Companies | Who Actually Knows the Bottlenecks |
| :--- | :--- | :--- | :--- |
| **Integrators** | Halls 4 & 5 | ABIS, Suguna, Sneha, Venky's, HMA, Indbro | Head of Integration, GM Live Production, Audit/Accounts Lead, IT/SAP Lead |
| **Feed Mills** | Halls 5–7 & CLFMA JJ37 | Godrej Agrovet, Prodigy, Bentoli, KSE, Japfa | QC Director, Chief Nutritionist, Plant Head, Raw Material Procurement |
| **OEMs** | Halls 2–4 | Dhumal, Chak Rader, AgroLogic, Big Dutchman | MD, Head of Product/Automation, National Service/AMC Head |

### How to Open (Zero Sales Vibe)
Stand like a peer, not a pitchman. Start with curiosity about *their* operations:
* **Opener 1 (General Ops):** *"Hi! I'm an engineer working on automating messy field paperwork and ERP handoffs in poultry. Curious—for a team your size, where does data still get stuck between the farm/plant and your head office?"*
* **Opener 2 (Integrators):** *"Hi! Quick question from an engineering angle—are your line supervisors still sending handwritten shed cards over WhatsApp, or have you fully digitized farm-to-SAP?"*
* **Opener 3 (Feed Mills):** *"Hi! Curious how your QC team handles incoming maize lab COAs during peak evening truck rush—are those still checked manually off PDFs?"*
* **Opener 4 (OEMs):** *"Hi! When an integrator has a mortality spike in an EC shed, how do you guys currently correlate your controller logs with their farm registers?"*

---

## PART 4: How to Find the Bottleneck (The 4-Step FDE Diagnostic)

Once they engage, **listen 80% of the time**. Walk through these 4 mental checkpoints—not as a checklist you read off paper, but as natural follow-ups:

1. **Map the Workflow:**  
   *"Walk me through what happens from the moment a shed card is written / a truck arrives at the gate until it hits your ERP or final payout."*
2. **Find the Swivel-Chair / Delay Tax:**  
   *"Where does work pause waiting for someone to type, verify, or cross-check two different things?"*
3. **Check Data & Constraints Reality:**  
   *"What format is that data in today (paper, WhatsApp photos, scanned PDFs, Excel, SAP), and what happens if a number is wrong—is there a strict compliance or payout rule?"*
4. **Quantify the Cost of Doing Nothing:**  
   *"If that step wasn't delayed or manual, what would actually change—fewer disputes, faster batch closing, catching problems a week earlier?"*

### When (and How) to Show the Tablet
**Only** pull out [index.html](file:///Users/hemanthdadi/Downloads/Poultry_Expo_Brief/index.html) if they describe a real pain that matches (e.g., messy WhatsApp cards, COA checking, or controller-vs-mortality correlation):
> *"That exact handoff gap is why we built a small offline prototype to test an approach we call **'AI reads, people confirm, rules decide.'** We never let AI do FCR or payout math—AI just extracts the messy photo, a human taps confirm, and deterministic rules flag mismatches. Here's roughly what that looks like..."*

Show the relevant tab (`🐔 Broiler Integrator`, `🌽 Feed Mill COA`, or `📡 OEM Controller`) for **30 seconds max**, then close the tablet and go back to *their* problem.

---

## PART 5: Pivots When You Don't Get the Expected Response

Real conversations rarely follow a script. Use these pivots to stay authentic and either find a *different* real bottleneck or exit gracefully:

### Pivot 1: *"We already have SAP / our own field app."*
* **Don't argue.** Validate it and probe the seam:
  > *"Nice—getting supervisors onto an app is half the battle. Where do you still see friction *around* SAP? For example, 3rd-party lab COAs, transport/weighbridge slips, or reconciling physical feed bags against what's keyed in?"*

### Pivot 2: *"We don't really have leakage or data delays—our team is on top of it."*
* **Don't push the same angle.** Pivot to **effort** or **different departments**:
  > *"That's rare and impressive. Out of curiosity, how many people in the back office does it take to keep it that clean? Or is the bigger headache right now somewhere else—like vendor billing, hatchery records, or lab turnaround?"*

### Pivot 3: *"We don't do contract farming (we only sell feed / chicks / equipment)."*
* **Pivot to their actual bottleneck:**
  * **If pure feed mill:** *"Got it—then farm shed cards aren't your world. On the mill side, where does QC or raw material intake still slow down? Incoming grain COAs, broker disputes, or silo traceability?"*
  * **If pure hatchery/layer/trader:** Ask one curiosity question (*"What's the most manual data headache in your operation?"*). If it's not a fit, wrap up warmly in 20 seconds and move on.

### Pivot 4: *"The bottleneck is actually something completely different (e.g., hatchery, billing, vet reports, transport)."*
* **This is an FDE win, not a failure!** You aren't a 1-product salesperson—you build solutions around bottlenecks.
  > *"Tell me more about that. What does that workflow look like today, and where does it break?"*  
  Use the **Discovery Capture Sheet (Part 6)** to document *their* actual problem and offer a tailored PoV.

### Pivot 5: *"I'm just in sales / marketing—I don't know the operations side."*
* **Pivot to ally-building:**
  > *"Totally fair! I'm trying to talk to operations and QC leads while I'm at HITEX just to understand their workflow bottlenecks. Is your GM of Integration or QC Head around the booth today, or could you point me to them?"*

### Pivot 6: *"Leave your card / send us an email."*
* **Honest exit / low-friction test:**
  > *"Sure, happy to. Just so I don't spam you with generic stuff—was there a specific manual workflow on your mind, or are you guys pretty much set right now?"*  
  If they say *"We're set"*, smile, thank them, and move to the next booth. Never chase someone who has no pain.

---

## PART 6: The Discovery Evidence Document (Capture After Every Good Talk)

Instead of pitching a contract, offer a **Zero-Commitment Discovery Brief** as your next step:
> *"Look, I don't want to guess what your data looks like. If you want, send me 5–10 anonymized sample documents (shed cards, COAs, or whatever report is giving your team headaches) next week. I'll map out the exact bottleneck, test whether automation actually works on your real format, and send you a 1-page Discovery Brief. If the math doesn't make sense, I'll tell you honestly."*

Fill this **1-Page FDE Discovery Capture** right after walking away from the booth (takes 2 minutes in your phone notes):

```
========================================================================
FDE FIELD DISCOVERY CAPTURE — HITEX 2026
========================================================================
Company / Person / Role:   _____________________________________________
WhatsApp / Contact:        _____________________________________________
Scale (Birds/mo or TPD):   _____________________________________________

1. THE BOTTLENECK (In their own words)
   • What hurts today?     _____________________________________________
   • Where does it pause?  _____________________________________________
   • Cost / impact:        _____________________________________________

2. WORKFLOW & DATA REALITY
   • Current steps:        [Input] -> [Handoff] -> [Verify] -> [ERP]
   • Data formats:         [ ] Paper  [ ] WhatsApp  [ ] PDF  [ ] CSV/ERP
   • Who must approve?     _____________________________________________

3. UNKNOWNS TO VALIDATE
   • Can they share 5-10 anonymized samples?   [ ] Yes  [ ] Needs approval
   • Strict business rules / compliance?       _________________________

4. PROPOSED NEXT STEP (PoV / Evidence)
   • Agreed action:        _____________________________________________
   • Target date:          _____________________________________________
========================================================================
```

---

## PART 7: 3-Day Expo Rhythm (Nov 25 – Nov 27, 2026)

* **Day 1 (Nov 25) — Listen & Map:** Walk Halls 2–7. Focus on having 10+ relaxed discovery conversations with OEMs, Feed Mills, and Integrators. Don't force demos; collect real-world pains and WhatsApp contacts.
* **Day 2 (Nov 26) — Deepen & Validate:** Peak day for MDs, GMs, and VPs. Re-visit promising contacts from Day 1, and use your tablet only as a **visual reference** when their described problem matches.
* **Day 3 (Nov 27) — Lock Discovery Samples Before 3:00 PM:** Exhibitors pack up by 3:30–4:00 PM. Follow up with your top 3–5 contacts to lock in **sample data exchanges** (5–10 real documents) so you can deliver concrete **FDE Discovery Briefs** the week after the expo.
