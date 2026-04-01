from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from core.cfg import settings
from core.exceptions import InvalidCredentialsError, TokenInvalidError, UserAlreadyExistsError
from database.unit_of_work import UnitOfWork
from models.models import User
from utils.hash import hash_password, verify_password


class AuthService:
    def create_access_token(self, subject: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return jwt.encode({"sub": subject, "exp": expire}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def decode_token(self, token: str) -> str | None:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload.get("sub")
        except JWTError:
            return None

    async def register(self, username: str, email: str, password: str) -> User:
        async with UnitOfWork() as uow:
            if await uow.user.get_by_username(username):
                raise UserAlreadyExistsError()
            if await uow.user.get_by_email(email):
                raise UserAlreadyExistsError()
            user = await uow.user.create_user(username, email, hash_password(password))
        return user

    async def login(self, username: str, password: str) -> str:
        async with UnitOfWork() as uow:
            user = await uow.user.get_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()
        return self.create_access_token(str(user.id))

    async def get_current_user(self, token: str) -> User | None:
        subject = self.decode_token(token)
        if not subject:
            raise TokenInvalidError()
        async with UnitOfWork() as uow:
            user = await uow.user.get_user(int(subject))
        return user
