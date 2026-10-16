# Architecture

main.py owns the event loop, setup menu, board orientation, rendering, selection
and promotion UI. A single ThreadPoolExecutor runs bot searches on board copies.
A generation counter discards results after undo, restart or opening the menu.
bot.py owns random easy moves and time-bounded iterative negamax/alpha-beta
search for medium/hard levels. Evaluation uses material and centrality.
python-chess owns board state, move legality and game outcomes.
pyproject.toml declares pygame-ce (imported as pygame) and python-chess;
uv.lock pins dependencies. uv manages Python 3.14+ and the local .venv.
Pieces use system Unicode fonts
with a letter fallback; no external image assets are required.
