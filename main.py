# オセロゲーム
from typing import List, Tuple

# プロジェクト内のモジュールを読み込む
from Game import coordinate
from UI import cli
from UI import sound
from Storage import save
from Storage import result_html


# =========================
# 定数
# =========================

BOARD_SIZE = 8

EMPTY = "-"
BLACK = "B"
WHITE = "W"

# =========================
# 盤面
# =========================


def create_board() -> List[List[str]]:
    """
    初期状態の盤面を作成する。
    """
    board = [
        [EMPTY for _ in range(BOARD_SIZE)]
        for _ in range(BOARD_SIZE)
    ]

    # 初期配置
    board[3][3] = WHITE
    board[3][4] = BLACK
    board[4][3] = BLACK
    board[4][4] = WHITE

    return board


def board_full(board: List[List[str]]) -> bool:
    """
    盤面がすべて埋まっているか判定する。
    """
    return all(
        cell != EMPTY
        for row in board
        for cell in row
    )


# =========================
# 手の取得
# =========================


def get_legal_moves(
    board: List[List[str]],
    player: str,
) -> List[Tuple[int, int]]:
    """
    指定したプレイヤーが置ける場所を取得する。

    Returns:
        (row, col) のタプルのリスト
    """
    legal_moves = []

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if coordinate.move_possible(
                board,
                row,
                col,
                player,
            ):
                legal_moves.append((row, col))

    return legal_moves


def move_to_position(move: str) -> Tuple[int, int]:
    """
    A1〜H8形式の入力を盤面上の座標に変換する。

    例:
        A1 -> (0, 0)
        D3 -> (2, 3)
        H8 -> (7, 7)
    """
    column = ord(move[0]) - ord("A")
    row = int(move[1]) - 1

    return row, column


# =========================
# プレイヤー
# =========================


def switch_player(player: str) -> str:
    """
    現在のプレイヤーを交代する。
    """
    if player == BLACK:
        return WHITE

    return BLACK


# =========================
# 勝敗
# =========================


def get_score(board: List[List[str]]) -> Tuple[int, int]:
    """
    黒と白の石数を取得する。

    Returns:
        (black_count, white_count)
    """
    black_count = sum(
        row.count(BLACK)
        for row in board
    )

    white_count = sum(
        row.count(WHITE)
        for row in board
    )

    return black_count, white_count


def get_winner(board: List[List[str]]) -> str | None:
    """
    勝者を判定する。

    Returns:
        BLACK / WHITE / None（引き分け）
    """
    black_count, white_count = get_score(board)

    if black_count > white_count:
        return BLACK

    if white_count > black_count:
        return WHITE

    return None


# =========================
# セーブデータ
# =========================

def load_game() -> Tuple[
    List[List[str]],
    str,
]:
    """
    セーブデータを読み込む。
    """
    board, current_player = save.load_game()

    return board, current_player


# =========================
# ゲーム終了
# =========================


def finish_game(
    board: List[List[str]],
) -> None:
    """
    ゲーム終了時の処理を行う。
    """
    winner = get_winner(board)

    cli.print_result(
        board,
        winner,
    )

    black_count, white_count = get_score(board)

    # HTML形式で結果を保存するか確認
    answer = input(
        "  結果をHTMLファイルに保存しますか？ (y/n) > "
    ).strip().lower()

    if answer == "y":
        result_html.export_result_html(
            board,
            winner,
            black_count,
            white_count,
        )

        cli.print_message(
            "ゲーム結果を output_othello.html に保存しました。"
        )

    cli.wait_for_enter()


# =========================
# ゲーム本体
# =========================


def play_game(
    board: List[List[str]],
    current_player: str,
) -> None:
    """
    オセロのゲームを進行する。
    """

    while not board_full(board):

        # 現在のプレイヤーが置ける場所を取得
        legal_moves = get_legal_moves(
            board,
            current_player,
        )

        # ゲーム画面を描画
        cli.draw_game_screen(
            board,
            current_player,
            legal_moves,
        )

        # 置ける場所がない場合
        if not legal_moves:
            sound.play_error()  # 操作できないときの音を再生
            cli.print_no_moves_message(
                current_player
            )

            # 相手にも置ける場所がなければ終了
            opponent = switch_player(
                current_player
            )

            opponent_moves = get_legal_moves(
                board,
                opponent,
            )

            if not opponent_moves:
                break

            current_player = opponent

            cli.wait_for_enter()
            continue

        # 手を入力
        move = cli.input_move()

        # セーブ
        if move == "S":
            save.save_game(
                board,
                current_player,
            )
            sound.play_save()  # セーブ完了時の音を再生
            cli.print_message(
                "ゲームをセーブしました。"
            )

            cli.wait_for_enter()
            continue

        # ゲーム終了
        if move == "Q":
            cli.print_message(
                "ゲームを終了します。"
            )

            cli.wait_for_enter()
            return

        # 座標に変換
        row, col = move_to_position(move)

        # 入力された場所が合法手か確認
        if (row, col) not in legal_moves:
            sound.play_error()  # 操作できないときの音を再生
            cli.print_invalid_move_message()

            cli.wait_for_enter()
            continue

        # 石を置く前の石数を取得
        before_black, before_white = get_score(board)

        # 石を置いて、挟んだ石を反転
        coordinate.reverse(
            board,
            row,
            col,
            current_player,
        )
        sound.play_place()  # 石を置いたときの音を再生

        # 石を置いた後の石数を取得
        after_black, after_white = get_score(board)

        # ひっくり返した石の枚数を計算
        if current_player == BLACK:
            flipped_count = after_black - before_black - 1
        else:
            flipped_count = after_white - before_white - 1

        cli.print_move_message(
            move,
            flipped_count,
        )

        cli.wait_for_enter()

        # プレイヤー交代
        current_player = switch_player(
            current_player
        )

    # ゲーム終了
    sound.play_result()  # ゲーム終了時の音を再生
    finish_game(board)


# =========================
# メニュー
# =========================


def start_new_game() -> None:
    """
    新しいゲームを開始する。
    """
    board = create_board()

    play_game(
        board,
        BLACK,
    )


def continue_game() -> None:
    """
    セーブデータからゲームを再開する。
    """

    if not save.has_save_data():
        cli.print_message(
            "セーブデータがありません。"
        )
        cli.wait_for_enter()
        return

    board, current_player = save.load_game()

    play_game(
        board,
        current_player,
    )


def start_menu() -> None:
    """
    メニュー画面を表示し、ゲームを開始する。
    """
    while True:
        cli.clear_screen()
        cli.print_menu()

        choice = cli.input_menu()

        if choice == 1:
            start_new_game()

        elif choice == 2:
            continue_game()

        elif choice == 3:
            cli.clear_screen()
            cli.print_title()
            cli.print_message(
                "ゲームを終了します。"
            )
            break


# =========================
# エントリーポイント
# =========================


def main() -> None:
    """
    アプリケーションのエントリーポイント。
    """
    sound.initialize()  # 効果音を初期化
    sound.play_title()  # タイトル画面の音を再生
    start_menu()


if __name__ == "__main__":
    main()
