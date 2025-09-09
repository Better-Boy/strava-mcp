from enum import Enum
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class SummaryAthlete(BaseModel):
    id: int
    resource_state: int
    firstname: Optional[str] = None
    lastname: Optional[str] = None

class DetailedAthlete(BaseModel):
    id: int
    username: Optional[str] = None
    resource_state: int
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    sex: Optional[str] = None
    premium: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    badge_type_id: Optional[int] = None
    profile_medium: Optional[str] = None
    profile: Optional[str] = None
    friend: Optional[str] = None
    follower: Optional[str] = None
    follower_count: Optional[int] = None
    friend_count: Optional[int] = None
    mutual_friend_count: Optional[int] = None
    athlete_type: Optional[int] = None
    date_preference: Optional[str] = None
    measurement_preference: Optional[str] = None
    clubs: Optional[List[dict]] = []
    ftp: Optional[int] = None
    weight: Optional[float] = None
    bikes: Optional[List[dict]] = []
    shoes: Optional[List[dict]] = []

class ActivityStats(BaseModel):
    recent_ride_totals: Optional[dict] = None
    recent_run_totals: Optional[dict] = None
    ytd_ride_totals: Optional[dict] = None
    ytd_run_totals: Optional[dict] = None
    all_ride_totals: Optional[dict] = None
    all_run_totals: Optional[dict] = None

class DetailedSegment(BaseModel):
    id: int
    resource_state: int
    name: str
    activity_type: str
    distance: float
    average_grade: float
    maximum_grade: float
    elevation_high: float
    elevation_low: float
    start_latlng: List[float]
    end_latlng: List[float]
    climb_category: int
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    private: bool
    hazardous: bool
    starred: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    total_elevation_gain: Optional[float] = None
    map: Optional[dict] = None
    effort_count: Optional[int] = None
    athlete_count: Optional[int] = None
    star_count: Optional[int] = None
    athlete_segment_stats: Optional[dict] = None

class SummarySegment(BaseModel):
    id: int
    resource_state: int
    name: str
    activity_type: str
    distance: float
    average_grade: float
    maximum_grade: float
    elevation_high: float
    elevation_low: float
    start_latlng: List[float]
    end_latlng: List[float]
    climb_category: int
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    private: bool
    hazardous: bool
    starred: bool

class DetailedActivity(BaseModel):
    id: int
    resource_state: int
    external_id: Optional[str] = None
    upload_id: Optional[int] = None
    athlete: SummaryAthlete
    name: str
    distance: float
    moving_time: int
    elapsed_time: int
    total_elevation_gain: float
    type: str
    sport_type: str
    start_date: datetime
    start_date_local: datetime
    timezone: str
    utc_offset: int
    start_latlng: Optional[List[float]] = None
    end_latlng: Optional[List[float]] = None
    location_city: Optional[str] = None
    location_state: Optional[str] = None
    location_country: Optional[str] = None
    achievement_count: int
    kudos_count: int
    comment_count: int
    athlete_count: int
    photo_count: int
    map: Optional[dict] = None
    trainer: bool
    commute: bool
    manual: bool
    private: bool
    flagged: bool
    gear_id: Optional[str] = None
    from_accepted_tag: Optional[bool] = None
    average_speed: float
    max_speed: float
    average_cadence: Optional[float] = None
    average_temp: Optional[int] = None
    average_watts: Optional[float] = None
    weighted_average_watts: Optional[int] = None
    kilojoules: Optional[float] = None
    device_watts: Optional[bool] = None
    has_heartrate: bool
    average_heartrate: Optional[float] = None
    max_heartrate: Optional[int] = None
    max_watts: Optional[int] = None
    elev_high: Optional[float] = None
    elev_low: Optional[float] = None
    pr_count: int
    total_photo_count: int
    has_kudoed: bool
    workout_type: Optional[int] = None
    suffer_score: Optional[int] = None
    description: Optional[str] = None
    calories: Optional[float] = None
    segment_efforts: Optional[List[dict]] = []
    splits_metric: Optional[List[dict]] = []
    laps: Optional[List[dict]] = []
    gear: Optional[dict] = None
    partner_brand_tag: Optional[str] = None
    photos: Optional[dict] = None
    highlighted_kudosers: Optional[List[dict]] = []
    hide_from_home: Optional[bool] = None
    device_name: Optional[str] = None
    embed_token: Optional[str] = None
    segment_leaderboard_opt_out: Optional[bool] = None
    leaderboard_opt_out: Optional[bool] = None

class SummaryActivity(BaseModel):
    id: int
    resource_state: int
    external_id: Optional[str] = None
    upload_id: Optional[int] = None
    athlete: SummaryAthlete
    name: str
    distance: float
    moving_time: int
    elapsed_time: int
    total_elevation_gain: float
    type: str
    sport_type: str
    workout_type: Optional[int] = None
    start_date: datetime
    start_date_local: datetime
    timezone: str
    utc_offset: int
    start_latlng: Optional[List[float]] = None
    end_latlng: Optional[List[float]] = None
    location_city: Optional[str] = None
    location_state: Optional[str] = None
    location_country: Optional[str] = None
    achievement_count: int
    kudos_count: int
    comment_count: int
    athlete_count: int
    photo_count: int
    map: Optional[dict] = None
    trainer: bool
    commute: bool
    manual: bool
    private: bool
    flagged: bool
    gear_id: Optional[str] = None
    from_accepted_tag: Optional[bool] = None
    average_speed: float
    max_speed: float
    average_cadence: Optional[float] = None
    average_watts: Optional[float] = None
    weighted_average_watts: Optional[int] = None
    kilojoules: Optional[float] = None
    device_watts: Optional[bool] = None
    has_heartrate: bool
    average_heartrate: Optional[float] = None
    max_heartrate: Optional[int] = None
    max_watts: Optional[int] = None
    pr_count: int
    total_photo_count: int
    has_kudoed: bool
    suffer_score: Optional[int] = None

class DetailedClub(BaseModel):
    id: int
    resource_state: int
    name: str
    profile_medium: Optional[str] = None
    profile: Optional[str] = None
    cover_photo: Optional[str] = None
    cover_photo_small: Optional[str] = None
    sport_type: str
    activity_types: List[str]
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    private: bool
    member_count: int
    featured: bool
    verified: bool
    url: str
    membership: Optional[str] = None
    admin: Optional[bool] = None
    owner: Optional[bool] = None
    description: Optional[str] = None
    club_type: Optional[str] = None
    post_count: Optional[int] = None
    owner_id: Optional[int] = None
    following_count: Optional[int] = None

class SummaryClub(BaseModel):
    id: int
    resource_state: int
    name: str
    profile_medium: Optional[str] = None
    profile: Optional[str] = None
    cover_photo: Optional[str] = None
    cover_photo_small: Optional[str] = None
    sport_type: str
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    private: bool
    member_count: int
    featured: bool
    verified: bool
    url: str

class StreamTypeEnum(str, Enum):
    time = "time"
    distance = "distance"
    latlng = "latlng"
    altitude = "altitude"
    velocity_smooth = "velocity_smooth"
    heartrate = "heartrate"
    cadence = "cadence"
    watts = "watts"
    temp = "temp"
    moving = "moving"
    grade_smooth = "grade_smooth"