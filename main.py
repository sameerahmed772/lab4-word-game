"""Core state transition helpers and main game loop for the Hangman game."""

import random


def update_game_state(
    secret_word: str, guessed_letters: list[str], guess: str, lives: int
) -> tuple[list[str], int]:
    """Return updated guessed letters and remaining lives after one guess.

    Behavior:
    - Always returns a new guessed-letters list that includes ``guess``.
    - Decrements ``lives`` by 1 only when ``guess`` is not in ``secret_word``.

    Assumptions:
    - Input validation (single-character guess, case normalization, duplicate checks)
      is handled by the caller.
    """
    new_guessed_letters = guessed_letters + [guess]

    if guess not in secret_word:
        new_lives = lives - 1
    else:
        new_lives = lives

    return new_guessed_letters, new_lives


def get_masked_word(secret_word: str, guessed_letters: list[str]) -> str:
    """Returns the word with un-guessed letters replaced by underscores."""
    return " ".join([char if char in guessed_letters else "_" for char in secret_word])


def play_game():
    """Handles a single session of the game."""
    lives = 6
    word_list = [
        "computer",
        "python",
        "developer",
        "software",
        "network",
        "algorithm",
        "variable",
    ]
    secret_word = random.choice(word_list)
    guessed_letters = []

    while lives > 0 and "_" in get_masked_word(secret_word, guessed_letters):
        print(f"\nWord: {get_masked_word(secret_word, guessed_letters)}")
        print(f"Lives remaining: {lives}")
        print(f"Guessed so far: {guessed_letters}")

        guess = input("Guess a letter: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single valid letter.")
            continue
        if guess in guessed_letters:
            print("You already guessed that letter!")
            continue

        guessed_letters, lives = update_game_state(
            secret_word, guessed_letters, guess, lives
        )

    if lives > 0:
        print(f"\nWord: {get_masked_word(secret_word, guessed_letters)}")
        print(f"You won! The word was '{secret_word}'")
    else:
        print(f"\nGame over! The word was '{secret_word}'")


def main():
    """Main UI loop to handle playing and replaying the game."""
    print("Welcome to Guess The Word!")
    play_again = "y"

    while play_again == "y":
        play_game()
        play_again = input("\nDo you want to play again? (y/n): ").lower()

        while play_again not in ["y", "n"]:
            play_again = input("Please enter 'y' or 'n': ").lower()


if __name__ == "__main__":
    # 1. Run Tests First
    print("Running core logic tests...")

    letters, lives = update_game_state("epita", ["e"], "p", 6)
    assert letters == ["e", "p"], f"Expected ['e', 'p'], got {letters}"
    assert lives == 6, f"Expected 6 lives, got {lives}"

    letters, lives = update_game_state("epita", ["e", "p"], "z", 6)
    assert letters == ["e", "p", "z"], f"Expected ['e', 'p', 'z'], got {letters}"
    assert lives == 5, f"Expected 5 lives, got {lives}"

    print("All core logic tests passed!\n")
    print("-" * 30)

    main()
