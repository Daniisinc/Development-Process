import random
import statistics
from hangman_stages import hangman_stages
from word_list import word_list
from dice import dice_art  # Assuming dice_art is imported correctly

# Global variables to keep track of scores
user_total_score = 0
game_count = 0

# First game function Rock Paper Scissors
def rock_paper_scissors():
    global user_total_score
    global game_count
    user_score = 0
    computer_score = 0

    # Users options/computers options
    options = ["rock", "paper", "scissors"]
    effects = {
        "rock": {"scissors": "Rock smashes scissors"},
        "paper": {"rock": "Paper covers rock"},
        "scissors": {"paper": "Scissors cuts paper"}
    }

    while True:
        user_pick = input("Type either rock, paper, or scissors, or 'q' to exit: ").lower()

        if user_pick == "q":
            break

        random1 = random.randint(0, 2)
        computer_pick = options[random1]

        if user_pick in options:
            if (user_pick == "rock" and computer_pick == "scissors") or \
                    (user_pick == "paper" and computer_pick == "rock") or \
                    (user_pick == "scissors" and computer_pick == "paper"):
                print("You won! The computer chose", computer_pick + ".")
                print(effects[user_pick][computer_pick])
                user_score += 1
            elif user_pick == computer_pick:
                print("No one won! The computer also chose", computer_pick + ".")
            else:
                print("You lost! The computer chose", computer_pick + ".")
                print(effects[computer_pick][user_pick])
                computer_score += 1
        else:
            print("Invalid choice! Please choose rock, paper, or scissors.")
        
    # Update total score and game count
    user_total_score += user_score
    game_count += 1

    # Display scores
    print("Your score for this game:", user_score)
    print("Your total score across all games:", user_total_score)
    print("Average score per game:", user_total_score / game_count)

# Dice Roll Game
class DiceGame:
    def __init__(self):
        self.winning_score = 30
        self.tries = 5  # Maximum rolls allowed
        self.all_time_rolls = []  # Stores rolls from all games for statistics
        self.current_rolls = []  # Tracks rolls within the current game
        self.current_score = 0  # Initializes current score to track it in real-time

    def roll_dice(self):
        """Generates a random roll, updates game history, adds to the current score, and prints the dice face."""
        roll_result = random.randint(1, 6)  # Generates a random roll between 1 and 6
        self.all_time_rolls.append(roll_result)  # Tracks roll in all-time history
        self.current_rolls.append(roll_result)  # Tracks roll in the current game
        self.current_score += roll_result  # Updates the current score directly

        # Retrieve ASCII art for the roll and print it
        dice_face = dice_art[roll_result]  # Ensure the dice value is valid
        for row in dice_face:
            print(row)  # Print each row of the dice ASCII art
        print()  # Print a separator for visual clarity between rolls

        return roll_result

    def reset_game(self):
        """Resets the current game's roll history and score for a new game session."""
        self.current_rolls = []  # Clear the list of rolls for the new game
        self.current_score = 0  # Reset the current score for the new game

    def play(self):
        """Conducts a single game session, rolling the dice up to the maximum roll limit."""
        self.reset_game()  # Prepare for a new game
        print('\nWelcome to Dice Game 🎲')
        print('-------------------------------------')
        print(f"Try to reach or exceed {self.winning_score} in {self.tries} rolls.\n")

        for current_roll in range(self.tries):
            input("Press Enter to roll the dice...")
            self.roll_dice()
            print(f"Current score: {self.current_score}")
            print(f"Tries left: {self.tries - current_roll - 1}\n")
            if self.current_score >= self.winning_score:
                print("🎉 Congrats! You've won!")
                break
        else:
            print("\nYou didn't reach the score. Try again!")
        print("******************Game Over*****************")
        self.print_statistics()  # Show statistics immediately after each game

    def print_statistics(self):
        """Prints statistics across all played games, updating after each game."""
        if self.all_time_rolls:
            try:
                print(f"Most frequent roll: {statistics.mode(self.all_time_rolls)}")
            except statistics.StatisticsError:
                print("No single most frequent roll.")  # Handles case with no clear mode
            print(f"Highest roll: {max(self.all_time_rolls)}")  # Highest roll in all games
            print(
                f"Average score per roll: {statistics.mean(self.all_time_rolls):.2f}")  # Average score per roll, updated after every game

        # Update total score and game count
        global user_total_score
        global game_count
        user_total_score += self.current_score
        game_count += 1

        # Display scores
        print("Your score for this game:", self.current_score)
        print("Your total score across all games:", user_total_score)
        print("Average score per game:", user_total_score / game_count)

# Hangman Game
class Hangman:
    """
    Hangman class represents the game logic.
    """
    def __init__(self):
        """
        Initializes the game with a random word from the word list,
        sets up game state, including guessed letters, remaining attempts,
        and hangman stages.
        """
        self.words = word_list
        self.word = random.choice(self.words).upper()
        self.guessed_letters = set()
        self.attempts_left = 6
        self.hangman_stages = hangman_stages
        self.user_score = 0

    def display_word(self):
        """
        Displays the current state of the guessed word, with letters revealed if guessed,
        and underscores for letters not guessed yet.
        """
        return ' '.join(letter if letter in self.guessed_letters else '_' for letter in self.word)

    def display_hangman(self):
        """
        Displays the hangman stage corresponding to the remaining attempts left.
        """
        return self.hangman_stages[6 - self.attempts_left]

    def guess(self, letter):
        """
        Processes a guessed letter, checks if it's correct or incorrect,
        updates game state accordingly, and returns True if the game is won or lost.
        """
        letter = letter.upper()
        if letter in self.guessed_letters:
            print("You've already guessed that letter.")
        elif letter in self.word:
            print("Correct guess!")
            self.guessed_letters.add(letter)
            if all(letter in self.guessed_letters for letter in self.word):
                print("Congratulations! You've won.")
                self.user_score = self.attempts_left + 1
                return True
        else:
            print("Incorrect guess!")
            self.attempts_left -= 1
            if self.attempts_left == 0:
                print("Game over! The word was:", self.word)
                return True
        return False

def hangman():
    """
    Main function to run the Hangman game.
    """
    global user_total_score
    global game_count
    game = Hangman()
    print("Welcome to Hangman!")

    while True:
        print("\n" + game.display_hangman())
        print(game.display_word())
        guess = input("Guess a letter: ").strip()
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter.")
            continue
        if game.guess(guess):
            break
    
    # Update total score and game count
    user_total_score += game.user_score
    game_count += 1

    # Display scores
    print("Your score for this game:", game.user_score)
    print("Your total score across all games:", user_total_score)
    print("Average score per game:", user_total_score / game_count)

# Starting message
while True:
    user_choice = input("Hey and welcome to my game inventory!! Pick a game from 3 options. Type RPS for rock paper scissors, DICE for the dice roll game, and HANGMAN for the hangman game! If you want to stop, just type q to quit. Have Fun!!: ")

    if user_choice.lower() == "rps":
        rock_paper_scissors()
    elif user_choice.lower() == "dice":
        dice_game = DiceGame()
        dice_game.play()
    elif user_choice.lower() == "hangman":
        hangman()
    elif user_choice.lower() == "q":
        break
    else:
        print("Invalid choice! Please choose again.")

print("Thank you for playing!")

