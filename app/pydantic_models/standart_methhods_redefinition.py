import inspect
from typing import Type

from fastapi import Form
from pydantic.fields import ModelField
from pydantic import BaseModel


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