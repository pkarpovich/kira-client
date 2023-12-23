from fastapi import APIRouter

spotify_router = APIRouter(prefix="/spotify")


@spotify_router.get("/auth")
def spotify_auth_endpoint():
    pass
