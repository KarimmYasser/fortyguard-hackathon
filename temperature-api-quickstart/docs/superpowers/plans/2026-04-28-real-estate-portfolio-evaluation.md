# Real-Estate Portfolio Heat Evaluation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite `notebooks/use_cases/real_estate_portfolio_heat_risk.ipynb` into a 10-step diurnal real-estate-agent-facing portfolio evaluation that runs end-to-end with cached files (offline) when `CACHED=True`, and exercises four FortyGuard API endpoints when `CACHED=False`.

**Architecture:** The notebook reads the user portfolio CSV plus four cached FortyGuard sample artifacts (24-hour heatmap GeoJSON, satellite seg JSON, street-view seg JSON, env-params JSON), computes diurnal per-property metrics, runs surface and ground-truth diagnostics on the top-N exposures, and emits two scores (heat-risk and opportunity), three folium maps (M1/M2/M3), four matplotlib charts (C1–C4), and a CSV (`outputs/portfolio_evaluation.csv`). Every expensive step has an `if CACHED:` cached-file branch and an `else:` live-API branch. No new Python modules are introduced; everything lives in the notebook.

**Tech Stack:** Jupyter (nbformat 4.5), pandas, folium, matplotlib, shapely, IPython.display.HTML, the FortyGuard SDK (`fortyguard.FortyGuardClient`, `fortyguard.samples.SAN_JOSE_POLYGON`).

**Spec:** [docs/superpowers/specs/2026-04-28-real-estate-portfolio-evaluation-design.md](../specs/2026-04-28-real-estate-portfolio-evaluation-design.md) (commit `d4c7a69`).

---

## File Structure

| Path | Action | Responsibility |
|---|---|---|
| `notebooks/use_cases/real_estate_portfolio_heat_risk.ipynb` | **Replace** | Full new 25-cell workflow (was 19 cells). Single self-contained notebook. |
| `outputs/portfolio_evaluation.csv` | **Create on run** | Final priority CSV with 19 columns × 10 rows. Output of Step 10. |
| `data/real_estate_san_jose_portfolio_sample.csv` | **Read only** | Portfolio input (10 rows). Already exists. |
| `data/real_state_san_jose_heatmap_sample_day_2024-10-02.geojson` | **Read only** | 24-hour cached heatmap (16,507 tiles, °F). |
| `data/real_state_san_jose_satellite_segmentation_sample_day_2024-10-02.json` | **Read only** | Cached satellite seg for P01. |
| `data/real_state_san_jose_street_view_segmentation_sample_day_2024-10-02.json` | **Read only** | Cached street-view seg for P01. |
| `data/real_state_san_jose_env_paramaters_sample_day_2024-10-02.json` | **Read only** | Cached env-params for P01 (24 hours). |

**Untouched:** every other notebook (especially [urban_forestry_tree_prioritization.ipynb](../../../notebooks/use_cases/urban_forestry_tree_prioritization.ipynb) and [urban_planner_bus_stop_prioritization.ipynb](../../../notebooks/use_cases/urban_planner_bus_stop_prioritization.ipynb)), the `fortyguard/` SDK package, `requirements.txt`.

The implementation strategy is **atomic full rewrite** (one Write of the complete .ipynb JSON) followed by an end-to-end execute via `jupyter nbconvert --to notebook --execute`. The notebook's narrative is sequential and the spec is fully detailed, so a single atomic write is more reliable than incremental cell edits.

---

## Task 1: Pre-flight checks

**Files:**
- Read: `data/real_estate_san_jose_portfolio_sample.csv`
- Read: `data/real_state_san_jose_heatmap_sample_day_2024-10-02.geojson` (existence only)
- Read: `data/real_state_san_jose_satellite_segmentation_sample_day_2024-10-02.json` (existence only)
- Read: `data/real_state_san_jose_street_view_segmentation_sample_day_2024-10-02.json` (existence only)
- Read: `data/real_state_san_jose_env_paramaters_sample_day_2024-10-02.json` (existence only)
- Modify: `outputs/` directory creation

- [ ] **Step 1: Verify required data files exist**

Run:
```bash
ls -la c:/development/fortyguard/repositories/temperature-api-quickstart/data/real_estate_san_jose_portfolio_sample.csv c:/development/fortyguard/repositories/temperature-api-quickstart/data/real_state_san_jose_heatmap_sample_day_2024-10-02.geojson c:/development/fortyguard/repositories/temperature-api-quickstart/data/real_state_san_jose_satellite_segmentation_sample_day_2024-10-02.json c:/development/fortyguard/repositories/temperature-api-quickstart/data/real_state_san_jose_street_view_segmentation_sample_day_2024-10-02.json c:/development/fortyguard/repositories/temperature-api-quickstart/data/real_state_san_jose_env_paramaters_sample_day_2024-10-02.json
```

Expected: 5 files listed, no "No such file or directory" errors. Sizes roughly: portfolio ~780 B, heatmap geojson ~17 MB, satellite ~445 KB, streetview ~630 KB, env-params ~12 KB.

- [ ] **Step 2: Ensure `outputs/` directory exists**

Run:
```bash
mkdir -p c:/development/fortyguard/repositories/temperature-api-quickstart/outputs
```

Expected: no output (directory already existed) or silent creation.

- [ ] **Step 3: Verify required Python packages are importable**

Run:
```bash
python -c "import pandas, folium, matplotlib, shapely, IPython; from fortyguard import FortyGuardClient; from fortyguard.samples import SAN_JOSE_POLYGON; print('OK')"
```

Expected output exactly: `OK`. If any import fails, install via `pip install -r c:/development/fortyguard/repositories/temperature-api-quickstart/requirements.txt`.

- [ ] **Step 4: Capture baseline notebook hash for diff later**

Run:
```bash
git -C c:/development/fortyguard/repositories/temperature-api-quickstart log --oneline -1 -- notebooks/use_cases/real_estate_portfolio_heat_risk.ipynb
```

Expected: a commit SHA (any commit). Note the SHA — you'll diff against it after the rewrite.

---

## Task 2: Replace the notebook with the full new workflow

**Files:**
- Replace: `notebooks/use_cases/real_estate_portfolio_heat_risk.ipynb` (write the entire .ipynb file)

This task is one atomic Write call. The complete JSON content is embedded below — copy it verbatim into the Write tool.

- [ ] **Step 1: Write the complete notebook file**

Use the Write tool with `file_path = c:/development/fortyguard/repositories/temperature-api-quickstart/notebooks/use_cases/real_estate_portfolio_heat_risk.ipynb` and the following content (one literal Python string, valid JSON, nbformat 4.5):

