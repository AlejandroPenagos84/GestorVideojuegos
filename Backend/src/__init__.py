from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.Tournament.routes import tournament_router
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"Server is starting...")
    await init_db()
    yield
    print(f"Server been stopped")

version = "v1"
version_prefix =f"/api/{version}"

app = FastAPI(
    title="VideoGames_Management",
    description="REST_API",
    version=version,
    lifespan=life_span
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tournament_router, prefix=f"{version_prefix}/tournaments", tags=["tournaments"])