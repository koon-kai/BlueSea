# -*- coding: utf-8 -*-
import time
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect,render_template, abort, g,Blueprint,flash
from werkzeug import check_password_hash, generate_password_hash
from database import db_session
from models import User,MarkItem,BookMark
#from extensions import cache


bookmark = Blueprint('bookmark', __name__)

db = db_session


def get_user_id(username):
    """Convenience method to look up the id for a username."""
    user = db.query(User).filter_by(name = username).first()
    if user == None:
        return None
    return user.id

#@cache.cached(timeout=1200, key_prefix='markitem_list')	
def get_markitem_list(user_id):
     markitem = db.query(MarkItem).filter_by(user_id = user_id)
     return markitem	 

#@cache.cached(timeout=1200, key_prefix='markitem')		 
def get_markitem(mark_id):
     markitem = db.query(MarkItem).filter_by(id = mark_id).first()
     return markitem	 
	 
def format_datetime(timestamp):
    """Format a timestamp for display."""
    #return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')
    return time.strftime('%Y-%m-%d @ %H:%M',time.localtime(timestamp))

def plus_one(mark_id):
      markitem = db.query(MarkItem).filter_by(id=mark_id).first()
      markitem.bookmark_count += 1
      db.merge(markitem)
      db.commit()

def sub_one(mark_id):
      markitem = db.query(MarkItem).filter_by(id=mark_id).first()
      markitem.bookmark_count -= 1
      db.merge(markitem)
      db.commit()

def gravatar_url(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)


@bookmark.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = db.query(User).filter_by(id =session['user_id']).first()


@bookmark.teardown_request
def shutdown_session(exception=None):
    db.remove()


@bookmark.route('/')
def home():
    if not g.user:
        return render_template('login.html')
    return render_template('bookmark/list.html', markitems= get_markitem_list(session['user_id']))     


@bookmark.route('/bookmark_detail/<mark_id>')
#@cache.cached(timeout=1200, key_prefix='bookmark_detail')	
def bookmark_detail(mark_id):
    if not g.user:
        abort(401)
    bookmarks = db.query(BookMark).filter_by(mark_id = mark_id)
    markitem = get_markitem(mark_id)
    return render_template('bookmark/detail.html',bookmarks = bookmarks,markitem=markitem)

@bookmark.route('/add_markitem/<user_id>',methods=['GET', 'POST'])
def add_markitem(user_id):
    if not g.user:
        abort(401)
    if request.method == 'POST':
        db.add(MarkItem(name=request.form['name'],user_id=user_id,bookmark_count=0,create_date=int(time.time())))
        db.commit() 
    return redirect('/')

@bookmark.route('/del_markitem/<mark_id>')
def del_markitem (mark_id):
    markitem = get_markitem(mark_id)
    db.delete(markitem)
    db.execute('delete from bookmark where mark_id=:id',{'id':mark_id})
    db.commit()
    return redirect('/')

@bookmark.route('/del_bookmark/<bookmark_id>/<mark_id>')
def del_bookmark (bookmark_id,mark_id):
     bookmark = db.query(BookMark).filter_by(id=bookmark_id).first()
     db.delete(bookmark)
     sub_one(mark_id)
     db.commit()
     return redirect('/')

@bookmark.route('/add_bookmark/<mark_id>',methods=['GET', 'POST'])
def add_bookmark(mark_id):
    if not g.user:
        abort(401)
    if request.method == 'POST':
        db.add(BookMark(mark_id=mark_id,title=request.form['title'],url=request.form['url'],create_date=int(time.time())))
        db.commit()
        plus_one(mark_id)
    return redirect('/')
	

@bookmark.route('/login', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    if g.user:
        return redirect('/')
    error = None
    if request.method == 'POST':
        user = db.query(User).filter_by(name = request.form['username']).first()
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user.pw_hash,request.form['password']):
            error = 'Invalid password'
        else:
            #flash('You were logged in')
            session['user_id'] = user.id
            return redirect('/')
    return render_template('login.html', error=error)

@bookmark.route('/to_register')
def rdirect_register ():
    return render_template('register.html')
	

@bookmark.route('/lovesong')
def lovesong():
    return render_template('/lovesong/lovesong.html')


@bookmark.route('/register', methods=['GET', 'POST'])
def register():
    """Registers the user."""
    if g.user:
        return redirect('/')
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                 '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif get_user_id(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            db.add(User(name=request.form['username'],email=request.form['email'],pw_hash=generate_password_hash(request.form['password'])))
            db.commit()
            flash('You were successfully registered and can login now')
            return redirect('/login')
    return render_template('register.html', error=error)


@bookmark.route('/logout')
def logout():
    """Logs the user out."""
    #flash('You were logged out')
    session.pop('user_id', None)
    return redirect('/login')

