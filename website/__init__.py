from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'EIgKcwiAndmX3qL6sMDCVQABJOY12rGeQXsY9Ri9S9h41ivryU'
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    app.config['UPLOAD_FOLDER'] = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\\files'
    app.config['MAX_CONTENT_PATH'] = 1096
    # app.config['SERVER_NAME'] = "pigcenter.local"
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    from .models import User, Note #ou entao posso usar import .models as models, especifiquei  nome pq n pode ter um . no inicio
    
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Database Created")
