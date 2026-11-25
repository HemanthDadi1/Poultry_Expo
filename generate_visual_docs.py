"""
Generates high-contrast, clean editorial SVG mock documents:
1. Authentic Indian Broiler Shed Daily Register (12,500 Cobb 500 birds, Siddipet Zone, Day 22 mortality spike 68 dead, 8 missing feed bags)
2. Scanned NABL Lab COA PDF (Maize Lot MH-402, 28.4 ppb Aflatoxin B1 breach, 13.8% moisture)
3. OEM Controller Environmental Graph (Dhumal SmartVent EC-800 24-hr log on Day 22 showing Static Pressure drop to 11 Pa and 36.8°C spike)
"""

import os
os.makedirs("assets", exist_ok=True)

# 1. SHED CARD (Siddipet Zone, 12,500 Birds)
shed_card_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1300" width="1000" height="1300" style="background:#ffffff; font-family:'Courier New', monospace, sans-serif;">
  <rect width="1000" height="1300" fill="#fcfcfc" />
  <rect x="20" y="20" width="960" height="1260" fill="#ffffff" stroke="#d1d5db" stroke-width="1.5" />
  
  <g transform="translate(40, 45)">
    <rect x="0" y="0" width="920" height="90" fill="#f9fafb" stroke="#111827" stroke-width="1.5" />
    <text x="460" y="28" text-anchor="middle" font-size="18" font-weight="900" fill="#111827" font-family="-apple-system, sans-serif">SRI BALAJI BROILER FARMS — SIDDIPET ZONE</text>
    <text x="460" y="46" text-anchor="middle" font-size="11" font-weight="bold" fill="#4b5563" font-family="-apple-system, sans-serif">CONTRACT GROWER DIVISION • INTEGRATOR: ABIS EXPORTS (IB GROUP)</text>
    
    <line x1="0" y1="58" x2="920" y2="58" stroke="#111827" stroke-width="1" />
    <text x="15" y="78" font-size="11" font-weight="bold" fill="#111827">FARMER: M. Chandraiah (#408)</text>
    <text x="280" y="78" font-size="11" font-weight="bold" fill="#111827">SHED: 04 (EC Tunnel)</text>
    <text x="500" y="78" font-size="11" font-weight="bold" fill="#111827">PLACED: 12,500 DOC</text>
    <text x="740" y="78" font-size="11" font-weight="bold" fill="#111827">BREED: COBB 500</text>
  </g>

  <g transform="translate(40, 150)">
    <rect x="0" y="0" width="920" height="36" fill="#111827" />
    <text x="30" y="22" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">DAY</text>
    <line x1="60" y1="0" x2="60" y2="36" stroke="#4b5563" />
    <text x="110" y="22" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">OPENING</text>
    <line x1="160" y1="0" x2="160" y2="36" stroke="#4b5563" />
    <text x="210" y="22" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">MORTALITY</text>
    <line x1="260" y1="0" x2="260" y2="36" stroke="#4b5563" />
    <text x="300" y="22" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">CULLS</text>
    <line x1="340" y1="0" x2="340" y2="36" stroke="#4b5563" />
    <text x="400" y="22" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">CLOSING</text>
    <line x1="460" y1="0" x2="460" y2="36" stroke="#4b5563" />
    <text x="580" y="22" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">FEED (50kg BAGS): OPN + REC - CON = CLS</text>
    <line x1="720" y1="0" x2="720" y2="36" stroke="#4b5563" />
    <text x="770" y="22" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">AVG WT</text>
    <line x1="820" y1="0" x2="820" y2="36" stroke="#4b5563" />
    <text x="870" y="22" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">WATER (L)</text>
  </g>

  <g transform="translate(40, 186)">
    <!-- Day 18 -->
    <g transform="translate(0, 0)">
      <rect x="0" y="0" width="920" height="38" fill="#ffffff" stroke="#e5e7eb" />
      <text x="30" y="24" text-anchor="middle" font-weight="bold">18</text>
      <text x="110" y="24" text-anchor="middle" fill="#1e3a8a">12340</text>
      <text x="210" y="24" text-anchor="middle" fill="#1e3a8a">8</text>
      <text x="300" y="24" text-anchor="middle" fill="#1e3a8a">2</text>
      <text x="400" y="24" text-anchor="middle" fill="#1e3a8a">12330</text>
      <text x="580" y="24" text-anchor="middle" fill="#1e3a8a">90 + 0 - 42 = 48</text>
      <text x="770" y="24" text-anchor="middle" fill="#1e3a8a">760g</text>
      <text x="870" y="24" text-anchor="middle" fill="#1e3a8a">3800</text>
    </g>

    <!-- Day 19 -->
    <g transform="translate(0, 38)">
      <rect x="0" y="0" width="920" height="38" fill="#f9fafb" stroke="#e5e7eb" />
      <text x="30" y="24" text-anchor="middle" font-weight="bold">19</text>
      <text x="110" y="24" text-anchor="middle" fill="#1e3a8a">12330</text>
      <text x="210" y="24" text-anchor="middle" fill="#1e3a8a">6</text>
      <text x="300" y="24" text-anchor="middle" fill="#1e3a8a">1</text>
      <text x="400" y="24" text-anchor="middle" fill="#1e3a8a">12323</text>
      <text x="580" y="24" text-anchor="middle" fill="#1e3a8a">48 + 120 - 45 = 123</text>
      <text x="770" y="24" text-anchor="middle" fill="#1e3a8a">840g</text>
      <text x="870" y="24" text-anchor="middle" fill="#1e3a8a">4050</text>
    </g>

    <!-- Day 20 -->
    <g transform="translate(0, 76)">
      <rect x="0" y="0" width="920" height="38" fill="#ffffff" stroke="#e5e7eb" />
      <text x="30" y="24" text-anchor="middle" font-weight="bold">20</text>
      <text x="110" y="24" text-anchor="middle" fill="#1e3a8a">12323</text>
      <text x="210" y="24" text-anchor="middle" fill="#1e3a8a">7</text>
      <text x="300" y="24" text-anchor="middle" fill="#1e3a8a">2</text>
      <text x="400" y="24" text-anchor="middle" fill="#1e3a8a">12314</text>
      <text x="580" y="24" text-anchor="middle" fill="#1e3a8a">123 + 0 - 46 = 77</text>
      <text x="770" y="24" text-anchor="middle" fill="#1e3a8a">915g</text>
      <text x="870" y="24" text-anchor="middle" fill="#1e3a8a">4140</text>
    </g>

    <!-- Day 21 -->
    <g transform="translate(0, 114)">
      <rect x="0" y="0" width="920" height="38" fill="#f9fafb" stroke="#e5e7eb" />
      <text x="30" y="24" text-anchor="middle" font-weight="bold">21</text>
      <text x="110" y="24" text-anchor="middle" fill="#1e3a8a">12314</text>
      <text x="210" y="24" text-anchor="middle" fill="#1e3a8a">9</text>
      <text x="300" y="24" text-anchor="middle" fill="#1e3a8a">3</text>
      <text x="400" y="24" text-anchor="middle" fill="#1e3a8a">12302</text>
      <text x="580" y="24" text-anchor="middle" fill="#1e3a8a">77 + 0 - 48 = 29</text>
      <text x="770" y="24" text-anchor="middle" fill="#1e3a8a">985g</text>
      <text x="870" y="24" text-anchor="middle" fill="#1e3a8a">4320</text>
    </g>

    <!-- DAY 22: ANOMALY SPIKE ROW -->
    <g transform="translate(0, 152)">
      <rect x="0" y="0" width="920" height="50" fill="#fef2f2" stroke="#b91c1c" stroke-width="2" />
      <text x="30" y="32" text-anchor="middle" font-weight="bold" fill="#b91c1c">22</text>
      <text x="110" y="32" text-anchor="middle" fill="#1e3a8a">12302</text>
      
      <circle cx="210" cy="27" r="18" fill="none" stroke="#b91c1c" stroke-width="2" stroke-dasharray="4,2" />
      <text x="210" y="33" text-anchor="middle" font-weight="bold" fill="#b91c1c" font-size="16">68</text>
      
      <text x="300" y="32" text-anchor="middle" fill="#1e3a8a">6</text>
      <text x="400" y="32" text-anchor="middle" fill="#1e3a8a">12228</text>
      
      <rect x="470" y="10" width="240" height="30" fill="none" stroke="#b91c1c" stroke-width="1.5" stroke-dasharray="4,2" />
      <text x="580" y="30" text-anchor="middle" fill="#b91c1c" font-weight="bold">29 + 75 - 55 = 41 [-8 BAGS]</text>
      
      <text x="770" y="32" text-anchor="middle" fill="#1e3a8a">1025g</text>
      <text x="870" y="32" text-anchor="middle" fill="#b91c1c" font-weight="bold">6800 L</text>
    </g>

    <g transform="translate(40, 210)">
      <text x="0" y="0" font-family="-apple-system, sans-serif" font-size="11" font-weight="bold" fill="#b91c1c">
        * REMARK: 13:30 Tunnel Fan #3 belt slipped. Inside shed temp peaked at 36.8°C. 68 suffocated. Physical feed audit found 41 bags vs 49 expected.
      </text>
    </g>

    <!-- Day 23 -->
    <g transform="translate(0, 226)">
      <rect x="0" y="0" width="920" height="38" fill="#ffffff" stroke="#e5e7eb" />
      <text x="30" y="24" text-anchor="middle" font-weight="bold">23</text>
      <text x="110" y="24" text-anchor="middle" fill="#1e3a8a">12228</text>
      <text x="210" y="24" text-anchor="middle" fill="#1e3a8a">22</text>
      <text x="300" y="24" text-anchor="middle" fill="#1e3a8a">3</text>
      <text x="400" y="24" text-anchor="middle" fill="#1e3a8a">12203</text>
      <text x="580" y="24" text-anchor="middle" fill="#1e3a8a">41 + 0 - 50 = 41</text>
      <text x="770" y="24" text-anchor="middle" fill="#1e3a8a">1090g</text>
      <text x="870" y="24" text-anchor="middle" fill="#1e3a8a">5100</text>
    </g>

    <!-- Day 24 -->
    <g transform="translate(0, 264)">
      <rect x="0" y="0" width="920" height="38" fill="#f9fafb" stroke="#e5e7eb" />
      <text x="30" y="24" text-anchor="middle" font-weight="bold">24</text>
      <text x="110" y="24" text-anchor="middle" fill="#1e3a8a">12203</text>
      <text x="210" y="24" text-anchor="middle" fill="#1e3a8a">11</text>
      <text x="300" y="24" text-anchor="middle" fill="#1e3a8a">1</text>
      <text x="400" y="24" text-anchor="middle" fill="#1e3a8a">12191</text>
      <text x="580" y="24" text-anchor="middle" fill="#1e3a8a">41 + 100 - 52 = 89</text>
      <text x="770" y="24" text-anchor="middle" fill="#1e3a8a">1175g</text>
      <text x="870" y="24" text-anchor="middle" fill="#1e3a8a">4700</text>
    </g>

    <!-- Day 25 -->
    <g transform="translate(0, 302)">
      <rect x="0" y="0" width="920" height="38" fill="#ffffff" stroke="#e5e7eb" />
      <text x="30" y="24" text-anchor="middle" font-weight="bold">25</text>
      <text x="110" y="24" text-anchor="middle" fill="#1e3a8a">12191</text>
      <text x="210" y="24" text-anchor="middle" fill="#1e3a8a">6</text>
      <text x="300" y="24" text-anchor="middle" fill="#1e3a8a">0</text>
      <text x="400" y="24" text-anchor="middle" fill="#1e3a8a">12185</text>
      <text x="580" y="24" text-anchor="middle" fill="#1e3a8a">89 + 0 - 54 = 35</text>
      <text x="770" y="24" text-anchor="middle" fill="#1e3a8a">1260g</text>
      <text x="870" y="24" text-anchor="middle" fill="#1e3a8a">4860</text>
    </g>
  </g>
</svg>
"""

with open("assets/shed_card_mock.svg", "w") as f:
    f.write(shed_card_svg.strip())

# 2. FEED COA (Maize Lot MH-402, 28.4 ppb Aflatoxin)
feed_coa_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1300" width="1000" height="1300" style="background:#ffffff; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
  <rect width="1000" height="1300" fill="#ffffff" />
  <rect x="25" y="25" width="950" height="1250" fill="#ffffff" stroke="#d1d5db" stroke-width="1.5" />

  <g transform="translate(50, 50)">
    <rect x="0" y="0" width="900" height="80" fill="#f9fafb" stroke="#111827" stroke-width="1.5" />
    <text x="20" y="30" font-size="16" font-weight="900" fill="#111827">ANALYTICAL TESTING SERVICES (HYDERABAD) • NABL TC-8492</text>
    <text x="20" y="50" font-size="11" fill="#4b5563">Chemical &amp; Toxicological Testing Laboratory • ISO/IEC 17025:2017 Accredited</text>
    <text x="20" y="68" font-size="10" fill="#6b7280">IDA Nacharam, Hyderabad, Telangana • Report ID: ATS/2026/MH-402</text>
  </g>

  <g transform="translate(50, 145)">
    <rect x="0" y="0" width="900" height="70" fill="#ffffff" stroke="#e5e7eb" />
    <text x="20" y="26" font-size="11" font-weight="bold" fill="#111827">CLIENT: PRODIGY FOODS PVT LTD (HYDERABAD FEED PLANT)</text>
    <text x="20" y="46" font-size="11" fill="#4b5563">Commodity: Yellow Maize (Corn Grain) • Consignment: 42.50 MT (Lot #MH-402)</text>
    <text x="550" y="26" font-size="11" font-weight="bold" fill="#111827">SUPPLIER: Sri Lakshmi Agro Traders (Nizamabad Mandi)</text>
    <text x="550" y="46" font-size="11" fill="#4b5563">Sample Date: 24-Nov-2026 • Vehicle: TS-08-UB-4412 / 4413</text>
  </g>

  <g transform="translate(50, 230)">
    <rect x="0" y="0" width="900" height="34" fill="#111827" />
    <text x="20" y="22" fill="#ffffff" font-size="11" font-weight="bold">TEST PARAMETER</text>
    <text x="320" y="22" fill="#ffffff" font-size="11" font-weight="bold">METHOD</text>
    <text x="500" y="22" fill="#ffffff" font-size="11" font-weight="bold">SPECIFICATION LIMIT</text>
    <text x="700" y="22" fill="#ffffff" font-size="11" font-weight="bold">OBSERVED VALUE</text>
    <text x="830" y="22" fill="#ffffff" font-size="11" font-weight="bold">STATUS</text>

    <!-- Row 1: Aflatoxin B1 Breach -->
    <g transform="translate(0, 34)">
      <rect x="0" y="0" width="900" height="46" fill="#fef2f2" stroke="#fecaca" />
      <text x="20" y="28" font-size="12" font-weight="bold" fill="#b91c1c">Aflatoxin B1 (Mycotoxin)</text>
      <text x="320" y="28" font-size="11" fill="#4b5563">AOAC 991.31 (HPLC)</text>
      <text x="500" y="28" font-size="12" font-weight="bold" fill="#111827">Max 20.0 ppb</text>
      <text x="700" y="28" font-size="14" font-weight="900" fill="#b91c1c">28.4 ppb</text>
      <rect x="820" y="11" width="65" height="24" fill="#fee2e2" stroke="#b91c1c" rx="2" />
      <text x="852" y="27" text-anchor="middle" font-size="10" font-weight="bold" fill="#b91c1c">BREACH</text>
    </g>

    <!-- Row 2: Moisture Breach -->
    <g transform="translate(0, 80)">
      <rect x="0" y="0" width="900" height="46" fill="#fef2f2" stroke="#fecaca" />
      <text x="20" y="28" font-size="12" font-weight="bold" fill="#b91c1c">Moisture Content</text>
      <text x="320" y="28" font-size="11" fill="#4b5563">IS: 4333 (Part II)</text>
      <text x="500" y="28" font-size="12" font-weight="bold" fill="#111827">Max 12.0 %</text>
      <text x="700" y="28" font-size="14" font-weight="900" fill="#b91c1c">13.8 %</text>
      <rect x="820" y="11" width="65" height="24" fill="#fee2e2" stroke="#b91c1c" rx="2" />
      <text x="852" y="27" text-anchor="middle" font-size="10" font-weight="bold" fill="#b91c1c">BREACH</text>
    </g>

    <!-- Row 3: Crude Protein Warning -->
    <g transform="translate(0, 126)">
      <rect x="0" y="0" width="900" height="42" fill="#fffbeb" stroke="#fde68a" />
      <text x="20" y="26" font-size="12" font-weight="bold" fill="#b45309">Crude Protein (CP, N x 6.25)</text>
      <text x="320" y="26" font-size="11" fill="#4b5563">IS: 7874 Kjeldahl</text>
      <text x="500" y="26" font-size="12" font-weight="bold" fill="#111827">Min 8.5 %</text>
      <text x="700" y="26" font-size="13" font-weight="bold" fill="#b45309">8.1 %</text>
      <rect x="820" y="9" width="65" height="24" fill="#fef3c7" stroke="#b45309" rx="2" />
      <text x="852" y="25" text-anchor="middle" font-size="10" font-weight="bold" fill="#b45309">WARNING</text>
    </g>

    <!-- Row 4: Damaged Grain Pass -->
    <g transform="translate(0, 168)">
      <rect x="0" y="0" width="900" height="40" fill="#ffffff" stroke="#e5e7eb" />
      <text x="20" y="25" font-size="12" fill="#111827">Damaged / Discolored Grains</text>
      <text x="320" y="25" font-size="11" fill="#4b5563">IS: 4333 Visual</text>
      <text x="500" y="25" font-size="12" fill="#111827">Max 4.0 %</text>
      <text x="700" y="25" font-size="13" font-weight="bold" fill="#15803d">2.2 %</text>
      <rect x="820" y="8" width="65" height="24" fill="#f0fdf4" stroke="#15803d" rx="2" />
      <text x="852" y="24" text-anchor="middle" font-size="10" font-weight="bold" fill="#15803d">PASS</text>
    </g>
  </g>

  <!-- Big Red Quarantine Box -->
  <g transform="translate(50, 480)">
    <rect x="0" y="0" width="900" height="70" fill="#fef2f2" stroke="#b91c1c" stroke-width="2" />
    <text x="450" y="30" text-anchor="middle" font-size="16" font-weight="900" fill="#b91c1c">CONSIGNMENT DISPOSITION: QUARANTINE / REJECTED</text>
    <text x="450" y="50" text-anchor="middle" font-size="11" font-weight="bold" fill="#b91c1c">DO NOT UNLOAD INTO SILOS • REQUIRES FORMAL QC DIRECTOR WRITTEN OVERRIDE</text>
  </g>
</svg>
"""

with open("assets/feed_mill_coa_mock.svg", "w") as f:
    f.write(feed_coa_svg.strip())

# 3. OEM CONTROLLER TELEMETRY GRAPH (Dhumal SmartVent EC-800)
oem_telemetry_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1300" width="1000" height="1300" style="background:#ffffff; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
  <rect width="1000" height="1300" fill="#ffffff" />
  <rect x="25" y="25" width="950" height="1250" fill="#ffffff" stroke="#d1d5db" stroke-width="1.5" />

  <!-- Controller Header -->
  <g transform="translate(50, 50)">
    <rect x="0" y="0" width="900" height="80" fill="#111827" />
    <text x="20" y="32" font-size="18" font-weight="900" fill="#ffffff">DHUMAL SMARTVENT EC-800 • HOURLY SENSOR &amp; ALARM AUDIT</text>
    <text x="20" y="54" font-size="11" fill="#9ca3af">Farm ID: Sri Balaji Shed 04 (Siddipet Zone) • Firmware: v4.2.1 • Date: 2026-11-24 (Day 22)</text>
  </g>

  <!-- Incident Timeline Graph Header -->
  <g transform="translate(50, 150)">
    <rect x="0" y="0" width="900" height="340" fill="#f9fafb" stroke="#e5e7eb" />
    <text x="20" y="30" font-size="13" font-weight="bold" fill="#111827">Day 22 Hourly Thermal &amp; Static Pressure Curve (Tunnel Ventilation)</text>
    
    <!-- Y-Axis labels -->
    <text x="20" y="70" font-size="10" fill="#b91c1c" font-weight="bold">38°C</text>
    <line x1="60" y1="65" x2="880" y2="65" stroke="#fecaca" stroke-dasharray="3,3" />
    
    <text x="20" y="130" font-size="10" fill="#b45309" font-weight="bold">32°C</text>
    <line x1="60" y1="125" x2="880" y2="125" stroke="#fde68a" stroke-dasharray="3,3" />

    <text x="20" y="200" font-size="10" fill="#15803d" font-weight="bold">24°C</text>
    <line x1="60" y1="195" x2="880" y2="195" stroke="#bbf7d0" stroke-width="1.5" />
    <text x="810" y="190" font-size="9" fill="#15803d" font-weight="bold">TARGET SETPOINT</text>

    <!-- Temperature Curve -->
    <path d="M 80 195 L 160 190 L 240 180 L 320 160 L 400 130 L 480 80 L 560 68 L 640 120 L 720 170 L 800 190" 
          fill="none" stroke="#b91c1c" stroke-width="3" />

    <!-- Static Pressure Drop Curve -->
    <path d="M 80 270 L 160 270 L 240 270 L 320 270 L 400 265 L 480 320 L 560 325 L 640 270 L 720 270 L 800 270" 
          fill="none" stroke="#2563eb" stroke-width="2.5" stroke-dasharray="6,3" />

    <!-- Static pressure legend -->
    <text x="60" y="290" font-size="10" fill="#2563eb" font-weight="bold">-- Static Pressure (Normal: 28 Pa)</text>
    <text x="280" y="290" font-size="10" fill="#b91c1c" font-weight="bold">— Inside Temperature (°C)</text>

    <!-- Time labels on X Axis -->
    <text x="80" y="240" font-size="10" fill="#6b7280">08:00</text>
    <text x="240" y="240" font-size="10" fill="#6b7280">10:00</text>
    <text x="400" y="240" font-size="10" fill="#6b7280">12:00</text>
    <text x="480" y="240" font-size="10" fill="#b91c1c" font-weight="bold">13:30 (TRIP)</text>
    <text x="560" y="240" font-size="10" fill="#b91c1c" font-weight="bold">14:00 (36.8°C)</text>
    <text x="640" y="240" font-size="10" fill="#15803d" font-weight="bold">15:00 (REPAIR)</text>
    <text x="800" y="240" font-size="10" fill="#6b7280">18:00</text>

    <!-- Alarm callout -->
    <g transform="translate(440, 75)">
      <rect x="0" y="0" width="220" height="38" fill="#fef2f2" stroke="#b91c1c" stroke-width="1.5" rx="3" />
      <text x="110" y="16" text-anchor="middle" font-size="10" font-weight="bold" fill="#b91c1c">ALARM #04: FAN 3 BELT SLIP</text>
      <text x="110" y="30" text-anchor="middle" font-size="9" fill="#111827">Static Press collapsed to 11 Pa</text>
    </g>
  </g>

  <!-- Correlation Summary Box -->
  <g transform="translate(50, 520)">
    <rect x="0" y="0" width="900" height="110" fill="#fef2f2" stroke="#b91c1c" stroke-width="2" />
    <text x="20" y="30" font-size="14" font-weight="900" fill="#b91c1c">INCIDENT ROOT-CAUSE CORRELATION VERIFIED</text>
    <text x="20" y="55" font-size="12" fill="#111827">1. Controller confirms Fan #3 belt failure at 13:30 caused shed temperature to spike from 28°C to 36.8°C.</text>
    <text x="20" y="75" font-size="12" fill="#111827">2. This mechanical event correlates 1:1 with the 68 bird suffocations reported in the manual shed register.</text>
    <text x="20" y="95" font-size="11" font-weight="bold" fill="#b91c1c">CONCLUSION: Mortality was caused by ventilation mechanical failure, not feed poisoning or pathogen outbreak.</text>
  </g>
</svg>
"""

with open("assets/oem_telemetry_mock.svg", "w") as f:
    f.write(oem_telemetry_svg.strip())

print("All 3 visual docs updated cleanly.")
