# -------------------
# Badoino Matteo
# Bernardi Gianluca
# Bruno Francesco
# -------------------

import sqlite3
import flask
from flask import Flask, jsonify, request, render_template, session

app = Flask(__name__)
app.secret_key = 'verifica'

db_connection = sqlite3.connect('db.db')
db_cursor = db_connection.cursor()
lista_client_id = [row[0] for row in db_cursor.execute(f'SELECT DISTINCT idClient FROM Operazioni ')]
db_cursor.close()


@app.route('/server/inizializzazione', methods=['GET'])
def inizializzazione():
    print(lista_client_id)
    if 'msg' in request.args:
        msg = request.args['msg']
        if msg == 'start':
            session['client_id'] = lista_client_id.pop()
            session['lista_operazioni'] = letturaDBOperazione(session['client_id'])
            print(session['lista_operazioni'])
            print(lista_client_id)
            return jsonify(session['client_id'])


@app.route('/server/richiesta', methods=['GET'])
def richiesta():
    print(session['lista_operazioni'])
    if 'msg' in request.args:
        msg = request.args['msg']
        if msg == 'richiesta':
            try:
                operazione_attuale = session['lista_operazioni'].pop()
                session['id_oprazione_attuale'] = operazione_attuale['id']
                session['operazione_attuale'] = operazione_attuale['op']
                return jsonify([{'operazione': session['operazione_attuale']}])
                #return jsonify(session['operazione_attuale'])
            except:
                return jsonify([{'operazione': 'end'}])


@app.route('/server/risultato', methods=['GET'])
def risultato():
    if 'risultato' in request.args:
        risultato = request.args['risultato']
        scritturaDB(session['id_oprazione_attuale'], session['client_id'], risultato)
        return jsonify(f"Grazie {session['client_id']}")


# lettura operazioni da db
def letturaDBOperazione(numClient):
    operazioni = []
    db_connection = sqlite3.connect('db.db')
    db_cursor = db_connection.cursor()
    for row in db_cursor.execute(f'SELECT idOperazione, operazione FROM Operazioni '
                                 f'WHERE idClient=="{numClient}" and risultato ISNULL'):
        operazioni.append({'id': row[0], 'op': row[1]})
    db_cursor.close()
    return operazioni


def scritturaDB(id, idClient, risultato):
    db_connection = sqlite3.connect('db.db')
    db_cursor = db_connection.cursor()
    print(f"{id} | {idClient} | {risultato}")
    db_cursor.execute(
        f'UPDATE Operazioni SET risultato = "{risultato}" WHERE idOperazione="{id}" and idClient="{idClient}"')
    db_cursor.execute('COMMIT;')
    db_cursor.close()


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug='on')
