from random_words import RandomWords
import time
from tkinter import *


# from tkPDFViewer import tkPDFViewer as pdf


# I Made this a class so that I could easily and clearly access data such as the
# word's letters as well as their length
class Word:
    def __init__(self, word):
        self.word = word
        self.letters = list(word)
        self.length = len(self.letters)

    def verify(self, letter):
        return letter in self.letters


# Player is mainly so that individual players can guess their letters/words
class Player:
    def __init__(self, name):
        self.name = name
        self.currentWord = None

    def guess(self, playerGuess):
        if len(list(playerGuess)) > 1:
            if playerGuess == self.currentWord.word:
                return 142
            else:
                return 893
        else:
            guessResult = self.currentWord.verify(playerGuess)
            return guessResult


# ScoreBoard is the controller for the system. It handles getting new words as well
# as managing player's turns and displaying winners.
class ScoreBoard:
    def __init__(self):
        self.currentWord = None
        self.players = []
        self.wrongGuesses = []
        self.wordDisplay = ""   # wordDisplay handles displaying the mix of letters
        # and underscores that appear to the players.
        self.onGoing = True   # When someone wins, onGoing is set to False and the game
        # ends.
        self.correctGuessCount = 0
        self.winner = ""
        self.currentStickManStage = 1   # I'll maybe use this to incorporate
        # an actual stick figure who can be 'hung' throughout the game.

    def getNewWord(self):
        rw = RandomWords()   # This part gets the random English word
        potentialWord = rw.random_word(min_letter_count=3)
        while len(list(potentialWord)) > 8:
            potentialWord = rw.random_word(min_letter_count=3)
        newWord = Word(potentialWord)
        # The word display needs to be cleared before a new word can be loaded
        self.wordDisplay = ""
        for _ in range(newWord.length):
            self.wordDisplay += "_ "
        # This initializes the word display to have the same number of underscores
        # as the current word has letters.
        self.currentWord = newWord
        self.wrongGuesses.clear()
        # This resets the list of incorrect guesses.
        for player in self.players:
            player.currentWord = newWord
        # This sets each player's current word to the new word.

    def takeTurn(self, player):
        print("//////////////////////////////////////////////////////////////")
        print("Current Players:")
        # This string will be populated with the names of the current players.
        playerString = ""
        for playerFromList in self.players:
            playerString += "   " + playerFromList.name
        print(playerString)
        print("Wrong Guesses:")
        print(self.wrongGuesses)
        # This is the mix of correct letters and underscores
        # i.e. "_ a _ _ b _ "
        print(self.wordDisplay)
        print(player.name + ", What's your guess?")
        playerGuess = input(">>> ")
        # 893 is the result code for an incorrect word guess
        # i.e. a player guessed at the whole word and was wrong.
        result = 893
        # When a player guesses a letter or word that has already been guessed,
        # it is not counted as another an incorrect guess, but their turn is skipped.
        skipTurn = False
        # This checks that the current player's guess has not already been guessed.
        if playerGuess not in list(self.wrongGuesses):
            result = player.guess(playerGuess)
        else:
            skipTurn = True
            print(" ")
            print(" ")
            print("You already guessed that letter!")
            print(" ")
            print(" ")
        # 142 is the result code for a correct word guess
        # i.e. the current player has guessed the entire word correctly.
        if result == 142:
            currentPlayerIndex = self.players.index(player)
            self.winner = self.players[currentPlayerIndex]
            self.onGoing = False
            result = False
        elif result == 893:
            result = False
        # result = True when a player guessed a correct letter
        if result:
            if self.onGoing:
                # counts how many times the current letter occurs in the current word
                instancesOfLetters = 0
                for letter in self.currentWord.letters:
                    if letter == playerGuess:
                        instancesOfLetters += 1
                # this will be set to True when all instances of the current letter have been found.
                foundAllLetters = False
                # this keeps track of all the index positions at which the current letter
                # occurs in the current word.
                indexesOfLetters = []
                # This is a list of all the letters that make up the current word.
                # This list will be edited as all instances of the current letter
                # are found within the current word.
                lettersOfWord = self.currentWord.letters.copy()
                instancesFound = 0
                # This while loop gets the next index position of the current letter
                # within the current word.
                while not foundAllLetters:
                    index = 0
                    currentLetter = lettersOfWord[index]
                    while playerGuess != currentLetter:
                        index += 1
                        currentLetter = lettersOfWord[index]
                    instancesFound += 1
                    indexesOfLetters.append(index)
                    lettersOfWord.pop(index)
                    if instancesFound == instancesOfLetters:
                        foundAllLetters = True
                # This temporary list will be used to break down, edit and then rebuild
                # The word display.
                tempList = self.wordDisplay.split()
                indexCompensation = 0
                self.correctGuessCount += len(indexesOfLetters)
                for index in indexesOfLetters:
                    tempList[index + indexCompensation] = playerGuess
                    indexCompensation += 1
                self.wordDisplay = ""
                for char in tempList:
                    self.wordDisplay += char + " "
                # This checks to see if the final letter has been guessed.
                if self.correctGuessCount >= self.currentWord.length:
                    currentPlayerIndex = self.players.index(player)
                    self.winner = self.players[currentPlayerIndex]
                    self.onGoing = False

        elif not skipTurn:
            # This checks to see if the maximum number of incorrect guessed has been reached.
            if len(self.wrongGuesses) >= 6:
                for _ in range(5):
                    print("********************************************")
                print("You lose! Getting a new word...")
                print("By the way, the word was " + self.currentWord.word)
                # The sleeping increments makes it seem like the program is loading.
                time.sleep(0.5)
                print(".")
                time.sleep(0.7)
                print("..")
                time.sleep(0.4)
                print("...")
                time.sleep(0.8)
                for _ in range(5):
                    print("********************************************")
                # This resets the current word to a new word.
                self.getNewWord()
                self.wrongGuesses = []
                self.correctGuessCount = 0
            else:
                # I'll get this part working eventually
                """
                root = Tk()
                root.geometry("550x750")
                v1 = pdf.ShowPdf()
                v2 = v1.pdf_view(root,
                                 pdf_location=r"images/" + str(self.currentStickManStage) + ".pdf",
                                 width=50, height=100)
                v2.pack()
                root.mainloop()
                self.currentStickManStage += 1
                """
                self.wrongGuesses.append(playerGuess)

    def addPlayer(self, player):
        newPlayer = Player(player)
        self.players.append(newPlayer)

    def removePlayer(self, player):
        for playerName in self.players:
            if playerName.name == player:
                self.players.remove(playerName)

    # This function the driver function which only runs once per session.
    # The Tk parts are for the stick man visual which I will add later.
    def runGame(self):
        root = Tk()
        root.geometry('750x700')
        addingPlayers = True
        # This while loop allows you to add as many players as you want.
        while addingPlayers:
            print("Enter player name below")
            playerName = input(">>> ")
            self.addPlayer(playerName)
            print("Would you like to add another player (Yes or No)")
            answer = input(">>> ")
            if answer.lower() == "no":
                addingPlayers = False
        self.getNewWord()
        playerIndex = 0
        while self.onGoing:
            self.takeTurn(self.players[playerIndex])
            playerIndex += 1
            if playerIndex >= len(self.players):
                playerIndex = 0
        print(self.winner.name + " Wins!!!!")
        print("The word was " + self.currentWord.word + "!")


scoreBoard = ScoreBoard()
scoreBoard.runGame()
