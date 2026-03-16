## App States

A game like Hangman usually has four main states:

nitialization: the game chooses a secret word, resets the guessed letters, and sets the number of allowed attempts.
Active Play: the player keeps entering guesses, and the game updates the displayed word and remaining attempts.
Win State: the player reveals every letter in the secret word before running out of attempts.
Loss State: the player uses all allowed incorrect guesses before finishing the word.

## App Variables

The core variables are:

secret_word: the hidden word the player is trying to guess.
guessed_letters: a collection storing all letters the player has already entered.
remaining_attempts: the number of wrong guesses the player can still make.
display_word: the current visible version of the word, with guessed letters revealed and unknown letters hidden.
max_attempts: the maximum number of incorrect guesses allowed.

## App Rules and Invariants

**Rules:**

* The player guesses one letter at a time.
* If the guessed letter is in the secret word, every occurrence of that letter is revealed.
* If the guessed letter is not in the word, remaining_attempts decreases.
* The game ends when the full word is revealed or when remaining_attempts reaches zero.

**Invariants:**

* $0 \le \text{remaining\_attempts} \le \text{max\_attempts}$
* `guessed_letters` should contain only valid alphabetic guesses.
* The length of `display_word` must always match the length of `secret_word`.
* Letters already revealed in `display_word` must always match the corresponding letters in `secret_word`.

## App Bugs and Edge Cases

Case sensitivity: uppercase and lowercase letters should be normalized so that A and a are treated the same.
Repeated guesses: guessing the same letter twice should not unfairly reduce attempts.
Non-alphabetic input: numbers, spaces, punctuation, or emoji should be rejected.
Empty or multi-character input: the game should decide whether to allow only single-letter guesses and reject anything else.
Multiple occurrences of a letter:** if the word contains the same letter more than once, all instances should be revealed together.
Winning on the last attempt: the game should correctly detect a win even if it happens when only one attempt remains.
nvalid state updates: remaining attempts should never go below zero, and `display_word` should never become inconsistent with `secret_word`.

## Auto Play Mode Requirements

Mode Selection: At startup, the user chooses between Manual Play or Auto Play.
Automated Logic: The computer acts as the player, automatically selecting letters until the game ends.
Non-Redundancy The Auto Player must track its own moves to ensure it never suggests a letter it has already tried.
Session Loop Once an Auto Play game concludes, the system must navigate back to the initial mode selection screen.

## Design Decisions (Auto Play)

Input Abstraction: Modify the main loop to accept guesses from either a `user_input` or an `auto_generator`.
Unique Guessing: Use a shuffled list of the alphabet to pop letters, ensuring $100\%$ unique guesses for the computer.
Pacing: Implement a small time delay between auto-guesses to ensure the game remains readable for the user.
