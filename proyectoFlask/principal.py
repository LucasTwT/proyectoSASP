import random
import os
import torch
import albumentations as A
import cv2
from albumentations.pytorch import ToTensorV2
from torchvision import models
import  torch.nn as nn
from  algoritmoRiego import *
import numpy as np

if torch.cuda.is_available():
    device = 'cuda'
else:
    device = 'cpu'

def configuracion_modelo(model: models.resnet18, out_features: int):
    for param in model.parameters():
        param.require_grad = False
    in_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Linear(in_features, out_features),
    )
    return model

transform = A.Compose([
    A.Resize(224, 224),
    A.RandomCrop(width=150, height=200),
    A.Rotate(limit=40, p=0.5, border_mode=cv2.BORDER_CONSTANT),
    A.HorizontalFlip(p=0.6),
    A.VerticalFlip(p=0.3),
    A.RGBShift(r_shift_limit=25, g_shift_limit=25, b_shift_limit=25, p=0.3),
    A.Normalize(mean=[0, 0, 0], std=[1, 1, 1]),
    ToTensorV2(),
])

class HuertoVirtual:
    def __init__(self, filas, columnas, img_path):
        self.filas = filas
        self.columnas = columnas
        self.huerto = [[None for _ in range(columnas)] for _ in range(filas)]
        self.img_path = img_path
        self.plantas_disponibles = [
            {"tipo": "Tomatos", "requerimientos": {'humedad': 92, 'temperatura': 25}, "clases": 10},
            {"tipo": "Peppers", "requerimientos": {'humedad': 92, 'temperatura': 25}, "clases": 2},
            {"tipo": "Potatos", "requerimientos": {'humedad': 75, 'temperatura': 25}, "clases": 3}
        ]
        self.TIPO_PLANTA_CODIGO = {"Tomatos": 0, "Peppers": 1, "Potatos": 2}
        self.modelos = self.cargar_modelos()
        
        self.salidas = {
            0: {  # Tomates
                0: 'mancha diana',
                1: 'virus del mosaico del tomate',
                2: 'virus del rizado amarillo de la hoja del tomate',
                3: 'mancha bacteriana',
                4: 'tizón temprano',
                #5: 'sano',
                6: 'tizón tardío',
                7: 'moho de la hoja',
                8: 'mancha foliar de Septoria',
                9: 'ácaros rojos de dos manchas'
            },
            1: {  # Pimientos
                0: 'mancha bacteriana',
                #1: 'sano'
            },
            2: {  # Papas
                0: 'tizón temprano',
                #1: 'sano',
                2: 'tizón tardío'
            }
        }

    def cargar_modelos(self):
        modelos = {}
        for planta in self.plantas_disponibles:
            modelo = models.resnet18(weights=None)
            modelo = configuracion_modelo(modelo, planta["clases"])  # Ajustar número de clases según la planta
            modelo.load_state_dict(torch.load(f'out/pesos/{planta["tipo"]}.pth', map_location=device))
            modelo.to(device)
            modelo.eval()
            modelos[planta["tipo"]] = modelo
        return modelos
    
    def procesar_imagen(self, img_path):
        imagen = cv2.imread(img_path)
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        imagen = transform(image=imagen)['image']
        return imagen.unsqueeze(0).to(device)
    
    def plantar(self):
        # Llena el huerto con plantas aleatoria.
        for i in range(self.filas):
            for j in range(self.columnas):
                planta = random.choice(self.plantas_disponibles)
                self.huerto[i][j] = {
                    "tipo": planta["tipo"],
                    "requerimientos": planta["requerimientos"],
                    "coordenadas": (i, j),
                    "sensor": self.obtener_datos_sensor_suelo(),
                    "foto":  self.obtencion_img(planta["tipo"], self.img_path)
                }
                
    def preds_IA(self):
        preds = []
        for i in range(self.filas):
            fila_pred = []
            for j in range(self.columnas):
                planta = self.huerto[i][j]
                if planta and planta["foto"] != "Imagen no encontrada":
                    imagen = self.procesar_imagen(planta["foto"])
                    modelo = self.modelos.get(planta["tipo"])
                    if modelo:
                        with torch.no_grad():
                            output = modelo(imagen)
                            prediccion = torch.argmax(output, dim=1).item()
                            tipo_codificado = self.TIPO_PLANTA_CODIGO.get(planta["tipo"], -1)
                            fila_pred.append([tipo_codificado, prediccion])
                        continue
                # Si no hay imagen o modelo, metemos valores por defecto
                fila_pred.append([-1, -1])
            preds.append(fila_pred)
        self.predicciones = preds
        return preds


    
    def mostrar_huerto(self):
        """Muestra el huerto en forma de matriz."""
        for fila in self.huerto:
            print([p["tipo"] for p in fila])
            
    def obtener_planta(self, x, y):
        """Obtiene la información de una planta en (x, y)."""
        if 0 <= x < self.filas and 0 <= y < self.columnas:
            return self.huerto[x][y]
        else:
            return "Coordenadas fuera de rango."
    
    def obtencion_img(self, tipo_planta, path):
            """Devuelve una imagen aleatoria del tipo de planta especificado."""
            categoria_path = os.path.join(path, tipo_planta)
            
            if not os.path.exists(categoria_path):
                return "Imagen no encontrada"
            imagenes = [img for img in os.listdir(categoria_path) if img.endswith('.JPG')]
            
            if imagenes:
                return os.path.join(categoria_path, random.choice(imagenes))
            
            return "Imagen no encontrada"
        
    def __getitem__(self, indices):
        i, j = indices  # Desempaquetar la tupla de índices
        if 0 <= i < self.filas and 0 <= j < self.columnas:
            return self.huerto[i][j]
        else:
            raise IndexError("Coordenadas fuera de rango.")

    def obtener_datos_sensor_suelo(self):
        return {"humedad": random.randint(45, 100), "temperatura": random.randint(15, 35)}
    
    def algoritmo_riego(self):
        cont = 0
        for i in range(self.filas):
            for j in range(self.columnas):
                cont+=1
                datos_sensor = self.huerto[i][j]['sensor']
                decision, razones = calcular_riego(datos_sensor['humedad'], datos_sensor['temperatura'], lluvia_1h , esta_lloviendo)
                exportar_json(decision, razones, datos_sensor['temperatura'], datos_sensor['humedad'], 'Data/JSONsDatosRiego', cont)
    
    
    def pred2bool(self, pred: list) -> list:
        criterio_bueno = {
            1: 1,
            2: 1,
            0: 5
        }
        resultado = []
        for fila in pred:
            fila_bool = []
            for tipo, enf in fila:
                fila_bool.append(enf != criterio_bueno.get(tipo, None))
            resultado.append(fila_bool)
        return resultado