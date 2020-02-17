def compute_score(guess, position, word):
    """
    Return the score that bases on guess.

    Parameters:
        guess (character): random words from words.txt
        position (int): the position of first character
        word (character): the correct word

    Return:
        (int): current score
        
    '''
    """

   guess = input()
   score = 0
   position = [position:len(guess)]
   if guess in word:
       score = score + 20
    
