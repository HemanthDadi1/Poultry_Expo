/**
 * Poultry India Expo 2026 — Field Inspection Ledger v2 (Anti-AI Slop Compliant)
 * Axiom: "AI reads. People confirm. Rules decide."
 * Author: Hemanth Dadi
 *
 * What's new in v2:
 * - Two-row nav: brand row + big tab strip
 * - Dismissible status banner
 * - Lock confirmation bar with timestamp
 * - Sticky table headers
 * - Draggable pane divider
 * - Portrait-stacked layout fix
 * - clearStagedFile(), handleModalOverlayClick()
 */

// ── Application State ────────────────────────────────────────────────────────
const state = {
  currentVertical: 'broiler',
  broilerData: null,
  feedData: null,
  oemData: null,
  supervisorLocked: false,
  zoomLevel: 1.0,
  showGrounding: true,
  broilerResult: null,
  feedResult: null,
  customDoc: null
};

// ── Realistic Indian Poultry Datasets ────────────────────────────────────────
const EMBEDDED_DATA = {
  broiler: {
    metadata: {
      title: "Broiler Daily Register Card — Batch #14",
      farm_name: "Sri Balaji Farms (Grower #408 — M. Chandraiah)",
      integrator: "ABIS Exports / IB Group (Telangana Division)",
      location: "Siddipet Zone, Telangana",
      chicks_placed: 12500,
      shed_no: "Shed 04 (EC Tunnel)",
      supervisor_name: "K. Sreedhar Rao (ATO — Siddipet Hub)"
    },
    rows: [
      { day: 18, opening_birds: 12340, mortality: 8,  culls: 2, closing_birds: 12330, opening_feed_bags: 90,  feed_bags_received: 0,   feed_bags_consumed: 42, closing_feed_bags: 48, avg_body_weight_g: 760,  water_liters: 3800 },
      { day: 19, opening_birds: 12330, mortality: 6,  culls: 1, closing_birds: 12323, opening_feed_bags: 48,  feed_bags_received: 120, feed_bags_consumed: 45, closing_feed_bags: 123, avg_body_weight_g: 840, water_liters: 4050 },
      { day: 20, opening_birds: 12323, mortality: 7,  culls: 2, closing_birds: 12314, opening_feed_bags: 123, feed_bags_received: 0,   feed_bags_consumed: 46, closing_feed_bags: 77, avg_body_weight_g: 915,  water_liters: 4140 },
      { day: 21, opening_birds: 12314, mortality: 9,  culls: 3, closing_birds: 12302, opening_feed_bags: 77,  feed_bags_received: 0,   feed_bags_consumed: 48, closing_feed_bags: 29, avg_body_weight_g: 985,  water_liters: 4320 },
      // DAY 22: Mortality Spike (68 birds) + 8 Missing Feed Bags
      { day: 22, opening_birds: 12302, mortality: 68, culls: 6, closing_birds: 12228, opening_feed_bags: 29,  feed_bags_received: 75,  feed_bags_consumed: 55, closing_feed_bags: 41, avg_body_weight_g: 1025, water_liters: 6800 },
      { day: 23, opening_birds: 12228, mortality: 22, culls: 3, closing_birds: 12203, opening_feed_bags: 41,  feed_bags_received: 0,   feed_bags_consumed: 50, closing_feed_bags: 41, avg_body_weight_g: 1090, water_liters: 5100 },
      { day: 24, opening_birds: 12203, mortality: 11, culls: 1, closing_birds: 12191, opening_feed_bags: 41,  feed_bags_received: 100, feed_bags_consumed: 52, closing_feed_bags: 89, avg_body_weight_g: 1175, water_liters: 4700 },
      { day: 25, opening_birds: 12191, mortality: 6,  culls: 0, closing_birds: 12185, opening_feed_bags: 89,  feed_bags_received: 0,   feed_bags_consumed: 54, closing_feed_bags: 35, avg_body_weight_g: 1260, water_liters: 4860 }
    ]
  },
  feed: {
    metadata: {
      title: "Certificate of Analysis (COA) — Inward Raw Material",
      feed_mill: "Prodigy Foods Pvt Ltd (Hyderabad Hub)",
      lot_number: "MH-402 (Nizamabad Mandi)",
      supplier_name: "Sri Lakshmi Agro Traders",
      commodity: "yellow_maize",
      consignment_qty_mt: 42.50
    },
    parameters: {
      aflatoxin_b1_ppb: 28.4,
      moisture_pct: 13.8,
      crude_protein_pct: 8.1,
      damaged_grain_pct: 2.2,
      foreign_matter_pct: 1.4,
      free_fatty_acids_pct: 1.6
    }
  },
  oem: {
    device_info: {
      controller_model: "Dhumal SmartVent EC-800",
      farm_id: "SHED_04_SIDDIPET",
      date: "2026-11-24",
      flock_day: 22,
      peak_inside_temp: 36.8,
      min_static_pressure: 11.0
    },
    hourly_telemetry: [
      { time_str: "08:00", inside_temp_c: 26.5, rh_pct: 65, static_pressure_pa: 28, fan_stage: 4 },
      { time_str: "10:00", inside_temp_c: 28.8, rh_pct: 66, static_pressure_pa: 28, fan_stage: 4 },
      { time_str: "12:00", inside_temp_c: 32.5, rh_pct: 68, static_pressure_pa: 27, fan_stage: 5 },
      { time_str: "13:00", inside_temp_c: 35.8, rh_pct: 74, static_pressure_pa: 12, fan_stage: 5 },
      { time_str: "14:00", inside_temp_c: 36.8, rh_pct: 74, static_pressure_pa: 11, fan_stage: 5 },
      { time_str: "15:00", inside_temp_c: 33.5, rh_pct: 70, static_pressure_pa: 26, fan_stage: 4 },
      { time_str: "16:00", inside_temp_c: 29.5, rh_pct: 68, static_pressure_pa: 27, fan_stage: 4 }
    ]
  }
};

