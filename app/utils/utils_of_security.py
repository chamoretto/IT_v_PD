from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from pony.orm import db_session

from app.settings.config import cfg
from app.utils.pydantic_security import TokenData, HumanInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = cfg.get('db', "hash_algorithm")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def generate_security(oauth2_scheme, secret_key, entity,
                      getter_human=None,
                      credentials_exception=HTTPException(
                          status_code=status.HTTP_401_UNAUTHORIZED,
                          detail="Could not validate credentials",
                          headers={"WWW-Authenticate": "Bearer"},
                      )):
    """
        Генерирукм функции безопасности для абстрактного уровня доступа

    :param oauth2_scheme:
    :param secret_key:
    :param entity:
    :param getter_human:
    :param credentials_exception:
    :return:
    """

    if getter_human is None:
        @db_session
        def getter_human(username: str):
            if entity.exists(username=username):
                human_db = entity.get(username=username)
                return HumanInDB.from_orm(human_db)

    def authenticate_human(username: str, password: str):

        """ Аунтидификация пользователя"""

        human = getter_human(username)
        if not human:
            return False
        if not verify_password(password, human.hash_password):
            return False
        return human

    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):

        """ Создание токена для пользователя """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
        return encoded_jwt

    def get_current_human(token: str = Depends(oauth2_scheme)):

        """ Получение текущего пользователя"""

        try:
            payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        human = getter_human(username=token_data.username)
        if human is None:
            raise credentials_exception
        return human

    return getter_human, authenticate_human, get_current_human, create_access_token
