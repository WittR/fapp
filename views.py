from flask import *
from flask_login import LoginManager, login_user, login_required
import pymongo
from bson.json_util import dumps
from bson import ObjectId
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
        p = user.check_auth()
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
    anneeEntree = int(data.get('anneeEntree'))
    classesAValider = {str(anneeEntree): data.get('class1')}
    if data.get('class2') != "":
        anneeEntree += 1
        classesAValider[str(anneeEntree)] = data.get('class2')
    if data.get('class3') != "":
        anneeEntree += 1
        classesAValider[str(anneeEntree)] = data.get('class3')
    if data.get('class4') != "":
        anneeEntree += 1
        classesAValider[str(anneeEntree)] = data.get('class4')
    user.aValider = classesAValider
    db.User.update({"mail": user.mail}, user.__dict__)
    return "OK"


@app.route('/mod/validation/')
@login_required
def modPanel():
    user = User.get_by_id(session['id'])
    if (user.mod is None):
        return redirect("/")
    query = []
    classesMod = []
    classes = {}
    for classe in user.mod:
        classesMod.append(classe)
        for annee in user.mod[classe]:
            results = db.User.find({"aValider." + annee: classe})
            classes[classe] = results
    keys = list(classes.keys())
    return render_template('modPanel.html', classes=classesMod, listValid=classes, classesKeys=keys)


@app.route('/mod/validate', methods=['POST'])
def mod_validate():
    modo = User.get_by_id(session['id'])
    data = request.form
    cible = User.get_by_id(data.get('id'))
    classe = data.get('classe')
    for annee in modo.mod[classe]:
        cible.aValider.pop(annee)
        if hasattr(cible, 'classes'):
            cible.classes[annee] = classe
        else:
            cible.classes = {annee: classe}
    print("Validation" + classe)
    print(cible.__dict__)
    print({"_id": cible.id})
    db.User.update({"_id": ObjectId(cible.id)}, cible.__dict__)
    redirect("/mod/validation/")
    return "oui"


@app.route('/mod/invalidate', methods=['POST'])
def mod_invalidate():
    modo = User.get_by_id(session['id'])
    data = request.form
    cible = User.get_by_id(data.get('id'))
    classe = data.get('classe')
    for annee in modo.mod[classe]:
        cible.aValider.pop(annee)
        if hasattr(cible, 'nonValide'):
            cible.nonValide[annee] = classe
        else:
            cible.nonValide = {annee: classe}
    print("nonValidation" + classe)
    print(cible.__dict__)

    return "non"


@app.route('/get/getecoles', methods=['GET'])
def get_ecoles():
    inputecole = ".*" + request.args.get('input') + '.*'
    inputecole = {"nom": {'$regex': inputecole, "$options": "i"}}
    results = db.Ecoles.find(inputecole).limit(10)
    listeecole = []
    for x in list(results):
        listeecole.append(x['nom'])
    return json.dumps({'status': 'OK', 'listecole': listeecole})


@loginManager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


if __name__ == "__main__":
    app.run()
