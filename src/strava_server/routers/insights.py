from fastapi import APIRouter, Header, Path
from typing import Dict, Any
from datetime import datetime, timedelta
from statistics import mean
from ..utils import *

insights_router = APIRouter()

@insights_router.get("/insights/performance-efficiency/{activity_id}", operation_id="getPerformanceEfficiency")
async def performance_efficiency(
    activity_id: int = Path(..., description="The identifier of the activity"),
    authorization: str = Header(..., description="Bearer token for authentication")
) -> Dict[str, Any]:
    """Check if HR efficiency improved within an activity."""
    token = extract_bearer_token(authorization)

    streams = await make_strava_request("GET", f"/activities/{activity_id}/streams", token, {"keys":"heartrate,velocity_smooth","key_by_type":"true"})
    
    hr = streams.get("heartrate", {}).get("data", [])
    spd = streams.get("velocity_smooth", {}).get("data", [])
    
    if not hr or not spd:
        return {"insight": "No HR or speed data"}
    
    avg_hr = mean(hr)
    avg_speed = mean(spd) * 3.6  # km/h
    
    efficiency = avg_speed / avg_hr
    return {"insight": f"Efficiency score {efficiency:.2f} (km/h per bpm). Higher = better.", "avg_hr": avg_hr, "avg_speed_kmh": avg_speed}


@insights_router.get("/insights/recovery-risk", operation_id="getRecoveryRisk")
async def recovery_risk(
    authorization: str = Header(..., description="Bearer token for authentication")
) -> Dict[str, Any]:
    """Compare 7-day vs 28-day load to detect overtraining."""
    after_28 = int((datetime.utcnow() - timedelta(days=28)).timestamp())
    after_7 = int((datetime.utcnow() - timedelta(days=7)).timestamp())
    token = extract_bearer_token(authorization)
    all_28 = await make_strava_request("GET", "/athlete/activities", token, params={"after": after_28})
    all_7 = [a for a in all_28 if datetime.strptime(a["start_date"], "%Y-%m-%dT%H:%M:%SZ").timestamp() >= after_7]
    
    load_28 = sum([a["distance"] for a in all_28])
    load_7 = sum([a["distance"] for a in all_7])
    
    risk = "balanced"
    if load_7 > (load_28/4)*1.3:
        risk = "overload risk"
    elif load_7 < (load_28/4)*0.7:
        risk = "low load (possible detraining)"
    
    return {"load_7_days_km": load_7/1000, "load_28_days_km": load_28/1000, "risk": risk}