```json
{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "intro-md",
   "metadata": {},
   "source": [
    "# Use Case — Portfolio Heat Evaluation for the Real-Estate Agent\n",
    "\n",
    "**Who this is for**  \n",
    "Real-estate agents preparing a portfolio review with a client; portfolio managers and client advisors; secondarily REIT asset managers, private real-estate investors, and property operations leads.\n",
    "\n",
    "**The scenario**  \n",
    "You manage (or advise on) a 10-asset San Jose portfolio. The client wants to know which assets are at heat risk *today*, which represent the biggest *opportunity* if you treat them, and what those answers mean in dollars. Walking a building per day is not an option — you need a desk-first screening that gives you defensible numbers and slide-ready visuals before the meeting.\n",
    "\n",
    "This notebook combines **your portfolio data** with **FortyGuard layers** to answer five questions:\n",
    "\n",
    "1. **Where in the portfolio is hot, when, and by how much?**  ← 24-hour heatmap × portfolio\n",
    "2. **Why are the hottest properties hot?**  ← satellite segmentation on top exposures\n",
    "3. **What does the curb actually look like?**  ← street-view ground-truth on the #1 exposure\n",
    "4. **What does tenant comfort look like through the day?**  ← environmental parameters\n",
    "5. **What's the risk and the opportunity per asset, in dollars and tiers?**  ← composite scoring + business translation\n",
    "\n",
    "> **Cached by default.** The notebook ships with `CACHED=True` so it runs end-to-end against the bundled sample files in `data/` — no API key needed for the demo. Set `CACHED=False` at the top of the Setup cell to run the same workflow live against any portfolio.\n",
    "\n",
    "> **Bring your own portfolio.** Sample data ships at `data/real_estate_san_jose_portfolio_sample.csv`. Swap the path in Step 1 — as long as the columns match (`property_id`, `name`, `type`, `year_built`, `sqft`, `market_value_musd`, `latitude`, `longitude`), everything downstream works.\n",
    "\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "setup-md",
   "metadata": {},
   "source": ["## Setup"]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "setup-code",
   "metadata": {},
   "outputs": [],
   "source": [
    "import sys, pathlib\n",
    "ROOT = pathlib.Path.cwd().parents[1]\n",
    "sys.path.insert(0, str(ROOT))\n",
    "\n",
    "from dotenv import load_dotenv\n",
    "load_dotenv(ROOT / '.env')\n",
    "\n",
    "import json\n",
    "import random\n",
    "import pandas as pd\n",
    "import folium\n",
    "import matplotlib.pyplot as plt\n",
    "from shapely.geometry import Point, shape, mapping\n",
    "from IPython.display import HTML, display\n",
    "\n",
    "from fortyguard import FortyGuardClient\n",
    "from fortyguard.samples import SAN_JOSE_POLYGON\n",
    "\n",
    "# ── configuration ──────────────────────────────────────────────────\n",
    "STUDY_DATE         = '2024-10-02'         # matches the bundled cached files\n",
    "STUDY_HOUR         = '14:00'              # design-peak snapshot for the live API\n",
    "GRANULARITY_M      = 100                  # heatmap resolution\n",
    "TOP_N_TO_ENRICH    = 3                    # API budget for satellite / env-params\n",
    "CACHED             = True                 # set False for live API calls\n",
    "BASELINE_C         = 24.0                 # comfortable ambient baseline\n",
    "COOLING_KWH_PER_SF = 0.18                 # extra kWh per sf per °C above baseline\n",
    "KWH_PRICE_USD      = 0.24\n",
    "SLA_HI_C           = 32.0                 # tenant-comfort heat-index threshold\n",
    "TEMP_C_SANITY      = (15.0, 55.0)         # F→C conversion sanity range\n",
    "ASSET_TYPE_PALETTE = {\n",
    "    'Office':       '#1f77b4',\n",
    "    'Residential':  '#2ca02c',\n",
    "    'Retail':       '#ff7f0e',\n",
    "    'Mixed-Use':    '#9467bd',\n",
    "    'Industrial':   '#8c564b',\n",
    "}\n",
    "\n",
    "# ── data paths ──────────────────────────────────────────────────────\n",
    "DATA            = ROOT / 'data'\n",
    "PORTFOLIO_CSV   = DATA / 'real_estate_san_jose_portfolio_sample.csv'\n",
    "HEATMAP_GEOJSON = DATA / 'real_state_san_jose_heatmap_sample_day_2024-10-02.geojson'\n",
    "SATELLITE_JSON  = DATA / 'real_state_san_jose_satellite_segmentation_sample_day_2024-10-02.json'\n",
    "STREETVIEW_JSON = DATA / 'real_state_san_jose_street_view_segmentation_sample_day_2024-10-02.json'\n",
    "ENV_PARAMS_JSON = DATA / 'real_state_san_jose_env_paramaters_sample_day_2024-10-02.json'\n",
    "HEAT_INTEL_PDF  = DATA / 'real_state_san_jose_heat_intelligence_sample_day_2024-10-02.pdf'\n",
    "OUTPUT_CSV      = ROOT / 'outputs' / 'portfolio_evaluation.csv'\n",
    "OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)\n",
    "\n",
    "client = FortyGuardClient()  # used only when CACHED=False\n",
    "print(f\"CACHED={CACHED}  STUDY_DATE={STUDY_DATE}  TOP_N_TO_ENRICH={TOP_N_TO_ENRICH}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "step1-md",
   "metadata": {},
   "source": [
    "---\n",
    "## Step 1 — Load your portfolio\n",
    "\n",
    "### What you are doing\n",
    "Reading the portfolio CSV. Any columns may ride along — the workflow only needs `latitude` and `longitude` to do the geospatial work; the rest pass through to the final output so finance and ops see the asset IDs and values they already recognize.\n",
    "\n",
    "### Why this matters\n",
    "Starting from the operations system of record means the output carries *your* property IDs, *your* asset types, *your* square-footages — ready to paste into the client report or CRM."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "step1-code",
   "metadata": {},
   "outputs": [],
   "source": [
    "portfolio = pd.read_csv(PORTFOLIO_CSV)\n",
    "type_counts = portfolio['type'].value_counts().to_dict()\n",
    "print(f\"Loaded {len(portfolio)} properties, \"\n",
    "      f\"total value ${portfolio['market_value_musd'].sum():.0f}M, \"\n",
    "      f\"total {portfolio['sqft'].sum():,} sqft\")\n",
    "print(f\"  asset-type mix: {type_counts}\")\n",
    "portfolio"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "step2-md",
   "metadata": {},
   "source": [
    "---\n",
    "## Step 2 — Heat layer (online or cached)\n",
    "\n",
    "### What you are doing\n",
    "When `CACHED=True` we read the bundled 24-hour heatmap GeoJSON — 16,507 tiles, each carrying hourly temperatures `'00'..'23'` plus min/max/avg. Values in the file are in °F, so we convert and assert a sanity range. When `CACHED=False` we call `client.create_heatmap` for the design hour.\n",
    "\n",
    "### Why this matters\n",
    "A city-wide weather observation misses intra-city variation that *actually* drives cooling cost and tenant complaints. At 100 m resolution we can distinguish a building on the hot side of a block from one on the cool side. The 24-hour cached layer also unlocks **peak-hour** and **diurnal-swing** signals you cannot get from a single-hour call."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "step2-code",
   "metadata": {},
   "outputs": [],
   "source": [
    "def _f_to_c(f):\n",
    "    return (f - 32.0) * 5.0 / 9.0\n",
    "\n",
    "def _load_cached_heatmap():\n",
    "    \"\"\"Return (tiles, aoi_bounds). tiles = list of (polygon, hourly_c, peak_c, peak_h, min_c).\"\"\"\n",
    "    with open(HEATMAP_GEOJSON, 'r', encoding='utf-8') as f:\n",
    "        gj = json.load(f)\n",
    "    feats = gj.get('features', [])\n",
    "    tiles = []\n",
    "    minx = miny =  1e9\n",
    "    maxx = maxy = -1e9\n",
    "    for ft in feats:\n",
    "        poly = shape(ft['geometry'])\n",
    "        props = ft['properties']\n",
    "        hourly_c = [_f_to_c(props[f\"{h:02d}\"]) for h in range(24)]\n",
    "        peak_c   = max(hourly_c)\n",
    "        peak_h   = hourly_c.index(peak_c)\n",
    "        min_c    = min(hourly_c)\n",
    "        tiles.append((poly, hourly_c, peak_c, peak_h, min_c))\n",
    "        x0, y0, x1, y1 = poly.bounds\n",
    "        if x0 < minx: minx = x0\n",
    "        if y0 < miny: miny = y0\n",
    "        if x1 > maxx: maxx = x1\n",
    "        if y1 > maxy: maxy = y1\n",
    "    return tiles, (minx, miny, maxx, maxy)\n",
    "\n",
    "if CACHED:\n",
    "    tiles, aoi_bounds = _load_cached_heatmap()\n",
    "    peaks = [t[2] for t in tiles]\n",
    "    lo, hi = min(peaks), max(peaks)\n",
    "    assert TEMP_C_SANITY[0] <= lo and hi <= TEMP_C_SANITY[1], \\\n",
    "        f\"F→C sanity check failed: peak range {lo:.1f}..{hi:.1f} outside {TEMP_C_SANITY}\"\n",
    "    print(f\"[cached] {len(tiles)} tiles, peak temp range {lo:.1f}..{hi:.1f} °C\")\n",
    "    print(f\"[cached] AOI bounds (lon,lat): ({aoi_bounds[0]:.4f}, {aoi_bounds[1]:.4f}) → \"\n",
    "          f\"({aoi_bounds[2]:.4f}, {aoi_bounds[3]:.4f})\")\n",
    "else:\n",
    "    heatmap = client.create_heatmap(\n",
    "        polygon_aoi=SAN_JOSE_POLYGON, start_date=STUDY_DATE, start_time=STUDY_HOUR,\n",
    "        filter_type=1, granularity=GRANULARITY_M,\n",
    "    )\n",
    "    map_data = heatmap['result'].get('map_data') or {}\n",
    "    feats = map_data.get('features', []) if isinstance(map_data, dict) else []\n",
    "    tiles = []\n",
    "    minx = miny =  1e9\n",
    "    maxx = maxy = -1e9\n",
    "    sh = int(STUDY_HOUR.split(':')[0])\n",
    "    for ft in feats:\n",
    "        poly = shape(ft['geometry'])\n",
    "        t = ft['properties'].get('temperature')\n",
    "        # Single-hour live data: broadcast to 24-hour tuple so downstream code is uniform.\n",
    "        # Diurnal columns will be degenerate in this mode — see banner below.\n",
    "        hourly_c = [t] * 24\n",
    "        tiles.append((poly, hourly_c, t, sh, t))\n",
    "        x0, y0, x1, y1 = poly.bounds\n",
    "        if x0 < minx: minx = x0\n",
    "        if y0 < miny: miny = y0\n",
    "        if x1 > maxx: maxx = x1\n",
    "        if y1 > maxy: maxy = y1\n",
    "    aoi_bounds = (minx, miny, maxx, maxy)\n",
    "    print(f\"[online] {len(tiles)} tiles at {GRANULARITY_M}m, single hour {STUDY_HOUR}.\")\n",
    "    print(\"[online] ⚠ Diurnal swing / peak_hour / aoi_percentile collapse to the snapshot \"\n",
    "          \"hour. Use CACHED=True with a 24h GeoJSON for full-day analysis.\")\n",
    "\n",
    "def tile_for(lat, lon):\n",
    "    p = Point(lon, lat)\n",
    "    for t in tiles:\n",
    "        if t[0].contains(p):\n",
    "            return t\n",
    "    return min(tiles, key=lambda t: t[0].centroid.distance(p))"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "step3-md",
   "metadata": {},
   "source": [
    "---\n",
    "## Step 3 — Diurnal temperature attach\n",
    "\n",
    "### What you are doing\n",
    "For each property, find the tile that contains it, copy off the **peak temperature**, **peak hour**, **min temperature**, **diurnal swing**, and the **AOI percentile** (this property's peak relative to all 16,507 city tiles). Now every property has an analysis-ready row.\n",
    "\n",
    "### Why this matters\n",
    "This is the moment your portfolio table becomes a *risk* table. Every downstream question — ranking, scoring, business translation — is a `groupby` or sort on this DataFrame."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "step3-code",
   "metadata": {},
   "outputs": [],
   "source": [
    "def _percentile_rank(value, sorted_values):\n",
    "    lo, hi = 0, len(sorted_values)\n",
    "    while lo < hi:\n",
    "        mid = (lo + hi) // 2\n",
    "        if sorted_values[mid] <= value: lo = mid + 1\n",
    "        else: hi = mid\n",
    "    return round(100.0 * lo / max(1, len(sorted_values)), 1)\n",
    "\n",
    "aoi_peak_sorted = sorted(t[2] for t in tiles)\n",
    "\n",
    "records = []\n",
    "for _, r in portfolio.iterrows():\n",
    "    poly, hourly_c, peak_c, peak_h, min_c = tile_for(r.latitude, r.longitude)\n",
    "    records.append({\n",
    "        'peak_temp_c'   : round(peak_c, 1),\n",
    "        'peak_hour'     : peak_h,\n",
    "        'min_temp_c'    : round(min_c, 1),\n",
    "        'diurnal_swing_c': round(peak_c - min_c, 1),\n",
    "        'aoi_percentile': _percentile_rank(peak_c, aoi_peak_sorted),\n",
    "    })\n",
    "portfolio = pd.concat([portfolio.reset_index(drop=True), pd.DataFrame(records)], axis=1)\n",
    "portfolio = portfolio.sort_values('peak_temp_c', ascending=False).reset_index(drop=True)\n",
    "portfolio.insert(0, 'temp_rank', portfolio.index + 1)\n",
    "\n",
    "cols_t1 = ['temp_rank', 'property_id', 'name', 'type', 'sqft',\n",
    "           'peak_temp_c', 'peak_hour', 'min_temp_c', 'diurnal_swing_c', 'aoi_percentile']\n",
    "portfolio[cols_t1]"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "step4-md",
   "metadata": {},
   "source": [
    "---\n",
    "## Step 4 — Portfolio overview map (M1)\n",
    "\n",
    "### What you are doing\n",
    "Rendering every property on a folium map. Marker size scales with peak temperature; color encodes asset type. Popups show the dollar value, square footage, peak temperature, peak hour, and AOI percentile.\n",
    "\n",
    "### Why this matters\n",
    "This is the slide-1 visual for the client meeting. Before any score is computed, the map already tells the agent which assets to talk about — the big red circles."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "step4-code",
   "metadata": {},
   "outputs": [],
   "source": [
    "def _legend_html(palette):\n",
    "    rows = ''.join(\n",
    "        f'<tr><td style=\"background:{c};width:18px;\"></td>'\n",
    "        f'<td style=\"padding-left:6px;\">{name}</td></tr>'\n",
    "        for name, c in palette.items()\n",
    "    )\n",
    "    return (\n",
    "        '<div style=\"position:fixed;bottom:30px;left:30px;z-index:9999;'\n",
    "        'background:white;padding:8px 12px;border:1px solid #888;'\n",
    "        'font:12px sans-serif;\">'\n",
    "        '<b>Asset type</b>'\n",
    "        f'<table>{rows}</table>'\n",
    "        '</div>'\n",
    "    )\n",
    "\n",
    "center = [portfolio['latitude'].mean(), portfolio['longitude'].mean()]\n",
    "m1 = folium.Map(location=center, zoom_start=13, tiles='cartodbpositron')\n",
    "\n",
    "min_peak = portfolio['peak_temp_c'].min()\n",
    "for _, p in portfolio.iterrows():\n",
    "    folium.CircleMarker(\n",
    "        location=[p.latitude, p.longitude],\n",
    "        radius=4 + (p.peak_temp_c - min_peak) * 1.2,\n",
    "        color='#333', weight=1,\n",
    "        fill=True, fill_color=ASSET_TYPE_PALETTE.get(p['type'], '#888'),\n",
    "        fill_opacity=0.85,\n",
    "        popup=(f\"<b>{p['name']}</b><br/>\"\n",
    "               f\"{p['type']}, {p['sqft']:,} sqft, ${p['market_value_musd']}M<br/>\"\n",
    "               f\"peak: {p.peak_temp_c:.1f}°C @ {int(p.peak_hour):02d}:00<br/>\"\n",
    "               f\"AOI percentile: {p.aoi_percentile}\"),\n",
    "    ).add_to(m1)\n",
    "\n",
    "m1.get_root().html.add_child(folium.Element(_legend_html(ASSET_TYPE_PALETTE)))\n",
    "m1"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "step5-md",
   "metadata": {},
   "source": [
    "---\n",
    "## Step 5 — Above-average hot exposures (M2)\n",
    "\n",
    "### What you are doing\n",
    "Filtering to properties whose peak temperature is at or above the portfolio median, and overlaying the city's hottest-tile network (AOI 90th percentile) underneath. The zoomed map M2 shows where the action is.\n",
    "\n",
    "### Why this matters\n",
    "The agent doesn't need ten talking points; they need three. M2 is the slide-2 visual that says: \"these are the assets we have to discuss.\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "step5-code",
   "metadata": {},
   "outputs": [],
   "source": [
    "median_peak = portfolio['peak_temp_c'].median()\n",
    "hot = portfolio[portfolio['peak_temp_c'] >= median_peak].copy()\n",
    "\n",
    "p90 = sorted(t[2] for t in tiles)[int(0.90 * len(tiles))]\n",
    "overlay_tiles = [t for t in tiles if t[2] >= p90]\n",
    "if len(overlay_tiles) > 500:\n",
    "    random.seed(42)\n",
    "    overlay_tiles = random.sample(overlay_tiles, 500)\n",
    "\n",
    "m2 = folium.Map(location=center, zoom_start=14, tiles='cartodbpositron')\n",
    "for poly, _, peak_c, _, _ in overlay_tiles:\n",
    "    folium.GeoJson(\n",
    "        mapping(poly),\n",
    "        style_function=lambda x: {\n",
    "            'fillColor': '#d73027', 'color': '#d73027',\n",
    "            'weight': 0, 'fillOpacity': 0.25,\n",
    "        },\n",
    "    ).add_to(m2)\n",
    "for _, p in hot.iterrows():\n",
    "    folium.CircleMarker(\n",
    "        location=[p.latitude, p.longitude],\n",
    "        radius=8, color='black', weight=1,\n",
    "        fill=True, fill_color=ASSET_TYPE_PALETTE.get(p['type'], '#888'), fill_opacity=0.9,\n",
    "        popup=(f\"#{p.temp_rank} {p['name']}<br/>\"\n",
    "               f\"peak: {p.peak_temp_c:.1f}°C @ {int(p.peak_hour):02d}:00\"),\n",
    "    ).add_to(m2)\n",
    "\n",
    "print(f\"{len(hot)} above-average exposures (median peak {median_peak:.1f}°C); \"\n",
    "      f\"city 90th-pct = {p90:.1f}°C ({len(overlay_tiles)} tiles shown)\")\n",
    "display(m2)\n",
    "hot[['temp_rank','property_id','name','type','peak_temp_c','peak_hour','aoi_percentile']]"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "step6-md",
   "metadata": {},
   "source": [
    "---\n",
    "## Step 6 — Surface diagnosis (satellite segmentation)\n",
    "\n",
    "### What you are doing\n",
    "For the top-N hottest properties, characterize the surface mix in their immediate surroundings: building, road, sidewalk, tree, grass. We bucket those into `impervious_pct` and `vegetation_pct` for scoring, and chart the full breakdown.\n",
    "\n",
    "### Why this matters\n",
    "Temperature alone doesn't tell you what to spend money on. A hot property surrounded by impervious rooftops is a cool-roof candidate. A hot property with minimal vegetation is a planting candidate. The surface mix points to the lever — without us prescribing which one to pull."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "step6-code",
   "metadata": {},
   "outputs": [],
   "source": [
    "IMPERV_KEYS = {'road', 'roads', 'pavement', 'building', 'buildings',\n",
    "               'rooftop', 'rooftops', 'sidewalk', 'earth', 'bare', 'ground'}\n",
    "VEGGIE_KEYS = {'vegetation', 'tree', 'trees', 'grass', 'greenery', 'park'}\n",
    "\n",
    "def _bucket(segments, keys):\n",
    "    total = 0.0\n",
    "    for cls, pct in (segments or {}).items():\n",
    "        if any(k in cls.lower() for k in keys):\n",
    "            try: total += float(pct)\n",
    "            except (TypeError, ValueError): pass\n",
    "    return round(total, 1)\n",
    "\n",
    "top_n = portfolio.head(TOP_N_TO_ENRICH).copy()\n",
    "seg_data = {}  # property_id -> segments dict\n",
    "\n",
    "if CACHED:\n",
    "    with open(SATELLITE_JSON, 'r', encoding='utf-8') as f:\n",
    "        sat_doc = json.load(f)\n",
    "    sat_lat = float(sat_doc['coordinates']['latitude'])\n",
    "    sat_lon = float(sat_doc['coordinates']['longitude'])\n",
    "    sat_segs = sat_doc['segmentation'].get('segments', {}) or {}\n",
    "    matches = portfolio[\n",
    "        (portfolio['latitude'].sub(sat_lat).abs() < 1e-3) &\n",
    "        (portfolio['longitude'].sub(sat_lon).abs() < 1e-3)\n",
    "    ]\n",
    "    if len(matches):\n",
    "        pid = matches.iloc[0]['property_id']\n",
    "        seg_data[pid] = sat_segs\n",
    "        # If the cached property isn't in the top_n, append it so the deep-dive shows.\n",
    "        if pid not in top_n['property_id'].values:\n",
    "            top_n = pd.concat([top_n, portfolio[portfolio['property_id'] == pid]],\n",
    "                              ignore_index=True)\n",
    "    print(f\"⚠ Cached deep-dive applies to {list(seg_data.keys())} only. \"\n",
    "          f\"Set CACHED=False to enrich the full top-{TOP_N_TO_ENRICH}.\")\n",
    "else:\n",
    "    for _, r in top_n.iterrows():\n",
    "        print(f\"  satellite: #{int(r.temp_rank)} {r.property_id}\")\n",
    "        sat = client.satellite_segmentation(\n",
    "            latitude=r.latitude, longitude=r.longitude,\n",
    "            start_date=STUDY_DATE, start_time=STUDY_HOUR,\n",
    "            filter_type=1, granularity=GRANULARITY_M, verbose=False,\n",
    "        )\n",
    "        seg_data[r.property_id] = sat['result'].get('segmentation', {}).get('segments', {}) or {}\n",
    "\n",
    "top_n['impervious_pct'] = top_n['property_id'].map(\n",
    "    lambda pid: _bucket(seg_data.get(pid), IMPERV_KEYS) if pid in seg_data else None)\n",
    "top_n['vegetation_pct'] = top_n['property_id'].map(\n",
    "    lambda pid: _bucket(seg_data.get(pid), VEGGIE_KEYS) if pid in seg_data else None)\n",
    "\n",
    "# Chart C2 — stacked bar of segment classes for the available enriched properties\n",
    "enriched_rows = [(pid, segs) for pid, segs in seg_data.items() if segs]\n",
    "if enriched_rows:\n",
    "    classes = sorted({c for _, s in enriched_rows for c in s.keys()})\n",
    "    fig, ax = plt.subplots(figsize=(8, max(2.5, 0.8 * len(enriched_rows))))\n",
    "    bottoms = [0.0] * len(enriched_rows)\n",
    "    pids    = [pid for pid, _ in enriched_rows]\n",
    "    for c in classes:\n",
    "        vals = [float(segs.get(c, 0.0)) for _, segs in enriched_rows]\n",
    "        ax.barh(pids, vals, left=bottoms, label=c)\n",
    "        bottoms = [b + v for b, v in zip(bottoms, vals)]\n",
    "    ax.set_xlabel('% of surrounding scene')\n",
    "    ax.set_title('C2 — Satellite surface composition (top exposures)')\n",
    "    ax.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), fontsize=8)\n",
    "    plt.tight_layout(); plt.show()\n",
    "\n",
    "top_n[['temp_rank','property_id','name','peak_temp_c','impervious_pct','vegetation_pct']]"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "step7-md",
   "metadata": {},
   "source": [
    "---\n",
    "## Step 7 — Street-view ground truth on #1\n",
    "\n",
    "### What you are doing\n",
    "Pulling the front-facing street view at the highest-ranked enriched property and rendering the original alongside the segmented version. Tabulating the front-view composition (sky, building, tree, road, sidewalk, car, grass).\n",
    "\n",
    "### Why this matters\n",
    "Satellite shows the roof; the agent's client walks past the curb. Sky-fraction tells you canyon openness; car-fraction tells you traffic load; tree-fraction at the curb is what a passer-by experiences. This step grounds the satellite story in something a non-engineer recognizes."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "step7-code",
   "metadata": {},
   "outputs": [],
   "source": [
    "# \"Property #1\" = highest temp_rank within the enriched subset (cached: P01; online: top-N #1)\n",
    "enriched_subset = top_n[top_n['property_id'].isin(seg_data.keys())] if seg_data else top_n\n",
    "property_one = enriched_subset.iloc[0] if len(enriched_subset) else top_n.iloc[0]\n",
    "\n",
    "if CACHED:\n",
    "    with open(STREETVIEW_JSON, 'r', encoding='utf-8') as f:\n",
    "        sv = json.load(f)\n",
    "    front      = sv.get('front', {}) or {}\n",
    "    sv_orig    = front.get('original_image')\n",
    "    sv_seg     = front.get('segmented_image')\n",
    "    sv_segs    = front.get('segments', {}) or {}\n",
    "    image_date = front.get('image_date', 'n/a')\n",
    "else:\n",
    "    sv_resp = client.street_view_segmentation(\n",
    "        latitude=property_one.latitude, longitude=property_one.longitude,\n",
    "        start_date=STUDY_DATE, start_time=STUDY_HOUR,\n",
    "        filter_type=1, granularity=GRANULARITY_M, verbose=False,\n",
    "    )\n",
    "    front      = (sv_resp['result'] or {}).get('front', {}) or {}\n",
    "    sv_orig    = front.get('original_image')\n",
    "    sv_seg     = front.get('segmented_image')\n",
    "    sv_segs    = front.get('segments', {}) or {}\n",
    "    image_date = front.get('image_date', 'n/a')\n",
    "\n",
    "print(f\"Street-view #1 = {property_one['property_id']} ({property_one['name']}) — \"\n",
    "      f\"imagery date {image_date} (front view only)\")\n",
    "\n",
    "def _img_tag(b64, label):\n",
    "    if not b64:\n",
    "        return f'<div style=\"padding:1em;border:1px dashed #888;width:350px\">{label}: missing</div>'\n",
    "    return (f'<figure style=\"margin:0\">'\n",
    "            f'<img src=\"data:image/jpeg;base64,{b64}\" '\n",
    "            f'style=\"width:350px;border:1px solid #888;\"/>'\n",
    "            f'<figcaption style=\"text-align:center;font:11px sans-serif\">{label}</figcaption>'\n",
    "            f'</figure>')\n",
    "\n",
    "display(HTML(\n",
    "    '<div style=\"display:flex;gap:12px;flex-wrap:wrap\">'\n",
    "    + _img_tag(sv_orig, 'original') + _img_tag(sv_seg, 'segmented') +\n",
    "    '</div>'\n",
    "))\n",
    "\n",
    "pd.DataFrame(sorted(sv_segs.items(), key=lambda kv: -kv[1]),\n",
    "             columns=['class', 'pct'])"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "step8-md",
   "metadata": {},
   "source": [
    "---\n",
    "## Step 8 — Diurnal driver profile (env-params)\n",
    "\n",
    "### What you are doing\n",
    "Pulling the full-day environmental parameters for the top-N exposures: heat index, apparent temperature, relative humidity, solar irradiance. Computing per property: peak heat index, peak apparent temperature, hours-above-SLA in business hours (09:00–18:00), peak solar irradiance.\n",
    "\n",
    "### Why this matters\n",
    "Tenant-comfort SLAs are written in terms of heat index, not dry-bulb temperature. A building at 34 °C ambient with low humidity is comfortable; one at 31 °C with 80 % humidity is not. Heat index is the number complaints cluster around — and it's what the leasing team will quote back to you."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "step8-code",
   "metadata": {},
   "outputs": [],
   "source": [
    "def _slice_business_hours(values):\n",
    "    return [values[h] for h in range(9, 19)]  # 09:00..18:00 inclusive\n",
    "\n",
    "env_data = {}  # property_id -> dict of full-day series\n",
    "\n",
    "if CACHED:\n",
    "    with open(ENV_PARAMS_JSON, 'r', encoding='utf-8') as f:\n",
    "        env_doc = json.load(f)\n",
    "    loc = env_doc['locations'][0]\n",
    "    env_lat, env_lon = float(loc['lat']), float(loc['lon'])\n",
    "    params = loc.get('parameters', {}) or {}\n",
    "    series = {\n",
    "        'heat_index_celsius'           : list(params.get('heat_index_celsius') or []),\n",
    "        'apparent_temperature_celsius' : list(params.get('apparent_temperature_celsius') or []),\n",
    "        'relative_humidity_percent'    : list(params.get('relative_humidity_percent') or []),\n",
    "        'solar_irradiance'             : list(loc.get('solar_irradiance') or []),\n",
    "    }\n",
    "    matches = portfolio[\n",
    "        (portfolio['latitude'].sub(env_lat).abs() < 1e-3) &\n",
    "        (portfolio['longitude'].sub(env_lon).abs() < 1e-3)\n",
    "    ]\n",
    "    if len(matches):\n",
    "        env_data[matches.iloc[0]['property_id']] = series\n",
    "    print(f\"⚠ Cached env-params apply to {list(env_data.keys())} only. \"\n",
    "          f\"Set CACHED=False to enrich the full top-{TOP_N_TO_ENRICH}.\")\n",
    "else:\n",
    "    for _, r in top_n.iterrows():\n",
    "        print(f\"  env-params: #{int(r.temp_rank)} {r.property_id}\")\n",
    "        env = client.environmental_parameters(\n",
    "            latitude=r.latitude, longitude=r.longitude,\n",
    "            temperature=float(r.peak_temp_c),\n",
    "            start_date=STUDY_DATE, start_time='09:00', end_time='18:00',\n",
    "            filter_type=2, verbose=False,\n",
    "        )\n",
    "        loc = env['result']['locations'][0]\n",
    "        p = loc.get('parameters', {}) or {}\n",
    "        env_data[r.property_id] = {\n",
    "            'heat_index_celsius'           : list(p.get('heat_index_celsius') or []),\n",
    "            'apparent_temperature_celsius' : list(p.get('apparent_temperature_celsius') or []),\n",
    "            'relative_humidity_percent'    : list(p.get('relative_humidity_percent') or []),\n",
    "            'solar_irradiance'             : list(loc.get('solar_irradiance') or []),\n",
    "        }\n",
    "\n",
    "def _peak_metrics(s):\n",
    "    hi   = s.get('heat_index_celsius') or []\n",
    "    appt = s.get('apparent_temperature_celsius') or []\n",
    "    sol  = s.get('solar_irradiance') or []\n",
    "    business = _slice_business_hours(hi) if len(hi) >= 19 else hi\n",
    "    return {\n",
    "        'peak_heat_index_c'    : max(hi) if hi else None,\n",
    "        'peak_apparent_temp_c' : max(appt) if appt else None,\n",
    "        'hours_above_sla'      : sum(1 for v in business if v is not None and v > SLA_HI_C),\n",
    "        'peak_solar_irradiance': max(sol) if sol else None,\n",
    "    }\n",
    "\n",
    "metrics = {pid: _peak_metrics(s) for pid, s in env_data.items()}\n",
    "for col in ('peak_heat_index_c', 'peak_apparent_temp_c', 'hours_above_sla', 'peak_solar_irradiance'):\n",
    "    top_n[col] = top_n['property_id'].map(lambda p: (metrics.get(p) or {}).get(col))\n",
    "\n",
    "# Chart C3 — diurnal driver profile for property #1 (2-row subplot)\n",
    "if property_one['property_id'] in env_data:\n",
    "    s = env_data[property_one['property_id']]\n",
    "    n = len(s.get('heat_index_celsius') or [])\n",
    "    hours = list(range(n))\n",
    "    fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(9, 6), sharex=True)\n",
    "    if s.get('heat_index_celsius'):\n",
    "        ax_top.plot(hours, s['heat_index_celsius'], label='Heat index (°C)', color='#d62728')\n",
    "    if s.get('apparent_temperature_celsius'):\n",
    "        ax_top.plot(hours, s['apparent_temperature_celsius'], label='Apparent temp (°C)', color='#ff7f0e')\n",
    "    ax_top.axhline(SLA_HI_C, color='#888', linestyle='--', linewidth=1, label=f'SLA ({SLA_HI_C}°C)')\n",
    "    ax_top.set_ylabel('°C')\n",
    "    ax_top.legend(loc='upper left', fontsize=9)\n",
    "    if s.get('relative_humidity_percent'):\n",
    "        ax_rh = ax_top.twinx()\n",
    "        ax_rh.plot(hours, s['relative_humidity_percent'], label='RH (%)', color='#1f77b4', alpha=0.6)\n",
    "        ax_rh.set_ylabel('Relative humidity (%)', color='#1f77b4')\n",
    "        ax_rh.legend(loc='upper right', fontsize=9)\n",
    "    if s.get('solar_irradiance'):\n",
    "        ax_bot.plot(hours, s['solar_irradiance'], color='#bcbd22')\n",
    "    ax_bot.set_ylabel('Solar irradiance (W/m²)')\n",
    "    ax_bot.set_xlabel('Hour of day')\n",
    "    ax_top.set_title(f\"C3 — Diurnal drivers — {property_one['property_id']} ({property_one['name']})\")\n",
    "    plt.tight_layout(); plt.show()\n",
    "\n",
    "top_n[['temp_rank','property_id','name','peak_temp_c',\n",
    "       'peak_heat_index_c','peak_apparent_temp_c','hours_above_sla']]"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "step9-md",
   "metadata": {},
   "source": [
    "---\n",
    "## Step 9 — Composite scores (risk + opportunity)\n",
    "\n",
    "### What you are doing\n",
    "Two scores, both 0–1, both min-max-normalized on the analyzed subset:\n",
    "\n",
    "- **`heat_risk_score`** = `0.40·peak_temp + 0.20·impervious + 0.20·peak_HI + 0.20·hours_above_SLA` — *which assets are exposed today.*\n",
    "- **`opportunity_score`** = `0.50·peak_temp + 0.30·impervious + 0.20·veg_deficit` — *which assets have the most headroom for cooling investment.*\n",
    "\n",
    "### Why this matters\n",
    "The investment committee wants one number per asset for risk *and* one for upside. Two scores answer two different questions: which to flag, and which to treat. The agent uses them together — high risk + high opportunity = treat now; high risk + low opportunity = divest; low risk + high opportunity = hold and watch."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "step9-code",
   "metadata": {},
   "outputs": [],
   "source": [
    "def _mm(s):\n",
    "    s = pd.Series(s).astype(float)\n",
    "    lo, hi = s.min(skipna=True), s.max(skipna=True)\n",
    "    if pd.isna(lo) or pd.isna(hi) or hi == lo:\n",
    "        return s * 0.0\n",
    "    return (s - lo) / (hi - lo)\n",
    "\n",
    "analyzed = top_n.dropna(subset=['impervious_pct', 'vegetation_pct',\n",
    "                                 'peak_heat_index_c', 'hours_above_sla']).copy()\n",
    "if len(analyzed) < 2:\n",
    "    print(f\"⚠ Analyzed subset has {len(analyzed)} property — scores are not comparable \"\n",
    "          f\"across assets in this run. Set CACHED=False or expand cached coverage \"\n",
    "          f\"to score the full top-{TOP_N_TO_ENRICH}.\")\n",
    "\n",
    "temp_n  = _mm(analyzed['peak_temp_c'])\n",
    "imp_n   = _mm(analyzed['impervious_pct'])\n",
    "hi_n    = _mm(analyzed['peak_heat_index_c'])\n",
    "sla_n   = _mm(analyzed['hours_above_sla'])\n",
    "veg_def = _mm(100.0 - analyzed['vegetation_pct'])\n",
    "\n",
    "analyzed['heat_risk_score']   = (0.40*temp_n + 0.20*imp_n + 0.20*hi_n + 0.20*sla_n).round(3)\n",
    "analyzed['opportunity_score'] = (0.50*temp_n + 0.30*imp_n + 0.20*veg_def).round(3)\n",
    "\n",
    "top_n = top_n.merge(\n",
    "    analyzed[['property_id','heat_risk_score','opportunity_score']],\n",
    "    on='property_id', how='left',\n",
    ")\n",
    "\n",
    "top_n[['temp_rank','property_id','name','peak_temp_c',\n",
    "       'impervious_pct','vegetation_pct','peak_heat_index_c','hours_above_sla',\n",
    "       'heat_risk_score','opportunity_score']]"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "step10-md",
   "metadata": {},
   "source": [
    "---\n",
    "## Step 10 — Business translation + investment summary\n",
    "\n",
    "### What you are doing\n",
    "Translating the technical numbers into the four outputs the agent's client actually cares about:\n",
    "\n",
    "- **Cooling OpEx uplift (USD / yr)** — `(Δ°C above 24) × sqft × 0.18 kWh/sf/°C × $0.24/kWh`. Triage-grade, defensible at a meeting.\n",
    "- **Insurance risk tier** A / B / C — percentile buckets on `heat_risk_score`.\n",
    "- **Tenant-comfort SLA flag** — boolean, flips when peak heat index is above 32 °C.\n",
    "- **Final ranked map M3 + risk-vs-opportunity scatter C4 + diurnal curves C1.**\n",
    "\n",
    "### Why this matters\n",
    "“Property X has a heat-risk score of 0.82” is a modeling statement. “Property X is in tier C, carries ~$58 k/yr in avoidable cooling OpEx, and will breach the comfort SLA on design-peak days” is a decision."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "step10-code",
   "metadata": {},
   "outputs": [],
   "source": [
    "def _opex_uplift(peak_temp_c, sqft):\n",
    "    if pd.isna(peak_temp_c): return None\n",
    "    delta = max(0.0, peak_temp_c - BASELINE_C)\n",
    "    return round(delta * sqft * COOLING_KWH_PER_SF * KWH_PRICE_USD, 0)\n",
    "\n",
    "def _tier(score):\n",
    "    if pd.isna(score): return 'unranked'\n",
    "    if score >= 0.67:  return 'C'\n",
    "    if score >= 0.33:  return 'B'\n",
    "    return 'A'\n",
    "\n",
    "def _comfort_flag(hi):\n",
    "    if pd.isna(hi): return None\n",
    "    return bool(hi > SLA_HI_C)\n",
    "\n",
    "portfolio = portfolio.merge(\n",
    "    top_n[['property_id','impervious_pct','vegetation_pct',\n",
    "           'peak_heat_index_c','peak_apparent_temp_c','hours_above_sla',\n",
    "           'peak_solar_irradiance','heat_risk_score','opportunity_score']],\n",
    "    on='property_id', how='left',\n",
    ")\n",
    "portfolio['cooling_opex_uplift_usd'] = portfolio.apply(\n",
    "    lambda r: _opex_uplift(r.peak_temp_c, r.sqft), axis=1)\n",
    "portfolio['insurance_tier']   = portfolio['heat_risk_score'].apply(_tier)\n",
    "portfolio['comfort_sla_risk'] = portfolio['peak_heat_index_c'].apply(_comfort_flag)\n",
    "\n",
    "out_cols = [\n",
    "    'temp_rank','property_id','name','type','sqft','market_value_musd',\n",
    "    'peak_temp_c','peak_hour','diurnal_swing_c','aoi_percentile',\n",
    "    'impervious_pct','vegetation_pct','peak_heat_index_c','hours_above_sla',\n",
    "    'heat_risk_score','opportunity_score',\n",
    "    'cooling_opex_uplift_usd','insurance_tier','comfort_sla_risk',\n",
    "]\n",
    "portfolio[out_cols].to_csv(OUTPUT_CSV, index=False)\n",
    "print(f\"Saved → {OUTPUT_CSV}\")\n",
    "print(f\"Aggregate avoidable cooling OpEx: $\"\n",
    "      f\"{portfolio['cooling_opex_uplift_usd'].sum():,.0f} / year\")\n",
    "portfolio[out_cols]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "step10-visuals-code",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Map M3 — final ranked priority map\n",
    "m3 = folium.Map(location=center, zoom_start=14, tiles='cartodbpositron')\n",
    "for poly, _, peak_c, _, _ in overlay_tiles:\n",
    "    folium.GeoJson(\n",
    "        mapping(poly),\n",
    "        style_function=lambda x: {\n",
    "            'fillColor': '#d73027', 'color': '#d73027',\n",
    "            'weight': 0, 'fillOpacity': 0.20,\n",
    "        },\n",
    "    ).add_to(m3)\n",
    "for _, p in portfolio.iterrows():\n",
    "    score = p.heat_risk_score if pd.notna(p.heat_risk_score) else 0.0\n",
    "    color = '#d73027' if score >= 0.67 else ('#fee090' if score >= 0.33 else '#1a9850')\n",
    "    folium.CircleMarker(\n",
    "        location=[p.latitude, p.longitude],\n",
    "        radius=6 + score * 14,\n",
    "        color='black', weight=1,\n",
    "        fill=True, fill_color=color, fill_opacity=0.9,\n",
    "        popup=(f\"<b>#{int(p.temp_rank)} {p['name']}</b><br/>\"\n",
    "               f\"risk: {p.heat_risk_score if pd.notna(p.heat_risk_score) else 'n/a'}<br/>\"\n",
    "               f\"opportunity: {p.opportunity_score if pd.notna(p.opportunity_score) else 'n/a'}<br/>\"\n",
    "               f\"OpEx uplift: ${(p.cooling_opex_uplift_usd or 0):,.0f}/yr<br/>\"\n",
    "               f\"tier: {p.insurance_tier}, SLA risk: {p.comfort_sla_risk}\"),\n",
    "    ).add_to(m3)\n",
    "display(m3)\n",
    "\n",
    "# Chart C4 — Risk vs Opportunity scatter (4 quadrants for the agent)\n",
    "scored = portfolio.dropna(subset=['heat_risk_score', 'opportunity_score'])\n",
    "if len(scored):\n",
    "    fig, ax = plt.subplots(figsize=(7, 6))\n",
    "    ax.scatter(scored['heat_risk_score'], scored['opportunity_score'],\n",
    "               s=80, c='#1f77b4', edgecolor='black')\n",
    "    for _, r in scored.iterrows():\n",
    "        ax.annotate(r['property_id'], (r['heat_risk_score'], r['opportunity_score']),\n",
    "                    xytext=(5, 5), textcoords='offset points', fontsize=9)\n",
    "    ax.axvline(0.5, color='#888', linewidth=1)\n",
    "    ax.axhline(0.5, color='#888', linewidth=1)\n",
    "    ax.set_xlim(-0.05, 1.05); ax.set_ylim(-0.05, 1.05)\n",
    "    ax.set_xlabel('Heat-risk score →')\n",
    "    ax.set_ylabel('Opportunity score →')\n",
    "    ax.set_title('C4 — Risk vs Opportunity (4 quadrants)')\n",
    "    ax.text(0.02, 0.98, 'Hold',   transform=ax.transAxes, fontsize=10, color='#666', va='top')\n",
    "    ax.text(0.98, 0.98, 'Treat',  transform=ax.transAxes, fontsize=10, color='#666', va='top', ha='right')\n",
    "    ax.text(0.02, 0.02, 'Watch',  transform=ax.transAxes, fontsize=10, color='#666', va='bottom')\n",
    "    ax.text(0.98, 0.02, 'Divest', transform=ax.transAxes, fontsize=10, color='#666', va='bottom', ha='right')\n",
    "    plt.tight_layout(); plt.show()\n",
    "\n",
    "# Chart C1 — Diurnal temperature curves for the analyzed subset\n",
    "analyzed_pids = list(env_data.keys()) or list(top_n['property_id'].head(TOP_N_TO_ENRICH))\n",
    "fig, ax = plt.subplots(figsize=(9, 4))\n",
    "for _, p in portfolio[portfolio['property_id'].isin(analyzed_pids)].iterrows():\n",
    "    poly, hourly_c, peak_c, peak_h, min_c = tile_for(p.latitude, p.longitude)\n",
    "    ax.plot(range(24), hourly_c, label=f\"{p['property_id']} {p['name']}\")\n",
    "ax.axhline(BASELINE_C, color='#888', linestyle='--', linewidth=1, label=f'baseline {BASELINE_C}°C')\n",
    "ax.set_xlabel('Hour of day'); ax.set_ylabel('°C')\n",
    "ax.set_title('C1 — Diurnal surface temperature — analyzed subset')\n",
    "ax.legend(loc='lower right', fontsize=8)\n",
    "plt.tight_layout(); plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "wrapup-md",
   "metadata": {},
   "source": [
    "---\n",
    "## Wrap-up\n",
    "\n",
    "Starting from a real-estate portfolio CSV you now have evidence-based answers for the client meeting:\n",
    "\n",
    "| Artifact | Used by |\n",
    "|----------|---------|\n",
    "| **M1** portfolio overview map | Client deck — slide 1 |\n",
    "| **M2** hot-exposures zoom map | Client deck — slide 2 |\n",
    "| **M3** final ranked priority map | Client deck — slide 3 |\n",
    "| **C1** diurnal temperature curves | Backup / analyst review |\n",
    "| **C2** surface composition stacked bar | Backup |\n",
    "| **C3** HI / apparent / RH / solar profile (#1) | Deep-dive slide |\n",
    "| **C4** risk vs opportunity scatter (4 quadrants) | Decision slide |\n",
    "| `outputs/portfolio_evaluation.csv` | CRM / client report |\n",
    "| [Heat-intelligence PDF report](../../data/real_state_san_jose_heat_intelligence_sample_day_2024-10-02.pdf) | Forward to client unchanged |\n",
    "\n",
    "Every input is explicit. Every weight is at the top of the notebook. Set `CACHED=False` to rerun against any portfolio with a live FortyGuard API key — the same workflow applies, with the caveat that diurnal columns reduce to the snapshot hour until a 24-hour live API is available.\n",
    "\n",
    "**Apply this pattern to adjacent use cases**: insured-properties portfolio (insurance underwriting), data-center sites (operational-risk screening), hospitality assets (guest-comfort benchmarking), retail acquisitions (foot-traffic comfort). The workflow — *portfolio × diurnal heatmap × surface diagnosis × ground-truth × env-params → risk + opportunity table* — transfers directly."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
```

