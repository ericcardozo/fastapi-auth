from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth.app.models import Token
from auth.app.handlers import handle_login

from tests.unit.mock.context import FakeContext

router = APIRouter()

@router.post('/login', response_model=Token)
async def login(form_data : OAuth2PasswordRequestForm = Depends())->Token:
    context = FakeContext()
    try:
        return handle_login(form_data.username, form_data.password, context)
    
    except AssertionError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))
    