# 📋 FortyGuard Hackathon '26 — Registration & Submission Portals

This document tracks both the initial event registration details and the final project submission requirements for **PyreShield AI**.

---

## Part 1: Initial Hackathon Registration Form

* **Target Form URL:** [https://www.fortyguard.com/hackathon-registration](https://www.fortyguard.com/hackathon-registration)  
* **Webhook Target:** `https://n8n.srv1629125.hstgr.cloud/webhook/hackathon-register`

### Field-by-Field Initial Registration Values

| Field Name | Type | Value Submitted | Notes / Dropdown Options |
| :--- | :--- | :--- | :--- |
| **Full Name \*** | Text | `Karim Yasser` | As in resume |
| **Email \*** | Email | `karimmyasserr@gmail.com` | Primary contact email |
| **Role \*** | Dropdown | `Student` | `Developer`, `Designer`, `Student`, `Researcher`, `Data Scientist`, `Product Manager`, `Entrepreneur`, `Other` |
| **Organization or University \*** | Text | `Cairo University, Faculty of Engineering` | Bachelor of Computer Engineering (GPA 3.84) |
| **Country \*** | Text | `Egypt` | |
| **City \*** | Text | `Cairo` | |
| **Experience Level \*** | Dropdown | `Intermediate (1–3 years)` | `Beginner (0–1 years)`, `Intermediate (1–3 years)`, `Advanced (3–5 years)`, `Expert (5+ years)` |
| **How are you taking part? \*** | Radio | `I’m taking part solo` | Solo participation (or team 2–3) |
| **How Did You Hear About Us? \*** | Dropdown | `Social Media` | `Social Media`, `Friend / Colleague`, `Newsletter`, `Blog / Article`, `Search Engine`, `Event / Conference`, `Other` |
| **Agreement Checkbox** | Checkbox | `true` (Checked) | Agree to hackathon updates & communications |

### Initial "Your Idea & Motivation" Text Submitted

```text
I'm applying under Track 06 (Agentic AI) and Track 02 (Future Buildings & Energy) to build an autonomous thermal hazard and electrical fire prevention agent called PyreShield AI.

This project addresses a severe local hazard in my home country, Egypt. During recent record heatwaves, cities have faced a wave of appliance explosions and building fires when outdoor AC compressors, exposed electrical panels, and battery storage systems overheat. The reason standard weather tools fail to prevent these disasters is simple: standard forecasts measure air high above open fields, but the equipment that explodes sits in the street-level microclimate—within 2 meters of hot asphalt and concrete. A city forecast might report a manageable 39°C, while the ambient air 2 meters above the ground in an unshaded street canyon hits an extreme 49°C, triggering thermal runaway and electrical arc explosions.

FortyGuard’s 2-meter street-level Temperature API solves this exact blind spot. I am building a LangGraph agent pipeline that maps critical building infrastructure (rooftop/balcony HVAC condensers, street-level power transformers, and EV charging hubs) to FortyGuard's 2-meter temperature, exceedance, and persistence layers. 

By measuring the real boundary-layer air surrounding these assets, the agent:
1. Detects cumulative thermal soak (hours spent above equipment safety ratings like 40°C/45°C) using FortyGuard's persistence endpoint.
2. Predicts explosion and blowout risks 12 hours ahead using short-range forecast intelligence.
3. Autonomously triggers B2B facility load-shedding and HVAC duty-cycling schedules to prevent commercial fires, while dispatching proactive hazard alerts to residents.

My motivation stems from wanting to turn cutting-edge thermal AI into a life-saving tool. I recently completed an AI research internship at Nile University's SESC Research Center, where I built an autonomous multi-agent pipeline and 19-tool MCP harness for OpenFOAM thermal/CFD simulations—research my supervisor is publishing into a peer-reviewed paper with our team as co-authors. Having engineered thermodynamic constraint layers, boundary parsers, and self-healing agent harnesses, I want to leverage FortyGuard’s 2-meter resolution data to build an autonomous system that stops heat-induced electrical explosions before they happen.
```

---

## Part 2: Final Project Submission Form (Due Aug 30, 2026, 11:59 PM GST)

* **Official Final Submission Form:** [https://forms.gle/jLgBzVTG1NhJ3gNe6](https://forms.gle/jLgBzVTG1NhJ3gNe6)
* **Team Channel Setup Form (if needed):** [https://forms.gle/CCCvSNgDsDiNZ2gk7](https://forms.gle/CCCvSNgDsDiNZ2gk7)

### Required Field-by-Field Blueprint for PyreShield AI

| Field Name | Description & Requirement | PyreShield AI Prepared Entry |
| :--- | :--- | :--- |
| **1. Project Title** | Title of the project | `PyreShield AI — Autonomous Microclimate Thermal Runaway & Electrical Fire Prevention Agent` |
| **2. One-Line Pitch** | Clear, catchy one-line summary | `Autonomous LangGraph agent utilizing FortyGuard 2m persistence layers to predict and prevent heat-induced building fires, transformer blowouts, and HVAC thermal runaway.` |
| **3. Primary Track** | Main track evaluated for judging | `Track 6 — Agentic Track (API + Agentic AI)` |
| **4. Secondary Tracks** | Up to 2 optional tags | `Track 2 — Future Buildings & Energy`, `Track 3 — Industrial & Enterprise` |
| **5. Target User & Problem** | Who benefits & pain point solved | Facility managers, municipal grid operators, EV charging network engineers, and property insurers facing heat-induced equipment explosions and electrical fires caused by microclimate boundary-layer thermal soak. |
| **6. Geography & Dates** | US location & date range analyzed | U.S. dense urban heat islands (e.g., Phoenix, AZ / Las Vegas, NV / Houston, TX) across summer 2024–2026 + 12-hour predictive forecast windows. |
| **7. FortyGuard API Usage** | How FortyGuard endpoints were used | Polling `/v1/heatmap` with `analytic_type="persistence"` & `"exceedance"` to measure cumulative asset thermal soak past 40°C/45°C; `/v1/env_params` for point solar irradiance/heat index; `/v1/satellite` for surface reflectivity. |
| **8. API Key ID** | Key submitted for verification | `<YOUR_FORTYGUARD_API_KEY_OR_ID>` (so judges can verify API credit consumption on backend). |
| **9. AI Tools Used** | Disclose AI tools/models | Anthropic Claude, LangGraph, Python FastAPI, Mapbox GL JS. |
| **10. Code Repo Link** | Public GitHub or GitLab repo | `https://github.com/karimmyasser/pyreshield-ai` *(Add `Hackathon-FG` / `hackathon@fortyguard.com` if private)*. |
| **11. Live Demo URL** | Hosted web app (no login barrier) | Deployed live URL (e.g. Vercel/Render/Fly.io) tested in Incognito window. |
| **12. Demo Video Link** | YouTube / Loom video (max 3 min) | YouTube/Loom video with UI demo + voiceover walkthrough. |