Note: the JSON file content above must be written **exactly** to the notebook path. Use the Write tool's `file_path` and `content` parameters; do not wrap the content in any extra encoding.

- [ ] **Step 2: Verify the file was written and parses as valid JSON**

Run:
```bash
python -c "import json; nb=json.load(open('c:/development/fortyguard/repositories/temperature-api-quickstart/notebooks/use_cases/real_estate_portfolio_heat_risk.ipynb','r',encoding='utf-8')); print('cells:', len(nb['cells']), 'nbformat:', nb['nbformat'], 'minor:', nb['nbformat_minor'])"
```

Expected output exactly: `cells: 22 nbformat: 4 minor: 5`

If the cell count is wrong, the JSON is corrupt — re-run Step 1.

- [ ] **Step 3: Verify cell IDs are unique and step ordering is correct**

Run:
```bash
python -c "
import json
nb = json.load(open('c:/development/fortyguard/repositories/temperature-api-quickstart/notebooks/use_cases/real_estate_portfolio_heat_risk.ipynb','r',encoding='utf-8'))
ids = [c['id'] for c in nb['cells']]
assert len(ids) == len(set(ids)), f'duplicate ids: {ids}'
expected = ['intro-md','setup-md','setup-code','step1-md','step1-code','step2-md','step2-code','step3-md','step3-code','step4-md','step4-code','step5-md','step5-code','step6-md','step6-code','step7-md','step7-code','step8-md','step8-code','step9-md','step9-code','step10-md','step10-code','step10-visuals-code','wrapup-md']
print('id_count:', len(ids), 'expected:', len(expected))
"
```

