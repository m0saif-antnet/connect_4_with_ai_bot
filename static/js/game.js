const ROWS = 6;
const COLS = 7;

// Game pieces
const EMPTY = 0;
const HUMAN_PIECE = 1;
const AI_PIECE = 2;

let board = [];
let gameOver = false;
let isAiThinking = false;
let lastAiMove = null;
let winningCells = [];
const boardElement = document.getElementById("board");
const statusMessageElement = document.getElementById("status-message");
const restartButton = document.getElementById("restart-button");
const restartModal = document.getElementById("restart-modal");
const restartMatchBtn = document.getElementById("restart-match-btn");
const changeSettingsBtn = document.getElementById("change-settings-btn");
const cancelBtn = document.getElementById("cancel-btn");
const urlParams = new URLSearchParams(window.location.search);
const difficultySelect = {
  value: urlParams.get("difficulty") || "medium"
};

const algorithmSelect = {
  value: urlParams.get("algorithm") || "alpha_beta"
};

const infoAlgorithm = document.getElementById("info-algorithm");
const infoDifficulty = document.getElementById("info-difficulty");
const infoColumn = document.getElementById("info-column");
const infoScore = document.getElementById("info-score");
const infoDepth = document.getElementById("info-depth");

const humanSound = new Audio("/static/sounds/human.wav");
const aiSound = new Audio("/static/sounds/ai.wav");
const winSound = new Audio("/static/sounds/win.wav");

function createEmptyBoard() {
  return Array.from({ length: ROWS }, () => Array(COLS).fill(EMPTY));
}

function initializeGame() {
  board = createEmptyBoard();
  gameOver = false;
  isAiThinking = false;
  lastAiMove = null;
  winningCells = [];

  updateStatusMessage("Your turn");
  resetAiInfo();
  renderBoard(board);
  syncSettingsInfo();
}

function renderBoard(currentBoard) {
  boardElement.innerHTML = "";

  for (let row = 0; row < ROWS; row++) {
    for (let col = 0; col < COLS; col++) {
      const cell = document.createElement("div");
      cell.classList.add("cell");
      cell.dataset.row = row;
      cell.dataset.col = col;

      if (currentBoard[row][col] === HUMAN_PIECE) {
        cell.classList.add("player-one");
      } else if (currentBoard[row][col] === AI_PIECE) {
        cell.classList.add("player-two");
      }
      if (
        lastAiMove &&
        lastAiMove.row === row &&
        lastAiMove.col === col
      ) {
        cell.classList.add("last-move");
      }

      if (gameOver || isAiThinking) {
        cell.classList.add("disabled");
      }
      if (
      winningCells.some(c => c.row === row && c.col === col)
      ) {
        cell.classList.add("winning-cell");
      }
      cell.addEventListener("click", handleCellClick);
      boardElement.appendChild(cell);
    }
  }
}

function handleCellClick(event) {
  if (gameOver || isAiThinking) return;
  lastAiMove = null;
  const col = getColumnFromClick(event);
  if (col === null) return;

  const row = applyFrontendMove(board, col, HUMAN_PIECE);
  const success = row !== null;
  if (!success) {
    updateStatusMessage("Invalid move. Please choose another column.");
    return;
  }

  renderBoard(board);
  const humanWin = checkWin(board, HUMAN_PIECE);
  if (humanWin) {
    winningCells = humanWin;
    lastAiMove = null;
    gameOver = true;
    winSound.play();
    launchConfetti();
    updateStatusMessage("You win!");
    renderBoard(board);
    return;
  }

  if (isBoardFull(board)) {
    gameOver = true;
    updateStatusMessage("Draw game.");
    renderBoard(board);
    return;
  }
  isAiThinking = true;
  updateStatusMessage("AI is thinking...");
  renderBoard(board);

  setTimeout(() => {
    sendAiMoveRequest(
      board,
      difficultySelect.value,
      algorithmSelect.value
    );
  }, 600);
}

function getColumnFromClick(event) {
  const col = event.target.dataset.col;
  if (col === undefined) return null;
  return Number(col);
}

function findAvailableRow(currentBoard, col) {
  for (let row = ROWS - 1; row >= 0; row--) {
    if (currentBoard[row][col] === EMPTY) {
      return row;
    }
  }
  return null;
}
 
function applyFrontendMove(currentBoard, col, piece) {
  if (col < 0 || col >= COLS) return null;

  const row = findAvailableRow(currentBoard, col);
  if (row === null) return null;

  currentBoard[row][col] = piece;

  if (piece === HUMAN_PIECE) {
    humanSound.play();
  }

  return row;
}

