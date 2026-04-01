from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models.models import User
from schemas.schemas_auth import TokenOut, UserOut, UserRegister
from service.auth_service import AuthService
from utils.dependencies import get_current_user


router = APIRouter(prefix="/auth")


@router.post("/register", response_model=UserOut, status_code=201)
async def register(data: UserRegister):
    auth = AuthService()
    user = await auth.register(data.username, data.email, data.password)
    return user

@router.post("/login", response_model=TokenOut)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    auth = AuthService()
    token = await auth.login(form.username, form.password)
    return TokenOut(access_token=token)

@router.get("/me", response_model=UserOut)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
