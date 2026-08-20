# Heat Intelligence — FortyGuard Temperature API®

> **Official Endpoint:** `POST https://api.fortyguard.com/v1/heat_intelligence`  
> **Plan Availability:** <span style="color:#8b5cf6;font-weight:bold;">PREMIUM</span> (API Premium plan only)  
> **Official Docs Source:** [https://docs-api.fortyguard.com/docs/heat-intelligence](https://docs-api.fortyguard.com/docs/heat-intelligence)

Heat Intelligence transforms raw temperature data into comprehensive, multi-dimensional intelligence reports for any urban location. This service examines spatial and temporal temperature patterns through five targeted analytics categories—Geographic, Environmental, Urban, Events, and Anthropogenic—providing deep, actionable insights for urban planning, climate resilience, and infrastructure design.

---

## 📋 Request Parameters

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `latitude` | `number` | **Yes** | Latitude coordinate of the location to analyze. |
| `longitude` | `number` | **Yes** | Longitude coordinate of the location to analyze. |
| `temperature` | `number` | **Yes** | Temperature value in degrees Celsius for the location. |
| `date` | `string` | **Yes** | Date for the temperature reading in YYYY-MM-DD format. Must fall between 2019-01-01 and 12 hours past the current time, and should match the date/time of the heatmap that produced this temperature. Out-of-range dates are rejected with 400 Bad Request. |
| `analysis` | `array[string]` | **Yes** | Type of analysis options:<br>• "geographic"<br>• "environmental"<br>• "urban"<br>• "events"<br>• "anthropogenic" |


### 🔬 Analysis Dimensions

Pass a list containing any of the 5 supported analysis categories in the `analysis` array:
- `"geographic"` — Topographic, elevation, and regional spatial heat patterns.
- `"environmental"` — Atmospheric, humidity, solar exposure, and microclimate factors.
- `"urban"` — Built environment, building footprint, surface materials, and canyon heat entrapment.
- `"events"` — Anomalous microclimate spikes and temporal heatwave events.
- `"anthropogenic"` — Human-made heat emissions (traffic, industrial equipment, AC heat exhaust).

---

## 💻 Request Example (Python)

```python
import requests

response = requests.post(
    'https://api.fortyguard.com/v1/heat_intelligence',
    headers={
        'api-key': 'YOUR_API_KEY',
        'Content-Type': 'application/json'
    },
    json={
        'latitude': 40.7128,
        'longitude': -74.0060,
        'temperature': 34.5,
        'date': '2024-07-15',
        'analysis': [
            'geographic',
            'environmental',
            'urban',
            'events',
            'anthropogenic'
        ]
    }
)

print(response.json())
```

---

## 📥 Responses

### 1. Initial Submission Response (HTTP 200)
```json
{
  "error": false,
  "status_code": 200,
  "message": "Heat Intelligence Submitted Successfully",
  "data": {
    "activity_id": "f3e1c68b-1cc3-46bc-8589-1faaf30ef30a"
  }
}
```

### 2. Completed Status Response (HTTP 200 from GET /v1/status/{activity_id})
```json
{
  "error": false,
  "status_code": 200,
  "message": "Completed",
  "data": {
    "activity_id": "f3e1c68b-1cc3-46bc-8589-1faaf30ef30a",
    "status": "Completed",
    "result": {
      "download_link": "https://storage.fortyguard.com/reports/heat-intelligence-f3e1c68b.pdf?token=..."
    }
  }
}
```

### 📊 Result Delivery & Schema Info
Heat Intelligence uses the same status endpoint as other asynchronous activities, but the completed status response returns JSON with data.result.download_link. The status endpoint does not stream the PDF directly.

Heat Intelligence report generation may take several minutes. The download_link is temporary. Use it immediately to download the PDF, do not log or share the full signed URL, and stop polling once Completed and download_link are returned. Failed is a terminal status.

> [!WARNING]
> **Temporary Download Link:** `data.result.download_link` is a temporary presigned URL. Fetch and persist the PDF file immediately. Do not log or expose the full signed URL in client-side code.
