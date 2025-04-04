from flask import Flask, render_template

import sys
from pathlib import Path
from principal import HuertoVirtual
# Agrega la ruta del proyecto al PATH de Python
ruta_proyecto = Path(__file__).parent.parent  # Ajusta según tu estructura
sys.path.append(str(ruta_proyecto))

app = Flask(__name__)

@app.route('/')
def hola_mundo():
    return "Hola mundo"

@app.route('/predicciones')
def hola_template():
    huerto = HuertoVirtual(3, 3, 'Data')
    huerto.plantar()
    huerto.mostrar_huerto()
    predicciones = huerto.preds_IA()
    return render_template('index.html', predicciones=predicciones)

if __name__ == '__main__':
    app.run(debug=True)