from fastapi import APIRouter, Path, Query, Header
from typing import Dict, Any
from datetime import datetime, timedelta
from statistics import mean
from ..utils import *

analysis_router = APIRouter()

@analysis_router.get("/analysis/activity-distribution", operation_id="getActivityDistribution")
async def activity_distribution(
    days: int = Query(90, description="Timeframe in days"),
    authorization: str = Header(..., description="Bearer token for authentication")
) -> Dict[str, Any]:
    """Distribution of activity types in last N days."""

    after = int((datetime.utcnow() - timedelta(days=days)).timestamp())
    token = extract_bearer_token(authorization)
    activities = await make_strava_request("GET", "/athlete/activities", token, params={"after": after})
    
    type_counts = {}
    for a in activities:
        type_counts[a["type"]] = type_counts.get(a["type"], 0) + 1
    
    total = sum(type_counts.values())
    distribution = {k: f"{(v/total)*100:.1f}%" for k,v in type_counts.items()}
    
    return {"days": days, "distribution": distribution}


@analysis_router.get("/analysis/pace-zones/{activity_id}", operation_id="getPaceZones")
async def pace_zones(
    activity_id: int = Path(..., description="The identifier of the activity"),
    authorization: str = Header(..., description="Bearer token for authentication")
) -> Dict[str, Any]:
    """Analyze time spent in pace/speed zones."""
    token = extract_bearer_token(authorization)
    streams = await make_strava_request("GET", f"/activities/{activity_id}/streams", token, {"keys": "velocity_smooth", "key_by_type": "true"})
    speeds = streams.get("velocity_smooth", {}).get("data", [])
    
    if not speeds:
        return {"activity_id": activity_id, "pace_zones": "No speed data"}
    
    # Convert m/s to min/km
    paces = [1000/s if s > 0 else None for s in speeds if s > 0]
    
    zones = {"Easy":0,"Tempo":0,"Interval":0,"Sprint":0}
    for p in paces:
        if p > 6: zones["Easy"] += 1
        elif 5 <= p <= 6: zones["Tempo"] += 1
        elif 4 <= p < 5: zones["Interval"] += 1
        else: zones["Sprint"] += 1
    
    total = sum(zones.values())
    pct = {k: f"{(v/total)*100:.1f}%" for k,v in zones.items()}
    return {"activity_id": activity_id, "pace_zones": pct}


@analysis_router.get("/analysis/elevation-trends", operation_id="getElevationTrends")
async def elevation_trends(
    weeks: int = Query(8, description="Number of recent weeks"),
    authorization: str = Header(..., description="Bearer token for authentication")
) -> Dict[str, Any]:
    """Weekly elevation gain trends."""
    after = int((datetime.utcnow() - timedelta(weeks=weeks)).timestamp())
    token = extract_bearer_token(authorization)
    activities = await make_strava_request("GET", "/athlete/activities", token, params={"after": after})
    
    weekly = {}
    for a in activities:
        week = datetime.strptime(a["start_date"], "%Y-%m-%dT%H:%M:%SZ").isocalendar()[1]
        weekly[week] = weekly.get(week, 0) + a.get("total_elevation_gain", 0)
    
    sorted_weeks = dict(sorted(weekly.items()))
    trend = "increasing" if list(sorted_weeks.values())[-1] > mean(list(sorted_weeks.values())[:-1]) else "stable/decreasing"
    
    return {"weekly_elevation_gain": sorted_weeks, "trend": trend}
