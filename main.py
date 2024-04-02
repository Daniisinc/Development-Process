import random
from hangman_stages import hangman_stages
from word_list import word_list

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
                user_score += 1
            elif user_pick == computer_pick:
                print("No one won! The computer also chose", computer_pick + ".")
            else:
                print("You lost! The computer chose", computer_pick + ".")
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
def dice_roll():
    global user_total_score
    global game_count
    target = random.randint(1, 6)
    tries = 0

    while True:
        guess = input("Guess the number rolled (1-6) or 'q' to exit: ")

        if guess.lower() == "q":
            break

        if guess.isdigit():
            guess = int(guess)
            if guess == target:
                print("You got it!")
                tries += 1
                break
            else:
                print("Try again!")
            tries += 1
        else:
            print("Invalid input! Please enter a number.")

    # Update total score and game count
    user_total_score += 1 / tries
    game_count += 1

    # Display scores
    print("Your score for this game:", 1 / tries)
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
        dice_roll()
    elif user_choice.lower() == "hangman":
        hangman()
    elif user_choice.lower() == "q":
        break
    else:
        print("Invalid choice! Please choose again.")

print("Thank you for playing!")
