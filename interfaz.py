from rich.align import Align
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout

from config import Mode, AppState

"""
MÓDULO: interfaz.py
Este módulo es el encargado exclusivo del renderizado visual en la terminal usando la librería Rich.
Toma los datos del reproductor en un momento dado (nombre de canción, progreso, volumen, lista filtrada)
y construye los componentes de la interfaz de usuario: el panel superior, la barra de progreso temporal,
el menú de canciones paginado y la barra inferior que se adapta según estemos navegando o buscando texto.
"""

def format_time(seconds):
    if seconds <= 0:
        return "00:00"
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"


def render_progress(player):
    bar_len = 30
    progress = player.get_progress()

    filled = int(progress * bar_len)
    bar = "█" * filled + "-" * (bar_len - filled)

    elapsed = player.get_elapsed_time()
    duration = player.get_duration()

    return f"[{bar}] {format_time(elapsed)} / {format_time(duration)}"


def build_ui(player):
    with player.lock:
        playlist_snap = player.playlist.copy()
        current_idx = player.current_index
        current_state = player.current_state
        search_query = player.search_query
        mode = player.mode
        song = player.get_current_song()
        duration = player.get_duration()
        volume = player.volume

    if volume == 0:
        vol_icon = "🔇"
    elif volume < 40:
        vol_icon = "🔈"
    elif volume < 75:
        vol_icon = "🔉"
    else:
        vol_icon = "🔊"
        
    vol_bar_len = 5
    vol_filled = int((volume / 100) * vol_bar_len)
    vol_bar = "█" * vol_filled + "░" * (vol_bar_len - vol_filled)

    if not song or len(player.original_playlist) == 0:
        header = Panel("[red]No song[/red]", title="🎵 Now Playing", expand=False)
    else:
        header = Panel(
            f" [bold green]{song}[/bold green] \n [cyan]Mode: {mode}[/cyan]   |   [yellow]{vol_icon} [{vol_bar}] {volume}%[/yellow] ",
            title="🎵 Now Playing",
            expand=False,
            border_style="bright_blue"
        )

    if duration > 0:
        progress_text = render_progress(player)
    else:
        progress_text = "[yellow]Loading track...[/yellow]"

    table = Table(
        title=f"=== Playlist ({current_idx + 1} / {len(playlist_snap)}) ===",
        border_style="bright_black"
    )
    table.add_column("#", justify="center")
    table.add_column("Song", width=60) 

    PAGE_SIZE = 10 
    start_idx = max(0, current_idx - (PAGE_SIZE // 2))
    end_idx = min(len(playlist_snap), start_idx + PAGE_SIZE)

    if end_idx - start_idx < PAGE_SIZE:
        start_idx = max(0, end_idx - PAGE_SIZE)

    for i in range(start_idx, end_idx):
        s = playlist_snap[i]
        display_name = s[:55] + "..." if len(s) > 55 else s

        if current_state == AppState.NAV and i == current_idx:
            table.add_row(str(i + 1), f"[bold magenta]▶ {display_name}[/bold magenta]")
        else:
            table.add_row(str(i + 1), f"[dim]{display_name}[/dim]")

    if current_state == AppState.NAV:
        controls_text = "[P] Play  [U] Pause  [S] Stop  [N] Next  [B] Back  [M] Mode  [K/+] Vol+  [J/-] Vol-  [F] Buscar  [Q] Quit"
    else:
        controls_text = f"[Filtrando]: {search_query} | [Enter] Escuchar | [ESC] Volver"

    controls = Panel(
        Align.center(controls_text), 
        title=f"🎮 Controls ({current_state})",
        border_style="yellow"
    )

    layout = Layout()
    layout.split_column(
        Layout(Align.center(header), size=4),
        Layout(Align.center(progress_text), size=3),
        Layout(Align.center(table)),
        Layout(controls, size=3)
    )

    return layout