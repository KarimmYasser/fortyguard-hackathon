# Environmental Parameters - FortyGuard Temperature API®

> **Official Endpoint:** `POST https://api.fortyguard.com/v1/env_params`  
> **Plan Availability:** <span style="color:#10b981;font-weight:bold;">BOTH</span> (Basic: Up to 3 parameters/request | Premium: Full access to all parameters)  
> **Official Docs Source:** [https://docs-api.fortyguard.com/docs/environmental-parameters](https://docs-api.fortyguard.com/docs/environmental-parameters)

A multidimensional temperature intelligence service offering operationally vital metrics including heat index, apparent temperature, and wet bulb temperature for thermal stress assessment. Captures atmospheric and hydrological variables (precipitation, AQI, ozone levels) plus solar irradiance profiles (GHI, DNI, DHI) to support energy modeling, urban planning, and climate resilience.

---

## 📋 Request Parameters

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `latitude` / `point.latitude` | `number` | **Yes** | Latitude coordinate of the location. |
| `longitude` / `point.longitude` | `number` | **Yes** | Longitude coordinate of the location. |
| `temperature` | `number` | No / Contextual | Optional heat-stress threshold (e.g. `35` °C) for exceedance calculations. The API calculates and returns the actual ambient temperature along with the environmental parameters. |
| `date_time` | `object` | **Yes** | Date and time range configuration object. |
| `date_time.start_date` | `string` | **Yes** | Start date in YYYY-MM-DD format. Must fall between 2021-01-01 and 12 hours past the current time, and should match the date/time of the heatmap you generated for this location. Out-of-range dates are rejected with 400 Bad Request. |
| `date_time.filter_type` | `number` | **Yes** | Filter type options:<br>• 1 (Single Hour) - requires start_date and start_time<br>• 2 (Range of Hours) - requires start_date, start_time, and end_time<br>• 3 (Single Day) - requires only start_date |
| `date_time.end_date` | `string` | No | End date in YYYY-MM-DD format. Auto-populated based on filter_type. |
| `date_time.start_time` | `string` | No | Start time in HH:MM 24-hour format. Required for filter_type 1 and 2. |
| `date_time.end_time` | `string` | No | End time in HH:MM 24-hour format. Required for filter_type 2. |
| `analysis` | `string[]` | No | Optional list of environmental parameters to return. Omit to receive all of them. API Basic and API Startup are limited to 3 parameters per request; API Premium has full access.<br><br>Thermal & atmospheric:<br>• heat_index_celsius - heat index ("feels like"), °C<br>• apparent_temperature_celsius - apparent temperature, °C<br>• wet_bulb_temperature_celsius - wet-bulb temperature, °C<br>• relative_humidity_percent - relative humidity, %<br>• precipitation_mm - precipitation, mm<br>• cloud_cover_octas - effective cloud cover, octas<br>• elevation - ground elevation, m<br><br>Air quality (US AQI) & gases:<br>• air_quality:idx - overall US Air Quality Index<br>• air_quality_pm2p5:idx - AQI, PM2.5<br>• air_quality_pm10:idx - AQI, PM10<br>• air_quality_no2:idx - AQI, nitrogen dioxide<br>• aqi_us_co - AQI, carbon monoxide<br>• air_quality_o3:idx - AQI, ozone<br>• air_quality_so2:idx - AQI, sulphur dioxide<br>• methane_ppb - methane, ppb<br>• co2_ppm - carbon dioxide, ppm<br><br>Solar:<br>• solar_irradiance - clear-sky GHI / DNI / DHI |



---

## 🧪 Environmental Parameters Catalog (`analysis`)

You can specify a subset of parameters in the `analysis` array, or omit `analysis` on Premium to retrieve all available metrics:

### 1. Thermal Stress & Atmospheric
- `heat_index_celsius` - Heat Index ("feels like" temperature accounting for humidity), in °C.
- `apparent_temperature_celsius` - Combined perceptual temperature taking wind, humidity, and radiation into account, in °C.
- `wet_bulb_temperature_celsius` - Wet-bulb temperature indicating thermodynamic heat dissipation limit, in °C. Critical for human survivability & evaporative cooling thresholds.
- `relative_humidity_percent` - Relative atmospheric humidity percentage (0-100%).
- `precipitation_mm` - Liquid precipitation accumulation, in mm.
- `cloud_cover_octas` - Effective cloud cover measured in octas (0-8 scale).
- `elevation` - Ground surface elevation above sea level, in meters (m).

### 2. Air Quality Index (US AQI) & Atmospheric Trace Gases
- `air_quality:idx` - Overall aggregated US Air Quality Index (0-500 scale).
- `air_quality_pm2p5:idx` - AQI sub-index for Fine Particulate Matter ($PM_{2.5}$).
- `air_quality_pm10:idx` - AQI sub-index for Coarse Particulate Matter ($PM_{10}$).
- `air_quality_no2:idx` - AQI sub-index for Nitrogen Dioxide ($NO_2$).
- `aqi_us_co` - AQI sub-index for Carbon Monoxide ($CO$).
- `air_quality_o3:idx` - AQI sub-index for Ground-level Ozone ($O_3$).
- `air_quality_so2:idx` - AQI sub-index for Sulfur Dioxide ($SO_2$).
- `methane_ppb` - Atmospheric Methane concentration in parts per billion (ppb).
- `co2_ppm` - Atmospheric Carbon Dioxide concentration in parts per million (ppm).

### 3. Solar Radiation & Irradiance Profiles
- `solar_irradiance` - Clear-sky solar irradiance components:
 - **GHI (Global Horizontal Irradiance):** Total solar radiation received per unit area by a horizontal surface ($W/m^2$).
 - **DNI (Direct Normal Irradiance):** Solar radiation received per unit area by a surface held perpendicular to solar rays ($W/m^2$).
 - **DHI (Diffuse Horizontal Irradiance):** Solar radiation scattered by atmospheric molecules and aerosols ($W/m^2$).

---

## 💻 Request Example (Python)

```python
import requests

response = requests.post(
    'https://api.fortyguard.com/v1/env_params',
    headers={
        'api-key': 'YOUR_API_KEY',
        'Content-Type': 'application/json'
    },
    json={
        'latitude': 40.7128,
        'longitude': -74.0060,
        'temperature': 32.4,
        'date_time': {
            'start_date': '2024-07-15',
            'start_time': '14:00',
            'filter_type': 1
        },
        'analysis': [
            'heat_index_celsius',
            'apparent_temperature_celsius',
            'wet_bulb_temperature_celsius',
            'relative_humidity_percent',
            'air_quality:idx',
            'solar_irradiance'
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
  "message": "Environment Parameters Analysis Submitted Successfully",
  "data": {
    "activity_id": "f501e334-572b-40c4-8eb9-c9b679eff6ee"
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
    "activity_id": "UUID_STRING",
    "status": "Completed",
    "result": {
      "metadata": {
        "timezone": "TIMEZONE_STRING",
        "timezone_offset_hours": "NUMBER",
        "time_range": {
          "start": "YYYY-MM-DDTHH:MM:SS±HH:MM",
          "end": "YYYY-MM-DDTHH:MM:SS±HH:MM",
          "interval": "TIME_INTERVAL_STRING",
          "count": "INTEGER"
        },
        "timestamps": [
          "YYYY-MM-DDTHH:MM:SS±HH:MM"
        ]
      },
      "locations": [
        {
          "lat": "NUMBER",
          "lon": "NUMBER",
          "elevation": "NUMBER",
          "temperature": "NUMBER",
          "parameters": {
            "heat_index_celsius": ["NUMBER_OR_NULL"],
            "apparent_temperature_celsius": ["NUMBER_OR_NULL"],
            "relative_humidity_percent": ["NUMBER_OR_NULL"],
            "precipitation_mm": ["NUMBER_OR_NULL"],
            "cloud_cover_octas": ["NUMBER_OR_NULL"],
            "wet_bulb_temperature_celsius": ["NUMBER_OR_NULL"],
            "air_quality:idx": ["NUMBER_OR_NULL"],
            "air_quality_pm2p5:idx": ["NUMBER_OR_NULL"],
            "air_quality_pm10:idx": ["NUMBER_OR_NULL"],
            "air_quality_no2:idx": ["NUMBER_OR_NULL"],
            "aqi_us_co": ["NUMBER_OR_NULL"],
            "air_quality_o3:idx": ["NUMBER_OR_NULL"],
            "air_quality_so2:idx": ["NUMBER_OR_NULL"],
            "methane_ppb": ["NUMBER_OR_NULL"],
            "co2_ppm": ["NUMBER_OR_NULL"]
          },
          "solar_irradiance": {
            "clear_sky": {
              "ghi": "NUMBER",
              "dni": "NUMBER",
              "dhi": "NUMBER"
            },
            "description": "STRING_EXPLANATION_OF_SOLAR_OUTPUT"
          }
        }
      ]
    }
  }
}
```

### 📊 Result Schema & Handling Missing Data
Once the environmental parameters analysis activity has finished processing, the final response contains three main outputs:
• Time metadata (metadata) - timezone + the exact timestamps/time range the data corresponds to
• Location context (locations) - the latitude/longitude (and often elevation) that was analyzed
• Environmental outputs (parameters + solar_irradiance) - time-aligned arrays of weather/comfort, air-quality, gases, and solar irradiance metrics

Missing numeric values:
• New missing numeric environmental values are returned as JSON null
• Older stored responses may still contain legacy -999
• null means data was unavailable from the upstream provider
• Missing values must not be interpreted as zero
• Response arrays and live field names remain unchanged

This response is returned when the activity status is "Completed".

> [!IMPORTANT]
> **Handling Null / Missing Values:**
> - Missing numeric values are returned as JSON `null` (or legacy `-999` in older archives).
> - `null` indicates upstream telemetry unavailability; **never interpret null as zero**.