Expected: `id_count: 25 expected: 25` — wait, this is wrong. The JSON above has only 22 cells. Recount and adjust.

**Correction**: count the cells listed in the JSON. The cells are: intro-md, setup-md, setup-code, step1-md, step1-code, step2-md, step2-code, step3-md, step3-code, step4-md, step4-code, step5-md, step5-code, step6-md, step6-code, step7-md, step7-code, step8-md, step8-code, step9-md, step9-code, step10-md, step10-code, step10-visuals-code, wrapup-md = **25 cells**.

Re-run with the correct expected count. Replace the verification command with:
```bash
python -c "
import json
nb = json.load(open('c:/development/fortyguard/repositories/temperature-api-quickstart/notebooks/use_cases/real_estate_portfolio_heat_risk.ipynb','r',encoding='utf-8'))
ids = [c['id'] for c in nb['cells']]
assert len(ids) == len(set(ids)), f'duplicate ids: {ids}'
print('cells:', len(ids))
print('ids:', ids)
"
```

Expected: `cells: 25` and the printed list matches the order intro-md → wrapup-md.

If cell count or order is wrong, fix the JSON in Step 1 and re-run.

---

## Task 3: End-to-end smoke test (CACHED=True)

**Files:**
- Modify (executed): `notebooks/use_cases/real_estate_portfolio_heat_risk.ipynb` (writes back execution counts and outputs)
- Create: `outputs/portfolio_evaluation.csv`

