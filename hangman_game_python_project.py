# -*- coding: utf-8 -*-
"""Hangman Game Python Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZC4CzhlNI7l3W-8loKqC-zpQ0o8VgL-d
"""

import random

# Hangman ASCII Art
HANGMAN_PICS = [
    """
     +---+
         |
         |
         |
        ===""",
    """
     +---+
     O   |
         |
         |
        ===""",
    """
     +---+
     O   |
     |   |
         |
        ===""",
    """
     +---+
     O   |
    /|   |
         |
        ===""",
    """
     +---+
     O   |
    /|\\  |
         |
        ===""",
    """
     +---+
     O   |
    /|\\  |
    /    |
        ===""",
    """
     +---+
     O   |
    /|\\  |
    / \\  |
        ==="""
]

# Word Categories
word_categories = {
    "animals": ["lion", "tiger", "elephant", "zebra"],
    "fruits": ["apple", "banana", "mango", "peach"],
    "technology": ["python", "laptop", "developer", "server"]
}

# Select a word by category and difficulty
def select_word_by_category():
    print("Categories:", ", ".join(word_categories.keys()))
    category = input("Choose a category: ").lower()
    while category not in word_categories:
        category = input("Invalid category. Try again: ").lower()
    return random.choice(word_categories[category])

def select_word_by_difficulty():
    words = {
        "easy": ["cat", "dog", "book", "tree"],
        "medium": ["python", "orange", "planet"],
        "hard": ["developer", "hangman", "algorithm"]
    }

    difficulty = input("Choose difficulty (easy, medium, hard): ").lower()
    while difficulty not in words:
        difficulty = input("Invalid choice. Please choose easy, medium, or hard: ").lower()

    word = random.choice(words[difficulty])
    attempts = {"easy": 8, "medium": 6, "hard": 4}[difficulty]

    return word, attempts

# Show hangman image
def display_hangman(attempts_left):
    index = 6 - attempts_left
    print(HANGMAN_PICS[index])

# Game initialization
def initialize_game(word, attempts):
    hidden_word = ["_"] * len(word)
    return {
        "word": word,
        "hidden_word": hidden_word,
        "guessed_letters": set(),
        "attempts_left": attempts
    }

# Process guesses
def process_guess(game_state, guess):
    word = game_state["word"]
    hidden_word = game_state["hidden_word"]
    guessed_letters = game_state["guessed_letters"]

    if guess in guessed_letters:
        return game_state, "Already guessed!"

    guessed_letters.add(guess)

    if guess in word:
        for i in range(len(word)):
            if word[i] == guess:
                hidden_word[i] = guess
        return game_state, "Correct guess!"

    game_state["attempts_left"] -= 1
    return game_state, "Wrong guess!"

# Load and save high score
def load_high_score():
    try:
        with open("score.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open("score.txt", "w") as f:
        f.write(str(score))

# Main game loop
def play_hangman():
    high_score = load_high_score()
    score = {"wins": 0, "losses": 0}

    while True:
        word, attempts = select_word_by_difficulty()
        game_state = initialize_game(word, attempts)

        while game_state["attempts_left"] > 0:
            print(" ".join(game_state["hidden_word"]))
            print(f"Attempts left: {game_state['attempts_left']}")
            display_hangman(game_state["attempts_left"])
            guess = input("Guess a letter: ").lower()

            game_state, message = process_guess(game_state, guess)
            print(message)

            if "_" not in game_state["hidden_word"]:
                print(f"Congratulations! You guessed the word: {game_state['word']}")
                score["wins"] += 1
                break
        else:
            print(f"Game over! The word was: {game_state['word']}")
            score["losses"] += 1

        print(f"Wins: {score['wins']} | Losses: {score['losses']}")

        # Check if there's a new high score
        if score["wins"] > high_score:
            print("New high score!")
            save_high_score(score["wins"])
        else:
            print(f"High score: {high_score}")

        if input("Play again? (y/n): ").lower() != 'y':
            break

# Start the game
play_hangman()