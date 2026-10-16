# Progress

Implemented the initial playable two-player UI, move hints, promotion chooser,
undo, restart and game status. Setup instructions are in the root README.md.
Validation: `python3 -m py_compile main.py` passed on Python 3.14.6.
A local .venv was created, but dependency installation failed because pypi.org
could not be resolved in this environment. Runtime and visual checks remain
unverified at initial creation. Saved games are absent.

After a user-reported pygame 2.6.1 source-build failure (missing SDL.h on
Python 3.14), requirements now select pygame-ce >=2.5.7. PyPI confirms a
CPython 3.14 macOS universal2 wheel for 2.5.7. Installation remains unverified
in the restricted agent environment. Existing user-created pyproject.toml and
uv.lock are unchanged; requirements.txt remains the documented setup source.

Added Bot/Duo setup, three difficulty levels, color selection, black orientation,
background bot search, stale-result protection and paired undo in bot mode.
Dependencies are now installed in .venv (pygame-ce 2.5.8 and chess 1.11.2).
Four unittest checks passed: legal bot moves with unchanged search input,
mate-in-one and terminal positions, all-square coordinate round trips for both
orientations, and a dummy-display menu/Duo/undo/menu event-loop smoke check.
Native graphical appearance and interactive bot play remain unverified.
