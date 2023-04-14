# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 16:51:25 2023

@author: Vitaly
"""

from dataclasses import dataclass

@dataclass(slots = True)
class WordTransl:

    word: str
    translation: str
    pk: int = 0
    
@dataclass(slots = True)
class Lesson_data:

    date: int
    theme: str
    difficulty: int
    pk: int = 0