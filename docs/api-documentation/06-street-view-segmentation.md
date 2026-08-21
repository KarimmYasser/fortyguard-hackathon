# Street View Segmentation - FortyGuard Temperature API®

> **Official Endpoint:** `POST https://api.fortyguard.com/v1/streetview`  
> **Plan Availability:** <span style="color:#8b5cf6;font-weight:bold;">PREMIUM</span> (API Premium plan only)  
> **Official Docs Source:** [https://docs-api.fortyguard.com/docs/street-view-segmentation](https://docs-api.fortyguard.com/docs/street-view-segmentation)

This endpoint performs segmentation analysis on street view imagery to identify and classify urban features, building facades, vegetation, road surfaces, and thermal characteristics from ground-level perspectives.

---

## 📋 Request Parameters

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `latitude` | `number` | **Yes** | Latitude coordinate of the street view location. |
| `longitude` | `number` | **Yes** | Longitude coordinate of the street view location. |
| `vertical_angle` | `number` | **Yes** | Vertical viewing angle in degrees (tilt up/down). |
| `horizontal_angle` | `number` | **Yes** | Horizontal viewing angle in degrees (pan left/right, 0-360). |
| `back_view` | `boolean` | **Yes** | Whether to capture the back view (opposite direction). |


---

## 💻 Request Example (Python)

```python
import requests

response = requests.post(
    'https://api.fortyguard.com/v1/streetview',
    headers={
        'api-key': 'YOUR_API_KEY',
        'Content-Type': 'application/json'
    },
    json={
        'latitude': 40.7128,
        'longitude': -74.0060,
        'vertical_angle': 10.0,
        'horizontal_angle': 90.0,
        'back_view': False
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
  "message": "Street View Segmentation Submitted Successfully",
  "data": {
    "activity_id": "e574b989-c100-4a03-97d8-beef65656623"
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
    "activity_id": "e574b989-c100-4a03-97d8-beef65656623",
    "status": "Completed",
    "result": {
      "coordinates": {
        "latitude": "40.7128",
        "longitude": "-74.006"
      },
      "front": {
        "original_image": "",
        "segments": {},
        "image_legend": {},
        "segmented_image": "",
        "image_date": "YYYY-MM-DD"
      }
    }
  }
}
```

### 📊 Result Schema Breakdown
#### `Coordinates` (`object`)
Location that was analyzed.
• latitude (string) - Latitude value
• longitude (string) - Longitude value

#### `Front` (`object`)
Street View "front" camera results for that location.
• original_image (string) - Base64-encoded original street view image. Note: If raw Base64, users may need data:image/png;base64, to render in a browser
• segments (object) - Class coverage values (typically percentages of the image)
• image_legend (object) - RGB color legend for rendering the segmentation output
• segmented_image (string) - Base64-encoded segmentation mask image, decode to display/save the segmentation output
• image_date (string) - Date the Street View image was captured, in YYYY-MM-DD format
