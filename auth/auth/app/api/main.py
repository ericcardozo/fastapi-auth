from fastapi import FastAPI
from auth import __version__
from auth.app.api.routers import auth

api = FastAPI()
api.include_router(auth.router, prefix='/auth')

@api.get('/')
async def version() -> dict[str, str]:
    return { "version": __version__, }