# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from database import Model


class User(Model):
    __tablename__ = 'user'
    id = Column('user_id', Integer, primary_key=True,autoincrement = True)
    name = Column('user_name', String(200))
    email = Column('email',String(200))
    pw_hash = Column('pw_hash',String(200))

    def __init__(self,name,email,pw_hash):
        self.name = name
        self.email = email
        self.pw_hash = pw_hash

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
    # Required for administrative interface
    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<User %s>' % (self.name)  