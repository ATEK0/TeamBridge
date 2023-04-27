from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user

import json
from . import db

from .models import Note

views = Blueprint('views', __name__)


@views.route('/', methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        user = current_user.query.filter_by(email = current_user.email).first()
        
        title = request.form.get("title")
        text = request.form.get("note")
        if len(title) > 1 and len(text) > 1:
            new_note = Note(title=title, text=text,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added", category="success")
        else:
            flash("You need to insert something to create a note", category="error")
    
    return render_template("home.html", client=current_user)


@views.route('/delete-note', methods=["POST"])
# @login_required
def deleteNote():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if current_user.id == note.user_id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})
        else:
            flash("Something went wrong", category="error")
        
        
    return jsonify({}), current_user