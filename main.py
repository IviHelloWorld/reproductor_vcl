import os
import threading
import time
from rich.live import Live

from motor import MusicPlayer
from interfaz import build_ui
from controles import handle_input

"""
MÓDULO: main.py
Este archivo es el punto de entrada principal ("orquestador") del reproductor. 
Su tarea es instanciar la clase 'MusicPlayer' pasándole la ruta de la carpeta de música, iniciar 
los hilos de ejecución secundarios independientes (para el control de reproducción automática y 
la escucha del teclado) y ejecutar el bucle principal de refresco visual en tiempo real de Rich.
"""

def main():
    player = MusicPlayer()

    while not player.folder or not os.path.isdir(player.folder):
        print("\n🎵 --- BIENVENIDO AL REPRODUCTOR ---")
        ruta = input("Por favor, ingresa la ruta absoluta de tu carpeta de música: ").strip()
        
        ruta = ruta.strip('"').strip("'")
        
        if os.path.isdir(ruta):
            player.folder = ruta
            player.playlist = player.load_songs()
            player.original_playlist = player.playlist.copy()
            player.save_config()
        else:
            print("\n[Error] La ruta no es válida o la carpeta no existe. Intenta de nuevo.")

    if not player.playlist:
        print(f"\nNo se encontraron canciones (.mp3, .flac, .wav, .ogg) en: {player.folder}")

        player.folder = ""
        player.save_config()
        return

    threading.Thread(target=player.engine, daemon=True).start()
    threading.Thread(target=handle_input, args=(player,), daemon=True).start()

    with Live(build_ui(player), refresh_per_second=12, screen=True) as live:
        while player.running:
            live.update(build_ui(player))
            time.sleep(0.08)


if __name__ == "__main__":
    main()