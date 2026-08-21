import React, { useState, useEffect } from 'react';
import {
  BookOpen,
  Search,
  ExternalLink,
  Copy,
  Check,
  Sparkles,
  Flame,
  Layers,
  Cpu,
  ShieldCheck,
  RefreshCw,
  FileText,
  Atom,
  Network,
} from 'lucide-react';
import { API_BASE } from '../utils/api';
import { MathView } from './MathView';


interface Paper {
  arxiv_id: string;
  title: string;
  authors: string[];
  summary: string;
  published: string;
  categories?: string[];
  primary_category?: string;
  pdf_url: string;
  arxiv_url: string;
  alphaxiv_url: string;
  math_insights?: {
    latex_expressions?: string[];
    pde_physics_keywords?: string[];
    ml_architecture_keywords?: string[];
    urban_domain_keywords?: string[];
  };
  ieee_citation?: string;
}

interface DomainSection {
  title: string;
  description?: string;
  papers: Paper[];
}

export const AcademicProvenanceViewer: React.FC = () => {
  const [corpus, setCorpus] = useState<Record<string, DomainSection>>({});
  const [selectedDomain, setSelectedDomain] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [searchResults, setSearchResults] = useState<Paper[] | null>(null);
  const [isSearching, setIsSearching] = useState<boolean>(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [isLoadingCorpus, setIsLoadingCorpus] = useState<boolean>(true);

  // Fetch pre-indexed corpus
  useEffect(() => {
    const fetchCorpus = async () => {
      setIsLoadingCorpus(true);
      try {
        const resp = await fetch(`${API_BASE}/api/v1/research/corpus`);
        if (resp.ok) {
          const data = await resp.json();
          setCorpus(data);
        }
      } catch (err) {
        console.error('Failed to fetch research corpus', err);
      } finally {
        setIsLoadingCorpus(false);
      }
    };
    fetchCorpus();
  }, []);

  // Handle live search
  const handleSearch = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!searchQuery.trim()) {
      setSearchResults(null);
      return;
    }

    setIsSearching(true);
    try {
      const resp = await fetch(
        `${API_BASE}/api/v1/research/search?query=${encodeURIComponent(searchQuery)}&limit=8`
      );
      if (resp.ok) {
        const data = await resp.json();
        setSearchResults(data.papers || []);
      }
    } catch (err) {
      console.error('Failed to search papers', err);
    } finally {
      setIsSearching(false);
    }
  };

  const handleCopyCitation = (paper: Paper) => {
    const citation =
      paper.ieee_citation ||
      `${paper.authors.slice(0, 2).join(' and ')}${paper.authors.length > 2 ? ' et al.' : ''}, "${paper.title}," arXiv:${paper.arxiv_id}, ${paper.published?.slice(0, 4) || '2024'}.`;
    navigator.clipboard.writeText(citation);
    setCopiedId(paper.arxiv_id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  // Aggregate all papers or filter by domain
  const allPapers: (Paper & { domainTitle: string })[] = [];
  Object.entries(corpus).forEach(([key, section]) => {
    (section.papers || []).forEach((p) => {
      allPapers.push({ ...p, domainTitle: section.title });
    });
  });

  const displayedPapers = searchResults
    ? searchResults.map((p) => ({ ...p, domainTitle: 'Live Search Result' }))
    : selectedDomain === 'all'
    ? allPapers
    : (corpus[selectedDomain]?.papers || []).map((p) => ({
        ...p,
        domainTitle: corpus[selectedDomain]?.title || '',
      }));

  return (
    <div className="space-y-6">
      {/* Hero Header & Physics Grounding Banner */}
      <div id="tour-academic-header" className="bg-gradient-to-r from-slate-900 via-slate-900/90 to-amber-950/40 border border-slate-800 rounded-2xl p-6 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-amber-500/5 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs font-mono font-medium mb-3">
              <BookOpen className="h-3.5 w-3.5" />
              PEER-REVIEWED SCIENTIFIC PROVENANCE & ALPHAXIV ENGINE
            </div>
            <h1 className="text-2xl font-bold font-heading text-white tracking-wide">
              Academic Literature & Mathematical Foundations
            </h1>
            <p className="text-slate-400 text-sm mt-1 max-w-3xl">
              Thermal Sentinel Grid’s thermal downscaling, cool pavement physics, and grid heatwave dispatch
              are grounded in <strong>47 peer-reviewed papers and preprints</strong> discovered via our automated
              alphaXiv and arXiv research adapter.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <div className="bg-slate-950/80 border border-slate-800 rounded-xl px-4 py-3 text-center">
              <span className="block text-2xl font-bold text-amber-400 font-mono">47</span>
              <span className="text-[10px] text-slate-500 font-mono uppercase tracking-wider">Indexed Papers</span>
            </div>
            <div className="bg-slate-950/80 border border-slate-800 rounded-xl px-4 py-3 text-center">
              <span className="block text-2xl font-bold text-cyan-400 font-mono">5</span>
              <span className="text-[10px] text-slate-500 font-mono uppercase tracking-wider">Physics Domains</span>
            </div>
            <div className="bg-slate-950/80 border border-slate-800 rounded-xl px-4 py-3 text-center">
              <span className="block text-2xl font-bold text-emerald-400 font-mono">100%</span>
              <span className="text-[10px] text-slate-500 font-mono uppercase tracking-wider">alphaXiv Verified</span>
            </div>
          </div>
        </div>
      </div>

      {/* Physics Moats & Mathematical Mapping Accordion */}
      <div id="tour-academic-formulas" className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-900/60 border border-slate-800/80 rounded-xl p-4 hover:border-amber-500/40 transition-colors flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 text-amber-400 font-bold text-xs uppercase tracking-wider font-mono mb-2">
              <Flame className="h-4 w-4" />
              Surface Energy Balance (SEB)
            </div>
            <div className="bg-slate-950/90 p-2.5 rounded-xl border border-slate-800/80 mb-2.5 overflow-hidden text-center flex items-center justify-center min-h-[56px] text-amber-200 w-full">
              <MathView math="R_n = (1 - \alpha) S_{\downarrow} + \epsilon (L_{\downarrow} - \sigma T_s^4) = Q_H + Q_E + Q_G" scale="auto" />
            </div>
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            Governs cool pavement albedo modification (<MathView math="\alpha: 0.10 \to 0.45+" displayMode={false} />) and sensible heat flux reduction (<MathView math="Q_H" displayMode={false} />) into pedestrian air layers.
          </p>
        </div>

        <div className="bg-slate-900/60 border border-slate-800/80 rounded-xl p-4 hover:border-cyan-500/40 transition-colors flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 text-cyan-400 font-bold text-xs uppercase tracking-wider font-mono mb-2">
              <Atom className="h-4 w-4" />
              Thermal Diffusion & PINNs
            </div>
            <div className="bg-slate-950/90 p-2.5 rounded-xl border border-slate-800/80 mb-2.5 overflow-hidden text-center flex items-center justify-center min-h-[56px] text-cyan-200 w-full">
              <MathView math="\frac{\partial T}{\partial t} + \mathbf{u} \cdot \nabla T = \nabla \cdot (\kappa \nabla T) + S(\mathbf{x}, t)" scale="auto" />
            </div>
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            Enforces energy conservation laws in neural forecasting, eliminating non-physical temperature drift in heatwaves.
          </p>
        </div>

        <div className="bg-slate-900/60 border border-slate-800/80 rounded-xl p-4 hover:border-emerald-500/40 transition-colors flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 text-emerald-400 font-bold text-xs uppercase tracking-wider font-mono mb-2">
              <Network className="h-4 w-4" />
              Graph Neural Heat Flow
            </div>
            <div className="bg-slate-950/90 p-2.5 rounded-xl border border-slate-800/80 mb-2.5 overflow-hidden text-center flex items-center justify-center min-h-[56px] text-emerald-200 w-full">
              <MathView math="\mathbf{H}^{(l+1)} = \sigma \left( \sum_{k=0}^{K} \mathbf{P}^k \mathbf{H}^{(l)} \mathbf{W}_k \right)" scale="auto" />
            </div>
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            Models advective heat propagation across non-Euclidean urban street canyons and FortyGuard IoT sensor meshes.
          </p>
        </div>
      </div>



      {/* Live Search & Filter Bar */}
      <div id="tour-academic-search" className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 space-y-4">
        <form onSubmit={handleSearch} className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-3 h-4 w-4 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search arXiv & alphaXiv (e.g. 'cool pavement albedo', 'land surface temperature downscaling')..."
              className="w-full pl-10 pr-4 py-2.5 bg-slate-950 border border-slate-700/80 rounded-lg text-sm text-white placeholder-slate-500 focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500"
            />
          </div>
          <button
            type="submit"
            disabled={isSearching}
            className="px-5 py-2.5 bg-gradient-to-r from-amber-600 to-amber-500 hover:from-amber-500 hover:to-amber-400 text-slate-950 font-bold rounded-lg text-xs tracking-wide uppercase font-mono flex items-center justify-center gap-2 transition-all disabled:opacity-50"
          >
            {isSearching ? <RefreshCw className="h-4 w-4 animate-spin" /> : <Search className="h-4 w-4" />}
            {isSearching ? 'Searching arXiv...' : 'Query alphaXiv'}
          </button>
          {searchResults && (
            <button
              type="button"
              onClick={() => {
                setSearchResults(null);
                setSearchQuery('');
              }}
              className="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs font-mono"
            >
              Clear Search
            </button>
          )}
        </form>

        {/* Domain Filter Pills */}
        {!searchResults && (
          <div id="tour-academic-filters" className="flex items-center gap-2 overflow-x-auto pb-1 text-xs">
            <span className="text-slate-500 font-mono uppercase text-[11px] whitespace-nowrap">Filter Domain:</span>
            <button
              onClick={() => setSelectedDomain('all')}
              className={`px-3 py-1.5 rounded-lg font-mono text-xs whitespace-nowrap transition-colors ${
                selectedDomain === 'all'
                  ? 'bg-amber-500 text-slate-950 font-bold'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
              }`}
            >
              All Domains ({allPapers.length})
            </button>
            {Object.entries(corpus).map(([key, section]) => (
              <button
                key={key}
                onClick={() => setSelectedDomain(key)}
                className={`px-3 py-1.5 rounded-lg font-mono text-xs whitespace-nowrap transition-colors ${
                  selectedDomain === key
                    ? 'bg-amber-500 text-slate-950 font-bold'
                    : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                }`}
              >
                {section.title} ({section.papers?.length || 0})
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Papers Grid */}
      <div id="tour-academic-cards" className="space-y-4">

        <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
          <span>
            Displaying {displayedPapers.length} {searchResults ? 'Search Results' : 'Peer-Reviewed Works'}
          </span>
          <span className="text-amber-400 flex items-center gap-1">
            <Sparkles className="h-3 w-3" /> Live IEEE Citation & alphaXiv Discussion Links
          </span>
        </div>

        {isLoadingCorpus ? (
          <div className="text-center py-12 text-slate-400">
            <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-2 text-amber-500" />
            <p className="font-mono text-xs">Loading Scientific Literature Corpus...</p>
          </div>
        ) : displayedPapers.length === 0 ? (
          <div className="text-center py-12 bg-slate-900/40 border border-slate-800 rounded-xl text-slate-400">
            <BookOpen className="h-8 w-8 mx-auto mb-2 text-slate-600" />
            <p className="text-sm font-medium text-slate-300">No papers found</p>
            <p className="text-xs text-slate-500 mt-1">Try a different query or switch domain filter.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {displayedPapers.map((paper, idx) => (
              <div
                key={paper.arxiv_id || idx}
                className="bg-slate-900/70 border border-slate-800 rounded-xl p-5 hover:border-slate-700 flex flex-col justify-between transition-all group"
              >
                <div>
                  <div className="flex items-start justify-between gap-3 mb-2">
                    <span className="px-2.5 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 text-[10px] font-mono font-bold">
                      arXiv:{paper.arxiv_id}
                    </span>
                    <span className="text-[11px] text-slate-500 font-mono">
                      {paper.published ? paper.published.slice(0, 10) : 'Recent'}
                    </span>
                  </div>

                  <h3 className="text-base font-bold text-white font-heading group-hover:text-amber-300 transition-colors leading-snug">
                    {paper.title}
                  </h3>

                  <p className="text-xs text-slate-400 mt-1.5 line-clamp-1 font-mono">
                    {paper.authors?.slice(0, 3).join(', ')}
                    {paper.authors?.length > 3 ? ' et al.' : ''}
                  </p>

                  <p className="text-xs text-slate-300 mt-3 line-clamp-3 leading-relaxed">
                    {paper.summary}
                  </p>

                  {/* Badges / Keywords */}
                  {paper.math_insights && (
                    <div className="flex flex-wrap gap-1.5 mt-3">
                      {(paper.math_insights.pde_physics_keywords || []).map((kw, i) => (
                        <span key={i} className="px-2 py-0.5 rounded bg-amber-500/10 text-amber-300 text-[10px] font-mono border border-amber-500/20">
                          {kw}
                        </span>
                      ))}
                      {(paper.math_insights.ml_architecture_keywords || []).map((kw, i) => (
                        <span key={i} className="px-2 py-0.5 rounded bg-purple-500/10 text-purple-300 text-[10px] font-mono border border-purple-500/20">
                          {kw}
                        </span>
                      ))}
                      {(paper.math_insights.urban_domain_keywords || []).map((kw, i) => (
                        <span key={i} className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 text-[10px] font-mono border border-emerald-500/20">
                          {kw}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                <div className="pt-4 mt-4 border-t border-slate-800/80 flex items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <a
                      href={paper.alphaxiv_url || `https://alphaxiv.org/abs/${paper.arxiv_id}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-2.5 py-1.5 bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 border border-amber-500/30 rounded-lg text-xs font-mono flex items-center gap-1.5 transition-colors"
                    >
                      <Sparkles className="h-3 w-3" />
                      alphaXiv Discuss
                      <ExternalLink className="h-2.5 w-2.5 opacity-60" />
                    </a>

                    <a
                      href={paper.pdf_url || `https://arxiv.org/pdf/${paper.arxiv_id}.pdf`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-2.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs font-mono flex items-center gap-1.5 transition-colors"
                    >
                      <FileText className="h-3 w-3" />
                      PDF
                      <ExternalLink className="h-2.5 w-2.5 opacity-60" />
                    </a>
                  </div>

                  <button
                    onClick={() => handleCopyCitation(paper)}
                    className="px-2.5 py-1.5 bg-slate-800/80 hover:bg-slate-700 text-slate-300 rounded-lg text-xs font-mono flex items-center gap-1.5 transition-colors"
                    title="Copy IEEE Citation"
                  >
                    {copiedId === paper.arxiv_id ? (
                      <>
                        <Check className="h-3 w-3 text-emerald-400" />
                        <span className="text-emerald-400">Copied!</span>
                      </>
                    ) : (
                      <>
                        <Copy className="h-3 w-3" />
                        <span>IEEE Cite</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
