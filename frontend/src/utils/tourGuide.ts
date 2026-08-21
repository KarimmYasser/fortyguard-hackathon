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
                'Welcome to Thermal Sentinel Grid! This tour guide is available across ALL 10 tabs to guide you through every physics engine, simulation tool, and live API capability.',
              side: 'bottom',
              align: 'end',
            },
          },
          {
            element: '#tour-hero-header',
            popover: {
              title: '🌟 Executive Mission Overview',
              description:
                'Thermal Sentinel Grid couples FortyGuard 2-meter microclimate AI with IEEE differential equations and multi-agent dispatch to protect electrical power grids from heatwave thermal runaway.',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-video-showcase',
            popover: {
              title: '🎬 3-Minute Video Showcase & Live Demo',
              description:
                'Watch the official programmatic motion illustration pitch or toggle to the full automated live UI product walkthrough. Jump directly to any timestamp using interactive chapter markers.',
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
                'Switch between unmitigated baseline operation (overheating excursion past 140°C) and physics-bounded proactive mitigation.',
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
              title: '⚡ Tab 1: Mission Control Telemetry',
              description:
                'Scrub through the 12-hour forward forecast timeline and inspect IEEE C57.91 winding hot-spot temperatures in real time.',
              side: 'top',
              align: 'start',
            },
          },
          {
            element: '#tour-card-sandbox',
            popover: {
              title: '🎛️ Tab 2: What-If Physics Studio',
              description:
                'Modulate ambient temperature spikes, battery storage MWh, and cooling fans with sub-15ms real-time ODE re-solving.',
              side: 'top',
              align: 'start',
            },
          },
          {
            element: '#tour-card-gis',
            popover: {
              title: '🗺️ Tab 6: Hyperlocal 2m GIS Engine',
              description:
                'Explore 2-meter FortyGuard convective & surface temperatures, resolving localized +4.5°C asphalt traps and urban heat canyons.',
              side: 'top',
              align: 'start',
            },
          },
          {
            element: '#tour-card-agent',
            popover: {
              title: '🤖 Tab 8: LangGraph Multi-Agent Stack',
              description:
                'Inspect the 5-node cognitive pipeline with live GPT-5.4 synthesis via Siemens SDC LLM Gateway and full audit trails.',
              side: 'top',
              align: 'start',
            },
          },
          {
            element: '#tour-card-roi',
            popover: {
              title: '💰 Tab 9: Avoided Loss & ROI Audit',
              description:
                'Audit investment-grade economics with the DOE LBNL ICE model showing $2.79M net savings and 5,952x economic ROI per heatwave event.',
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
              title: '📊 Real-Time Physics KPI Grid',
              description:
                'Tracks IEEE winding hot-spot rise (T_hs), Arrhenius cellulose loss-of-life acceleration (V), avoided capital losses, and FortyGuard persistence (P_40).',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-telemetry-charts',
            popover: {
              title: '📈 3-Axis Synchronized Physics Telemetry',
              description:
                'Interactive Apache ECharts rendering Ambient 2m vs. Top-Oil vs. Winding Hot-Spot temperatures alongside Arrhenius aging curves and BESS dispatch schedules.',
              side: 'top',
              align: 'center',
            },
          },
          {
            element: '#tour-safety-gate',
            popover: {
              title: '🛡️ CBF-QP Safety Barrier Invariance',
              description:
                'Control Barrier Functions (h(x) >= 0) mathematically guarantee safety sets, overriding any hallucinations with certified physical invariance.',
              side: 'top',
              align: 'start',
            },
          },
          {
            element: '#tour-audit-ledger',
            popover: {
              title: '📜 Multi-Agent Immutable Audit Ledger',
              description:
                'Chronological, tamper-evident audit ledger capturing every action dispatched by the LangGraph agent stack with UTC timestamps.',
              side: 'top',
              align: 'end',
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
                'Click one-click stress presets: Phoenix 23 Peak, Airport SCADA Blindspot (0°C delta), 31-Day Desertification, or Zero-BESS Stress to instantly reconfigure the environment.',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-sandbox-controls',
            popover: {
              title: '🎛️ Real-Time Parameter Sliders',
              description:
                'Modulate key stress variables: FortyGuard 2m microclimate delta (+1°C to +8°C), heatwave duration, BESS peak shaving capacity (MW), transformer MVA rating, and auxiliary cooling fans.',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-kpi-grid',
            popover: {
              title: '📊 Instant Sub-15ms ODE Solver Output',
              description:
                'Observe how customized stress variables immediately recalculate the full IEEE C57.91 2nd-order non-linear differential solver with instantaneous numerical feedback.',
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
              title: '⚡ 14-Bus AC Distribution Feeder Power Flow',
              description:
                'Full non-linear forward-backward sweep AC power flow solver calculating real and reactive power (P, Q), bus voltages (V, theta), and feeder line losses in real time.',
              side: 'bottom',
              align: 'center',
            },
          },
          {
            element: '#tour-powerflow-diagram',
            popover: {
              title: '🗺️ Interactive Single-Line Diagram',
              description:
                'Visual distribution network layout showing substation transformers, distributed PV solar, EV charging clusters, and BESS injection nodes.',
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
              title: '🌡️ Resolving +4.5°C Urban Asphalt Traps',
              description:
                'Demonstrates why generic 10km airport weather fails: dark asphalt and heat canyons create localized microclimates 4.5°C hotter than airport readings.',
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
                'Auditable breakdown of avoided catastrophic replacement costs ($1.25M), customer interruption costs (VoLL), and capital aging deferral ($2.79M net savings).',
              side: 'top',
              align: 'center',
            },
          },
          {
            element: '#tour-financial-matrix',
            popover: {
              title: '📊 Comparative Advantage Matrix',
              description:
                'Demonstrates up to $2.79M net avoided loss per extreme heatwave event with >24x to 5,952x operational ROI over baseline airport controllers.',
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
