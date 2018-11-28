import pymongo
import datetime
from . import models
import config


def inscriptionUser(user):
    client = pymongo.MongoClient(config.DATABASE)
    db = client.Faidherbe
    now = datetime.datetime.now()
    print("mail :" + str(user.mail))
    if db.User.find_one({"mail": user.mail}) is None:
        user = user.__dict__
        print(user)
        db.User.insert_one(user)
        return "Bravo le veau ! Casse-toi de mon obstacle !"
    else:
        return "Cette adresse mail a déjà un compte"
