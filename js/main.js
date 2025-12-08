// Esperamos a que todo el contenido de la página se haya cargado antes de ejecutar el código
document.addEventListener('DOMContentLoaded', () => {

    // Referencias a los elementos del HTML que vamos a manipular
    const playerList = document.getElementById('playerList');
    const searchBar = document.getElementById('searchBar');
    
    // Variable global para almacenar los datos de los jugadores cargados desde el JSON
    let jugadoresData = [];

    // --- FUNCIONES PRINCIPALES ---

    /**
     * Carga los datos de los jugadores desde el archivo JSON.
     * Utiliza la API Fetch para leer el archivo de forma asíncrona.
     */
    async function cargarDatos() {
        try {
            // Hacemos la petición para obtener el archivo JSON
            const response = await fetch('data/jugadores.json');
            
            // Verificamos si la petición fue exitosa
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            // Convertimos la respuesta a un objeto JSON y la guardamos en nuestra variable
            jugadoresData = await response.json();
            
            // Una vez cargados los datos, los mostramos en la página
            mostrarJugadores(jugadoresData);

        } catch (error) {
            // Si algo sale mal, mostramos un mensaje de error en la consola y en la página
            console.error("No se pudieron cargar los datos de los jugadores:", error);
            playerList.innerHTML = '<p style="color: red; text-align: center;">Error al cargar los datos. Por favor, inténtelo más tarde.</p>';
        }
    }

    /**
     * Genera el HTML para cada jugador y lo inserta en la página.
     * @param {Array} jugadores - Un array con los datos de los jugadores a mostrar.
     */
    function mostrarJugadores(jugadores) {
        // Limpiamos el contenido actual de la lista para evitar duplicados
        playerList.innerHTML = ''; 
        
        // Recorremos cada jugador en el array recibido
        jugadores.forEach((player, index) => {
            
            // --- LÓGICA PARA LA RUTA DE LA FOTO ---
            // 1. Obtenemos el nombre completo del jugador.
            // 2. Lo convertimos a minúsculas.
            // 3. Reemplazamos espacios por guiones bajos (_) para que sea un nombre de archivo válido.
            // 4. Quitamos caracteres especiales que no son letras, números o guiones bajos.
            const nombreArchivo = player['Nombre completo'].toLowerCase().replace(/\s+/g, '_').replace(/[^a-z0-9_]/g, '');
            const imagePath = `static/fotos/${nombreArchivo}.png`;
            const defaultImagePath = 'static/fotos/default-player.png'; // Ruta a la imagen por defecto

            // Creamos un elemento 'div' para la tarjeta del jugador
            const playerCard = document.createElement('div');
            playerCard.className = 'player-card';

            // Usamos 'innerHTML' para definir la estructura HTML de la tarjeta
            // Usamos "template literals" (comillas invertidas ``) para poder insertar variables fácilmente
            playerCard.innerHTML = `
                <div class="player-info">
                    <strong>${player['Nombre completo']}</strong><br>
                    <small>Cédula: ${player['Cédula']} | Fecha de nacimiento: ${player['Fecha de nacimiento']} | Celular: ${player['Celular']}</small>
                </div>
                <img src="${imagePath}" alt="${player['Nombre completo']}" onerror="this.onerror=null; this.src='${defaultImagePath}';">
                <button onclick="toggleDetails(${index})">Ver detalles</button>
            `;

            // Creamos otro 'div' para los detalles ocultos
            const detailsDiv = document.createElement('div');
            detailsDiv.className = 'details';
            detailsDiv.id = `details-${index}`; // ID único para cada sección de detalles
            
            // Usamos el operador '||' para mostrar "No disponible" si el campo está vacío
            detailsDiv.innerHTML = `
                <p><strong>Altura:</strong> ${player['Altura (cm)']} cm</p>
                <p><strong>Peso:</strong> ${player['Peso (kg)']} kg</p>
                <p><strong>Sanatorio:</strong> ${player['Sanatorio']}</p>
                <p><strong>Grupo sanguíneo:</strong> ${player['Grupo sanguíneo']}</p>
                <p><strong>Enfermedades previas:</strong> ${player['Enfermedades previas']}</p>
                <p><strong>Alergias:</strong> ${player['Alergias']}</p>
                <p><strong>Medicamentos habituales:</strong> ${player['Medicamentos habituales']}</p>
                <p><strong>Cirugías previas:</strong> ${player['Cirugías previas']}</p>
                <p><strong>Lesiones previas:</strong> ${player['Lesiones previas']}</p>
                <p><strong>Contacto de referencia 1:</strong> ${player['Contacto de referencia 1'] || 'No disponible'}</p>
                <p><strong>Contacto de referencia 2:</strong> ${player['Contacto de referencia 2'] || 'No disponible'}</p>
            `;

            // Añadimos la tarjeta y los detalles al contenedor principal
            playerList.appendChild(playerCard);
            playerList.appendChild(detailsDiv);
        });
    }

    // --- EVENT LISTENERS (MANEJO DE INTERACCIONES) ---

    /**
     * Muestra u oculta la sección de detalles de un jugador.
     * La hacemos global (window.toggleDetails) para que el 'onclick' en el HTML pueda encontrarla.
     */
    window.toggleDetails = (index) => {
        const detailsRow = document.getElementById(`details-${index}`);
        const isVisible = detailsRow.style.display === 'block';
        detailsRow.style.display = isVisible ? 'none' : 'block';
    };

    /**
     * Filtra los jugadores en tiempo real según lo que se escriba en la barra de búsqueda.
     */
    searchBar.addEventListener('keyup', (event) => {
        const filter = event.target.value.toUpperCase();
        
        // Filtramos el array 'jugadoresData' original
        const filteredPlayers = jugadoresData.filter(player => 
            // Comprobamos si el nombre completo del jugador incluye el texto del filtro
            player['Nombre completo'].toUpperCase().includes(filter)
        );
        
        // Mostramos solo los jugadores que coincidieron con la búsqueda
        mostrarJugadores(filteredPlayers);
    });

    // --- INICIALIZACIÓN ---
    
    // Llamamos a la función cargarDatos para empezar el proceso cuando la página esté lista
    cargarDatos();
});