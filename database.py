# coding: utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config

config = config.cof()

engine = create_engine(config.db_url,
                       convert_unicode=True,
                       **config.db_conn_opt)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,bind=engine))


Model = declarative_base(name='Model')
Model.query = db_session.query_property()


def init_db():
    import models
    print u'database init successfully.'
    Model.metadata.create_all(bind=engine)
    return

  
   
		

