"""オセロのゲーム効果音を管理するモジュールです。"""

from pathlib import Path
import pygame


SOUND_DIR = Path(__file__).resolve().parent.parent / "sounds"

_place_sound = None
_result_sound = None
_save_sound = None
_error_sound = None


def initialize() -> None:
    """効果音を読み込みます。"""
    global _title_sound
    global _place_sound
    global _result_sound
    global _save_sound
    global _error_sound

    pygame.mixer.init()

    _title_sound = pygame.mixer.Sound(SOUND_DIR / "title.mp3")
    _place_sound = pygame.mixer.Sound(SOUND_DIR / "place.mp3")
    _result_sound = pygame.mixer.Sound(SOUND_DIR / "result.mp3")
    _save_sound = pygame.mixer.Sound(SOUND_DIR / "save.mp3")
    _error_sound = pygame.mixer.Sound(SOUND_DIR / "error.mp3")


def play_title() -> None:
    """タイトル画面の音を再生します。"""
    _title_sound.play()


def play_place() -> None:
    """石を置いたときの音を再生します。"""
    _place_sound.play()


def play_result() -> None:
    """ゲーム終了時の音を再生します。"""
    _result_sound.play()


def play_save() -> None:
    """セーブ完了時の音を再生します。"""
    _save_sound.play()


def play_error() -> None:
    """操作できないときの音を再生します。"""
    _error_sound.play()


def cleanup() -> None:
    """音声機能を終了します。"""
    pygame.mixer.quit()
