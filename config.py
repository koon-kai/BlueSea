# coding: utf-8
import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
PER_PAGE = 30
SECRET_KEY = 'bluesea_key'
#DATABASE_URI = cof.db_url
#DATABASE_CONNECT_OPTIONS = cof.db_conn_opt

class cof: pass

cof.db_url = 'sqlite:///' + os.path.join(_basedir, 'bluesea.db')
cof.db_conn_opt  = {}