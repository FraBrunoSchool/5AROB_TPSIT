"""
    Bruno Francesco,
    Classe: 5A Rob,
    Data: 23/02/2021
    Url: http://127.0.0.1:5000/
"""
from flask import Flask, render_template, request
import semaforo
import sqlite3
import datetime

app = Flask(__name__)
s = semaforo.semaforo()

# tempi default messi ad 1
tempi = {
    'verde': 1,
    'rosso': 1,
    'giallo': 1
}
# appena acceso è sempre attivo di default
STATO = "ATTIVO"  # "SPENTO"


# con 'type="number"' nel file index.html limito l'imput ai soli numeri, in modo da non avere altri input

# con 'value="1"' nel file index.html imposto l'input di testo di defaul a 1
# in modo che prevengo errori nello script di py

@app.route('/', methods=['GET', 'POST'])
def index():
    global STATO
    app.logger.info("Pagina richiesta dal client")
    if request.method == 'POST':
        app.logger.info("POST effettuata dal client")
        comando = request.form['comando']
        app.logger.info(f"E' stato dato il comando: {comando}")
        tempo = request.form['valore']
        if comando == "rosso":
            # controllo che il valore sia maggiore o uguale ad uno, meno non avrebbe senso
            if int(tempo) >= 1: tempi['rosso'] = int(tempo)
        if comando == "verde":
            # controllo che il valore sia maggiore o uguale ad uno, meno non avrebbe senso
            if int(tempo) >= 1: tempi['verde'] = int(tempo)
        if comando == "giallo":
            # controllo che il valore sia maggiore o uguale ad uno, meno non avrebbe senso
            if int(tempo) >= 1: tempi['giallo'] = int(tempo)
        app.logger.info(f"Imposto {comando} a {tempo}")
        # esegue solo se attivo
        if comando == "spento" and STATO == "ATTIVO":
            STATO = "SPENTO"
            app.logger.info("Spengo il semaforo e lo scrivo sul db")
            database("SPENTO")
        # esegue solo se spento
        if comando == "riattiva" and STATO == "SPENTO":
            STATO = "ATTIVO"
            app.logger.info(f"Riattivo il semaforo e lo scrivo sul db")
            database("ATTIVO")

    if STATO == "ATTIVO":
        app.logger.info(f"Semaforo Acceso")
        s.verde(tempi['verde'])
        s.giallo(tempi['giallo'])
        s.rosso(tempi['rosso'])

    if STATO == "SPENTO":
        app.logger.info(f"Semaforo Spento")
        for _ in range(3):
            s.giallo(1)
            s.luci_spente(1)

    return render_template('index.html')


def database(tipo_operazione):
    app.logger.info(f"Mi connetto al db")
    db_connection = sqlite3.connect('static/db_operazioni.db')
    app.logger.info(f"Connessione avvenuta")
    db_cursor = db_connection.cursor()
    data = f"{datetime.datetime.now()}"
    app.logger.info(
        f"Eseguo sul db: INSERT INTO operazioni('tipo_operazione', 'data') VALUES ('{tipo_operazione}', '{data}')")
    db_cursor.execute(f"INSERT INTO operazioni('tipo_operazione', 'data') VALUES ('{tipo_operazione}', '{data}')")
    app.logger.info(f"Eseguo sul db: COMMIT;")
    db_cursor.execute("COMMIT;")
    db_cursor.close()
    app.logger.info(f"Chiudo il db")


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug='on')
