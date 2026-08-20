# 🎙️ Mentorship Webinars & Session Dialogues Hub

This directory contains full verbatim transcripts, structured summaries, and actionable insights extracted directly from the official **FortyGuard Hackathon '26** onboarding, technical workshops, and partner mentorship sessions.

> [!TIP]
> 📖 **Master Distillation & Idea Framework:**  
> For the complete synthesized playbook on idea selection, problem framing, commercial positioning, and the 6 demonstrated industry blueprints, read **[Mentor Insights & Idea Selection Framework](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/research/MENTOR_INSIGHTS_AND_IDEA_FRAMEWORK.md)**.


---


## 🗂️ Catalog of Sessions

| # | Session Title | Key Speakers / Mentors | Duration / Date | Key Themes & Topics Covered |
| :-: | :--- | :--- | :--- | :--- |
| **01** | **[Onboarding & Kickoff Session](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/sessions-dialogue/1-onboarding-kickoff-session.md)** | **Jay** (Founder & CEO)<br>**Nahil** (Product & Community Lead) | Aug 18, 2026<br>*Sprint Kickoff* | Hackathon rules, $6,000 + NVIDIA Jetson AI prizes, 7 tracks, US 2m data scope, live URL & 3-min video requirements, GitHub collaborator `Hackathon FG`. |
| **02** | **[Building on the FortyGuard Temperature API®](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/sessions-dialogue/2-building-fortyguard-temperature-api.md)** | **Fawad Shah** (Head of Software Engineering)<br>**Nahil** (Community Lead) | 1h 01m<br>Aug 18, 2026 | Asynchronous submit-and-poll architecture, 6 core API endpoints, Quickstart Python SDK walkthrough, bounding box & polygon queries, rate limiting & error handling. |
| **03** | **[Heat Intelligence Cloud: What You Can Build](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/sessions-dialogue/3-heat-cloud-webinar-session.md)** | **Lead Solutions Architect / AI ML Team** | 38m<br>Aug 19, 2026 | 4 data layers (Temperature, Comfort UTCI, Air Quality, Land Cover), 6 live production app demos across PropTech, InsurTech, Logistics, Worker Safety, and Utilities. |
| **04** | **[Breaking Silos with Autodesk: Data to Design](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/sessions-dialogue/4-autodesk-webinar-session.md)** | **Jordana Rosa** (Senior Technical Specialist, Autodesk)<br>**Jay** (FortyGuard) | 1h 00m<br>Aug 19, 2026 | AEC & Autodesk Forma integration, early-stage microclimate modeling, 4x hackathon winner framework, team communication, leadership, and pitching with clarity. |

---

## 🔍 Detailed Session Summaries

### 1. [Onboarding & Kickoff Session](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/sessions-dialogue/1-onboarding-kickoff-session.md)
* **Objective:** Official launch of the FortyGuard Hackathon'26 (*Building the World's Temperature AI*).
* **Key Guidelines:**
  * Hard submission deadline: **August 30, 2026, at 11:59 PM GST**.
  * Deliverables: Working live URL / deployed application, 3-minute video presentation, public GitHub repository with `Hackathon FG` invited as a collaborator.
  * API Scope: 2-meter resolution ground-level air temperature covering the United States, including 12-hour real-time AI forecasts and historical data back to 2021.
  * Security: Individual API keys generated via the Temperature Dashboard; do not commit keys to public repos.

---

### 2. [Building on the FortyGuard Temperature API®](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/sessions-dialogue/2-building-fortyguard-temperature-api.md)
* **Objective:** Deep technical walkthrough by FortyGuard's Head of Software Engineering, Fawad Shah.
* **Key Architecture Points:**
  * **Asynchronous Polling:** Heavy geospatial polygon computations execute asynchronously; clients initiate jobs and poll every 3–5 seconds until the status is `completed`.
  * **6 Core Endpoints:** Heat Map, Parcel Analytics, Time-Series / Historical Data, Forecast Data, Exceedance Layer, and Environmental Parameters.
  * **Quickstart SDK Walkthrough:** Header-based authentication (`x-api-key`), parsing GeoJSON geometries, handling rate limits, and computing temperature threshold metrics (e.g., continuous hours > 35°C).
  * **Agentic AI Track:** Guidance on orchestrating FortyGuard API endpoints inside autonomous multi-agent systems and LLM tool harnesses.

---

### 3. [Heat Intelligence Cloud: What You Can Build](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/sessions-dialogue/3-heat-cloud-webinar-session.md)
* **Objective:** Architectural exploration of the FortyGuard Heat Intelligence Cloud and live application demos across 6 key industries.
* **Core Layers:**
  1. *Surface Temperature* (2m ambient convective & radiative microclimate).
  2. *Thermal Comfort Analysis* (UTCI / Apparent Temperature).
  3. *Air Quality Indicators* (AQI, PM2.5, ozone correlation).
  4. *Land Cover Analysis* (Satellite & street-view canopy / surface segmentation).
* **6 Industry Demonstrations:** Real Estate & PropTech, Insurance & Underwriting, Municipal Urban Planning, Outdoor Worker Safety, Cold-Chain Logistics, and Electric Grid / Utility Peak Load Management.

---

### 4. [Breaking Silos with Autodesk: Data to Design](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/sessions-dialogue/4-autodesk-webinar-session.md)
* **Objective:** Bridge the gap between raw microclimate geospatial data and Architectural / Engineering / Construction (AEC) design workflows.
* **Speakers:** Jordana Rosa (Autodesk Forma specialist & 4x Hackathon Winner) & Jay (FortyGuard CEO).
* **Core Takeaways:**
  * **Autodesk Developer Network Partnership:** Integrating FortyGuard 2m data directly into Autodesk Forma, Revit, and Civil 3D for early-stage thermal performance modeling.
  * **Winning Hackathon Mindset:** Solving real industrial pain points, prioritizing team trust and communication, building rapidly, and crafting crisp impact-focused pitches.
