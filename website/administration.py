from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify

from .models.User import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

administration = Blueprint('administration', __name__)

@administration.route('/admin/administration', methods=['GET', 'POST'])
def admin():
    return("lez go")
