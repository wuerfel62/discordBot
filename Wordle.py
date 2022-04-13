import random
#from termcolor.termcolor import colored
import os

class wordle:
    
    def __init__(self) -> None:
        self.is_ingame = False
            
        self.wordList = open('wordListDE.txt', 'r').read().split()

        self.errMsg = ""

        self.guessedWords = []
        self.guessCount = 0
        self.wordToGuess = ""
        self.wordToGuessList = []

    def start_game(self):
        print("new Wordle game started")

        self.is_ingame = True

        self.errMsg = ""

        self.guessedWords = []
        self.guessCount = 0
        self.wordToGuess = self.wordList[random.randint(0, len(self.wordList))]
        self.wordToGuessList = [char for char in self.wordToGuess]

        print("word to guess: " + self.wordToGuess)

    def check_word(self, word):
        if(len(word) != 5):
            return ["not 5 letters"]
        elif(word == self.wordToGuess):

            self.guessedWords.append("**" + word + "**")
            self.is_ingame = False

            print("Game finished")

            return self.guessedWords
        elif word not in self.wordList:
            return [word + " is not in the Wordlist"]
        else:
            self.guessedWords.append(self.format_word(word))
            self.guessCount += 1
            return self.guessedWords

    def has_lost(self):
        if self.guessCount == 6:
            return True
        else:
            return False

    def format_word(self, word):
        wordToGuessList = [char for char in self.wordToGuess]
        if not self.errMsg == "":
            print(self.errMsg, sep=" ")

        tempStrList = [char for char in word]
        tempStr = ""
        for i in range (0,5):
            if(tempStrList[i] == wordToGuessList[i]):
                tempStr += "**" + tempStrList[i]+ "**"
            elif(tempStrList[i] in wordToGuessList):
                tempStr += "*" + tempStrList[i]+ "*"
            else:
                tempStr += tempStrList[i]

        self.errMsg = ""

        return(tempStr)