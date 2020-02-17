def compute_score(guess, position, word):
    score = 0
    counted = []# 紀錄已經算過的位置 
    for i,char in enumerate(guess):
        if char == word[position+i]:
            score += 100
            # print(i,char,word[position+i])
        else:#如果不一樣則往後搜尋看有沒有沒算過且相同的字元
            for j in range(len(word)):
                # print(char, ": ", j, ", ", word[j + position + i + 1])
                if (j not in counted) and (word[j] == char):#如果沒有算過
                    score += 20
                    # print(j, char, word[j])
                    counted.append(j)#算過，把他記錄下來
    return score

def prompt_guess(position, length):
    x = position+1
    y =  position+length+1
    while True:
        guess = input('Now guess'+ ' '+str(length)+' ' +'letters corresonding to letters' +' '+ str(x) +' '+ 'to' +' '+ str(y)+' ' + 'of the unknown word:') 
        if len(guess) != length:
            print ('Invalid guess'+' '+guess+' .' + 'Should be' + str(length) + 'characters long')
        elif len(guess) == length:
            
            return guess

            

