import json
import requests

api_key = "3d208747e3095b645933ba83d8156fed"
lat = 40.119646
lon = -3.664446

url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"

respuesta = requests.get(url)
data_clima = respuesta.json()

with open("clima.json", "w") as archivo:
    json.dump(data_clima, archivo)


def calcular_riego(humedad, temp, lluvia_1h, esta_lloviendo):
    # Parámetros técnicos según FAO para riego agrícola
    UMBRALES = {
        'humedad_critica': 25,  # % HR suelos arcillosos
        'temp_alerta': 30,       # °C para incrementar requerimiento
        'lluvia_minima': 5       # mm/m² en última hora
    }
    
    razones = []
    regar = False
    
    # 1. Verificar lluvia actual
    if esta_lloviendo:
        razones.append("Precipitación en curso")
        return False, razones
    
    # 2. Ajustar humedad crítica por temperatura
    humedad_ajustada = UMBRALES['humedad_critica']
    if temp > UMBRALES['temp_alerta']:
        humedad_ajustada += 5
        razones.append(f"Temperatura elevada ({temp}°C)")
    
    # 3. Lógica principal de riego
    if humedad < humedad_ajustada:
        razones.append(f"Humedad del suelo crítica ({humedad}%)")
        regar = True
    
    # 4. Considerar lluvia reciente
    if lluvia_1h >= UMBRALES['lluvia_minima']:
        razones.append(f"Lluvia reciente ({lluvia_1h}mm/m²)")
        regar = False
    
    # 5. Seguridad contra exceso de agua
    if humedad > 80:
        razones.append("Suelo sobresaturado")
        regar = False
    
    return regar, razones

# Cargar datos
with open('clima.json', 'r') as f:
    datos = json.load(f)

# Extraer variables
esta_lloviendo = datos.get('weather', [{}])[0].get('main') == 'Rain'
humedad = datos.get('main', {}).get('humidity', 0)
temp = datos.get('main', {}).get('temp', 20)
lluvia_1h = datos.get('rain', {}).get('1h', 0)

# # Calcular decisión
# decision, razones = calcular_riego(humedad, temp, lluvia_1h, esta_lloviendo)

# Generar output
def exportar_json(decision, razones):
    resultado = {
        "riego_requerido": decision,
        "parametros": {
            "humedad_suelo": humedad,
            "temperatura": temp,
            "lluvia_1h": lluvia_1h
        },
        "razones": razones,
        "alerta_meteorologica": esta_lloviendo
    }
    with open('data.json', 'w') as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)