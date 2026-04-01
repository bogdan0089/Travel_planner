from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from core.exceptions import TokenInvalidError
from database.unit_of_work import UnitOfWork
from models.models import User
from service.auth_service import AuthService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    auth = AuthService()
    user = await auth.get_current_user(token)
    if not user:
        raise TokenInvalidError()
    return user
