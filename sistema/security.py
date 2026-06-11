from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from sistema.database import get_session
from sistema.settings import Settings
from sistema.ti_models import UsuariosTi

settings = Settings()  # type: ignore

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
password_hash = PasswordHash.recommended()

Token = Annotated[str, Depends(oauth2_scheme)]
T_session = Annotated[Session, Depends(get_session)]


def create_access_token(
    data: dict,
) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encode_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encode_jwt


def get_current_user_rh(token: Token, session: T_session):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        subject_email = payload.get("sub")

        if not subject_email:
            raise credentials_exception

    except DecodeError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise credentials_exception
    user = session.scalar(select(UsuariosTi).where(UsuariosTi.email_corp == subject_email))

    if not user:
        raise credentials_exception

    return user


def verify_password(plain_password, hashed_password):
    return password_hash.verify(hashed_password, plain_password)


def get_password_hash(password):
    return password_hash.hash(password)
