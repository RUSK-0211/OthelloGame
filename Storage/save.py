# オセロのセーブデータを管理するモジュール
import json
from pathlib import Path
from typing import List, Tuple


# プロジェクトのルートディレクトリ
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# セーブデータの保存先
SAVE_FILE = PROJECT_ROOT / "othello_save.json"


def has_save_data() -> bool:
    """セーブデータが存在するか確認します。

    Returns:
        bool: セーブデータが存在する場合はTrue、存在しない場合はFalse
    """
    return SAVE_FILE.exists()


def save_game(board: List[List[str]], current_player: str) -> None:
    """現在のゲーム状態をJSONファイルに保存します。

    Args:
        board: 現在の盤面
        current_player: 現在のプレイヤー
    """
    game_state = {
        "board": board,
        "current_player": current_player,
    }

    with SAVE_FILE.open("w", encoding="utf-8") as file:
        json.dump(game_state, file, ensure_ascii=False, indent=4)


def load_game() -> Tuple[List[List[str]], str]:
    """保存されたゲーム状態を読み込みます。

    Returns:
        Tuple[List[List[str]], str]:
            - board: 保存されていた盤面
            - current_player: 次に操作するプレイヤー

    Raises:
        FileNotFoundError:
            セーブデータが存在しない場合
        json.JSONDecodeError:
            セーブデータが正しいJSONではない場合
        KeyError:
            必要なデータがセーブデータに存在しない場合
    """
    with SAVE_FILE.open("r", encoding="utf-8") as file:
        game_state = json.load(file)

    board = game_state["board"]
    current_player = game_state["current_player"]

    return board, current_player


def delete_save_data() -> None:
    """セーブデータを削除します。

    ゲームを最後までプレイした後など、
    不要になったセーブデータを削除するために使用します。
    """
    if SAVE_FILE.exists():
        SAVE_FILE.unlink()
