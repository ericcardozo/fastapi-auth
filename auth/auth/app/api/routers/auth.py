from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from auth.domain.models import Credentials, Token
from auth.app.handlers import handle_login

from tests.unit.mock.context import Users

router = APIRouter()

@router.post('/login', response_model=Token)
async def login(form_data : OAuth2PasswordRequestForm = Depends())->Token:
    context = Users()
    try:
        credentials = Credentials(username=form_data.username, password=form_data.password)
        return handle_login(credentials, context)
    
    except AssertionError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))