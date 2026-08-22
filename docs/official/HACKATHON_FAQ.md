# ❓ FortyGuard Hackathon '26 - Comprehensive Master FAQ

> **Official Event Knowledge Base & Slack Q&A Synthesis**  
> Compiled from official FortyGuard announcements, mentor & organizer answers, and all real-time debugging threads across `#announcements`, `#help-general`, and `#help-technical`.

---

## 📑 Table of Contents
1. [Official Links & Submission Portals](#-1-official-links--submission-portals)
2. [Dates, Deadlines & Schedule](#-2-dates-deadlines--schedule)
3. [Prizes & Awards](#-3-prizes--awards)
4. [Team Management, Teammates & Channel Setup](#-4-team-management-teammates--channel-setup)
5. [API Access, Key Generation & Credit Quotas](#-5-api-access-key-generation--credit-quotas)
6. [Geographic Coverage & Temporal Range](#-6-geographic-coverage--temporal-range)
7. [Project Scope, Eligibility & Tech Stacks](#-7-project-scope-eligibility--tech-stacks)
8. [API Endpoints, Parameters & Payload Schemas](#-8-api-endpoints-parameters--payload-schemas)
9. [Batch Requests & Parallel Execution Patterns](#-9-batch-requests--parallel-execution-patterns)
10. [Async Polling Lifecycle & Non-Obvious Production Gotchas](#-10-async-polling-lifecycle--non-obvious-production-gotchas)
11. [Analytics Types & Visualizations](#-11-analytics-types--visualizations)
12. [The 7 Challenge Tracks & Project Concepts](#-12-the-7-challenge-tracks--project-concepts)
13. [Code Reuse & Boilerplate Policy (Quickstart & Webinars)](#-13-code-reuse--boilerplate-policy)
14. [Building ML Models, Datasets & Agentic AI (Tracks 5, 6, 7)](#-14-building-ml-models-datasets--agentic-ai)
15. [Third-Party LLM Keys, External Data & Caching](#-15-third-party-llm-keys-external-data--caching)
16. [Project Pivots, Track Changes & Resubmissions](#-16-project-pivots-track-changes--resubmissions)
17. [Final Submission Requirements & Judging Rubric](#-17-final-submission-requirements--judging-rubric)
18. [Workshop & Live Session Summaries](#-18-workshop--live-session-summaries)
19. [Troubleshooting & HTTP Status Code Reference](#-19-troubleshooting--http-status-code-reference)

---

## 🌐 1. Official Links & Submission Portals

| Portal / Resource | Link | Description |
| :--- | :--- | :--- |
| **Official Submission Form** | [forms.gle/jLgBzVTG1NhJ3gNe6](https://forms.gle/jLgBzVTG1NhJ3gNe6) | **Final submission portal** (due 30 August 2026, 11:59 PM GST). |
| **Team Channel Setup Form** | [forms.gle/CCCvSNgDsDiNZ2gk7](https://forms.gle/CCCvSNgDsDiNZ2gk7) | Team leaders fill this out to auto-create a private Slack channel with the bot & organizers. |
| **Event Website** | [fortyguard.com/hackathon26](https://www.fortyguard.com/hackathon26) | Official hackathon overview, schedule, and details. |
| **Temperature Dashboard (GUI)** | [dashboard.fortyguard.com](https://dashboard.fortyguard.com) | Interactive web UI to draw polygons, explore heatmaps, generate PDF reports, and create API keys. |
| **API Documentation & Swagger** | [docs-api.fortyguard.com/docs](https://docs-api.fortyguard.com/docs) | Official interactive API reference and credit calculator. |
| **Quickstart GitHub Repository** | [FortyGuard-Tech/temperature-api-quickstart](https://github.com/FortyGuard-Tech/temperature-api-quickstart) | Official Python SDK & Jupyter Notebooks with pre-cached fixtures (`CACHED=True`). |
| **Participant Handbook (PDF)** | [Google Drive Link](https://drive.google.com/file/d/1GPAke_0Nez8vaRFs_gqzUsZmQoptsjL3/view?usp=sharing) | Full quickstart, sample notebooks & track details. |
| **Technical Support Email** | `support@fortyguard.com` | Contact for API bugs, credit issues, and endpoint errors. |
| **General Inquiries Email** | `hackathon@fortyguard.com` | Contact for registration, team modifications, and rules. |

---

## ⏱️ 2. Dates, Deadlines & Schedule

### Q: When does the hackathon run?
* **Build Window:** Opens **18 August 2026 at 12:00 AM GST** and closes **30 August 2026 at 11:59 PM GST**.
* **Format:** Fully online and global.

### Q: What is the exact submission deadline?
* **Deadline:** **30 August 2026, 11:59 PM GST (UTC+4)**.
* **Late Policy:** **Strict cutoff** - the submission form closes automatically, and late submissions will not be accepted. Submit with time to spare.

### Q: Where do I check for official schedule updates?
* `#announcements` in Slack is the single authoritative source of truth.

---

## 🎁 3. Prizes & Awards

### Q: What prizes are awarded to winning teams?
* **Total Cash Prize Pool:** **$6,000 USD**
  * 🥇 **1st Place:** **$3,000** + NVIDIA Jetson AI Developer Kit
  * 🥈 **2nd Place:** **$2,000** + NVIDIA Jetson AI Developer Kit
  * 🥉 **3rd Place:** **$1,000** + NVIDIA Jetson AI Developer Kit
* **NVIDIA Jetson AI Developer Kit Hardware:**
  * Up to 67 TOPS AI performance, 1,024 CUDA + 32 Tensor cores, 6-core Arm Cortex-A78AE CPU, 8 GB LPDDR5 RAM.
* **Additional Winner Perks:**
  * **Incubation:** Acceleration pathways with partner programs.
  * **Career:** Internship and project opportunities with FortyGuard.
  * **Platform:** FortyGuard API discounts and ongoing credit access.
  * **All Participants:** Official verified certificate of completion and shareable digital builder badge.

---

## 👥 4. Team Management, Teammates & Channel Setup

### Q: How big can a team be?
* **1 to 3 people.** Solo entries are 100% welcome and eligible for all awards.

### Q: Does listing a teammate on the Team Registration Form automatically register them?
* **No.** Listing someone on the team channel form does **not** automatically register them for the hackathon.
* **Required Dual Registration Process:**
  1. Each teammate must first register independently on the main hackathon website (`https://www.fortyguard.com/hackathon-registration`) to receive a Slack invite and official enrollment.
  2. Each member creates a free account at [dashboard.fortyguard.com](https://dashboard.fortyguard.com) to generate their API key.
  3. The team leader submits the [Team Channel Setup Form](https://forms.gle/CCCvSNgDsDiNZ2gk7) with all registered members' emails and Slack handles.

### Q: What should I do if my assigned teammates are unresponsive?
* If assigned teammates do not reply to emails or Slack DMs:
  1. You may choose to proceed as a **Solo participant** (1 person).
  2. Or post in the **`#looking-for-team`** Slack channel to team up with active builders.
* You do not need admin approval to change teammates - simply submit the final project submission form with the active team members.

### Q: How do teammates join Slack if their invite link expired?
* Request an invite through Slack's built-in workspace invitation request tool or ask in `#help-general`. Remind teammates to check their spam/promotions folders for emails from `slack.com`.

### Q: If I registered as solo, can I still join a team later?
* **Yes.** You can form or join a team anytime before submission.

---

## 🔑 5. API Access, Key Generation & Credit Quotas

### Q: How do I generate my Hackathon API key?
1. Sign up or log in at [dashboard.fortyguard.com](https://dashboard.fortyguard.com).
2. Click **Profile** in the bottom-left navigation bar.
3. Scroll down to the **Temperature API Key** section and click **Create API Key** *(Tip: On smaller screens, scroll down or zoom out if the button is off-screen)*.
4. Copy your key into a secure `.env` file (`FORTYGUARD_API_KEY=your_key_here`).

### Q: What tier and credit quota do participants receive?
* **Quota:** **2,000,000 free credits** per hackathon key.
* **Duration:** Valid for **5 weeks** (covers development, testing, judging, and live demos).
* **Tier:** **Full Premium Access** - all endpoints (Heatmaps, Environmental Parameters, Satellite Segmentation, Street View Segmentation, and Heat Intelligence reports) are unlocked.

### Q: Do failed API calls cost credits?
* **No.** Credits are **only deducted on successful task completion**. Failed requests (4xx/5xx errors or rejected requests) cost **0 credits**.

### Q: Can teammates share an API key, or should each member get their own?
* Each team member can generate their own individual 2M credit key from their Dashboard account.
* Teams can also standardize on a single shared API key in their deployed backend. If only one person is writing API code, one key is sufficient, though having individual keys helps trace debugging calls.

### Q: How do I check remaining credits?
* Hit `POST /v1/system/fetch-api-key-usage` (or `GET /v1/credits`), check notebook `00_setup.ipynb`, or check the usage view in the Temperature Dashboard profile.

---

## 🗺️ 6. Geographic Coverage & Temporal Range

### Q: Is FortyGuard Temperature API available worldwide or US-only?
* **Strictly US-Wide:** All coordinates, bounding boxes, and GeoJSON polygons must be located within the territorial United States.
* International locations (e.g. London, Dubai, Cairo, Tokyo) will return errors or empty result sets.

### Q: When registering on the Dashboard, I selected a specific US state. Does that restrict my API queries?
* **No.** The state selected during signup is merely an initial map viewport for the browser GUI. Your API key can query coordinates anywhere across the entire United States.

### Q: What is the supported date range and forecasting horizon?
* **Historical Data:** Supported from **2021-01-01** up to the present day.
* **Real-time Forecast:** Supports predictive heatmaps up to **12 hours into the future** from current time.
* **Long-Term / Multi-Day Projections:** The API does not provide 7-day or seasonal forecasts directly. Build long-range projections by training models on FortyGuard's historical data or integrating external NOAA/climate models.

### Q: What units are used for temperature?
* All input parameters and API output readings are in **Celsius (°C)**. Convert client-side if Fahrenheit or Kelvin is needed ($T_F = T_C \times 1.8 + 32$, $T_K = T_C + 273.15$).

---

## 💡 7. Project Scope, Eligibility & Tech Stacks

### Q: Does the project have to strictly use Deep Learning / Machine Learning?
* **No.** While the event is titled "Building the World's Temperature AI," projects are **not required to use deep learning**.
* **Eligible Approaches:**
  * **Computational & Algorithmic:** Optimization algorithms (e.g. Dijkstra cool-routing), heuristics, rule-based systems, simulation engines.
  * **Hazard Avoidance & Safety Rules:** Threshold alarms, HVAC load-shedding triggers, transformer blowout prevention.
  * **Data Science & Statistics:** Spatial regressions, demographic equity indexes.
  * **Agentic AI:** Autonomous LLM agents sequencing API calls.
* **Core Rule:** As long as FortyGuard 2m temperature data is central to solving a genuine real-world problem with a measurable outcome, it is fully eligible to win.

### Q: Are we restricted to Python and Jupyter Notebooks?
* **No.** Jupyter notebooks are solely for quickstart exploration. You are completely free to build with any modern tech stack:
  * **Frontend:** React, Next.js, Vue, Svelte, Tailwind CSS, Vanilla JS.
  * **Mapping / Geospatial:** Mapbox GL, Leaflet, Deck.gl, OpenLayers, Cesium.
  * **Backend:** FastAPI, Flask, Node.js, Go, Django.
  * **Mobile / Agents:** Flutter, React Native, LangGraph, CrewAI, AutoGen.

### Q: What is the difference between the Dashboard and the API?
* **Temperature Dashboard:** Browser-based point-and-click GUI ([dashboard.fortyguard.com](https://dashboard.fortyguard.com)). Ideal for visual exploration, drawing polygons, and exporting PDF reports without code.
* **Temperature API:** Programmatic HTTP interface for building scalable, deployed applications, autonomous agents, and custom algorithms.

---

## 🔬 8. API Endpoints, Parameters & Payload Schemas

### Overview of Production Endpoints
* **Base URL:** `https://api.fortyguard.com`
* **Auth Header:** `api-key: YOUR_API_KEY` (or `Authorization: Bearer <TOKEN>`)

| Endpoint | Method | Path | Description |
| :--- | :--- | :--- | :--- |
| **Create Heatmap** | `POST` | `/v1/heatmap` | Generates 2m air temperature tiles (~20m physical resolution) over a polygon AOI. |
| **Check Activity Status** | `GET` | `/v1/status/{activity_id}` | Polls async status and retrieves result tiles/metrics. |
| **Environmental Parameters** | `POST` | `/v1/env_params` | Hyperlocal Heat Index, AQI, Solar Irradiance, and Wet Bulb temperature at a point coordinate. |
| **Heat Intelligence** | `POST` | `/v1/heat_intelligence` | Multi-dimensional diagnostic risk report *(note: underscore, not hyphen)*. |
| **Satellite Segmentation** | `POST` | `/v1/satellite` | Computer-vision land-cover classification (vegetation, canopy, pavement, water). |
| **Street View Segmentation** | `POST` | `/v1/street` *(or `/v1/streetview`)* | Street-level facade, canopy, and urban geometry segmentation. |
| **Credit Balance** | `POST` / `GET` | `/v1/system/fetch-api-key-usage` *(or `/v1/credits`)* | Inspects current consumed and remaining API credit balance. |

---

### Request Parameter Details

#### 1. `filter_type` (Temporal Filtering for Heatmaps)
* `1` = **Single Hour** (Requires `start_date` and `start_time`, e.g., `"2025-07-15"`, `"14:00"`).
* `2` = **Hour Range** (Requires `start_date`, `start_time`, and `end_time`).
* `3` = **Entire Day** (Requires `start_date`; analyzes all 24 hours of the day).
* `4` = **Date Range** (Requires `start_date` and `end_date`; queries multi-day spans up to ~1 month).

#### 2. `granularity` (Spatial Tile Resolution)
* Supported values: `60`, `80`, or `100` (meters).
* `100m` = Fast & credit-efficient (recommended for development/testing).
* `60m` = Ultra high-resolution (recommended for final evaluation and high-density downtown blocks).

#### 3. `polygon_aoi` Format
* Must be a valid GeoJSON `FeatureCollection` containing a `Polygon`.
* Coordinates **must** be `[longitude, latitude]` in EPSG:4326.
* Polygon ring **must be closed** (first and last coordinate pairs are identical).
* Recommended maximum area per query: up to ~130 km² (50 mi²).

```json
{
  "polygon_aoi": {
    "type": "FeatureCollection",
    "features": [{
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [[
          [-112.08, 33.44],
          [-112.06, 33.44],
          [-112.06, 33.46],
          [-112.08, 33.46],
          [-112.08, 33.44]
        ]]
      }
    }]
  },
  "date_time": {
    "start_date": "2025-07-15",
    "start_time": "14:00",
    "filter_type": 1
  },
  "granularity": 100
}
```

---

### Clarification on `/v1/env_params` Payload

> [!NOTE]
> **Do I need to pass a temperature value into `/v1/env_params`?**  
> **No.** You do **not** need to supply a measured temperature. The API accepts a location (`point` or `latitude`/`longitude`) and a timestamp, and **returns** temperature, heat index, AQI, and solar irradiance. If an optional threshold is accepted for thermal exceedance calculations, pass a threshold like `35` (°C).
>
> **Minimal Working `/v1/env_params` Payload:**
> ```json
> {
>   "point": {
>     "longitude": -118.2437,
>     "latitude": 34.0522
>   },
>   "start_date": "2025-07-15",
>   "start_time": "14:00",
>   "filter_type": 1
> }
> ```

---

## ⚡ 9. Batch Requests & Parallel Execution Patterns

### Q: Does the API support native batching?
* The API does **not** have a single bulk batch endpoint.
* Instead, submit multiple asynchronous requests using `wait=False` (in the Python client) or asynchronous HTTP POSTs, collect their `activity_id` values, and poll them concurrently with exponential backoff:

```python
import time
from fortyguard import FortyGuardClient

client = FortyGuardClient()

requests_payloads = [
    {
        "polygon_aoi": { ... },
        "start_date": "2025-07-15",
        "start_time": "14:00",
        "filter_type": 1,
        "granularity": 100,
    },
    # Add more AOI / timestamp requests...
]

# 1. Submit all requests asynchronously
activity_ids = []
for req in requests_payloads:
    resp = client.create_heatmap(**req, wait=False)  # wait=False returns immediately
    activity_ids.append(resp["activity_id"])
    print(f"Submitted: {resp['activity_id']}")

# 2. Poll until all tasks complete with exponential backoff
results = {}
pending = set(activity_ids)
backoff = 3

while pending:
    for act_id in list(pending):
        status = client.get_status(act_id)
        if status.get("status", "").lower() in ["succeeded", "completed"]:
            results[act_id] = status.get("data", {}).get("result")
            pending.remove(act_id)
            print(f"✓ Completed: {act_id}")
        elif status.get("status", "").lower() in ["failed", "error"]:
            pending.remove(act_id)
            print(f"✗ Failed: {act_id}")
    if pending:
        time.sleep(backoff)
        backoff = min(backoff * 1.5, 30)

print(f"Batch completed! Processed {len(results)} analyses.")
```

---

## ⚠️ 10. Async Polling Lifecycle & Non-Obvious Production Gotchas

> [!WARNING]
> ### 6 Non-Obvious Behaviors & Best Practices:
> 1. **`start_time` must be `"HH:MM"` string:** Pass `"14:00"` - do **not** pass an integer like `14`.
> 2. **Avoid invalid `analytic_type` casing/values:** The default is `tcm` (raw temperature). Omit `analytic_type` or pass lower-case `"time_of_measure"`, `"exceedance"`, or `"persistence"`.
> 3. **Empty Data on First "Completed" Poll:** In asynchronous polling, `map_data` / `stats_data` may momentarily be empty when `status` first flips to `"Completed"`. Your polling loop must verify that `features` or `stats_data` are populated before treating the response as ready.
> 4. **Credits on Failed Tasks:** Failed tasks are free and do not consume credits. Successful analyses consume credits based on your plan tier.
> 5. **Recommended Polling Interval:** Use exponential backoff (e.g., `3s → 6s → 12s` up to max 30s) when polling `/v1/status/{activity_id}` rather than rapid hammering.
> 6. **Aggressive Client-Side Caching:** For periodic checks of identical locations (e.g. checking an area every hour), store hourly snapshots keyed by `(lat, lon, date, hour)` to avoid redundant credit consumption.

### Robust Python Polling Pattern

```python
import time
import requests

def poll_for_heatmap(base_url, headers, activity_id, max_retries=30, initial_interval=3):
    url = f"{base_url}/v1/status/{activity_id}"
    interval = initial_interval
    for attempt in range(max_retries):
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json().get("data", {})
        status = data.get("status", "")
        
        map_features = data.get("result", {}).get("map_data", {}).get("features", [])
        stats = data.get("result", {}).get("stats_data", [])
        
        if status.lower() == "completed" and (len(map_features) > 0 or len(stats) > 0):
            return data["result"]
        elif status.lower() == "failed":
            raise RuntimeError(f"Heatmap task failed: {data.get('error', 'Unknown backend error')}")
            
        time.sleep(interval)
        interval = min(interval * 2, 30)  # Exponential backoff: 3s -> 6s -> 12s -> 24s -> 30s
    raise TimeoutError("Heatmap polling exceeded maximum wait time.")
```

---

## 📊 11. Analytics Types & Visualizations

| Analytic / View | Parameter / Method | Description | Primary Use Case |
| :--- | :--- | :--- | :--- |
| **Standard (TCM)** | `analytic_type="tcm"` *(or omit)* | Raw 2m air temperature (°C) across every spatial tile. | Baseline heat mapping, urban heat islands. |
| **Time of Measure** | `analytic_type="time_of_measure"` | Identifies the hour of day (0-23) when each tile peaks. Use `filter_type=3`. | Shift scheduling, delivery dispatching, sea breeze fingerprinting. |
| **Exceedance** | `analytic_type="exceedance"`, `threshold=35`, `direction="above"` | Cumulative degree-hours accrued past a temperature threshold (°C). | Worker OSHA compliance, cumulative thermal burden, HVAC strain. |
| **Persistence** | `analytic_type="persistence"`, `threshold=35`, `direction="above"` | Maximum continuous duration (consecutive hours) sustained above a threshold. | Sustained heatwave endurance, vulnerable population alerts. |
| **Time Series** | Built in Dashboard / Client Code | Line chart of average, hottest, and coolest spots across time. | Tracking heat wave progression and extreme divergence. |
| **Distribution** | Built in Dashboard / Client Code | Histogram of temperature readings across all tiles in an AOI. | Distinguishing uniform heat from multimodal microclimate pockets. |

---

## 🎯 12. The 7 Challenge Tracks & Project Concepts

1. **Track 1 - Resilient Cities & Infrastructure:** Cool-walking route planners, bus stop/playground shade-audit tools, digital-twin tree canopy simulators.
2. **Track 2 - Future Buildings & Energy:** Siting & facade-orientation advisor, utility demand-response signals, building retrofit ROI calculators.
3. **Track 3 - Industrial & Enterprise:** Data center thermal siting screener, cold-chain logistics protector, parametric heat-risk insurance scorecards.
4. **Track 4 - Government & Environment:** Demographic heat-vulnerability mapping, outdoor workforce heat alerts, agricultural microclimate timing.
5. **Track 5 - Model Designing:** Composite vulnerability algorithms, predictive worker-strain models, microclimate forecasting layers.
6. **Track 6 - Agentic Track (API + Agentic AI):** Autonomous natural-language heat analysts, 24/7 portfolio sweep agents, tool-using research assistants.
7. **Track 7 - Data Analysis & Correlation:** Non-weather outcome regressions (hospital ER visits, energy demand, transit ridership), heat equity and redlining analyses.

---

## 📜 13. Code Reuse & Boilerplate Policy

### Q: Can we build upon or extend the Quickstart notebooks or webinar ideas?
**Yes, absolutely!**
* **Allowed:** Using the Quickstart notebooks, sample pipelines, or webinar concepts as a foundation.
* **Rules to Follow:**
  1. **README Disclosure:** Clearly state in your repository's `README.md` which components originated from the Quickstart or webinars (e.g., *"We began with Notebook 01 and extended it with LangGraph agent orchestration and custom persistence thresholds"*).
  2. **Substantial Original Work:** The bulk of the project must be original, solving a specific real-world problem.
  3. **Repository Creation Date:** The repository must be created after the hackathon kickoff (**August 18, 2026**).

---

## 🤖 14. Building ML Models, Datasets & Agentic AI

### Q: What should an ML model or Agent do that the API doesn't already do? (Tracks 5, 6, 7)
* **The API provides raw observations:** "What is the 2m temperature at location $(x, y)$ on date $t$?"
* **Your AI / Agent System provides intelligence & decision-making:**
  1. **Extended Multi-Day Forecasting:** Modeling beyond 12 hours using historical analogs and regressions.
  2. **Multi-Source Vulnerability Scoring (0-100):** Combining FortyGuard temperature with Census demographics and infrastructure vulnerability.
  3. **Autonomous Hazard Remediation:** Detecting persistence past equipment safety limits (40°C/45°C) and triggering automated load-shedding or alert dispatches.

---

## 💻 15. Third-Party LLM Keys, External Data & Caching

### Q: Does FortyGuard provide LLM API keys (OpenAI / Claude / Gemini)?
* **No.** FortyGuard provides the **FortyGuard Temperature API key** (2M credits).
* You provide your own LLM keys (Anthropic Claude, OpenAI, Google AI Studio, Groq, Ollama, etc.) and disclose them in the submission form. Never commit private LLM keys to public repos.

### Q: Are external datasets permitted?
* **Yes, highly encouraged!** Combining FortyGuard data with OSHA safety thresholds, NOAA weather, USGS/Landsat satellite imagery, OpenStreetMap, or demographic data is welcomed as long as **FortyGuard temperature data is the core driver of the application**.

### Q: Can I cache API responses locally?
* **Yes!** Local caching is actively recommended in the Participant Handbook to reduce latency and conserve API quota during development and live judging.

---

## 🔄 16. Project Pivots, Track Changes & Resubmissions

### Q: Can I change my project idea or switch to a different track?
* **Yes.** You are free to change your project concept or track at any time before the deadline.

### Q: How do I submit an updated project or change my track?
* Simply fill out and submit the official submission form again with the updated information. **The judging system automatically retains and evaluates your latest submission entry.**

---

## 🚀 17. Final Submission Requirements & Judging Rubric

### 📦 Submission Checklist (Due 30 August 2026, 11:59 PM GST)
Form URL: **[https://forms.gle/jLgBzVTG1NhJ3gNe6](https://forms.gle/jLgBzVTG1NhJ3gNe6)**

1. **Project Title & One-Line Pitch**
2. **Primary Track** (evaluated for judging) + up to 2 Secondary Tracks
3. **Problem & Target User** (who benefits, before/after impact)
4. **Geography & Time Period Covered** (US area, date range)
5. **FortyGuard API Usage Details**
6. **API Key ID** (to verify real API usage on backend)
7. **AI Tools Used Disclosure**
8. **Code Repository Link** (GitHub/GitLab - add `hackathon@fortyguard.com` / `Hackathon-FG` if private)
9. **Live Demo URL** (Hosted web app, accessible in incognito without install)
10. **Demo Video Link** (YouTube/Loom, max 3 min, must show working UI + voiceover)

### 🏆 Judging Rubric (100% Total)
* **Impact & Relevance - 40%:** Solves a real urban heat problem with measurable client benefit and commercial viability.
* **Technical Execution - 35%:** Robust build, client-grade deployable quality, sound data architecture.
* **Innovation - 15%:** Originality or novel multidisciplinary approach.
* **Communication - 10%:** Clear, compelling demo, writeup, and video narrative.

---

## 🎥 18. Workshop & Live Session Summaries

1. **Onboarding & Kickoff (18 Aug):** Jay Sadiq (CEO) & Snehil Ahuja (Product Lead) - Challenge overview, track selection, scoring rubrics, and winning strategies.
2. **Building on the FortyGuard Temperature API (18 Aug):** Complete walkthrough of all 6 endpoints, payload formatting, common pitfalls, and agent orchestration.
3. **Heat Intelligence Cloud (19 Aug):** Aashan Javed (AI/ML Engineer) - Production use cases, data intelligence patterns, and commercial opportunities.
4. **Breaking Silos with Autodesk (19 Aug):** Jordana Rosa (Autodesk Forma) - Contextual site data, environmental analysis, and connecting spatial APIs to generative design tools.

---

## 🛠️ 19. Troubleshooting & HTTP Status Code Reference

| Status / Issue | Probable Cause | Immediate Remedy |
| :--- | :--- | :--- |
| `401 Unauthorized` | Invalid or missing API key in headers. | Verify `api-key: YOUR_KEY` header. Regenerate fresh key in Dashboard → Profile. |
| `400 Bad Request` | Polygon outside US, unclosed coordinates, or invalid `start_time`. | Ensure coordinates are `[lon, lat]`, first/last coordinates match, and `start_time` is `"HH:MM"`. |
| `404 Not Found` | Wrong endpoint URL spelling. | Use `/v1/heat_intelligence` (underscore), `/v1/env_params`, `/v1/heatmap`. |
| `500 Server Error` | Unrecognized `analytic_type` or malformed parameter types. | Omit `analytic_type` to use default `tcm`; pass `start_time` as string `"14:00"`. |
| `Activity Stuck on "Processing"` | Large polygon (>130 km²) or dense date range. | Check activity status manually; start testing with smaller polygons and `granularity=100`. |
| Empty `stats_data` / `map_data` | Premature exit on initial `"Completed"` status poll. | Keep polling until `result.map_data.features` has items (>0). |

---

> [!TIP]
> For complete OpenAPI 3.1 specifications and detailed payload definitions, refer to the [FortyGuard API Master Reference](../api-documentation/FORTYGUARD_API_MASTER_REFERENCE.md) and [Official Announcements](OFFICIAL_ANNOUNCEMENTS.md).
