import logging.handlers
import random
import time

from flask import Flask, render_template, redirect

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


feedback_logger = logging.getLogger('stats for bandits')
feedback_logger.setLevel('INFO')
feedback_logger.addHandler(logging.handlers.RotatingFileHandler('../data/likes.tsv',
                                                                maxBytes=5 * 10**6,
                                                                backupCount=1))


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
    feedback_logger.info(f'{time.time()}\t{model}\t{feedback}')
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
