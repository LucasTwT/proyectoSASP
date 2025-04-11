from flask import Flask, render_template
import sys
from pathlib import Path
from principal import HuertoVirtual
import json
import datetime
from crear_grafos import crear_grafo

# Agrega la ruta del proyecto al PATH de Python
ruta_proyecto = Path(__file__).parent.parent  # Ajusta según tu estructura
sys.path.append(str(ruta_proyecto))

app = Flask(__name__)

@app.route('/')
def base_template():
    return render_template('home.html')


@app.route('/huerto')
def gestion_huerto():
    h = HuertoVirtual(10, 10, 'Data/imgsPlants')
    h.plantar()
    preds = h.preds_IA()
    preds_bool = h.pred2bool(preds)
    h.algoritmo_riego()
    data = carga_de_datos('Data/JSONsDatosRiego', (h.filas*h.columnas))
    estadisticas = stats(data, preds_bool)
    distancias = crear_grafo(preds_bool, preds, "static/imgs")
    return render_template('huerto.html', estadisticas=estadisticas, plantas=h)

def carga_de_datos(path, num):
    files = []
    for n in range(1, num):
        with open(f'{path}/dataRiego{n}.json') as f:
            files.append(json.load(f))
    return files

def stats(files: list, pred_bool: list) -> dict:
    estadisticas = {
            'Dia': datetime.datetime.now().date(),
            'temperatura_media': 0,
            'humedad_media': 0,
            'lluvia_1h': "",
            'alerta_meteo': "",
            'Temperatura_MAX': 0,
            'Temperatura_MIN': 0,
            'Humedad_MAX': 0,
            'Humedad_MIN': 0,
            'Número_plantas_enfermas': 0,
    }
    humedades = []
    temperaturas = []
    num = 0
    for filas in pred_bool:
        for columnas in filas:
            num += columnas
    for file in files:
        humedades.append(file['parametros']['humedad_suelo'])
        temperaturas.append(file['parametros']['temperatura'])
    estadisticas['lluvia_1h'] = "hay lluvia 🌧️" if  files[0]['parametros']['lluvia_1h'] == True  else "No hay lluvia ☀️"
    estadisticas['alerta_meteo'] = "ALERTA METEOROLÓGICA ⏰" if  files[0]['alerta_meteorologica'] == True  else "No hay alerta 😀"
    estadisticas['humedad_media'] = str(sum(humedades) / len(files)) + '%'
    estadisticas['temperatura_media'] = str(sum(temperaturas) / len(files)) + "°C"
    estadisticas['Temperatura_MAX'] = str(max(temperaturas)) + "°C"
    estadisticas['Temperatura_MIN'] = str(min(temperaturas)) + "°C"
    estadisticas['Humedad_MAX'] = str(max(humedades))  + '%'
    estadisticas['Humedad_MIN'] = str(min(humedades))  + '%'
    if num > 5:
        estadisticas['Número_plantas_enfermas'] = f'{num} 💀'
    elif num > 3:
        estadisticas['Número_plantas_enfermas'] = f'{num} 🤒'
    elif num > 1:
        estadisticas['Número_plantas_enfermas'] = f'{num} 😷'
    else:
        estadisticas['Número_plantas_enfermas'] = f'{num} 😀'
    return estadisticas

if __name__ == '__main__':
    app.run(debug=True)