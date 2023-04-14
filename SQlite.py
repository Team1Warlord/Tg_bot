# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 16:23:36 2023

@author: Vitaly
"""

from typing import Any
from inspect import get_annotations

from pony import orm

from AbstractRepo import AbstractRepository, T
import database 
from utility import py2sqlite_type_converter

class SQlite(AbstractRepository[T]):
    """
    SQLite3 repository
    """
    def __init__(self, data_type: type,
                        table_type: str) -> None:

        self.table_type = database.def_database.get_database(table_type)
        self.data_type = data_type
        self.data_fields = get_annotations(self.data_type, eval_str=True)
        self.data_fields.pop('pk')

    @staticmethod
    def bind(db_name: str = 'database.db'):
        database.db.bind(provider='sqlite', 
                    filename=db_name,
                    create_db=True)

        database.db.generate_mapping(create_tables=True)

    @orm.db_session
    def add(self, obj: T) -> int:
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')

        kwargs = {
            a: py2sqlite_type_converter(getattr(obj, a)) 
            for a in self.data_fields.keys()
        }

        db_obj = self.table_type(**kwargs)
        orm.commit()

        obj.pk = db_obj.pk
        return obj.pk

    @orm.db_session
    def get(self, pk: int) -> T | None:
        db_obj = orm.select(p for p in self.table_type if p.pk == pk)[:]

        if len(db_obj) == 0:
            return None

        return self.data_type(**db_obj[0].get_data())

    # @orm.db_session
    #  def update(self, obj: T) -> None:
    #      if obj.pk == 0:
    #          raise ValueError('attempt to update object with unknown primary key')
    
    #      db_obj = self.table_type[obj.pk]

    #      for f in self.data_fields.keys():
    #          setattr(db_obj, f, py2sqlite_type_converter(getattr(obj, f)))

    @orm.db_session
    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        if where is None:  # return all objects from the table
            db_obj_lst = orm.select(p for p in self.table_type)[:]

            obj_lst = []
            for db_obj in db_obj_lst:
                obj_lst.append(self.data_type(**db_obj.get_data()))
            return obj_lst
        # return objects accroding to condition
        attr1, value1 = list(where.items())[0]
        db_obj_lst = orm.select(p for p in self.table_type
            if getattr(p, attr1) == value1)
        db_obj_lst = [p for p in db_obj_lst
            if all(getattr(p, attr) == value for (attr, value) in where.items())]

        obj_lst = []
        for db_obj in db_obj_lst:
            obj_lst.append(self.data_type(**db_obj.get_data()))

        return obj_lst

    # @orm.db_session
    # # def delete(self, pk: int) -> None:
    # #     try:
    # #         self.table_type[pk].delete()
    # #     except orm.ObjectNotFound:
    # #         pass