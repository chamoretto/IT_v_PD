from functools import reduce

# =======! Правила изменения типа pony-атрибутов !=======
change_attr_type_rules = {
    "Json": "Union[Json, dict]",
    "time": "time",
    "datetime": "datetime"
}
change_attr_type = {
    lambda i, db: i.param_type in change_attr_type_rules:
        lambda i: setattr(i, 'param_type', change_attr_type_rules[i.param_type]),
    lambda i, db: i.param_type in db.entities and i.db_type in ["Required", "PrimaryKey"]:
        lambda i: setattr(i, 'param_type', "Pk" + i.param_type),
    lambda i, db: i.param_type in db.entities and i.db_type == "Optional":
        lambda i: [setattr(i, 'param_type', "OptionalPk" + i.param_type),
                   setattr(i, 'db_type', "")],
    lambda i, db: i.param_type in db.entities and i.db_type == "Set":
        lambda i: [setattr(i, 'param_type', "SetPk" + i.param_type),
                   setattr(i, 'db_type', "")],
}

# =======! Интерпретируем типы полей БД в pydantic-язык !=======
change_db_field = {
    "PrimaryKey": "",
    "Required": "",
    "Optional": "Optional",
    "Set": "Set",
    "Discriminator": "Optional",
}
type_db_param_to_text = {
    lambda i: i.db_type in change_db_field:
        lambda i: setattr(i, 'db_type', change_db_field[i.db_type]),
}

# =======! Устанавливаем значения по умолчанию !=======
change_default_rules = {
    "": None,
    "PrimaryKey": None,
    "Required": None,
    "Optional": "None",
    "Set": "[]"
}
change_default = {
    lambda i: i.default is not None and "lambda" not in i.default and i.param_type == "bool":
        lambda i: setattr(i, 'default', ("True" if any(j in i.default.lower() for j in ["1", "true"]) else "False")),
    lambda i: i.default is not None and "lambda" not in i.default and i.param_type in ["int", "float"]:
        lambda i: setattr(i, 'default', reduce(lambda st, i: st.replace(i), ["'", '"'], i.default)),
    lambda i: i.default is not None and "lambda" not in i.default and i.param_type == "Json":
        lambda i: setattr(i, 'default', '"' + i.default + '"'),
    lambda i: i.default is None or "lambda" in i.default:
        lambda i: setattr(i, 'default', change_default_rules[i.db_type]),
    lambda i: (i.default is None or "lambda" in i.default) and "Set" in i.param_type:
        lambda i: setattr(i, 'default', "[]"),
    lambda i: (i.default is None or "lambda" in i.default) and "Optional" in i.param_type:
        lambda i: setattr(i, 'default', "None"),
}
