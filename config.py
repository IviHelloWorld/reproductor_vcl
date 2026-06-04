"""
MÓDULO: config.py
Este módulo define las constantes y los estados globales de la aplicación. 
Contiene el nombre del archivo JSON de configuración, los modos de reproducción disponibles 
(normal, aleatorio, repetir una, repetir todas) y los estados posibles de la interfaz (navegación o búsqueda).
"""

CONFIG_FILE = "player_config.json"

class Mode:
    NORMAL = "normal"
    SHUFFLE = "shuffle"
    REPEAT_ONE = "repeat_one"
    REPEAT_ALL = "repeat_all"

class AppState:
    NAV = "Navegación"
    SEARCH = "Búsqueda"