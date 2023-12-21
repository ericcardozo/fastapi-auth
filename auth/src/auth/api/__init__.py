__version__ = '0.1.0'

from fastapi import FastAPI
from auth.api.routers import login

api = FastAPI()
api.include_router(login.router)

@api.get('/')
async def home() -> dict[str, str]:
    return { "version": __version__, }