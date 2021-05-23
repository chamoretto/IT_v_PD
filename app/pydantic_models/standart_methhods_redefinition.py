from __future__ import annotations
import inspect
from typing import Type, Union, Dict, Any, cast, TypeVar
import warnings

from fastapi import Form, Request
from pydantic.fields import ModelField
from pydantic import BaseModel, BaseConfig, ConfigError
from pydantic.utils import is_valid_field
from pydantic.main import inherit_config
from fastapi import status

import enum
from importlib import import_module
import inspect

from app.utils.exceptions import ChildHTTPException as HTTPException


DictStrAny = dict[str, Any]
Model = TypeVar('Model', bound='BaseModel')


def pydantic_from_orm(cls, db_ent, all_obj=False):
    data: dict = db_ent.to_dict(related_objects=all_obj or False, with_collections=True)
    if all_obj:
        data |= {key: val.to_dict(related_objects=False, with_collections=True)
                 for key, val in data.items() if hasattr(val, "to_dict")}
        data |= {key: [i.to_dict(related_objects=False, with_collections=True) for i in val]
                 for key, val in data.items() if type(val) in [list, set, frozenset]}
    print(data)
    return cls(**data)


setattr(BaseModel, "from_pony_orm", classmethod(pydantic_from_orm))


def as_form(cls: Type[BaseModel]):
    """
    Adds an as_form class method to decorated models. The as_form class method
    can be used with FastAPI endpoints
    """
    new_params = [
        inspect.Parameter(
            field.alias,
            inspect.Parameter.POSITIONAL_ONLY,
            default=(Form(field.default) if not field.required else Form(...)),
            annotation=field.outer_type_,
        )
        for field in cls.__fields__.values()
    ]

    async def _as_form(**data):
        return cls(**data)

    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)
    _as_form.__signature__ = sig
    setattr(cls, "as_form", _as_form)
    return cls


class PydanticValidators:

    @staticmethod
    def datetime(cls: BaseModel, value):
        if value is None or not bool(value):
            return None
        return value

    @staticmethod
    def date(cls: BaseModel, value):
        if value is None or not bool(value):
            return None
        return value

    def __class_getitem__(cls, code: 'AllInfoStr') -> str:
        print('----------------', code.html_type or [str(code.html_type)])
        if hasattr(PydanticValidators, str(code.html_type)):
            return f'\n\n\t@validator("{code.name}", pre=True, always=True)\n' \
                   f'\tdef {code.name}_to_{code.html_type}_validator(cls, value):\n' \
                   f'\t\treturn PydanticValidators.{code.html_type}(cls, value)\n'
        return ""


@enum.unique
class AccessType(enum.Enum):
    PUBLIC = "public"
    USER = "user"
    SMMER = "smm"
    DIRECTION_EXPERT = "expert"
    ADMIN = "admin"
    DEVELOPER = "dev"
    SELF = "self"

    @classmethod
    def get_obj(cls, val: str):
        if val in cls._value2member_map_:
            return cls._value2member_map_[val]
        print(val)
        raise AttributeError

    def __str__(self):
        return self.value


@enum.unique
class AccessMode(enum.Enum):
    LOOK = "look"
    CREATE = "create"
    EDIT = "edit"

    @classmethod
    def get_obj(cls, val: str):
        if val in cls._value2member_map_:
            return cls._value2member_map_[val]
        print(val)
        raise AttributeError

    def __str__(self):
        return self.value


