# -*- coding: utf-8 -*-
import time
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from database import Model


class Account(Model):
    __tablename__ = 'account'
    id = Column('id', Integer, primary_key=True,autoincrement = True)
    user_id = Column('user_id',Integer)
    account_name = Column('account_name',String(100))
    user_name = Column('user_name',String(100))
    email = Column('email',String(200))
    passwd = Column('passwd', String(200))
    create_date = Column('create_date',Integer)

    def __init__(self,user_id,account_name,user_name,email,passwd,create_date):
        self.user_id = user_id
        self.account_name = account_name
        self.user_name = user_name
        self.email = email
        self.passwd = passwd
		
        if create_date == None:
            self.create_date = int(time.time())
        else:
            self.create_date = create_date

    def __repr__(self):
        return '<Account %s>' % (self.account_name) 