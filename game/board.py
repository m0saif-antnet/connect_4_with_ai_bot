from copy import deepcopy

from Connect_4_with_AI_bot.config import COLS, EMPTY, ROWS


def create_board() -> list[list[int]]:
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def copy_board(board: list[list[int]]) -> list[list[int]]:
    return deepcopy(board)


def is_valid_column(board: list[list[int]], col: int) -> bool:
    if not 0 <= col < COLS:
        return False
    return board[0][col] == EMPTY


def get_next_open_row(board: list[list[int]], col: int) -> int | None:
    if not is_valid_column(board, col):
        return None

    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            return row
    return None


def drop_piece(board: list[list[int]], row: int, col: int, piece: int) -> None:
    board[row][col] = piece


def apply_move(board: list[list[int]], col: int, piece: int) -> bool:
    if not is_valid_column(board, col):
        return False

    row = get_next_open_row(board, col)
    if row is None:
        return False

    drop_piece(board, row, col, piece)
    return True


def get_valid_moves(board: list[list[int]]) -> list[int]:
    return [col for col in range(COLS) if is_valid_column(board, col)]


def is_board_full(board: list[list[int]]) -> bool:
    return len(get_valid_moves(board)) == 0