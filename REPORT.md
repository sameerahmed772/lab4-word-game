# Report - Lab 4 Word Game

## Objective

Improve the repository from an empty baseline into a complete and maintainable Python word game project.

## What Was Implemented

- Full CLI game flow with menu and replayable rounds
- Category-based word bank with custom hints
- Input validation for robust gameplay
- Scoring model based on remaining attempts
- Persistent stats (games played, wins, losses, total score, win rate)
- User-facing documentation in `README.md`

## Design Choices

- Used a small `Stats` dataclass to keep state explicit and easier to maintain.
- Kept gameplay logic in focused helper functions (`play_round`, `show_stats`, `choose_category`) to improve readability.
- Stored stats in JSON to avoid external dependencies.

## Quality Improvements

- Added graceful fallback if stats file is corrupted or missing.
- Prevented duplicate guesses and invalid inputs from breaking flow.
- Organized project documentation for easier onboarding.

## Next Steps

- Add automated tests for scoring and game-state transitions.
- Add optional word-list loading from external files.
- Add configurable max attempts/difficulty via CLI flags.
