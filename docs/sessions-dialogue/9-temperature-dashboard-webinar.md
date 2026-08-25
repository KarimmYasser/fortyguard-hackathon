# Mastering the FortyGuard Temperature Dashboard: Microclimate Intelligence, Live Feature Walkthrough & Hackathon Submissions — Full Transcript & Summary

**Recording:** Zoho Webinar Recording (Session 09)  
**Date:** August 25, 2026 | **Duration:** 1 hour 16 minutes | **Language:** English  

**Speakers:**
- **Snehil Ahuja** — Product Lead at FortyGuard (Leads product strategy, UI/UX design, and development of the FortyGuard Temperature Intelligence Suite, Temperature Dashboard, and Temperature Property)
- **Aamir** — Software Engineer, Cloud & Data Architect at FortyGuard (Co-host & Moderator)

---

## Executive Summary & Session Overview

In this comprehensive technical walkthrough and masterclass, **Snehil Ahuja** (Product Lead at FortyGuard) and **Aamir** provide an end-to-end live demonstration of the **FortyGuard Temperature Dashboard**—the production web platform built on top of the FortyGuard Temperature API®. 

This session bridges raw API endpoints with visual, analytical, and diagnostic capabilities, showing participants how to turn 2-meter resolution ground-level air temperature into multi-layered spatial intelligence, defensible analytics, and production-grade applications. Additionally, Snehil unveils the **Public Community Voting feature** and outlines the definitive submission rules, technical requirements, scoring rubrics, and judging criteria for the Hackathon'26 sprint.

---

## Key Highlights & Technical Insights

### 1. Platform Capabilities & Spatial Controls
- **State Selection & Active Subscriptions:** Users configure their active coverage area (e.g., California). The UI highlights active coverage in high-contrast brightness, allowing users to drill down into cities and neighborhoods (e.g., San Jose, Los Angeles).
- **Geospatial Area of Interest (AOI) Drawing:**
  - **Circle Polygon:** Quick radius-based exploration of neighborhoods or municipal districts.
  - **Custom Freehand Polygon:** Custom bounding geometry (e.g., irregular parcels, transit corridors, urban districts).
  - **Custom Polygon Upload:** Direct upload of pre-existing GeoJSON / Shapefile boundaries.
- **Granularity Modes:**
  - **$100\text{m} \times 100\text{m}$ Grid:** Macro city-wide macroclimate overview and regional heat stress assessment.
  - **$60\text{m} \times 60\text{m}$ Grid:** Hyperlocal asset-level resolution for dissecting individual households, industrial facilities, substations, and park segments.
- **Temporal Windows & Seasonal Comparisons:** Support for single hour, range of hours (e.g., 12:00 AM – 11:00 PM), single day, range of days, and full monthly/seasonal aggregations (e.g., July 2025 vs. July 2026; January vs. July baselines).

---

### 2. Analytical & Visualization Engine
- **Equal Interval & Hotspot Isolation:** Map controls allow toggling temperature bins and applying equal-interval classification to filter out background variance and isolate persistent structural hotspots within seconds.
- **Heat Flow Simulation (Time-Series Playback):** Dynamic temporal video/playback showing heat progression across the diurnal cycle, illustrating how thermal energy accumulates and peaks between 1:00 PM and 5:00 PM (13:00 – 17:00).
- **12-Hour AI Forecast Heat Map:** Real-time AI casting providing predictive forward-looking heat maps 12 hours into the future.
- **Cross-Layer Spatial Correlation:** Uploading custom point/vector layers (e.g., municipal bus stops, power substations, distribution transformers) to perform spatial intersection and measure thermal exposure on specific physical assets.
- **Statistical Distributions:** Automated generation of Min, Max, Mean, Temperature Frequency histograms, Normal probability curves (expected likelihood), and Box plots for median and outlier detection.

---

