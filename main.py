"""Guess the Word desktop game with a polished Tkinter UI.

Run with: python3 main.py
"""

from __future__ import annotations

import json
import random
import string
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import ttk


STATS_FILE = Path("game_stats.json")


WORD_BANK: dict[str, list[dict[str, str]]] = {
    "animals": [
        {"word": "elephant", "hint": "Largest land mammal"},
        {"word": "giraffe", "hint": "Tall animal with a long neck"},
        {"word": "dolphin", "hint": "Intelligent marine mammal"},
        {"word": "kangaroo", "hint": "Australian marsupial that jumps"},
        {"word": "penguin", "hint": "Flightless bird from icy regions"},
    ],
    "technology": [
        {"word": "python", "hint": "Popular programming language"},
        {"word": "algorithm", "hint": "Step-by-step problem-solving method"},
        {"word": "database", "hint": "Organized collection of data"},
        {"word": "compiler", "hint": "Converts source code to machine code"},
        {"word": "firewall", "hint": "Protects a network from threats"},
    ],
    "geography": [
        {"word": "sahara", "hint": "World's largest hot desert"},
        {"word": "himalaya", "hint": "Mountain range with Everest"},
        {"word": "amazon", "hint": "World's largest rainforest"},
        {"word": "pacific", "hint": "Largest ocean on Earth"},
        {"word": "andes", "hint": "Longest continental mountain range"},
    ],
}


@dataclass
class Stats:
    played: int = 0
    won: int = 0
    total_score: int = 0
    best_score: int = 0
    current_streak: int = 0
    best_streak: int = 0

    @property
    def lost(self) -> int:
        return self.played - self.won

    @property
    def win_rate(self) -> float:
        if self.played == 0:
            return 0.0
        return (self.won / self.played) * 100


@dataclass(frozen=True)
class DifficultyConfig:
    attempts: int
    round_time: int
    hint_penalty: int
    score_multiplier: float


DIFFICULTIES: dict[str, DifficultyConfig] = {
    "Easy": DifficultyConfig(attempts=8, round_time=90, hint_penalty=8, score_multiplier=1.0),
    "Medium": DifficultyConfig(attempts=7, round_time=75, hint_penalty=10, score_multiplier=1.3),
    "Hard": DifficultyConfig(attempts=6, round_time=60, hint_penalty=15, score_multiplier=1.6),
}


@dataclass
class RoundState:
    word: str = ""
    hint: str = ""
    attempts_left: int = 0
    max_attempts: int = 0
    seconds_left: int = 0
    guessed_letters: set[str] | None = None
    wrong_letters: set[str] | None = None
    hint_used: bool = False
    active: bool = False

    def __post_init__(self) -> None:
        self.guessed_letters = set() if self.guessed_letters is None else self.guessed_letters
        self.wrong_letters = set() if self.wrong_letters is None else self.wrong_letters


class GuessTheWordApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Guess the Word - Pro")
        self.geometry("980x700")
        self.minsize(920, 640)
        self.configure(bg="#f4f7fb")

        self.stats = self.load_stats()
        self.round_state = RoundState()
        self.timer_job: str | None = None
        self.keyboard_buttons: dict[str, ttk.Button] = {}

        self._create_styles()
        self._create_layout()
        self._bind_keys()
        self._refresh_stats_panel()
        self._set_status("Select category and difficulty, then start a round.", "info")

    def _create_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("Card.TFrame", background="#ffffff")
        style.configure("Header.TLabel", font=("Avenir Next", 26, "bold"), foreground="#12365f", background="#f4f7fb")
        style.configure("SubHeader.TLabel", font=("Avenir Next", 11), foreground="#4b647c", background="#f4f7fb")
        style.configure("Body.TLabel", font=("Avenir Next", 12), foreground="#1f2b3a", background="#ffffff")
        style.configure("Status.TLabel", font=("Avenir Next", 12, "bold"), foreground="#2b4f72", background="#ffffff")
        style.configure("Word.TLabel", font=("Menlo", 32, "bold"), foreground="#0d3b66", background="#ffffff")
        style.configure("StatValue.TLabel", font=("Avenir Next", 16, "bold"), foreground="#144b7d", background="#ffffff")
        style.configure("Action.TButton", font=("Avenir Next", 11, "bold"), padding=(10, 8))
        style.configure("Letter.TButton", font=("Menlo", 11, "bold"), padding=(8, 6))

    def _create_layout(self) -> None:
        container = ttk.Frame(self, padding=18)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=3)
        container.columnconfigure(1, weight=2)
        container.rowconfigure(2, weight=1)

        title_frame = ttk.Frame(container)
        title_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        ttk.Label(title_frame, text="Guess the Word", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            title_frame,
            text="Professional edition with timer, streak tracking, and adaptive difficulty",
            style="SubHeader.TLabel",
        ).pack(anchor="w")

        controls = ttk.Frame(container, style="Card.TFrame", padding=14)
        controls.grid(row=1, column=0, sticky="ew", padx=(0, 12), pady=(0, 12))

        ttk.Label(controls, text="Category", style="Body.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.category_var = tk.StringVar(value="animals")
        self.category_combo = ttk.Combobox(
            controls,
            textvariable=self.category_var,
            values=list(WORD_BANK.keys()),
            state="readonly",
            width=16,
        )
        self.category_combo.grid(row=1, column=0, sticky="w", padx=(0, 10))

        ttk.Label(controls, text="Difficulty", style="Body.TLabel").grid(row=0, column=1, sticky="w", padx=(0, 10))
        self.difficulty_var = tk.StringVar(value="Medium")
        self.difficulty_combo = ttk.Combobox(
            controls,
            textvariable=self.difficulty_var,
            values=list(DIFFICULTIES.keys()),
            state="readonly",
            width=12,
        )
        self.difficulty_combo.grid(row=1, column=1, sticky="w", padx=(0, 10))

        self.start_btn = ttk.Button(controls, text="Start New Round", style="Action.TButton", command=self.start_round)
        self.start_btn.grid(row=1, column=2, padx=(8, 8))

        self.hint_btn = ttk.Button(controls, text="Use Hint", style="Action.TButton", command=self.use_hint)
        self.hint_btn.grid(row=1, column=3, padx=(0, 8))

        self.reset_stats_btn = ttk.Button(
            controls,
            text="Reset Stats",
            style="Action.TButton",
            command=self.reset_stats,
        )
        self.reset_stats_btn.grid(row=1, column=4)

        game_card = ttk.Frame(container, style="Card.TFrame", padding=18)
        game_card.grid(row=2, column=0, sticky="nsew", padx=(0, 12))
        game_card.columnconfigure(0, weight=1)
        game_card.rowconfigure(4, weight=1)

        self.word_var = tk.StringVar(value="_ _ _ _")
        self.meta_var = tk.StringVar(value="Attempts: 0 | Time: 00s")
        self.wrong_var = tk.StringVar(value="Wrong: -")
        self.hint_var = tk.StringVar(value="Hint: Not used")
        self.status_var = tk.StringVar(value="")

        ttk.Label(game_card, textvariable=self.word_var, style="Word.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(game_card, textvariable=self.meta_var, style="Body.TLabel").grid(row=1, column=0, sticky="w", pady=(8, 2))
        ttk.Label(game_card, textvariable=self.wrong_var, style="Body.TLabel").grid(row=2, column=0, sticky="w", pady=(2, 2))
        ttk.Label(game_card, textvariable=self.hint_var, style="Body.TLabel").grid(row=3, column=0, sticky="w", pady=(2, 12))

        input_frame = ttk.Frame(game_card, style="Card.TFrame")
        input_frame.grid(row=4, column=0, sticky="new")
        input_frame.columnconfigure(0, weight=1)

        self.guess_var = tk.StringVar()
        self.guess_entry = ttk.Entry(input_frame, textvariable=self.guess_var, width=8, font=("Menlo", 13))
        self.guess_entry.grid(row=0, column=0, sticky="w")

        self.submit_guess_btn = ttk.Button(
            input_frame,
            text="Submit Guess",
            style="Action.TButton",
            command=self.submit_guess,
        )
        self.submit_guess_btn.grid(row=0, column=1, padx=(8, 0))

        self.progress_var = tk.DoubleVar(value=100)
        self.attempts_bar = ttk.Progressbar(input_frame, maximum=100, variable=self.progress_var)
        self.attempts_bar.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(12, 4))

        ttk.Label(input_frame, textvariable=self.status_var, style="Status.TLabel").grid(row=2, column=0, columnspan=2, sticky="w")

        keyboard_frame = ttk.Frame(game_card, style="Card.TFrame")
        keyboard_frame.grid(row=5, column=0, sticky="s", pady=(18, 0))
        self._create_keyboard(keyboard_frame)

        stats_card = ttk.Frame(container, style="Card.TFrame", padding=18)
        stats_card.grid(row=1, column=1, rowspan=2, sticky="nsew", pady=(0, 12))
        stats_card.columnconfigure(0, weight=1)

        ttk.Label(stats_card, text="Player Statistics", style="Body.TLabel").grid(row=0, column=0, sticky="w")

        self.stats_labels: dict[str, ttk.Label] = {}
        stats_rows = [
            ("Games", "played"),
            ("Wins", "won"),
            ("Losses", "lost"),
            ("Win Rate", "win_rate"),
            ("Total Score", "total_score"),
            ("Best Score", "best_score"),
            ("Current Streak", "current_streak"),
            ("Best Streak", "best_streak"),
        ]

        for idx, (label, key) in enumerate(stats_rows, start=1):
            ttk.Label(stats_card, text=label, style="Body.TLabel").grid(row=idx, column=0, sticky="w", pady=(12 if idx == 1 else 6, 0))
            widget = ttk.Label(stats_card, text="0", style="StatValue.TLabel")
            widget.grid(row=idx, column=0, sticky="e", pady=(12 if idx == 1 else 6, 0))
            self.stats_labels[key] = widget

    def _create_keyboard(self, parent: ttk.Frame) -> None:
        letters = list(string.ascii_uppercase)
        for idx, letter in enumerate(letters):
            row = idx // 9
            col = idx % 9
            btn = ttk.Button(
                parent,
                text=letter,
                width=3,
                style="Letter.TButton",
                command=lambda current=letter.lower(): self.guess_letter(current),
            )
            btn.grid(row=row, column=col, padx=3, pady=3)
            self.keyboard_buttons[letter.lower()] = btn

    def _bind_keys(self) -> None:
        self.bind("<Return>", lambda _event: self.submit_guess())

    def load_stats(self) -> Stats:
        if not STATS_FILE.exists():
            return Stats()

        try:
            data = json.loads(STATS_FILE.read_text(encoding="utf-8"))
            return Stats(
                played=int(data.get("played", 0)),
                won=int(data.get("won", 0)),
                total_score=int(data.get("total_score", 0)),
                best_score=int(data.get("best_score", 0)),
                current_streak=int(data.get("current_streak", 0)),
                best_streak=int(data.get("best_streak", 0)),
            )
        except (json.JSONDecodeError, OSError, ValueError):
            return Stats()

    def save_stats(self) -> None:
        payload = {
            "played": self.stats.played,
            "won": self.stats.won,
            "total_score": self.stats.total_score,
            "best_score": self.stats.best_score,
            "current_streak": self.stats.current_streak,
            "best_streak": self.stats.best_streak,
        }
        STATS_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def reset_stats(self) -> None:
        self.stats = Stats()
        self.save_stats()
        self._refresh_stats_panel()
        self._set_status("Player statistics reset.", "info")

    def start_round(self) -> None:
        category = self.category_var.get().strip().lower()
        difficulty = self.difficulty_var.get().strip()

        if category not in WORD_BANK:
            self._set_status("Invalid category selected.", "error")
            return
        if difficulty not in DIFFICULTIES:
            self._set_status("Invalid difficulty selected.", "error")
            return

        config = DIFFICULTIES[difficulty]
        entry = random.choice(WORD_BANK[category])

        self.round_state = RoundState(
            word=entry["word"].lower(),
            hint=entry["hint"],
            attempts_left=config.attempts,
            max_attempts=config.attempts,
            seconds_left=config.round_time,
            hint_used=False,
            active=True,
        )

        self._reset_keyboard()
        self._update_round_ui()
        self._set_status(f"Round started: {category.title()} | {difficulty}", "success")
        self.guess_entry.focus_set()
        self._start_timer()

    def _start_timer(self) -> None:
        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None
        self._tick_timer()

    def _tick_timer(self) -> None:
        if not self.round_state.active:
            return

        if self.round_state.seconds_left <= 0:
            self._finish_round(False, "Time is up.")
            return

        self.round_state.seconds_left -= 1
        self._update_round_ui()
        self.timer_job = self.after(1000, self._tick_timer)

    def submit_guess(self) -> None:
        raw = self.guess_var.get().strip().lower()
        self.guess_var.set("")
        self.guess_letter(raw)

    def guess_letter(self, letter: str) -> None:
        if not self.round_state.active:
            self._set_status("Start a new round to make guesses.", "info")
            return

        if len(letter) != 1 or not letter.isalpha():
            self._set_status("Enter one alphabetic character.", "error")
            return

        if letter in self.round_state.guessed_letters or letter in self.round_state.wrong_letters:
            self._set_status(f"'{letter.upper()}' was already used.", "info")
            return

        self._disable_letter(letter)

        if letter in self.round_state.word:
            self.round_state.guessed_letters.add(letter)
            self._set_status(f"Great guess: {letter.upper()} is in the word.", "success")
        else:
            self.round_state.wrong_letters.add(letter)
            self.round_state.attempts_left -= 1
            self._set_status(f"{letter.upper()} is not in the word.", "error")

        self._update_round_ui()
        self._evaluate_round_state()

    def use_hint(self) -> None:
        if not self.round_state.active:
            self._set_status("Start a new round before using a hint.", "info")
            return

        if self.round_state.hint_used:
            self._set_status("Hint already used this round.", "info")
            return

        self.round_state.hint_used = True
        self.hint_var.set(f"Hint: {self.round_state.hint}")
        self._set_status("Hint revealed. Score penalty will apply.", "info")

    def _evaluate_round_state(self) -> None:
        if all(letter in self.round_state.guessed_letters for letter in self.round_state.word):
            self._finish_round(True, "You solved the word.")
            return

        if self.round_state.attempts_left <= 0:
            self._finish_round(False, "No attempts left.")

    def _finish_round(self, won: bool, reason: str) -> None:
        self.round_state.active = False
        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None

        self.stats.played += 1

        difficulty = self.difficulty_var.get().strip()
        config = DIFFICULTIES.get(difficulty, DIFFICULTIES["Medium"])

        if won:
            base = int(self.round_state.attempts_left * 12 * config.score_multiplier)
            time_bonus = int(max(self.round_state.seconds_left, 0) * 0.5)
            hint_penalty = config.hint_penalty if self.round_state.hint_used else 0
            round_score = max(base + time_bonus - hint_penalty, 0)

            self.stats.won += 1
            self.stats.total_score += round_score
            self.stats.current_streak += 1
            self.stats.best_score = max(self.stats.best_score, round_score)
            self.stats.best_streak = max(self.stats.best_streak, self.stats.current_streak)

            self._set_status(
                f"Win! Word: {self.round_state.word.upper()} | Score: {round_score} | {reason}",
                "success",
            )
        else:
            self.stats.current_streak = 0
            self._set_status(
                f"Round lost. Word was {self.round_state.word.upper()} | {reason}",
                "error",
            )

        self.save_stats()
        self._refresh_stats_panel()
        self._update_round_ui(force_reveal=True)
        self._disable_keyboard()

    def _update_round_ui(self, force_reveal: bool = False) -> None:
        if not self.round_state.word:
            self.word_var.set("_ _ _ _")
            self.meta_var.set("Attempts: 0 | Time: 00s")
            self.wrong_var.set("Wrong: -")
            self.progress_var.set(100)
            return

        if force_reveal:
            display_word = " ".join(self.round_state.word.upper())
        else:
            display_word = " ".join(
                letter.upper() if letter in self.round_state.guessed_letters else "_"
                for letter in self.round_state.word
            )
        self.word_var.set(display_word)

        self.meta_var.set(
            f"Attempts: {self.round_state.attempts_left}/{self.round_state.max_attempts} | "
            f"Time: {self.round_state.seconds_left:02d}s"
        )

        wrong = " ".join(sorted(letter.upper() for letter in self.round_state.wrong_letters))
        self.wrong_var.set(f"Wrong: {wrong if wrong else '-'}")

        if not self.round_state.hint_used:
            self.hint_var.set("Hint: Not used")

        if self.round_state.max_attempts > 0:
            percent = (self.round_state.attempts_left / self.round_state.max_attempts) * 100
            self.progress_var.set(max(percent, 0))

    def _refresh_stats_panel(self) -> None:
        self.stats_labels["played"].configure(text=str(self.stats.played))
        self.stats_labels["won"].configure(text=str(self.stats.won))
        self.stats_labels["lost"].configure(text=str(self.stats.lost))
        self.stats_labels["win_rate"].configure(text=f"{self.stats.win_rate:.1f}%")
        self.stats_labels["total_score"].configure(text=str(self.stats.total_score))
        self.stats_labels["best_score"].configure(text=str(self.stats.best_score))
        self.stats_labels["current_streak"].configure(text=str(self.stats.current_streak))
        self.stats_labels["best_streak"].configure(text=str(self.stats.best_streak))

    def _reset_keyboard(self) -> None:
        for button in self.keyboard_buttons.values():
            button.state(["!disabled"])

    def _disable_keyboard(self) -> None:
        for button in self.keyboard_buttons.values():
            button.state(["disabled"])

    def _disable_letter(self, letter: str) -> None:
        button = self.keyboard_buttons.get(letter)
        if button is not None:
            button.state(["disabled"])

    def _set_status(self, message: str, level: str) -> None:
        color_map = {
            "success": "#126a3e",
            "error": "#9f1d35",
            "info": "#2b4f72",
        }
        self.status_var.set(message)

        style = ttk.Style(self)
        style.configure(
            "Status.TLabel",
            foreground=color_map.get(level, "#1f2b3a"),
            background="#ffffff",
            font=("Avenir Next", 12, "bold"),
        )


def main() -> None:
    app = GuessTheWordApp()
    app.mainloop()


if __name__ == "__main__":
    main()
