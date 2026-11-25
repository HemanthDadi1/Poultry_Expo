/**
 * Poultry India Expo 2026 - Deterministic Rules Engine (JS Parity)
 * Engineering Axiom: "AI reads. People confirm. Rules decide."
 * Author: Hemanth Dadi
 * 
 * Exact 1-to-1 deterministic parity with rules_engine.py.
 * Guaranteed 100% offline execution with zero network dependency.
 */

const COBB_500_BENCHMARK = {
  1:  { target_weight_g: 42,   cum_feed_g: 18,   target_fcr: 0.85, max_daily_mort_pct: 0.20 },
  7:  { target_weight_g: 195,  cum_feed_g: 190,  target_fcr: 0.97, max_daily_mort_pct: 0.15 },
  14: { target_weight_g: 485,  cum_feed_g: 585,  target_fcr: 1.20, max_daily_mort_pct: 0.12 },
  18: { target_weight_g: 760,  cum_feed_g: 1000, target_fcr: 1.31, max_daily_mort_pct: 0.12 },
  20: { target_weight_g: 905,  cum_feed_g: 1240, target_fcr: 1.37, max_daily_mort_pct: 0.12 },
  21: { target_weight_g: 980,  cum_feed_g: 1370, target_fcr: 1.40, max_daily_mort_pct: 0.12 },
  22: { target_weight_g: 1060, cum_feed_g: 1500, target_fcr: 1.41, max_daily_mort_pct: 0.12 },
  23: { target_weight_g: 1145, cum_feed_g: 1640, target_fcr: 1.43, max_daily_mort_pct: 0.12 },
  24: { target_weight_g: 1230, cum_feed_g: 1790, target_fcr: 1.45, max_daily_mort_pct: 0.12 },
  25: { target_weight_g: 1320, cum_feed_g: 1945, target_fcr: 1.47, max_daily_mort_pct: 0.12 },
  28: { target_weight_g: 1610, cum_feed_g: 2450, target_fcr: 1.52, max_daily_mort_pct: 0.12 },
  35: { target_weight_g: 2360, cum_feed_g: 3780, target_fcr: 1.60, max_daily_mort_pct: 0.12 },
  42: { target_weight_g: 3120, cum_feed_g: 5350, target_fcr: 1.71, max_daily_mort_pct: 0.12 },
};

function getCobbBenchmarkForDay(day) {
  if (COBB_500_BENCHMARK[day]) {
    return COBB_500_BENCHMARK[day];
  }
  const days = Object.keys(COBB_500_BENCHMARK).map(Number).sort((a, b) => a - b);
  if (day <= days[0]) return COBB_500_BENCHMARK[days[0]];
  if (day >= days[days.length - 1]) return COBB_500_BENCHMARK[days[days.length - 1]];

  let lowerDay = days[0];
  let upperDay = days[days.length - 1];
  for (let d of days) {
    if (d <= day) lowerDay = d;
    if (d >= day) {
      upperDay = d;
      break;
    }
  }

  const factor = (day - lowerDay) / (upperDay - lowerDay);
  const low = COBB_500_BENCHMARK[lowerDay];
  const high = COBB_500_BENCHMARK[upperDay];

  return {
    target_weight_g: Math.round((low.target_weight_g + factor * (high.target_weight_g - low.target_weight_g)) * 10) / 10,
    cum_feed_g: Math.round((low.cum_feed_g + factor * (high.cum_feed_g - low.cum_feed_g)) * 10) / 10,
    target_fcr: Math.round((low.target_fcr + factor * (high.target_fcr - low.target_fcr)) * 1000) / 1000,
    max_daily_mort_pct: low.max_daily_mort_pct
  };
}

/**
 * Evaluates broiler daily ledger with strict mass-balance and deterministic thresholds.
 */
