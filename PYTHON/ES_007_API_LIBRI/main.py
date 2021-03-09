import sqlite3
import flask
from flask import jsonify, request

app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Biblioteca online</h1><p>Prototipo di web API.</p>"


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    db_connection = sqlite3.connect('static/DB_Libreria.db')
    db_cursor = db_connection.cursor()
    results = []
    for row in db_cursor.execute(f'SELECT * FROM Books'):
        results.append({'id': row[0], 'titolo': row[1], 'autore': row[2], 'anno_pubblicazione': row[3]})
    db_connection.close()
    return jsonify(results)


@app.route('/api/v1/resources/books/id', methods=['GET'])
def api_id():
    print(request.args)
    if 'id' in request.args:
        id_libro = int(request.args['id'])
        db_connection = sqlite3.connect('static/DB_Libreria.db')
        db_cursor = db_connection.cursor()
        results = []
        for row in db_cursor.execute(f'SELECT * FROM Books WHERE id = {id_libro}'):
            results.append({'id': row[0], 'titolo': row[1], 'autore': row[2], 'anno_pubblicazione': row[3]})
        db_connection.close()
        return jsonify(results)
    else:
        print("Error: No id or title field provided. Please specify an id or a tile.")
        return "http://127.0.0.1:5000/api/v1/resources/books/id?id=... per riceve informazioni su quel libro"


@app.route('/api/v1/resources/books/title', methods=['GET'])
def api_title():
    print(request.args)
    if 'title' in request.args:
        titolo_libro = request.args['title']
        db_connection = sqlite3.connect('static/DB_Libreria.db')
        db_cursor = db_connection.cursor()
        results = []
        for row in db_cursor.execute(f'SELECT * FROM Books WHERE titolo = "{titolo_libro}"'):
            results.append({'id': row[0], 'titolo': row[1], 'autore': row[2], 'anno_pubblicazione': row[3]})
        db_connection.close()
        return jsonify(results)
    else:
        print("Error: No id or title field provided. Please specify an id or a tile.")
        return "http://127.0.0.1:5000/api/v1/resources/books/title?title=... per riceve informazioni su quel libro"


@app.route('/api/v1/resources/books/author', methods=['GET'])
def api_author():
    print(request.args)
    if 'author' in request.args:
        autore_libro = request.args['author']
        db_connection = sqlite3.connect('static/DB_Libreria.db')
        db_cursor = db_connection.cursor()
        results = []
        for row in db_cursor.execute(f'SELECT * FROM Books WHERE autore = "{autore_libro}"'):
            results.append({'id': row[0], 'titolo': row[1], 'autore': row[2], 'anno_pubblicazione': row[3]})
        db_connection.close()
        return jsonify(results)
    else:
        print("Error: No id or title field provided. Please specify an id or a tile.")
        return "http://127.0.0.1:5000/api/v1/resources/books/author?author=... per riceve informazioni su quel libro"


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug='on')
