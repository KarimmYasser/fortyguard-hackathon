export interface ScenarioLocation {
  city: string;
  state: string;
  latitude: number;
  longitude: number;
  substation_id: string;
  substation_name: string;
}

/**
 * Where a payload's numbers actually came from. The backend stamps this on
 * every analytics response so the UI can never present fixture data as live.
 */
export type DataSourceTag = 'fortyguard_live' | 'fortyguard_live_partial' | 'phoenix_fixture';
export type EvidenceKind = 'measured' | 'externally_modelled' | 'derived' | 'assumed' | 'simulated' | 'validated' | 'unvalidated';

export interface SimulationProvenance {
  schema_version: string;
  model_version: string;
  operating_mode: 'demo' | 'hybrid' | 'operational';
  scenario_id: string;
  boundary_source: string;
  evidence: Array<{ field: string; kind: EvidenceKind; source: string; note?: string }>;
  validation_status: 'environment_only' | 'partially_validated' | 'unvalidated';
  limitations: string[];
}

export interface PersistenceMetrics {
  threshold_c: number;
  persistence_hours_p40: number;
  /** Hours above threshold, straight from the `exceedance` analytic. */
  exceedance_hours_e40?: number;
  exceedance_degree_hours_h40: number;
  thermal_soak_index_tsi: number;
  consecutive_heatwave_days: number;
  /** Tile count backing the persistence statistic. */
  n_cells?: number;
  analysis_date?: string;
  data_source?: DataSourceTag;
}

export interface UrbanCanyonMetrics {
  height_to_width_ratio_hw: number;
  frontal_area_density_lambda_f: number;
  canyon_albedo: number;
  morphological_sheltering_kappa: number;
  cooling_derate_eta_cool: number;
}

export interface SoilCableMetrics {
  volumetric_soil_moisture_theta_v: number;
  critical_moisture_theta_crit: number;
  soil_thermal_resistivity_rho_dry: number;
  soil_thermal_resistivity_rho_wet: number;
  current_rho_soil: number;
  cable_ampacity_derate: number;
}

export interface ScenarioMetadata {
  scenario_id: string;
  name: string;
  location: ScenarioLocation;
  date_range: {
    start_date: string;
    end_date: string;
    filter_type: number;
  };
  persistence_metrics: PersistenceMetrics;
  urban_canyon_metrics: UrbanCanyonMetrics;
  soil_cable_metrics: SoilCableMetrics;
}

export interface TimelineStep {
  hour_index: number;
  timestamp: string;
  time_label: string;
  
  // Boundary Condition
  /**
   * Coolest tile in the AOI. Named for historical reasons — this is NOT an
   * airport station reading. Sky Harbor measures *warmer* than downtown.
   */
  coolest_tile_2m_c: number;
  fortyguard_2m_ambient_c: number;
  /** Measured spatial spread within the AOI (mean − min), not an assumed constant. */
  intra_aoi_spread_c: number;
  solar_irradiance_w_m2: number;
  /** Hottest tile in the AOI — what the most exposed asset actually sees. */
  tile_peak_2m_c?: number;
  relative_humidity_pct?: number;
  wet_bulb_temp_c?: number;
  heat_index_c?: number;
  cloud_cover_pct?: number;
  data_source?: DataSourceTag;
  
  // Internal State
  baseline_top_oil_c: number;
  baseline_hot_spot_c: number;
  mitigated_top_oil_c: number;
  mitigated_hot_spot_c: number;
  top_oil_ceiling_c: number;
  hot_spot_ceiling_c: number;

  // Aging & Loading
  baseline_aging_factor_v: number;
  mitigated_aging_factor_v: number;
  baseline_cumulative_aging_hours: number;
  mitigated_cumulative_aging_hours: number;
  baseline_load_k: number;
  mitigated_load_k: number;
  bess_soc_pct: number;
}

export interface TrajectorySummary {
  peak_top_oil_c: number;
  peak_hot_spot_c: number;
  peak_aging_acceleration_v: number;
  total_loss_of_life_hours: number;
  breached_emergency_ceiling: boolean;
  avoided_loss_of_life_hours?: number;
}

export interface SafetyGateVerdict {
  status: "ACCEPT" | "MODIFY" | "REJECT";
  is_safe: boolean;
  hot_spot_compliant: boolean;
  top_oil_compliant: boolean;
  voltage_compliant: boolean;
  n_minus_one_compliant: boolean;
  bess_reserve_compliant: boolean;
  projected_peak_hot_spot_c: number;
  projected_peak_top_oil_c: number;
  voltage_pu_min: number;
  voltage_pu_max: number;
  bess_min_soc_pct: number;
  nominal_load_k: number;
  safe_max_load_k: number;
  violations: string[];
  mitigation_adjustments: string[];
  barrier_slack_delta: number;
  audit_timestamp: string;
}

export interface EconomicEvaluation {
  total_outage_consequence_usd: number;
  baseline_failure_probability_pct: number;
  mitigated_failure_probability_pct: number;
  avoided_outage_risk_usd: number;
  avoided_aging_hours: number;
  capital_aging_deferral_usd: number;
  mitigation_cost_usd: number;
  net_avoided_loss_usd: number;
  roi_multiple: number;
}

export interface SoilCableState {
  volumetric_moisture_theta_v: number;
  soil_thermal_resistivity_rho_soil: number;
  cable_ampacity_derate: number;
  cable_conductor_temp_c: number;
  cable_margin_c: number;
  transformer_hot_spot_margin_c: number;
  compound_site_margin_c: number;
  is_cable_bottleneck: boolean;
}

export interface VirtualMoistureState {
  paper_moisture_pct: number;
  oil_moisture_ppm: number;
  oil_saturation_limit_ppm: number;
  relative_saturation_rs_oil: number;
  dielectric_breakdown_probability: number;
  dielectric_alarm: boolean;
  dielectric_status: string;
}

export interface HeatmapFeature {
  type: "Feature";
  geometry: {
    type: "Polygon";
    coordinates: number[][][];
  };
  properties: {
    tile_id: string;
    ambient_temp_c: number;
    ambient_temp_f: number;
    persistence_hours_p40: number;
    exceedance_degree_hours: number;
    land_cover: string;
    albedo: number;
    asset_present: string;
  };
}

export interface HeatmapCollection {
  type: "FeatureCollection";
  features: HeatmapFeature[];
}

export interface ReplayDataset {
  scenario_metadata: ScenarioMetadata;
  provenance: SimulationProvenance;
  timeline_steps: TimelineStep[];
  baseline_summary: TrajectorySummary;
  mitigated_summary: TrajectorySummary;
  safety_gate_verdict: SafetyGateVerdict;
  economic_evaluation: EconomicEvaluation;
  soil_cable_state: SoilCableState;
  virtual_moisture_state: VirtualMoistureState;
  urban_canyon_state: Record<string, any>;
  sensitivity_analysis?: Record<string, any>;
  integrated_grid_evaluation?: Record<string, any>;
  heatmap_geojson_tiles: HeatmapCollection;
}
