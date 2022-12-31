from flaskr import db

from flask_login import UserMixin
from sqlalchemy.sql import func

"""Model/Table for chat application"""
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

    def __repr__(self):
        return f"User: ¨{self.email}"