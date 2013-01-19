# -*- coding: utf-8 -*-
import time
from sqlalchemy import create_engine, Column, Integer, String, DateTime,Text
from database import Model


class Note(Model):
    __tablename__ = 'note'
    id = Column('note_id', Integer, primary_key=True,autoincrement = True)
    title = Column('title', String(200))
    content = Column('content',Text)
    user_id = Column('user_id',Integer)
    create_date = Column('create_date',Integer)

    def __init__(self,title,content,user_id):
        self.title = title
        self.content = content
	self.user_id = user_id 
	#if create_date == None:
        self.create_date =int(time.time())
        #else:
        #self.create_date = create_date

    def __repr__(self):
        return '<Note %s>' % (self.title) 