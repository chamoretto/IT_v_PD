from typing import Optional, List

from app.pydantic_models.standart_methhods_redefinition import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []


class Human(BaseModel):
    username: str
    email: Optional[str] = None

    class Config:
        from_orm = True


class PdContacts(BaseModel):
    phone: Optional[str] = None
    vk: Optional[str] = None
    insagramm: Optional[str] = None
    facebook: Optional[str] = None
    home_adress: Optional[str] = None
    telegram: Optional[str] = None


class HumanInDB(Human):
    hash_password: str
    id: int
    username: str
    name: str
    surname: str
    contacts: Optional[PdContacts] = None
    photo: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_orm = True

# class AdminInDB(HumanInDB):
#
#     class Config:
#         from_orm = True
