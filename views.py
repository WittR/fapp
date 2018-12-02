from flask import *
from flask_login import LoginManager, login_user, login_required
import pymongo
from bson.json_util import dumps

app = Flask(__name__)
app.config.from_object('config')
loginManager = LoginManager(app)
client = pymongo.MongoClient(app.config['DATABASE'])
db = client.Faidherbe

from . import modelbdd, models
from .models import User


@app.route('/')
def index():
    listePromo = [i for i in range(200, 225)]
    return render_template('inscription.html', listePromo=listePromo)


@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/authtest/')
@login_required
def authtest():
    return render_template('authtest.html')


@app.route('/login/go/', methods=['POST'])
def check_login():
    if request.method == "POST" and "email" in request.form:
        user = User()
        user.mail = request.form["email"]
        user.set_password(request.form["password"])
        if user.check_auth() and user.is_active:
            # remember = request.form.get("remember", "no") == "yes"
            if login_user(user):
                flash("Logged in!")
                return "oui, bravo"
            else:
                flash("unable to log you in")

    return "NON CONNARD"


@app.route('/go/', methods=['POST'])
def inscription():
    print("incroyable du cul !")
    data = request.form
    print(data)
    user = models.User()
    user.name = data.get('name')
    user.prenom = data.get('firstname')
    user.mail = data.get('mail')
    user.classeSup = data.get('classeSup')
    user.classeSpe = data.get('classeSpe')
    user.promo = data.get('promo')
    user.set_password(data.get('password'))
    user.integration = data.get('integration')
    print(user)
    return modelbdd.inscriptionUser(user)


@app.route('/get/getecoles', methods=['GET'])
def get_ecoles():
    inputecole = ".*" + request.args.get('input') +'.*'
    print(inputecole)
    inputecole = {"nom": {'$regex': inputecole,"$options": "i"}}
    print(inputecole)
    results = db.Ecoles.find(inputecole).limit(10)
    listeecole = []
    for x in list(results):
        listeecole.append(x['nom'])
    return json.dumps({'status': 'OK', 'listecole': listeecole})


@loginManager.user_loader
def load_user(user_id):
    print(user_id)
    return User.get_by_id(user_id)


if __name__ == "__main__":
    app.run()
