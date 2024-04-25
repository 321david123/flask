from flask import Flask, jsonify

app = Flask(__name__)

# Ruta para devolver un mensaje JSON
@app.route('/')
def hello():
    return jsonify({'mensaje': '¡Hola, mundo!'})

if __name__ == '__main__':
    app.run(debug=True)
