class Board(object):#需要修改
    """
    Somewhere to arrange tiles and keeps track of which cells have bonuses

    """
    def __init__(self, size, word_bonuses, letter_bonuses, start):
        """
        Constructor
        Parameters:
            size (int): the number of rows/columns on the board (i.e. 15)
            word_bonuses (dict): a dictionary with scale of word bonuses as the key, and a list of positions where this scale occurs
            letter_bonuses (dict): a dictionary with scale of letter bonuses as the key, and a list of positions where this scale occurs
            start (tuple): (row, column) position of the starting cell
                
        """

        self._size = size
        self._grid = [[[None,None] for i in range(self._size)] for j in range(self._size)]

        self._word_bonuses = []
        for key in word_bonuses:
            value = word_bonuses[key]
            for x,y in value:
                self._grid[x][y][1] = WordBonus(key)

        self._letter_bonuses = []
        for key in letter_bonuses:
            value = letter_bonuses[key]
            for x,y in value:
                self._grid[x][y][1] = LetterBonus(key)
        self._start = start


    def get_start(self):
        """
        Returns the starting position
        
        """
        return self._start

    def get_size(self):
        """
        Returns the number of (rows, columns) on the board
        
        """
        return (self._size,self._size)

    def is_position_valid(self, position):
        """
        Returns True iff the position is valid (i.e. it is on the board)
        
        """
        x,y = position
        return x >= 0 and x < self._size and y >= 0 and y < self._size

    def get_bonus(self, position):
        """
        Returns the bonus for a position on the board, else None if there is no bonus
        
        """
        x,y = position
        return self._grid[x][y][1]

    def get_all_bonuses(self):
        """
        Returns a dictionary of all bonuses, keys being positions and values being Bonus.
        
        """
        bonuses = {}
        for i in range(self._size):
            for j in range(self._size):
                if self._grid[i][j][1]!=None:
                    bonuses[(i,j)]=self._grid[i][j][1]
        return bonuses

    def get_tile(self, position):
        """
        Returns the tile at position, else None if no tile has been placed there yet
        
        """
        x,y = position
        return self._grid[x][y][0]

    def place_tile(self, position, tile):
        """
        Places a tile at position; raises an IndexError if position is invalid
        
        """
        if not self.is_position_valid(position):
            raise IndexError
        x,y = position
        self._grid[x][y][0] = tile

    def __str__(self):
        """
        Returns a human readable representation of the game board as shown in the examples below.
        
        """
        grid = ''
        dash = '-'*10*self._size+'-\n'

        for i in range(self._size):
            line = dash
            for j in range(self._size):
                line += Box(self._grid[i][j][0],self._grid[i][j][1])
            line += '|\n'
            grid += line
        grid += '-'*10*self._size+'-'
        return grid


    def reset(self):
        """
        Resets the board for a new game
        
        """
        [[[None,None] for i in range(self._size)] for j in range(self._size)]

def Box(tile,bonus):
    box = [' ']*10
    box[0] ='|'
    tile_str = str(tile)
    bonus_str = str(bonus)
    len_tile =len(tile_str)
    len_bonus = len(bonus_str)
    box[2:len_tile+2] = tile_str
    if bonus!= None:
        box[7:len_bonus+7] = bonus_str
    return ''.join(box)
