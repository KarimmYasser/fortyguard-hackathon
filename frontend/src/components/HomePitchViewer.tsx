import React, { useState, useRef } from 'react';
import {
  Video,
  Sparkles,
  Zap,
  Layers,
  Cpu,
  ShieldCheck,
  Calculator,
  Sliders,
  MapPin,
  Flame,
  Network,
  Award,
  ArrowRight,
  Radio,
  CheckCircle2,
  Clock,
  Download,
  HelpCircle,
  Compass,
  Activity,
  BookOpen,
  Thermometer,
  Film,
  BriefcaseBusiness,
  BarChart3,
  ExternalLink,
} from 'lucide-react';
import { ActiveTab } from './Navbar';
import { startTourGuide } from '../utils/tourGuide';

interface HomePitchViewerProps {
  onNavigateTab: (tab: ActiveTab) => void;
  onOpenLiveScan?: () => void;
  onOpenDatabaseModal?: () => void;
}

interface ChapterMarker {
  time: number;
  label: string;
  desc: string;
  icon: React.ElementType;
}

export const HomePitchViewer: React.FC<HomePitchViewerProps> = ({
  onNavigateTab,
  onOpenLiveScan,
  onOpenDatabaseModal,
}) => {
  const [activeVideoSource, setActiveVideoSource] = useState<'pitch' | 'live_demo' | 'business_demo'>('business_demo');
  const [playerMode, setPlayerMode] = useState<'youtube' | 'local'>('youtube');
  const [currentTime, setCurrentTime] = useState<number>(0);

  const videoRef = useRef<HTMLVideoElement>(null);

  const handleStartTour = () => {
    startTourGuide({
      activeTab: 'home',
      onNavigateTab,
      onOpenLiveScan,
      onOpenDatabaseModal,
    });
  };

  const videoSources = {
    business_demo: {
      bundled: true,
      url: '/videos/business_value_demo.mp4',
      subtitledUrl: '/videos/final_submission_fortyguard_burned_subtitles.mp4',
      youtubeUrl: 'https://youtu.be/2kf-TLSv9kU',
      title: '⚡ 4-Min Business Value & Customer Discovery Demo',
      badge: 'Judges Choice · Subtitled',
      description: 'Unhurried 1080p full interaction focused on commercial ROI, COCO customer discovery, OSHA worker safety shifts, and deterministic safety gates.',
    },
    pitch: {
      bundled: true,
      url: '/videos/video.mp4',
      youtubeUrl: undefined,
      title: '🎬 3-Minute Motion Illustration Pitch',
      badge: 'Official Pitch Video',
      description: 'Programmatic motion-graphics pitch breaking down the market blindspot, 4 scientific moats, and hybrid Physical-AI architecture.',
    },
    live_demo: {
      bundled: true,
      url: '/videos/live_product_demo.mp4',
      youtubeUrl: undefined,
      title: '💻 Live UI Product Demo Walkthrough',
      badge: 'Interactive Product Demo',
      description: 'Unedited 1080p capture of the deployed platform: live FortyGuard scan, 12-hour scrub, What-If Studio, AC power flow, and a real LangGraph dispatch run. Figures shift as the sandbox sliders move — that is the simulation responding, not a different dataset.',
    },
  };

  const chapters: ChapterMarker[] = [
    { time: 0, label: '0:00 Market Blindspot', desc: 'Phoenix 12h Thermal Soak ($2.58M Risk)', icon: Flame },
    { time: 30, label: '0:30 4 Scientific Moats', desc: 'Soil Dryout & IEEE Physics ODEs', icon: Layers },
    { time: 60, label: '1:00 Hybrid Physical-AI', desc: 'LangGraph + Deterministic Safety Gate', icon: Cpu },
    { time: 90, label: '1:30 Live Mission Control', desc: '12h Proactive Dispatch & What-If Studio', icon: Sliders },
    { time: 135, label: '2:15 Auditable ROI', desc: 'VoLL Scenario Model ($2.58M Exposure)' , icon: Calculator },
    { time: 165, label: '2:45 Verification & Outro', desc: 'Tracks 06 & 02 Compliance Seals', icon: Award },
  ];

  const handleSeek = (seconds: number) => {
    if (videoRef.current) {
      videoRef.current.currentTime = seconds;
      setCurrentTime(seconds);
      videoRef.current.play().catch(() => {});
    }
  };

  return (
    <div className="space-y-10 pb-12">
      {/* 1. Hero Title & Vision Header */}
      <section
        id="tour-hero-header"
        className="relative overflow-hidden rounded-3xl border border-slate-800 bg-gradient-to-b from-slate-900/90 via-[#0a0f1d]/80 to-[#080c14] p-8 md:p-12 shadow-2xl"
      >
        {/* Glow Accents */}
        <div className="absolute -top-24 -left-24 h-96 w-96 rounded-full bg-amber-500/10 blur-3xl pointer-events-none"></div>
        <div className="absolute -bottom-24 -right-24 h-96 w-96 rounded-full bg-cyan-500/10 blur-3xl pointer-events-none"></div>

        <div className="relative z-10 flex flex-col lg:flex-row items-start lg:items-center justify-between gap-8">
          <div className="space-y-4 max-w-3xl">
            {/* Badges */}
            <div className="flex flex-wrap items-center gap-2">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono font-bold bg-cyan-500/15 text-cyan-300 border border-cyan-500/30">
                <ShieldCheck className="h-3.5 w-3.5" /> Track 03: Industrial & Enterprise
              </span>
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono font-bold bg-purple-500/15 text-purple-300 border border-purple-500/30">
                <Cpu className="h-3.5 w-3.5" /> Track 06: Agentic AI
              </span>
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono font-bold bg-orange-500/15 text-orange-300 border border-orange-500/30">
                <Zap className="h-3.5 w-3.5" /> Track 02: Energy Systems
              </span>
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono font-bold bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
                <ShieldCheck className="h-3.5 w-3.5" /> IEEE C57.91 & ANSI C84.1 Verified
              </span>
            </div>

            {/* Main Headline */}
            <h1 className="text-3xl sm:text-5xl lg:text-6xl font-black tracking-tight text-white font-heading leading-tight">
              THERMAL SENTINEL GRID
            </h1>

            {/* Subheading */}
            <p className="text-sm sm:text-base md:text-lg text-slate-300 font-sans leading-relaxed">
              Physics-Constrained Multi-Agent Thermal Resilience for Critical Energy Infrastructure.
              Coupling <span className="text-amber-400 font-semibold">FortyGuard 2-Meter Microclimate AI</span> with{' '}
              <span className="text-cyan-400 font-semibold">IEEE C57.91 Differential Equations</span>,{' '}
              <span className="text-purple-400 font-semibold">LangGraph Multi-Agent Dispatch</span>, and a deterministic{' '}
              <span className="text-emerald-400 font-semibold">CBF-inspired deterministic trajectory</span> safety gate.
            </p>

            {/* Action Buttons */}
            <div className="flex flex-wrap items-center gap-3 pt-2">
              <button
                onClick={() => onNavigateTab('overview')}
                className="px-5 py-2.5 rounded-2xl bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-400 hover:to-orange-400 text-slate-950 font-bold text-sm shadow-xl shadow-amber-500/25 flex items-center gap-2 transition-all hover:scale-[1.02]"
              >
                <span>Launch Mission Control</span>
                <ArrowRight className="h-4 w-4" />
              </button>

              <button
                onClick={() => onNavigateTab('sandbox')}
                className="px-5 py-2.5 rounded-2xl bg-slate-800 hover:bg-slate-700 text-slate-100 font-bold text-sm border border-slate-700 flex items-center gap-2 transition-all"
              >
                <Sliders className="h-4 w-4 text-cyan-400" />
                <span>Open What-If Studio</span>
              </button>

              <button
                onClick={handleStartTour}
                className="px-4 py-2.5 rounded-2xl bg-gradient-to-r from-amber-500/15 to-orange-500/15 hover:from-amber-500/25 hover:to-orange-500/25 text-amber-300 font-bold text-sm border border-amber-500/40 flex items-center gap-2 transition-all shadow-md shadow-amber-500/10 hover:scale-[1.02]"
                title="Start Guided Spotlight Tour"
              >
                <Compass className="h-4 w-4 text-amber-400 animate-spin-slow" />
                <span>Interactive Guided Tour</span>
              </button>

              {onOpenLiveScan && (
                <button
                  onClick={onOpenLiveScan}
                  className="px-4 py-2.5 rounded-2xl bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-300 font-bold text-sm border border-cyan-500/30 flex items-center gap-2 transition-all"
                >
                  <Radio className="h-4 w-4 text-cyan-400 animate-pulse" />
                  <span>FortyGuard Live API Scan</span>
                </button>
              )}
            </div>
          </div>

          {/* Quick Stat Pill Card */}
          <div className="w-full lg:w-80 glass-panel rounded-2xl p-5 border border-slate-800 bg-slate-950/60 shadow-xl space-y-3 font-mono text-xs">
            <div className="text-slate-400 font-bold uppercase tracking-wider text-[10px] flex items-center justify-between">
              <span>Core Impact Metrics</span>
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-ping"></span>
            </div>
            <div className="space-y-2 divide-y divide-slate-800/60">
              <div className="flex items-center justify-between pt-1">
                <span className="text-slate-400">Net Avoided Loss:</span>
                <span className="text-emerald-400 font-bold">$2.57M scenario estimate</span>
              </div>
              <div className="flex items-center justify-between pt-2">
                <span className="text-slate-400">Economic ROI:</span>
                <span className="text-amber-400 font-bold">5,472.6x assumption-based</span>
              </div>
              <div className="flex items-center justify-between pt-2">
                <span className="text-slate-400">Microclimate Trap:</span>
                <span className="text-rose-400 font-bold">12h Above 40°C</span>
              </div>
              <div className="flex items-center justify-between pt-2">
                <span className="text-slate-400">Aging Life Saved:</span>
                <span className="text-cyan-400 font-bold">374.3 Equiv. Hours</span>
              </div>
              <div className="flex items-center justify-between pt-2">
                <span className="text-slate-400">Hospital Feeder Uptime:</span>
                <span className="text-emerald-400 font-bold">100.0% (ANSI C84.1)</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 2. Featured Video Hub & Chapter Navigation */}
      <section id="tour-video-showcase" className="space-y-4">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <div className="p-2 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20">
                <Video className="h-5 w-5" />
              </div>
              <div>
                <h2 className="text-lg font-extrabold text-white uppercase tracking-wide font-heading">
                  Official 3-Minute Video Showcase
                </h2>
                <p className="text-xs text-slate-400 font-mono">
                  Watch the presentation pitch or switch to the full automated live UI product walkthrough.
                </p>
              </div>
            </div>
          </div>

          {/* Right Header Controls: Mode Switcher & Download Button */}
          <div className="flex flex-wrap items-center gap-2.5">
            {/* Video Mode Switcher Pills */}
            <div className="flex items-center bg-slate-900 border border-slate-800 p-1 rounded-2xl text-xs font-mono">
              <button
                onClick={() => setActiveVideoSource('business_demo')}
                className={`px-3.5 py-1.5 rounded-xl font-bold transition-all flex items-center gap-2 ${
                  activeVideoSource === 'business_demo'
                    ? 'bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 shadow-md shadow-emerald-500/25'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                <Zap className="h-3.5 w-3.5" />
                <span>Business Value Demo (Subtitled)</span>
              </button>
              <button
                onClick={() => setActiveVideoSource('pitch')}
                className={`px-3.5 py-1.5 rounded-xl font-bold transition-all flex items-center gap-2 ${
                  activeVideoSource === 'pitch'
                    ? 'bg-gradient-to-r from-amber-500 to-orange-500 text-slate-950 shadow-md shadow-amber-500/25'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                <Sparkles className="h-3.5 w-3.5" />
                <span className="hidden sm:inline">Motion Pitch</span>
              </button>
              <button
                onClick={() => setActiveVideoSource('live_demo')}
                className={`px-3.5 py-1.5 rounded-xl font-bold transition-all flex items-center gap-2 ${
                  activeVideoSource === 'live_demo'
                    ? 'bg-gradient-to-r from-cyan-500 to-blue-500 text-slate-950 shadow-md shadow-cyan-500/25'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                <Cpu className="h-3.5 w-3.5" />
                <span className="hidden sm:inline">Product Demo</span>
              </button>
            </div>

            {/* Stream Player Toggle (YouTube / Local MP4) */}
            <div className="flex items-center bg-slate-900 border border-slate-800 p-1 rounded-2xl text-xs font-mono">
              <button
                onClick={() => setPlayerMode('youtube')}
                className={`px-3 py-1.5 rounded-xl font-bold transition-all flex items-center gap-1.5 ${
                  playerMode === 'youtube'
                    ? 'bg-rose-500 text-white shadow-md shadow-rose-500/25'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
                title="Stream via Official YouTube Player"
              >
                <Video className="h-3.5 w-3.5" />
                <span>YouTube</span>
              </button>
              <button
                onClick={() => setPlayerMode('local')}
                className={`px-3 py-1.5 rounded-xl font-bold transition-all flex items-center gap-1.5 ${
                  playerMode === 'local'
                    ? 'bg-cyan-500 text-slate-950 shadow-md shadow-cyan-500/25'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
                title="Stream via Direct High-Bitrate MP4"
              >
                <Film className="h-3.5 w-3.5" />
                <span>Direct MP4</span>
              </button>
            </div>

            {/* Open YouTube External Link */}
            <a
              href="https://youtu.be/2kf-TLSv9kU"
              target="_blank"
              rel="noopener noreferrer"
              className="px-3 py-2 rounded-2xl bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30 text-rose-300 hover:text-rose-200 text-xs font-mono font-medium flex items-center gap-1.5 transition-all shadow-sm"
              title="Watch on YouTube"
            >
              <ExternalLink className="h-3.5 w-3.5" />
              <span className="hidden sm:inline">YouTube</span>
            </a>

            {/* Download MP4 Button */}
            <a
              href="/videos/final_submission_fortyguard_burned_subtitles.mp4"
              download
              className="px-3 py-2 rounded-2xl bg-slate-900 hover:bg-slate-800 border border-slate-800 hover:border-slate-700 text-slate-300 hover:text-white text-xs font-mono font-medium flex items-center gap-1.5 transition-all shadow-sm"
              title="Download Burned-in Subtitled MP4"
            >
              <Download className="h-3.5 w-3.5 text-amber-400" />
              <span className="hidden sm:inline">MP4</span>
            </a>
          </div>
        </div>

        {/* Video Player Card */}
        <div className="max-w-6xl mx-auto w-full rounded-3xl overflow-hidden border border-slate-800 bg-slate-950 shadow-2xl p-2.5 sm:p-4">
          {playerMode === 'youtube' && activeVideoSource === 'business_demo' ? (
            <div className="w-full aspect-video rounded-2xl overflow-hidden bg-black shadow-inner border border-slate-800">
              <iframe
                className="w-full h-full border-0"
                src="https://www.youtube-nocookie.com/embed/2kf-TLSv9kU?autoplay=0&rel=0&modestbranding=1"
                title="Thermal Sentinel Grid - FortyGuard Hackathon Submission Pitch"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                allowFullScreen
              />
            </div>
          ) : (
            <video
              key={`${activeVideoSource}-${playerMode}`}
              ref={videoRef}
              src={
                activeVideoSource === 'business_demo'
                  ? '/videos/final_submission_fortyguard_burned_subtitles.mp4'
                  : videoSources[activeVideoSource].url
              }
              controls
              playsInline
              preload="metadata"
              className="w-full aspect-video rounded-2xl bg-black shadow-inner"
            >
              <track
                src="/videos/final_submission_fortyguard.vtt"
                kind="subtitles"
                srcLang="en"
                label="English Subtitles"
                default
              />
            </video>
          )}
        </div>

        {/* Chapter Jump Buttons (Aligned with Player) */}
        <div className="max-w-6xl mx-auto w-full space-y-2">
          <div className="text-xs font-mono text-slate-400 flex items-center gap-2">
            <Clock className="h-3.5 w-3.5 text-amber-400" />
            <span>VIDEO CHAPTERS (JUMP TO SECTION):</span>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2">
            {chapters.map((ch, idx) => {
              const Icon = ch.icon;
              const isCurrent = currentTime >= ch.time && (idx === chapters.length - 1 || currentTime < chapters[idx + 1].time);
              return (
                <button
                  key={ch.time}
                  onClick={() => handleSeek(ch.time)}
                  className={`p-3 rounded-2xl text-left border transition-all ${
                    isCurrent
                      ? 'bg-amber-500/15 border-amber-500/40 text-amber-300 shadow-md shadow-amber-500/10 ring-1 ring-amber-500/30'
                      : 'bg-slate-900/80 border-slate-800/80 text-slate-400 hover:border-slate-700 hover:text-slate-200'
                  }`}
                >
                  <div className="flex items-center gap-1.5 text-xs font-bold font-mono">
                    <Icon className="h-3.5 w-3.5 text-amber-400" />
                    <span>{ch.label}</span>
                  </div>
                  <div className="text-[11px] text-slate-400 truncate mt-1">
                    {ch.desc}
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      </section>

      {/* 3. Interactive Application Launchpad Grid */}
      <section className="space-y-4">
        <div id="tour-launchpad-header" className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              <Layers className="h-5 w-5" />
            </div>
            <div>
              <h2 className="text-lg font-extrabold text-white uppercase tracking-wide font-heading">
                Interactive System Launchpad
              </h2>
              <p className="text-xs text-slate-400 font-mono">
                Click any module card to jump directly into the live interactive engine.
              </p>
            </div>
          </div>

          <button
            onClick={handleStartTour}
            className="px-4 py-2 rounded-2xl bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/30 text-amber-300 font-mono font-bold text-xs flex items-center gap-2 transition-all shadow-sm shadow-amber-500/10 hover:shadow-amber-500/20 hover:scale-[1.02]"
            title="Start Guided Spotlight Tour"
          >
            <HelpCircle className="h-3.5 w-3.5 text-amber-400" />
            <span>How to Use / Guided Tour</span>
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {/* Card 1: Mission Control Overview */}
          <div
            id="tour-card-overview"
            onClick={() => onNavigateTab('overview')}
            className="glass-panel p-6 rounded-3xl border border-slate-800 hover:border-amber-500/40 bg-slate-950/70 hover:bg-slate-900/80 transition-all cursor-pointer group shadow-xl hover:shadow-amber-500/10 flex flex-col justify-between"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="p-2.5 rounded-2xl bg-amber-500/10 text-amber-400 border border-amber-500/20 group-hover:scale-110 transition-transform">
                  <Zap className="h-5 w-5" />
                </div>
                <span className="text-[11px] font-mono text-slate-500">TAB 2</span>
              </div>
              <h3 className="text-base font-bold text-white font-heading group-hover:text-amber-400 transition-colors">
                Mission Control & Telemetry
              </h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                12-hour forward forecast scrubber, IEEE C57.91 hot-spot differential ODEs, and baseline vs mitigated comparison.
              </p>
            </div>
            <div className="flex items-center gap-1.5 text-xs font-mono text-amber-400 font-bold pt-4">
              <span>Open Mission Control</span>
              <ArrowRight className="h-3.5 w-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>

          {/* Portfolio Operations */}
          <div
            id="tour-card-operations"
            onClick={() => onNavigateTab('portfolio_operations')}
            className="glass-panel p-6 rounded-3xl border border-slate-800 hover:border-cyan-500/40 bg-slate-950/70 hover:bg-slate-900/80 transition-all cursor-pointer group shadow-xl hover:shadow-cyan-500/10 flex flex-col justify-between"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="p-2.5 rounded-2xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 group-hover:scale-110 transition-transform">
                  <BriefcaseBusiness className="h-5 w-5" />
                </div>
                <span className="text-[11px] font-mono text-slate-500">OPERATIONS</span>
              </div>
              <h3 className="text-base font-bold text-white font-heading group-hover:text-cyan-400 transition-colors">
                Portfolio Risk & Intervention Command
              </h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Rank registered assets, screen candidate field-work windows from measured environmental inputs, and inspect MCP-accessible SHA-256 evidence.
              </p>
            </div>
            <div className="flex items-center gap-1.5 text-xs font-mono text-cyan-400 font-bold pt-4">
              <span>Open Portfolio Operations</span>
              <ArrowRight className="h-3.5 w-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>

          {/* Card 2: What-If Studio */}
          <div
            id="tour-card-sandbox"
            onClick={() => onNavigateTab('sandbox')}
            className="glass-panel p-6 rounded-3xl border border-slate-800 hover:border-cyan-500/40 bg-slate-950/70 hover:bg-slate-900/80 transition-all cursor-pointer group shadow-xl hover:shadow-cyan-500/10 flex flex-col justify-between"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="p-2.5 rounded-2xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 group-hover:scale-110 transition-transform">
                  <Sliders className="h-5 w-5" />
                </div>
                <span className="text-[11px] font-mono text-slate-500">TAB 3</span>
              </div>
              <h3 className="text-base font-bold text-white font-heading group-hover:text-cyan-400 transition-colors">
                What-If Stress Studio & BESS
              </h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Interactive parameter modulation (ambient spike, BESS MWh, load factor) with 2-state cell electro-thermal ODEs.
              </p>
            </div>
            <div className="flex items-center gap-1.5 text-xs font-mono text-cyan-400 font-bold pt-4">
              <span>Launch Stress Studio</span>
              <ArrowRight className="h-3.5 w-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>

          {/* Card 3: 72h Compounding */}
          <div
            id="tour-card-72h"
            onClick={() => onNavigateTab('multi_day_72h')}
            className="glass-panel p-6 rounded-3xl border border-slate-800 hover:border-orange-500/40 bg-slate-950/70 hover:bg-slate-900/80 transition-all cursor-pointer group shadow-xl hover:shadow-orange-500/10 flex flex-col justify-between"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="p-2.5 rounded-2xl bg-orange-500/10 text-orange-400 border border-orange-500/20 group-hover:scale-110 transition-transform">
                  <Flame className="h-5 w-5" />
                </div>
                <span className="text-[11px] font-mono text-slate-500">TAB 4</span>
              </div>
              <h3 className="text-base font-bold text-white font-heading group-hover:text-orange-400 transition-colors">
                72h Compounding Heatwave
              </h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Continuous 3-day simulation showing night-time thermal soak, soil moisture desertification, and compounding aging.
              </p>
            </div>
            <div className="flex items-center gap-1.5 text-xs font-mono text-orange-400 font-bold pt-4">
              <span>View 72h Simulation</span>
              <ArrowRight className="h-3.5 w-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>

          {/* Card 4: AC Power Flow & DLR */}
          <div
            id="tour-card-powerflow"
            onClick={() => onNavigateTab('power_flow')}
            className="glass-panel p-6 rounded-3xl border border-slate-800 hover:border-emerald-500/40 bg-slate-950/70 hover:bg-slate-900/80 transition-all cursor-pointer group shadow-xl hover:shadow-emerald-500/10 flex flex-col justify-between"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="p-2.5 rounded-2xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 group-hover:scale-110 transition-transform">
                  <Activity className="h-5 w-5" />
                </div>
                <span className="text-[11px] font-mono text-slate-500">TAB 5</span>
              </div>
              <h3 className="text-base font-bold text-white font-heading group-hover:text-emerald-400 transition-colors">
                AC Power Flow & Dynamic Line Rating
              </h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                4-bus single-line diagram, IEEE 738-inspired DLR and catenary estimates, plus analytical uncertainty-bounded dispatch screening.
              </p>
            </div>
            <div className="flex items-center gap-1.5 text-xs font-mono text-emerald-400 font-bold pt-4">
              <span>Open AC Power Flow</span>
              <ArrowRight className="h-3.5 w-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>

          {/* Card 5: IEEE Annex G */}
          <div
            id="tour-card-ieee"
            onClick={() => onNavigateTab('ieee_annex_g')}
            className="glass-panel p-6 rounded-3xl border border-slate-800 hover:border-blue-500/40 bg-slate-950/70 hover:bg-slate-900/80 transition-all cursor-pointer group shadow-xl hover:shadow-blue-500/10 flex flex-col justify-between"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="p-2.5 rounded-2xl bg-blue-500/10 text-blue-400 border border-blue-500/20 group-hover:scale-110 transition-transform">
                  <Award className="h-5 w-5" />
                </div>
                <span className="text-[11px] font-mono text-slate-500">TAB 6</span>
              </div>
              <h3 className="text-base font-bold text-white font-heading group-hover:text-blue-400 transition-colors">
                IEEE Std C57.91 Annex G Benchmark
              </h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Exact verification against Clause G.2 (Step Load) and Clause G.3 (Diurnal Ramp) standard tables (&lt;0.0001°C error).
              </p>
            </div>
            <div className="flex items-center gap-1.5 text-xs font-mono text-blue-400 font-bold pt-4">
              <span>Inspect IEEE Standards</span>
              <ArrowRight className="h-3.5 w-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>

          {/* Independent Ground Truth */}
          <div
            id="tour-card-ground-truth"
            onClick={() => onNavigateTab('ground_truth')}
            className="glass-panel p-6 rounded-3xl border border-slate-800 hover:border-cyan-500/40 bg-slate-950/70 hover:bg-slate-900/80 transition-all cursor-pointer group shadow-xl hover:shadow-cyan-500/10 flex flex-col justify-between"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="p-2.5 rounded-2xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 group-hover:scale-110 transition-transform">
                  <Thermometer className="h-5 w-5" />
                </div>
                <span className="text-[11px] font-mono text-slate-500">VALIDATION</span>
              </div>
              <h3 className="text-base font-bold text-white font-heading group-hover:text-cyan-400 transition-colors">
                Independent Ground Truth Comparison
              </h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Timestamp-aligned PHX ASOS observations versus FortyGuard 2m values, with correlation, RMSE, coverage, and explicit UHI limitations.
              </p>
            </div>
            <div className="flex items-center gap-1.5 text-xs font-mono text-cyan-400 font-bold pt-4">
              <span>Inspect Ground Truth</span>
              <ArrowRight className="h-3.5 w-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>

          {/* Card 6: Academic Provenance & alphaXiv */}
          <div
            id="tour-card-academic"
            onClick={() => onNavigateTab('academic_provenance')}
            className="glass-panel p-6 rounded-3xl border border-slate-800 hover:border-teal-500/40 bg-slate-950/70 hover:bg-slate-900/80 transition-all cursor-pointer group shadow-xl hover:shadow-teal-500/10 flex flex-col justify-between"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="p-2.5 rounded-2xl bg-teal-500/10 text-teal-400 border border-teal-500/20 group-hover:scale-110 transition-transform">
                  <BookOpen className="h-5 w-5" />
                </div>
                <span className="text-[11px] font-mono text-slate-500">TAB 7</span>
              </div>
              <h3 className="text-base font-bold text-white font-heading group-hover:text-teal-400 transition-colors">
                Academic Provenance & alphaXiv
              </h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                50+ peer-reviewed papers discovered via alphaXiv, Surface Energy Balance PDEs, and live academic literature search.
              </p>
            </div>
            <div className="flex items-center gap-1.5 text-xs font-mono text-teal-400 font-bold pt-4">
              <span>Search Academic Corpus</span>
              <ArrowRight className="h-3.5 w-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>

          {/* Card 7: 2m GIS Heatmap */}
          <div
            id="tour-card-gis"
            onClick={() => onNavigateTab('gis_map')}
            className="glass-panel p-6 rounded-3xl border border-slate-800 hover:border-rose-500/40 bg-slate-950/70 hover:bg-slate-900/80 transition-all cursor-pointer group shadow-xl hover:shadow-rose-500/10 flex flex-col justify-between"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="p-2.5 rounded-2xl bg-rose-500/10 text-rose-400 border border-rose-500/20 group-hover:scale-110 transition-transform">
                  <MapPin className="h-5 w-5" />
                </div>
                <span className="text-[11px] font-mono text-slate-500">TAB 8</span>
              </div>
              <h3 className="text-base font-bold text-white font-heading group-hover:text-rose-400 transition-colors">
                Hyperlocal 2m GIS Engine
              </h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                FortyGuard 2-meter convective and radiative temperature layers resolving the measured +1.1°C land-cover delta and the 12-hour thermal soak that drives insulation aging.
              </p>
            </div>
            <div className="flex items-center gap-1.5 text-xs font-mono text-rose-400 font-bold pt-4">
              <span>Explore GIS Heatmap</span>
              <ArrowRight className="h-3.5 w-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>

          {/* Card 8: 4 Scientific Moats and safety filtering */}
          <div
            id="tour-card-moats"
            onClick={() => onNavigateTab('physics_moats')}
            className="glass-panel p-6 rounded-3xl border border-slate-800 hover:border-emerald-500/40 bg-slate-950/70 hover:bg-slate-900/80 transition-all cursor-pointer group shadow-xl hover:shadow-emerald-500/10 flex flex-col justify-between"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="p-2.5 rounded-2xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 group-hover:scale-110 transition-transform">
                  <ShieldCheck className="h-5 w-5" />
                </div>
                <span className="text-[11px] font-mono text-slate-500">TAB 9</span>
              </div>
              <h3 className="text-base font-bold text-white font-heading group-hover:text-emerald-400 transition-colors">
                4 Asymmetric Scientific Moats
              </h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Underground cable-soil dryout, urban canyon aerodynamic throttling, virtual paper-oil moisture, and deterministic model preflight.
              </p>
            </div>
            <div className="flex items-center gap-1.5 text-xs font-mono text-emerald-400 font-bold pt-4">
              <span>Review Scientific Moats</span>
              <ArrowRight className="h-3.5 w-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>

          {/* Card 9: LangGraph Engine */}
          <div
            id="tour-card-agent"
            onClick={() => onNavigateTab('agent_graph')}
            className="glass-panel p-6 rounded-3xl border border-slate-800 hover:border-purple-500/40 bg-slate-950/70 hover:bg-slate-900/80 transition-all cursor-pointer group shadow-xl hover:shadow-purple-500/10 flex flex-col justify-between"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="p-2.5 rounded-2xl bg-purple-500/10 text-purple-400 border border-purple-500/20 group-hover:scale-110 transition-transform">
                  <Cpu className="h-5 w-5" />
                </div>
                <span className="text-[11px] font-mono text-slate-500">TAB 10</span>
              </div>
              <h3 className="text-base font-bold text-white font-heading group-hover:text-purple-400 transition-colors">
                LangGraph Multi-Agent Stack
              </h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Five-node orchestration pipeline synthesizing operator-reviewed mitigation recommendations, work orders, and advisories.
              </p>
            </div>
            <div className="flex items-center gap-1.5 text-xs font-mono text-purple-400 font-bold pt-4">
              <span>Inspect Agent Graph</span>
              <ArrowRight className="h-3.5 w-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>

          {/* Card 10: Avoided Loss & ROI Audit */}
          <div
            id="tour-card-roi"
            onClick={() => onNavigateTab('financial_roi')}
            className="glass-panel p-6 rounded-3xl border border-slate-800 hover:border-amber-500/40 bg-slate-950/70 hover:bg-slate-900/80 transition-all cursor-pointer group shadow-xl hover:shadow-amber-500/10 flex flex-col justify-between"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="p-2.5 rounded-2xl bg-amber-500/10 text-amber-400 border border-amber-500/20 group-hover:scale-110 transition-transform">
                  <Calculator className="h-5 w-5" />
                </div>
                <span className="text-[11px] font-mono text-slate-500">TAB 11</span>
              </div>
              <h3 className="text-base font-bold text-white font-heading group-hover:text-amber-400 transition-colors">
                Scenario Avoided-Loss Economics
              </h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                VoLL-informed scenario model: approximately $2.57M avoided exposure and a 5,472.6x assumption-based ratio; not realized savings or certification.
              </p>
            </div>
            <div className="flex items-center gap-1.5 text-xs font-mono text-amber-400 font-bold pt-4">
              <span>View Financial Model</span>
              <ArrowRight className="h-3.5 w-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>

          {/* Card 11: Data Science Studio & Analytics */}
          <div
            id="tour-card-datascience"
            onClick={() => onNavigateTab('data_science')}
            className="glass-panel p-6 rounded-3xl border border-slate-800 hover:border-purple-500/40 bg-slate-950/70 hover:bg-slate-900/80 transition-all cursor-pointer group shadow-xl hover:shadow-purple-500/10 flex flex-col justify-between"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="p-2.5 rounded-2xl bg-purple-500/10 text-purple-400 border border-purple-500/20 group-hover:scale-110 transition-transform">
                  <BarChart3 className="h-5 w-5" />
                </div>
                <span className="text-[11px] font-mono text-slate-500">TAB 12</span>
              </div>
              <h3 className="text-base font-bold text-white font-heading group-hover:text-purple-400 transition-colors">
                Data Science Studio & ML
              </h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Medallion ETL pipeline (Bronze/Silver/Gold 18 features), polynomial Ridge surrogate regressor, spatial OLS, and Weibull survival analysis.
              </p>
            </div>
            <div className="flex items-center gap-1.5 text-xs font-mono text-purple-400 font-bold pt-4">
              <span>Open Data Science Studio</span>
              <ArrowRight className="h-3.5 w-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        </div>
      </section>


      {/* 4. Verification & Submission Standard Strip */}
      <section id="tour-disclosure-strip" className="glass-panel rounded-3xl p-6 border border-slate-800 bg-[#070b14] space-y-4">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-4">
          <div className="flex items-center gap-2">
            <Award className="h-5 w-5 text-amber-400" />
            <h3 className="text-sm font-bold text-white uppercase tracking-wider font-mono">
              Judge Evaluation & Technical Disclosure Checklist
            </h3>
          </div>
          <div className="flex items-center gap-2 text-xs font-mono text-emerald-400">
            <CheckCircle2 className="h-4 w-4" />
            <span>Automated regression suite available (pytest tests/ -q)</span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs font-mono">
          <div className="space-y-1.5">
            <span className="text-slate-400 font-bold text-[11px]">1. FORTYGUARD APIS INTEGRATED</span>
            <p className="text-slate-300">
              <code>POST /v1/heatmap</code> (GeoJSON polygon scan; <code>tcm</code> thermal matrix, <code>persistence</code> P40 & <code>exceedance</code> analytics), <code>POST /v1/env_params</code> (12h boundary conditions), and submit-and-poll <code>GET /v1/status</code>.
            </p>
          </div>
          <div className="space-y-1.5">
            <span className="text-slate-400 font-bold text-[11px]">2. HYBRID PHYSICAL-AI FORMULATION</span>
            <p className="text-slate-300">
              Closed-form exponential ODE integrator (IEEE C57.91 Annex G, NumPy) + LangGraph cognitive orchestrator + Non-LLM CBF constraint-projection safety gate.
            </p>
          </div>
          <div className="space-y-1.5">
            <span className="text-slate-400 font-bold text-[11px]">3. STANDARDS COMPLIANCE</span>
            <p className="text-slate-300">
              ANSI C84.1 Voltage Range A (0.95-1.05 pu), IEEE C57.91 (Winding Hot-Spot Ths ≤ 140°C), and DOE LBNL ICE Interruption Valuation.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePitchViewer;
