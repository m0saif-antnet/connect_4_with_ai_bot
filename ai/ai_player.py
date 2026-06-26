from config import (
    DEFAULT_ALGORITHM,
    DEFAULT_DIFFICULTY,
    get_depth_for_difficulty,
    normalize_algorithm,
    normalize_difficulty,
)
from ai.minimax import minimax, minimax_alpha_beta


def get_depth_from_difficulty(difficulty: str) -> int:
    return get_depth_for_difficulty(difficulty)


class AIPlayer:
    def __init__(
        self,
        ai_piece: int,
        opponent_piece: int,
        difficulty: str = DEFAULT_DIFFICULTY,
        algorithm: str = DEFAULT_ALGORITHM,
    ) -> None:
        self.ai_piece = ai_piece
        self.opponent_piece = opponent_piece
        self.difficulty = normalize_difficulty(difficulty)
        self.algorithm = normalize_algorithm(algorithm)
        self.depth = get_depth_from_difficulty(self.difficulty)

    def set_difficulty(self, difficulty: str) -> None:
        self.difficulty = normalize_difficulty(difficulty)
        self.depth = get_depth_from_difficulty(self.difficulty)

    def set_algorithm(self, algorithm: str) -> None:
        self.algorithm = normalize_algorithm(algorithm)

    def choose_move(self, board: list[list[int]]) -> int | None:
        result = self.choose_move_with_details(board)
        return result["column"]

    def choose_move_with_details(self, board: list[list[int]]) -> dict:
        if self.algorithm == "minimax":
            best_col, best_score = minimax(
                board=board,
                depth=self.depth,
                maximizing_player=True,
                ai_piece=self.ai_piece,
                opponent_piece=self.opponent_piece,
            )
        else:
            best_col, best_score = minimax_alpha_beta(
                board=board,
                depth=self.depth,
                alpha=float("-inf"),
                beta=float("inf"),
                maximizing_player=True,
                ai_piece=self.ai_piece,
                opponent_piece=self.opponent_piece,
            )

        return {
            "column": best_col,
            "score": best_score,
            "depth": self.depth,
            "algorithm": self.algorithm,
            "difficulty": self.difficulty,
        } 