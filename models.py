# models.py
import pymongo
from .views import app, db
from flask_login import LoginManager, UserMixin
import hashlib


class User(UserMixin):

    def __init__(self):
        self.name = "Random"

    def check_auth(self):
        check = {'mail': self.mail, 'password': self.password}
        print(check)
        i = db.User.find_one(check)
        print(i)
        print(i is not None)
        return i is not None

    @staticmethod
    def get_by_id(id):
        dbUser = db.User.find_one({"mail": id})
        if dbUser is not None:
            user = User()
            user.mail = dbUser['mail']
            user.id = user.mail
            return user
        else:
            return None

    def get_id(self):
        return self.mail

    def set_password(self, password):
        self.password = hashlib.sha512(password.encode()).hexdigest()
