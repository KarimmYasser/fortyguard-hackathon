import { driver, DriveStep, Driver } from 'driver.js';
import { ActiveTab } from '../components/Navbar';

export interface TourGuideOptions {
  activeTab: ActiveTab;
  onNavigateTab?: (tab: ActiveTab) => void;
  onOpenLiveScan?: () => void;
  onOpenDatabaseModal?: () => void;
}

type TourAction =
  | { type: 'click'; selector: string }
  | { type: 'open-live-scan' }
  | { type: 'open-database' };

type PreparedStep = DriveStep & {
  element: string;
  data?: {
    action?: TourAction;
    navigateTab?: ActiveTab;
    timeoutMs?: number;
  };
};

const TARGET_TIMEOUT_MS = 30_000;
const CONDITIONAL_TIMEOUT_MS = 60_000;

const step = (
  element: string,
  title: string,
  description: string,
  side: 'top' | 'right' | 'bottom' | 'left' = 'bottom',
  align: 'start' | 'center' | 'end' = 'center',
  action?: TourAction,
  timeoutMs?: number,
): PreparedStep => ({
  element,
  popover: { title, description, side, align },
  data: { action, timeoutMs },
});

const click = (selector: string): TourAction => ({ type: 'click', selector });

const getContentStepsForTab = (tab: ActiveTab): PreparedStep[] => {
  switch (tab) {
    case 'home':
      return [
        step('#tour-navbar-tour-btn', '🧭 Tour Guide', 'This target-aware guide covers all 14 tabs. It waits for lazy modules and API-backed panels before showing a step, so every popover remains anchored.', 'bottom', 'end'),
        step('#tour-hero-header', '🌟 Mission & Architecture', 'Thermal Sentinel Grid couples measured FortyGuard 2-meter environmental boundaries with deterministic grid-asset physics, bounded dispatch, and auditable economics.'),
        step('#tour-video-showcase', '🎬 Pitch & Product Walkthrough', 'Watch the motion-graphics pitch or the recorded live product walkthrough, then use chapter markers to jump to the relevant capability.', 'top'),
        step('#tour-navbar-live-scan', '📡 Live FortyGuard Ingestion', 'Open an on-demand scan for a chosen corridor and catalog date. The live result can then drive the complete physics and economics stack.'),
        step('#tour-navbar-db-modal', '🗄️ Durable Cloud Database', 'Inspect Supabase-backed records, saved scans, deterministic solve replays, credit accounting, and dispatch history.'),
        step('#tour-navbar-mode-toggle', '🛡️ Baseline vs Mitigated', 'Switch the shared dashboard between unmitigated and bounded-action trajectories.'),
        step('#tour-navbar-tabs', '🗂️ Fourteen Platform Views', 'Use the two-row module navigation to open operations, simulation, validation, scientific evidence, orchestration, economics, and analytics views.'),
        step('#tour-launchpad-header', '🚀 Operational Modules', 'The launchpad and navigation expose the grid physics, operations, evidence, and analytics modules.', 'top'),
        step('#tour-card-overview', '⚡ Mission Control', 'Scrub the 12-hour trajectory and compare synchronized thermal, safety, and audit telemetry.', 'top', 'start'),
        step('#tour-card-operations', '🧭 Portfolio Operations', 'Rank registered assets, find candidate crew windows, and retrieve the same deterministic evidence exposed through MCP.', 'top', 'start'),
        step('#tour-card-sandbox', '🎛️ What-If Studio', 'Change environmental and asset assumptions, then persist or replay the complete calculated trajectory.', 'top', 'start'),
        step('#tour-card-72h', '🔥 72h Compounding', 'Inspect three consecutive days from a frozen 72-row live FortyGuard capture driving modelled compounding physics.', 'top', 'start'),
        step('#tour-card-powerflow', '⚡ AC Power Flow', 'Explore the 4-bus forward-backward-sweep model, analytical uncertainty screen, DLR, and cascading hazard views.', 'top', 'start'),
        step('#tour-card-ieee', '🏆 IEEE Annex G', 'Review numerical benchmark comparisons against the published Annex G reference cases.', 'top', 'start'),
        step('#tour-card-ground-truth', '🌡️ Independent Ground Truth', 'Compare timestamp-aligned FortyGuard 2m values with PHX ASOS station observations, including explicit limits on what the comparison establishes.', 'top', 'start'),
        step('#tour-card-academic', '📚 Academic Provenance', 'Inspect the production-indexed research corpus, formulas, filters, and live literature search.', 'top', 'start'),
        step('#tour-card-gis', '🗺️ Hyperlocal 2m GIS', 'View the measured 2m thermal parcel inputs and their spatial spread over the target corridor.', 'top', 'start'),
        step('#tour-card-moats', '🔬 Scientific Moats', 'Review cable-soil, canyon, moisture, and bounded-trajectory safety models.', 'top', 'start'),
        step('#tour-card-agent', '🤖 LangGraph Engine', 'Inspect the five-node orchestration pipeline and optionally execute it to reveal live result panels.', 'top', 'start'),
        step('#tour-card-roi', '💰 Avoided Loss ROI', 'Audit the scenario-modelled loss components, mitigation costs, and ROI assumptions.', 'top', 'start'),
        step('#tour-card-datascience', '📊 Data Science Studio', 'Inspect the Medallion ETL pipeline, polynomial Ridge physics surrogate, spatial OLS regression, anomaly detection, and Weibull survival analysis.', 'top', 'start'),
        step('#tour-disclosure-strip', '✅ Verification & Disclosure', 'Finish the landing page with the automated checks, reproducibility notes, and explicit boundary between measured evidence and modelled outputs.', 'top'),
      ];

    case 'portfolio_operations':
      return [
        step('#tour-operations-header', '🧭 Portfolio Operations', 'Move from a single asset replay to fleet-level thermal triage, candidate field windows, and shared deterministic evidence.'),
        step('#tour-operations-controls', '🎚️ Explicit Screening Policy', 'Adjust wet-bulb, 2 m air-temperature, and consecutive-hour thresholds; recalculation produces a new content-addressed evidence identity.', 'bottom'),
        step('#tour-operations-ranking', '📊 Transparent Risk Ranking', 'Rank registered assets using available environmental and registry evidence. Missing fields are excluded rather than silently imputed.', 'top'),
        step('#tour-worker-window', '👷 Candidate Intervention Window', 'Screen measured wet-bulb and 2 m air temperature against explicit thresholds. This is not presented as OSHA or WBGT certification.', 'top'),
        step('#tour-operations-evidence', '🔐 Content-Addressed Evidence', 'The operator API and MCP tools share one read-only deterministic core and return the same SHA-256 evidence identity.', 'top'),
        step('#tour-coco-generator', '💼 COCO Customer Discovery Engine', 'Synthesize 4-pillar executive proposals (Context, Outcomes, Constraints, Options) across 4 commercial archetypes (Utility, Solar/BESS, Data Center, Hospital).', 'top'),
      ];

    case 'overview':
      return [
        step('#tour-replay-bar', '⏱️ Synchronized 12h Replay', 'Scrub or play the 12-hour heatwave trajectory, step hour by hour, and change playback speed. All thermal, financial, and compliance panels update synchronously.'),
        step('#tour-provenance-panel', '🧾 Evidence Contract', 'Expand this panel to distinguish measured, externally modelled, derived, assumed, simulated, validated, and unvalidated fields—and read the model limitations.', 'bottom'),
        step('#tour-navbar-mode-toggle', '🛡️ Compare Operating Modes', 'Toggle between unmitigated baseline and bounded-action mitigated states without altering boundary conditions.'),
        step('#tour-kpi-grid', '📊 Primary Telemetry Hub', 'High-level executive telemetry summarizing peak temperatures, microclimate offsets, persistence, and net avoided loss.'),
        step('#tour-kpi-hotspot', '🔥 Winding Hot-Spot (T_hs)', 'Monitors transformer winding hot-spot against the IEEE C57.91 140°C emergency insulation breakdown limit.'),
        step('#tour-kpi-microclimate', '🌡️ 2M Microclimate Parcel', 'FortyGuard hyperlocal measured 2m air temperature resolving the measured intra-corridor spread and asphalt heating.'),
        step('#tour-kpi-persistence', '⏳ Thermal Soak Index (TSI)', 'Tracks cumulative hours above 40°C (P40) and degree-hours exceedance (H40) driving insulation loss-of-life.'),
        step('#tour-kpi-roi', '💰 Scenario Economics', 'Review the VoLL-informed avoided-exposure estimate and assumption-based ratio. These are model outputs, not realized savings or certification.'),
        step('#tour-chart-boundary', '📈 Boundary Forcing Chart', 'FortyGuard 2m convective air and solar flux time-series comparing AOI mean vs coolest parcel.'),
        step('#tour-chart-transformer', '⚡ Differential Thermal ODEs', 'IEEE C57.91 / IEC 60076-7 state estimation tracking top-oil and hot-spot temperature evolution.'),
        step('#tour-chart-aging', '📉 Arrhenius Loss-of-Life & BESS', 'Relative aging acceleration V(t) and synchronized BESS state of charge (SoC) peak-shaving dispatch.'),
        step('#tour-safety-gate', '🛡️ Bounded-Trajectory Safety Gate', 'Deterministic mathematical gate verifying ANSI C84.1 voltage, thermal ceilings, and N-1 reliability.'),
        step('#tour-audit-ledger', '📜 Scenario Audit Trail', 'Cryptographically hashed event ledger logging data ingestion, physics solves, and dispatch decisions.'),
      ];

    case 'sandbox':
      return [
        step('#tour-sandbox-header', '🎛️ Live What-If Studio', 'Build a deterministic scenario from explicit environmental, asset, storage, geometry, and cooling assumptions.'),
        step('#tour-sandbox-actions', '⚡ Scenario Presets & Archetypes', 'Apply reproducible presets (Utility Substation, Solar Farm 25MVA, AI Data Center 75MVA, Hospital Feeder 15MVA, Weather Blindspot, Soil Desertification, or Zero-BESS Stress) before fine-tuning.'),
        step('#tour-sandbox-controls', '🎚️ Six Multi-Physics Controls', 'Modulate microclimate spread, heatwave day, BESS capacity, transformer rating, canyon aspect ratio, and forced-cooling state. Each change launches a new solve.'),
        step('#tour-bess-controls', '🔋 BESS Dispatch Inputs', 'Adjust peak discharge power and initial state of charge for the separate two-state battery thermal trajectory.'),
        step('#tour-bess-results', '🌡️ BESS Thermal & Aging Results', 'Inspect core temperature, state of health, SEI degradation, degradation cost, and the 12-hour trajectory.'),
        step('#tour-telemetry-charts', '📈 Rebased Output Trajectory', 'The shared telemetry charts update from the solved sandbox payload; identical full requests can replay from durable storage.', 'top'),
      ];

    case 'multi_day_72h':
      return [
        step('#tour-72h-header', '🔥 72-Hour Live-Capture Replay', 'Three complete consecutive days of frozen live FortyGuard hourly rows provide the environmental boundary for modelled compounding physics.'),
        step('#tour-72h-day-selector', '📅 Day Selector', 'Move between each 24-hour slice while preserving the continuous 72-hour state history.'),
        step('#tour-72h-metrics', '📉 Compounding Effects', 'Compare measured daily extrema with modelled soil dryout, cable temperature, baseline hot spot, and mitigated hot spot.', 'top'),
        step('#tour-72h-provenance', '🧾 72-Hour Evidence Split', 'This strip identifies which 72-hour values came from the frozen FortyGuard capture and which load, soil, and dispatch values are modelled.', 'top'),
        step('#tour-72h-timeline', '🕐 Selected-Day Timeline', 'Inspect all 24 hourly boundary and soil-resistivity steps for the selected day while preserving continuous state across all three days.', 'top'),
      ];

    case 'power_flow':
      return [
        step('#tour-powerflow-header', '⚡ 4-Bus Feeder Analysis', 'The shipped network uses a nonlinear forward-backward sweep, not a 14-bus Newton-Raphson model.'),
        step('#tour-powerflow-subviews', '🧭 Three Grid Views', 'Switch among feeder topology, IEEE 738 dynamic line rating, and cascading-hazard analysis.'),
        step('#tour-cc-opf-controls', '🛡️ Uncertainty-Aware Dispatch Screen', 'Compare deterministic flow with the analytical Gaussian-quantile uncertainty screen and confidence controls.'),
        step('#tour-powerflow-diagram', '🗺️ Single-Line Topology', 'Inspect bus voltage, power injection, line loading, and compliance state.', 'top', 'center', click('#tour-powerflow-tab-topology')),
        step('#tour-powerflow-voltvar', '🎛️ Volt/VAR Controls', 'Tune OLTC position and BESS P/Q support, then inspect the recalculated voltage envelope.', 'top', 'center', click('#tour-powerflow-tab-topology')),
        step('#tour-dlr-panel', '🌬️ IEEE 738 Dynamic Line Rating', 'Switching this tour step opens the DLR view and waits for its panel before highlighting conductor heat balance and ampacity.', 'top', 'center', click('#tour-powerflow-tab-dlr')),
        step('#tour-hazard-gauge', '⚠️ Cascading Hazard', 'The hazard view translates the current operating state into modelled time-dependent cascading-risk indicators.', 'top', 'center', click('#tour-powerflow-tab-hazard')),
      ];

    case 'ground_truth':
      return [
        step('#tour-ground-truth-header', '🌡️ Independent Station Comparison', 'Compare timestamp-aligned FortyGuard urban 2m values against PHX ASOS station observations. Choose the frozen replay or explicitly request an IEM refresh.', 'bottom', 'center', undefined, CONDITIONAL_TIMEOUT_MS),
        { ...step('#tour-ground-truth-interpretation', '🧭 Interpretation Guardrail', 'The observed urban-minus-station contrast is reported descriptively and is not presented as a causal urban heat-island result.'), skipMissingElement: true },
        { ...step('#tour-ground-truth-metrics', '📊 Agreement Metrics', 'Review mean ΔT, Pearson correlation, RMSE, positive-delta hours, pair count, and coverage.'), skipMissingElement: true },
        { ...step('#tour-ground-truth-chart', '📈 Timestamp-Aligned Series', 'Inspect both temperature series and the hourly ΔT bars on one aligned Phoenix-local-time axis.', 'top'), skipMissingElement: true },
        { ...step('#tour-ground-truth-uhi', '⚠️ UHI Limitation', 'Sky Harbor is an urban airport rather than a rural control, so this comparison alone cannot establish an urban heat-island effect.', 'top'), skipMissingElement: true },
        { ...step('#tour-ground-truth-provenance', '🔎 Source & Coverage', 'Confirm evidence class, station distance, selected source, time-zone conversion, coverage, and the environmental-only validation scope.', 'top'), skipMissingElement: true },
      ];

    case 'ieee_annex_g':
      return [
        step('#tour-ieee-header', '📜 IEEE C57.91 Annex G Benchmark', 'Review the repository’s numerical comparison cases and their stated reference tolerances; this is solver regression evidence, not third-party certification.'),
        step('#tour-ieee-clauses', '📑 Standard Test Cases', 'Switch between Clause G.2 (Step Load Response) and Clause G.3 (Diurnal Ambient Cycle).'),
        step('#tour-ieee-metrics', '🔬 Reference Error & Arrhenius', 'Inspect the reported top-oil and hot-spot deviations and the Arrhenius reference value at 110°C.', 'top'),
        step('#tour-ieee-table', '📊 Benchmark Differential Table', 'Detailed hour-by-hour side-by-side comparison between solver state output and IEEE Analytical benchmark values.', 'top'),
      ];

    case 'academic_provenance':
      return [
        step('#tour-academic-header', '📚 Production Research Corpus', 'The application exposes 22 production-indexed records from the broader research pass.'),
        step('#tour-academic-formulas', '📐 Physical Foundations', 'Review the equations that ground the thermal, line-rating, battery, and reliability models.'),
        step('#tour-academic-search', '🔍 Literature Search', 'Run a live arXiv/alphaXiv query without presenting the search result as production model validation.'),
        step('#tour-academic-filters', '🏷️ Domain Filters', 'Filter the indexed corpus by the scientific subsystem you are investigating.', 'top', 'start'),
        step('#tour-academic-cards', '⚡ Paper Records', 'Open source links and copy citations from the returned records.', 'top'),
      ];

    case 'gis_map':
      return [
        step('#tour-gis-header', '🗺️ Hyperlocal 2m GIS', 'The map displays FortyGuard-derived 2m boundary data and clearly separates it from downstream model outputs.'),
        step('#tour-gis-layers', '🧭 Map Layers', 'Switch each parcel between 2m ambient temperature, P40 persistence, and land-cover albedo.', 'bottom'),
        step('#tour-gis-map', '🌡️ Spatial Thermal Parcel', 'Select parcels and inspect same-hour spatial variation over the area of interest; the spread never subtracts extrema from different hours.', 'top'),
        step('#tour-gis-inspector', '🔬 Parcel Physics Inspector', 'Review the selected parcel’s ambient temperature, persistence, degree-hours, albedo, morphology, and interpretation.', 'left'),
        step('#tour-gis-scan-btn', '📡 Open Live Scan', 'Launch a fresh paid/cached FortyGuard scan for a selected corridor.', 'top'),
      ];

    case 'physics_moats':
      return [
        step('#tour-moats-header', '🔬 Four Asymmetric Scientific Moats', 'Deterministic multi-physics coupling mechanisms that standard SCADA and generic LLMs cannot observe.'),
        step('#tour-moats-tabs', '🧭 Moat Subsystem Selector', 'Select among cable-soil dryout, bounded trajectory checks, canyon aerodynamics, and virtual moisture desorption.'),
        step('#tour-moats-cards', '📐 Formula & Telemetry Workspace', 'Each subsystem pairs its explicit mathematical formulation and assumptions with the current scenario output.'),
        step('#tour-moat-1', '⚡ Moat 1: Buried Cable-Soil Dryout', 'IEC 60287 multi-physics modeling showing non-linear soil thermal resistivity surge (0.9 to 2.45 K·m/W) causing cable ampacity bottleneck.', 'top', 'center', click('#tour-moat-tab-1')),
        step('#tour-moat-2', '🛡️ Moat 2: Deterministic Safety Gate', 'A bounded-trajectory model preflight checks thermal, voltage, reserve, and energy limits under forecast uncertainty.', 'top', 'center', click('#tour-moat-tab-2')),
        step('#tour-moat-3', '🏙️ Moat 3: Urban Canyon Aerodynamics', 'Oke canyon fluid dynamics calculating aerodynamic wind sheltering (H/W > 1.5) and 32% convective cooling derate.', 'top', 'center', click('#tour-moat-tab-3')),
        step('#tour-moat-4', '💧 Moat 4: Virtual Moisture Sensor', 'Fickian paper-to-oil moisture desorption tracking dielectric arcing breakdown risk before thermal limits are reached.', 'top', 'center', click('#tour-moat-tab-4')),
      ];

    case 'agent_graph':
      return [
        step('#tour-agent-header', '🤖 Five-Node Orchestration', 'The compiled pipeline coordinates forecast ingest, physical projection, planning, deterministic safety validation, and audit/dispatch.'),
        step('#tour-agent-trigger-btn', '⚡ Execute the Pipeline', 'The tour can execute this action automatically before it visits result-only panels. No popover is shown until the execution completes.'),
        step('#tour-agent-dag', '🔄 Pipeline DAG', 'Select any of the five nodes to inspect forecast ingest, physical projection, planning, deterministic safety validation, or audit/dispatch.', 'top'),
        step('#tour-agent-state', '📦 Node Inspector', 'Review the selected node’s declared inputs, emitted outputs, deterministic or LLM role, and explanatory rationale.', 'top'),
        step('#tour-agent-execution-status', '✅ Live Execution Status', 'This conditional panel appears only after execution starts; the guide triggers the run and waits for it.', 'top', 'center', click('#tour-agent-trigger-btn'), CONDITIONAL_TIMEOUT_MS),
        { ...step('#tour-agent-work-order', '📋 Work Order & Advisory', 'When the API returns dispatch artifacts, inspect the utility work order and citizen advisory here.', 'top', 'center', undefined, CONDITIONAL_TIMEOUT_MS), skipMissingElement: true },
        { ...step('#tour-agent-audit-trail', '📜 Node Transition Trail', 'Inspect the returned node-by-node execution trace and timestamps.', 'top', 'center', undefined, CONDITIONAL_TIMEOUT_MS), skipMissingElement: true },
      ];

    case 'financial_roi':
      return [
        step('#tour-financial-header', '💰 Scenario Economics', 'These are model outputs for the active scenario—not booked savings or a regulatory guarantee.'),
        step('#tour-financial-breakdown', '💵 Economic Components', 'Audit modeled avoided consequence exposure, capital-aging deferral, mitigation expense, and the resulting assumption-based ratio.', 'top'),
        step('#tour-financial-matrix', '📊 Comparative Matrix', 'Compare alternatives and inspect how active scenario inputs change avoided loss and ROI.', 'top'),
      ];

    case 'data_science':
      return [
        step('#tour-data-science-header', '📊 Data Science Studio', 'Explore the Bronze→Silver→Gold feature pipeline and analytics derived from the scenario records.'),
        step('#tour-data-science-tabs', '🧭 Analytics Workbench', 'Six API-backed sections cover EDA, empirical correlations, spatial regression (OLS), risk tiers, ML surrogate diagnostics, and temporal patterns.'),
        step('#tour-data-science-eda', '🥉🥈🥇 EDA & Features', 'Review record counts, engineered-feature metadata, null rates, and descriptive statistics.', 'top', 'center', click('#tour-data-science-tab-eda')),
        step('#tour-data-science-correlation', '🔗 Correlation Taxonomy', 'Empirical pairs are ranked separately from derived or structural relationships that are true by construction.', 'top', 'center', click('#tour-data-science-tab-correlation')),
        step('#tour-data-science-spatial', '🗺️ Spatial Regression (OLS)', 'Inspect Ordinary Least Squares regression linking land-cover canopy deficit and canyon height/width ratio to microclimate temperature spread.', 'top', 'center', click('#tour-data-science-tab-spatial')),
        step('#tour-data-science-risk', '🎯 Risk Distribution', 'Inspect risk tiers and the reported microclimate divergence test with its sample evidence.', 'top', 'center', click('#tour-data-science-tab-risk')),
        step('#tour-data-science-ml', '🧠 Model Diagnostics', 'Review the actual surrogate backend and measured R², MAE, maximum error, anomaly detector, and Weibull assumptions.', 'top', 'center', click('#tour-data-science-tab-ml')),
        step('#tour-data-science-temporal', '⏱️ Temporal Patterns', 'Finish with the hour-by-hour hot-spot, aging, storage, boundary, margin, and loading table.', 'top', 'center', click('#tour-data-science-tab-temporal')),
      ];

    default:
      return [];
  }
};

