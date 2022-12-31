from flask import Blueprint

"""blueprints"""
views = Blueprint('views', __name__)
authn = Blueprint('authn', __name__)

"""import all files to make the app see them """
from flaskr.modules import routes, auth, events