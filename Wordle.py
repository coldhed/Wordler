import random

class Wordle:
    def __init__(self, dataSet):
        self.guessList = list(line.strip().lower() for line in open("wordLists\\" + dataSet + "\\guessList.txt"))
        self.answerList = list(line.strip().lower() for line in open("wordLists\\" + dataSet + "\\answerList.txt"))
        
        # random.seed()
        random.seed()
        
        self.playing = False
        
    def initGame(self):
        self.word = random.choice(self.answerList)
        self.nGuesses = 0
        
        self.playing = True
        
    def guess(self, guess):
        if not guess.isalpha() or len(guess) != 5 or guess not in self.guessList: return -1
        
        self.nGuesses += 1
        
        result = ""
        for i, l in enumerate(guess):
            if (l == self.word[i]):
                result += 'g'
            elif (l in self.word):
                result += 'y'
            else:
                result += 'b'
        
        if result == "ggggg":
            self.playing = False
            return self.nGuesses
            
        else:
            return result