import logging
import logging.handlers
import time
import random
from flask import Flask, render_template, redirect
app = Flask(__name__)


feedback_logger = logging.getLogger('stats for bandits')
feedback_logger.setLevel('INFO')
feedback_logger.addHandler(logging.handlers.RotatingFileHandler('../data/likes.tsv',
                                                                maxBytes=5000,
                                                                backupCount=3))

letters = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Digamma', 'Zeta', 'Eta',
           'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Xi', 'Omicron', 'Pi',
           'San', 'Koppa', 'Rho', 'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega',]

planets = ['Ceres', 'Pallas', 'Juno', 'Vesta', 'Astraea', 'Hebe', 'Iris', 'Flora', 'Metis', 'Hygiea',
           'Parthenope', 'Victoria', 'Egeria', 'Irene', 'Eunomia', 'Psyche', 'Thetis', 'Melpomene',
           'Fortuna', 'Massalia', 'Lutetia', 'Kalliope', 'Thalia', 'Themis', 'Phocaea', 'Proserpina',
           'Euterpe', 'Bellona', 'Amphitrite', 'Urania', 'Euphrosyne', 'Pomona', 'Polyhymnia', 'Circe',
           'Leukothea', 'Atalante', 'Fides', 'Leda', 'Laetitia', 'Harmonia', 'Daphne', 'Isis', 'Ariadne',
           'Nysa', 'Eugenia', 'Hestia', 'Aglaja', 'Doris', 'Pales', 'Virginia', 'Nemausa', 'Europa', 'Kalypso',
           'Alexandra', 'Pandora', 'Melete', 'Mnemosyne', 'Concordia', 'Elpis', 'Echo', 'Danaë', 'Erato',
           'Ausonia', 'Angelina', 'Cybele', 'Maja', 'Asia', 'Leto', 'Hesperia', 'Panopaea', 'Niobe', 'Feronia',
           'Klytia', 'Galatea', 'Eurydike', 'Freia', 'Frigga', 'Diana', 'Eurynome', 'Sappho', 'Terpsichore',
           'Alkmene', 'Beatrix', 'Klio']


def generate_name():
    letter = random.choice(letters)
    planet = random.choice(planets)
    return f'{letter}_{planet}'.lower()


@app.route('/')
def hello_world():
    name = generate_name()
    return render_template('index.html', title='Home', name=name)


@app.route('/like')
def like():
    feedback_logger.info(f'{time.time()}\tmodel_b\tlike')
    return redirect("/", code=302)


@app.route('/retry')
def retry():
    feedback_logger.info(f'{time.time()}\tmodel_b\tdislike')
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