- [ ] **Step 1: Execute the notebook end-to-end via nbconvert**

Run:
```bash
cd c:/development/fortyguard/repositories/temperature-api-quickstart && jupyter nbconvert --to notebook --execute notebooks/use_cases/real_estate_portfolio_heat_risk.ipynb --output real_estate_portfolio_heat_risk.ipynb --ExecutePreprocessor.timeout=300
```

Expected: `[NbConvertApp] Writing N bytes to ...` with no Python tracebacks. Execution should complete in 60–180 seconds (the heatmap geojson is 17 MB and 16,507-tile point-in-polygon takes time).

If execution fails:
- **`AssertionError: F→C sanity check failed`** — the geojson temperature scale is unexpected; inspect a sample tile property and adjust `TEMP_C_SANITY` only if the values are genuinely out of the (15, 55) °C range. Do not commit a relaxed range without confirming the source data.
- **`KeyError` on `'00'..'23'`** — the geojson tile properties don't have the expected keys; inspect the file structure and adjust the loader. (This shouldn't happen — the file was inspected in brainstorming.)
- **Slow execution / timeout** — increase `--ExecutePreprocessor.timeout=600`.

- [ ] **Step 2: Verify the output CSV exists, has 19 columns and 10 rows**

Run:
```bash
python -c "
import pandas as pd
df = pd.read_csv('c:/development/fortyguard/repositories/temperature-api-quickstart/outputs/portfolio_evaluation.csv')
print('rows:', len(df), 'cols:', len(df.columns))
print('columns:', list(df.columns))
expected_cols = ['temp_rank','property_id','name','type','sqft','market_value_musd','peak_temp_c','peak_hour','diurnal_swing_c','aoi_percentile','impervious_pct','vegetation_pct','peak_heat_index_c','hours_above_sla','heat_risk_score','opportunity_score','cooling_opex_uplift_usd','insurance_tier','comfort_sla_risk']
assert list(df.columns) == expected_cols, 'column mismatch'
assert len(df) == 10, f'row count {len(df)}'
print('OK')
"
```

