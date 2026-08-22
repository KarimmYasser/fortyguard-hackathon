import { driver, DriveStep } from 'driver.js';
import { ActiveTab } from '../components/Navbar';

export interface TourGuideOptions {
  activeTab: ActiveTab;
  onNavigateTab?: (tab: ActiveTab) => void;
  onOpenLiveScan?: () => void;
}

export const startTourGuide = ({
  activeTab,
  onNavigateTab,
  onOpenLiveScan,
}: TourGuideOptions) => {
  const getStepsForTab = (tab: ActiveTab): DriveStep[] => {
    switch (tab) {
      case 'home':
        return [
          {
            element: '#tour-navbar-tour-btn',
            popover: {
              title: '🧭 Universal Interactive Tour Guide',
              description:
                'Welcome to Thermal Sentinel Grid! This interactive tour guide is available across ALL 11 operational tabs to guide you step-by-step through every physics engine, simulation studio, and live API capability.',
              side: 'bottom',
              align: 'end',
            },
          },
          {
            element: '#tour-hero-header',
            popover: {
              title: '🌟 Executive Mission & Architecture',
              description:
                'Thermal Sentinel Grid couples FortyGuard 2-meter microclimate AI with IEEE differential equations and multi-agent dispatch to protect electrical power grids from heatwave thermal runaway.',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-video-showcase',
            popover: {
              title: '🎬 3-Minute Video Showcase & Live Walkthrough',
              description:
                'Watch the official programmatic motion illustration pitch or toggle to the full automated live UI product walkthrough. Jump directly to any timestamp using interactive chapter markers or download high-definition MP4 renders.',
              side: 'top',
              align: 'center',
            },
          },
          {
            element: '#tour-navbar-live-scan',
            popover: {
              title: '📡 FortyGuard Live Cloud Ingestion Hub',
              description:
                'Trigger live, ad-hoc 2-meter microclimate scans directly against FortyGuard tOS Enterprise API with real credit billing and async polling.',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-navbar-mode-toggle',
            popover: {
              title: '🛡️ Baseline vs. Mitigated Mode Switcher',
              description:
                'Switch between unmitigated baseline operation (overheating excursion past 140°C) and physics-bounded proactive mitigation across all dashboard views.',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-launchpad-header',
            popover: {
              title: '🚀 10 Interactive Operational Modules',
              description:
                'Launch directly into all 10 live operational modules across the platform. Click any card or use the top navigation bar to explore.',
              side: 'top',
              align: 'center',
            },
          },
          {
            element: '#tour-card-overview',
            popover: {
              title: '⚡ Tab 2: Mission Control Telemetry',
              description:
                'Scrub through the 12-hour forward forecast timeline and inspect IEEE C57.91 winding hot-spot temperatures in real time.',
              side: 'top',
              align: 'start',
            },
          },
          {
            element: '#tour-card-sandbox',
            popover: {
              title: '🎛️ Tab 3: What-If Physics Studio & BESS',
              description:
                'Modulate ambient temperature spikes, battery storage MWh, and cooling fans with 2-state cell electro-thermal ODEs and sub-15ms re-solving.',
              side: 'top',
              align: 'start',
            },
          },
          {
            element: '#tour-card-72h',
            popover: {
              title: '🔥 Tab 4: 72h Compounding Heatwave',
              description:
                'Continuous 3-day simulation showing night-time thermal soak, soil moisture desertification, and compounding insulation aging.',
              side: 'top',
              align: 'start',
            },
          },
          {
            element: '#tour-card-powerflow',
            popover: {
              title: '⚡ Tab 5: AC Power Flow & Dynamic Line Rating',
              description:
                '4-bus single-line diagram, IEEE 738 DLR dynamic ampacity headroom (+22.5%), catenary sag, and Chance-Constrained SOCP OPF.',
              side: 'top',
              align: 'start',
            },
          },
          {
            element: '#tour-card-ieee',
            popover: {
              title: '🏆 Tab 6: IEEE Annex G Standard Benchmark',
              description:
                'Direct numerical verification against Clause G.2 (Step Load) and Clause G.3 (Diurnal Ramp) standard tables (<0.0001°C error).',
              side: 'top',
              align: 'start',
            },
          },
          {
            element: '#tour-card-academic',
            popover: {
              title: '📚 Tab 7: Academic Provenance & alphaXiv Corpus',
              description:
                '50+ peer-reviewed papers discovered via alphaXiv, Surface Energy Balance PDEs, and live academic literature search.',
              side: 'top',
              align: 'start',
            },
          },
          {
            element: '#tour-card-gis',
            popover: {
              title: '🗺️ Tab 8: Hyperlocal 2m GIS Engine',
              description:
                'Explore 2-meter FortyGuard convective & surface temperatures, resolving the measured +1.1°C asphalt land-cover delta and the 12-hour thermal soak it sustains.',
              side: 'top',
              align: 'start',
            },
          },
          {
            element: '#tour-card-moats',
            popover: {
              title: '🛡️ Tab 9: 4 Asymmetric Scientific Moats',
              description:
                'Underground cable-soil dryout, urban canyon aerodynamic throttling, virtual paper-oil moisture, and CBF-QP barrier.',
              side: 'top',
              align: 'start',
            },
          },
          {
            element: '#tour-card-agent',
            popover: {
              title: '🤖 Tab 10: LangGraph Multi-Agent Stack',
              description:
                'Inspect the 5-node cognitive pipeline with live GPT-5.4 work order synthesis and tamper-evident audit trails.',
              side: 'top',
              align: 'start',
            },
          },
          {
            element: '#tour-card-roi',
            popover: {
              title: '💰 Tab 11: Avoided Loss & ROI Audit',
              description:
                'Audit investment-grade economics with the DOE LBNL ICE model showing $2.74M net savings and 5,835x economic ROI per heatwave event.',
              side: 'top',
              align: 'start',
            },
          },
        ];

      case 'overview':
        return [
          {
            element: '#tour-replay-bar',
            popover: {
              title: '⏱️ 12-Hour Synchronized Replay Scrubber',
              description:
                'Scrub through the historic Phoenix July 2023 heatwave timeline at 1-hour intervals. Notice how all physics telemetry, heat index, and aging metrics synchronize instantly (<10ms).',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-navbar-mode-toggle',
            popover: {
              title: '🛡️ Baseline vs. Mitigated Comparison',
              description:
                'Toggle between Baseline (red) and Mitigated (gold) modes to see how proactive multi-agent dispatch bounds the winding temperature below 140°C.',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-kpi-grid',
            popover: {
              title: '📊 Real-Time Physics & Microclimate KPI Grid',
              description:
                'Examine the four primary telemetry indicators: FortyGuard 2m Ambient Air (42.7°C), Top-Oil Temperature (134.5°C baseline / 84.8°C mitigated), Winding Hot-Spot (165.7°C baseline / 112.2°C mitigated), and Arrhenius Insulation Aging Acceleration (144.3x vs 1.25x).',
              side: 'top',
              align: 'center',
            },
          },
          {
            element: '#tour-telemetry-charts',
            popover: {
              title: '📈 Apache ECharts Synchronized Multi-Axis Telemetry',
              description:
                'Interactive multi-layer physics charts plotting FortyGuard 2m ambient vs natural-terrain reference, top-oil and winding hot-spot rises, and Arrhenius aging factor progression.',
              side: 'top',
              align: 'center',
            },
          },
          {
            element: '#tour-safety-gate',
            popover: {
              title: '🛡️ Robust Control Barrier Function (CBF-QP) Gate',
              description:
                'Non-LLM deterministic quadratic program certifying that the candidate mitigation policy maintains forward-invariance of safe thermal sets and ANSI C84.1 voltage envelopes.',
              side: 'top',
              align: 'center',
            },
          },
          {
            element: '#tour-audit-ledger',
            popover: {
              title: '📜 Tamper-Evident Chronological Audit Ledger',
              description:
                'Full audit trail recording environmental boundary ingestion, physical state estimation, safety gate evaluations, and autonomous dispatch authorizations.',
              side: 'top',
              align: 'center',
            },
          },
        ];

      case 'sandbox':
        return [
          {
            element: '#tour-sandbox-actions',
            popover: {
              title: '⚡ Instant Scenario Stress Presets',
              description:
                'Click one-click stress presets: Phoenix 23 Peak, Station-Weather Blindspot (0°C delta), 31-Day Desertification, or Zero-BESS Stress to instantly reconfigure the environment.',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-sandbox-controls',
            popover: {
              title: '🎛️ Real-Time Multi-Physics Sliders',
              description:
                'Modulate key stress variables: FortyGuard 2m microclimate delta (+1°C to +8°C), heatwave duration, BESS peak shaving capacity (MW), transformer MVA rating, building canyon H/W ratio, and auxiliary cooling fans with sub-15ms re-solving.',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-bess-panel',
            popover: {
              title: '🔋 2-State BESS Electro-Thermal & SEI Engine',
              description:
                'Simulate battery cell core (Tc) vs. surface (Ts) thermal ODEs, internal Joule heating, Arrhenius SEI capacity fade, real-time degradation cost ($/MWh), and enforcement of the 55°C thermal runaway safety barrier.',
              side: 'top',
              align: 'center',
            },
          },
        ];

      case 'multi_day_72h':
        return [
          {
            element: '#tour-72h-header',
            popover: {
              title: '🔥 72-Hour Continuous Compounding Simulation',
              description:
                'Simulates multi-day heat dome persistence over 3 full diurnal cycles (72 continuous hours) to model compounding heat traps and overnight thermal soak.',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-72h-day-selector',
            popover: {
              title: '📅 Day-by-Day Diurnal Progression',
              description:
                'Switch between Day 1, Day 2, and Day 3 to observe progressive soil moisture desertification and exponential heat accumulation.',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-72h-metrics',
            popover: {
              title: '📉 Compounding Asset Degradation Cards',
              description:
                'Visualizes cumulative Arrhenius insulation aging hours accelerating exponentially past normal life expectancy without proactive cooling.',
              side: 'top',
              align: 'center',
            },
          },
        ];

      case 'power_flow':
        return [
          {
            element: '#tour-powerflow-header',
            popover: {
              title: '⚡ 4-Bus AC Distribution Feeder Power Flow',
              description:
                'Non-linear forward-backward sweep AC power flow and Second-Order Cone CC-OPF calculating active & reactive power (P, Q), bus voltages (V, theta), line losses, and dynamic ratings in real time.',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-cc-opf-controls',
            popover: {
              title: '🛡️ Chance-Constrained SOCP OPF Formulation',
              description:
                'Toggle between Deterministic AC Power Flow and Chance-Constrained SOCP OPF with 90%, 95%, or 99% confidence guarantees under FortyGuard microclimate temperature uncertainty.',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-powerflow-diagram',
            popover: {
              title: '🗺️ Interactive Single-Line Diagram Topology',
              description:
                'Visual distribution network layout with probabilistic voltage intervals [V_min, V_max], active power injections, and thermal compliance status per bus.',
              side: 'top',
              align: 'center',
            },
          },
          {
            element: '#tour-powerflow-voltvar',
            popover: {
              title: '🎛️ Dynamic Volt/VAR & OLTC Optimization',
              description:
                'Tune On-Load Tap Changer (OLTC) tap steps and BESS reactive power injection to maintain ANSI C84.1 voltage compliance (0.95–1.05 pu).',
              side: 'top',
              align: 'center',
            },
          },
        ];

      case 'ieee_annex_g':
        return [
          {
            element: '#tour-ieee-header',
            popover: {
              title: '📜 IEEE Std C57.91-2011 Annex G Benchmark',
              description:
                'Direct mathematical verification against official IEEE standards tables: Annex G.2 (Step-Load Response) and Annex G.3 (Diurnal Ambient Ramp).',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-ieee-table',
            popover: {
              title: '🔬 <0.0001°C Exact Numerical Precision Table',
              description:
                'Side-by-side comparison table proving our Python numerical ODE solver matches the IEEE published standard ground truth with zero mathematical drift.',
              side: 'top',
              align: 'center',
            },
          },
        ];

      case 'academic_provenance':
        return [
          {
            element: '#tour-academic-header',
            popover: {
              title: '📚 Peer-Reviewed Scientific Provenance',
              description:
                'Discover 50+ peer-reviewed papers and preprints grounding FortyGuard’s thermal downscaling, cool pavement physics, Dynamic Line Rating (IEEE 738), BESS degradation, Weibull hazards, and CC-OPF dispatch.',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-academic-formulas',
            popover: {
              title: '📐 Surface Energy Balance & Physical Foundations',
              description:
                'Inspect the foundational PDEs: Surface Energy Balance (SEB), Dynamic Line Rating heat balance, Battery 2-state thermal ODEs, and Arrhenius-Weibull hazard integrals rendered in KaTeX.',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-academic-search',
            popover: {
              title: '🔍 Live arXiv & alphaXiv Research Engine',
              description:
                'Type any research query (e.g., "dynamic line rating", "battery degradation", "chance constrained OPF") to execute real-time searches across arXiv and alphaXiv.',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-academic-filters',
            popover: {
              title: '🏷️ Specialized Domain Filters',
              description:
                'Filter papers by specialized domains: Dynamic Line Rating (IEEE 738), BESS Electro-Thermal, Arrhenius-Weibull Risk, Chance-Constrained OPF, Cool Pavements, and PINNs.',
              side: 'top',
              align: 'start',
            },
          },
          {
            element: '#tour-academic-cards',
            popover: {
              title: '⚡ Interactive Citations & alphaXiv Discussions',
              description:
                'Click "alphaXiv Discuss" to explore community discussions, read full PDFs, or click "IEEE Cite" to copy publication-ready citations.',
              side: 'top',
              align: 'center',
            },
          },
        ];

      case 'gis_map':
        return [
          {
            element: '#tour-gis-header',
            popover: {
              title: '🗺️ Hyperlocal 2m Microclimate GIS Engine',
              description:
                'Interactive geospatial map rendering 2-meter FortyGuard thermal rasters over urban substation corridors at 60m spatial resolution.',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-gis-map',
            popover: {
              title: '🌡️ Resolving the 12-Hour Asphalt Thermal Soak',
              description:
                'Demonstrates why generic station weather fails: it reports a peak, not a duration. Dark asphalt and heat canyons hold 2m air above 40°C for 12 unbroken hours — a measured +1.1°C over natural desert terrain, sustained long enough to age insulation 144x faster.',
              side: 'top',
              align: 'center',
            },
          },
          {
            element: '#tour-gis-scan-btn',
            popover: {
              title: '📡 Live FortyGuard Cloud API Parcel Scan',
              description:
                'Trigger on-demand 2-meter scans against FortyGuards live cloud API for any coordinates or target corridor.',
              side: 'top',
              align: 'center',
            },
          },
        ];

      case 'physics_moats':
        return [
          {
            element: '#tour-moats-header',
            popover: {
              title: '🔬 4 Asymmetric Scientific Moats',
              description:
                'Deep-dive into the four core physics-constrained models that separate Thermal Sentinel Grid from black-box AI wrappers.',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-moats-cards',
            popover: {
              title: '📐 Coupled Multi-Physics Formulations',
              description:
                'Explore IEC 60287 underground soil dryout, Urban Canyon fluid dynamics, Virtual Moisture Sensor ODEs, and Control Barrier Function (CBF-QP) safety guarantees.',
              side: 'top',
              align: 'center',
            },
          },
        ];

      case 'agent_graph':
        return [
          {
            element: '#tour-agent-header',
            popover: {
              title: '🤖 LangGraph Multi-Agent Architecture',
              description:
                'Official compiled StateGraph coordinating 5 nodes: forecast ingestion, physical projection, mitigation planning, safety barrier gating, and live GPT-5.4 narrative synthesis.',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-agent-trigger-btn',
            popover: {
              title: '⚡ Trigger Live Agentic Scan & Mitigation',
              description:
                'Click here to trigger the compiled StateGraph in real time. It solves IEEE non-linear differential equations and generates live B2B work orders & B2C citizen advisories via GPT-5.4 (~2.5s).',
              side: 'bottom',
              align: 'end',
            },
          },
          {
            element: '#tour-agent-dag',
            popover: {
              title: '🔄 5-Node Cognitive Pipeline DAG',
              description:
                'Click any node card (forecast_node → physics_node → planner_node → safety_gate_node → audit_dispatch_node) to inspect its state transitions and layer specifications.',
              side: 'top',
              align: 'center',
            },
          },
          {
            element: '#tour-agent-state',
            popover: {
              title: '📦 Active StateGraph Node Inspector',
              description:
                'Examine the state payload: Ingested State Inputs, Emitted State Outputs, and Explainable Physical Reasoning certified by the non-LLM CBF-QP barrier.',
              side: 'top',
              align: 'center',
            },
          },
          {
            element: '#tour-agent-work-order',
            popover: {
              title: '📋 Dispatched B2B Work Order & B2C Citizen Advisory',
              description:
                'Displays the authorized B2B Utility Work Order (WO-TSG-04) with physical SCADA controls, plus the public B2C Citizen Advisory dynamically synthesized by GPT-5.4.',
              side: 'top',
              align: 'center',
            },
          },
          {
            element: '#tour-agent-audit-trail',
            popover: {
              title: '📜 Real-Time Node Transition Audit Trail',
              description:
                'Tamper-evident chronological audit trail logging exact UTC timestamps, traversed nodes, and dispatch messages across the LangGraph state machine.',
              side: 'top',
              align: 'center',
            },
          },
        ];

      case 'financial_roi':
        return [
          {
            element: '#tour-financial-header',
            popover: {
              title: '💰 Avoided Loss & ROI Financial Audit',
              description:
                'Investment-grade financial model based on the US Department of Energy (DOE) and LBNL Interruption Cost Estimate (ICE) Calculator.',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-financial-breakdown',
            popover: {
              title: '💵 Quantified Outage & Capital Protection',
              description:
                'Auditable breakdown of avoided catastrophic replacement costs ($1.25M), customer interruption costs (VoLL), and capital aging deferral ($2.74M net savings).',
              side: 'top',
              align: 'center',
            },
          },
          {
            element: '#tour-financial-matrix',
            popover: {
              title: '📊 Comparative Advantage Matrix',
              description:
                'Demonstrates up to $2.74M net avoided loss per extreme heatwave event with >24x to 5,835x operational ROI over baseline station-weather controllers.',
              side: 'top',
              align: 'center',
            },
          },
        ];

      default:
        return [];
    }
  };

  const steps = getStepsForTab(activeTab);
  if (!steps.length) return;

  const driverObj = driver({
    showProgress: true,
    animate: true,
    allowClose: true,
    overlayColor: 'rgba(2, 6, 23, 0.88)',
    stagePadding: 8,
    stageRadius: 16,
    popoverClass: 'driverjs-theme',
    nextBtnText: 'Next →',
    prevBtnText: '← Back',
    doneBtnText: 'Finish Tour ✨',
    steps,
  });

  driverObj.drive();
};
