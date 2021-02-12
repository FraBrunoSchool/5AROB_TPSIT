from flask import Flask, render_template, request
from AlphaBot import AlphaBot


app = Flask(__name__)
alphabot = AlphaBot()
alphabot.stop()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        dir = request.form['direzione']
        print(f"post {dir}")
        switcher = {
            "forward": alphabot.forward,
            "backward": alphabot.backward,
            "right": alphabot.right,
            "left": alphabot.left,
            "stop": alphabot.stop
        }
        switcher[dir]()
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='192.168.0.42', debug='on')
