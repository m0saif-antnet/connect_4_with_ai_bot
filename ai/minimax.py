# i tried to leave some important comments for Yasser, Gad, Abdo and shon (if needed) to make it easier to understand before push it in GIThub (a7la klam wallahi :)) 
#
import math

from heuristics import score_position

from game.board import (
    copy_board,
    apply_move,
    get_valid_moves,
    winning_move,
    is_terminal_state,
    get_winner,
)


# =============================================================================
# HELPERS 
# =============================================================================

def evaluate_terminal_state(board: list[list[int]], ai_piece: int, opponent_piece: int) -> int:
    """
    Return a score for a board that has reached a terminal state (game over).

    """
    winner = get_winner(board)

    if winner == ai_piece:
        return 100_000        
    elif winner == opponent_piece:
        return -100_000      
    else:
        return 0              


def simulate_move(board: list[list[int]], col: int, piece: int) -> list[list[int]]:
    
    """
    Create a copy of the board with one new move applied.

    """
    new_board = copy_board(board)
    apply_move(new_board, col, piece)
    return new_board

########## CHECK AGAIN  ya gd3an re5ma 7bten k'logic 

def get_ordered_moves(valid_moves: list[int]) -> list[int]:
    """
    Reorder valid moves so that center columns are tried first.
    """
    center = 3  # Center column of a standard 7-column board

    # Sort by distance from center (closest to center = tried first)
    return sorted(valid_moves, key=lambda col: abs(center - col))


# =============================================================================
# VERSION 1: Basic Minimax () 3shan n3ml test w nfhm el algorithm without "any pruning "YET" ) RE5MA 7bten :( 3shan kda 7bet aseb Comments 3shan el fehm eb2a a7sn 
# =============================================================================

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
        # AI's turn: byshoof a7san move with the HIGHEST score ( just looking for it not not playing it yet )
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


# =============================================================================

# VERSION 2: Minimax WITH Alpha-Beta Pruning (de b2a WITH pruning we bnst5demha fe el Game , much faster )

# =============================================================================

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

    # Try center columns first ( more pruning y3ny kda el Ai has found the path thats better for it ) the same goes for the oppenent BTW 
    # ALPHA Y3NY = AI 
    # Beta y3ny = opponent

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

            # Update alpha: the AI now knows it can get at least `best_score`
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