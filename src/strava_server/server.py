from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import FastMCP
from api import router

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    yield
    pass

@asynccontextmanager
async def combined_lifespan(fastapi_app: FastAPI):
    async with app_lifespan(fastapi_app):
        async with mcp_app.lifespan(fastapi_app):
            yield

app = FastAPI(
    title="Strava API v3",
    description="FastAPI implementation of Strava API v3",
    version="3.0.0",
    lifespan=combined_lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router)

server = FastMCP.from_fastapi(app, 
                 name="MCP server for Strava API")

mcp_app = server.http_app(path='/mcp')

def create_server():
    global server
    return server

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)