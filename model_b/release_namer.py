import random

from flask import Flask, render_template, redirect

from utils import ClueLogger

app = Flask(__name__)


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
def index():
    name = generate_name()
    return render_template('index.html', title='Home', name=name)


@app.route('/feedback/<model>/<feedback>/')
def collect_feedback(model, feedback):
    logger.out(model, feedback)
    return redirect("/", code=302)


@app.route('/healthcheck/')
def healthcheck():
    return "I'm okay"


if __name__ == '__main__':
    logger = ClueLogger(block='var_namer', model='model_b')
    app.run(host='0.0.0.0', port=5000)
