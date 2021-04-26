# CS2800Final
SMT Constraint Generator for Jotto

We have written a Python program to convert a game state of Jotto into a satisfiability modulo theory (SMT) problem, the solution of which will tell us which words fit the 
restrictions imposed by previous guesses. This implementation generates constraints for a Jotto game with no duplicates, meaning that neither the guesses nor the secret word can have any duplicate letters (like "foo").

First, it's important to understand the game of Jotto. As a reference, it's fairly similar to
mastermind, but with words. When played with humans, there is a guesser and a word-holder. The
word-holder discloses the length of their word to the guesser. The guesser then guesses a series
of English words of the given length. The word-holder responds to each guess with a number corresponding
to how many letters the guessed word has in common with their word. For example:

Word-holder: 4 (thinking of "dogs")  
Guesser: have  
Word-holder: 0  
Guesser: slip  
Word-holder: 1  
Guesser: coup  
Word-holder: 1  
Guesser: dost  
Word-holder: 3  
Guesser: rods  
Word-holder: 3  
Guesser: dons  
Word-holder: 3  
Guesser: dogs  
Word-holder: You got it. Good job, friend!  

Given a guess history like a subset of the example above, the end result of our program will be a list of words that "passes" all of the parts of the history. For
example, given the history above, the program would return "dogs" 
(or "pwnk" if it's in the dictionary - because that would give all of the same results). The core of our project is converting the guess history (and our word list) into an SMT problem.

Our initial searches revealed no prior SMT solving of this game. Algorithms have been developed to make
guesses, but as far as we can tell, no one has done what we have.

# Use Instructions
To use this project, you will need Z3Py, an SMT solver library for Python.You can install it using pip. More detailed instructions can be found here: https://github.com/Z3Prover/z3#python

Once Z3Py is installed, you should be able to run main.py. Before you do that, though, you may want to generate some guesses with guess_generator.py. When you run it, it will ask you to enter the words as guesses, then the corresponding number indicating how many letters match with the secret word. When you are done, use "s" to save the information you entered to a text file that is readable by main.py.  

When you have a guess history, you can run main.py. It will prompt you to enter a location to find your guesses. Enter the location you saved the guesses to when using the guess_generator.

After you've entered this, the program should give you a word that satisfies the guesses you've provided according to the rules of the game. If it does not, there are no solutions. This means that the word-holder picked a word that is not in the dictionary or they made a mistake in assigning numbers to guesses. If you do get a word, press enter to get another word that satisfies the constraints. You can do this until there are no more solutions left, or you can type anything and press enter to exit.

