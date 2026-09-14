import logging
import os

from fastapi import FastAPI, HTTPException
from fastapi import Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

try:
	# When running as a package (for example: `uvicorn Demo.Backend.main:app`)
	# use a relative import so Python finds the module inside the same package.
	from .chess_engine_v01 import find_best_move_for_fen
except Exception:
	# Fallback to absolute import when running the file directly from Demo/Backend
	from chess_engine_v01 import find_best_move_for_fen


class BestMoveRequest(BaseModel):
	fen: str
	side: Optional[str] = None
	depth: Optional[int] = 4


app = FastAPI(title="Checkmate Engine API")

DEFAULT_CORS_ORIGINS = [
	"http://localhost:3000",
	"http://127.0.0.1:3000",
]


def get_cors_origins():
	configured_origins = os.getenv("CORS_ORIGINS")
	if not configured_origins:
		logging.warning(
			"CORS_ORIGINS is not set; allowing local development origins: %s",
			", ".join(DEFAULT_CORS_ORIGINS),
		)
		return DEFAULT_CORS_ORIGINS

	origins = [origin.strip() for origin in configured_origins.split(",") if origin.strip()]
	if not origins:
		logging.warning(
			"CORS_ORIGINS is empty; allowing local development origins: %s",
			", ".join(DEFAULT_CORS_ORIGINS),
		)
		return DEFAULT_CORS_ORIGINS

	return origins


origins = get_cors_origins()


@app.middleware("http")
async def warn_if_cors_origin_blocked(request: Request, call_next):
	origin = request.headers.get("origin")
	if origin and origin not in origins:
		logging.warning(
			"CORS request from blocked origin %s; configure CORS_ORIGINS to allow it",
			origin,
		)
	return await call_next(request)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
	return {"status": "ok", "msg": "Checkmate engine running"}


@app.post("/engine/best_move")
def engine_best_move(req: BestMoveRequest):
	# Validate depth
	depth = req.depth if req.depth is not None else 3
	if depth <= 0 or depth > 6:
		# limit depth for safety
		raise HTTPException(status_code=400, detail="depth must be between 1 and 6")

	try:
		best, stats = find_best_move_for_fen(req.fen, side_input=req.side, depth=depth)
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

	if not best:
		return {"from": None, "to": None, "error": "no legal moves", "stats": stats}

	(r1, c1), (r2, c2) = best
	# convert to algebraic: file = a-h => chr(97 + c), rank = 8 - r
	from_sq = f"{chr(97 + c1)}{8 - r1}"
	to_sq = f"{chr(97 + c2)}{8 - r2}"

	return {"from": from_sq, "to": to_sq, "stats": stats}

