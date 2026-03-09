# Lab 4 - Word Game

A command-line word guessing game written in Python.

## Features

- Multiple categories (`animals`, `technology`, `geography`)
- Hint system (one hint per round)
- Score system based on remaining attempts
- Persistent player stats stored locally in `game_stats.json`
- Simple menu for play/stats/quit

## Requirements

- Python 3.9+

## Run

```bash
python3 main.py
```

## How To Play

1. Choose `Play` from the menu.
2. Pick a category.
3. Guess letters one by one.
4. Type `hint` once per round if you need help.
5. Win by revealing the full word before attempts reach 0.

## Scoring

- Base score: `attempts_left * 10`
- If you use a hint: `-10` penalty
- Score floor: `0`

## Project Structure

- `main.py`: game logic and CLI
- `README.md`: usage instructions
- `REPORT.md`: implementation summary
- `JOURNAL.md`: interaction/change log

## Future Improvements

- Add difficulty levels and custom word lists
- Add unit tests for core functions
- Add leaderboard for multiple players
