# models.py
import pymongo
from .views import app, db
from flask_login import LoginManager, UserMixin
import hashlib
from bson import json_util, ObjectId
from bson.json_util import dumps


class User(UserMixin):

    def __init__(self):
        pass

    def check_auth(self):
        check = {'mail': self.mail, 'password': self.password}
        i = db.User.find_one(check)
        exist = i is not None
        if exist:
            id = i['_id']
            return (exist, str(id))
        else:
            return (exist,0)

    # Not used ?
    @staticmethod
    def get_by_mail(id):
        dbUser = db.User.find_one({"mail": id})
        if dbUser is not None:
            user = User()
            user.__dict__ = dbUser
            user.id = str(user._id)
            return user
        else:
            return None

    @staticmethod
    def get_by_id(id):
        print("'" + str(id) + "'")
        dbUser = db.User.find_one({"_id": ObjectId(id)})
        print(dbUser is not None)
        if dbUser is not None:
            user = User()
            user.__dict__ = dbUser
            user.id = str(user._id)
            print(user._id)
            return user
        else:
            return None

    def get_id(self):
        print("get id :" + self._id)
        return str(self._id)

    def set_password(self, password):
        self.password = hashlib.sha512(password.encode()).hexdigest()
