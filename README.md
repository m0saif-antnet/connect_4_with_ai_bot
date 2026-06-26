# Intelligent Connect Four Player

## Project Overview
This project implements an **Intelligent Connect Four player** that plays against a human user.

The AI uses classic **Artificial Intelligence search techniques**:

- Minimax Algorithm
- Alpha-Beta Pruning
- Heuristic Evaluation

The goal is to create a smart game agent that analyzes the board and selects the best move.

---

# Connect Four Game

Connect Four is a **two-player strategy board game**.

### Board Size
- 6 rows
- 7 columns

### Game Rules
1. Players take turns dropping discs into columns.
2. Each disc falls to the **lowest available position** in that column.
3. The first player to connect **four discs in a row** wins.

Winning connections can be:
- Horizontal
- Vertical
- Diagonal

---

# AI Techniques Used

## Minimax Algorithm
Minimax is a decision-making algorithm used in two-player games with perfect information.

The algorithm:
- Simulates future moves
- Builds a **game tree**
- Chooses the move that maximizes the AI’s chance of winning.

---

## Alpha-Beta Pruning
Alpha-Beta pruning improves Minimax by:

- Skipping branches that will not affect the final result
- Reducing the number of explored nodes
- Making the search **much faster**

---

## Heuristic Evaluation
The heuristic function evaluates board states when the search depth limit is reached.

The evaluation considers:
- Number of connected AI pieces
- Potential winning opportunities
- Opponent threats
- Center column advantage

The function returns a **score representing how good the board state is for the AI**.

---

# Difficulty Levels

AI difficulty is controlled using **search depth**.

| Level | Depth |
|------|------|
| Easy | 1 |
| Medium | 2 |
| Hard | 3 |

Higher depth means:
- Stronger AI
- More computation time

---

# Project Structure

```text
connect4_project/
│
├── app.py
├── config.py
├── requirements.txt
│
├── game/
│   ├── board.py
│   ├── rules.py
│   └── game_state.py
│
├── ai/
│   ├── minimax.py
│   ├── heuristics.py
│   └── ai_player.py
│
├── templates/
│   ├── index.html
│   └── game.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── game.js
│
└── tests/
    ├── test_rules.py
    ├── test_heuristics.py
    └── test_minimax.py
```

---

# Installation

## Clone the repository

```bash
git clone https://github.com/M0SAIF-ANTNET/Connect_4_with_AI_bot
cd Connect_4_with_AI_bot
```

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Project

Start the Flask server:

```bash
python app.py
```

Then open your browser:

```text
[http://127.0.0.1:5000](http://127.0.0.1:5000)
```

---

# How the System Works

1. The player makes a move from the interface.
2. The frontend sends the board state to the backend.
3. The backend runs the AI algorithm.
4. Minimax explores possible moves.
5. Alpha-Beta pruning removes unnecessary branches.
6. The heuristic function evaluates board states.
7. The best move is returned to the frontend.
8. The board updates with the AI move.


---

# License

This project is developed for **educational purposes** as part of an Artificial Intelligence course.

---

# Authors

Artificial Intelligence Course Project
Faculty of Computer Science and Information Technology Helwan National University 
