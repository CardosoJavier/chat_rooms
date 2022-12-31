from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from flask_socketio import SocketIO

""" database settings """
db = SQLAlchemy()
DB_NAME = 'CR.db'

""" socket settings """
socketio = SocketIO()

def create_app():

    """ app settings """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mySecret!'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    """ init app """
    socketio.init_app(app)
    db.init_app(app)

    """ add blueprintd to app """
    from flaskr.modules import views as view_bp
    from flaskr.modules import authn as authn_bp

    app.register_blueprint(view_bp)
    app.register_blueprint(authn_bp)
    
    """ database settings """
    with app.app_context():
        db.create_all()

    from flaskr.models import User
    
    """ login manager settings """
    login_manager = LoginManager()

    # if user not login, redirect to login page
    login_manager.login_view = 'authn.login'

    # init login manager
    login_manager.init_app(app)

    """ stores user id in a session. It will get the id from the database
    using the id passed as argument"""
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app
