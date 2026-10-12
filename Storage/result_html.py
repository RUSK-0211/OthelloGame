# オセロのゲーム結果をHTMLファイルとして出力するモジュール
from pathlib import Path
from typing import List, Optional


# プロジェクトのルートディレクトリ
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# HTMLファイルの出力先
RESULT_FILE = PROJECT_ROOT / "output_othello.html"


COLUMN_LABELS = "ABCDEFGH"


def board_to_html(board: List[List[str]]) -> str:
    """盤面をHTMLのtable要素に変換します。

    Args:
        board: オセロの盤面

    Returns:
        str: 盤面を表すHTML
    """
    rows = []

    # 列番号
    header_cells = "".join(
        f"<th>{column}</th>" for column in COLUMN_LABELS
    )

    rows.append(
        f"""
        <tr>
            <th></th>
            {header_cells}
        </tr>
        """
    )

    # 盤面
    for row_index, row in enumerate(board):
        cells = []

        for cell in row:
            if cell == "B":
                cells.append('<td><span class="stone black"></span></td>')
            elif cell == "W":
                cells.append('<td><span class="stone white"></span></td>')
            else:
                cells.append("<td></td>")

        rows.append(
            f"""
            <tr>
                <th>{row_index + 1}</th>
                {''.join(cells)}
            </tr>
            """
        )

    return f"""
    <table class="board">
        {''.join(rows)}
    </table>
    """


def get_result_text(winner: Optional[str]) -> str:
    """勝者に応じた結果メッセージを返します。

    Args:
        winner: 勝者。B、W、またはNone

    Returns:
        str: 結果メッセージ
    """
    if winner == "B":
        return "黒の勝ち！"

    if winner == "W":
        return "白の勝ち！"

    return "引き分け！"


def get_winner_class(winner: Optional[str]) -> str:
    """勝者に応じたCSSクラスを返します。

    Args:
        winner: 勝者。B、W、またはNone

    Returns:
        str: CSSクラス名
    """
    if winner == "B":
        return "black-win"

    if winner == "W":
        return "white-win"

    return "draw"


def create_result_html(
    board: List[List[str]],
    winner: Optional[str],
    black_count: int,
    white_count: int
) -> str:
    """ゲーム結果のHTML全体を生成します。

    Args:
        board: 最終盤面
        winner: 勝者。B、W、またはNone
        black_count: 黒石の数
        white_count: 白石の数

    Returns:
        str: 完成したHTML
    """
    result_text = get_result_text(winner)
    winner_class = get_winner_class(winner)
    board_html = board_to_html(board)

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>オセロゲームの結果</title>
    <link rel="stylesheet" href="style.css">
</head>

<body>
    <main class="result-container">

        <nav class="navbar">
            <div class="navbar-title">
                OTHELLO
            </div>

            <div class="navbar-page">
                GAME RESULT
            </div>
        </nav>

        <header class="result-header">
            <p class="result-message {winner_class}">
                {result_text}
            </p>
        </header>

        <section class="score-section">
            <h2>SCORE</h2>

            <div class="score">
                <div class="score-item black-score">
                    <span class="player-label">BLACK</span>
                    <span class="score-value">{black_count}</span>
                </div>

                <div class="score-divider">-</div>

                <div class="score-item white-score">
                    <span class="player-label">WHITE</span>
                    <span class="score-value">{white_count}</span>
                </div>
            </div>
        </section>

        <section class="board-section">
            <h2>FINAL BOARD</h2>
            {board_html}
        </section>

    </main>
</body>
</html>
"""


def export_result_html(
    board: List[List[str]],
    winner: Optional[str],
    black_count: int,
    white_count: int
) -> None:
    """ゲーム結果をHTMLファイルとして出力します。

    Args:
        board: 最終盤面
        winner: 勝者。B、W、またはNone
        black_count: 黒石の数
        white_count: 白石の数
    """
    html = create_result_html(
        board,
        winner,
        black_count,
        white_count
    )

    with RESULT_FILE.open("w", encoding="utf-8") as file:
        file.write(html)
