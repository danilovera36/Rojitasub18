from flask import Flask, render_template_string
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    # Ruta al archivo Excel
    excel_file_path = "/home/danilovera/Descargas/rojita/jugadores.xlsx"
    try:
        jugadores_df = pd.read_excel(excel_file_path)
    except Exception as e:
        return f"Error al leer el archivo Excel: {e}"

    jugadores = jugadores_df.to_dict(orient="records")

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
                color: #FF0000;
                font-size: 24px;
                margin: 0;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                background-color: #fff;
                border: 1px solid #ddd;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #FF0000;
                color: white;
            }
            tr:hover {
                background-color: #f1f1f1;
            }
            .details {
                display: none; /* Ocultar inicialmente */
                background-color: #f9f9f9;
                padding: 20px;
                border: 1px solid #ddd;
                margin-top: 10px;
                border-radius: 8px;
            }
            .details .data-row {
                display: flex;
                margin-bottom: 10px;
                align-items: center;
            }
            .details .data-row div {
                margin-left: 10px;
                font-size: 14px;
            }
            .player-photo {
                width: 120px;
                height: 120px;
                border-radius: 50%;
                background-color: #f1f1f1;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 12px;
                color: #666;
                overflow: hidden;
                margin-right: 20px;
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
        <img src="/static/logo.png" alt="Logo Federación" class="logo">
        <h1>SELECCIÓN COLONIA INTERIOR SUB 18</h1>
    </header>

    <table>
        <thead>
            <tr>
                <th>Nombre completo</th>
                <th>Acción</th>
            </tr>
        </thead>
        <tbody>
            {% for player in jugadores %}
            <tr>
                <td>{{ player["Nombre completo"] }}</td>
                <td><button onclick="toggleDetails(this)">Ver detalles</button></td>
            </tr>
            <tr class="details">
                <td colspan="2">
                    <div class="data-row">
                        <div class="player-photo">
                            <img src="{{ player.get('Foto', '/static/default-player.png') }}" alt="Foto de {{ player['Nombre completo'] }}" style="width: 100%; height: 100%;">
                        </div>
                        <div>
                            <strong>Nombre:</strong> {{ player["Nombre completo"] }}<br>
                            <strong>Cédula:</strong> {{ player["Cédula"] }}<br>
                            <strong>Edad:</strong> {{ player["Edad"] }}<br>
                            <strong>Fecha de nacimiento:</strong> {{ player["Fecha de nacimiento"] }}<br>
                            <strong>Celular:</strong> {{ player["Celular"] }}<br>
                            <strong>Altura:</strong> {{ player["Altura (cm)"] }} cm<br>
                            <strong>Peso:</strong> {{ player["Peso (kg)"] }} kg<br>
                            <strong>Sanatorio:</strong> {{ player["Sanatorio"] }}<br>
                            <strong>Grupo sanguíneo:</strong> {{ player["Grupo sanguineo"] }}<br>
                            <strong>Enfermedades previas:</strong> {{ player["Enfermedades previas"] }}<br>
                            <strong>Alergias:</strong> {{ player["Alergias"] }}<br>
                            <strong>Medicamentos habituales:</strong> {{ player["Medicamentos habituales"] }}<br>
                            <strong>Cirugías previas:</strong> {{ player["Cirugías previas"] }}<br>
                            <strong>Lesiones previas:</strong> {{ player["Lesiones previas"] }}<br>
                            <strong>Contacto de referencia 1:</strong> {{ player["Contacto de referencia (nombre, relación, teléfono)"] }}<br>
                            <strong>Contacto de referencia 2:</strong> {{ player["Contacto de referencia 2 (nombre, relación, teléfono)"] }}
                        </div>
                    </div>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <script>
        function toggleDetails(button) {
            const row = button.parentElement.parentElement;
            const details = row.nextElementSibling;
            if (details && details.classList.contains('details')) {
                details.style.display = details.style.display === 'block' ? 'none' : 'block';
            }
        }
    </script>

    </body>
    </html>
    """
    return render_template_string(html_template, jugadores=jugadores)

if __name__ == "__main__":
    app.run(debug=True)
