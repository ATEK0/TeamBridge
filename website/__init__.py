from flask import Flask, render_template
from flask_login import current_user

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO

from os import path
import json

from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()

def loadConfigsJson(file_path):
    with open(file_path, "r") as config_file:
        config = json.load(config_file)
    return config

def create_app():
    
    config = loadConfigsJson("config/configs.json")
    
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config["SECRET_KEY"]
    app.config['UPLOAD_FOLDER'] = f'C:\ISTEC\PROJETO FINAL\TESTES\webserver\\files'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc://@{config['DB_HOST']}\SQLEXPRESS/{config['DB_NAME']}?trusted_connection=yes&driver={config['DB_DRIVER']}" # para usar com SQLServer Local
    
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://<username>:<password>@<server>/hitsTest?driver=ODBC+Driver+17+for+SQL+Server' # para usar com SQLServer Online
    
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://<user>:<password>a@<servidor>:3306/<database>' # para usar com MySQL Online
    
        
    app.config['UPLOAD_FOLDER'] = './profiles'
    
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, async_mode='threading')
    
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
        return render_template('errors/error404.html', client=current_user, error=True, message="The page you are looking for doesn't exist."), 404
    
    #for db creation
    from .models.User import User
    from .models.Admins import Admins
    from .models.Company import Company
    from .models.Files import Files
    from .models.Note import Note
    from .models.Team import Team
    from .models.UserCompany import UserCompany
    from .models.CompanyInvites import CompanyInvites
    
    with app.app_context():
        db.create_all()
      
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

