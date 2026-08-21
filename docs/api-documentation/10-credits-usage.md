# Check API Credits Usage - FortyGuard Temperature API®

> **Official Endpoints:**  
> - `POST https://api.fortyguard.com/v1/system/fetch-api-key-usage`  
> - `POST https://api.fortyguard.com/v1/system/fetch-api-key-custom-usage`  
> **Plan Availability:** <span style="color:#10b981;font-weight:bold;">BOTH</span> (Available across all plans)  
> **Official Docs Source:** [https://docs-api.fortyguard.com/docs/credits-usage](https://docs-api.fortyguard.com/docs/credits-usage)

Track your API key credit consumption, view current billing cycle limits, inspect subscription status, and monitor per-service credit burn rates.

---

## 🔌 1. Billing Cycle Usage Endpoint

Fetches the current active subscription cycle summary, total quota, used credits, and service breakdown.

- **URL:** `POST https://api.fortyguard.com/v1/system/fetch-api-key-usage`
- **Headers:** `api-key: YOUR_API_KEY` or pass key in JSON body
- **Request Body:**
```json
{
  "api_key": "YOUR_API_KEY"
}
```

### Response Payload Structure
```json
{
  "error": false,
  "status_code": 200,
  "data": {
    "plan_name": "API Premium",
    "total_credits": 5000000,
    "credits_used": 142300,
    "credits_remaining": 4857700,
    "credits_reset_date": "2026-09-01T00:00:00Z",
    "status": "Active",
    "services_breakdown": [
      { "name": "Heatmap Generation", "credits": 85000, "percentage": 59.7 },
      { "name": "Tile Satellite Segmentation", "credits": 25000, "percentage": 17.6 },
      { "name": "Streetview Segmentation", "credits": 18000, "percentage": 12.6 },
      { "name": "Environment Parameter Analysis", "credits": 9300, "percentage": 6.5 },
      { "name": "Heat Intelligence Report", "credits": 5000, "percentage": 3.5 }
    ]
  }
}
```

---

## 🔌 2. Custom Date-Range Usage Endpoint

Fetches granular credit consumption for an arbitrary historical window.

- **URL:** `POST https://api.fortyguard.com/v1/system/fetch-api-key-custom-usage`
- **Headers:** `api-key: YOUR_API_KEY`
- **Request Body:**
```json
{
  "api_key": "YOUR_API_KEY",
  "start_date": "2026-08-01T00:00:00Z",
  "end_date": "2026-08-20T23:59:59Z"
}
```

---

## 🐍 Python Verification Script

```python
import requests

def check_credits(api_key: str):
    url = "https://api.fortyguard.com/v1/system/fetch-api-key-usage"
    res = requests.post(url, json={"api_key": api_key})
    res.raise_for_status()
    data = res.json()["data"]
    
    print(f"Plan: {data.get('plan_name')}")
    print(f"Used: {data.get('credits_used'):,} / {data.get('total_credits'):,} credits")
    print(f"Remaining: {data.get('credits_remaining'):,} credits")
    print(f"Reset Date: {data.get('credits_reset_date')}")

check_credits("YOUR_API_KEY")
```
