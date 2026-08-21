# Release Notes - FortyGuard Temperature API®

> **Official Docs Source:** [https://docs-api.fortyguard.com/docs/release-notes](https://docs-api.fortyguard.com/docs/release-notes)

A running log of every change to FortyGuard's Temperature API® and its documentation.

---

## 🚀 Version 1.0.0 - Initial Public Release
*Release Date: April 22, 2026*

First general-availability release of the FortyGuard Enterprise API. Introduces the core Temperature API® surface, two subscription plans, credit tracking, and complete documentation for every supported endpoint.

### ✨ Added (Endpoints & Services)
- `POST /v1/heatmap` - Generate high-resolution GeoJSON thermal maps for a polygon AOI across Single Hour, Range of Hours, Single Day, and Range of Days filters at granularity 60m / 80m / 100m. Supports Snapshot (`tcm`), Time of Measure, Exceedance, and Persistence analytics.
- `POST /v1/satellite` - Tile-based satellite view segmentation with Base64-encoded imagery and per-class coverage metrics.
- `POST /v1/streetview` - Ground-level street view segmentation including front (and optional back) view with per-class coverage metrics.
- `POST /v1/heat_intelligence` - Multi-dimensional Heat Intelligence Reports across Geographic, Environmental, Urban, Events, and Anthropogenic categories, delivered via temporary presigned `download_link`.
- `POST /v1/env_params` - Environmental Parameters including Heat Index, Apparent Temperature, Wet-Bulb Temperature, Relative Humidity, AQI ($PM_{2.5}$, $PM_{10}$, $NO_2$, $CO$, $O_3$, $SO_2$), Methane, $CO_2$, and Solar Irradiance (GHI, DNI, DHI).
- `GET /v1/status/{activity_id}` - Unified status and result-retrieval endpoint for all asynchronous task submissions.
- `POST /v1/system/fetch-api-key-usage` & `POST /v1/system/fetch-api-key-custom-usage` - Real-time credit usage reporting at billing-cycle and custom date-range granularity.
- **Direct API Key Header Auth:** Direct authentication via `api-key` request header (no OAuth or token exchange required).

### 🏷️ Plans & Access Control
- **API Basic Plan:** 1,000,000 monthly credits, commercial license, heatmaps up to 10 mi², full Map Statistics, and up to 3 customizable environmental parameters per request.
- **API Premium Plan:** 5,000,000 monthly credits, commercial license, heatmaps up to 50 mi², full access to all Environmental Parameters, plus Satellite Segmentation, Street View Segmentation, Heat Intelligence Reports, and Temperature Property APIs.
- **Per-endpoint plan badges** and in-page availability banners across all documentation views.

### 📚 Documentation & Developer Tools
- Complete Quickstart guide with asynchronous submit-and-poll code samples.
- Known Limitations and Input Validation rules reference.
- Interactive API Credit Usage tracker tool.
