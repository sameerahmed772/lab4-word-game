# Lab 4 - Guess The Word - Report

## First Impressions

At first, making a Hangman game looked easy. But the strict rules, like no `while True` loops and no string replacement functions, made it a lot harder. It was a good challenge to think differently about how the game runs. Setting up the GitHub agents took some time, but it helped organize the work.

## Key Learnings

* **Python Skills:** I learned how to separate the game logic from the user interface. To hide the word, I used list comprehensions and `.join()` instead of normal string replacement.
* **Testing:** Writing small tests for the `update_game_state` function before finishing the whole game was very helpful. It made sure the core rules worked without having to play the game manually every time.

## CoPilot Prompting Experience & Observations

Using "Ask Mode" to brainstorm the states and variables was a great way to start.

* **Good surprise:** I was surprised by how well CoPilot reviewed and explained my manual code when I asked it to check my `update_game_state` function.
* **Bad surprise:** I was surparised in a bad way when CoPilot kept suggesting `while True` loops for the main game, even though it's a bad practice for this assignment.

## Limitations and Reliability

The biggest limitation is that CoPilot doesn't always follow strict project rules. It likes to take the easy way out (like using global variables or infinite loops). You can't just copy and paste; you have to really read what it gives you and fix it to match the constraints.

## Overall Reflection

AI tools save a lot of time, especially for generating documentation or getting unstuck. However, I learned that I still need to be the one controlling the code structure. AI is a good assistant, but I have to make the final decisions.