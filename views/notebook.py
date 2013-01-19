# -*- coding: utf-8 -*-
import time
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect,render_template, abort, g,Blueprint,flash
from werkzeug import check_password_hash, generate_password_hash
from database import db_session
from models import User,Note
import markdown


note = Blueprint('note', __name__, template_folder='templates')

db = db_session



def get_note_list(user_id):
     notes = db.query(Note).filter_by(user_id = user_id)
     return notes	 


@note.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = db.query(User).filter_by(id =session['user_id']).first()


@note.route('/notebook')
def notebook():
    if not g.user:
        return render_template('login.html')
    return render_template('notebook/list.html', notes= get_note_list(session['user_id']))     


@note.route('/notebook/add', methods=['GET', 'POST'])
def add_note():
    if request.method == 'GET':
        return render_template("notebook/add.html")

    title = request.form["note[title]"]
    origin_content = request.form["note[content]"]
    content = markdown.markdown(origin_content)
    if title != '' and origin_content != '':
        db.add(Note(title=title,content=content,user_id=session['user_id']))
        db.commit()
        return redirect("/notebook")
    else:
        return render_template("notebook/add.html")


@note.route('/notebook/edit/<nid>',methods=['GET', 'POST'])
def edit_note(nid):
    if request.method == 'GET':
        note = db.query(Note).get(nid)
        print note
        if note is None:
            abort(404)
        return render_template("notebook/edit.html",note=note)

    title = request.form["note[title]"]
    origin_content = request.form["note[content]"]
    content = markdown.markdown(origin_content)
    if title != '' and origin_content != '':
        note = db.query(Note).get(nid)
        note.title = title
        note.user_id = session['user_id']
        note.content = content
        db.commit()
        return redirect("/notebook")
    else:
        return render_template("notebook/edit.html")


@note.route('/notebook/del/<note_id>')
def del_note(note_id):
    note = db.query(Note).filter_by(id=note_id).first()
    db.delete(note)
    db.commit()
    return redirect('/notebook')





	




