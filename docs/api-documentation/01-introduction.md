# Introduction - FortyGuard Temperature API®

> **Official Docs Source:** [https://docs-api.fortyguard.com/docs/introduction](https://docs-api.fortyguard.com/docs/introduction)  
> **Framework:** FortyGuard Temperature Operating System (tOS)  
> **Core Engine:** Proprietary Large Temperature Models (LTMs)  

As cities grapple with intensifying heat and climate volatility, the need for precise, actionable urban temperature intelligence has never been more urgent. The FortyGuard API Services framework responds to this challenge by offering a powerful suite of heat-intelligent endpoints that translate granular temperature data into operational insights.

This documentation provides a comprehensive overview of the technical capabilities, service architecture, and data workflows that define FortyGuard's **Temperature API®**. Built upon our proprietary **Large Temperature Models (LTMs)**, these APIs enable developers, urban planners, logistics coordinators, and policymakers to seamlessly integrate climate context into digital platforms and physical infrastructure decisions.

---

## 🌟 Core Capabilities

Our API suite provides:
- **Real-Time & Forecasted Heatmaps:** High-resolution 2-meter air temperature mapping across 60m, 80m, and 100m spatial resolutions with up to 12-hour predictive forecasting.
- **Advanced Computer Vision Segmentation:** Pixel-level classification of satellite imagery and street-level panoramic views to quantify urban materials, vegetation, and thermal properties.
- **Comprehensive Environmental Parameters:** Multi-dimensional microclimate indices including Heat Index, Apparent Temperature, Wet-Bulb Temperature, AQI pollutants (PM2.5, PM10, NO₂, CO, O₃, SO₂), greenhouse gases (CO₂, Methane), and Solar Irradiance (GHI, DNI, DHI).
- **Heat Intelligence & Property Reports:** Automated multi-dimensional diagnostic reports synthesizing Geographic, Environmental, Urban, Event-based, and Anthropogenic factors.

---

## 🏷️ Plan Availability & Tiers

Each endpoint in this documentation is tagged with its subscription requirement:

| Tier Badge | Description | Included Services |
| :--- | :--- | :--- |
| <span style="color:#10b981;font-weight:bold;">BOTH</span> | Available on both **API Basic** and **API Premium** | Heatmaps (up to 10 mi²), Map Statistics, Environmental Parameters (up to 3/request), Status Polling, Credit Tracking |
| <span style="color:#3b82f6;font-weight:bold;">BASIC</span> | Included in **API Basic** | 1,000,000 monthly credits, Commercial License, Heatmap generation (≤10 mi²), Environmental Parameters (≤3/req) |
| <span style="color:#8b5cf6;font-weight:bold;">PREMIUM</span> | Exclusive to **API Premium** | 5,000,000 monthly credits, Commercial License, Heatmap generation (≤50 mi²), Full Environmental Parameters, Tile Satellite Segmentation, Street View Segmentation, Heat Intelligence Reports |

---

## 🏙️ Key Use Cases

1. **Climate-Aware Infrastructure Planning:**  
   Use temperature intelligence and environmental parameters to design and maintain roads, transformers, electrical enclosures, bridges, and public utilities to withstand extreme heat stress.
2. **Property & Asset Intelligence:**  
   Generate property-level heat performance reports to assess livability, operational efficiency, and financial risk - supporting ESG appraisals and insurance underwriting.
3. **Smart Mobility & Logistics:**  
   Integrate thermal comfort-based routing and forecasted heat zones into transportation networks, delivery fleets, and cold chains to reduce energy consumption and improve worker safety.
4. **Environmental & Health Monitoring:**  
   Track apparent temperature, wet-bulb thresholds, and air quality pollutants to power heatwave early warning systems.
5. **Urban Design & Public Space Optimization:**  
   Leverage microclimate models to guide placement of shade canopies, cool pavement coatings, and urban greening.
6. **Energy & Building Systems Planning:**  
   Combine solar irradiance, temperature, and humidity data to forecast HVAC cooling loads and optimize renewable energy placement.
