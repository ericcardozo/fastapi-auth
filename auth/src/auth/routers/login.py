from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post("/login")
async def login():
    return {"message": "login"}