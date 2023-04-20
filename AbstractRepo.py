# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 16:27:32 2023

@author: Vitaly
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Protocol, Any
from dataclasses import dataclass

@dataclass(slots = True)
class WordTransl:

    word: str
    translation: str
    pk: int = 0
    
@dataclass(slots = True)
class Lesson_data:

    date: str
    theme: str
    difficulty: int
    pk: int = 0

class Model(Protocol):  # pylint: disable=too-few-public-methods
    """
    Модель должна содержать атрибут pk
    """
    pk: int


T = TypeVar('T', bound=Model)



class AbstractRepository(ABC, Generic[T]):
    """
    Абстрактный репозиторий.
    Абстрактные методы:
    add
    get
    get_all
    update
    delete
    """

    @abstractmethod
    def add(self, obj: T) -> int:
        """
        Добавить объект в репозиторий, вернуть id объекта,
        также записать id в атрибут pk.
        """

    @abstractmethod
    def get(self, pk: int) -> T | None:
        """ Получить объект по id """

    @abstractmethod
    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """

    # @abstractmethod
    # def update(self, obj: T) -> None:
    #     """ Обновить данные об объекте. Объект должен содержать поле pk. """

    # @abstractmethod
    # def delete(self, pk: int) -> None:
    #     """ Удалить запись """