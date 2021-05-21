from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Tuple, Union
from pydantic import ValidationError
from collections import defaultdict

from fastapi import Depends, HTTPException, status, APIRouter
from jose import JWTError, jwt
from pony.orm import db_session
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from app.db import models as m

from app.settings.config import cfg
from app.utils.pydantic_security import TokenData, HumanInDB, Token, BaseModel
from app.pydantic_models.standart_methhods_redefinition import AccessType, AccessMode

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

# scopes_to_db = {
#     "user": m.User,
#     "smmer": m.Smm,
#     "direction_expert": m.DirectionExpert,
#     "admin": m.Admin,
#     "developer": m.Developer
# }

scopes_to_db: Dict[m.db.Entity, List[AccessType]] = {
    m.User: [AccessType.USER],
    m.Smm: [AccessType.SMMER],
    m.DirectionExpert: [AccessType.DIRECTION_EXPERT],
    m.Admin: [AccessType.ADMIN, AccessType.SMMER],
    m.Developer: [AccessType.DEVELOPER, AccessType.USER,
                  AccessType.DIRECTION_EXPERT, AccessType.ADMIN,
                  AccessType.SMMER]
}
scopes_to_db: Dict[m.db.Entity, List[str]] = {key: [i.value for i in val] for key, val in scopes_to_db.items()}
app_routers_to_scopes: dict[str, list[str]] = defaultdict(lambda i: [])
app_routers_to_scopes.update({
    "admin": scopes_to_db[m.Admin],
    "public_router": [],
    "user": scopes_to_db[m.User],
    "smm": scopes_to_db[m.Smm],
    "dev": scopes_to_db[m.Developer],
    "direction_expert": scopes_to_db[m.DirectionExpert],
})


class PassScopes(BaseModel):
    scopes: List[str] = []
    scope_str: str = ""


def generate_security(entity, getter_human=None):
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
            if m.Human.exists(username=username):
                human_db = m.Human.get(username=username)
                return HumanInDB.from_pony_orm(human_db)

    def authenticate_human(username: str, password: str):

        """ Аунтидификация пользователя"""

        human = getter_human(username)
        if not human:
            return False
        if not verify_password(password, human.hash_password):
            return False
        return human

    def get_current_human(
            security_scopes: SecurityScopes = PassScopes(),
            token: str = Depends(oauth2_scheme)):

        """ Получение текущего пользователя"""

        try:
            print(security_scopes.scopes)
            if security_scopes.scopes and bool(security_scopes.scopes):
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
            print(security_scopes.scopes)
            print(token_data.scopes)
            for scope in security_scopes.scopes:
                if scope not in token_data.scopes:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Not enough permissions",
                        headers={"WWW-Authenticate": authenticate_value},
                    )
            return human
        except HTTPException as e:
            print("---===", [e])
            raise e
        except Exception as e:
            print("Произошла ошибка в текущем пользователе!!!", [e])
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    return getter_human, authenticate_human, get_current_human, basic_create_access_token


security = APIRouter(
    tags=["security"],
    responses={404: {"description": "Not found"}},
)


def check_scopes(username: str, password: str, scopes: List[str]) \
        -> Tuple[Optional[m.db.Entity], Union[List[str], bool]]:
    if not m.Human.exists(username=username):
        return None, False
    ent = m.Human.get(username=username)
    scopes = [i for i in scopes_to_db[ent.__class__] if i in scopes]
    if verify_password(password, ent.hash_password):
        return ent, scopes
    return None, False
    # print(username, password, "||", scopes)
    # print(scopes_to_db.keys())
    # for scope in scopes:
    #     if scope in scopes_to_db:
    #         if scopes_to_db[scope].exists(username=username):
    #             ent = scopes_to_db[scope].get(username=username)
    #             if not verify_password(password, ent.hash_password):
    #                 print("error password")
    #                 return False
    #             roles.append(ent)
    #         else:
    #             return False
    # return roles


@security.post("/token", response_model=Token)
@db_session
def basic_login(form_data: OAuth2PasswordRequestForm = Depends(), access_token_time=0):
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": 'Bearer Basic realm="Restricted Area"'},
    )
    create_access_token = basic_create_access_token
    print(form_data.scopes)
    ent, form_data.scopes = check_scopes(form_data.username, form_data.password, form_data.scopes)
    print(form_data.scopes)
    if not ent:
        print(0, ent)
        raise error
    # ent = HumanInDB.from_pony_orm(ent)
    if access_token_time == 0:
        access_token_time = 30
    access_token_expires = timedelta(minutes=access_token_time)
    access_token = create_access_token(
        data={"sub": ent.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    print(form_data.scopes, "access_token", access_token)
    return {"access_token": access_token, "token_type": "bearer"}
