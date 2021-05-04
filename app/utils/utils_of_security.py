from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Callable, Any
from pydantic import ValidationError

from fastapi import Depends, HTTPException, status, APIRouter
from jose import JWTError, jwt
from pony.orm import db_session
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from app.db import raw_models as models

from app.settings.config import cfg
from app.utils.pydantic_security import TokenData, HumanInDB, Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = cfg.get('db', "hash_algorithm")
SECRET_KEY = cfg.get('keys', "basic")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def basic_create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """ Создание токена для пользователя """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "user": "Участник программы 1000ln",
        "smmer": "Редактор различного контента на сайте",
        "direction_expert": "Проверяющий работы на конкурсе",
        "admin": "Управляющий сайтом",
        "developer": "Разработчик сайта"
    },
)
scopes_to_db = {
    "user": models.User,
    "smmer": models.Smm,
    "direction_expert": models.DirectionExpert,
    "admin": models.Admin,
    "developer": models.Developer
}


def generate_security(entity,
                      getter_human=None,
                      ):
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
            print('---------', username)

    def authenticate_human(username: str, password: str):

        """ Аунтидификация пользователя"""
        print(username)
        human = getter_human(username)
        if not human:
            return False
        if not verify_password(password, human.hash_password):
            return False
        return human

    def get_current_human(
            security_scopes: SecurityScopes,
            token: str = Depends(oauth2_scheme)
    ):

        """ Получение текущего пользователя"""
        if security_scopes.scopes:
            authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        else:
            authenticate_value = f"Bearer"
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_scopes = payload.get("scopes", [])
            token_data = TokenData(scopes=token_scopes, username=username)
        except (JWTError, ValidationError):
            raise credentials_exception
        human = getter_human(username=token_data.username)
        if human is None:
            raise credentials_exception
        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
        return human

    return getter_human, authenticate_human, get_current_human, basic_create_access_token


security = APIRouter(
    tags=["security"],
    responses={404: {"description": "Not found"}},
)


def check_scopes(username, password, scopes):
    roles = []

    print(username, password, "||", scopes)
    print(scopes_to_db.keys())
    for scope in scopes:
        if scope in scopes_to_db:
            if scopes_to_db[scope].exists(username=username):
                ent = scopes_to_db[scope].get(username=username)
                if not verify_password(password, ent.hash_password):
                    print("error password")
                    return False
                roles.append(ent)
            else:
                return False
    return roles


@security.post("/token", response_model=Token)
@db_session
def basic_login(form_data: OAuth2PasswordRequestForm = Depends(),
                                     authenticate: str = None,
                                     access_token_time=0,
                                     create_access_token: str = None):
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if create_access_token is None and authenticate is None:
        print(1)
        role = check_scopes(form_data.username, form_data.password, form_data.scopes)
        if not role or not bool(role):
            print(0, role)
            raise error
        role = HumanInDB.from_orm(role[-1])
        create_access_token = basic_create_access_token
        access_token_time = 30
    elif authenticate is None:
        print(2)
        raise error
    elif create_access_token is None:
        print(3)
        raise error
    else:
        print(4)
        role = authenticate(form_data.username, form_data.password)
    if not role:
        print(5)
        raise error
    access_token_expires = timedelta(minutes=access_token_time)
    access_token = create_access_token(
        data={"sub": role.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    print(form_data.scopes, "access_token", access_token)
    return {"access_token": access_token, "token_type": "bearer"}
