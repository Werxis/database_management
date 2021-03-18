from datetime import datetime
import hashlib, uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
import bcrypt

db = SQLAlchemy()

class NoteModel(db.Model):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True)
    body = Column(Text, nullable=False)
    last_update = Column(DateTime, unique=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("UserModel", back_populates="notes")

    def __init__(self, username: str, title: str, body: str):
        self.title = title
        self.body = body
        self.last_update = datetime.now()
    
    def update(self, body: str):
        self.body = body
        self.last_update = datetime.now()
    
    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "last_update": self.last_update
        }

class UserModel(UserMixin, db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    salted_password = Column(String(100), nullable=False)
    notes = relationship("NoteModel", back_populates="user")

    def __init__(self, username: str, password: str):
        self.username = username
        self.salted_password = get_salted_password(password)
    
    def check_password(self, password: str) -> bool:
        return compare_passwords(password, self.salted_password)
    
    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }

def compare_passwords(password: str, salted_password: str) -> bool:
    return bcrypt.checkpw(password, salted_password)

def get_salted_password(password: str) -> str:
    return bcrypt.hashpw(password, bcrypt.gensalt(10) )
