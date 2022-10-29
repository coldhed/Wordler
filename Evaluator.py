from Wordler import Wordler
from Wordle import Wordle

class Evaluator():
    def __init__(self, dataSet_):
        self.dataSet = dataSet_
        self.answerList = list(line.strip().lower() for line in open("wordLists/"+ self.dataSet +"/answerList.txt"))
    
    def evaluate(self):
        with open("wordLists/" + self.dataSet + "/evaluation.csv", 'w') as f:
            totalGuesses = 0
            
            for word in self.answerList:
                wordler = Wordler(self.dataSet)
                wordler.initSolving()
                
                wordle = Wordle(self.dataSet)
                wordle.initSetWord(word)
                
                while True:
                    totalGuesses += 1
                    guess = wordler.bestGuess()[0][0] # get only the best guess
                    
                    answer = wordle.guess(guess)
                    
                    if type(answer) == int:
                        print(guess)
                        f.write(guess + "\n")
                        break
                    
                    wordler.solvingGuess(guess, answer)
                    
                    print(guess, end=', ')
                    f.write(guess + ', ')
                
                del wordler
                del wordle
        
        print("Expected guesses: " + str(totalGuesses / len(self.answerList)))
        f.write("Expected guesses: " + str(totalGuesses / len(self.answerList)))