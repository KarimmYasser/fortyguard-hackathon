# 📖 FortyGuard Temperature API® — Complete Scraped Documentation

Welcome to the complete, official FortyGuard Temperature API® documentation repository, fully scraped and organized for instant offline and programmatic access.

---

## 🗂️ Documentation Navigation

| # | Section | Description | Target Path |
| :-: | :--- | :--- | :--- |
| **01** | [Introduction](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/api-documentation/01-introduction.md) | Architectural overview, LTM physics, plan tiers, and use cases | `01-introduction.md` |
| **02** | [Quickstart Guide](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/api-documentation/02-quickstart.md) | Submit-and-poll async workflow, HTTP status codes, Python polling script | `02-quickstart.md` |
| **03** | [Authentication](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/api-documentation/03-authentication.md) | API key header format (`api-key: YOUR_KEY`), best practices, code snippets | `03-authentication.md` |
| **04** | [Create Heatmap](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/api-documentation/04-create-heatmap.md) | `POST /v1/heatmap` — Snapshot, Exceedance, Persistence, Time of Measure | `04-create-heatmap.md` |
| **05** | [Satellite View Segmentation](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/api-documentation/05-satellite-view-segmentation.md) | `POST /v1/satellite` — Tile-based computer vision land cover segmentation | `05-satellite-view-segmentation.md` |
| **06** | [Street View Segmentation](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/api-documentation/06-street-view-segmentation.md) | `POST /v1/streetview` — Ground-level facade, street, and canopy segmentation | `06-street-view-segmentation.md` |
| **07** | [Heat Intelligence](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/api-documentation/07-heat-intelligence.md) | `POST /v1/heat_intelligence` — 5-dimension deep diagnostic reports & PDF delivery | `07-heat-intelligence.md` |
| **08** | [Environmental Parameters](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/api-documentation/08-environmental-parameters.md) | `POST /v1/env_params` — Heat index, wet bulb, AQI, greenhouse gases, solar GHI/DNI/DHI | `08-environmental-parameters.md` |
| **09** | [Check Status](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/api-documentation/09-check-status.md) | `GET /v1/status/{activity_id}` — Polling lifecycle states & result payload retrieval | `09-check-status.md` |
| **10** | [Credits & Usage](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/api-documentation/10-credits-usage.md) | `POST /v1/system/fetch-api-key-usage` — Credit balances & service breakdown | `10-credits-usage.md` |
| **11** | [Error Handling](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/api-documentation/11-error-handling.md) | HTTP status codes, error payload format, retry logic | `11-error-handling.md` |
| **12** | [Known Limitations](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/api-documentation/12-known-limitations.md) | Area limits (10 vs 50 mi²), date rules (2019 to now+12h), regional coverage | `12-known-limitations.md` |
| **13** | [Release Notes](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/api-documentation/13-release-notes.md) | Changelog and platform updates (v1.0.0 GA) | `13-release-notes.md` |
| 📄 | [All-in-One Master Reference](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/api-documentation/FORTYGUARD_API_MASTER_REFERENCE.md) | Single consolidated reference file containing everything | `FORTYGUARD_API_MASTER_REFERENCE.md` |
| ⚡ | [OpenAPI 3.1 Specification](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/api-documentation/openapi.json) | Machine-readable API schema for Postman, Swagger, SDK generators | `openapi.json` |
