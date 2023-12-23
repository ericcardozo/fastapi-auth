from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/login')
async def login(form_data : OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    if form_data.username != 'johndoe' or form_data.password != 'secret':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    return { 'access_token' : 'johndoe' }