// ── Boot ─────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('./sw.js').catch(() => {});
  }

  const docImg = document.getElementById('doc-image');
  const fallbackMsg = document.getElementById('doc-fallback-msg');
  if (docImg && fallbackMsg) {
    docImg.addEventListener('load', () => {
      docImg.style.display = 'block';
      fallbackMsg.style.display = 'none';
    });
    docImg.addEventListener('error', () => {
      docImg.style.display = 'none';
      fallbackMsg.style.display = 'block';
    });
  }

  state.broilerData = JSON.parse(JSON.stringify(EMBEDDED_DATA.broiler));
  state.feedData    = JSON.parse(JSON.stringify(EMBEDDED_DATA.feed));
  state.oemData     = JSON.parse(JSON.stringify(EMBEDDED_DATA.oem));

  setupTouchPinchZoom();
  setupPaneDivider();
  recalculateBroiler();
  recalculateFeed();
  switchVertical('broiler');
});

// ── DRAGGABLE PANE DIVIDER ────────────────────────────────────────────────────
function setupPaneDivider() {
  const divider  = document.getElementById('pane-divider');
  const leftPane = document.querySelector('.left-pane');
  const container = document.querySelector('.split-container');
  if (!divider || !leftPane || !container) return;

  let dragging = false;
  let startX   = 0;
  let startW   = 0;

  divider.addEventListener('mousedown', (e) => {
    dragging = true;
    startX   = e.clientX;
    startW   = leftPane.offsetWidth;
    divider.classList.add('dragging');
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';
  });

  document.addEventListener('mousemove', (e) => {
    if (!dragging) return;
    const delta   = e.clientX - startX;
    const totalW  = container.offsetWidth;
    const newW    = Math.max(280, Math.min(totalW - 300, startW + delta));
    leftPane.style.width = newW + 'px';
    leftPane.style.flex  = 'none';
  });

  document.addEventListener('mouseup', () => {
    if (!dragging) return;
    dragging = false;
    divider.classList.remove('dragging');
    document.body.style.cursor = '';
    document.body.style.userSelect = '';
  });

  // Touch support for drag
  divider.addEventListener('touchstart', (e) => {
    dragging = true;
    startX   = e.touches[0].clientX;
    startW   = leftPane.offsetWidth;
  }, { passive: true });

  document.addEventListener('touchmove', (e) => {
    if (!dragging || e.touches.length !== 1) return;
    const delta = e.touches[0].clientX - startX;
    const totalW = container.offsetWidth;
    const newW = Math.max(280, Math.min(totalW - 300, startW + delta));
    leftPane.style.width = newW + 'px';
    leftPane.style.flex  = 'none';
  }, { passive: true });

  document.addEventListener('touchend', () => { dragging = false; });
}

// ── NATIVE PINCH-TO-ZOOM & PAN ───────────────────────────────────────────────
const BASE_DOC_WIDTH = 580;

function setupTouchPinchZoom() {
  const viewport = document.getElementById('doc-viewport');
  if (!viewport) return;

  let initialDistance = 0;
  let initialScale    = 1;

  viewport.addEventListener('touchstart', (e) => {
    if (e.touches.length === 2) {
      initialDistance = Math.hypot(
        e.touches[0].pageX - e.touches[1].pageX,
        e.touches[0].pageY - e.touches[1].pageY
      );
      initialScale = state.zoomLevel;
    }
  }, { passive: true });

  viewport.addEventListener('touchmove', (e) => {
    if (e.touches.length === 2 && initialDistance > 0) {
      const d = Math.hypot(
        e.touches[0].pageX - e.touches[1].pageX,
        e.touches[0].pageY - e.touches[1].pageY
      );
      state.zoomLevel = Math.max(0.4, Math.min(3.0, initialScale * (d / initialDistance)));
      applyZoom();
    }
  }, { passive: true });

  setTimeout(fitDocWidth, 120);
}

