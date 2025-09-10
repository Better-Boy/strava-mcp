## Endpoint Details

All endpoints require an **Authorization header** with a valid bearer token:

```
Authorization: Bearer <access_token>
```

OAuth2 scopes determine which endpoints a token can access. See [Strava API Scopes](https://developers.strava.com/docs/authentication/#detailsaboutrequestingaccess) for more info.

---

## 📊 Analytics Endpoints

### `GET /analysis/activity-distribution`

* **Description**: Distribution of activity types in the last N days.
* **Query Params**:

  * `days` (int, default=90) → Timeframe in days.
* **Headers**:

  * `Authorization` → Bearer token.
* **Response**:

```json
{
  "days": 30,
  "distribution": {
    "Run": "60.0%",
    "Ride": "30.0%",
    "Swim": "10.0%"
  }
}
```

* **Scope**: `activity:read_all`

---

### `GET /analysis/pace-zones/{activity_id}`

* **Description**: Analyze time spent in pace/speed zones for a given activity.
* **Path Params**:

  * `activity_id` (int) → The Strava activity ID.
* **Headers**:

  * `Authorization` → Bearer token.
* **Response**:

```json
{
  "activity_id": 123456789,
  "pace_zones": {
    "Easy": "50.0%",
    "Tempo": "25.0%",
    "Interval": "15.0%",
    "Sprint": "10.0%"
  }
}
```

* **Notes**:

  * Converts Strava speed stream (`m/s`) into **pace (min/km)**.
  * Zones:

    * Easy > 6:00 min/km
    * Tempo 5:00–6:00 min/km
    * Interval 4:00–5:00 min/km
    * Sprint < 4:00 min/km
* **Scope**: `activity:read_all`

---

### `GET /analysis/elevation-trends`

* **Description**: Weekly elevation gain trends over the last N weeks.
* **Query Params**:

  * `weeks` (int, default=8) → Number of recent weeks.
* **Headers**:

  * `Authorization` → Bearer token.
* **Response**:

```json
{
  "weekly_elevation_gain": {
    "35": 1234,
    "36": 1850,
    "37": 1600
  },
  "trend": "increasing"
}
```

* **Notes**:

  * Groups activities by **ISO week number**.
  * Computes trend:

    * `"increasing"` if the most recent week > average of prior weeks.
    * `"stable/decreasing"` otherwise.
* **Scope**: `activity:read_all`

---

## 📊 Insights Endpoints

### `GET /insights/performance-efficiency/{activity_id}`

* **Description**: Evaluates HR-to-speed efficiency within a single activity.
* **Path Params**:

  * `activity_id` (int) → The Strava activity ID.
* **Headers**:

  * `Authorization` → Bearer token.
* **Response**:

```json
{
  "insight": "Efficiency score 0.45 (km/h per bpm). Higher = better.",
  "avg_hr": 152.3,
  "avg_speed_kmh": 8.5
}
```

* **Notes**:

  * Fetches **heart rate** and **velocity streams**.
  * Converts average speed → km/h.
  * Computes efficiency = `avg_speed / avg_hr`.
* **Scope**: `activity:read_all`

---

### `GET /insights/recovery-risk`

* **Description**: Compares **7-day vs 28-day training load** to highlight recovery and overtraining risks.
* **Headers**:

  * `Authorization` → Bearer token.
* **Response**:

```json
{
  "load_7_days_km": 55.3,
  "load_28_days_km": 180.7,
  "risk": "overload risk"
}
```

* **Risk Levels**:

  * `"balanced"` → Training load is consistent.
  * `"overload risk"` → Last 7 days > 130% of typical weekly average.
  * `"low load (possible detraining)"` → Last 7 days < 70% of typical weekly average.
* **Scope**: `activity:read_all`

---

## 🏃 Athlete Endpoints

### `GET /athletes/{athlete_id}/stats`

**Description**: Returns stats for a specific athlete (recent, year-to-date, all-time).
**Scope**: `profile:read_all`

---

### `GET /athlete`

**Description**: Returns the currently authenticated athlete.
**Scope**: `profile:read_all`

---

### `PUT /athlete`

**Description**: Update the authenticated athlete’s profile (currently only weight).
**Scope**: `profile:write`

---

### `GET /athlete/zones`

**Description**: Returns authenticated athlete’s HR and power zones.
**Scope**: `profile:read_all`

---

## 📍 Segment Endpoints

### `GET /segments/{segment_id}`

**Description**: Returns details for a given segment.
**Scope**: `read_all`

---

### `GET /segments/starred`

**Description**: Returns authenticated athlete’s starred segments.
**Scope**: `read_all`

---

### `GET /segments/explore`

**Description**: Explore segments within a bounding box and filters.
**Scope**: `read`

---

## ⏱️ Segment Efforts Endpoints

### `GET /segment_efforts`

**Description**: Returns segment efforts for a given segment.
**Scope**: `activity:read_all`

---

### `GET /segment_efforts/{effort_id}`

**Description**: Returns a specific segment effort.
**Scope**: `activity:read_all`

---

## 🏃 Activity Endpoints

### `GET /activities/{activity_id}`

**Description**: Returns a detailed activity.
**Scope**: `activity:read_all`

---

### `GET /athlete/activities`

**Description**: Returns a list of authenticated athlete’s activities.
**Scope**: `activity:read_all`

---

### `GET /activities/{activity_id}/laps`

**Description**: Returns laps of an activity.
**Scope**: `activity:read_all`

---

### `GET /activities/{activity_id}/zones`

**Description**: Returns HR/power zones for an activity.
**Scope**: `activity:read_all`

---

### `GET /activities/{activity_id}/comments`

**Description**: Returns comments on an activity (paginated).
**Scope**: `activity:read_all`

---

### `GET /activities/{activity_id}/kudos`

**Description**: Returns athletes who gave kudos.
**Scope**: `activity:read_all`

---

## 👥 Clubs Endpoints

### `GET /clubs/{club_id}`

**Description**: Returns a club by ID.
**Scope**: `read`

---

### `GET /clubs/{club_id}/members`

**Description**: Returns club members (paginated).
**Scope**: `read`

---

### `GET /clubs/{club_id}/activities`

**Description**: Returns recent club activities.
**Scope**: `read`

---

### `GET /athlete/clubs`

**Description**: Returns clubs the authenticated athlete belongs to.
**Scope**: `read`

---

## 👟 Gear Endpoints

### `GET /gear/{gear_id}`

**Description**: Returns gear/equipment by ID.
**Scope**: `read_all`

---

## 🗺️ Routes Endpoints

### `GET /routes/{route_id}`

**Description**: Returns details of a route.
**Scope**: `read_all`

---

### `GET /athletes/{athlete_id}/routes`

**Description**: Returns athlete’s created routes.
**Scope**: `read_all`

---

## 📊 Streams Endpoints

### `GET /activities/{activity_id}/streams`

**Description**: Returns activity streams (e.g. lat/lng, HR, cadence).
**Scope**: `activity:read_all`

---

### `GET /segment_efforts/{effort_id}/streams`

**Description**: Returns streams for a segment effort.
**Scope**: `activity:read_all`

---

### `GET /segments/{segment_id}/streams`

**Description**: Returns streams for a segment (distance, latlng, altitude only).
**Scope**: `read_all`

---

### `GET /routes/{route_id}/streams`

**Description**: Returns streams for a route.
**Scope**: `read_all`

---

## 🩺 Utility Endpoints

### `GET /health`

**Description**: Returns API health status.
**Scope**: None (public).

---

### `GET /`

**Description**: Returns API info, version, docs URL, and base Strava API URL.
**Scope**: None (public).

---

⚠️ **Note on Scopes**:

* `read`: Basic read (public data).
* `read_all`: Access to private segments, routes, clubs, gear.
* `profile:read_all`: Access to non-public athlete data.
* `activity:read_all`: Access to all activity details, including private.
* `profile:write`: Modify athlete profile.

