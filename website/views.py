from flask import Blueprint, render_template, request, flash, jsonify, url_for, send_file, redirect
from flask_login import login_required, current_user, logout_user

from unidecode import unidecode

from werkzeug.utils import secure_filename

import os, shutil

import json
from . import db

from .models import Note, User, Files

views = Blueprint('views', __name__)

def get_dir_size(path):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total


@views.route('/', methods=["GET", "POST"])
def home():    
    return "ta tudo bem"