Expected output exactly: ends with `OK`. The printed `columns:` line should match the `expected_cols` list verbatim.

- [ ] **Step 3: Spot-check the data sanity**

Run:
```bash
python -c "
import pandas as pd
df = pd.read_csv('c:/development/fortyguard/repositories/temperature-api-quickstart/outputs/portfolio_evaluation.csv')
# peak temps in plausible range
assert (df['peak_temp_c'] >= 15).all() and (df['peak_temp_c'] <= 55).all(), 'peak_temp_c out of range'
# peak_hour 0..23
assert (df['peak_hour'] >= 0).all() and (df['peak_hour'] <= 23).all(), 'peak_hour out of range'
# diurnal_swing_c >= 0
assert (df['diurnal_swing_c'] >= 0).all(), 'negative diurnal_swing'
# aoi_percentile 0..100
assert (df['aoi_percentile'] >= 0).all() and (df['aoi_percentile'] <= 100).all(), 'aoi_percentile out of range'
# At least P01 has impervious + vegetation populated (cached path)
p01 = df[df['property_id'] == 'P01']
assert len(p01) == 1, 'P01 missing'
assert pd.notna(p01['impervious_pct'].iloc[0]), 'P01 impervious_pct is NaN'
assert pd.notna(p01['vegetation_pct'].iloc[0]), 'P01 vegetation_pct is NaN'
# Insurance tier in {A,B,C,unranked}
assert df['insurance_tier'].isin({'A','B','C','unranked'}).all(), 'unknown tier'
print('OK')
"
```

