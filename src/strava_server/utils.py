from fastapi import HTTPException
import httpx

STRAVA_BASE_URL = "https://www.strava.com/api/v3"

# Helper function to extract bearer token from Authorization header
def extract_bearer_token(authorization: str) -> str:
    """Extract bearer token from Authorization header"""
    if not authorization:
        raise HTTPException(
            status_code=401, 
            detail="Authorization header is required"
        )
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, 
            detail="Authorization header must start with 'Bearer '"
        )
    
    token = authorization[7:]  # Remove "Bearer " prefix
    if not token:
        raise HTTPException(
            status_code=401, 
            detail="Bearer token is required"
        )
    
    return token

# Helper function to make authenticated requests to Strava
async def make_strava_request(
    method: str,
    endpoint: str,
    token: str,
    params: dict = None,
    data: dict = None,
    files: dict = None
):
    headers = {"authorization": f"Bearer {token}"}
    url = f"{STRAVA_BASE_URL}{endpoint}"
    async with httpx.AsyncClient() as client:
        if method.upper() == "GET":
            response = await client.get(url, headers=headers, params=params)
        elif method.upper() == "POST":
            response = await client.post(url, headers=headers, data=data, files=files)
        elif method.upper() == "PUT":
            response = await client.put(url, headers=headers, data=data)
        else:
            raise HTTPException(status_code=405, detail="Method not allowed")
    
    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response