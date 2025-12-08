import pandas as pd
import json

# Leer el archivo Excel
try:
    jugadores_df = pd.read_excel('jugadores.xlsx')
    print("Archivo Excel leído correctamente.")
except Exception as e:
    print(f"Error al leer el archivo Excel: {e}")
    exit()

# Limpiar y preparar los datos para JSON
# Convertimos los datos NaN (Not a Number) a cadenas vacías o a "NO" para que sea más fácil manejarlos en JS
jugadores_df = jugadores_df.fillna('')

# Convertimos el DataFrame de pandas a una lista de diccionarios
# Esto es lo que JSON entiende como un array de objetos
jugadores_json = jugadores_df.to_dict(orient='records')

# Guardar la lista de diccionarios en un archivo JSON
try:
    with open('jugadores.json', 'w', encoding='utf-8') as f:
        json.dump(jugadores_json, f, ensure_ascii=False, indent=4)
    print("Archivo 'jugadores.json' creado exitosamente.")
except Exception as e:
    print(f"Error al escribir el archivo JSON: {e}")