function zoomDoc(delta) {
  state.zoomLevel = Math.max(0.4, Math.min(3.0, state.zoomLevel + delta));
  applyZoom();
}

function resetZoomDoc() {
  state.zoomLevel = 1.0;
  applyZoom();
}

function fitDocWidth() {
  const viewport = document.getElementById('doc-viewport');
  if (viewport && viewport.clientWidth > 0) {
    const availW = Math.max(260, viewport.clientWidth - 32);
    state.zoomLevel = Math.max(0.4, Math.min(2.5, availW / BASE_DOC_WIDTH));
    applyZoom();
  }
}

function applyZoom() {
  const wrapper  = document.getElementById('doc-wrapper');
  const zoomText = document.getElementById('zoom-level-text');
  if (wrapper) {
    wrapper.style.width    = `${Math.round(BASE_DOC_WIDTH * state.zoomLevel)}px`;
    wrapper.style.maxWidth = 'none';
  }
  if (zoomText) {
    zoomText.textContent = `${Math.round(state.zoomLevel * 100)}%`;
  }
}

function toggleGroundingLayer() {
  const chk = document.getElementById('chk-grounding');
  state.showGrounding = chk.checked;
  const wrapper = document.getElementById('doc-wrapper');
  if (wrapper) wrapper.style.filter = state.showGrounding ? 'none' : 'contrast(1.1) grayscale(0.3)';
}

// ── VERTICAL SWITCHER ────────────────────────────────────────────────────────
function switchVertical(vertKey) {
  state.currentVertical = vertKey;
  state.supervisorLocked = false;

  document.querySelectorAll('.vertical-tab-btn').forEach(btn => btn.classList.remove('active'));
  const activeBtn = document.getElementById(`tab-${vertKey}`);
  if (activeBtn) activeBtn.classList.add('active');

  // Reset lock UI without re-rendering yet
  _applyLockStateToDOM();

  // Show banner again when switching tabs
  const banner = document.getElementById('status-banner');
  if (banner) banner.style.display = '';

  if      (vertKey === 'broiler') renderBroilerView();
  else if (vertKey === 'feed')    renderFeedView();
  else if (vertKey === 'oem')     renderOemView();

  // Fit document width to viewport on tab switch
  setTimeout(fitDocWidth, 80);
}

// ── 1. BROILER INTEGRATOR VIEW ───────────────────────────────────────────────
function recalculateBroiler() {
  const placed = state.broilerData.metadata.chicks_placed || 12500;
  state.broilerResult = evaluateBroilerShedLedger(placed, state.broilerData.rows, 50.0, state.supervisorLocked);

  const badge = document.getElementById('badge-broiler-alerts');
  if (badge) {
    badge.textContent    = state.broilerResult.anomalies_count;
    badge.style.display  = state.broilerResult.anomalies_count > 0 ? 'inline-block' : 'none';
  }
}

function renderBroilerView() {
  recalculateBroiler();
  const res = state.broilerResult;

  if (state.customDoc && state.customDoc.vertical === 'broiler') {
    document.getElementById('doc-title-text').textContent = state.customDoc.title;
    document.getElementById('doc-image').src              = state.customDoc.dataUrl;
    document.getElementById('meta-source').textContent    = state.customDoc.source;
  } else {
    document.getElementById('doc-title-text').textContent = 'WhatsApp Shed Register Photo (Shed 04 — Siddipet)';
    document.getElementById('doc-image').src              = 'assets/shed_card_mock.svg';
    document.getElementById('meta-source').textContent    = 'WhatsApp Photo (Siddipet Zone Farm 408)';
  }

  // Banner
  const banner      = document.getElementById('status-banner');
  const bannerTitle = document.getElementById('banner-title');
  const bannerDesc  = document.getElementById('banner-desc');

  if (res.status === 'BREACH') {
    banner.className     = 'status-banner breach';
    bannerTitle.textContent = `CRITICAL BREACH: ${res.anomalies_count} Anomalies Flagged`;
    bannerDesc.textContent  = `Day 22 records an abnormal mortality spike (68 birds, 0.54% vs 0.12% standard) and an unexplained 8-bag feed discrepancy (opening + received − consumed ≠ physical closing).`;
  } else {
    banner.className     = 'status-banner pass';
    bannerTitle.textContent = 'COMPLIANT: All Rules Passed';
    bannerDesc.textContent  = 'All days conform to Cobb 500 breed standards. Mass-balance verified across all days.';
  }

  // KPIs
  _setKpi(1, 'Current Live Birds',   res.current_live_birds.toLocaleString('en-IN'), `Placed: ${res.initial_placed_chicks.toLocaleString('en-IN')} (${res.total_mortality} dead)`, 'kpi-cell');
  _setKpi(2, 'Cumulative Mortality', `${res.cumulative_mortality_pct.toFixed(2)}%`,   'Benchmark: < 1.80%', res.cumulative_mortality_pct > 1.8 ? 'kpi-cell breach' : 'kpi-cell');
  _setKpi(3, 'Feed Consumed',        `${res.total_feed_consumed_bags} Bags`,           `${res.total_feed_consumed_kg.toLocaleString('en-IN')} kg (50 kg/bag)`, 'kpi-cell');
  _setKpi(4, `Calculated FCR (Day ${state.broilerData.rows[state.broilerData.rows.length - 1].day})`,
              res.final_fcr.toFixed(3),
              `Cobb 500 Target: ${res.target_fcr.toFixed(3)} (Drift: ${res.fcr_drift >= 0 ? '+' : ''}${res.fcr_drift.toFixed(3)})`,
              res.fcr_drift > 0.05 ? 'kpi-cell breach' : 'kpi-cell');

  document.getElementById('table-title').textContent = `Extracted Ledger Table (Days ${state.broilerData.rows[0].day} to ${state.broilerData.rows[state.broilerData.rows.length - 1].day})`;
  document.getElementById('oem-chart-section').style.display = 'none';
  renderBroilerTable(res.ledger);
  _applyLockStateToDOM();
}

function renderBroilerTable(ledgerRows) {
  const container = document.getElementById('table-container');
  const locked    = state.supervisorLocked;

  let html = `
    <table class="ledger-table">
      <thead>
        <tr>
          <th>Day</th>
          <th>Opening</th>
          <th>Mort</th>
          <th>Culls</th>
          <th>Closing</th>
          <th>Feed Bags (Opn + Rec − Con = Cls)</th>
          <th>Avg Wt</th>
          <th>Cobb Std</th>
          <th>FCR</th>
          <th>Verdict</th>
        </tr>
      </thead>
      <tbody>
  `;

  ledgerRows.forEach((r, idx) => {
    const isAnomaly = (r.day === 22);
    const fcr = r.calculated_fcr ? r.calculated_fcr.toFixed(3) : '—';
    const inp = (val, field, w) => locked
      ? `<span class="tabular-nums">${val}</span>`
      : `<input type="number" class="table-input tabular-nums" style="width:${w || 58}px;" value="${val}" onchange="updateBroilerRow(${idx},'${field}',this.value)">`;

    html += `
      <tr class="${isAnomaly ? 'row-breach' : ''}" id="row-day-${r.day}">
        <td><strong>Day ${r.day}</strong></td>
        <td class="tabular-nums">${r.opening_birds.toLocaleString('en-IN')}</td>
        <td>${inp(r.mortality, 'mortality', 52)}</td>
        <td>${inp(r.culls, 'culls', 44)}</td>
        <td class="tabular-nums"><strong>${r.closing_birds.toLocaleString('en-IN')}</strong></td>
        <td class="tabular-nums" style="font-size:10px;">
          ${r.opening_feed_bags} + ${r.feed_bags_received} − ${inp(r.feed_bags_consumed, 'feed_bags_consumed', 44)} = ${inp(r.closing_feed_bags, 'closing_feed_bags', 44)}
        </td>
        <td>${inp(r.avg_body_weight_g, 'avg_body_weight_g', 56)} g</td>
        <td class="tabular-nums" style="color:var(--text-muted);">${r.target_body_weight_g}g</td>
        <td class="tabular-nums"><strong>${fcr}</strong></td>
        <td>${isAnomaly ? '<span class="rule-pill breach">BREACH</span>' : '<span class="rule-pill pass">PASS</span>'}</td>
      </tr>
    `;
  });

  html += '</tbody></table>';
  container.innerHTML = html;
}

function updateBroilerRow(rowIdx, field, newVal) {
  if (state.supervisorLocked) return;
  state.broilerData.rows[rowIdx][field] = Number(newVal);
  renderBroilerView();
}

// ── 2. FEED MILL COA VIEW ────────────────────────────────────────────────────
function recalculateFeed() {
  const meta = state.feedData.metadata;
  state.feedResult = evaluateFeedCoa(
    meta.commodity || 'yellow_maize',
    meta.lot_number,
    meta.supplier_name,
    state.feedData.parameters,
    state.supervisorLocked
  );

  const badge = document.getElementById('badge-feed-alerts');
  if (badge) badge.textContent = state.feedResult.anomalies_count;
}

function renderFeedView() {
  recalculateFeed();
  const res = state.feedResult;

  if (state.customDoc && state.customDoc.vertical === 'feed') {
    document.getElementById('doc-title-text').textContent = state.customDoc.title;
    document.getElementById('doc-image').src              = state.customDoc.dataUrl;
    document.getElementById('meta-source').textContent    = state.customDoc.source;
  } else {
    document.getElementById('doc-title-text').textContent = 'Lab COA Scan (Yellow Maize Lot MH-402)';
    document.getElementById('doc-image').src              = 'assets/feed_mill_coa_mock.svg';
    document.getElementById('meta-source').textContent    = 'Scanned Lab PDF (Nizamabad Mandi Inward)';
  }

  const banner      = document.getElementById('status-banner');
  const bannerTitle = document.getElementById('banner-title');
  const bannerDesc  = document.getElementById('banner-desc');

  if (res.has_critical_breach) {
    banner.className     = 'status-banner breach';
    bannerTitle.textContent = 'CRITICAL REJECTION: Aflatoxin B1 Breach (28.4 ppb > 20.0 ppb Limit)';
    bannerDesc.textContent  = 'Consignment Lot MH-402 (42.5 MT) fails BIS safety specification. High moisture (13.8%) indicates active mold risk. Silo discharge locked.';
  } else {
    banner.className     = 'status-banner pass';
    bannerTitle.textContent = 'LOT RELEASE APPROVED';
    bannerDesc.textContent  = 'All parameters conform to procurement tolerances. Ready for batch formulation.';
  }

  _setKpi(1, 'Consignment Qty',  '42.50 MT',                                       '2 Trailers (Nizamabad Mandi)', 'kpi-cell');
  _setKpi(2, 'Aflatoxin B1',     `${state.feedData.parameters.aflatoxin_b1_ppb} ppb`, 'Limit: Max 20.0 ppb', 'kpi-cell breach');
  _setKpi(3, 'Moisture Content', `${state.feedData.parameters.moisture_pct}%`,       'Limit: Max 12.0%',
    state.feedData.parameters.moisture_pct > 12.0 ? 'kpi-cell breach' : 'kpi-cell');
  _setKpi(4, 'Lot Disposition',
    res.has_critical_breach ? 'REJECTED' : 'ACCEPTED',
    res.has_critical_breach ? 'Quarantine Mandated' : 'Silo Release Permitted',
    res.has_critical_breach ? 'kpi-cell breach' : 'kpi-cell');

  document.getElementById('table-title').textContent = 'COA Chemical & Toxin Specification Table';
  document.getElementById('oem-chart-section').style.display = 'none';
  renderFeedTable(res.parameters_table);
  _applyLockStateToDOM();
}

function renderFeedTable(paramRows) {
  const container = document.getElementById('table-container');
  const locked    = state.supervisorLocked;

  let html = `
    <table class="ledger-table">
      <thead>
        <tr>
          <th>Test Parameter</th>
          <th>Observed Value</th>
          <th>Specification Tolerance</th>
          <th>Standard Method</th>
          <th>Critical Flag</th>
          <th>Rule Verdict</th>
        </tr>
      </thead>
      <tbody>
  `;

  paramRows.forEach(p => {
    const isBreach = p.status === 'BREACH';
    const inp = locked
      ? `<span class="tabular-nums">${p.value} ${p.unit}</span>`
      : `<input type="number" step="0.1" class="table-input tabular-nums" style="width:60px;" value="${p.value}" onchange="updateFeedParam('${p.key}',this.value)"> ${p.unit}`;

    html += `
      <tr class="${isBreach ? 'row-breach' : ''}">
        <td><strong>${p.label}</strong></td>
        <td>${inp}</td>
        <td class="tabular-nums">${p.max_limit ? `Max ${p.max_limit} ${p.unit}` : `Min ${p.min_limit} ${p.unit}`}</td>
        <td style="color:var(--text-muted);">${p.key.includes('aflatoxin') ? 'AOAC 991.31 (HPLC)' : 'IS Standard'}</td>
        <td>${p.is_critical ? '<strong style="color:var(--breach-text);">CRITICAL</strong>' : '<span style="color:var(--text-muted);">Standard</span>'}</td>
        <td>${isBreach ? '<span class="rule-pill breach">BREACH</span>' : '<span class="rule-pill pass">PASS</span>'}</td>
      </tr>
    `;
  });

  html += '</tbody></table>';
  container.innerHTML = html;
}

function updateFeedParam(key, val) {
  if (state.supervisorLocked) return;
  state.feedData.parameters[key] = Number(val);
  renderFeedView();
}

