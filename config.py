"""
Project configuration for the Connect Four AI system.

This file contains shared constants used across:
- route layer
- game layer
- AI layer
"""

# =========================
# Board Configuration
# =========================
ROWS: int = 6
COLS: int = 7
CONNECT_N: int = 4

# =========================
# Cell / Piece Values
# =========================
EMPTY: int = 0
HUMAN_PIECE: int = 1
AI_PIECE: int = 2

VALID_PIECES: set[int] = {EMPTY, HUMAN_PIECE, AI_PIECE}

# =========================
# Difficulty Configuration
# =========================
EASY_DEPTH: int = 2
MEDIUM_DEPTH: int = 4
HARD_DEPTH: int = 6

DIFFICULTY_DEPTH_MAP: dict[str, int] = {
    "easy": EASY_DEPTH,
    "medium": MEDIUM_DEPTH,
    "hard": HARD_DEPTH,
}

VALID_DIFFICULTIES: set[str] = set(DIFFICULTY_DEPTH_MAP.keys())

# =========================
# Algorithm Configuration
# =========================
DEFAULT_ALGORITHM: str = "alpha_beta"
VALID_ALGORITHMS: set[str] = {
    "minimax",
    "alpha_beta",
}

# =========================
# Default Gameplay Settings
# =========================
DEFAULT_DIFFICULTY: str = "medium"
DEFAULT_SEARCH_DEPTH: int = DIFFICULTY_DEPTH_MAP[DEFAULT_DIFFICULTY]

# =========================
# Flask Configuration
# =========================
DEBUG: bool = True
HOST: str = "127.0.0.1"
PORT: int = 5000
SECRET_KEY: str = "connect-four-dev-secret-key"

# =========================
# AI Evaluation Configuration
# =========================
AI_WIN_SCORE: int = 1_000_000
AI_LOSS_SCORE: int = -1_000_000
DRAW_SCORE: int = 0

CENTER_COLUMN_BONUS: int = 6
THREE_IN_A_ROW_SCORE: int = 50
TWO_IN_A_ROW_SCORE: int = 10
OPPONENT_THREE_THREAT_PENALTY: int = 80

# =========================
# Request / API Configuration
# =========================
MOVE_ENDPOINT: str = "/move"
HOME_ENDPOINT: str = "/"
GAME_PAGE_ENDPOINT: str = "/game"

# =========================
# Validation Helpers
# =========================
def get_depth_for_difficulty(difficulty: str) -> int:
    """
    Return the search depth for a given difficulty.
    Falls back to the default difficulty if the input is invalid.
    """
    normalized = (difficulty or "").strip().lower()
    return DIFFICULTY_DEPTH_MAP.get(normalized, DEFAULT_SEARCH_DEPTH)


def is_valid_difficulty(difficulty: str) -> bool:
    """
    Check whether the provided difficulty is supported.
    """
    return (difficulty or "").strip().lower() in VALID_DIFFICULTIES


def is_valid_algorithm(algorithm: str) -> bool:
    """
    Check whether the provided algorithm is supported.
    """
    return (algorithm or "").strip().lower() in VALID_ALGORITHMS


def normalize_difficulty(difficulty: str) -> str:
    """
    Normalize difficulty input and return a safe value.
    """
    normalized = (difficulty or "").strip().lower()
    return normalized if normalized in VALID_DIFFICULTIES else DEFAULT_DIFFICULTY


def normalize_algorithm(algorithm: str) -> str:
    """
    Normalize algorithm input and return a safe value.
    """
    normalized = (algorithm or "").strip().lower()
    return normalized if normalized in VALID_ALGORITHMS else DEFAULT_ALGORITHM