def create_model(
        __model_name: str,
        *,
        __config__: Type[BaseConfig] = None,
        __base__: Union[Type['Model'], list[Type['Model']]] = None,
        __module__: str = __name__,
        __validators__: Dict[str, classmethod] = None,
        **field_definitions: Any,
) -> Type['Model']:
    """
    Dynamically create a model.
    :param __model_name: name of the created model
    :param __config__: config class to use for the new model
    :param __base__: base class for the new model to inherit from
    :param __module__: module of the created model
    :param __validators__: a dict of method names and @validator class methods
    :param field_definitions: fields of the model (or extra fields if a base is supplied)
        in the format `<name>=(<type>, <default default>)` or `<name>=<default value>, e.g.
        `foobar=(str, ...)` or `foobar=123`, or, for complex use-cases, in the format
        `<name>=<FieldInfo>`, e.g. `foo=Field(default_factory=datetime.utcnow, alias='bar')`
    """

    if __base__ is not None:
        if __config__ is not None:
            raise ConfigError('to avoid confusion __config__ and __base__ cannot be used together')
    else:
        __base__ = cast(Type['Model'], BaseModel)

    fields = {}
    annotations = {}

    for f_name, f_def in field_definitions.items():
        if not is_valid_field(f_name):
            warnings.warn(f'fields may not start with an underscore, ignoring "{f_name}"', RuntimeWarning)
        if isinstance(f_def, tuple):
            try:
                f_annotation, f_value = f_def
            except ValueError as e:
                raise ConfigError(
                    'field definitions should either be a tuple of (<type>, <default>) or just a '
                    'default value, unfortunately this means tuples as '
                    'default values are not allowed'
                ) from e
        else:
            f_annotation, f_value = None, f_def

        if f_annotation:
            annotations[f_name] = f_annotation
        fields[f_name] = f_value

    namespace: 'DictStrAny' = {'__annotations__': annotations, '__module__': __module__}
    if __validators__:
        namespace.update(__validators__)
    namespace.update(fields)
    if __config__:
        namespace['Config'] = inherit_config(__config__, BaseConfig)
    if type(__base__) not in [tuple, set, list, frozenset, tuple]:
        __base__: tuple[Type['Model']] = (__base__,)
        print('rfwef')
    else:
        print('sdf')
        __base__: tuple[Type['Model']] = tuple(__base__)
    print('5778346', [__base__])
    return cast(Type['Model'], type(__model_name, __base__, namespace))


_roles = [i.value for i in AccessType]
_modes = [i.value for i in AccessMode]
_access_level = [(str(role), str(mode)) for role in _roles for mode in _modes]


# print(_access_level)


def get_pd_class(ent_name: str, request: Request,
                 roles: Union[AccessType, str, list[Union[AccessType, str]]],
                 modes: Union[AccessMode, str, list[Union[AccessMode, str]]]
                 ) -> Type[BaseModel]:
    print("roles", roles)
    print('modes', modes)
    if (type(roles) in [str, AccessType] or len(roles) == 1) and (type(modes) in [str, AccessMode] or len(modes) == 1):
        if type(roles) not in [str, AccessType]:
            roles: str = roles[0]
        if type(modes) not in [str, AccessMode]:
            modes: str = modes[0]
        model = getattr(import_module(f"app.pydantic_models.gen.{roles}.{roles}_{modes}"), ent_name)
        if f"{roles}_{modes}.py" in inspect.getfile(model):
            return model
        raise HTTPException(
            request=request,
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Вы не обладаете домтаточными правами доступа для совершения данного действия",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if type(roles) in [str, AccessType]:
        roles: list[str] = [roles]
    if type(modes) in [str, AccessMode]:

        modes: list[str] = [modes]
    print(_access_level)
    _bases = sorted([(str(role), str(mode)) for role in roles for mode in modes], key=lambda i: -_access_level.index(i))
    bases = []
    for [role, mode] in _bases:
        try:
            obj = getattr(import_module(f"app.pydantic_models.gen.{role}.{role}_{mode}"), ent_name)
            assert f"{role}_{mode}.py" in inspect.getfile(obj)
            bases.append(obj)
        except (ImportError, AttributeError, AssertionError) as e:
            print(f"ошибка при импорте модуля {role}_{mode}, {ent_name}", __file__, e)
    # print(bases)
    if bool(bases):
        return create_model('ModelForDb', __base__=bases)
    raise HTTPException(
        request=request,
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Вы не обладаете домтаточными правами доступа для совершения данного действия",
        headers={"WWW-Authenticate": "Bearer"},
    )

# from app.pydantic_models import gen

# print(gen.input_ent)

# print(*get_pd_class("User", [AccessType.PUBLIC, AccessType.DEVELOPER, AccessType.USER], [AccessMode.CREATE, AccessMode.LOOK]).__fields__.items(), sep="\n")
# get_pd_class("", AccessType.ADMIN, AccessMode.CREATE)
