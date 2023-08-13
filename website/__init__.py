from flask import Flask, render_template
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from os import path

from werkzeug.security import generate_password_hash

from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'EIgKcwiAndmX3qL6sMDCVQABJOY12rGeQXsY9Ri9S9h41ivryU'
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    app.config['UPLOAD_FOLDER'] = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\\files'
        
    app.config['UPLOAD_FOLDER'] = './profiles'
    
    db.init_app(app)
    
    from .home import home
    from .administration import administration
    from .fileExplorer import fileExplorer
    from .auth import auth
    from .profilePage import profilePage
    from .dashboard import dashboard
    
    app.register_blueprint(home, url_prefix="/")
    app.register_blueprint(administration, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(profilePage, url_prefix="/")
    app.register_blueprint(fileExplorer, url_prefix="/")
    app.register_blueprint(dashboard, url_prefix="/")

    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('error.html', client=current_user, error=True, message="The page you are looking for doesn't exist."), 404
    
    
    from .models import User #ou entao posso usar import .models as models, especifiquei  nome pq n pode ter um . no inicio

    
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
        

