import pymongo
import datetime
from . import models
from .views import app


def inscriptionUser(user):
    client = pymongo.MongoClient(app.config['DATABASE'])
    db = client.Faidherbe
    now = datetime.datetime.now()
    if db.User.find_one({"mail": user.mail}) is None:
        user = user.__dict__
        db.User.insert_one(user)
        return "Bravo le veau ! Casse-toi de mon obstacle !"
    else:
        return "Cette adresse mail a déjà un compte"
