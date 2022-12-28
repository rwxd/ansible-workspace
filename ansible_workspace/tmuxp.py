from dataclasses import dataclass


@dataclass
class TmuxpWindow:
    window_name: str
    start_directory: str
    layout: str = 'tiled'
    shell_command_before: str = ''


@dataclass
class TmuxpWorkspace:
    session_name: str
    start_directory: str
    windows: list[TmuxpWindow]
