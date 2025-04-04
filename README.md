# Proyecto de SASP:

## Descripción:
Crear una simulación de un huerto con herramientas avanzadas 

## División del proyecto:

- Algoritmo de riego automático
- Rutas automáticas 
- Ia de clasificación de enfermedades

## IA de clasificación del enfermedades:

## Finalidad:
Detección de las enfermedades de los tomates, pimientos y patatas

### **Estructura**  

#### **Peppers/** _(Pimientos)_  
- `Pepper__bell__Bacterial_spot` → Imágenes de pimientos afectados por la enfermedad "Bacterial Spot" (mancha bacteriana).  
- `Pepper__bell__healthy` → Imágenes de pimientos sanos.  

#### **Potatos/** _(Papas)_  
- `Potato__Early_blight` → Imágenes de papas con la enfermedad "Early Blight" (tizón temprano).  
- `Potato__healthy` → Imágenes de papas sin enfermedades.  
- `Potato__Late_blight` → Imágenes de papas afectadas por "Late Blight" (tizón tardío).  

#### **Tomatos/** _(Tomates)_  
- `Tomato__Target_Spot` → Tomates afectados por la enfermedad "Target Spot" (mancha diana).  
- `Tomato__Tomato_mosaic_virus` → Tomates infectados con el virus del mosaico del tomate.  
- `Tomato__Tomato_YellowLeaf__Curl_Virus` → Tomates afectados por el virus del rizado amarillo de la hoja del tomate.  
- `Tomato__Bacterial_spot` → Tomates con la enfermedad "Bacterial Spot" (mancha bacteriana).  
- `Tomato__Early_blight` → Tomates con la enfermedad "Early Blight" (tizón temprano).  
- `Tomato__healthy` → Tomates sin enfermedades.  
- `Tomato__Late_blight` → Tomates afectados por "Late Blight" (tizón tardío).  
- `Tomato__Leaf_Mold` → Tomates con la enfermedad "Leaf Mold" (moho de la hoja).  
- `Tomato__Septoria_leaf_spot` → Tomates con la enfermedad "Septoria Leaf Spot" (mancha foliar de Septoria).  
- `Tomato__Spider_mites_Two_spotted_spider_mite` → Tomates afectados por arañas rojas de dos manchas.  

### Códigos:

#### De entrenamiento

---

- ``pepper.py`` : se entrena a la red con las imágenes de pimientos
- ``potatos.py`` : se entrena a la red con las imágenes de patatas
- ``tomatos.py`` : se entrena a la red con las imágenes de tomates

---

#### Pesos _(out/pesos)_:

---

- ``Peppers.pth`` : pesos IA pimientos
- ``Potatos.pth`` : pesos IA patatas
- ``Tomatos.pth`` : pesos IA tomates

---

#### Resultados entrenamiento _(out/.)_:
- ``resTrainPepper.json`` : resultados del entrenamiento pimientos
- ``resTrainPotatos.json`` : resultados del entrenamiento patatas
- ``resTrainTomato.json`` : resultados del entrenamiento tomates

### Implementacion en el código principal:

