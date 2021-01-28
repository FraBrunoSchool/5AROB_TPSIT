import hashlib
import sqlite3

from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def validate(username, password):
    db_connection = sqlite3.connect('static/DB_Registrazione.db')
    db_cursor = db_connection.cursor()
    lista_iscritti = []
    for row in db_cursor.execute('SELECT * FROM Iscritti'): lista_iscritti.append((row[0], row[1]))
    print(lista_iscritti)
    for iscritto in lista_iscritti:
        if username == iscritto[0] and password == iscritto[1]:
            return True
    return False


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password = (hashlib.sha256(bytes(f"{password}", "utf-8"))).hexdigest()
        print(password)

        val_ok = validate(username, password)
        if not val_ok:
            error = "Credenziali non valide"
            print("qui")
        else:
            return redirect(url_for('secret'))
        print(f"username: {username}, password: {password}")

    return render_template('login.html', error=error)


def insert_user(username, password):
    print("insert user")
    db_connection = sqlite3.connect('static/DB_Registrazione.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f"INSERT INTO Iscritti VALUES ('{username}', '{password}')")
    return True


@app.route('/registrazione', methods=['GET', 'POST'])
def registrazione():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password = (hashlib.sha256(bytes(f"{password}", "utf-8"))).hexdigest()
        print(password)

        val_ok = insert_user(username, password)
        if not val_ok:
            error = "Credenziali non valide"
            print("qui")
        else:
            return redirect(url_for('secret'))
        print(f"username: {username}, password: {password}")

    return render_template('login.html', error=error)

@app.route('/secret')
def secret():
    return "This is a secret page!"


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug='on')
