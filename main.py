"""Word game CLI with hints, scoring, and persistent stats.

Run with: python3 main.py
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path


STATS_FILE = Path("game_stats.json")


WORD_BANK: dict[str, list[dict[str, str]]] = {
	"animals": [
		{"word": "elephant", "hint": "Largest land mammal"},
		{"word": "giraffe", "hint": "Tall animal with a long neck"},
		{"word": "dolphin", "hint": "Intelligent marine mammal"},
		{"word": "kangaroo", "hint": "Australian marsupial that jumps"},
	],
	"technology": [
		{"word": "python", "hint": "Popular programming language"},
		{"word": "algorithm", "hint": "Step-by-step problem-solving method"},
		{"word": "database", "hint": "Organized collection of data"},
		{"word": "compiler", "hint": "Converts source code to machine code"},
	],
	"geography": [
		{"word": "sahara", "hint": "World's largest hot desert"},
		{"word": "himalaya", "hint": "Mountain range with Everest"},
		{"word": "amazon", "hint": "World's largest rainforest"},
		{"word": "pacific", "hint": "Largest ocean on Earth"},
	],
}


@dataclass
class Stats:
	played: int = 0
	won: int = 0
	total_score: int = 0

	@property
	def lost(self) -> int:
		return self.played - self.won

	@property
	def win_rate(self) -> float:
		if self.played == 0:
			return 0.0
		return (self.won / self.played) * 100


def load_stats(path: Path = STATS_FILE) -> Stats:
	if not path.exists():
		return Stats()
	try:
		data = json.loads(path.read_text(encoding="utf-8"))
		return Stats(
			played=int(data.get("played", 0)),
			won=int(data.get("won", 0)),
			total_score=int(data.get("total_score", 0)),
		)
	except (json.JSONDecodeError, OSError, ValueError):
		return Stats()


def save_stats(stats: Stats, path: Path = STATS_FILE) -> None:
	payload = {
		"played": stats.played,
		"won": stats.won,
		"total_score": stats.total_score,
	}
	path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def choose_category() -> str:
	categories = list(WORD_BANK.keys())
	print("\nChoose a category:")
	for idx, category in enumerate(categories, start=1):
		print(f"  {idx}. {category.title()}")

	while True:
		choice = input("Enter category number: ").strip()
		if choice.isdigit() and 1 <= int(choice) <= len(categories):
			return categories[int(choice) - 1]
		print("Invalid choice. Please choose a valid category number.")


def reveal_progress(word: str, guessed: set[str]) -> str:
	return " ".join(letter if letter in guessed else "_" for letter in word)


def play_round(stats: Stats) -> None:
	category = choose_category()
	entry = random.choice(WORD_BANK[category])
	word = entry["word"].lower()
	hint = entry["hint"]

	attempts_left = 7
	guessed_letters: set[str] = set()
	wrong_letters: set[str] = set()
	hint_used = False

	print(f"\nCategory: {category.title()}")

	while attempts_left > 0:
		progress = reveal_progress(word, guessed_letters)
		print(f"\nWord: {progress}")
		print(f"Attempts left: {attempts_left}")
		print(f"Wrong guesses: {' '.join(sorted(wrong_letters)) or '-'}")

		if all(letter in guessed_letters for letter in word):
			base_score = attempts_left * 10
			score = base_score - 10 if hint_used else base_score
			stats.played += 1
			stats.won += 1
			stats.total_score += max(score, 0)
			print(f"\nYou won! The word was '{word}'.")
			print(f"Score this round: {max(score, 0)}")
			return

		raw = input("Guess a letter (or type 'hint'): ").strip().lower()
		if raw == "hint":
			if hint_used:
				print("Hint already used this round.")
			else:
				hint_used = True
				print(f"Hint: {hint}")
			continue

		if len(raw) != 1 or not raw.isalpha():
			print("Enter one alphabetic letter, or 'hint'.")
			continue

		if raw in guessed_letters or raw in wrong_letters:
			print("You already tried that letter.")
			continue

		if raw in word:
			guessed_letters.add(raw)
			print("Good guess!")
		else:
			wrong_letters.add(raw)
			attempts_left -= 1
			print("Nope, that letter is not in the word.")

	stats.played += 1
	print(f"\nYou lost. The word was '{word}'.")


def show_stats(stats: Stats) -> None:
	print("\n=== Player Stats ===")
	print(f"Games played: {stats.played}")
	print(f"Wins: {stats.won}")
	print(f"Losses: {stats.lost}")
	print(f"Win rate: {stats.win_rate:.1f}%")
	print(f"Total score: {stats.total_score}")


def main() -> None:
	stats = load_stats()

	print("Welcome to the Word Game!")
	print("Try to guess the word letter-by-letter before attempts run out.")

	while True:
		print("\nMenu")
		print("  1. Play")
		print("  2. View stats")
		print("  3. Quit")
		choice = input("Select an option: ").strip()

		if choice == "1":
			play_round(stats)
			save_stats(stats)
		elif choice == "2":
			show_stats(stats)
		elif choice == "3":
			save_stats(stats)
			print("Thanks for playing. Goodbye!")
			break
		else:
			print("Invalid option. Choose 1, 2, or 3.")


if __name__ == "__main__":
	main()
