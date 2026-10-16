# Decisions

- 2026-10-14: Add a self-contained bot rather than requiring an external engine.
  Easy uses random moves; medium/hard use bounded searches. Search runs in one
  worker on copied state so rendering continues. Generation checks reject stale
  results after game controls. Bot undo returns to the human's previous turn.

- 2026-10-14: Replace the original pygame distribution with pygame-ce >=2.5.7
  for prebuilt CPython 3.14 macOS universal2 wheels. The pygame import stays
  unchanged. This supersedes the initial graphics dependency selection.

- 2026-10-14: Use python-chess for complete move legality and outcomes, avoiding
  a separate rule implementation. Use Pygame for a local two-player interface.
- 2026-10-14: Automatically accept claimable draws using claim_draw=True.
  This simplifies local play; there is no separate draw-claim button.
