# Quickstart Guide — FortyGuard Temperature API®

> **Official Docs Source:** [https://docs-api.fortyguard.com/docs/quickstart](https://docs-api.fortyguard.com/docs/quickstart)

Get started with the FortyGuard Enterprise API in minutes. This guide will help you authenticate, make your first asynchronous request, track its lifecycle, and retrieve your final results.

---

## 🔑 1. Authentication

All requests to the FortyGuard Enterprise API require an API key passed in the request headers:

```http
api-key: YOUR_API_KEY
Content-Type: application/json
```

> [!NOTE]
> No OAuth or token exchange is required. Your API key alone provides secure, authenticated access.

---

## 🚀 2. Asynchronous Task Workflow

The FortyGuard Engine processes high-resolution geospatial models and Large Temperature Models asynchronously:

1. **Submit Task (POST):** You call an analysis endpoint (e.g. `/v1/heatmap`, `/v1/env_params`, `/v1/satellite`, `/v1/streetview`, `/v1/heat_intelligence`).
2. **Receive Activity ID:** The API immediately returns an `activity_id` with status `"Processing"`.
3. **Poll Status (GET):** Query `GET /v1/status/{activity_id}` until the status transitions to `"Completed"` or `"Failed"`.
4. **Retrieve Results:** The completed status response body contains your final data payload (GeoJSON, array data, or download link).

---

## 📊 Status & Response Codes Table

| Response / Status | Meaning | Action Required |
| :--- | :--- | :--- |
| **200 / 202** | Request accepted or status retrieved | Inspect JSON response |
| **400 / 422** | Invalid request parameters or validation error | Fix payload format (coordinates, dates) |
| **401** | Missing or invalid API key | Verify `api-key` header |
| **403** | Insufficient plan access or unauthorized tier | Upgrade to API Premium if required |
| **404** | Activity not found or not yet indexed | Retry status check after a short delay |
| **429** | Rate limit exceeded | Back off and retry |
| **500** | Server-side processing error | Check logs and retry or contact support |
| **`Submitted` / `Processing`** | Task is actively computing | Continue bounded polling (e.g. every 2–5s) |
| **`Completed`** | Task finished successfully | Retrieve result data payload (Credits deducted) |
| **`Failed`** | Task execution failed | Stop polling, record activity_id (No credits deducted) |

> [!IMPORTANT]
> Credits are **only deducted** after successful task completion (`status: "Completed"`). Failed tasks do not consume credits.

---

## 🐍 End-to-End Python Example

```python
import time
import requests

API_KEY = "YOUR_API_KEY"
HEADERS = {
    "api-key": API_KEY,
    "Content-Type": "application/json"
}

# -------------------------------------------------------------
# Step 1: Submit your task (e.g. Heatmap generation)
# -------------------------------------------------------------
submit_url = "https://api.fortyguard.com/v1/heatmap"
payload = {
    "polygon_aoi": {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-74.0170, 40.7050],
                        [-74.0030, 40.7050],
                        [-74.0030, 40.7180],
                        [-74.0170, 40.7180],
                        [-74.0170, 40.7050]
                    ]]
                }
            }
        ]
    },
    "date_time": {
        "start_date": "2024-07-15",
        "start_time": "14:00",
        "filter_type": 1  # Single Hour
    },
    "granularity": 100
}

response = requests.post(submit_url, headers=HEADERS, json=payload)
response.raise_for_status()
submit_data = response.json()

activity_id = submit_data["data"]["activity_id"]
print(f"Task submitted successfully. Activity ID: {activity_id}")

# -------------------------------------------------------------
# Step 2: Poll task status until Completed or Failed
# -------------------------------------------------------------
status_url = f"https://api.fortyguard.com/v1/status/{activity_id}"
max_attempts = 30
poll_interval_seconds = 3

for attempt in range(max_attempts):
    time.sleep(poll_interval_seconds)
    status_response = requests.get(status_url, headers=HEADERS)
    
    if status_response.status_code == 200:
        result_data = status_response.json()
        current_status = result_data["data"].get("status")
        print(f"[{attempt + 1}/{max_attempts}] Status: {current_status}")
        
        if current_status == "Completed":
            print("Task completed successfully!")
            results = result_data["data"]["result"]
            # Process GeoJSON tiles or statistics
            print(f"Received result keys: {list(results.keys())}")
            break
        elif current_status == "Failed":
            print(f"Task failed: {result_data.get('message', 'Unknown failure')}")
            break
    else:
        print(f"Status check HTTP {status_response.status_code}: {status_response.text}")
```
