import math
from .heuristics import score_position
from game.board import (
    copy_board,
    apply_move,
    get_valid_moves)
from game.rules import(
    winning_move,
    is_terminal_state,
    get_winner,
)

# HELPERS 

def evaluate_terminal_state(board: list[list[int]], ai_piece: int, opponent_piece: int) -> int: # 
    winner = get_winner(board)
    if winner == ai_piece:
        return 1_000        
    elif winner == opponent_piece:
        return -1_000      
    else:
        return 0              
        
def simulate_move(board: list[list[int]], col: int, piece: int) -> list[list[int]]:
    new_board = copy_board(board)
    apply_move(new_board, col, piece)
    return new_board
    
def get_ordered_moves(valid_moves: list[int]) -> list[int]:
    center = 3  
    return sorted(valid_moves, key=lambda col: abs(center - col))  # Sort by distance from center (closest to center = tried first)


#  ============================================================================= VERSION 1: Basic Minimax () ============================================================================= #
def minimax(
    board: list[list[int]],
    depth: int,
    maximizing_player: bool,
    ai_piece: int,
    opponent_piece: int,
) -> tuple[int | None, int]:
 
    valid_moves = get_valid_moves(board)
    terminal = is_terminal_state(board)

    # --- Base cases: stop recursion ---

    if terminal:
        return (None, evaluate_terminal_state(board, ai_piece, opponent_piece))
        
    if depth == 0:
        return (None, score_position(board, ai_piece, opponent_piece))
        
    if not valid_moves:
        return (None, 0)

    # --- Recursive cases ---

    if maximizing_player:
        best_score = -math.inf
        best_col = valid_moves[0]   # Default to first valid move

        for col in valid_moves:
            new_board = simulate_move(board, col, ai_piece)
            _, score = minimax(new_board, depth - 1, False, ai_piece, opponent_piece)

            if score > best_score:
                best_score = score
                best_col = col

        return (best_col, best_score)

    else:
        # Opponent's turn: look for the move with the LOWEST score
        best_score = math.inf
        best_col = valid_moves[0]

        for col in valid_moves:
            new_board = simulate_move(board, col, opponent_piece)
            _, score = minimax(new_board, depth - 1, True, ai_piece, opponent_piece)

            if score < best_score:
                best_score = score
                best_col = col

        return (best_col, best_score)

# ============================================================================= Minimax WITH Alpha-Beta Pruning ============================================================================= #

def minimax_alpha_beta(
    board: list[list[int]],
    depth: int,
    alpha: float,
    beta: float,
    maximizing_player: bool,
    ai_piece: int,
    opponent_piece: int,
) -> tuple[int | None, int]:

    valid_moves = get_valid_moves(board)
    terminal = is_terminal_state(board)

    # --- Base cases: stop recursion ---

    if terminal:
        return (None, evaluate_terminal_state(board, ai_piece, opponent_piece))

    if depth == 0:
        return (None, score_position(board, ai_piece, opponent_piece))

    if not valid_moves:
        return (None, 0)

    ordered_moves = get_ordered_moves(valid_moves)

    # --- Recursive cases with pruning ---

    if maximizing_player:
        # AI's turn: maximize the score
        best_score = -math.inf
        best_col = ordered_moves[0]

        for col in ordered_moves:
            new_board = simulate_move(board, col, ai_piece)
            _, score = minimax_alpha_beta(
                new_board, depth - 1, alpha, beta, False, ai_piece, opponent_piece
            )

            if score > best_score:
                best_score = score
                best_col = col
            alpha = max(alpha, best_score)

            # Prune: the opponent already has a path that's better for them
            # than anything we could get here — stop searching this branch
            if alpha >= beta:
                break   # Beta cutoff
        return (best_col, best_score)

    else:
        # Opponent's turn: minimize the score
        best_score = math.inf
        best_col = ordered_moves[0]

        for col in ordered_moves:
            new_board = simulate_move(board, col, opponent_piece)
            _, score = minimax_alpha_beta(
                new_board, depth - 1, alpha, beta, True, ai_piece, opponent_piece
            )

            if score < best_score:
                best_score = score
                best_col = col

            # Update beta: `best_score` ( )
            beta = min(beta, best_score)

            # Prune: the AI already has a path that's better for it
           
            if alpha >= beta:
                break   

        return (best_col, best_score)
