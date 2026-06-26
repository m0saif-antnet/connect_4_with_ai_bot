from config import COLS, ROWS

from .board import is_board_full


def check_horizontal_win(board: list[list[int]], piece: int) -> bool:
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (
                board[row][col] == piece
                and board[row][col + 1] == piece
                and board[row][col + 2] == piece
                and board[row][col + 3] == piece
            ):
                return True
    return False


def check_vertical_win(board: list[list[int]], piece: int) -> bool:
    for col in range(COLS):
        for row in range(ROWS - 3):
            if (
                board[row][col] == piece
                and board[row + 1][col] == piece
                and board[row + 2][col] == piece
                and board[row + 3][col] == piece
            ):
                return True
    return False


def check_positive_diagonal_win(board: list[list[int]], piece: int) -> bool:
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (
                board[row][col] == piece
                and board[row - 1][col + 1] == piece
                and board[row - 2][col + 2] == piece
                and board[row - 3][col + 3] == piece
            ):
                return True
    return False


def check_negative_diagonal_win(board: list[list[int]], piece: int) -> bool:
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (
                board[row][col] == piece
                and board[row + 1][col + 1] == piece
                and board[row + 2][col + 2] == piece
                and board[row + 3][col + 3] == piece
            ):
                return True
    return False


def winning_move(board: list[list[int]], piece: int) -> bool:
    return (
        check_horizontal_win(board, piece)
        or check_vertical_win(board, piece)
        or check_positive_diagonal_win(board, piece)
        or check_negative_diagonal_win(board, piece)
    )


def is_draw(board: list[list[int]]) -> bool:
    return is_board_full(board) and not winning_move(board, 1) and not winning_move(board, 2)


def is_terminal_state(board: list[list[int]]) -> bool:
    return winning_move(board, 1) or winning_move(board, 2) or is_draw(board)


def get_winner(board: list[list[int]]) -> int | None:
    if winning_move(board, 1):
        return 1
    if winning_move(board, 2):
        return 2
    return None 
