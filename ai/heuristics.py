from config import (
    ROWS,
    COLS,
    EMPTY,
    CENTER_COLUMN_BONUS,
    THREE_IN_A_ROW_SCORE,
    TWO_IN_A_ROW_SCORE,
    OPPONENT_THREE_THREAT_PENALTY,
    AI_WIN_SCORE,
)


def evaluate_window(window: list[int], ai_piece: int, opponent_piece: int) -> int:
    """
    Evaluates a single window of 4 cells and returns a score.
    """
    score = 0
    ai_count       = window.count(ai_piece)
    opponent_count = window.count(opponent_piece)
    empty_count    = window.count(EMPTY)

    if ai_count == 4:
        score += AI_WIN_SCORE
    elif ai_count == 3 and empty_count == 1:
        score += THREE_IN_A_ROW_SCORE
    elif ai_count == 2 and empty_count == 2:
        score += TWO_IN_A_ROW_SCORE

    if opponent_count == 3 and empty_count == 1:
        score -= OPPONENT_THREE_THREAT_PENALTY

    return score


def score_center_column(board: list[list[int]], ai_piece: int) -> int:
    """
    Rewards the AI for controlling the center column.
    Center column index is 3 for a 7-column board.
    """
    center_col   = COLS // 2
    center_array = [board[row][center_col] for row in range(ROWS)]
    return center_array.count(ai_piece) * CENTER_COLUMN_BONUS


def score_horizontal(board: list[list[int]], ai_piece: int, opponent_piece: int) -> int:
    """
    Scans all horizontal windows and sums their scores.
    """
    score = 0
    for row in range(ROWS):
        for col in range(COLS - 3):
            window = board[row][col:col + 4]
            score += evaluate_window(window, ai_piece, opponent_piece)
    return score


def score_vertical(board: list[list[int]], ai_piece: int, opponent_piece: int) -> int:
    """
    Scans all vertical windows and sums their scores.
    """
    score = 0
    for col in range(COLS):
        for row in range(ROWS - 3):
            window = [board[row + i][col] for i in range(4)]
            score += evaluate_window(window, ai_piece, opponent_piece)
    return score


def score_positive_diagonal(board: list[list[int]], ai_piece: int, opponent_piece: int) -> int:
    """
    Scans all positive diagonals (bottom-left to top-right) and sums their scores.
    """
    score = 0
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [board[row + i][col + i] for i in range(4)]
            score += evaluate_window(window, ai_piece, opponent_piece)
    return score


def score_negative_diagonal(board: list[list[int]], ai_piece: int, opponent_piece: int) -> int:
    """
    Scans all negative diagonals (top-left to bottom-right) and sums their scores.
    """
    score = 0
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = [board[row - i][col + i] for i in range(4)]
            score += evaluate_window(window, ai_piece, opponent_piece)
    return score


def score_position(board: list[list[int]], ai_piece: int, opponent_piece: int) -> int:
    """
    Main heuristic function. Combines all scoring components and returns
    the total board evaluation score. Called by minimax at depth limit.
    """
    score = 0
    score += score_center_column(board, ai_piece)
    score += score_horizontal(board, ai_piece, opponent_piece)
    score += score_vertical(board, ai_piece, opponent_piece)
    score += score_positive_diagonal(board, ai_piece, opponent_piece)
    score += score_negative_diagonal(board, ai_piece, opponent_piece)
    return score