# CheckMate Machine ♟️
IEEE-VIT's Chess Playground. Includes a Chess Engine, a working demo and some support tools for using it.

## Overview
CheckMate Machine is a compact toolkit created by IEEE-VIT that combines:
- A lightweight search-based chess engine,
- A demo 2D web UI for playing against the engine,
- A lightweight FastAPI backend that exposes the engine as an HTTP service,
- Vision & preprocessing helpers to take and convert board screenshots into FEN strings.

## Project Structure
- **`2DChessBoard`**: vision / preprocessing pipeline used to convert 2D screenshots into chessboard FEN input.
- **`Chess Engine`**: the engine implementation (board, move generation, minimax search)
- **`Demo/Frontend/`**: simple static demo (HTML, CSS and JS) that renders a board and can play single-player vs the engine.
- **`Demo/Backend/`**: backend FastAPI service that exposes `/engine/best_move`. 


## Quick Start
Get the demo running locally in two terminals: backend (engine API) and frontend (static site).

1) Create & activate a Python virtual environment (Optional, but recommended)

```bash
python -m venv .venv
# Windows
.\\.venv\\Scripts\\activate
# macOS / Linux
source .venv/bin/activate
```

2) Install dependencies

```bash
pip install -r requirements.txt
```

3) Run the backend (FastAPI + engine)

```bash
uvicorn Demo.Backend.main:app --reload --host 127.0.0.1 --port 8000
```

4) Serve the frontend (static)

```bash
# from repo root
python -m http.server 3000 --directory Demo/Frontend
# open http://localhost:3000 in your browser
```

### Using the Engine API
The backend exposes a single useful endpoint for the demo UI:

- POST `/engine/best_move` — request the engine's recommended move.

Request JSON body example:

```json
{
	"fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1",
	"side": "white",
	"depth": 2
}
```

Example curl test (from a terminal):

```bash
curl -X POST http://127.0.0.1:8000/engine/best_move \\
	-H "Content-Type: application/json" \\
	-d '{"fen":"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1","depth":2}'
```

Response format (JSON):

```json
{
	"from": "e2",
	"to": "e4",
	"stats": { "nodes_evaluated": 123, "depth": 2 }
}
```
