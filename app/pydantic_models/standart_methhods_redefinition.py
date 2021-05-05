from pydantic import BaseModel


def pydantic_from_orm(cls, db_ent):
    return cls(**db_ent.to_dict(related_objects=False, with_collections=True))


setattr(BaseModel, "from_pony_orm", classmethod(pydantic_from_orm))