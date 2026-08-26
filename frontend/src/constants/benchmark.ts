/**
 * Canonical Phoenix benchmark figures — single source of truth for the UI.
 *
 * Every number here is either returned by the live FortyGuard API for the
 * pinned benchmark date (2023-07-19, downtown Phoenix AOI) or computed by our
 * physics solvers from that data. They are reproducible via:
 *
 *   GET /api/v1/replay/phoenix-2023
 *
 * These previously lived as hardcoded literals scattered across ~15 components,
 * which is how the UI ended up displaying a 47.6 °C peak and a 7.17 h
 * persistence that the API never returned. Import from here instead.
 *
 * Regenerate the underlying capture with:
 *   python scripts/regenerate_phoenix_fixture.py
 */

export const BENCHMARK = {
  analysisDate: '2023-07-19',
  location: 'Phoenix, AZ — Downtown Substation TX-04',

  /** Measured 2m convective air temperature (FortyGuard `tcm` analytic). */
  peak2mC: 42.7,
  peak2mF: 108.9,

  /**
   * Natural-terrain reference (South Mountain desert), measured the same hour.
   * NOT an airport station: we probed Sky Harbor and it read *warmer* than
   * downtown (42.78 °C) — an airport ringed by runways is itself a heat island.
   */
  referenceTerrainC: 41.6,
  referenceTerrainLabel: 'South Mountain natural desert (9.5 mi S)',

  /** Measured land-cover delta. Was previously asserted as +4.5 °C. */
  microclimateDeltaC: 1.1,

  /** Persistence & exceedance — the real story. */
  persistenceHoursP40: 12.0,
  exceedanceDegreeHoursH40: 17.48,
  thermalSoakIndex: 3.68,
  thresholdC: 40,
  nCells: 480,
  consecutiveHeatwaveDays: 24,

  peakSolarWm2: 890,

  /** Physics — baseline (no mitigation). */
  baseline: {
    topOilC: 128.3,
    hotSpotC: 159.5,
    agingAccelerationX: 88.4,
    lossOfLifeHours: 377.8,
    failureProbabilityPct: 90.8,
  },

  /** Physics — after deterministic safety-gated mitigation. */
  mitigated: {
    topOilC: 95.5,
    hotSpotC: 122.5,
    agingAccelerationX: 3.45,
    lossOfLifeHours: 12.4,
    failureProbabilityPct: 1.13,
  },

  /** IEEE C57.91 emergency ceiling. */
  hotSpotLimitC: 140,

  avoidedAgingHours: 365.4,
  netAvoidedLossUsd: 2566193,
  roiMultiple: 5472.6,
  outageConsequenceUsd: 2860000,
} as const;

/** Peak hot-spot reduction attributable to the agent, in °C. */
export const HOT_SPOT_REDUCTION_C = Number(
  (BENCHMARK.baseline.hotSpotC - BENCHMARK.mitigated.hotSpotC).toFixed(1),
); // 37.0

export type DataSource = 'fortyguard_live' | 'fortyguard_live_partial' | 'phoenix_fixture';

export const DATA_SOURCE_LABEL: Record<DataSource, string> = {
  fortyguard_live: 'Live FortyGuard API',
  fortyguard_live_partial: 'Live (partial — indices from benchmark)',
  phoenix_fixture: 'Cached benchmark replay',
};
