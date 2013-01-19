# coding: utf-8
import os.path
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from database import init_db
from flask import Flask
from views import format_datetime,gravatar_url
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqlamodel import ModelView
import config
from models import User,MarkItem,BookMark,Account,Note
from database import db_session
#from flask.ext.cache import Cache
#from extensions import cache


app = Flask(__name__)
app.config.from_object(config)


def register_blueprints(app):
    # Prevents circular imports
    from views import bookmark
    from views import note
    app.register_blueprint(bookmark)
    app.register_blueprint(note)
    
register_blueprints(app)

#init cache
#cache = Cache()
#cache.init_app(app, config={'CACHE_TYPE': 'memcached'})

#register filters
app.jinja_env.filters['datetimeformat'] = format_datetime
app.jinja_env.filters['gravatar'] = gravatar_url

admin = Admin(app,name="BlueSea")
admin.add_view(ModelView(User, db_session))
admin.add_view(ModelView(MarkItem, db_session))
admin.add_view(ModelView(BookMark, db_session))
admin.add_view(ModelView(Account, db_session))
admin.add_view(ModelView(Note, db_session))


#admin.init_app(app)


if __name__ == '__main__':
    #init_db()
    app.run('0.0.0.0',port=1220)