async function sendAiMoveRequest(currentBoard, difficulty, algorithm) {
  try {
    const response = await fetch("https://connect4withaibot-production.up.railway.app" , {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        board: currentBoard,
        difficulty: difficulty,
        algorithm: algorithm
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Failed to get AI move.");
    }

    handleAiResponse(data);
  } catch (error) {
    updateStatusMessage(
      error.message || "An error occurred while contacting the server."
    );
    isAiThinking = false;
    renderBoard(board);
  }
}

function handleAiResponse(responseData) {
  const aiCol = responseData.column;

  if (aiCol === null || aiCol === undefined) {
    gameOver = true;
    isAiThinking = false;
    updateStatusMessage("No valid AI move available.");
    renderBoard(board);
    return;
  }

  const aiRow = applyFrontendMove(board, aiCol, AI_PIECE);
  lastAiMove = { row: aiRow, col: aiCol };
  aiSound.play();

  isAiThinking = false;

  renderBoard(board);
  updateAiInfo(responseData);

  const aiWin = checkWin(board, AI_PIECE);
  if (aiWin) {
    winningCells = aiWin;
    lastAiMove = null;
    gameOver = true;
    winSound.play();
    shakeScreen();
    updateStatusMessage(`AI wins. Column ${aiCol}`);
    renderBoard(board);
    return;
  }

  if (isBoardFull(board)) {
    gameOver = true;
    updateStatusMessage("Draw game.");
    renderBoard(board);
    return;
  }

  updateStatusMessage(`Your turn. AI played column ${aiCol}`);
}

// Win effect
function launchConfetti() {
  for (let i = 0; i < 60; i++) {
    const c = document.createElement("div");
    c.classList.add("confetti");
    c.style.left = Math.random() * 100 + "vw";
    document.body.appendChild(c);
    setTimeout(() => c.remove(), 3000);
  }
}
// Lose effect
function shakeScreen() {
  document.body.classList.add("shake");
  setTimeout(() => document.body.classList.remove("shake"), 500);
}
function updateStatusMessage(message) {
  statusMessageElement.textContent = message;
}

function restartGame() {
  initializeGame();
}

function syncSettingsInfo() {
  infoAlgorithm.textContent = algorithmSelect.value;
  infoDifficulty.textContent = difficultySelect.value;
}

function updateAiInfo(details) {
  infoAlgorithm.textContent = details.algorithm ?? algorithmSelect.value;
  infoDifficulty.textContent = details.difficulty ?? difficultySelect.value;
  infoColumn.textContent = details.column ?? "-";
  infoScore.textContent = details.score ?? "-";
  infoDepth.textContent = details.depth ?? "-";
}

function resetAiInfo() {
  infoColumn.textContent = "-";
  infoScore.textContent = "-";
  infoDepth.textContent = "-";
  syncSettingsInfo();
}

function isBoardFull(currentBoard) {
  return currentBoard[0].every(cell => cell !== EMPTY);
}

function checkWin(currentBoard, piece) {
  return (
    checkHorizontalWin(currentBoard, piece) ||
    checkVerticalWin(currentBoard, piece) ||
    checkPositiveDiagonalWin(currentBoard, piece) ||
    checkNegativeDiagonalWin(currentBoard, piece)
  );
}

function checkHorizontalWin(currentBoard, piece) {
  for (let row = 0; row < ROWS; row++) {
    for (let col = 0; col < COLS - 3; col++) {
      if (
        currentBoard[row][col] === piece &&
        currentBoard[row][col + 1] === piece &&
        currentBoard[row][col + 2] === piece &&
        currentBoard[row][col + 3] === piece
      ) {
        return [
          { row, col },
          { row, col: col + 1 },
          { row, col: col + 2 },
          { row, col: col + 3 }
        ];
      }
    }
  }
  return null;
}

function checkVerticalWin(currentBoard, piece) {
  for (let col = 0; col < COLS; col++) {
    for (let row = 0; row < ROWS - 3; row++) {
      if (
        currentBoard[row][col] === piece &&
        currentBoard[row + 1][col] === piece &&
        currentBoard[row + 2][col] === piece &&
        currentBoard[row + 3][col] === piece
      ) {
        return [
          { row, col },
          { row: row + 1, col },
          { row: row + 2, col },
          { row: row + 3, col }
        ];
      }
    }
  }
  return null;
}

function checkPositiveDiagonalWin(currentBoard, piece) {
  for (let row = 3; row < ROWS; row++) {
    for (let col = 0; col < COLS - 3; col++) {
      if (
        currentBoard[row][col] === piece &&
        currentBoard[row - 1][col + 1] === piece &&
        currentBoard[row - 2][col + 2] === piece &&
        currentBoard[row - 3][col + 3] === piece
      ) {
        return [
          { row, col },
          { row: row - 1, col: col + 1 },
          { row: row - 2, col: col + 2 },
          { row: row - 3, col: col + 3 }
        ];
      }
    }
  }
  return null;
}

function checkNegativeDiagonalWin(currentBoard, piece) {
  for (let row = 0; row < ROWS - 3; row++) {
    for (let col = 0; col < COLS - 3; col++) {
      if (
        currentBoard[row][col] === piece &&
        currentBoard[row + 1][col + 1] === piece &&
        currentBoard[row + 2][col + 2] === piece &&
        currentBoard[row + 3][col + 3] === piece
      ) {
        return [
          { row, col },
          { row: row + 1, col: col + 1 },
          { row: row + 2, col: col + 2 },
          { row: row + 3, col: col + 3 }
        ];
      }
    }
  }
  return null;
}
function launchConfetti() {
  const colors = ["#facc15", "#ef4444", "#22c55e", "#3b82f6", "#a855f7"];

  for (let i = 0; i < 80; i++) {
    const confetti = document.createElement("div");
    confetti.classList.add("confetti");
    confetti.style.left = Math.random() * 100 + "vw";
    confetti.style.background =
      colors[Math.floor(Math.random() * colors.length)];
    confetti.style.animationDuration =
      (Math.random() * 2 + 1) + "s";

    document.body.appendChild(confetti);

    setTimeout(() => confetti.remove(), 3000);
  }
}
// Open popup instead of instant restart
restartButton.addEventListener("click", () => {
  restartModal.classList.remove("hidden");
});

// Restart match (same settings)
restartMatchBtn.addEventListener("click", () => {
  restartModal.classList.add("hidden");
  restartGame();
});


changeSettingsBtn.addEventListener("click", () => {
  window.location.href = "/settings"; 
});

cancelBtn.addEventListener("click", () => {
  restartModal.classList.add("hidden");
});
initializeGame();