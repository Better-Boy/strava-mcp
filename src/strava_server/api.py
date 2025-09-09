from fastapi import HTTPException, Query, Path, Header, APIRouter

from .models import *
from .utils import *

router = APIRouter()

# Athletes Endpoints
@router.get("/athletes/{athlete_id}/stats", response_model=ActivityStats)
async def get_athlete_stats(
    athlete_id: int = Path(..., description="The identifier of the athlete"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns the activity stats of an athlete."""
    token = extract_bearer_token(authorization)
    response = await make_strava_request("GET", f"/athletes/{athlete_id}/stats", token)
    return response.json()

@router.get("/athlete", response_model=DetailedAthlete)
async def get_authenticated_athlete(
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns the currently authenticated athlete."""
    token = extract_bearer_token(authorization)
    response = await make_strava_request("GET", "/athlete", token)
    return response.json()

@router.put("/athlete", response_model=DetailedAthlete)
async def update_authenticated_athlete(
    weight: float = Query(..., description="The weight of the athlete in kilograms"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Update the currently authenticated athlete."""
    token = extract_bearer_token(authorization)
    data = {"weight": weight}
    response = await make_strava_request("PUT", "/athlete", token, data=data)
    return response.json()

@router.get("/athlete/zones")
async def get_authenticated_athlete_zones(
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns the authenticated athlete's heart rate and power zones."""
    token = extract_bearer_token(authorization)
    response = await make_strava_request("GET", "/athlete/zones", token)
    return response.json()

# Segments Endpoints
@router.get("/segments/{segment_id}", response_model=DetailedSegment)
async def get_segment_by_id(
    segment_id: int = Path(..., description="The identifier of the segment"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns the specified segment."""
    token = extract_bearer_token(authorization)
    response = await make_strava_request("GET", f"/segments/{segment_id}", token)
    return response.json()

@router.get("/segments/starred", response_model=List[SummarySegment])
async def get_starred_segments(
    page: Optional[int] = Query(1, description="Page number"),
    per_page: Optional[int] = Query(30, description="Number of items per page"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """List of the authenticated athlete's starred segments."""
    token = extract_bearer_token(authorization)
    params = {"page": page, "per_page": per_page}
    response = await make_strava_request("GET", "/segments/starred", token, params=params)
    return response.json()

@router.get("/segments/explore")
async def explore_segments(
    bounds: List[float] = Query(..., description="Rectangular boundary for search"),
    activity_type: Optional[str] = Query(None, description="Desired activity type"),
    min_cat: Optional[int] = Query(None, ge=0, le=5, description="Minimum climbing category"),
    max_cat: Optional[int] = Query(None, ge=0, le=5, description="Maximum climbing category"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns the top 10 segments matching a specified query."""
    token = extract_bearer_token(authorization)
    params = {
        "bounds": ",".join(map(str, bounds)),
        "activity_type": activity_type,
        "min_cat": min_cat,
        "max_cat": max_cat
    }
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}
    response = await make_strava_request("GET", "/segments/explore", token, params=params)
    return response.json()

# Segment Efforts Endpoints
@router.get("/segment_efforts")
async def get_segment_efforts(
    segment_id: int = Query(..., description="The identifier of the segment"),
    start_date_local: Optional[datetime] = Query(None, description="Start date filter"),
    end_date_local: Optional[datetime] = Query(None, description="End date filter"),
    per_page: Optional[int] = Query(30, description="Number of items per page"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns segment efforts for a given segment."""
    token = extract_bearer_token(authorization)
    params = {
        "segment_id": segment_id,
        "start_date_local": start_date_local.isoformat() if start_date_local else None,
        "end_date_local": end_date_local.isoformat() if end_date_local else None,
        "per_page": per_page
    }
    params = {k: v for k, v in params.items() if v is not None}
    response = await make_strava_request("GET", "/segment_efforts", token, params=params)
    return response.json()

@router.get("/segment_efforts/{effort_id}")
async def get_segment_effort_by_id(
    effort_id: int = Path(..., description="The identifier of the segment effort"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns a segment effort from an activity."""
    token = extract_bearer_token(authorization)
    response = await make_strava_request("GET", f"/segment_efforts/{effort_id}", token)
    return response.json()

@router.get("/activities/{activity_id}", response_model=DetailedActivity)
async def get_activity_by_id(
    activity_id: int = Path(..., description="The identifier of the activity"),
    include_all_efforts: Optional[bool] = Query(False, description="Include all segment efforts"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns the given activity."""
    print(authorization)
    token = extract_bearer_token(authorization)
    params = {"include_all_efforts": include_all_efforts} if include_all_efforts else {}
    response = await make_strava_request("GET", f"/activities/{activity_id}", token, params=params)
    return response.json()

@router.get("/athlete/activities", response_model=List[SummaryActivity])
async def get_athlete_activities(
    before: Optional[int] = Query(None, description="Filter activities before this timestamp"),
    after: Optional[int] = Query(None, description="Filter activities after this timestamp"),
    page: Optional[int] = Query(1, description="Page number"),
    per_page: Optional[int] = Query(30, description="Number of items per page"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns the activities of the authenticated athlete."""
    token = extract_bearer_token(authorization)
    params = {"before": before, "after": after, "page": page, "per_page": per_page}
    params = {k: v for k, v in params.items() if v is not None}
    response = await make_strava_request("GET", "/athlete/activities", token, params=params)
    return response.json()

@router.get("/activities/{activity_id}/laps")
async def get_activity_laps(
    activity_id: int = Path(..., description="The identifier of the activity"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns the laps of an activity."""
    token = extract_bearer_token(authorization)
    response = await make_strava_request("GET", f"/activities/{activity_id}/laps", token)
    return response.json()

@router.get("/activities/{activity_id}/zones")
async def get_activity_zones(
    activity_id: int = Path(..., description="The identifier of the activity"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns the zones of a given activity."""
    token = extract_bearer_token(authorization)
    response = await make_strava_request("GET", f"/activities/{activity_id}/zones", token)
    return response.json()

@router.get("/activities/{activity_id}/comments")
async def get_activity_comments(
    activity_id: int = Path(..., description="The identifier of the activity"),
    page: Optional[int] = Query(None, description="Page number (deprecated)"),
    per_page: Optional[int] = Query(30, description="Items per page (deprecated)"),
    page_size: Optional[int] = Query(30, description="Number of items per page"),
    after_cursor: Optional[str] = Query(None, description="Cursor for pagination"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns the comments on the given activity."""
    token = extract_bearer_token(authorization)
    params = {
        "page": page,
        "per_page": per_page,
        "page_size": page_size,
        "after_cursor": after_cursor
    }
    params = {k: v for k, v in params.items() if v is not None}
    response = await make_strava_request("GET", f"/activities/{activity_id}/comments", token, params=params)
    return response.json()

@router.get("/activities/{activity_id}/kudos")
async def get_activity_kudos(
    activity_id: int = Path(..., description="The identifier of the activity"),
    page: Optional[int] = Query(1, description="Page number"),
    per_page: Optional[int] = Query(30, description="Number of items per page"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns the athletes who kudoed an activity."""
    token = extract_bearer_token(authorization)
    params = {"page": page, "per_page": per_page}
    response = await make_strava_request("GET", f"/activities/{activity_id}/kudos", token, params=params)
    return response.json()

# Clubs Endpoints
@router.get("/clubs/{club_id}", response_model=DetailedClub)
async def get_club_by_id(
    club_id: int = Path(..., description="The identifier of the club"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns a given club."""
    token = extract_bearer_token(authorization)
    response = await make_strava_request("GET", f"/clubs/{club_id}", token)
    return response.json()

@router.get("/clubs/{club_id}/members")
async def get_club_members(
    club_id: int = Path(..., description="The identifier of the club"),
    page: Optional[int] = Query(1, description="Page number"),
    per_page: Optional[int] = Query(30, description="Number of items per page"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns club members."""
    token = extract_bearer_token(authorization)
    params = {"page": page, "per_page": per_page}
    response = await make_strava_request("GET", f"/clubs/{club_id}/members", token, params=params)
    return response.json()

@router.get("/clubs/{club_id}/admins")
async def get_club_admins(
    club_id: int = Path(..., description="The identifier of the club"),
    page: Optional[int] = Query(1, description="Page number"),
    per_page: Optional[int] = Query(30, description="Number of items per page"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns club administrators."""
    token = extract_bearer_token(authorization)
    params = {"page": page, "per_page": per_page}
    response = await make_strava_request("GET", f"/clubs/{club_id}/admins", token, params=params)
    return response.json()

@router.get("/clubs/{club_id}/activities")
async def get_club_activities(
    club_id: int = Path(..., description="The identifier of the club"),
    page: Optional[int] = Query(1, description="Page number"),
    per_page: Optional[int] = Query(30, description="Number of items per page"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns recent activities from club members."""
    token = extract_bearer_token(authorization)
    params = {"page": page, "per_page": per_page}
    response = await make_strava_request("GET", f"/clubs/{club_id}/activities", token, params=params)
    return response.json()

@router.get("/athlete/clubs", response_model=List[SummaryClub])
async def get_athlete_clubs(
    page: Optional[int] = Query(1, description="Page number"),
    per_page: Optional[int] = Query(30, description="Number of items per page"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns clubs the authenticated athlete belongs to."""
    token = extract_bearer_token(authorization)
    params = {"page": page, "per_page": per_page}
    response = await make_strava_request("GET", "/athlete/clubs", token, params=params)
    return response.json()

# Gear Endpoints
@router.get("/gear/{gear_id}")
async def get_gear_by_id(
    gear_id: str = Path(..., description="The identifier of the gear"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns equipment using its identifier."""
    token = extract_bearer_token(authorization)
    response = await make_strava_request("GET", f"/gear/{gear_id}", token)
    return response.json()

# Routes Endpoints
@router.get("/routes/{route_id}")
async def get_route_by_id(
    route_id: int = Path(..., description="The identifier of the route"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns a route using its identifier."""
    token = extract_bearer_token(authorization)
    response = await make_strava_request("GET", f"/routes/{route_id}", token)
    return response.json()

@router.get("/athletes/{athlete_id}/routes")
async def get_athlete_routes(
    athlete_id: int = Path(..., description="The identifier of the athlete"),
    page: Optional[int] = Query(1, description="Page number"),
    per_page: Optional[int] = Query(30, description="Number of items per page"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns routes created by the athlete."""
    token = extract_bearer_token(authorization)
    params = {"page": page, "per_page": per_page}
    response = await make_strava_request("GET", f"/athletes/{athlete_id}/routes", token, params=params)
    return response.json()

@router.get("/routes/{route_id}/export_gpx")
async def get_route_as_gpx(
    route_id: int = Path(..., description="The identifier of the route"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns a GPX file of the route."""
    token = extract_bearer_token(authorization)
    response = await make_strava_request("GET", f"/routes/{route_id}/export_gpx", token)
    return Response(content=response.content, media_type="application/gpx+xml")

@router.get("/routes/{route_id}/export_tcx")
async def get_route_as_tcx(
    route_id: int = Path(..., description="The identifier of the route"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns a TCX file of the route."""
    token = extract_bearer_token(authorization)
    response = await make_strava_request("GET", f"/routes/{route_id}/export_tcx", token)
    return Response(content=response.content, media_type="application/tcx+xml")

@router.get("/uploads/{upload_id}")
async def get_upload_by_id(
    upload_id: int = Path(..., description="The identifier of the upload"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns an upload for a given identifier."""
    token = extract_bearer_token(authorization)
    response = await make_strava_request("GET", f"/uploads/{upload_id}", token)
    return response.json()

# Streams Endpoints
@router.get("/activities/{activity_id}/streams")
async def get_activity_streams(
    activity_id: int = Path(..., description="The identifier of the activity"),
    keys: List[StreamTypeEnum] = Query(..., description="Desired stream types"),
    key_by_type: bool = Query(True, description="Must be true"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns the given activity's streams."""
    token = extract_bearer_token(authorization)
    params = {
        "keys": ",".join(keys),
        "key_by_type": key_by_type
    }
    response = await make_strava_request("GET", f"/activities/{activity_id}/streams", token, params=params)
    return response.json()

@router.get("/segment_efforts/{effort_id}/streams")
async def get_segment_effort_streams(
    effort_id: int = Path(..., description="The identifier of the segment effort"),
    keys: List[StreamTypeEnum] = Query(..., description="The types of streams to return"),
    key_by_type: bool = Query(True, description="Must be true"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns streams for a segment effort."""
    token = extract_bearer_token(authorization)
    params = {
        "keys": ",".join(keys),
        "key_by_type": key_by_type
    }
    response = await make_strava_request("GET", f"/segment_efforts/{effort_id}/streams", token, params=params)
    return response.json()

@router.get("/segments/{segment_id}/streams")
async def get_segment_streams(
    segment_id: int = Path(..., description="The identifier of the segment"),
    keys: List[str] = Query(..., description="The types of streams to return"),
    key_by_type: bool = Query(True, description="Must be true"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns the given segment's streams."""
    token = extract_bearer_token(authorization)
    # Validate keys for segments (only distance, latlng, altitude allowed)
    valid_keys = ["distance", "latlng", "altitude"]
    for key in keys:
        if key not in valid_keys:
            raise HTTPException(status_code=400, detail=f"Invalid key '{key}' for segment streams. Valid keys: {valid_keys}")
    
    params = {
        "keys": ",".join(keys),
        "key_by_type": key_by_type
    }
    response = await make_strava_request("GET", f"/segments/{segment_id}/streams", token, params=params)
    return response.json()

@router.get("/routes/{route_id}/streams")
async def get_route_streams(
    route_id: int = Path(..., description="The identifier of the route"),
    authorization: str = Header(..., description="Bearer token for authentication")
):
    """Returns the given route's streams."""
    token = extract_bearer_token(authorization)
    response = await make_strava_request("GET", f"/routes/{route_id}/streams", token)
    return response.json()

# Health check endpoint
@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Strava API FastAPI Implementation"}

# Root endpoint with API information
@router.get("/")
async def root():
    """API information and documentation."""
    return {
        "title": "Strava API v3 FastAPI Implementation",
        "description": "A FastAPI implementation of the Strava API v3 endpoints",
        "version": "3.0.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "base_url": STRAVA_BASE_URL,
        "auth_note": "All endpoints require Bearer token in Authorization header (Authorization: Bearer <token>)"
    }