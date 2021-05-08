from typing import Any

class AddArrtInDbClass(object):
    """
    Класс-родитель для сущностей БД

    Содержит инструменты для добавления новых методов (и не только)
    к классам сущностей БД.
    Добавляется к классам сущностей БД как второй родитель,
    что позволяет использовать синтаксис:

    @Group.only_getter
    def get_all_homework(self):
        # какой-то код
        return all_homework

    К примеру, можно добавить к сущности группы (Group)
    геттер (@property), возвращающий список всего домашнего задания
    для этой группы.
    """

    change_field: dict[Any, dict[str, str]] = dict()  # Список изменённых атрибутов
    # change_field_types = dict()

    @classmethod
    def getter_and_classmethod(cls, func):
        """добавляет одноимянный атрибут и метод сласса"

        Это означает, что можно так:
        Group['20ВП1'].func
        и Group.cl_func(name='20ВП1')
        вместо name='20ВП1' могут быть любые параметры, идентифицирующие сущность
        """
        setattr(cls, func.__name__, property(func))  # types.MethodType(func, cls)

        def w(*arfs, **kwargs):
            if cls.exists(**kwargs):
                ent = cls.get(**kwargs)
                return getattr(ent, func.__name__)
            return None

        setattr(cls, 'cl_' + func.__name__, classmethod(w))
        # AddArrtInDbClass.change_field[cls] = set(list(AddArrtInDbClass.change_field.get(cls, [])) + [func.__name__, 'cl_' + func.__name__])
        AddArrtInDbClass.change_field[cls] = AddArrtInDbClass.change_field.get(cls, dict()) | {func.__name__: "@property", 'cl_' + func.__name__: "@classmethod"}
        # AddArrtInDbClass.change_field_types[func.__name__] = "@property"
        # AddArrtInDbClass.change_field_types['cl_' + func.__name__] = "@classmethod"

    @classmethod
    def only_func(cls, func):
        """добавляет к классу одноимянную функцию

        Это означает, что можно так:
        Group['20ВП1'].func(ваши параметры, которые требует функция)"""
        setattr(cls, func.__name__, func)  # types.MethodType(func, cls)
        AddArrtInDbClass.change_field[cls] = AddArrtInDbClass.change_field.get(cls, dict()) | {func.__name__: ""}
        # AddArrtInDbClass.change_field[cls] = set(list(AddArrtInDbClass.change_field.get(cls, [])) + [func.__name__])
        # AddArrtInDbClass.change_field_types[func.__name__] = ""


    @classmethod
    def func_and_classmethod(cls, func):
        """добавляет к классу одноимянную функцию и метод класса

        Это означает, что можно так:
        Group['20ВП1'].func(ваши параметры, которые требует функция)
        и так
        Group['20ВП1'].func(ваши параметры, которые требует функция)"""
        setattr(cls, func.__name__, func)

        def w(*arfs, **kwargs):
            if cls.exists(id=kwargs.get('id', -1234)):
                ent = cls.get(id=kwargs.get('id', -1234))
                return getattr(ent, func.__name__)(*arfs, **kwargs)
            return None

        setattr(cls, 'cl_' + func.__name__, classmethod(w))
        AddArrtInDbClass.change_field[cls] = AddArrtInDbClass.change_field.get(cls, dict()) | {func.__name__: "", 'cl_' + func.__name__: "@classmethod" }
        # AddArrtInDbClass.change_field[cls] = set(list(AddArrtInDbClass.change_field.get(cls, [])) + [func.__name__, 'cl_' + func.__name__])
        # AddArrtInDbClass.change_field_types[func.__name__] = ""
        # AddArrtInDbClass.change_field_types['cl_' + func.__name__] = "@classmethod"



    @classmethod
    def only_setter(cls, func):
        """добавляет к классу одноимянный сеттер

        Это означает, что можно так:
        Group['20ВП1'].func = ваше значение"""
        setattr(cls, func.__name__, getattr(cls, func.__name__).setter(func))  # types.MethodType(func, cls)
        AddArrtInDbClass.change_field[cls] = AddArrtInDbClass.change_field.get(cls, dict()) | {func.__name__: f"@{func.__name__}.setter"}
        # AddArrtInDbClass.change_field[cls] = set(list(AddArrtInDbClass.change_field.get(cls, [])) + [func.__name__])
        # AddArrtInDbClass.change_field_types[func.__name__] = f"@{func.__name__}.setter"

    @classmethod
    def only_getter(cls, func):
        """добавляет одноимянный геттер

        Это означает, что можно так:
        Group['20ВП1'].func"""
        setattr(cls, func.__name__, property(func))  # types.MethodType(func, cls)
        AddArrtInDbClass.change_field[cls] = AddArrtInDbClass.change_field.get(cls, dict()) | {func.__name__: "@property"}
        # AddArrtInDbClass.change_field[cls] = set(list(AddArrtInDbClass.change_field.get(cls, [])) + [func.__name__])
        # AddArrtInDbClass.change_field_types[func.__name__] = "@property"


    @classmethod
    def only_classmetod(cls, func):
        """добавляет к классу метод класса

        Это означает, что можно так:
        Group.func()"""
        setattr(cls, func.__name__, classmethod(func))
        AddArrtInDbClass.change_field[cls] = AddArrtInDbClass.change_field.get(cls, dict()) | {func.__name__: "@classmethod"}
        # AddArrtInDbClass.change_field[cls] = set(list(AddArrtInDbClass.change_field.get(cls, [])) + [func.__name__])
        # AddArrtInDbClass.change_field_types[func.__name__] = "@classmethod"


    @classmethod
    def only_staticmethod(cls, func):
        """добавляет к классу статический метод

        Это означает, что можно так:
        Group.func(<параметры>)
        Group['20ВП1'].func(<параметры>)"""
        setattr(cls, func.__name__, staticmethod(func))
        AddArrtInDbClass.change_field[cls] = AddArrtInDbClass.change_field.get(cls, dict()) | {func.__name__: "@staticmethod"}
        # AddArrtInDbClass.change_field[cls] = set(list(AddArrtInDbClass.change_field.get(cls, [])) + [func.__name__])
        # AddArrtInDbClass.change_field_types[func.__name__] = "@staticmethod"