const DATA_TABS: ActiveTab[] = [
  'overview',
  'portfolio_operations',
  'sandbox',
  'multi_day_72h',
  'power_flow',
  'ieee_annex_g',
  'ground_truth',
  'academic_provenance',
  'gis_map',
  'physics_moats',
  'agent_graph',
  'financial_roi',
  'data_science',
];

const commonDataSteps = (): PreparedStep[] => [
  step('#tour-replay-bar', '⏱️ Shared Scenario Timeline', 'This replay controller remains synchronized across data-backed modules. Play, pause, step, scrub, reset, or change speed without changing the underlying evidence.', 'bottom'),
  step('#tour-provenance-panel', '🧾 Shared Evidence Contract', 'Open this disclosure to separate measured and external inputs from assumptions, derived values, simulations, validation status, and known limitations.', 'bottom'),
];

const stepsForSingleTab = (tab: ActiveTab): PreparedStep[] => {
  const content = getContentStepsForTab(tab);
  if (tab === 'home' || tab === 'portfolio_operations' || tab === 'overview') return content;
  return [...commonDataSteps(), ...content];
};

const withNavigation = (tab: ActiveTab, steps: PreparedStep[]): PreparedStep[] =>
  steps.map((item) => ({ ...item, data: { ...item.data, navigateTab: tab } }));

