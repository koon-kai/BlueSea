# -*- coding: utf-8 -*-
import time
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from database import Model


class MarkItem(Model):
    __tablename__ = 'markitem'
    id = Column('mark_id', Integer, primary_key=True,autoincrement = True)
    name = Column('mark_name', String(200))
    user_id = Column('user_id',Integer)
    bookmark_count =Column('bm_count',Integer)
    create_date = Column('create_date',Integer)

    def __init__(self,name,user_id,bookmark_count,create_date):
        self.name = name
	self.user_id = user_id
        self.bookmark_count = bookmark_count
	if create_date == None:
            self.create_date =int(time.time())
        else:
            self.create_date = create_date

    def __repr__(self):
        return '<MarkItem %s>' % (self.name) 