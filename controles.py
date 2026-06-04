import time
import msvcrt

from config import Mode, AppState

"""
MÓDULO: controles.py
Este módulo gestiona la captura de teclas en caliente utilizando la librería nativa de Windows 'msvcrt'.
Su función principal es escuchar de forma asíncrona las pulsaciones del usuario sin bloquear el programa.
Dependiendo de si la aplicación está en modo Navegación o Búsqueda, traduce los caracteres presionados 
en órdenes para el reproductor (reproducir, pausar, alterar volumen, escribir texto o salir del programa).
"""

def handle_input(player):
    while player.running:
        if msvcrt.kbhit():
            char = msvcrt.getch().decode("utf-8", errors="ignore")
            
            if player.current_state == AppState.NAV:
                if char == "+":
                    player.set_volume(2)
                    continue
                elif char == "-":
                    player.set_volume(-2)
                    continue

                cmd = char.upper()
                if cmd == "P": player.play()
                elif cmd == "U": player.pause()
                elif cmd == "S": player.stop()
                elif cmd == "N": 
                    with player.lock: player.next_song()
                elif cmd == "B": 
                    with player.lock: player.previous_song()
                elif cmd == "K": player.set_volume(2)
                elif cmd == "J": player.set_volume(-2)
                elif cmd == "F":
                    with player.lock:
                        player.current_state = AppState.SEARCH
                        player.search_query = ""
                elif cmd == "M":
                    with player.lock:
                        modes = [Mode.NORMAL, Mode.SHUFFLE, Mode.REPEAT_ONE, Mode.REPEAT_ALL]
                        i = modes.index(player.mode)
                        player.mode = modes[(i + 1) % len(modes)]
                        player.save_config()
                elif cmd == "Q":
                    player.running = False
                    player.stop()
                    player.save_config()
                    player.player.release()
                    player.instance.release()
                    break

            elif player.current_state == AppState.SEARCH:
                if char == "\r":
                    with player.lock:
                        if player.playlist:
                            selected_song = player.playlist[0]
                            player.playlist = player.original_playlist.copy()
                            player.current_index = player.playlist.index(selected_song)
                            player.current_state = AppState.NAV
                            player.play()
                        else:
                            player.current_state = AppState.NAV
                            player.playlist = player.original_playlist.copy()
                            player.search_query = ""
                
                elif char == "\x1b": 
                    with player.lock:
                        player.current_state = AppState.NAV
                        player.playlist = player.original_playlist.copy()
                        player.search_query = ""
                
                elif char == "\x08": 
                    with player.lock:
                        player.search_query = player.search_query[:-1]
                        player.playlist = [s for s in player.original_playlist if player.search_query.lower() in s.lower()]
                
                else: 
                    with player.lock:
                        player.search_query += char
                        player.playlist = [s for s in player.original_playlist if player.search_query.lower() in s.lower()]

        time.sleep(0.02)