/** Home launches the complete cross-tab walkthrough; other tabs stay focused. */
const getStepsForTab = (tab: ActiveTab): PreparedStep[] => {
  if (tab !== 'home') return stepsForSingleTab(tab);
  return [
    ...withNavigation('home', getContentStepsForTab('home')),
    ...DATA_TABS.flatMap((targetTab) => withNavigation(targetTab, getContentStepsForTab(targetTab))),
    ...getModalSteps(),
  ];
};

const getModalSteps = (): PreparedStep[] => [
  step('#tour-live-scan-modal', '📡 Live Cloud Scan Hub', 'Choose a corridor and catalog date, inspect usage, and execute a genuine FortyGuard request.', 'bottom', 'center', { type: 'open-live-scan' }),
  step('#tour-live-scan-usage', '🪙 API Usage & Cache', 'Review the account response and available credits. Cached requests avoid repeating identical vendor work.', 'bottom', 'center', { type: 'open-live-scan' }),
  step('#tour-live-scan-presets', '🌍 Preset Corridors', 'Use a known demo corridor or enter custom coordinates and a valid catalog date.', 'bottom', 'center', { type: 'open-live-scan' }),
  step('#tour-live-scan-coordinates', '📍 Scan Boundary', 'Latitude, longitude, city label, and date become part of the persisted scan and deterministic solve identity.', 'top', 'center', { type: 'open-live-scan' }),
  step('#tour-live-scan-analytic', '🌡️ Analytic & Threshold', 'Select the requested FortyGuard analytic and heat threshold. Missing vendor data is surfaced as an error rather than replaced with Phoenix values.', 'top', 'center', { type: 'open-live-scan' }),
  step('#tour-live-scan-execute', '⚡ Execute Live Scan', 'This action can consume credits when no durable cache entry exists. Results are persisted for later Saved Scan replay.', 'top', 'center', { type: 'open-live-scan' }),
  step('#tour-db-modal', '🗄️ Database Audit Hub', 'The guide now switches to durable persistence, saved scans, ledgers, and architecture.', 'bottom', 'center', { type: 'open-database' }),
  step('#tour-db-summary', '📊 Storage Summary', 'Supabase is authoritative in production; local SQLite is a local or warm-container fallback.', 'bottom', 'center', { type: 'open-database' }),
  step('#tour-db-tabs', '🧭 Database Views', 'Move among table counts, saved scans, credit entries, dispatch orders, and storage architecture.', 'bottom', 'center', { type: 'open-database' }),
  step('#tour-db-tables', '🗂️ Persisted Domains', 'Inspect the application’s logical tables and current row counts.', 'top', 'center', click('#tour-db-tab-tables')),
  step('#tour-db-scans', '💾 Saved Scans', 'Select a persisted scan and rerun calculations from its cached hourly evidence without rescanning.', 'top', 'center', click('#tour-db-tab-scans')),
  step('#tour-db-ledger', '🪙 Credit Ledger', 'Review recorded vendor-credit deductions and cache-aware request accounting.', 'top', 'center', click('#tour-db-tab-ledger')),
  step('#tour-db-dispatch', '🛡️ Dispatch History', 'Inspect persisted work orders and their bounded-trajectory safety fields.', 'top', 'center', click('#tour-db-tab-dispatch')),
  step('#tour-db-architecture', '🏗️ Persistence Architecture', 'Review the roles of authoritative Supabase storage and the environment-dependent SQLite fallback.', 'top', 'center', click('#tour-db-tab-architecture')),
];

