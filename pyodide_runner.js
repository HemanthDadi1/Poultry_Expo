/**
 * Pyodide WebAssembly Runner for Browser-side Python Execution
 * Author: Hemanth Dadi
 * 
 * Provides offline-first Python in the browser.
 * If offline or Pyodide CDN unavailable, automatically falls back to rules_engine.js
 * while maintaining 100% deterministic math parity.
 */

class PythonRulesRunner {
  constructor() {
    this.pyodide = null;
    this.isLoaded = false;
    this.isLoading = false;
    this.engineMode = 'offline_js'; // 'pyodide_wasm' or 'offline_js'
    this.pythonCode = null;
  }

  async init(pythonSource) {
    this.pythonCode = pythonSource;
    if (typeof loadPyodide === 'function') {
      try {
        this.isLoading = true;
        console.log("Initializing Pyodide WebAssembly environment...");
        this.pyodide = await loadPyodide();
        if (this.pythonCode) {
          await this.pyodide.runPythonAsync(this.pythonCode);
        }
        this.isLoaded = true;
        this.engineMode = 'pyodide_wasm';
        console.log("Pyodide WebAssembly rules engine active.");
        if (window.onPyodideStatusChange) {
          window.onPyodideStatusChange('pyodide_wasm');
        }
      } catch (err) {
        console.warn("Pyodide init failed or offline, falling back to local deterministic JS engine:", err);
        this.engineMode = 'offline_js';
        if (window.onPyodideStatusChange) {
          window.onPyodideStatusChange('offline_js');
        }
      } finally {
        this.isLoading = false;
      }
    } else {
      console.log("Offline mode: running local deterministic engine.");
      this.engineMode = 'offline_js';
      if (window.onPyodideStatusChange) {
        window.onPyodideStatusChange('offline_js');
      }
    }
  }

  async evaluateBroiler(initialChicks, rows, bagWeight = 50.0, locked = false) {
    if (this.isLoaded && this.pyodide) {
      try {
        const pyArgs = JSON.stringify({ initialChicks, rows, bagWeight, locked });
        const script = `
import json
args = json.loads('''${pyArgs}''')
res = evaluate_broiler_shed_ledger(args['initialChicks'], args['rows'], args['bagWeight'], args['locked'])
json.dumps(res)
`;
        const pyJson = await this.pyodide.runPythonAsync(script);
        return JSON.parse(pyJson);
      } catch (err) {
        console.error("Pyodide exec error, falling back to JS engine:", err);
      }
    }
    // Deterministic fallback
    return evaluateBroilerShedLedger(initialChicks, rows, bagWeight, locked);
  }

  async evaluateCoa(commodity, lotNumber, supplier, testValues, qcApproved = false, overrideReason = "") {
    if (this.isLoaded && this.pyodide) {
      try {
        const pyArgs = JSON.stringify({ commodity, lotNumber, supplier, testValues, qcApproved, overrideReason });
        const script = `
import json
args = json.loads('''${pyArgs}''')
res = evaluate_feed_coa(args['commodity'], args['lotNumber'], args['supplier'], args['testValues'], args['qcApproved'], args['overrideReason'])
json.dumps(res)
`;
        const pyJson = await this.pyodide.runPythonAsync(script);
        return JSON.parse(pyJson);
      } catch (err) {
        console.error("Pyodide exec error, falling back to JS engine:", err);
      }
    }
    // Deterministic fallback
    return evaluateFeedCoa(commodity, lotNumber, supplier, testValues, qcApproved, overrideReason);
  }
}

window.pythonRulesRunner = new PythonRulesRunner();
