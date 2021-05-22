import sqlite3

from flask import Flask, jsonify, request, render_template, session

# creo una nuova app di flask
app = Flask(__name__)


# decoratore che mi serve per definire una nuova url, accetto solo i metodi get
@app.route('/api/v1/resources/grandezza/id', methods=['GET'])
# funzione che verrà eseguita solo quando verrà chiamata la route
def grandezza_id():
    # controllo se l'utente passa come argomento 'nome_grandezza', senza non potrei eseguire il codice
    if 'nome_grandezza' in request.args:
        # salvo dentro ad una variabile il contenuto dell'argomento che mi viene mandato
        nome_grandezza = request.args['nome_grandezza']
        # mi connetto al db
        db_connection = sqlite3.connect('static/meteo_db.db')
        # credo un cursore con il quale spostarmi nel db
        db_cursor = db_connection.cursor()
        results = []
        # eseguo la mia query
        for row in db_cursor.execute(f'SELECT id_misura FROM grandezze WHERE grandezza_misurata = "{nome_grandezza}"'):
            results.append(row[0])
        # chiudo la connessione con il db
        db_connection.close()
        # rispondo inviando la risposta sotto forma di json
        return jsonify({"id_misurazione": results[0]})


# decoratore che mi serve per definire una nuova url, accetto solo i metodi get
@app.route('/api/v1/resources/stazione/id', methods=['GET'])
# funzione che verrà eseguita solo quando verrà chiamata la route
def stazione_id():
    # controllo se l'utente passa come argomento 'nome_stazione', senza non potrei eseguire il codice
    if 'nome_stazione' in request.args:
        # salvo dentro ad una variabile il contenuto dell'argomento che mi viene mandato
        nome_stazione = request.args['nome_stazione']
        # mi connetto al db
        db_connection = sqlite3.connect('static/meteo_db.db')
        # credo un cursore con il quale spostarmi nel db
        db_cursor = db_connection.cursor()
        results = []
        # eseguo la mia query
        for row in db_cursor.execute(f'SELECT id_stazione FROM stazioni WHERE nome = "{nome_stazione}"'):
            results.append(row[0])
        # chiudo la connessione con il db
        db_connection.close()
        # rispondo inviando la risposta sotto forma di json
        return jsonify({"id_stazione": results[0]})


# decoratore che mi serve per definire una nuova url, accetto solo i metodi get
@app.route('/api/v1/resources/inserimento', methods=['GET'])
# funzione che verrà eseguita solo quando verrà chiamata la route
def inserimento():
    # controllo se l'utente passa gli argomenti che mi servono, senza non potrei eseguire il codice
    if 'valore' in request.args and 'id_grandezza' in request.args and 'id_stazione' in request.args and 'data' in request.args:
        # salvo a delle variabili gli argomenti che mi ha mandato
        valore = request.args['valore']
        id_grandezza = request.args['id_grandezza']
        id_stazione = request.args['id_stazione']
        data = request.args['data']
        # mi connetto al db
        db_connection = sqlite3.connect('static/meteo_db.db')
        # credo un cursore con il quale spostarmi nel db
        db_cursor = db_connection.cursor()
        # eseguo la mia query che in questo caso è una insert
        db_cursor.execute(f"INSERT INTO misurazioni ('id_stazione', 'id_grandezza', "
                          f"'data_ora', 'valore') "
                          f"VALUES ('{int(id_stazione)}','{int(id_grandezza)}', "
                          f"'{data}','{float(valore)}')")
        # eseguo il commit, perchè se no la modifica che apporto al db non viene salvata
        db_cursor.execute(f"COMMIT;")
        # chiudo la connessione con il db
        db_connection.close()
        # rispondo inviando la risposta sotto forma di json, questo caso è solo un stringa di conferma
        return jsonify({"inserimento": "eseguito correttamente"})


# decoratore che mi serve per definire una nuova url, accetto solo i metodi get
@app.route('/api/v1/resources/valori', methods=['GET'])
# funzione che verrà eseguita solo quando verrà chiamata la route
def valori():
    # controllo se l'utente passa gli argomenti che mi servono, senza non potrei eseguire il codice
    if 'id_grandezza' in request.args and 'id_stazione' in request.args:
        # salvo a delle variabili gli argomenti che mi ha mandato
        id_grandezza = request.args['id_grandezza']
        id_stazione = request.args['id_stazione']
        # mi connetto al db
        db_connection = sqlite3.connect('static/meteo_db.db')
        # credo un cursore con il quale spostarmi nel db
        db_cursor = db_connection.cursor()
        results = []
        # eseguo la mia query
        for row in db_cursor.execute(f'SELECT avg(valore), max(valore), min(valore) FROM misurazioni '
                                     f'WHERE id_stazione = "{id_stazione}" AND id_grandezza = "{id_grandezza}"'):
            results.append({'avg': row[0], 'max': row[1], 'min': row[2]})
        # chiudo la connessione con il db
        db_connection.close()
        # rispondo inviando la risposta sotto forma di json
        return jsonify({"valori": results[0]})


if __name__ == '__main__':
    # avvio la mia app, con ip 127.0.01 e con la debug mode on che mi permette di non doverlo riavviare io ogni volta che apporto una modifica
    app.run(host='127.0.0.1', debug='on')
