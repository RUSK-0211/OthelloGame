# 盤面・文字表示のためのモジュール
import os
from typing import List, Tuple


# =========================
# 定数
# =========================

BOARD_SIZE = 8
EMPTY = "-"
BLACK = "B"
WHITE = "W"
LEGAL_MOVE = "+"

COLUMN_LABELS = "ABCDEFGH"


# =========================
# 画面操作
# =========================

def clear_screen() -> None:
    """ターミナルの画面をクリアする。"""
    os.system("cls" if os.name == "nt" else "clear")


def wait_for_enter(message: str = "Enterキーを押してください...") -> None:
    """Enterキーが押されるまで待機する。"""
    input(message)


# =========================
# 盤面表示
# =========================

def print_board(
    board: List[List[str]],
    legal_moves: List[Tuple[int, int]] | None = None,
) -> None:
    """
    オセロの盤面を表示する。

    Args:
        board: 8×8の盤面
        legal_moves: 現在のプレイヤーが置ける場所
    """
    if legal_moves is None:
        legal_moves = []

    legal_move_set = set(legal_moves)

    # 列番号
    print()
    print("      " + "   ".join(COLUMN_LABELS))

    # 上側の枠
    print("    ┌" + "───┬" * 7 + "───┐")

    for row in range(BOARD_SIZE):
        cells = []

        for col in range(BOARD_SIZE):
            if (row, col) in legal_move_set:
                cell = LEGAL_MOVE
            elif board[row][col] == BLACK:
                cell = "X"
            elif board[row][col] == WHITE:
                cell = "O"
            else:
                cell = " "

            cells.append(cell)

        print(
            f" {row + 1}  │"
            + "│".join(f" {cell} " for cell in cells)
            + "│"
        )

        if row < BOARD_SIZE - 1:
            print("    ├" + "───┼" * 7 + "───┤")

    # 下側の枠
    print("    └" + "───┴" * 7 + "───┘")
    print()


# =========================
# ゲーム情報表示
# =========================

def print_score(board: List[List[str]]) -> None:
    """現在の黒・白の石数を表示する。"""
    black_count = sum(row.count(BLACK) for row in board)
    white_count = sum(row.count(WHITE) for row in board)

    print(f"  ● BLACK  {black_count:>2}    ○ WHITE  {white_count:>2}")


def print_turn(player: str) -> None:
    """現在のプレイヤーを表示する。"""
    player_name = "BLACK" if player == BLACK else "WHITE"
    stone = "●" if player == BLACK else "○"

    print(f"\n  {stone} {player_name} の番")


def print_game_status(
    board: List[List[str]],
    player: str,
) -> None:
    """現在のゲーム状態をまとめて表示する。"""
    print_score(board)
    print_turn(player)


# =========================
# メッセージ表示
# =========================

def print_message(message: str) -> None:
    """ゲーム中のメッセージを表示する。"""
    print()
    print(f"  {message}")


def print_legal_moves(
    legal_moves: List[Tuple[int, int]],
) -> None:
    """現在置ける場所を表示する。"""
    moves = []

    for row, col in legal_moves:
        move = f"{COLUMN_LABELS[col]}{row + 1}"
        moves.append(move)

    print(f"  置ける場所: {' / '.join(moves)}")


def print_move_message(
    move: str,
    flipped_count: int,
) -> None:
    """石を置いた結果を表示する。"""
    if flipped_count == 1:
        stone_text = "1枚"
    else:
        stone_text = f"{flipped_count}枚"

    print_message(
        f"{move} に置きました。{stone_text}の石をひっくり返しました。"
    )


def print_no_moves_message(player: str) -> None:
    """置ける場所がない場合のメッセージを表示する。"""
    player_name = "BLACK" if player == BLACK else "WHITE"
    print_message(
        f"{player_name} は置ける場所がありません。パスします。"
    )


def print_invalid_move_message() -> None:
    """無効な手が入力された場合のメッセージを表示する。"""
    print_message("そこには置けません。置ける場所を選んでください。")


# =========================
# 入力
# =========================

def input_move() -> str:
    """
    プレイヤーから手を入力してもらう。

    Returns:
        A1〜H8、S（セーブ）、Q（終了）
    """
    while True:
        move = input("  手を入力してください > ").strip().upper()

        if move in ("S", "Q"):
            return move

        if len(move) != 2:
            print_message("A1〜H8の形式で入力してください。")
            continue

        column = move[0]
        row = move[1]

        if column not in COLUMN_LABELS or row not in "12345678":
            print_message("A1〜H8の形式で入力してください。")
            continue

        return move


# =========================
# メニュー
# =========================

def print_title() -> None:
    """ゲームタイトルを表示する。"""
    print()
    print("╔════════════════════════════════════╗")
    print("║               OTHELLO              ║")
    print("╚════════════════════════════════════╝")
    print()


def print_menu() -> None:
    """ゲーム開始メニューを表示する。"""
    print_title()

    print("  1. はじめから")
    print("  2. セーブデータから")
    print("  3. 終了")
    print()


def input_menu() -> int:
    """メニュー番号を入力する。"""
    while True:
        choice = input("  選択してください > ").strip()

        if choice in ("1", "2", "3"):
            return int(choice)


# =========================
# ゲーム画面
# =========================

def draw_game_screen(
    board: List[List[str]],
    player: str,
    legal_moves: List[Tuple[int, int]],
) -> None:
    """
    ゲーム画面全体を描画する。

    盤面・石数・現在のプレイヤーをまとめて表示する。
    """
    clear_screen()

    print_title()
    print_board(board, legal_moves)
    print_game_status(board, player)

    print()
    print_legal_moves(legal_moves)

    print()
    print("  「+」が現在置ける場所です。")
    print("  S : セーブ")
    print("  Q : ゲーム終了")
    print()


# =========================
# 結果表示
# =========================

def print_result(
    board: List[List[str]],
    winner: str | None,
) -> None:
    """ゲーム終了時の結果を表示する。"""
    clear_screen()

    print_title()
    print_board(board)
    print_score(board)

    print()

    if winner == BLACK:
        print("  ● BLACK の勝利！")
    elif winner == WHITE:
        print("  ○ WHITE の勝利！")
    else:
        print("  引き分け！")

    print()
