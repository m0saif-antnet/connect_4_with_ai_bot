const ROWS = 6;
const COLS = 7;
const EMPTY = 0;
const HUMAN_PIECE = 1;
const AI_PIECE = 2;
let timeLeft = 10;  // time allowed per turn (in seconds)
let timerInterval = null; // stores the interval so we can stop it later
let board = [];
let gameOver = false;
let isAiThinking = false;

const boardElement = document.getElementById("board");
const statusMessageElement = document.getElementById("status-message");
const restartButton = document.getElementById("restart-button");
const difficultySelect = document.getElementById("difficulty-select");
const algorithmSelect = document.getElementById("algorithm-select");

const infoAlgorithm = document.getElementById("info-algorithm");
const infoDifficulty = document.getElementById("info-difficulty");
const infoColumn = document.getElementById("info-column");
const infoScore = document.getElementById("info-score");
const infoDepth = document.getElementById("info-depth");
const humanSound = new Audio("/static/sounds/human.wav"); // sound when human player makes a move
const aiSound = new Audio("/static/sounds/ai.wav");   // sound when AI makes a move
const winSound = new Audio("/static/sounds/win.wav"); // sound when a player wins

function startTimer() {
  stopTimer(); // clear any existing timer before starting a new one

  timeLeft = 10; // reset timer to 10 seconds
  updateTimerUI(); // update timer display on screen

  timerInterval = setInterval(() => {
    timeLeft--; // decrease time every second
    updateTimerUI();  // update UI

    if (timeLeft <= 0) {   // if time runs out
      stopTimer();     // stop the timer
      updateStatusMessage("Time is up ⏰");  // show message to player 
    }
  }, 1000);   // runs every 1 second
}

function stopTimer() { 
  if (timerInterval) {
    clearInterval(timerInterval);   // stop the interval
    timerInterval = null;    // reset variable
  }
}

function updateTimerUI() {
  const timerElement = document.getElementById("timer");

  timerElement.textContent = "Time: " + timeLeft;  // display remaining time

  if (timeLeft <= 3) {
    timerElement.style.color = "red";  // change color when time is running low to red color
  } else {
    timerElement.style.color = "#facc15"; // yellow color
  }
}
function createEmptyBoard() {
  return Array.from({ length: ROWS }, () => Array(COLS).fill(EMPTY));
}

function initializeGame() {
  board = createEmptyBoard();
  gameOver = false;
  isAiThinking = false;
  
  updateStatusMessage("Your turn");
  resetAiInfo();
  renderBoard(board);
  syncSettingsInfo();
    startTimer();
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

      if (gameOver || isAiThinking) {
        cell.classList.add("disabled");
      }

      cell.addEventListener("click", handleCellClick);
      boardElement.appendChild(cell);
    }
  }
}

function handleCellClick(event) {
  if (gameOver || isAiThinking) return;

  const col = getColumnFromClick(event);
  if (col === null) return;

  const success = applyFrontendMove(board, col, HUMAN_PIECE);
  if (!success) {
    updateStatusMessage("Invalid move. Please choose another column.");
    return;
  }

  renderBoard(board);

  startTimer();

  if (checkWin(board, HUMAN_PIECE)) {
    gameOver = true;
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

  sendAiMoveRequest(board, difficultySelect.value, algorithmSelect.value);
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
  if (col < 0 || col >= COLS) return false;

  const row = findAvailableRow(currentBoard, col);
  if (row === null) return false;

  currentBoard[row][col] = piece;
    if (piece === HUMAN_PIECE) {
    humanSound.play();  // play sound when human makes a move
  }
  return true;
}

async function sendAiMoveRequest(currentBoard, difficulty, algorithm) {
  try {
    const response = await fetch("/move", {
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
    updateStatusMessage(error.message || "An error occurred while contacting the server.");
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

  applyFrontendMove(board, aiCol, AI_PIECE);
   aiSound.play();  // play sound when AI makes a move
  isAiThinking = false;

  renderBoard(board);
  updateAiInfo(responseData);

  if (checkWin(board, AI_PIECE)) {
    gameOver = true;
    winSound.play();  // play sound when a player wins the game
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

  startTimer();
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
        return true;
      }
    }
  }
  return false;
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
        return true;
      }
    }
  }
  return false;
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
        return true;
      }
    }
  }
  return false;
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
        return true;
      }
    }
  }
  return false;
}

restartButton.addEventListener("click", restartGame);
difficultySelect.addEventListener("change", syncSettingsInfo);
algorithmSelect.addEventListener("change", syncSettingsInfo);

initializeGame();