from flask import Flask, render_template_string
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)

# Configura tu conexión a la base de datos
DATABASE_URL = "postgresql://rojita_sub_18_user:zpdx3RKqcQKRRKf1RhgMLPUxNYJmbLBY@dpg-ct8a08t2ng1s73aell30-a:5432/rojita_sub_18"

# Crear el motor de conexión
engine = create_engine(DATABASE_URL)

# Función para cargar los datos desde la base de datos
def cargar_datos():
    try:
        # Consulta a la base de datos para obtener los datos de los jugadores
        query = "SELECT * FROM jugadores"
        jugadores_df = pd.read_sql(query, engine)

        # Verificar si los datos se cargaron correctamente
        print(jugadores_df.columns)

        # Verificar y procesar las rutas de las fotos
        jugadores_df['Foto'] = jugadores_df['Nombre completo'].apply(lambda x: buscar_imagen(x))

        return jugadores_df
    except Exception as e:
        print(f"Error al cargar los datos de la base de datos: {e}")
        return pd.DataFrame()  # Retorna un DataFrame vacío en caso de error

# Función para buscar las imágenes de los jugadores
def buscar_imagen(nombre_jugador):
    imagen_path = f'static/fotos/{nombre_jugador}.png'
    if os.path.exists(imagen_path):
        return imagen_path
    else:
        return 'static/fotos/default-player.png'

# Ruta principal de la aplicación
@app.route('/')
def home():
    # Cargar los datos desde la base de datos
    jugadores_df = cargar_datos()

    # Verificar si el DataFrame está vacío
    if jugadores_df.empty:
        return "Error al cargar los datos de la base de datos"

    # Crear el HTML para mostrar los jugadores
    html_template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Selección Colonia Interior Sub 18</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f8f9fa;
            }
            header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 20px;
            }
            img.logo {
                width: 113px; 
                height: 113px;
            }
            h1 {
                text-align: center;
                flex-grow: 1;
                color: red;
                font-size: 24px;
                margin: 0;
            }
            #searchBar {
                width: 100%;
                padding: 10px;
                margin-bottom: 20px;
                font-size: 16px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            .player-card {
                background-color: #fff;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                margin: 10px 0;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .player-card img {
                width: 70px;
                height: 70px;
                border-radius: 50%;
                margin-right: 20px;
            }
            .player-info {
                flex-grow: 1;
            }
            .details {
                display: none;
                margin-top: 10px;
                background-color: #f9f9f9;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            button {
                background-color: #FF0000;
                color: white;
                border: none;
                padding: 8px 12px;
                cursor: pointer;
                border-radius: 4px;
            }
            button:hover {
                background-color: #cc0000;
            }
        </style>
    </head>
    <body>
    <header>
        <img src="static/logo.png" alt="Logo Federación" class="logo">
        <h1>SELECCIÓN COLONIA INTERIOR SUB 18</h1>
    </header>

    <input type="text" id="searchBar" onkeyup="searchPlayer()" placeholder="Buscar jugador..." />

    <div id="playerList">
        {% for index, player in jugadores.iterrows() %}
        <div class="player-card">
            <div class="player-info">
                <strong>{{ player['Nombre completo'] }}</strong><br>
                <small>Cédula: {{ player['Cédula'] }} | Fecha de nacimiento: {{ player['Fecha de nacimiento'] }} | Celular: {{ player['Celular'] }}</small>
            </div>
            <img src="{{ player['Foto'] }}" alt="{{ player['Nombre completo'] }}">
            <button onclick="toggleDetails({{ index }})">Ver detalles</button>
        </div>

        <div class="details" id="details-{{ index }}">
            <p><strong>Fecha de nacimiento:</strong> {{ player['Fecha de nacimiento'] }}</p>
            <p><strong>Celular:</strong> {{ player['Celular'] }}</p>
            <p><strong>Altura:</strong> {{ player['Altura (cm)'] }} cm</p>
            <p><strong>Peso:</strong> {{ player['Peso (kg)'] }} kg</p>
            <p><strong>Sanatorio:</strong> {{ player['Sanatorio'] }}</p>
            <p><strong>Grupo sanguíneo:</strong> {{ player['Grupo sanguíneo'] }}</p>
            <p><strong>Enfermedades previas:</strong> {{ player['Enfermedades previas'] }}</p>
            <p><strong>Alergias:</strong> {{ player['Alergias'] }}</p>
            <p><strong>Medicamentos habituales:</strong> {{ player['Medicamentos habituales'] }}</p>
            <p><strong>Cirugías previas:</strong> {{ player['Cirugías previas'] }}</p>
            <p><strong>Lesiones previas:</strong> {{ player['Lesiones previas'] }}</p>
            <p><strong>Contacto de referencia 1:</strong> {% if player['Contacto de referencia 1'] %}{{ player['Contacto de referencia 1'] }}{% else %}No disponible{% endif %}</p>
            <p><strong>Contacto de referencia 2:</strong> {% if player['Contacto de referencia 2'] %}{{ player['Contacto de referencia 2'] }}{% else %}No disponible{% endif %}</p>
        </div>
        {% endfor %}
    </div>

    <script>
        function toggleDetails(index) {
            const detailsRow = document.getElementById('details-' + index);
            const isVisible = detailsRow.style.display === 'block';
            detailsRow.style.display = isVisible ? 'none' : 'block';
        }

        function searchPlayer() {
            const filter = document.getElementById("searchBar").value.toUpperCase();
            const playerList = document.getElementById("playerList");
            const players = playerList.getElementsByClassName("player-card");

            for (let i = 0; i < players.length; i++) {
                const playerName = players[i].getElementsByClassName("player-info")[0];
                const nameText = playerName.innerText || playerName.textContent;
                if (nameText.toUpperCase().indexOf(filter) > -1) {
                    players[i].style.display = "";
                } else {
                    players[i].style.display = "none";
                }
            }
        }
    </script>

    </body>
    </html>
    """
    return render_template_string(html_template, jugadores=jugadores_df)

if __name__ == '__main__':
    app.run(debug=True)