// ── 3. OEM SMART SHED VIEW ───────────────────────────────────────────────────
function renderOemView() {
  document.getElementById('doc-title-text').textContent = 'EC-800 Shed Controller Telemetry + Manual Register Correlation';
  document.getElementById('doc-image').src              = 'assets/oem_telemetry_mock.svg';
  document.getElementById('meta-source').textContent    = 'Dhumal EC-800 CSV Telemetry (Siddipet Shed 04)';

  const banner = document.getElementById('status-banner');
  banner.className = 'status-banner breach';
  document.getElementById('banner-title').textContent = 'MECHANICAL EVENT CORRELATION: Day 22 Heat Prostration';
  document.getElementById('banner-desc').textContent  = 'At 13:30, Fan #3 belt slipped, dropping static pressure to 11 Pa. Shed temperature surged to 36.8°C, directly explaining the 68 bird suffocations reported in the manual register.';

  _setKpi(1, 'Peak Shed Temp',      '36.8°C',  'Setpoint: 24.0°C (+12.8°C Spike)',   'kpi-cell breach');
  _setKpi(2, 'Min Static Pressure', '11.0 Pa', 'Normal: 28.0 Pa (Belt Failure)',      'kpi-cell breach');
  _setKpi(3, 'Water Draw (Panting)','6,800 L',  'Baseline: 4,320 L (+57% Surge)',     'kpi-cell breach');
  _setKpi(4, 'Incident Duration',   '115 Min',  'Until Belt Repair at 15:00 IST',     'kpi-cell');

  document.getElementById('table-title').textContent = 'EC-800 Controller Hourly Climate Readings';
  document.getElementById('oem-chart-section').style.display = 'none';
  renderOemTelemetry();
  _applyLockStateToDOM();
}

function renderOemTelemetry() {
  const container = document.getElementById('table-container');
  const items     = state.oemData.hourly_telemetry;

  let html = `
    <table class="ledger-table">
      <thead>
        <tr>
          <th>Time</th>
          <th>Inside Temp</th>
          <th>RH %</th>
          <th>Static Pressure</th>
          <th>Fan Stage</th>
          <th>Status / Incident Alarm</th>
        </tr>
      </thead>
      <tbody>
  `;

  items.forEach(it => {
    const isAlarm = it.inside_temp_c >= 35.0 || it.static_pressure_pa <= 15;
    html += `
      <tr class="${isAlarm ? 'row-breach' : ''}">
        <td><strong>${it.time_str}</strong></td>
        <td class="tabular-nums" style="${it.inside_temp_c >= 35 ? 'color:var(--breach-text);font-weight:700;' : ''}">
          ${it.inside_temp_c}°C
        </td>
        <td class="tabular-nums">${it.rh_pct}%</td>
        <td class="tabular-nums" style="${it.static_pressure_pa <= 15 ? 'color:var(--breach-text);font-weight:700;' : ''}">
          ${it.static_pressure_pa} Pa${it.static_pressure_pa <= 15 ? ' [−17 Pa Drop]' : ''}
        </td>
        <td>Stage ${it.fan_stage}</td>
        <td>
          ${isAlarm ? '<span class="rule-pill alarm">ALARM: FAN 3 BELT SLIP</span>' : '<span class="rule-pill pass">NORMAL</span>'}
        </td>
      </tr>
    `;
  });

  html += '</tbody></table>';
  container.innerHTML = html;
}

// ── HELPER: Set KPI cell ─────────────────────────────────────────────────────
function _setKpi(n, label, value, sub, cellClass) {
  const lbl  = document.getElementById(`kpi-label-${n}`);
  const val  = document.getElementById(`kpi-val-${n}`);
  const s    = document.getElementById(`kpi-sub-${n}`);
  const cell = document.getElementById(`kpi-cell-${n}`);
  if (lbl)  lbl.textContent   = label;
  if (val)  val.textContent   = value;
  if (s)    s.textContent     = sub;
  if (cell) cell.className    = cellClass;
}

// ── SUPERVISOR LOCK ──────────────────────────────────────────────────────────
function toggleSupervisorLock() {
  if (!state.supervisorLocked) {
    if (state.currentVertical === 'feed' && state.feedResult && state.feedResult.has_critical_breach) {
      const reason = prompt('AFLATOXIN B1 EXCEEDS 20.0 PPB — BIS SAFETY LIMIT\n\nEnter mandatory QC Director justification to authorize batch hold override:');
      if (!reason || reason.trim().length < 5) {
        alert('Action cancelled. Batch remains under quarantine hold.');
        return;
      }
    }
    state.supervisorLocked = true;
  } else {
    state.supervisorLocked = false;
  }

  _applyLockStateToDOM();

  if      (state.currentVertical === 'broiler') renderBroilerView();
  else if (state.currentVertical === 'feed')    renderFeedView();
  else if (state.currentVertical === 'oem')     renderOemView();
}