function evaluateBroilerShedLedger(initialPlacedChicks, rows, bagWeightKg = 50.0, supervisorLocked = false) {
  const anomalies = [];
  const processedRows = [];

  let cumMortality = 0;
  let cumCulls = 0;
  let cumFeedKg = 0.0;
  let runningBirds = Number(initialPlacedChicks);

  rows.forEach((r, idx) => {
    const day = Number(r.day || idx + 1);
    const mortality = Number(r.mortality || 0);
    const culls = Number(r.culls || 0);

    // Bird mass balance check
    const expectedClosingBirds = runningBirds - mortality - culls;
    const reportedClosingBirds = Number(r.closing_birds !== undefined ? r.closing_birds : expectedClosingBirds);

    if (expectedClosingBirds !== reportedClosingBirds) {
      anomalies.push({
        code: "BIRD_COUNT_MISMATCH",
        severity: "BREACH",
        day: day,
        metric: "closing_birds",
        observed_value: reportedClosingBirds,
        expected_threshold: expectedClosingBirds,
        message: `Day ${day}: Bird tally mismatch! Opening ${runningBirds} - Mort ${mortality} - Culls ${culls} should equal ${expectedClosingBirds}, got ${reportedClosingBirds}.`,
        action_required: "Verify physical count before approving supervisor sign-off."
      });
    }

    // Feed mass balance check
    const openingBags = Number(r.opening_feed_bags || 0);
    const receivedBags = Number(r.feed_bags_received || 0);
    const consumedBags = Number(r.feed_bags_consumed || 0);
    const reportedClosingBags = Number(r.closing_feed_bags !== undefined ? r.closing_feed_bags : (openingBags + receivedBags - consumedBags));
    const expectedClosingBags = openingBags + receivedBags - consumedBags;

    if (expectedClosingBags !== reportedClosingBags) {
      anomalies.push({
        code: "FEED_INVENTORY_DISCREPANCY",
        severity: "BREACH",
        day: day,
        metric: "closing_feed_bags",
        observed_value: reportedClosingBags,
        expected_threshold: expectedClosingBags,
        message: `Day ${day}: Feed inventory discrepancy! ${openingBags} + ${receivedBags} - ${consumedBags} = ${expectedClosingBags} bags expected, but physical count reported ${reportedClosingBags} bags.`,
        action_required: "Inspect farm feed shed for unlogged feed bag leakage, rodent damage, or theft."
      });
    }

    // Accumulate
    cumMortality += mortality;
    cumCulls += culls;
    runningBirds = reportedClosingBirds;

    const dayFeedKg = consumedBags * bagWeightKg;
    cumFeedKg += dayFeedKg;

    const dailyMortPct = initialPlacedChicks > 0 ? (mortality / initialPlacedChicks) * 100.0 : 0.0;
    const cumMortPct = initialPlacedChicks > 0 ? (cumMortality / initialPlacedChicks) * 100.0 : 0.0;

    const benchmark = getCobbBenchmarkForDay(day);
    const maxAllowedDailyMort = benchmark.max_daily_mort_pct;

    if (dailyMortPct > maxAllowedDailyMort) {
      const severity = dailyMortPct > 0.25 ? "BREACH" : "WARNING";
      anomalies.push({
        code: "DAILY_MORTALITY_SPIKE",
        severity: severity,
        day: day,
        metric: "daily_mortality_pct",
        observed_value: Math.round(dailyMortPct * 1000) / 1000,
        expected_threshold: maxAllowedDailyMort,
        message: `Day ${day}: Daily mortality spike of ${mortality} birds (${dailyMortPct.toFixed(2)}%) exceeds limit of ${maxAllowedDailyMort.toFixed(2)}%.`,
        action_required: "Trigger urgent veterinarian site visit. Check ventilation fans and drinker lines."
      });
    }

    const avgBodyWeightG = Number(r.avg_body_weight_g || 0);
    const totalLiveBiomassKg = (runningBirds * avgBodyWeightG) / 1000.0;
    const fcr = totalLiveBiomassKg > 0 ? (cumFeedKg / totalLiveBiomassKg) : 0.0;
    const targetFcr = benchmark.target_fcr;
    const fcrDrift = fcr - targetFcr;

    if (avgBodyWeightG > 0 && fcrDrift > 0.05) {
      const severity = fcrDrift > 0.10 ? "BREACH" : "WARNING";
      anomalies.push({
        code: "FCR_DRIFT_EXCESS",
        severity: severity,
        day: day,
        metric: "fcr_drift",
        observed_value: Math.round(fcr * 1000) / 1000,
        expected_threshold: targetFcr,
        message: `Day ${day}: Cumulative FCR ${fcr.toFixed(3)} deviates from Cobb 500 standard ${targetFcr.toFixed(3)} by +${fcrDrift.toFixed(3)} points.`,
        action_required: "Review feed quality, feeder height wastage, and sub-clinical coccidiosis/enteritis."
      });
    }

    const waterL = Number(r.water_liters || 0);
    const waterFeedRatio = (dayFeedKg > 0 && waterL > 0) ? (waterL / dayFeedKg) : null;
    if (waterFeedRatio !== null) {
      if (waterFeedRatio < 1.4) {
        anomalies.push({
          code: "WATER_INTAKE_DEPRESSED",
          severity: "WARNING",
          day: day,
          metric: "water_feed_ratio",
          observed_value: Math.round(waterFeedRatio * 100) / 100,
          expected_threshold: "1.6 - 2.1",
          message: `Day ${day}: Low water intake (${waterFeedRatio.toFixed(2)} L/kg feed). Check nipple water pressure.`,
          action_required: "Check pressure regulators and flush lines."
        });
      } else if (waterFeedRatio > 2.6) {
        anomalies.push({
          code: "HEAT_STRESS_OR_ENTERITIS",
          severity: "WARNING",
          day: day,
          metric: "water_feed_ratio",
          observed_value: Math.round(waterFeedRatio * 100) / 100,
          expected_threshold: "1.6 - 2.1",
          message: `Day ${day}: Abnormally high water intake (${waterFeedRatio.toFixed(2)} L/kg feed). Indicates heat stress or wet litter risk.`,
          action_required: "Check tunnel ventilation, cool cell pads, and electrolyte dosing."
        });
      }
    }

    processedRows.push({
      day: day,
      opening_birds: Number(r.opening_birds || (runningBirds + mortality + culls)),
      mortality: mortality,
      culls: culls,
      closing_birds: runningBirds,
      daily_mort_pct: Math.round(dailyMortPct * 1000) / 1000,
      cum_mort_pct: Math.round(cumMortPct * 1000) / 1000,
      opening_feed_bags: openingBags,
      feed_bags_received: receivedBags,
      feed_bags_consumed: consumedBags,
      closing_feed_bags: reportedClosingBags,
      day_feed_kg: Math.round(dayFeedKg * 10) / 10,
      cum_feed_kg: Math.round(cumFeedKg * 10) / 10,
      avg_body_weight_g: avgBodyWeightG,
      target_body_weight_g: benchmark.target_weight_g,
      total_live_biomass_kg: Math.round(totalLiveBiomassKg * 100) / 100,
      calculated_fcr: Math.round(fcr * 1000) / 1000,
      target_fcr: targetFcr,
      fcr_drift: Math.round(fcrDrift * 1000) / 1000,
      water_liters: waterL > 0 ? waterL : null,
      water_feed_ratio: waterFeedRatio ? Math.round(waterFeedRatio * 100) / 100 : null,
      notes: r.notes || ""
    });
  });

  const lastRow = processedRows.length > 0 ? processedRows[processedRows.length - 1] : {};
  let overallStatus = "PASS";
  const hasBreach = anomalies.some(a => a.severity === "BREACH");
  const hasWarning = anomalies.some(a => a.severity === "WARNING");

  if (hasBreach) overallStatus = "BREACH";
  else if (hasWarning) overallStatus = "WARNING";

  return {
    status: overallStatus,
    supervisor_locked: supervisorLocked,
    initial_placed_chicks: initialPlacedChicks,
    current_live_birds: runningBirds,
    total_mortality: cumMortality,
    cumulative_mortality_pct: initialPlacedChicks > 0 ? Math.round((cumMortality / initialPlacedChicks) * 10000) / 100 : 0,
    total_feed_consumed_kg: Math.round(cumFeedKg * 10) / 10,
    total_feed_consumed_bags: Math.round((cumFeedKg / bagWeightKg) * 10) / 10,
    current_avg_weight_g: lastRow.avg_body_weight_g || 0,
    target_avg_weight_g: lastRow.target_body_weight_g || 0,
    final_fcr: lastRow.calculated_fcr || 0,
    target_fcr: lastRow.target_fcr || 0,
    fcr_drift: lastRow.fcr_drift || 0,
    anomalies_count: anomalies.length,
    anomalies: anomalies,
    ledger: processedRows
  };
}

