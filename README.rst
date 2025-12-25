ChronosChess
============

**ChronosChess** is a modern, feature-rich Python Chess application built with **Pygame** and **python-chess**. It integrates the powerful **Stockfish** engine for AI play and features a unique "Time Travel" system to review and branch game history.

Features
--------

- **AI Opposition**: Play against the Stockfish engine (auto-detected).
- **Time Travel**: Use Arrow Keys to navigate history (Undo/Redo). Making a move in the past creates a new timeline!
- **Visual Aids**:
    - **Colored Scopes**: 
        - **Blue Lines/Heatmap**: Player control.
        - **Red Lines/Heatmap**: Opponent threat.
    - **Move Highlighting**: Last move and selected piece.
- **Audio Feedback**: Subtle sound effects for moves.
- **Smart UI**: Game Over overlays and "New Game" restart.
- **Hotseat Mode**: Falls back to Player vs Player if no engine is found.

Installation
------------

1.  **Clone or Download** the repository.
2.  Install dependencies:

    .. code-block:: bash

        pip install -r requirements.txt

3.  (Optional) Place a Stockfish executable in a ``stockfish/`` folder if you want AI to play.

Usage
-----

Run the game with:

.. code-block:: bash

    python main.py

Controls
^^^^^^^^

- **Mouse Left-Click**: Select and move pieces.
- **Left Arrow**: Undo / Go Backward in time.
- **Right Arrow**: Redo / Go Forward in time.
- **New Game Button**: Appears when checkmate/stalemate occurs.

Requirements
------------

- Python 3.8+
- pygame
- python-chess

Credits
-------

Developed as a custom Python project.
Uses `Stockfish <https://stockfishchess.org/>`_ for AI.
