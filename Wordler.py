from Wordle import Wordle
import itertools
import math
import os
import csv

class Wordler(Wordle):
    def __init__(self, dataSet):
        Wordle.__init__(self, dataSet)
        
        self.ds = dataSet
        
        # yields all the possible results for a guess -> done in initiator function to avoid unnecesary compution
        self.guessResults = list(itertools.product('gyb', repeat=5))        

    
    # functions to limit the possible answers (answerList)
    # in the Wordle game:
    #   - black tiles -> letter not in word
    #   - yellow tile -> letter in word, but not that position
    #   - green tile -> letter in word and in position
    
    def setBlack(self, letter, list):
        if letter not in self.greenLetters:
            letter = letter.lower()
            
            return [word for word in list if letter not in word]
        else:
            return list
                
    def setYellow(self, letter, pos, list):
        letter = letter.lower()
        
        return [word for word in list if letter in word and word[pos] != letter]
    
    def setGreen(self, letter, pos, list):
        letter = letter.lower()
        
        return [word for word in list if word[pos] == letter]
    
    # best guess is calculated by maximizing entropy:
    # entropy is a measure of expected information
    # this info is based on bits
    # one bit represent cutting possibilites by half
    
    def bestGuess(self):
        # if there is only one solution in answerlistcopy we found the only option!
        # we cant do the same process due to information theory's definition of information
        # if we have only one option there is no information to be gained -> we know all
        if len(self.answerListCopy) == 1:
            return (self.answerListCopy[0], 'Answer Found')
        
        if self.playing:
            al = self.answerListCopy[:]
        else:
            al = self.answerList[:]
        
        # store the index and expected value (Entropy in bits) for each word in a tuple
        guessValue = list()
        
        # if the initial list already exist we avoid costly computation
        if len(self.answerList) == len(al) and os.path.exists("wordLists\\" + self.ds + "\\initialEntropy.csv"):
            with open("wordLists\\" + self.ds + "\\initialEntropy.csv") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    guessValue.append((row['word'], row['entropy']))
                    if len(guessValue) == 3:
                        return guessValue
                    
        
        for i in range(len(self.guessList)):
            guessValue.append((i, self.entropy(i, al)))
        
        guessValue.sort(key=lambda tup: tup[1], reverse=True)
        
        return [(self.guessList[ind], entropy) for (ind, entropy) in guessValue[:3]]


    
    # used to record the output in a file for future use
    def bestGuessFileOutput(self):
        # store the index and expected value (Entropy in bits) for each word in a tuple
        guessValue = list()
        
        for i in range(len(self.guessList)):
            guessValue.append((i, self.entropy(i)))
            
        guessValue.sort(key=lambda tup: tup[1], reverse=True)
        guessValue = [str(self.guessList[ind]) + "," + str(entropy) for (ind, entropy) in guessValue]
        
        with open("wordLists\\" + self.ds + "\\initialEntropy.csv", 'w') as f:
            f.write("word,entropy\n")
            for word in guessValue:
                f.write("%s\n" % word)
            
    def entropy(self, ind, al):
        # entropy is calculated as the summation of bits(x) * p(x) 
        # where x is an event and p(x) is the probability of that event
        # bits(x) is calculated as the base 2 logarithm of 1 / p(x)
        
        wordGuessed = self.guessList[ind]
        entropy = 0
        if wordGuessed in self.answerListCopy: # we marginally prefer guessing a word thats in the answerlist
            entropy += 0.000000000000001
        numAnswers = len(al)
        
        for result in self.guessResults: 
            # for every possible wordle result after inputing a word, we calculate how many answers are remaining
            possibleAnswers = al[:]
            
            for i, res in enumerate(result):
                letter = wordGuessed[i]
                if (res == 'g'): # cut all words that dont have wordGuessed[i] in their ith position
                    possibleAnswers = [word for word in possibleAnswers if word[i] == letter]
                elif (res == 'y'): # cut all words that dont have wordGuessed[i] in any position, or that have it in the ith pos
                    possibleAnswers = [word for word in possibleAnswers if letter in word and word[i] != letter]
                else: # (res == 'b') cut all words that have the wordGuessed[i] in any position
                    possibleAnswers = [word for word in possibleAnswers if letter not in word]
            
            probability = len(possibleAnswers) / numAnswers
            
            if probability != 0:
                entropy += math.log((1/probability), 2) * probability
        
        return entropy
    
    def initGameWHelp(self):
        self.initGame()
        
        self.answerListCopy = self.answerList[:]
    
        self.greenLetters = set()

    
    def limitAnswerList(self, guess, answer, al):
        for i, l in enumerate(answer):
            if l == 'g' or l == 'y':
                self.greenLetters.add(guess[i])
                
        
        for i, l in enumerate(answer):
                if l == 'g':
                    al = self.setGreen(guess[i], i, al)
                elif l == 'y':
                    al = self.setYellow(guess[i], i, al)
                else:
                    al = self.setBlack(guess[i], al)
    
        return al
    
    def guessWHelp(self, word):
        answer = self.guess(word)
        
        if isinstance(answer, int):
            return answer
        else:
            self.answerListCopy = self.limitAnswerList(word, answer, self.answerListCopy)
                    
            return answer
        
    def initSolving(self):
        self.answerListCopy = self.answerList[:]
        self.playing = True
        
        self.greenLetters = set()

    def solvingGuess(self, guess, answer):
        self.answerListCopy = self.limitAnswerList(guess, answer, self.answerListCopy)