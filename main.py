from Wordler import Wordler
from Evaluator import Evaluator

wordler = Wordler("wordle")

# wordler.initGameWHelp()
# while True:
#     print(wordler.bestGuess())
    
    
#     guess = input("Enter a guess: ")

#     answer = wordler.guessWHelp(guess)
    
#     if isinstance(answer, int):
#         if answer == -1:
#             print("Invalid guess. Please try again")
#         else:
#             print("You won! You guessed the word in " + str(answer) + " guesses!")
#             break
#     else:
#         print("Try again! The guess result was: " + answer)

# wordler.initSolving()
# answer = ""

# while answer != "ggggg":
#     print(wordler.bestGuess(3))
    
#     guess = input("What word did you guess? ")
#     answer = input("What was your answer? ")
    
#     wordler.solvingGuess(guess, answer)

evaluator = Evaluator("wordle")
evaluator.evaluate()