### 3. Environmental Parameters & Physics Indicators
- **Relative Humidity:** Contextualizes convective vs. evaporative cooling rates. High humidity combined with elevated temperatures accelerates microclimate heat accumulation.
- **Wet-Bulb Temperature ($T_{\text{wb}}$):** Crucial metric measured at 2 meters above ground level. Represents the thermodynamic threshold of human evaporative cooling and provides vital inputs for HVAC optimization, data center chiller loading, and outdoor labor safety.
- **Solar Irradiance:** Measures solar radiation flux ($W/m^2$) absorbed by surface materials versus reflected, directly correlating with impervious surface heat retention.
- **Atmospheric Variables:** Hourly readings for Wind Speed, Wind Direction, Cloud Cover, and Precipitation.
- **Air Quality Multi-Pollutant Suite:** Detailed indices and gas concentrations for Ozone ($O_3$), Sulfur Dioxide ($SO_2$), Nitrogen Dioxide ($NO_2$), and Particulate Matter ($PM_{2.5}$).

---

### 4. Advanced Analytical Layers
- **Time of Measure:** Pinpoints the exact hour of the day when maximum temperature peaks occur across individual grid tiles.
- **Exceedance Layer:** Calculates the **cumulative total hours** within a temporal window where air temperature exceeds a user-defined safety threshold (e.g., $>66^\circ\text{F}$ / $>35^\circ\text{C}$).
- **Persistence Layer:** Calculates the **longest unbroken consecutive stretch of hours** where air temperature remains continuously above the threshold without cooling relief.
- **Satellite View Land-Cover Segmentation (Bird's Eye):** Computer vision segmentation of satellite imagery quantifying ground absorption (e.g., 82% asphalt road and building concrete absorbing heat vs. 7% sparse vegetation/grass).
- **Street View Segmentation (Human-Height 2m):** Panoramic ground-level computer vision measuring human-perspective environment (e.g., road vs. tree canopy with sky masked out) to explain perceived microclimate comfort.
- **5-Pillar Heat Intelligence Diagnostic Report (Per Tile):**
  1. *Geographic Information:* Elevation, terrain gradient, proximity to water bodies (e.g., San Francisco Bay).
  2. *Historical Heatwave Events:* Contextualizing local temperatures against regional/national heatwaves.
  3. *Anthropogenic Factors:* Foot traffic intensity, transportation corridors, and commercial/industrial waste heat.
  4. *Urban Elements:* Tree canopy coverage %, building density, and impermeable surface ratio.
  5. *Environmental Factors:* Microclimate atmospheric parameters compared against historical standard baselines.
- **Multi-Map Temporal Comparison:** Side-by-side synchronized spatial comparison (e.g., August 1 heatwave peak vs. baseline; January winter baseline vs. July summer heat) to distinguish seasonal anomalies from permanent structural urban heat islands.

---

### 5. Official Hackathon Rules, Screening & Judging Criteria

| Milestone / Parameter | Official Requirement / Specification |
| :--- | :--- |
| **Submission Deadline** | **August 30, 2026 at 11:59 PM GST** (Strict hard cutoff). |
| **Deliverable 1: Live Application URL** | Publicly accessible deployed web application (e.g., Vercel, Netlify, Cloud Run, AWS). Prototypes with no live link cannot advance. |
| **Deliverable 2: Demo Video** | **3 to 5 minutes duration** (3 min target, up to 5 min allowed without penalty). Must be in **English**, demonstrating the live product UI and features. *No pure AI-generated promotional videos without real product UI.* |
| **Deliverable 3: GitHub Repository** | Public or private GitHub repo with **`Hackathon FG`** (`Hackathon@fortyguard.com`) invited as a collaborator. |
| **Deliverable 4: Submission Form** | One single submission per team submitted by the team lead via the official form. New submissions overwrite previous ones. |
| **API Quota Management** | 2,000,000 credits allocated per account for 5 weeks. If depleted, create a secondary account and list both keys in the submission form. |
| **Prizes & Hardware** | **Top 3 overall winners** across all tracks receive cash prizes from the $6,000 pool + **1 NVIDIA GPU / Jetson kit per winning team** (presented by Constantine from NVIDIA). |

#### Official Judging Rubric (100% Total)
1. **Impact & Relevance (40%):** Does the solution solve a real-world urban heat problem with measurable, defensible business/societal outcomes? Is it a production-grade utility rather than a toy demo?
2. **Technical Execution (35%):** Architectural quality, robust handling of FortyGuard API data, security, live deployment stability, and codebase cleanliness.
3. **Innovation (15%):** Originality of concept, novel multi-source data coupling, or creative synthesis across tracks.
4. **Communication (10%):** Clarity of the video pitch, written documentation, value proposition, and communication of the core "Why".

#### New Feature: Public Community Voting
- The Temperature Dashboard will introduce a **"Cast Your Vote"** tab in the side navigation.
- **Rules:** 1 verified vote per registered account.
- **Purpose:** Amplification, public awareness, and social proof for participant projects.
- **Judging Separation:** Community voting is designed for outreach and exposure; official winner selection is governed strictly by the judging panel using the 4 core rubrics.

---

## Subtitle & Document Exports

- **Plain Text Source Transcript:** [`9-tempreture-dashboard-webinar.txt`](file:///Users/karim/Development/projects/fortyguard-hackathon/scratch/9-tempreture-dashboard-webinar.txt)
- **Master Documentation Hub:** [`sessions-dialogue/README.md`](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/sessions-dialogue/README.md)

---

## Complete Timestamped Transcript

**[00:00]** *[Pre-session setup and waiting room]*

**[07:54]** **Aamir:** Okay guys, we will be starting in a couple of minutes. Thank you for your patience.

**[11:04]** **Aamir:** Hello, everyone. I hope everyone is doing good today. I'm sure you're a little surprised to see me over here, but today, don't worry, Snehil is with us, but not as a session coordinator today. Today, we will have the pleasure of learning from him directly, as he'll be presenting this session and taking us through a live demo.

**[11:35]** **Aamir:** So I'm proud to introduce Snehil Ahuja, someone most of you might already know, as he's been running this hackathon diligently from the very beginning. He is the Product Lead at FortyGuard, and he owns where the product goes: the direction, the decisions, and the harder questions sitting underneath both of those, which is where the product actually fits the market.

**[12:05]** **Aamir:** He is the bridge between our marketing team, software team, machine learning team, and all of the departments that speak different languages. He sits between them and points them at the same goal. He carries the product not just from the ideation phase, but through every single decision that shapes it to the moment it goes live.

**[12:31]** **Aamir:** What makes Snehil so rare is that his contribution has never stopped at just strategy; he works right across the product, design, and engineering, UI/UX, and frontend development as well, where he is genuinely excellent. He has not only built much of the Temperature Intelligence Suite himself—including the Temperature Dashboard, Temperature Property, and the products built on top of our APIs, to name only a few—the Temperature Dashboard you're about to see, the way it looks and works today, is because of him. A good deal of what you will be building on over these two weeks has been shaped through his guidance.

**[13:20]** **Aamir:** So, I hope you enjoy this session as he walks you through a live demo of the dashboard, its features, and its capabilities. He's also a very dear friend of mine; I've learned a great deal from him, and I'm certain you will too. Snehil, over to you.

**[13:39]** **Snehil Ahuja:** Thank you so much for the kind words, Aamir. I think if I have to introduce myself ever again, I'm just going to take you with me to introduce me! I don't think I can do a better job than you have done. But thank you so much. Whatever we all have accomplished on the dashboard and every other project is because of FortyGuard itself and the teamwork that we have. I have certainly learned a lot from you and the team.

**[14:08]** **Snehil Ahuja:** It's different to be in this seat rather than being the organizer, but I'll quickly start with the demo of the Temperature Dashboard, and we'll jump into Q&A after that about the dashboard itself. Then, there is one small thing that we want to reveal to you in terms of your project submissions—which we think is a great thing because more people will be able to see your projects. Secondly, we'll open it up to general Hackathon Q&A as well. Any question about the hackathon—how to start, how to submit—you can shoot it right in the chat. I'm here virtually to answer it live for you guys.

**[15:06]** **Snehil Ahuja:** All right, let's get started without any further ado. Let me share my screen. Can you just let me know if you can see my screen?

**[15:22]** **Aamir:** That is visible.

**[15:24]** **Snehil Ahuja:** All right guys. The moment we enter the dashboard itself, there is a subscribed state that you guys can select. For me, I've personally selected California. Growing up, I admired Los Angeles a lot, so LA was one of the coolest places I could think of. You guys can select one state at a time per account. If you see this highlight, this is the active state that you have. Once you load the dashboard, you see the visible brighter part, which shows the locations within this subscribed state that you can examine.

**[16:05]** **Snehil Ahuja:** For the demo, I have created a few things that I would like to show you guys. But before I jump into the heat maps themselves, I want to show you the temperature mapping interface. This is where all the magic starts; this is where the analytics originate. You can create many different queries from here. You can zoom into one of the locations—I'll go to Los Angeles again—and start with a circle polygon. This is one of my favorite tools because it's very easy to manage, quickly set an Area of Interest (AOI), and start mapping.

**[16:46]** **Snehil Ahuja:** You also have a custom polygon tool. If you have a particular shape like a parallelogram or any custom boundary you want to research, you can draw a polygon, or you can upload your own custom polygon (GeoJSON) if you already have an Area of Interest defined.

**[17:04]** **Snehil Ahuja:** Moving on to **Granularity**: this is where everything comes into the picture. You have seen the heat maps bisected into small squares; those are the tiles, and that represents the granularity at which you examine locations. A **100 by 100 meter** grid gives you a broader macro view of the area. A **60 by 60 meter** grid gives you a granular microclimate view where you can analyze every asset, every household, every industrial site, or segment parks into distinct tiles to see which specific section of a park is hottest.

**[17:41]** **Snehil Ahuja:** For citywide analysis, people often choose 100x100m. If you are doing neighborhood-level analysis, property valuation, or identifying cooling hotspots, 60x60m gives you precise hotspot and cool-spot detection.

**[18:02]** **Snehil Ahuja:** In terms of **Timeframe**, you can select:
1. Single Hour
2. Range of Hours
3. Single Day (all 24 hours aggregated)
4. Range of Days
5. Single Month (seasonal analysis)

With monthly data, you can compare seasons—for example, July of this year versus July of the previous year to see exact microclimate temperature differentials across full months.

**[18:46]** **Snehil Ahuja:** For this demo, I picked San Jose because NVIDIA is headquartered there and NVIDIA is actively supporting our hackathon.

**[19:10]** **Snehil Ahuja:** Let's look at **Map Controls**. This gives you full visual and interpretive control over the heat map. For example, if you look at the temperature ranges in the legend and unselect them all, it hides the heat map. If you select only the top three hottest classes, the map isolates the hottest tiles in seconds. This is instantaneous hotspot identification.

**[19:57]** **Snehil Ahuja:** You also have **Equal Interval Classification**. This divides all temperature ranges into equal interval sizes. Applying this refines the visualization to highlight the persistent, critical hotspots in the area.

**[20:30]** **Snehil Ahuja:** Next is the **Heat Flow Simulation**. For an hourly heat map or range of hours, you can play a dynamic time-series simulation showing how heat physically moves across your area of interest hour by hour. If you generate a single day or range of days, you can watch daily temperature progression; for a month, you can observe day-by-day shifts.

**[20:48]** **Snehil Ahuja:** If I pause the simulation between 1:00 PM and 2:00 PM, you see red hotspots peaking across San Jose. By the way, some participants reported earlier issues regarding forecast heat maps; that has been completely resolved. You can now generate 12-hour forward-looking forecast heat maps reliably.

**[21:40]** **Snehil Ahuja:** You can also download the heat map, recenter the view, and upload custom vector layers. For example, if you upload a point layer of municipal bus stops or electrical transformers, you can perform a spatial cross-intersection against the heat tiles to immediately determine which assets sit in dangerous thermal zones.

**[22:10]** **Snehil Ahuja:** Map controls also allow you to adjust color ramps to match specific analytical narratives and use cases. Moving to the **Heat Map Statistics** panel, you get basic descriptive statistics: maximum temperature, minimum temperature, and mean. You also get a temperature frequency bar chart, a normal probability distribution curve indicating expected values, and a box plot detailing anomalies, outliers, and the median baseline.

**[23:12]** **Snehil Ahuja:** The **Metadata** tab displays the parameters used when creating the map: for example, 23 hours from 12:00 AM to 11:00 PM covering an 85-square-mile area.

**[23:36]** **Snehil Ahuja:** Now let's move into the core intelligence features: **Analytics & Segmentation, Heat Intelligence, and Map Comparison**. When we designed the 7 Hackathon tracks, these features were built to power those use cases.

**[24:07]** **Snehil Ahuja:** Temperature is never just an isolated number; it is shaped by environmental parameters and urban context. Looking at our San Jose tile from 12:00 AM to 11:00 PM, let's examine the peak window from 12:00 PM to 5:00 PM. We provide reference tables indicating caution zones, normal zones, and threshold precautions.

**[25:25]** **Snehil Ahuja:** **Relative Humidity** plays a massive role; here it sits in the moderate-to-high range, contributing to the higher apparent temperature hotspot.

**[25:46]** **Snehil Ahuja:** **Wet-Bulb Temperature** is an essential factor for human comfort and physiological heat stress. Remember, FortyGuard reports air temperature at 2 meters above ground level. Wet-bulb temperature is critical if you are planning urban routing, outdoor worker shifts, HVAC efficiency, or data center cooling intake optimization.

**[26:19]** **Snehil Ahuja:** For temperature-dependent variables, we provide **Precipitation** (San Jose rarely sees rain in August) and comprehensive **Air Quality** metrics: not just a generic AQI, but granular concentrations for **Ozone ($O_3$)**, **Sulfur Dioxide ($SO_2$)**, and **Nitrogen Dioxide ($NO_2$)**.

**[26:58]** **Snehil Ahuja:** The heat map is not just a pretty picture. Clicking on any individual tile opens a deep-dive panel with full hourly environmental parameters: **Wind Speed, Wind Direction, Cloud Cover, Precipitation, and Relative Humidity**.

**[27:37]** **Snehil Ahuja:** **Solar Irradiance** indicates how much solar energy the surface absorbs versus reflects. High solar irradiance on low-albedo surfaces drives microclimate heat accumulation.

**[28:12]** **Snehil Ahuja:** Next is **Time of Measure**. If you want to know the exact hour of the day when temperature peaked across different sections of a city, Time of Measure maps this directly. In our dataset, temperatures ranged from $73^\circ\text{F}$ to $86^\circ\text{F}$, peaking between 1:00 PM and 2:00 PM in the southern region.

**[30:09]** **Snehil Ahuja:** Now let's look at **Exceedance**. We set a safety threshold—for example, $>66^\circ\text{F}$—and map the **total number of hours** the temperature exceeded that threshold. In our data, the hottest zone experienced 6 cumulative hours above $66^\circ\text{F}$.

**[31:16]** **Snehil Ahuja:** Next is **Persistence**. While Exceedance measures *total cumulative hours*, Persistence measures the *maximum unbroken consecutive stretch of hours* above the threshold without interruption. In our hotspot tiles, the temperature stayed continuously above the threshold for 5 consecutive hours without cooling relief.

**[32:02]** **Snehil Ahuja:** Switching to satellite view with reduced opacity reveals why: the persistent hotspot is entirely built-up urban fabric with asphalt and dense buildings. Nearby cooler zones contain lush greenery, tree canopies, and water channels.

**[33:05]** **Snehil Ahuja:** Now let's look at **Satellite View Segmentation (Bird's-Eye)**. For urban planners, this breaks down land cover composition. Segmenting our hotspot tile reveals that **82% is road and building footprint** (asphalt and concrete absorbing heat), while trees, grass, and plants account for only **7%**. This 82% to 7% imbalance explains the severe heat island effect and directly dictates the urban intervention required: cool pavements, shade structures, and vegetative canopy.

**[34:48]** **Snehil Ahuja:** We also provide **Street View Segmentation (Human-Height 2m)**. Because FortyGuard models air temperature at 2 meters, human-level perspective matters. Analyzing a cooler tile and toggling off the sky reveals 62% road but **18% dense tree canopy** providing direct shade, explaining why it stays significantly cooler.

**[36:06]** **Snehil Ahuja:** Next is **Heat Intelligence Reports**. This generates an exhaustive diagnostic report for any single tile based on 5 analytical pillars:
1. **Geographic Information:** Terrain elevation, topography, and proximity to water bodies (e.g., San Francisco Bay).
2. **Historical Events Analysis:** Tracking ongoing regional heatwave anomalies.
3. **Anthropogenic Factors:** Transportation corridors, vehicle foot traffic, and industrial waste heat emissions.
4. **Urban Elements:** Tree canopy percentage, building surface density, and pavement coverage.
5. **Environmental Factors:** Microclimate atmospheric parameters compared against baseline norms.

**[39:14]** **Snehil Ahuja:** Next is **Map Comparison**. You can compare multiple heat maps side by side. For example, comparing August 25 (today) with August 1 (peak heatwave in California). You can see the shift from blue (cooler) to deep red across the lower region of San Jose.

**[40:35]** **Snehil Ahuja:** You can also compare **January (winter) versus July (summer)**. In July, temperatures are high across the board, but the bottom-left zone consistently registers as the hottest relative hotspot even in January. This proves it is a permanent structural urban heat island, giving your project a clear target for architectural intervention.

**[42:33]** **Snehil Ahuja:** Regarding **API Keys & Quotas**: in your Profile section, you can generate your API key with **2,000,000 credits** valid for 5 weeks. If your team exhausts your 2,000,000 credits during heavy testing, simply create a secondary account and submit both the old and new API keys in your final hackathon submission form.

**[43:24]** **Snehil Ahuja:** Now, I want to share something exciting regarding project submissions: **Public Community Voting**. We are opening the Temperature Dashboard to the public. In the side navigation bar above Settings, a **"Cast Your Vote"** tab will appear when voting goes live.

**[44:21]** **Snehil Ahuja:** Visitors and community members can search for projects by name or team member, view the project demo video, and cast **one verified vote per registered account**. You cannot vote for multiple projects. You can share your project link across LinkedIn, Instagram, and your professional network. We want your projects to gain maximum public visibility and industry recognition.

**[45:51]** **Snehil Ahuja:** I'll open the floor to questions now!

**[46:15]** **Aamir:** Thank you so much, Snehil. That was a great session. Let's look at the questions coming in.

**[46:55]** **Audience Question:** Is the winning criteria based on votes? What if a project meets all technical requirements but doesn't get many votes?

**[47:02]** **Snehil Ahuja:** The 4 official judging criteria are still the primary criteria used by the judges to evaluate and score your projects. Voting is an added layer for public exposure and social influence. Do not worry if you don't receive many votes; projects are scored rigorously on their technical and commercial merits by the judging panel.

**[48:01]** **Audience Question:** When we submit the project, how will people vote?

**[48:07]** **Snehil Ahuja:** Voting happens directly on the Temperature Dashboard. Your network will visit the dashboard, sign up for a free account, navigate to "Cast Your Vote", and select your project.

**[48:34]** **Audience Question:** Is voting included in the official judging criteria?

**[48:37]** **Snehil Ahuja:** No, voting is not included in the official judging rubric. It is strictly for community exposure and public outreach.

**[49:14]** **Audience Question:** What is the hard submission deadline?

**[49:16]** **Snehil Ahuja:** The hard submission deadline is **August 30, 2026 at 11:59 PM GST**.

**[50:03]** **Snehil Ahuja:** All recordings and session materials are shared daily via Slack announcements and morning emails from `Hackathon@fortyguard.com`.

**[50:55]** **Audience Question:** How many teams are participating?

**[51:01]** **Snehil Ahuja:** We have over **3,000 registered participants** globally in this hackathon, backed by NVIDIA.

**[51:48]** **Audience Question:** Can our project use a custom database?

**[51:55]** **Snehil Ahuja:** Yes, absolutely. You can use any local or cloud database (e.g., PostgreSQL, Supabase, SQLite, Redis) that fits your architecture. Focus on delivering a functional end product.

**[52:25]** **Audience Question:** Can you clarify the 3-minute video requirement?

**[52:30]** **Snehil Ahuja:** The recommended target is **3 minutes**. However, we allow videos up to **5 minutes maximum without penalty**. We recommend writing a concise script. Cover the problem, the core features, how you utilized the FortyGuard API, secondary data sources, and the business value.

**[53:17]** **Audience Question:** What geographic data scope is available?

**[53:19]** **Snehil Ahuja:** The API covers the **entire United States** at 2-meter resolution, with historical data from 2021 to the present and 12-hour forward AI forecasts.

**[53:32]** **Audience Question:** How many winners will there be?

**[53:34]** **Snehil Ahuja:** There are **3 overall winners** (1st, 2nd, and 3rd place across all tracks). Each winning team walks away with a cash prize and an **NVIDIA GPU kit**. On Friday, **Constantine from NVIDIA** will present a special session detailing the NVIDIA hardware prizes.

**[54:16]** **Audience Question:** Can we combine external APIs with FortyGuard API?

**[54:21]** **Snehil Ahuja:** Yes! Coupling FortyGuard microclimate data with external datasets (demographics, grid SCADA, transit, health indices) is strongly encouraged.

**[55:12]** **Audience Question:** Can we use AI-generated avatar videos?

**[55:18]** **Snehil Ahuja:** No, pure AI-generated avatar videos without real UI will not suffice. The judges need to see your actual working software interface via screen capture. You can narrate live or record a voiceover, but the screen must demonstrate the live product.

**[56:07]** **Audience Question:** How should we submit the video?

**[56:15]** **Snehil Ahuja:** Host your video on YouTube (unlisted or public) or Vimeo, and provide the URL in the submission form.

**[56:33]** **Audience Question:** Can we use LLMs and AI coding assistants during development?

**[56:35]** **Snehil Ahuja:** Yes, absolutely! This is an AI hackathon. You are free to use LLMs, Cursor, Claude, Vercel v0, etc. Just disclose the tools and models utilized in your technical documentation.

**[57:03]** **Audience Question:** Does the prototype need to be a deployed production product?

**[57:08]** **Snehil Ahuja:** Yes. This is not a hackathon where you submit theoretical slide decks. Submissions must feature a **working live deployment URL** serving real end users.

**[57:57]** **Audience Question:** Can someone participate solo?

**[58:00]** **Snehil Ahuja:** Yes, solo participants are fully eligible and keep the entire cash prize and NVIDIA GPU for themselves if they win.

**[59:17]** **Audience Question:** Is a live deployed link mandatory?

**[59:19]** **Snehil Ahuja:** Yes. Without a functional live link, submissions cannot advance to the final judging round.

**[59:50]** **Audience Question:** When will winners be announced?

**[01:00:01]** **Snehil Ahuja:** Winners will be officially announced on **September 16, 2026**.

**[01:00:18]** **Audience Question:** Will all participants receive certificates?

**[01:00:22]** **Snehil Ahuja:** Yes, a **Certificate of Completion** is awarded to all participants who submit valid projects meeting all submission requirements. Finalists and winners receive special **Winner Certificates**.

**[01:01:02]** **Audience Question:** Must the video demo be in English?

**[01:01:03]** **Snehil Ahuja:** Yes, the video pitch and documentation must be in English for the international judging panel.

**[01:02:02]** **Audience Question:** How do team submissions work?

**[01:02:05]** **Snehil Ahuja:** The team lead submits the official form. If multiple submissions are made by the same team, the latest submission overwrites previous ones. Each team can only submit to one primary track.

**[01:03:39]** **Audience Question:** How should code repositories be shared?

**[01:03:51]** **Snehil Ahuja:** You must share your GitHub repository with `Hackathon FG` (`Hackathon@fortyguard.com`) as a collaborator.

**[01:08:33]** **Audience Question:** Can you repeat the 4 official judging criteria and their percentage weights?

**[01:08:33]** **Snehil Ahuja:** Yes, the 4 official judging criteria are:
1. **Impact and Relevance (40%):** Does the project address a real urban heat problem with measurable benefits and practical utility?
2. **Technical Execution (35%):** Code quality, handling of FortyGuard API data, system architecture, security, and deployment robustness.
3. **Innovation (15%):** Originality of the concept, multi-dataset coupling, and creative problem solving.
4. **Communication (10%):** Quality and clarity of the demo video, project description, and pitch.

**[01:13:36]** **Snehil Ahuja:** The official submission form link is shared in chat and on Slack. No travel is required; all prizes, funds, and NVIDIA GPUs will be distributed digitally and shipped directly to winners.

**[01:14:59]** **Snehil Ahuja:** Top 3 teams receive 1 GPU per team. The team lead allocates hardware distribution.

**[01:15:50]** **Snehil Ahuja:** Thank you, everyone, for joining today! Reach out on Slack or email `Hackathon@fortyguard.com` if you have further questions. Happy building, and we look forward to seeing your amazing submissions!
