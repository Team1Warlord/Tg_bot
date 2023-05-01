# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 16:27:01 2023

@author: Vitaly
"""

from pony import orm

db = orm.Database()

class def_database():
    @staticmethod
    def get_database(name: str) -> db.Entity:
        if name == 'WordTransl':
            return WordTransl
        elif name == 'Lesson_data':
            return Lesson_data
        elif name == 'Websites':
            return Websites

def convert_from_py2sqlite(data):
    if isinstance(data, int) and data == -1000:
        return None
    else:
        return data

class WordTransl(db.Entity):
    pk = orm.PrimaryKey(int, auto=True)
    word = orm.Required(str, 30)
    translation = orm.Required(str, 30)

    def get_data(self):
        return {
            'pk': convert_from_py2sqlite(self.pk),
            'word': self.word,
            'translation': self.translation
        }
    
class Websites(db.Entity):
    pk = orm.PrimaryKey(int, auto=True)
    website_name = orm.Required(str, 30)
    link = orm.Required(str, 120)

    def get_data(self):
        return {
            'pk': convert_from_py2sqlite(self.pk),
            'website_name': self.website_name,
            'link': self.link
        }

class Lesson_data(db.Entity):
    pk = orm.PrimaryKey(int, auto=True)
    date = orm.Required(str)
    theme = orm.Required(str)
    difficulty = orm.Required(int)

    def get_data(self):
        return {
            'pk': convert_from_py2sqlite(self.pk),
            'date': self.date,
            'theme': self.theme,
            'difficulty': self.difficulty
        }