Expected output exactly: `OK`.

- [ ] **Step 4: Confirm cell outputs were materialized in the .ipynb**

Run:
```bash
python -c "
import json
nb = json.load(open('c:/development/fortyguard/repositories/temperature-api-quickstart/notebooks/use_cases/real_estate_portfolio_heat_risk.ipynb','r',encoding='utf-8'))
code_cells = [c for c in nb['cells'] if c['cell_type'] == 'code']
print('code cells:', len(code_cells))
for c in code_cells:
    out_count = len(c.get('outputs', []))
    ec = c.get('execution_count')
    print(f'  id={c[\"id\"]:<22}  exec_count={ec}  outputs={out_count}')
"
```

Expected: every code cell has `execution_count` non-None (e.g., 1..11) and at least one entry in `outputs`. The notebook with materialized outputs is part of the deliverable.

---

## Task 4: Spot-check the visual artifacts

**Files:**
- Read: `notebooks/use_cases/real_estate_portfolio_heat_risk.ipynb` (cell outputs)

- [ ] **Step 1: Confirm M1, M2, M3 (folium maps) rendered**

Run:
```bash
python -c "
import json
nb = json.load(open('c:/development/fortyguard/repositories/temperature-api-quickstart/notebooks/use_cases/real_estate_portfolio_heat_risk.ipynb','r',encoding='utf-8'))
folium_cells = ['step4-code', 'step5-code', 'step10-visuals-code']
for cid in folium_cells:
    cell = next(c for c in nb['cells'] if c.get('id') == cid)
    outs = cell.get('outputs', [])
    has_html = any('text/html' in (o.get('data') or {}) for o in outs)
    has_iframe_or_folium = any(
        'folium' in str(o.get('data', {})).lower() or 'leaflet' in str(o.get('data', {})).lower()
        for o in outs
    )
    print(f'{cid}: html={has_html} folium/leaflet markers={has_iframe_or_folium}')
"
```

Expected: each of `step4-code`, `step5-code`, `step10-visuals-code` shows `html=True folium/leaflet markers=True` (the folium HTML embeds Leaflet references).

- [ ] **Step 2: Confirm C1, C2, C3, C4 (matplotlib charts) rendered**

Run:
```bash
python -c "
import json
nb = json.load(open('c:/development/fortyguard/repositories/temperature-api-quickstart/notebooks/use_cases/real_estate_portfolio_heat_risk.ipynb','r',encoding='utf-8'))
chart_cells = ['step6-code', 'step8-code', 'step10-visuals-code']
for cid in chart_cells:
    cell = next(c for c in nb['cells'] if c.get('id') == cid)
    outs = cell.get('outputs', [])
    has_png = any('image/png' in (o.get('data') or {}) for o in outs)
    print(f'{cid}: image/png={has_png}')
"
```

Expected: each cell shows `image/png=True`. (The `step10-visuals-code` cell contains C4 and C1 — both should render as PNG outputs.)

- [ ] **Step 3: Confirm street-view side-by-side rendered**

Run:
```bash
python -c "
import json
nb = json.load(open('c:/development/fortyguard/repositories/temperature-api-quickstart/notebooks/use_cases/real_estate_portfolio_heat_risk.ipynb','r',encoding='utf-8'))
cell = next(c for c in nb['cells'] if c.get('id') == 'step7-code')
outs = cell.get('outputs', [])
html_outs = [o for o in outs if 'text/html' in (o.get('data') or {})]
has_data_image = any('data:image/jpeg;base64' in str(o.get('data', {}).get('text/html', '')) for o in html_outs)
print('step7-code has base64 image embed:', has_data_image)
"
```

Expected: `step7-code has base64 image embed: True`. (Cached path embeds two base64 JPEG images side-by-side.)

---

## Task 5: Verify the bus-stop and tree notebooks are byte-identical to pre-change versions

**Files:**
- Read-only verification: `notebooks/use_cases/urban_planner_bus_stop_prioritization.ipynb`, `notebooks/use_cases/urban_forestry_tree_prioritization.ipynb`

- [ ] **Step 1: Confirm no other notebooks were modified**

Run:
```bash
git -C c:/development/fortyguard/repositories/temperature-api-quickstart status --short notebooks/use_cases/
```

Expected: only `M  notebooks/use_cases/real_estate_portfolio_heat_risk.ipynb` is shown (or `??` if not yet tracked). The tree notebook and bus-stop notebook must NOT appear.