const isVisible = (element: Element | null): element is HTMLElement => {
  if (!(element instanceof HTMLElement)) return false;
  const rect = element.getBoundingClientRect();
  const style = window.getComputedStyle(element);
  return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
};

const waitForVisibleTarget = (selector: string, timeoutMs: number): Promise<HTMLElement> =>
  new Promise((resolve, reject) => {
    let observer: MutationObserver | null = null;
    let timer = 0;
    let poller = 0;

    const cleanup = () => {
      observer?.disconnect();
      window.clearInterval(poller);
      window.clearTimeout(timer);
    };

    const check = () => {
      const element = document.querySelector(selector);
      if (isVisible(element)) {
        cleanup();
        resolve(element);
      }
    };

    observer = new MutationObserver(check);
    observer.observe(document.documentElement, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ['class', 'style', 'hidden'],
    });
    // Network-backed panels can resolve without a useful DOM mutation in the
    // exact frame we observe. Poll as a fallback for the full timeout window.
    poller = window.setInterval(check, 100);
    timer = window.setTimeout(() => {
      cleanup();
      reject(new Error(`Tour target did not become visible: ${selector}`));
    }, timeoutMs);
    check();
  });

const refreshActiveTarget = (driverObj: Driver) => {
  window.requestAnimationFrame(() => {
    driverObj.refresh();
    // Driver.js can leave the prior element's marker behind when React swaps
    // views during an animated transition. Keep exactly one semantic target.
    document.querySelectorAll('.driver-active-element').forEach((element) => {
      if (element !== driverObj.getActiveElement()) {
        element.classList.remove('driver-active-element', 'driver-no-interaction');
        element.removeAttribute('aria-haspopup');
        element.removeAttribute('aria-expanded');
        element.removeAttribute('aria-controls');
      }
    });
  });
};