function _applyLockStateToDOM() {
  const btn        = document.getElementById('btn-lock');
  const badge      = document.getElementById('gate-state-badge');
  const card       = document.getElementById('supervisor-card');
  const bar        = document.getElementById('lock-confirmation-bar');
  const ts         = document.getElementById('lock-timestamp');

  if (!btn) return;

  if (state.supervisorLocked) {
    card.classList.add('locked');
    btn.className   = 'btn-lock locked';
    btn.textContent = '🔒 Locked — Tap to Unlock';
    badge.className = 'verification-badge locked';
    badge.textContent = 'VERIFIED & LOCKED';

    if (bar) bar.style.display = '';
    if (ts) {
      const now = new Date();
      ts.textContent = now.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }) + ' IST';
    }
  } else {
    card.classList.remove('locked');
    btn.className   = 'btn-lock unverified';
    btn.textContent = 'Confirm & Lock Batch';
    badge.className = 'verification-badge unverified';
    badge.textContent = 'UNVERIFIED (EDITABLE)';

    if (bar) bar.style.display = 'none';
  }
}

function dismissBanner() {
  const banner = document.getElementById('status-banner');
  if (banner) banner.style.display = 'none';
}

function scrollToAnomalyRow() {
  const row = document.getElementById('row-day-22');
  if (row) row.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// ── TABLET INGESTION WORKFLOW ─────────────────────────────────────────────────
let stagedFile = { dataUrl: null, name: '' };

function openImportModal() {
  document.getElementById('import-modal').classList.add('open');
  renderPresetList();
}

function closeImportModal() {
  document.getElementById('import-modal').classList.remove('open');
}

function handleModalOverlayClick(event, modalId) {
  if (event.target === event.currentTarget) {
    document.getElementById(modalId).classList.remove('open');
  }
}

function handleTabletFileChosen(event, source) {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (e) => {
    stagedFile.dataUrl = e.target.result;
    stagedFile.name    = file.name;

    // Show staged file row
    const row = document.getElementById('staged-file-row');
    const nameEl = document.getElementById('staged-file-name');
    if (row)    row.style.display = '';
    if (nameEl) nameEl.textContent = `✓ ${file.name}`;

    // Auto-detect document type from filename
    const lower = file.name.toLowerCase();
    if (lower.includes('.pdf') || lower.includes('coa') || lower.includes('lab') || lower.includes('maize') || lower.includes('soya')) {
      document.getElementById('ingest-doc-type').value = 'coa';
    } else {
      document.getElementById('ingest-doc-type').value = 'shed_card';
    }
  };
  reader.readAsDataURL(file);

  // Reset input so same file can be re-selected
  event.target.value = '';
}

function clearStagedFile() {
  stagedFile = { dataUrl: null, name: '' };
  const row = document.getElementById('staged-file-row');
  if (row) row.style.display = 'none';
}

function executeTabletIngestion() {
  const prospect  = document.getElementById('ingest-prospect-name').value.trim() || 'Exhibitor Prospect';
  const docType   = document.getElementById('ingest-doc-type').value;
  const flockSize = Number(document.getElementById('ingest-flock-size').value) || 12500;
  const scenario  = document.getElementById('ingest-scenario').value;

  closeImportModal();

  const targetVertical = (docType === 'coa') ? 'feed' : 'broiler';
  const fallbackImg = (docType === 'coa') ? 'assets/feed_mill_coa_mock.svg' : 'assets/shed_card_mock.svg';

  state.customDoc = {
    vertical: targetVertical,
    dataUrl: stagedFile.dataUrl || fallbackImg,
    title: `${prospect} (${docType === 'coa' ? 'Lab COA' : 'Daily Register'})`,
    source: stagedFile.name ? `Attached: ${stagedFile.name}` : 'Tablet Live Ingest'
  };

  if (docType === 'shed_card') {
    state.broilerData.metadata.integrator    = prospect;
    state.broilerData.metadata.chicks_placed = flockSize;
    if (scenario === 'day22_spike') {
      state.broilerData.rows[4].mortality         = 68;
      state.broilerData.rows[4].closing_feed_bags = 41; // 8 bags discrepancy
    } else if (scenario === 'clean_pass') {
      state.broilerData.rows[4].mortality         = 8;
      state.broilerData.rows[4].closing_feed_bags = 49;
    }
    switchVertical('broiler');
  } else {
    state.feedData.metadata.feed_mill = prospect;
    if (scenario === 'aflatoxin_breach' || scenario === 'day22_spike') {
      state.feedData.parameters.aflatoxin_b1_ppb = 28.4;
      state.feedData.parameters.moisture_pct      = 13.8;
    } else if (scenario === 'clean_pass') {
      state.feedData.parameters.aflatoxin_b1_ppb = 12.0;
      state.feedData.parameters.moisture_pct      = 11.0;
    }
    switchVertical('feed');
  }
}

function renderPresetList() {
  const container = document.getElementById('preset-list-container');
  const presets = [
    { type: 'broiler', title: 'ABIS Exports — Shed 04 (12,500 Birds, Day 22 Anomaly)',  tag: 'BROILER' },
    { type: 'feed',    title: 'Prodigy Foods — Lot MH-402 (28.4 ppb Aflatoxin Breach)', tag: 'FEED COA' },
    { type: 'oem',     title: 'Dhumal EC-800 — Day 22 Heat Prostration Event Log',       tag: 'OEM' }
  ];

  container.innerHTML = presets.map(p => `
    <div class="preset-item">
      <span class="preset-name">${p.title}</span>
      <span class="preset-type-tag">${p.tag}</span>
      <button class="btn-preset-load" onclick="loadPreset('${p.type}')">Load</button>
    </div>
  `).join('');
}

function loadPreset(type) {
  state.customDoc = null;
  closeImportModal();
  switchVertical(type);
}

// ── RULES ENGINE MODAL ───────────────────────────────────────────────────────
function openRulesModal() {
  document.getElementById('rules-modal').classList.add('open');
  document.getElementById('code-snippet-box').innerHTML = `<pre><code>## rules_engine.py — Deterministic Validation Engine
## Axiom: AI reads. People confirm. Rules decide.
## Author: Hemanth Dadi

# ─── FCR Calculation ────────────────────────────────────────────────
# FCR = Total Feed Consumed (kg) / Total Live Bird Biomass (kg)
# No LLM predictions. No token sampling. Pure deterministic arithmetic.

def evaluate_broiler_shed_ledger(initial_placed_chicks, rows, bag_weight_kg=50.0):
    cum_mortality   = sum(r['mortality'] for r in rows)
    cum_culls       = sum(r['culls'] for r in rows)
    cum_feed_bags   = sum(r['feed_bags_consumed'] for r in rows)
    cum_feed_kg     = cum_feed_bags * bag_weight_kg
    live_birds      = initial_placed_chicks - cum_mortality - cum_culls
    final_wt_g      = rows[-1]['avg_body_weight_g']
    live_biomass_kg = (live_birds * final_wt_g) / 1000.0
    fcr             = round(cum_feed_kg / live_biomass_kg, 3)
    mort_pct        = round((cum_mortality / initial_placed_chicks) * 100, 2)

    # Mass-balance check: opening + received - consumed == closing
    anomalies = []
    for r in rows:
        expected_closing = r['opening_feed_bags'] + r['feed_bags_received'] - r['feed_bags_consumed']
        if abs(expected_closing - r['closing_feed_bags']) > 1:
            anomalies.append({'day': r['day'], 'discrepancy': expected_closing - r['closing_feed_bags']})
        if (r['mortality'] / initial_placed_chicks) * 100 > 0.15:
            anomalies.append({'day': r['day'], 'issue': 'Mortality spike > 0.15%'})

    return {'fcr': fcr, 'mortality_pct': mort_pct, 'anomalies': anomalies,
            'status': 'BREACH' if anomalies or fcr > 1.52 else 'PASS'}

# ─── Feed COA Spec Check ────────────────────────────────────────────
# BIS Yellow Maize Spec (IS 4483) + FSSAI Aflatoxin Limit

COA_SPECS = {
    'aflatoxin_b1_ppb':   {'max': 20.0,  'critical': True},
    'moisture_pct':       {'max': 12.0,  'critical': True},
    'crude_protein_pct':  {'min': 8.5,   'critical': False},
    'damaged_grain_pct':  {'max': 4.0,   'critical': False},
    'foreign_matter_pct': {'max': 1.5,   'critical': False},
    'free_fatty_acids_pct': {'max': 2.0, 'critical': False},
}

def evaluate_feed_coa(commodity, lot_number, supplier, params):
    results = {}
    for key, spec in COA_SPECS.items():
        value = params.get(key, 0)
        if 'max' in spec:
            status = 'BREACH' if value > spec['max'] else 'PASS'
        else:
            status = 'BREACH' if value &lt; spec['min'] else 'PASS'
        results[key] = {'value': value, 'status': status, 'critical': spec['critical']}

    has_breach = any(v['status'] == 'BREACH' for v in results.values())
    return {'lot': lot_number, 'results': results,
            'disposition': 'REJECT' if has_breach else 'APPROVE'}
</code></pre>`;
}

function closeRulesModal() {
  document.getElementById('rules-modal').classList.remove('open');
}
