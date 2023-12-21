from fastapi import FastAPI
from auth import __version__
from src.auth.routers import login

api = FastAPI()
api.include_router(login.router)

@api.get('/')
async def home() -> dict[str, str]:
    return { "version": __version__, }