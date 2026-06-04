import os
import time
import threading
import random
import json
import vlc

from config import CONFIG_FILE, Mode, AppState

"""
MÓDULO: motor.py
Este módulo contiene la lógica central del reproductor de música a través de la clase 'MusicPlayer'.
Se encarga de escanear la carpeta de música, gestionar la lista de reproducción actual, leer/escribir
la persistencia de datos en el archivo JSON e interactuar con el motor de audio de VLC. También incluye 
el hilo ('engine') que detecta automáticamente cuándo termina una canción para pasar a la siguiente, 
y la fórmula para corregir la escala de volumen y eliminar la zona muerta de audio.
"""

class MusicPlayer:
    def __init__(self, folder=""):
        self.folder = folder 
        self.lock = threading.Lock()
        
        self.current_index = 0
        self.is_playing = False
        self.volume = 50 

        self.running = True
        self.mode = Mode.NORMAL

        self.current_state = AppState.NAV
        self.search_query = ""

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        self.load_config()

        self.playlist = self.load_songs()
        self.original_playlist = self.playlist.copy()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    if not self.folder:
                        self.folder = data.get("folder", "")
                    self.current_index = data.get("current_index", 0)
                    self.mode = data.get("mode", Mode.NORMAL)
                    self.volume = data.get("volume", 50)
                    
                    if self.current_index >= len(self.playlist):
                        self.current_index = 0
            except (json.JSONDecodeError, PermissionError):
                self.current_index = 0
                self.mode = Mode.NORMAL
                self.volume = 50

    def save_config(self):
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump({
                    "folder": self.folder,  
                    "current_index": self.current_index,
                    "mode": self.mode,
                    "volume": self.volume
                }, f)
        except Exception:
            pass

    def load_songs(self):
        if not os.path.isdir(self.folder):
            return []

        return [
            f for f in os.listdir(self.folder)
            if f.lower().endswith((".mp3", ".flac", ".wav", ".ogg"))
        ]

    def get_current_song(self):
        try:
            if self.current_state == AppState.SEARCH:
                return self.original_playlist[self.current_index]
            return self.playlist[self.current_index]
        except IndexError:
            if self.original_playlist:
                self.current_index = min(self.current_index, len(self.original_playlist) - 1)
                return self.original_playlist[self.current_index]
            return "Cargando..."

    def _apply_volume(self):
        if self.volume == 0:
            vlc_vol = 0
        else:
            vlc_vol = int(6 + (self.volume * 0.94))
        self.player.audio_set_volume(vlc_vol)

    def play(self):
        song = self.get_current_song()
        if not song:
            return

        path = os.path.join(self.folder, song)

        media = self.instance.media_new(path)
        self.player.set_media(media)
        self.player.play()

        time.sleep(0.2)
        self._apply_volume()

        self.is_playing = True
        self.save_config()

    def set_volume(self, delta):
        with self.lock:
            self.volume = max(0, min(100, self.volume + delta))
            self._apply_volume()

    def stop(self):
        self.player.stop()
        self.is_playing = False

    def pause(self):
        self.player.pause()

    def next_song(self):
        target_len = len(self.original_playlist)
        if target_len == 0:
            return

        if self.mode == Mode.SHUFFLE:
            self.current_index = random.randint(0, target_len - 1)
        elif self.mode == Mode.REPEAT_ONE:
            pass
        else:
            self.current_index += 1
            if self.current_index >= target_len:
                if self.mode == Mode.REPEAT_ALL:
                    self.current_index = 0
                else:
                    self.current_index = target_len - 1

        self.play()

    def previous_song(self):
        target_len = len(self.original_playlist)
        if target_len == 0:
            return

        self.current_index -= 1
        if self.current_index < 0:
            if self.mode == Mode.REPEAT_ALL:
                self.current_index = target_len - 1
            else:
                self.current_index = 0

        self.play()

    def engine(self):
        while self.running:
            state = self.player.get_state()
            if self.is_playing and state == vlc.State.Ended:
                with self.lock:
                    self.next_song()
            time.sleep(0.5)

    def get_elapsed_time(self):
        return self.player.get_time() / 1000

    def get_duration(self):
        return self.player.get_length() / 1000 or 0

    def get_progress(self):
        duration = self.get_duration()
        elapsed = self.get_elapsed_time()

        if duration <= 0 or elapsed < 0:
            return 0
        return min(elapsed / duration, 1)