/**
 * Evaluates Feed COA against strict procurement specs.
 */
function evaluateFeedCoa(commodityKey, lotNumber, supplierName, testValues, qcApproved = false, overrideReason = "") {
  const specs = {
    yellow_maize: {
      name: "Yellow Maize (Corn Grain)",
      parameters: {
        aflatoxin_b1_ppb: { label: "Aflatoxin B1", unit: "ppb", max: 20.0, critical: true, warning_above: 15.0 },
        moisture_pct: { label: "Moisture", unit: "%", max: 12.0, critical: true, warning_above: 11.5 },
        crude_protein_pct: { label: "Crude Protein (CP)", unit: "%", min: 8.5, critical: false, warning_below: 8.8 },
        damaged_grain_pct: { label: "Damaged / Discolored Grain", unit: "%", max: 4.0, critical: false, warning_above: 3.0 },
        foreign_matter_pct: { label: "Foreign Matter / Dust", unit: "%", max: 1.5, critical: false, warning_above: 1.0 },
        free_fatty_acids_pct: { label: "Free Fatty Acids (FFA)", unit: "%", max: 2.0, critical: false, warning_above: 1.5 }
      }
    }
  };

  const specDef = specs[commodityKey] || specs.yellow_maize;
  const params = specDef.parameters;

  const results = [];
  const anomalies = [];
  let hasCriticalBreach = false;
  let hasWarning = false;

  for (let [paramKey, rules] of Object.entries(params)) {
    const val = testValues[paramKey];
    if (val === undefined || val === null) continue;

    const numVal = Number(val);
    const unit = rules.unit || "";
    const label = rules.label || paramKey;
    const isCritical = Boolean(rules.critical);

    let status = "PASS";
    let breachMsg = "";

    if (rules.max !== undefined && numVal > rules.max) {
      status = "BREACH";
      if (isCritical) hasCriticalBreach = true;
      breachMsg = `${label} of ${numVal} ${unit} exceeds maximum allowed limit of ${rules.max} ${unit}.`;
    } else if (rules.min !== undefined && numVal < rules.min) {
      status = "BREACH";
      if (isCritical) hasCriticalBreach = true;
      breachMsg = `${label} of ${numVal} ${unit} is below minimum required limit of ${rules.min} ${unit}.`;
    } else if (rules.warning_above !== undefined && numVal > rules.warning_above) {
      status = "WARNING";
      hasWarning = true;
      breachMsg = `${label} of ${numVal} ${unit} is in cautionary elevated range (threshold: ${rules.warning_above} ${unit}).`;
    } else if (rules.warning_below !== undefined && numVal < rules.warning_below) {
      status = "WARNING";
      hasWarning = true;
      breachMsg = `${label} of ${numVal} ${unit} is approaching lower limit (threshold: ${rules.warning_below} ${unit}).`;
    }

    if (status === "BREACH" || status === "WARNING") {
      anomalies.push({
        parameter: paramKey,
        label: label,
        value: numVal,
        unit: unit,
        status: status,
        is_critical: isCritical,
        message: breachMsg
      });
    }

    results.push({
      key: paramKey,
      label: label,
      value: numVal,
      unit: unit,
      min_limit: rules.min,
      max_limit: rules.max,
      status: status,
      is_critical: isCritical
    });
  }

  let lotDisposition = "ACCEPTED";
  if (hasCriticalBreach) lotDisposition = "REJECTED_QUARANTINE";
  else if (hasWarning) lotDisposition = "ACCEPT_WITH_PENALTY";

  const approvalBlocked = hasCriticalBreach && (!overrideReason || overrideReason.trim().length < 10);

  return {
    commodity_key: commodityKey,
    commodity_name: specDef.name,
    lot_number: lotNumber,
    supplier_name: supplierName,
    lot_disposition: lotDisposition,
    has_critical_breach: hasCriticalBreach,
    qc_approved: qcApproved,
    approval_blocked: approvalBlocked,
    override_reason: overrideReason,
    anomalies_count: anomalies.length,
    anomalies: anomalies,
    parameters_table: results
  };
}

// Export for browser and node
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    COBB_500_BENCHMARK,
    getCobbBenchmarkForDay,
    evaluateBroilerShedLedger,
    evaluateFeedCoa
  };
}
