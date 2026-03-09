# Lab 4 - Guess the Word (Professional Edition)

A polished desktop Guess the Word game built with Python and Tkinter.

## Highlights

- Professional graphical interface (card layout, action bar, status feedback)
- On-screen keyboard plus direct text input
- Category selector (`animals`, `technology`, `geography`)
- Difficulty modes (`Easy`, `Medium`, `Hard`) with adaptive attempts, timer, and scoring
- Live round timer with automatic loss on timeout
- Hint system with score penalty
- Persistent advanced stats:
	- games played, wins, losses, win rate
	- total score, best score
	- current streak, best streak
- Stats reset action for clean practice sessions

## Requirements

- Python 3.9+
- Tkinter (included in standard Python distribution on most systems)

## Run

```bash
python3 main.py
```

## Gameplay

1. Select a category and difficulty.
2. Click `Start New Round`.
3. Guess letters using keyboard buttons or by typing a letter and pressing Enter.
4. Optionally use one hint (penalty applies).
5. Win before attempts run out or timer reaches zero.

## Scoring Model

- Base score uses remaining attempts and selected difficulty multiplier.
- Time bonus rewards faster solutions.
- Hint usage applies difficulty-specific penalty.
- Minimum score per round is `0`.

## Project Files

- `main.py`: complete Tkinter app and game logic
- `README.md`: setup and usage guide
- `REPORT.md`: technical implementation summary
- `JOURNAL.md`: interaction/change history

## Potential Next Enhancements

- Unit and integration tests for game logic
- External word-pack loading from JSON files
- Multiplayer local profiles and leaderboard view
