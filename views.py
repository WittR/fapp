from flask import *
from . import modelbdd
import hashlib
from . import models


app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def index():
    listePromo = [i for i in range(200, 225)]
    return render_template('index.html', listePromo=listePromo)


@app.route('/contactform/contactform.php', methods=['POST'])
def contact():
    print("incroyable du cul !")
    data = request.form
    print(data)
    user = models.User(data.get('name'),data.get('firstname'))
    user.mail = data.get('mail')
    user.classeSup = data.get('classeSup')
    user.classeSpe = data.get('classeSpe')
    user.promo = data.get('promo')
    user.password = hashlib.sha1(str.encode(data.get('password'))).hexdigest()
    user.integration = data.get('integration')
    print(user)
    return modelbdd.inscriptionUser(user)


if __name__ == "__main__":
    app.run()