If either of the two reference notebooks shows up as modified, **stop** and revert them with:
```bash
git -C c:/development/fortyguard/repositories/temperature-api-quickstart checkout -- notebooks/use_cases/urban_planner_bus_stop_prioritization.ipynb notebooks/use_cases/urban_forestry_tree_prioritization.ipynb
```

Then investigate why they were touched and re-run from Task 2 Step 1.

---

## Task 6: Commit

**Files:**
- Stage: `notebooks/use_cases/real_estate_portfolio_heat_risk.ipynb`
- Stage: `outputs/portfolio_evaluation.csv` (only if outputs/ is tracked; otherwise leave it out — see Step 1)
- Stage: `data/real_estate_san_jose_portfolio_sample.csv`, the four `data/real_state_san_jose_*.json/geojson` files, and the PDF, since they are referenced by the notebook
- Do NOT stage: `data/sample_real_estate_portfolio.csv` deletion (that's pre-existing and unrelated to this commit — handle it in a separate change)

- [ ] **Step 1: Decide whether to track `outputs/`**

Run:
```bash
git -C c:/development/fortyguard/repositories/temperature-api-quickstart check-ignore -v outputs/portfolio_evaluation.csv 2>&1; echo "exitcode=$?"
```

If the output is `exitcode=0` with a `.gitignore` rule, the file is ignored — don't stage it. If `exitcode=1` (no rule), check if any other `outputs/*.csv` is currently tracked:
```bash
git -C c:/development/fortyguard/repositories/temperature-api-quickstart ls-files outputs/
```

If outputs/ is tracked, include `outputs/portfolio_evaluation.csv`. If not tracked and not ignored, leave it out of the commit (the notebook regenerates it on every run; tracking it adds churn without value).

- [ ] **Step 2: Stage the notebook and the data files referenced by the new workflow**

Run:
```bash
git -C c:/development/fortyguard/repositories/temperature-api-quickstart add notebooks/use_cases/real_estate_portfolio_heat_risk.ipynb data/real_estate_san_jose_portfolio_sample.csv data/real_state_san_jose_heatmap_sample_day_2024-10-02.geojson data/real_state_san_jose_satellite_segmentation_sample_day_2024-10-02.json data/real_state_san_jose_street_view_segmentation_sample_day_2024-10-02.json data/real_state_san_jose_env_paramaters_sample_day_2024-10-02.json data/real_state_san_jose_heat_intelligence_sample_day_2024-10-02.pdf
```

Then:
```bash
git -C c:/development/fortyguard/repositories/temperature-api-quickstart status --short
```

Expected: the seven added files marked `A`/`AM`, the modified notebook marked `M`. The `data/sample_real_estate_portfolio.csv` deletion remains unstaged (` D`) — leave it for a separate change.

- [ ] **Step 3: Create the commit**

Run:
```bash
git -C c:/development/fortyguard/repositories/temperature-api-quickstart commit -m "$(cat <<'EOF'
Rewrite real-estate portfolio notebook into 10-step heat evaluation

Adds CACHED=True default for offline demo, full 24-hour diurnal analysis,
opportunity score alongside heat-risk score, street-view ground-truth step,
4-quadrant risk-vs-opportunity scatter, and a final priority CSV at
outputs/portfolio_evaluation.csv. Per the design spec at
docs/superpowers/specs/2026-04-28-real-estate-portfolio-evaluation-design.md.

The bus-stop and tree notebooks are unchanged.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected: a single commit, ~7 files changed (notebook + 6 data files), no errors.

- [ ] **Step 4: Verify the commit**

Run:
```bash
git -C c:/development/fortyguard/repositories/temperature-api-quickstart log --oneline -1 && git -C c:/development/fortyguard/repositories/temperature-api-quickstart show --stat HEAD
```

Expected: a new commit with the message above; `--stat` shows ~7 files changed.

---

## Self-Review

### 1. Spec coverage

Walking the spec sections against the plan:

- **§1 Audience and goal** → Cell `intro-md` (Task 2, Step 1) leads with real-estate agent. ✓
- **§2 Scope** → File Structure section + Task 5 verifies tree/bus-stop untouched. ✓
- **§3 Inputs** → All six paths declared in `setup-code`. ✓
- **§4 Configuration constants** → `setup-code` sets `STUDY_DATE`, `STUDY_HOUR`, `GRANULARITY_M`, `TOP_N_TO_ENRICH`, `CACHED`, `BASELINE_C`, `COOLING_KWH_PER_SF`, `KWH_PRICE_USD`, `SLA_HI_C`, `TEMP_C_SANITY`, `ASSET_TYPE_PALETTE`. ✓
- **§5 Step 1 — Load portfolio** → cells `step1-md`, `step1-code`. ✓
- **§5 Step 2 — Heat layer** → cells `step2-md`, `step2-code` (online + cached duals, F→C, sanity assert, `tile_for` helper, AOI bounds). ✓
- **§5 Step 3 — Diurnal attach** → cells `step3-md`, `step3-code` (peak/hour/min/swing/aoi_percentile + temp_rank). ✓
- **§5 Step 4 — Map M1** → cells `step4-md`, `step4-code` (radius scales with peak, palette, popup, legend). ✓
- **§5 Step 5 — Map M2** → cells `step5-md`, `step5-code` (median filter, p90 underlay capped at 500 tiles, zoom). ✓
- **§5 Step 6 — Satellite** → cells `step6-md`, `step6-code` (online + cached duals, IMPERV/VEGGIE buckets, C2). ✓
- **§5 Step 7 — Street view** → cells `step7-md`, `step7-code` (online + cached duals, "#1" defined as enriched-subset top, side-by-side base64 HTML, imagery date). ✓
- **§5 Step 8 — env-params** → cells `step8-md`, `step8-code` (online + cached duals, peak HI/apparent/hours_above_sla/peak_solar, C3 2-row subplot with twin-RH-axis). ✓
- **§5 Step 9 — Composite scores** → cells `step9-md`, `step9-code` (heat_risk weights `0.40/0.20/0.20/0.20`, opportunity weights `0.50/0.30/0.20`, single-property notice). ✓
- **§5 Step 10 — Business translation** → cells `step10-md`, `step10-code` (OpEx, tier, comfort flag, CSV write); `step10-visuals-code` (M3 + C4 + C1). ✓
- **§5 Wrap-up** → cell `wrapup-md` with artifact table and PDF link. ✓
- **§6 Outputs** → All M1/M2/M3, C1–C4, T1/T2/T3, L1 produced. Verified in Task 4. ✓
- **§7 File-mode contract** → CACHED=True default in `setup-code`; per-step `if CACHED` branches; online-mode banner in `step2-code` warning that diurnal collapses. ✓
- **§8 Data-quality assumptions** → Q1 (F→C + sanity assert: `step2-code`), Q2 (P01-only notice: `step6-code`/`step8-code`), Q3 (verbatim paths in `setup-code`), Q4 (image_date printed: `step7-code`), Q5 (`COOLING_KWH_PER_SF` constant exposed at top), Q6 (`STUDY_DATE='2024-10-02'`), Q7 (AOI from geojson bounds in cached, SAN_JOSE_POLYGON in online). ✓
- **§9 Acceptance criteria** → Verified via Tasks 3 (criteria 1, 2, 4, 5, 6 — note 6 is online-only and out of scope for this run with `CACHED=True`), 4 (criterion 1 visuals), 5 (criterion 7). ✓

**Note on Acceptance Criterion 6** ("Setting `CACHED=False` and rerunning Steps 1, 2a, and 3–10 succeeds against a live API key"): the smoke test in Task 3 runs `CACHED=True` only. Live-mode verification requires a `.env` with API credentials and is **not** part of this plan. If a live verification is needed, run the notebook manually with `CACHED=False` after merging.

### 2. Placeholder scan

- No `TBD`, `TODO`, `implement later`, `fill in details` strings anywhere in the plan. ✓
- Every step has either complete code or a complete shell command. ✓
- "Add appropriate error handling" — not present. ✓
- "Similar to Task N" — not present (each task is self-contained). ✓

### 3. Type / name consistency

- `tile_for(lat, lon)` defined in `step2-code` is used unchanged in `step3-code` and `step10-visuals-code`. ✓
- `_mm()` defined in `step9-code` (notebook variable, not Python module). ✓
- `seg_data` (dict) is defined in `step6-code` and read in `step7-code` and `step9-code`. ✓
- `env_data` (dict) is defined in `step8-code` and read in `step9-code` and `step10-visuals-code`. ✓
- `top_n` is defined in `step6-code` and merged/extended through `step8-code`, `step9-code`, `step10-code`. ✓
- `portfolio` carries through `step1-code` → `step3-code` (sort + temp_rank inserted) → `step10-code` (merge + business columns). ✓
- `overlay_tiles` defined in `step5-code` and reused in `step10-visuals-code` (M3 underlay). ✓
- `property_one` defined in `step7-code` and reused in `step8-code` (chart C3). ✓
- All 19 CSV columns in Task 3 Step 2 verification match the columns built in `step10-code`. ✓
- `step10-visuals-code` cell ID is consistent across Tasks 2, 3, 4. ✓

No drift detected.

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-04-28-real-estate-portfolio-evaluation.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration.

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints.

**Which approach?**
