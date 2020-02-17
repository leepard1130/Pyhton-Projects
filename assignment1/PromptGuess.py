def prompt_guess(position, length):
    x = position+1
    y =  position+length+1
    while True:
        guess = input('Now guess'+ ' '+str(length)+' ' +'letters corresonding to letters' +' '+ str(x) +' '+ 'to' +' '+ str(y)+' ' + 'of the unknown word:') 
        if len(guess) != length:
            print ('Invalid')
        elif len(guess) == length:
            
       
            return guess
        
