from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from .api import router

app = FastAPI(
    title="Strava API v3",
    description="FastAPI implementation of Strava API v3",
    version="3.0.0"
)

app.include_router(router=router)

mcp = FastApiMCP(app, 
                 name="MCP server for Strava API",
                 description="")

mcp.mount_http()

mcp.run()

# def run():
    
#     import uvicorn
#     uvicorn.run(app=app, host="0.0.0.0", port=8000)

# if __name__ == "__main__":
#     run()