# 🎵 Reproductor VCL (Terminal Music Player)

Un reproductor de música modular para la terminal desarrollado en Python. Cuenta con una interfaz visual interactiva en consola usando **Rich**, sistema de búsqueda/filtrado de canciones en tiempo real, control de volumen corregido para eliminar zonas muertas y persistencia de configuración en JSON.

---

##  Prerrequisitos

Antes de clonar y ejecutar el proyecto, asegúrate de cumplir con lo siguiente:

1. **Python 3.x** instalado en tu sistema.
2. **VLC Media Player** instalado en tu computadora (el reproductor de escritorio normal). La librería de Python utiliza los motores nativos de VLC para procesar y reproducir el audio.

---

##  Instalación y Uso

Sigue estos pasos para poner a funcionar el reproductor en tu máquina:

1. **Descarga el proyecto:** Clonando el repositorio o descargando el archivo `.ZIP` desde GitHub.
2. **Abre tu terminal** (PowerShell, CMD o la terminal de tu sistema) y navega hasta la carpeta del proyecto:
```bash
   cd ruta/a/la/carpeta/reproductor_vcl
   ```
3. **Instala las dependencias obligatorias:** Ejecuta el siguiente comando para instalar las librerías necesarias de forma automática:
```bash
   pip install -r requirements.txt
   ```
4. **Ejecuta el programa:**
```bash
   python main.py
   ```

>  **Nota de primera configuración:** La primera vez que inicies el programa (o si la carpeta guardada deja de existir), la terminal se detendrá y te pedirá que ingreses la ruta absoluta de tu carpeta de música local (ej. `C:\Users\TuUsuario\Music`). Esta ruta se guardará de forma persistente en un archivo local `player_config.json` para que no tengas que escribirla nunca más.

---

##  Controles de la Interfaz

El reproductor responde inmediatamente a las pulsaciones de teclado en caliente sin necesidad de presionar `Enter` en el modo de navegación.

###  Modo Navegación
* `P` : Reproducir la canción seleccionada en el índice actual.
* `U` : Pausar / Reanudar el audio.
* `S` : Detener por completo la reproducción.
* `N` : Avanzar a la siguiente canción.
* `B` : Volver a la canción anterior.
* `M` : Alternar el modo de reproducción (`normal`, `shuffle` [aleatorio], `repeat_one` [repetir pista], `repeat_all` [repetir lista]).
* `K` o `+` : Subir el volumen (incrementos de 2%).
* `J` o `-` : Bajar el volumen (decrementos de 2%).
* `F` : Activar el **Modo Búsqueda** (Filtrado).
* `Q` : Guardar estado actual, liberar hilos y salir de la aplicación de forma segura.

###  Modo Búsqueda
* **Escribe directamente:** Empezará a filtrar las canciones de la lista por nombre en tiempo real.
* `Enter` : Reproduce el primer resultado del filtro, restablece la lista completa y regresa automáticamente al Modo Navegación.
* `BackSpace` (Retroceso) : Borra caracteres del filtro actual.
* `ESC` : Cancela la búsqueda actual, borra el filtro y regresa al Modo Navegación.

---

##  Estructura del Proyecto

* `main.py` - Orquestador y punto de entrada. Inicia los hilos asíncronos y refresca la UI.
* `motor.py` - Lógica central del reproductor, persistencia en JSON e interacción con el motor de audio VLC.
* `interfaz.py` - Construcción visual y renderizado de paneles, tablas y barras de progreso mediante Rich.
* `controles.py` - Captura e interpretación asíncrona de teclas en caliente nativas del sistema operativo.
* `config.py` - Constantes globales, estados de la app y modos de reproducción.
* `requirements.txt` - Lista de dependencias externas del proyecto.
* `.gitignore` - Archivo de protección para evitar subir cachés de Python (`__pycache__`) o configuraciones locales privadas.

* ---

## Roadmap / Próximas Características (Versión 2.0)

Este proyecto está en constante evolución. Para la **Versión 2.0**, se están planificando las siguientes mejoras mayoritarias:

*   **Interfaz Gráfica de Usuario (GUI):** Migración de la interfaz de terminal (Rich) a una ventana visual moderna e intuitiva.
*   **Aplicación Ejecutable Standalone (.exe):** Distribución del programa compilado como un ejecutable directo para Windows. Esto permitirá que cualquier persona use el reproductor con un doble clic, **sin necesidad de tener Python instalado previamente**.
*   **Integración de Dependencias:** Optimización del empaquetado para reducir o automatizar el requisito de instalar VLC Media Player de forma externa.
*   **Personalización de Temas:** Soporte para cambiar los colores de la interfaz y gestionar listas de reproducción avanzadas de forma visual.
