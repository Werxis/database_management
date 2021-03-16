from datetime import datetime
import hashlib, uuid
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import bcrypt

db = SQLAlchemy()

# class NoteModel(db.Model):
#     __tablename__ = "notes"

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(50), unique=True)
#     body = db.Column(db.Text, nullable=False)
#     last_update = db.Column(db.DateTime)

#     def __init__(self, title: str, body: str):
#         self.title = title
#         self.body = body
#         self.last_update = datetime.now()
    
#     def update(self, body: str):
#         self.body = body
#         self.last_update = datetime.now()
    
#     def json(self):
#         return {
#             "title": self.title,
#             "body": self.body,
#             "last_update": self.last_update
#         }

class UserModel(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    salted_password = db.Column(db.String(100), nullable=False)

    def __init__(self, username: str, password: str):
        self.username = username
        self.salted_password = get_salted_password(password)
    
    def check_password(self, password: str) -> bool:
        return compare_passwords(password, self.salted_password)
    
    def json(self):
        return {
            'username': self.username,
            'salted_password': self.salted_password
        }

def compare_passwords(password: str, salted_password: str) -> bool:
    return bcrypt.checkpw(password, salted_password)

def get_salted_password(password: str) -> str:
    return bcrypt.hashpw(password, bcrypt.gensalt(10) )
