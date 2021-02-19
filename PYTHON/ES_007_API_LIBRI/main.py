import flask
from flask import jsonify

books = [
    {'id': 0,
     'titolo': 'Il nome della Rosa',
     'autore': 'Umberto Eco',
     'anno_pubblicazione': '1980'
     },
    {'id': 1,
     'titolo': 'Il problema dei tre corpi',
     'autore': 'Liu Cixin',
     'anno_pubblicazione': '2008'
     },
    {'id': 2,
     'titolo': 'Fondazione',
     'autore': 'Isaac Asimov',
     'anno_pubblicazione': '1951'
     }
]

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Biblioteca online</h1><p>Prototipo di web API.</p>"


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)


if __name__ == '__main__':
    app.run()