const installTargetAwareKeyboardNavigation = (
  driverObj: Driver,
  isUnavailable: () => boolean,
): (() => void) => {
  const onKeyUp = (event: KeyboardEvent) => {
    const target = event.target;
    if (
      target instanceof HTMLElement
      && target.closest('input, textarea, select, [contenteditable="true"]')
    ) return;

    if (event.key === 'Escape') {
      event.preventDefault();
      driverObj.destroy();
      return;
    }

    if (isUnavailable() || driverObj.getActiveIndex() === undefined) return;

    const buttonSelector = event.key === 'ArrowRight'
      ? '.driver-popover-next-btn'
      : event.key === 'ArrowLeft'
        ? '.driver-popover-prev-btn'
        : null;
    if (!buttonSelector) return;

    const button = document.querySelector<HTMLButtonElement>(buttonSelector);
    if (!button || button.disabled) return;
    event.preventDefault();
    button.click();
  };

  // Driver.js keyboard control stays disabled because its built-in arrow
  // handlers call moveTo synchronously. Clicking our rendered controls routes
  // keyboard navigation through the same lazy/API/modal preparation callbacks.
  window.addEventListener('keyup', onKeyUp);
  return () => window.removeEventListener('keyup', onKeyUp);
};

export const startTourGuide = ({
  activeTab,
  onNavigateTab,
  onOpenLiveScan,
  onOpenDatabaseModal,
}: TourGuideOptions) => {
  const steps = getStepsForTab(activeTab);
  if (!steps.length) return;

  let preparing = false;
  let destroyed = false;
  let removeKeyboardNavigation = () => {};

  const runAction = (action?: TourAction) => {
    if (!action) return;
    if (action.type === 'click') {
      const target = document.querySelector(action.selector);
      if (!(target instanceof HTMLElement)) {
        throw new Error(`Tour action target is unavailable: ${action.selector}`);
      }
      if (target instanceof HTMLButtonElement && target.disabled) return;
      target.click();
      return;
    }
    if (action.type === 'open-live-scan') {
      const closeDatabase = document.querySelector('#tour-db-close');
      if (closeDatabase instanceof HTMLElement) closeDatabase.click();
      if (!onOpenLiveScan) throw new Error('The live scan opener is unavailable.');
      onOpenLiveScan();
      return;
    }
    const closeLiveScan = document.querySelector('#tour-live-scan-close');
    if (closeLiveScan instanceof HTMLElement) closeLiveScan.click();
    if (!onOpenDatabaseModal) throw new Error('The database opener is unavailable.');
    onOpenDatabaseModal();
  };

  const prepareAndMove = async (driverObj: Driver, index: number) => {
    if (preparing || destroyed || index < 0 || index >= steps.length) return;
    preparing = true;
    const targetStep = steps[index];

    try {
      // Every step knows its owning tab, so forward and backward navigation
      // both work across section boundaries. Reveal actions (sub-tabs/modals)
      // remain independent and run only when their target is hidden.
      if (targetStep.data?.navigateTab) {
        if (!onNavigateTab) throw new Error('Tab navigation is unavailable.');
        onNavigateTab(targetStep.data.navigateTab);
        // React may not have committed the destination view yet. Waiting for
        // the requested target below is the synchronization point.
      }
      if (!isVisible(document.querySelector(targetStep.element))) {
        // A cross-tab step may also need to reveal a nested subview. Wait for
        // its control to mount after navigation before clicking it.
        if (targetStep.data?.navigateTab && targetStep.data.action?.type === 'click') {
          await waitForVisibleTarget(
            targetStep.data.action.selector,
            targetStep.data?.timeoutMs ?? TARGET_TIMEOUT_MS,
          );
        }
        runAction(targetStep.data?.action);
      }
      await waitForVisibleTarget(targetStep.element, targetStep.data?.timeoutMs ?? TARGET_TIMEOUT_MS);
      if (!destroyed) {
        if (driverObj.getActiveIndex() === undefined) driverObj.drive(index);
        else driverObj.moveTo(index);
        refreshActiveTarget(driverObj);
      }
    } catch (error) {
      console.error(error);
      preparing = false;
      if (targetStep.skipMissingElement && index < steps.length - 1 && !destroyed) {
        void prepareAndMove(driverObj, index + 1);
        return;
      }
      driverObj.destroy();
    } finally {
      preparing = false;
    }
  };

  const driverObj = driver({
    showProgress: true,
    animate: true,
    allowClose: true,
    allowKeyboardControl: false,
    overlayColor: 'rgba(2, 6, 23, 0.88)',
    stagePadding: 8,
    stageRadius: 16,
    popoverClass: 'driverjs-theme',
    nextBtnText: 'Next →',
    prevBtnText: '← Back',
    doneBtnText: 'Finish Tour ✨',
    steps,
    onNextClick: (_element, _activeStep, { driver: instance, index }) => {
      if (index === undefined || index >= steps.length - 1) {
        instance.destroy();
        return;
      }
      void prepareAndMove(instance, index + 1);
    },
    onPrevClick: (_element, _activeStep, { driver: instance, index }) => {
      if (index !== undefined && index > 0) void prepareAndMove(instance, index - 1);
    },
    onDestroyed: () => {
      destroyed = true;
      removeKeyboardNavigation();
    },
  });

  removeKeyboardNavigation = installTargetAwareKeyboardNavigation(
    driverObj,
    () => preparing || destroyed,
  );
  void prepareAndMove(driverObj, 0);
};

