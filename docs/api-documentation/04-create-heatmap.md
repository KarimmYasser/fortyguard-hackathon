# Create Heatmap - FortyGuard Temperature API®

> **Official Endpoint:** `POST https://api.fortyguard.com/v1/heatmap`  
> **Plan Availability:** <span style="color:#10b981;font-weight:bold;">BOTH</span> (Basic: Up to 10 mi² | Premium: Up to 50 mi²)  
> **Official Docs Source:** [https://docs-api.fortyguard.com/docs/create-heatmap](https://docs-api.fortyguard.com/docs/create-heatmap)

The Heatmap Generation feature produces high-resolution thermal maps derived from spatial and temporal inputs. Built on FortyGuard's proprietary Large Temperature Models (LTMs), each output is a GeoJSON polygon layer with tiles containing predicted or observed temperature data.

---

## 🎯 Overview & Analytics Modes

The Heatmap Generation endpoint computes 2-meter air temperature rasters across polygon areas of interest. It supports 4 distinct analytical modes via `analytic_type`:

1. **`tcm` (Default):** Temperature snapshot raster returning temperature in degrees Celsius (°C) for each spatial grid cell.
2. **`time_of_measure`:** Returns the exact hour of the day (0-23, UTC) at which the maximum peak temperature occurs in each cell.
3. **`exceedance`:** Calculates the total number of hours the temperature exceeded (or fell below) a user-defined threshold (°C) within the time window.
4. **`persistence`:** Calculates the longest continuous consecutive sequence of hours where the temperature remained beyond the threshold (°C). Measures cumulative *thermal soak*.

---

## 📋 Request Parameters

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `polygon_aoi` | `object` | **Yes** | GeoJSON polygon defining the area of interest for heatmap generation. |
| `date_time` | `object` | **Yes** | Date and time range configuration object. |
| `date_time.start_date` | `string` | **Yes** | Start date in YYYY-MM-DD format. Supported range: 2019-01-01 through 12 hours past the current time.<br>• 2019 up to now - historical / real-time heatmaps<br>• up to 12 hours into the future - forecast heatmaps<br>Dates before 2019, or more than 12 hours ahead of the current time, are rejected with 400 Bad Request. |
| `date_time.filter_type` | `number` | **Yes** | Filter type options:<br>• 1 (Single Hour) - requires start_date and start_time<br>• 2 (Range of Hours, same day) - requires start_date, start_time, and end_time<br>• 3 (Single Day) - requires only start_date (covers 00:00-23:59)<br>• 4 (Range of Days - week / month, ≤ 1 month) - requires start_date and end_date |
| `granularity` | `number` | **Yes** | Spatial resolution/granularity level options:<br>• 60m<br>• 80m<br>• 100m |
| `date_time.end_date` | `string` | No | End date in YYYY-MM-DD format. Required for filter_type 4; auto-populated for filter_type 1-3. |
| `date_time.start_time` | `string` | No | Start time in HH:MM 24-hour format. Required for filter_type 1 and 2. |
| `date_time.end_time` | `string` | No | End time in HH:MM 24-hour format. Required for filter_type 2. Auto-calculated for filter_type 1 (start_time + 1 hour). |
| `analytic_type` | `string` | No | Analysis heatmap type (default 'tcm'):<br>• tcm - Temperature snapshot; value is temperature (°C) per tile<br>• time_of_measure - hour of day (0-23, UTC) at which the peak temperature occurs<br>• exceedance - number of hours the temperature passes the threshold<br>• persistence - longest continuous run of hours past the threshold<br>time_of_measure, exceedance and persistence return values in hours (stats_data.units = "hour"); tcm returns °C. |
| `threshold` | `number` | No | Temperature threshold in °C for exceedance / persistence. Defaults to 30 °C. Ignored by tcm and time_of_measure. |
| `direction` | `string` | No | Threshold direction for exceedance / persistence: 'above' (default) counts hours above the threshold, 'below' counts hours below it. Ignored by tcm and time_of_measure. |


### 🕒 Filter Types Explained

| `filter_type` | Name | Description | Required Parameters |
| :--- | :--- | :--- | :--- |
| **1** | Single Hour | Analyzes a specific 1-hour timestamp | `start_date`, `start_time` |
| **2** | Range of Hours | Analyzes hourly variation within the same day (max 23 hrs) | `start_date`, `start_time`, `end_time` |
| **3** | Single Day | Full 24-hour day aggregate (00:00 to 23:59) | `start_date` |
| **4** | Range of Days | Multi-day or multi-week aggregate (up to 1 month) | `start_date`, `end_date` |

---

## 💻 Request Examples

### 1. Single Hour (Snapshot)
```python
import requests

response = requests.post(
    'https://api.fortyguard.com/v1/heatmap',
    headers={'api-key': 'your_api_key', 'Content-Type': 'application/json'},
    json={
        'polygon_aoi': {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'properties': {},
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [[
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
        'date_time': {
            'start_date': '2024-07-15',
            'start_time': '14:00',
            'filter_type': 1
        },
        'granularity': 100
    }
)
print(response.json())
```

### 2. Exceedance Analysis (Hours above 40°C)
```python
import requests

response = requests.post(
    'https://api.fortyguard.com/v1/heatmap',
    headers={'api-key': 'your_api_key'},
    json={
        'polygon_aoi': {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'properties': {},
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [[
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
        'date_time': {
            'start_date': '2024-07-15',
            'start_time': '06:00',
            'end_time': '18:00',
            'filter_type': 2
        },
        'granularity': 100,
        'analytic_type': 'exceedance',
        'threshold': 40,
        'direction': 'above'
    }
)
```

### 3. Thermal Persistence Analysis (Continuous Soak)
```python
import requests

response = requests.post(
    'https://api.fortyguard.com/v1/heatmap',
    headers={'api-key': 'your_api_key'},
    json={
        'polygon_aoi': {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'properties': {},
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [[
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
        'date_time': {
            'start_date': '2024-07-15',
            'start_time': '06:00',
            'end_time': '18:00',
            'filter_type': 2
        },
        'granularity': 100,
        'analytic_type': 'persistence',
        'threshold': 35,
        'direction': 'above'
    }
)
```

### 4. Time of Measure Analysis (Peak Hour)
```python
import requests

response = requests.post(
    'https://api.fortyguard.com/v1/heatmap',
    headers={'api-key': 'your_api_key'},
    json={
        'polygon_aoi': {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'properties': {},
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [[
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
        'date_time': {
            'start_date': '2024-07-15',
            'filter_type': 3
        },
        'granularity': 100,
        'analytic_type': 'time_of_measure'
    }
)
```

---

## 📥 Responses

### 1. Initial Submission Response (HTTP 200)
```json
{
  "error": false,
  "status_code": 200,
  "message": "Heatmap Submitted Successfully",
  "data": {
    "activity_id": "f52d2453-6a59-4b31-afa3-8fe3bb1ac5df"
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
    "activity_id": "f52d2453-6a59-4b31-afa3-8fe3bb1ac5df",
    "status": "Completed",
    "result": {
      "map_data": {},
      "stats_data": {}
    }
  }
}
```

### 📊 Result Schema Breakdown
Once the heatmap generation activity has finished processing, the final response contains two main outputs:
• GeoJSON heatmap tiles (map_data)
• Aggregated temperature statistics (stats_data)

This response is returned when the activity status is "Completed".

#### `Result.map_data` (`GeoJSON FeatureCollection`)
Tile-based heatmap output formatted as GeoJSON polygons.

#### `Result.stats_data` (`object`)
Aggregated statistical summary of all tiles in the heatmap. This includes:
• Temperature_stats - Temperature statistics across the heatmap region
 - Minimum: Lowest temperature across the heatmap region
 - Maximum: Highest temperature across the heatmap region
 - Mean: Average temperature value
 - Standard_deviation: Variability of temperatures across tiles
• Overall_temperature_distribution (array[number]) - Sorted temperature values representing the overall distribution
• Normal_temperature_distribution (object) - Normalized curve data for plotting a temperature distribution
 - x_axis: Temperature range
 - y_axis: Probability density values
• Temperature_frequency (object) - Histogram-style frequency counts for temperature bins
