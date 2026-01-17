from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from base import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)

    email = db.Column(db.String(200), unique=True, nullable=False)
    username = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)

    friends = relationship("Friend", back_populates="user")

    def to_string(self) -> str:
        return f'ID:{self.id}\nEmail:{self.email}\nUsername:{self.username}'


class Friend(db.Model):
    __tablename__ = 'friends'
    # NON NULLABLE ATTRIBUTES
    id = db.Column(db.Integer, primary_key=True , autoincrement = True)
    name = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(200), nullable=False)

    # NULLABLE ATTRIBUTES
    age = db.Column(db.Integer(), nullable = True)
    note = db.Column(db.String(1024) , nullable = True)

    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable = False)
    user = relationship("User", back_populates="friends")

    created_at = db.Column(db.DateTime, default=db.func.now())

    #EXPORTING THE INFORMATION 

    def to_string(self) -> str:
        return f'ID:{self.id}\nName:{self.name}\nCountry:{self.country}\nAge:{self.age}\nNote:{self.note}\nUser_id:{self.id}'
