import random
import time


def update_game_state(secret_word, guessed_letters, guess, lives):
    new_guessed_letters = guessed_letters + [guess]
    new_lives = lives if guess in secret_word else lives - 1
    return new_guessed_letters, new_lives


def get_masked_word(secret_word, guessed_letters):
    return " ".join([char if char in guessed_letters else "_" for char in secret_word])


def play_game(is_auto=False):
    lives = 6
    word_list = ["computer", "python", "developer", "software", "network", "algorithm"]
    secret_word = random.choice(word_list)
    guessed_letters = []

    available_actions = list("abcdefghijklmnopqrstuvwxyz")
    random.shuffle(available_actions)

    while lives > 0 and "_" in get_masked_word(secret_word, guessed_letters):
        print(f"\nWord: {get_masked_word(secret_word, guessed_letters)}")
        print(f"Lives: {lives} | Guessed: {', '.join(guessed_letters)}")

        if is_auto:
            guess = available_actions.pop()
            print(f"Auto-Player guesses: {guess}")
            time.sleep(0.5)
        else:
            guess = input("Guess a letter: ").lower()
            if len(guess) != 1 or not guess.isalpha():
                print("Invalid input.")
                continue
            if guess in guessed_letters:
                print("Already guessed!")
                continue

        guessed_letters, lives = update_game_state(
            secret_word, guessed_letters, guess, lives
        )
    result = "won" if lives > 0 else "lost"
    print(f"\nFinal Word: {secret_word}")
    print(f"{'Auto-Player' if is_auto else 'You'} {result}!")


def main():
    print("Welcome to Guess The Word!")

    while True:
        mode = input("\nChoose mode: (1) Manual Play (2) Auto Play (Q) Quit: ").lower()

        if mode == "1":
            play_game(is_auto=False)
        elif mode == "2":
            play_game(is_auto=True)
        elif mode == "q":
            print("Goodbye!")
            break
        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main()
