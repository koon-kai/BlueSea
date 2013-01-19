# -*- coding: utf-8 -*-
import time
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from database import Model


class BookMark(Model):
    __tablename__ = 'bookmark'
    id = Column('bm_id', Integer, primary_key=True,autoincrement = True)
    mark_id = Column('mark_id',Integer)
    title = Column('title', String(200))
    url = Column('url',String(400))
    create_date = Column('create_date',Integer)

    def __init__(self,mark_id,title,url,create_date):
        self.mark_id = mark_id
        self.title = title
	self.url = url	
        if create_date == None:
            self.create_date = int(time.time())
        else:
            self.create_date = create_date

    def __repr__(self):
        return '<BookMark %s>' % (self.title) 