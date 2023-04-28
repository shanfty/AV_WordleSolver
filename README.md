# AV_WordleSolver

Vanderbilt University M.S of Computer Science | Automated Verification | CS 6315 | Spring 2023

# Instructions
Run the AV_WordleSolver.py
The program will give the user a random first guess based on the words in the words.txt file.
The user will enter that word in wordle then give the program feedback based on the results
If the letter is gray or not found in the word, the correct feedback would be 'x'
If the letter is yellow or found in the word but not at the correct location. The corresponding feedback letter would be 'y'
If the letter is green or found in the correct position, the feedback letter would be 'g'
The program will then give me the next best guess using a Z3 solver for the user to input, repeating this process until the feedback is 'ggggg'

# Example
If the worlde word is 'apple' and my first guess is 'plate', I would enter feedback of 'yyyxg'
