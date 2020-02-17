def score(filename):
    lines = {}
    f = open (filename, 'r')
    for i, line in enumerate(f) :
        lines[i] = line.strip()
    f.close()
    return lines
   

class Tile(object):
    
    def __init__(self, letter, score):
        self.letter = letter.upper()
        if self.letter in score:
            self.score = score[self.letter]

        else:
            self.score = 0
        
         
    def get_letter(self):
        return self.letter

    def get_score(self):
        return self.score

    def __str__(self):
        return '({0}:{1})'.format(self.letter, self.score)

    def __repr__(self):
        return '({0}, {1})'.format(self.letter, self.score)

    def reset(self):
        self.__init__(self.letter, self.score)
        
