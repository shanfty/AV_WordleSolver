from z3 import *
import random

def addAlphabetToSolver(solver, letters):
    for letter in letters:
        solver.add(letter >= 0, letter <= 25)

    return solver

#Setup Maps for letters and indicies
letterMap = {
    letter: index 
    for index, letter in enumerate("abcdefghijklmnopqrstuvwxyz")
}
mapIndex = {}
for letter, index in letterMap.items():
    mapIndex[index] = letter

def addWords(solver, words, letters):
    allWords = []

    for word in words:
        word_conjuction = z3.And([letters[index] == letterMap[letter] for index, letter in enumerate(word)])
        allWords.append(word_conjuction)

    solver.add(z3.Or(allWords))

    return solver

def printSolution(model, letters):
    word = []
    for index, letter in enumerate(letters):
        word.append(mapIndex[model[letter].as_long()])

    return ''.join(word)

def addWrongLetter(solver, letters, letter):
    for char in letters:
        solver.add(char != letterMap[letter])

    return solver

def addContainsLetter(solver, letters, letter):
    solver.add(z3.Or([char == letterMap[letter] for char in letters]))

    return solver

def addWrongPosition(solver, letters, letter, position):
    solver.add(letters[position] != letterMap[letter])

    return solver

def addCorrectLetter(solver, letters, letter, position):
    solver.add(letters[position] == letterMap[letter])

    return solver

if __name__ == "__main__":
    
    print("Loading possible words, please wait...")

    with open('wordList.txt') as f:
        words = [word.strip() for word in f.readlines()]

    play = True
    while(play):
        solver = z3.Solver()
        letters = [z3.Int(f"letter_{i}") for i in range(5)]
        solver = addAlphabetToSolver(solver, letters)
        solver = addWords(solver, words, letters)

        result = solver.check()
        assert result == z3.sat
        model = solver.model()

        bestGuess = random.choice(words)
        print("Words loaded, the random starting word is: " + bestGuess)
        feedback = None

        while(feedback != "ggggg"):
            feedback = input("Enter the feedback from last guess: ")
            while(len(feedback) != 5):
                feedback = input("Error! Please enter feedback again: ")
            for i, letter in enumerate(feedback):
                if(letter == 'x'): #Letter is not in the word
                    solver = addWrongLetter(solver, letters, bestGuess[i])
                if(letter == 'y'): #letter is in the word but wrong position
                    solver = addContainsLetter(solver, letters, bestGuess[i])
                    solver = addWrongPosition(solver, letters, bestGuess[i], i)
                if(letter == 'g'): #Letter is in the correct position
                    solver = addCorrectLetter(solver, letters, bestGuess[i], i)
            print("Solving...")
            result = solver.check()
            assert result == z3.sat
            model = solver.model()
            bestGuess = printSolution(model, letters)
            print(bestGuess)

        playAgain = input("Would you like to play again? Enter 'yes' to start over: ")
        if(playAgain != 'yes'):
            play = False