export const startPlatformServicesTour = ({
  onOpenLiveScan,
  onOpenDatabaseModal,
}: Pick<TourGuideOptions, 'onOpenLiveScan' | 'onOpenDatabaseModal'>) => {
  const steps = getModalSteps();
  let preparing = false;
  let destroyed = false;
  let removeKeyboardNavigation = () => {};

  const runAction = (action?: TourAction) => {
    if (!action) return;
    if (action.type === 'click') {
      const target = document.querySelector(action.selector);
      if (!(target instanceof HTMLElement)) throw new Error(`Tour action target is unavailable: ${action.selector}`);
      target.click();
    } else if (action.type === 'open-live-scan') {
      const closeDatabase = document.querySelector('#tour-db-close');
      if (closeDatabase instanceof HTMLElement) closeDatabase.click();
      if (!onOpenLiveScan) throw new Error('The live scan opener is unavailable.');
      onOpenLiveScan();
    } else {
      const close = document.querySelector('#tour-live-scan-close');
      if (close instanceof HTMLElement) close.click();
      if (!onOpenDatabaseModal) throw new Error('The database opener is unavailable.');
      onOpenDatabaseModal();
    }
  };

  const prepareAndMove = async (driverObj: Driver, index: number) => {
    if (preparing || destroyed || index < 0 || index >= steps.length) return;
    preparing = true;
    const targetStep = steps[index];

    try {
      if (!isVisible(document.querySelector(targetStep.element))) {
        runAction(targetStep.data?.action);
      }
      await waitForVisibleTarget(targetStep.element, targetStep.data?.timeoutMs ?? TARGET_TIMEOUT_MS);
      if (!destroyed) {
        if (driverObj.getActiveIndex() === undefined) driverObj.drive(index);
        else driverObj.moveTo(index);
        refreshActiveTarget(driverObj);
      }
    } catch (error) {
      console.error(error);
      driverObj.destroy();
    } finally {
      preparing = false;
    }
  };

  const driverObj = driver({
    showProgress: true,
    animate: true,
    allowClose: true,
    allowKeyboardControl: false,
    overlayColor: 'rgba(2, 6, 23, 0.88)',
    stagePadding: 8,
    stageRadius: 16,
    popoverClass: 'driverjs-theme',
    nextBtnText: 'Next →',
    prevBtnText: '← Back',
    doneBtnText: 'Finish Tour ✨',
    steps,
    onNextClick: (_element, _activeStep, { driver: instance, index }) => {
      if (index === undefined || index >= steps.length - 1) {
        instance.destroy();
        return;
      }
      void prepareAndMove(instance, index + 1);
    },
    onPrevClick: (_element, _activeStep, { driver: instance, index }) => {
      if (index !== undefined && index > 0) void prepareAndMove(instance, index - 1);
    },
    onDestroyed: () => {
      destroyed = true;
      removeKeyboardNavigation();
    },
  });

  removeKeyboardNavigation = installTargetAwareKeyboardNavigation(
    driverObj,
    () => preparing || destroyed,
  );

  void prepareAndMove(driverObj, 0);
};
