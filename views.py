from flask import *
from flask_login import LoginManager, login_user, login_required
import pymongo
from bson.json_util import dumps
import datetime

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
    return render_template('index.html', listePromo=listePromo)


@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/authtest/')
@login_required
def authtest():
    return render_template('index.html')


@app.route('/login/go/', methods=['POST'])
def check_login():
    if request.method == "POST" and "email" in request.form:
        user = User()
        user.mail = request.form["email"]
        user.set_password(request.form["password"])
        p= user.check_auth()
        user._id = p[1]
        if p[0] and user.is_active:
            # remember = request.form.get("remember", "no") == "yes"
            if login_user(user):
                flash("Logged in!")
                session['id'] = p[1]
                return "oui, bravo"
            else:
                flash("unable to log you in")

    return "NON CONNARD"


@app.route('/go/', methods=['POST'])
def inscription():
    data = request.form
    user = models.User()
    user.name = data.get('name')
    user.firstname = data.get('firstname')
    user.mail = data.get('mail')
    user.inscription = True
    user.set_password(data.get('password'))
    modelbdd.inscriptionUser(user)
    return "OK"


@app.route('/profil/complete/')
@login_required
def profil_complete():
    user = User.get_by_id(session['id'])
    if user.inscription == "validation":
        return redirect("/")
    listyears = [i for i in range(datetime.date.today().year, 1950, -1)]
    listClasseSup = ["MPSI1", "MPSI2", "Ma chère unité"]
    listClasseSpe = ["MP*", "MP2", "On y croit"]
    return render_template('profilcomplete.html', listyears=listyears, firstname=user.firstname, name=user.name,
                           listClasseSup=listClasseSup, listClasseSpe=listClasseSpe)


@app.route('/profil/complete/send/', methods=['POST'])
@login_required
def profil_complete_form():
    data = request.form
    user = User.get_by_id(session['id'])
    user.inscription = "validation"
    classes = []
    classesAValide = [data.get('class1')]
    if data.get('class2') != "":
        classesAValide.append(data.get('class2'))
    if data.get('class3') != "":
        classesAValide.append(data.get('class3'))
    prepa = {"start": data.get('anneeEntree'), "end": data.get('anneeSortie'), "classes":classes}
    user.prepa = prepa
    user.aValider = classesAValide
    db.User.update({"mail": user.mail}, user.__dict__)
    return "OK"


@app.route('/mod/validation/')
@login_required
def modPanel():
    user = User.get_by_id(session['id'])
    if (user.mod is None):
        return redirect("/")
    results = db.User.find({"inscription": "validation"})
    classes = {}
    for x in results:
        for y in x["aValider"]:
            if y in classes.keys():
                classes[y].append(x)
            else:
                l = []
                l.append(x)
                classes[y] = l
    keys = list(classes.keys())
    return render_template('modPanel.html', classes=user.mod, listValid=classes, classesKeys=keys)


@app.route('/mod/validate', methods=['POST'])
def mod_validate():
    data = request.form
    print(data)
    print(data.get('id'))
    print(User.get_by_id(id))
    return "oui"


@app.route('/mod/invalidate', methods=['POST'])
def mod_invalidate():
    data = request.form
    print(data.get('id'))
    print(User.get_by_id(id))
    return "non"


@app.route('/get/getecoles', methods=['GET'])
def get_ecoles():
    inputecole = ".*" + request.args.get('input') + '.*'
    inputecole = {"nom": {'$regex': inputecole, "$options": "i"}}
    results = db.Ecoles.find(inputecole).limit(10)
    listeecole = []
    for x in list(results):
        print(x)
        listeecole.append(x['nom'])
    return json.dumps({'status': 'OK', 'listecole': listeecole})


@loginManager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


if __name__ == "__main__":
    app.run()
