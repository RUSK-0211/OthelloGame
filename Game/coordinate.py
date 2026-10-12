# 座標処理のモジュールです
from typing import List, Tuple

# 有効手を探すために必要な、「移動可能な方向」を定義する
# （行方向の変化, 列方向の変化）を表すタプルを作る
# このタプルの添え字を指定して判定に使う
DIRECTIONS: List[Tuple[int, int]] = [
    (-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]


def opponent_judge(player: str) -> str:
    """ 相手の色を判定します

    Args:
        player (str): プレイヤーの色(B or W)

    Returns:
        str: 相手の色(B or W)
    """
    if player == 'W':
        opponent = 'B'
    else:
        opponent = 'W'

    return opponent  # 相手の色を戻り値とする


def move_possible(board: List[List[str]], row: int, col: int,
                  player: str) -> bool:
    """ 指定した座標(row, col)に石を置けるかどうかを判定します

    Args:
        board (List[List[any]]): ボードの状態を表す2次元リスト('_'(空きマス) or W or B)
        row (int): 行の添え字(0～7)
        col (int): 列の添え字(0～7)
        player (str): プレイヤーの色(W or B)

    Returns:
        bool: 指定した座標に置ける場合はTrue、置けない場合はFalse
    """
    # マスが埋まっていて置けない場合は無効(False)にする
    if board[row][col] != '-':
        return False

    # 相手の色
    opponent = opponent_judge(player)

    # 指定した場所の全方向を確認する
    for i, j in DIRECTIONS:
        r, c = row + i, col + j

        # 相手の石を探す
        found_opponent = False
        # 指定した座標のすぐ隣に相手の石がなければFalseなので抜ける
        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            r += i
            c += j
            found_opponent = True  # 見つけたらTrue

        # 相手の石を挟んで、自分の石を見つけられたら有効な座標
        if (
            found_opponent and  # 見つけたときの変数がTrueだったとき
            0 <= r < 8 and  # ボードの範囲
            0 <= c < 8 and  # ボードの範囲
            board[r][c] == player  # 範囲内にいるとき
        ):
            return True
    return False


def reverse(board: List[List[str]], row: int, col: int, player: str) -> None:
    """ 指定した座標(row, col)に石を置き、反転可能な石を反転させます

    Args:
        board (List[List[str]]): ボードの状態を表す2次元リスト('_'(空きマス) or W or B)
        row (int): 行の添え字(0～7)
        col (int): 列の添え字(0～7)
        player (str): プレイヤーの色
    """
    # 相手の色
    opponent = opponent_judge(player)

    # 指定された座標に石を置く
    board[row][col] = player

    # 置いた座標の周りを確認する
    for i, j in DIRECTIONS:
        r, c = row + i, col + j
        flip_stones = []  # 反転する石の座標を記録するリスト
        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            flip_stones.append((r, c))  # 判定の度に候補を記録していく
            r += i
            c += j

        # 自分の石がそのあとに見つかれば、間にある石を反転する
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
            for n, m in flip_stones:
                board[n][m] = player  # プレイヤーの色に変える
