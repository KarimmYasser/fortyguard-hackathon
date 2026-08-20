# Error Handling & Diagnostics — FortyGuard Temperature API®

> **Official Docs Source:** [https://docs-api.fortyguard.com/docs/errors](https://docs-api.fortyguard.com/docs/errors)

Understand error codes, response payloads, and mitigation strategies for the FortyGuard Temperature API®.

---

## 🚨 HTTP Status Code Matrix

| Status Code | Reason | Description & Troubleshooting |
| :--- | :--- | :--- |
| **`200 OK`** | Success | Request accepted or status query succeeded. |
| **`400 Bad Request`** | Validation Failure | Invalid geometry, malformed GeoJSON, invalid date format (must be YYYY-MM-DD), out-of-bounds date (< 2019 or > now + 12h), or unsupported filter type. **No credits charged.** |
| **`401 Unauthorized`** | Missing/Invalid Key | Request header `api-key` is missing, expired, or invalid. |
| **`403 Forbidden`** | Tier Limitation | Attempted to call a Premium-only endpoint (e.g., Satellite, Streetview, Heat Intelligence) using an API Basic key, or exceeded plan area limits (>10 mi² on Basic). |
| **`404 Not Found`** | Resource Missing | Invalid `activity_id` or task record not yet synchronized. |
| **`422 Unprocessable`** | Semantic Error | Coordinates outside supported geographic region (current release supports US only). |
| **`429 Too Many Requests`** | Rate Limit | Burst concurrency limit reached. Back off exponentially and retry. |
| **`500 Internal Error`** | Engine Failure | Upstream compute failure during ML execution. Failed activities do **not** deduct credits. |

---

## 📋 Standard Error JSON Payload

```json
{
  "error": true,
  "status_code": 400,
  "message": "Invalid date_time: start_date cannot be earlier than 2019-01-01 or more than 12 hours in the future.",
  "data": null
}
```

---

## 🛡️ Robust Client-Side Resilience Pattern (Python)

```python
import time
import requests
from requests.exceptions import HTTPError

def submit_with_retry(url, headers, payload, max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 429:
                wait_time = attempt * 2
                print(f"Rate limited (429). Retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue
                
            response.raise_for_status()
            return response.json()
            
        except HTTPError as e:
            if response.status_code in [400, 401, 403, 422]:
                # Permanent client errors - fail immediately
                raise ValueError(f"Client error {response.status_code}: {response.text}") from e
            elif attempt == max_retries:
                raise
            time.sleep(2 ** attempt)
            
    raise RuntimeError("Max retries exceeded")
```
