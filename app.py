from flask import Flask, jsonify, render_template, request

from config import (
    AI_PIECE,
    DEFAULT_ALGORITHM,
    DEFAULT_DIFFICULTY,
    DEBUG,
    GAME_PAGE_ENDPOINT,
    HOME_ENDPOINT,
    HOST,
    HUMAN_PIECE,
    MOVE_ENDPOINT,
    PORT,
    normalize_algorithm,
    normalize_difficulty,
)
from ai.ai_player import AIPlayer


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route(HOME_ENDPOINT, methods=["GET"])
    def home():
        return render_template("index.html")
    @app.route("/settings")
    def settings_page():
        return render_template("settings.html")
    @app.route(GAME_PAGE_ENDPOINT, methods=["GET"])
    def game_page():
        return render_template("game.html")

    @app.route(MOVE_ENDPOINT, methods=["POST"])
    def get_ai_move():
        data = request.get_json(silent=True)

        is_valid, error_message = validate_move_request(data)
        if not is_valid:
            return build_error_response(error_message, 400)

        board = data["board"]
        difficulty = normalize_difficulty(data.get("difficulty", DEFAULT_DIFFICULTY))
        algorithm = normalize_algorithm(data.get("algorithm", DEFAULT_ALGORITHM))

        ai_player = AIPlayer(
            ai_piece=AI_PIECE,
            opponent_piece=HUMAN_PIECE,
            difficulty=difficulty,
            algorithm=algorithm,
        )

        result = ai_player.choose_move_with_details(board)

        if result["column"] is None:
            return build_error_response("No valid moves available.", 400)

        return jsonify(build_move_response(result["column"], result))

    return app


def validate_move_request(data: dict | None) -> tuple[bool, str | None]:
    if data is None:
        return False, "Request body must be valid JSON."

    if "board" not in data:
        return False, "Missing required field: board."

    board = data["board"]

    if not isinstance(board, list):
        return False, "Board must be a 2D list."

    if len(board) != 6:
        return False, "Board must contain exactly 6 rows."

    for row in board:
        if not isinstance(row, list):
            return False, "Each board row must be a list."
        if len(row) != 7:
            return False, "Each board row must contain exactly 7 columns."
        for cell in row:
            if cell not in {0, 1, 2}:
                return False, "Board cells must only contain 0, 1, or 2."

    return True, None


def build_move_response(column: int, details: dict | None = None) -> dict:
    response = {"column": column}
    if details:
        response.update(
            {
                "score": details.get("score"),
                "depth": details.get("depth"),
                "algorithm": details.get("algorithm"),
                "difficulty": details.get("difficulty"),
            }
        )
    return response


def build_error_response(message: str, status_code: int = 400):
    return jsonify({"error": message}), status_code


app = create_app()

if __name__ == "__main__":
    app.run(debug=DEBUG, host=HOST, port=PORT)