"""
CSSE1001 Assignment 1
Semester 2, 2017
Sample Solution
"""

# Import statements go here
def load_words(filename, length):
    """ Returns a list of all words contained in filename that have the given length.'

        Parameters:
            filename: words.txt
            length(int): the number of character in the file 'word'

        Return:
            random choice(wordlist): 'choose any word.'
    """
    
    text = open(filename, "r")
    wordlist = []
    for line in text:
        for word in line.split():
            if len(word) == length:
                wordlist.append(word)
    text.close()
    return wordlist
# Fill these in with your details
__author__ = "Chun-Ta Lee (s4470024)"
__email__ = "chunta.lee@uqconnect.edu.au"
__date__ = "24/8/2017"


# Some useful constants
def prompt_guess(position, length):
    """ Repeatedly prompts the user to make a guess at a given position. Returns the first guess with the correct length.'

        Parameters:
            position(int): the beginning location when we input characters
            length(int): the number of characters in guess.'

        Return:
            guess(str): the guessing characters.

    """
        
    x = position+1
    y =  position+length
    while True:
        guess = input('Now guess'+ ' '+str(length)+' ' +'letters corresponding to letters' +' '+ str(x) +' '+ 'to' +' '+ str(y)+' ' + 'of the unknown word:'+' ') 
        if len(guess) != length:
            print ('Invalid guess'+' '+"'"+guess+"'"+'.'+' '+ 'Should be' + ' '+str(length) + ' '+'characters long.\n')
        elif len(guess) == length:
            
            return guess
# Each step of the game
STEPS = (
    # position, length
    (0, 2),
    (0, 3),
    (1, 3),
    (2, 3),
    (3, 3),
    (2, 4),
    (1, 4),
    (0, 4),
    (0, 5),
    (1, 5),
    (0, 6),
)

# Score values for correctly guessing a letter
RIGHT_POSITION_VALUE = 100
WRONG_POSITION_VALUE = 20
def compute_score(guess, position, word):
    """ Computes the score for a given guess'

        Parameters:
            guess(str): input guessing characters
            position(int): the beginning location when we input characters
            word(str): to load a word from the file 'words.txt'

        Return:
            score(int): marks which gets from guess
    """
                
    score = 0
    counted = []# To record the location which was counted. 
    for i,char in enumerate(guess):
        if char == word[position+i]:
            score += 100
            # print(i,char,word[position+i])
        else:#if the characters of guess doen't match the characters of word, then keep moving backward to find the correct one.
            for j in range(len(word)):
                # print(char, ": ", j, ", ", word[j + position + i + 1])
                if (j not in counted) and (word[j] == char):#if it doesn't count
                    score += 20
                    # print(j, char, word[j])
                    counted.append(j)#count it and record it
    return score

# Write your code here (i.e. functions)


def main():
    """
    Handles top-level interaction with user.
    
    """
    # Write the code for your main function here
    import random
    word= random.choice(load_words('words.txt', 6))
    
    print('Welcome to the brain teasing zig-zag word game.\n')
    response=input('What is your name?'+' ')
    name = response.split(' ')
    first_name = name[0]
    print('\nHi' + ' ' + first_name +'!'+' '+'We have selected a 6 letter word for you to guess.\n')
    print('Let the game begin!\n')
    wordguess= prompt_guess(0, 2)
    print('Your guess and score were:'+' '+wordguess+'____'+' :'+' '+str(compute_score(wordguess,0,word))+'\n')
    wordguess1= prompt_guess(0, 3)
    print('Your guess and score were:'+' '+wordguess1+'___'+' :'+' '+str(compute_score(wordguess1,0,word))+'\n')
    wordguess2= prompt_guess(1,3)
    print('Your guess and score were:'+' '+'_'+wordguess2+'__'+' :'+' '+str(compute_score(wordguess2,1,word))+'\n')
    wordguess3= prompt_guess(2,3)
    print('Your guess and score were:'+' '+'__'+wordguess3+'_'+' :'+' '+str(compute_score(wordguess3,2,word))+'\n')
    wordguess4= prompt_guess(3,3)
    print('Your guess and score were:'+' '+'___'+wordguess4+' :'+' '+str(compute_score(wordguess4,3,word))+'\n')
    wordguess5= prompt_guess(2, 4)
    print('Your guess and score were:'+' '+'__'+wordguess5+' :'+' '+str(compute_score(wordguess5,2,word))+'\n')
    wordguess6= prompt_guess(1, 4)
    print('Your guess and score were:'+' '+'_'+wordguess6+'_'+' :'+' '+str(compute_score(wordguess6,1,word))+'\n')
    wordguess7= prompt_guess(0, 4)
    print('Your guess and score were:'+' '+wordguess7+'__'+' :'+' '+str(compute_score(wordguess7,0,word))+'\n')
    wordguess8 = prompt_guess(0,5)
    print('Your guess and score were:'+' '+wordguess8+'_'+' :'+' '+str(compute_score(wordguess8,0,word))+'\n')
    wordguess9 = prompt_guess(1, 5)
    print('Your guess and score were:'+' '+'_'+wordguess9+' :'+' '+str(compute_score(wordguess9,1,word))+'\n')
    wordguess10 = prompt_guess(0, 6)
    print('Your guess and score were:'+' '+wordguess10+' :'+' '+str(compute_score(wordguess10,0,word))+'\n')

    score = compute_score(wordguess,0,word)+compute_score(wordguess1,0,word)+compute_score(wordguess2,1,word)+compute_score(wordguess3,2,word)+compute_score(wordguess4,3,word)+compute_score(wordguess5,2,word)+compute_score(wordguess6,1,word)+compute_score(wordguess7,0,word)+compute_score(wordguess8,0,word)+compute_score(wordguess9,1,word)+compute_score(wordguess10,0,word)
    if wordguess10 == word:
        print('Congratulations! You correctly guessed the word'+' '+"'"+word+"'."+'\nYour total score was'+' '+str(score)+'.')
    else:
        print('You did not manage to guess the correct word. It was'+' '"'"+ word+"'."+' '+'Better luck next time.'+'\nYour total score was'+' '+str(score)+'.')
              
if __name__ == "__main__":
    main()
