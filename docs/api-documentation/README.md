# 📖 FortyGuard Temperature API® - Complete Scraped Documentation

Welcome to the complete, official FortyGuard Temperature API® documentation repository, fully scraped and organized for instant offline and programmatic access.

> **⚠️ Read [14 — Field Notes](14-field-notes-live-integration.md) before writing integration code.**
> Sections 01–13 are the vendor's own documentation. Section 14 records behaviour
> we *measured* that the official docs do not state — including two cases where
> a field's name actively misleads (`env_params.temperature` echoes your input;
> `cloud_cover_octas` is a 0–100 percentage). Both silently corrupted our output
> before we caught them.

---

## 🗂️ Documentation Navigation

| # | Section | Description | Target Path |
| :-: | :--- | :--- | :--- |
| **01** | [Introduction](01-introduction.md) | Architectural overview, LTM physics, plan tiers, and use cases | `01-introduction.md` |
| **02** | [Quickstart Guide](02-quickstart.md) | Submit-and-poll async workflow, HTTP status codes, Python polling script | `02-quickstart.md` |
| **03** | [Authentication](03-authentication.md) | API key header format (`api-key: YOUR_KEY`), best practices, code snippets | `03-authentication.md` |
| **04** | [Create Heatmap](04-create-heatmap.md) | `POST /v1/heatmap` - Snapshot, Exceedance, Persistence, Time of Measure | `04-create-heatmap.md` |
| **05** | [Satellite View Segmentation](05-satellite-view-segmentation.md) | `POST /v1/satellite` - Tile-based computer vision land cover segmentation | `05-satellite-view-segmentation.md` |
| **06** | [Street View Segmentation](06-street-view-segmentation.md) | `POST /v1/streetview` - Ground-level facade, street, and canopy segmentation | `06-street-view-segmentation.md` |
| **07** | [Heat Intelligence](07-heat-intelligence.md) | `POST /v1/heat_intelligence` - 5-dimension deep diagnostic reports & PDF delivery | `07-heat-intelligence.md` |
| **08** | [Environmental Parameters](08-environmental-parameters.md) | `POST /v1/env_params` - Heat index, wet bulb, AQI, greenhouse gases, solar GHI/DNI/DHI | `08-environmental-parameters.md` |
| **09** | [Check Status](09-check-status.md) | `GET /v1/status/{activity_id}` - Polling lifecycle states & result payload retrieval | `09-check-status.md` |
| **10** | [Credits & Usage](10-credits-usage.md) | `POST /v1/system/fetch-api-key-usage` - Credit balances & service breakdown | `10-credits-usage.md` |
| **11** | [Error Handling](11-error-handling.md) | HTTP status codes, error payload format, retry logic | `11-error-handling.md` |
| **12** | [Known Limitations](12-known-limitations.md) | Area limits (10 vs 50 mi²), date rules (2019 to now+12h), regional coverage | `12-known-limitations.md` |
| **13** | [Release Notes](13-release-notes.md) | Changelog and platform updates (v1.0.0 GA) | `13-release-notes.md` |
| **14** | [🔬 Field Notes: Live Integration](14-field-notes-live-integration.md) | **Measured, not documented.** Misleading field semantics, per-key job serialisation, real latencies, spatial-contrast findings | `14-field-notes-live-integration.md` |
| 📄 | [All-in-One Master Reference](FORTYGUARD_API_MASTER_REFERENCE.md) | Single consolidated reference file containing everything | `FORTYGUARD_API_MASTER_REFERENCE.md` |
| ⚡ | [OpenAPI 3.1 Specification](openapi.json) | Machine-readable API schema for Postman, Swagger, SDK generators | `openapi.json` |
