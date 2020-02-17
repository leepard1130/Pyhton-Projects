"""
CSSE1001 Assignment 2
Semester 2, 2017
"""

# Import statements go here
import a2_support
import random
# Fill these in with your details
__author__ = "Chun Ta Lee "
__email__ = "chunta.lee@uqconnect.edu.au"
__date__ = "22/9/2017"

# Write your classes here

class Tile(object):
    """
    Represent a regular Scrabble tile


    """
    def __init__(self, letter, score):
        """ 
        Parameters:
            letter (str): the letter of the tile
            score (int): the score of the tile
            
        """
        self._letter = letter
        self._score = score

    def get_letter(self):
        """
        Returns the letter of the tile
        
        """
        return self._letter

    def get_score(self):
        """
        Returns the base score of the tile
        
        """
        return self._score

    def __str__(self):
        """
        Returns a human readable string, of the form {letter}:{score}

        """
        return "{0}:{1}".format(self._letter, self._score)

    def __repr__(self):
        """
        Returns a human readable string, of the form {letter}:{score}
        
        """
        return "{0}:{1}".format(self._letter, self._score)

    def reset(self):
        """
        Does nothing
        
        """
        return None


class Wildcard(Tile):
    """

    Represent a regular Scrabble tile

    """
    def __init__(self, score):
        """ Constructor

        Parameters:
            score (int): the score of the wildcard
        """
        super().__init__(a2_support.WILDCARD_CHAR, score)
        score = 0

    def set_letter(self, letter):
        """
        Sets the letter of the tile

        Parameters:
            letter (str): set the letter of the wildcard
        """
        return super().__init__(letter, self._score)

    def reset(self):
        """
        Resets this tile back to its wildcard state (i.e. unsets the letter)
        
        """
        return Wildcard.__init__(self, self._score)


class Bonus(object):
    """
    Simple superclass that is used to represent a generic bonus

    """
    def __init__(self,value):
        """ Constructor

        Parameters:
            value (int): the value of this bonus

        """
        self._value = value

    def get_value(self):
        """
        Returns the value of this bonus
        
        """
        return self._value


class WordBonus(Bonus):
    """
    Word bonus, subclass of Bonus

    """

    def __str__(self):
        """
        Returns a human readable string, of the form {type}{value}, where type is W for WordBonus
        
        """
        return "W{}".format(self._value)

class LetterBonus(Bonus):
    """
    Letter bonus, subclass of Bonus

    """

    def __str__(self):
        """
        Returns a human readable string, of the form {type}{value}, where type is L for LetterBonus
        
        """
        return "L{}".format(self._value)


class Player(object):
    """
    Represents a player and their rack of tiles

    """
    def __init__(self, name=''):
        """
        Constructor

        Parameters:
            name (str): the player's name
            
        """
        self._name = name
        self._score = 0
        self._rack = []

    def get_name(self):
        """Return the player's name
        """
        return self._name

    def add_tile(self, tile):
        """
        Adds a tile to the player's rack

        Parameters:
            tile (Tile): a Tile (Tile or Wildcard)
        """
        self._rack.append(tile)

    def remove_tile(self, index):
        """
        Removes and returns the tile at index from the player's rack
            Parameters:
                index (int): index from the player's rack
                
        """
        return self._rack.pop(index)

    def get_tiles(self):
        """
        Returns a list of all tiles in the player's rack (Return type: list<Tile>)
        
        """
        return self._rack

    def get_score(self):
        """
        Return's the player's score
        
        """
        return self._score

    def add_score(self, score):
        """
        Adds score to the player's total score
        
        """
        self._score += score

    def get_rack_score(self):
        """
        Returns the total score of all letters in the player's rack
        
        """
        score = 0
        for tile in self._rack:
            score += tile.get_score()
        return score

    def reset(self):
        """
        Resets the player for a new game, emptying their rack and clearing their score
        
        """
        return Player.__init__(self)

    def __contains__(self, tile):
        """
        Returns True iff the player has tile in their rack
        
        """
        if tile in self._rack:
            return True
        else:
            return False

    def __len__(self):
        """
        Returns the number of letters in the player's rack
        
        """
        return len(self._rack)

    def __str__(self):
        """
        Returns a string representation of this player and their rack, of the form {name}:{score}\n{tiles}
           where tiles is a comma (&space) separated list of all the tiles in the player's rack, in order
           
        """
        PlayerRack = self._name+":" + str(self._score) + "\n"
        tiles = []
        for tile in self._rack:
            tiles.append (str(tile))
        PlayerRack += ', '.join(tiles)
        return PlayerRack


class TileBag(object):
    """
    Used to hold Scrabble tiles

    """
    def __init__(self, data):
        """
        Constructor
            Parameters:
                data (dict): a data dictionary whose keys are letters
                (lowercase) and whose values are pairs of (count, score), 
                where count is the number of tiles to create with this letter, 
                and score is the tile's score
                
        """
        self._data = data
        self.tiles = []
        for letter in data:
            count, score = data[letter]
            for i in range(count):
                self.tiles.append(Tile(letter, score))
        self.shuffle()
        self._backup = self.tiles[:]
        
    def __len__(self):
        """
        Returns the number of tiles remaining in the bag
        
        """
        return len(self.tiles)

    def __str__(self):
        """
        Returns a human readable string, of each tile joined by a comma and a space; 
            i.e. "b:3, o:1, o:1, m:3" — the order the tiles are displayed does not matter
        """
        tiles = []
        for t in self.tiles:
            tiles.append(str(t))
        return ', '.join(tiles)

    def draw(self):
        """
        Draws and returns a random tile from the bag
        
        """
        DrawRe = random.randint (0,len(self.tiles)-1)
        return self.tiles.pop(DrawRe)

    def drop(self, tile):
        """
        Drops a tile into the bag
        
        """
        self.tiles.append(tile)

    def shuffle(self):
        """
        Shuffles the bag
        
        """
        random.shuffle(self.tiles)

    def reset(self):
        """
        Refills the bag and shuffles it, ready for a new game
        
        """
        self.tiles = self._backup[:]
        self.shuffle()

class Board(object):
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
        self._word_bonuses = word_bonuses
        self._letter_bonuses = letter_bonuses
        self._start = start
        self.setup(tiles, bonus)
        

    def get_start(self):
        """
        Returns the starting position
        
        """
        return self._start

    def get_size(self):
        """
        Returns the number of (rows, columns) on the board
        
        """
        return (self._size, self._size)


    def is_position_valid(self, position):
        """
        Returns True iff the position is valid (i.e. it is on the board)
        
        """
        row = position[0]
        column = position[1]
        return 0 <= row < self._size and 0 <=  column < self._size


    def get_bonus(self, position):
        """
        Returns the bonus for a position on the board, else None if there is no bonus
        
        """
        if self.is_position_valid(position):
            row = position[0]
            column = position[1]
            return self._bonus[row][column]
        else:
            return None

    def get_all_bonuses(self):
        """
        Returns a dictionary of all bonuses, keys being positions and values being Bonus.
        
        """
        bonuses = {}
        for row in range(self._size):
            for column in range(self._size):
                if self._bonus[row][column]:
                    bonuses[(row, column)] = self._bonus[row][column]

        return bonuses


    def get_tile(self, position):
        """
        Returns the tile at position, else None if no tile has been placed there yet
        
        """
        if self.is_position_valid(position):
            row = position[0]
            column = position[1]
            return self._tiles[row][column]
        else:
            return None


    def place_tile(self, position, tile):
        """
        Places a tile at position; raises an IndexError if position is invalid
        
        """
        if self.is_position_valid(position):
            row = position[0]
            column = position[1]
            self._tiles[row][column] = tile
        else:
            raise IndexError()

    def __str__(self):
        """
        Returns a human readable representation of the game board as shown in the examples below.
        
        """
        str_represent = '-' + '-' * 10 * self._size + "\n"
        for row in range(self._size):
            str_represent += "|"
            for column in range(self._size):
                tile = self._tiles[row][column]
                bonus = self._bonus[row][column]
                represent_bonus = ""
                if bonus:
                    represent_bonus = str(bonus)
                    
            str_represent += '\n'
            str_represent += '-' + '-' * 10 * self._size + '\n'
        return str_represent[:-1]

    def reset(self):
        """
        Resets the board for a new game
        
        """
        self.setup(tile, bonus)

    def setup(self, tiles, bonus):
        tile = self._tiles
        bonus = self._bonus
        self._bonus = []
        self._tiles = []

       

        for score in self._word_bonuses:
            for position in self._word_bonuses[score]:
                if self.is_position_valid(position):
                    row = position[0]
                    column = position[1]
                    self._bonus[row][column] = WordBonus(score)
                    

        for score in self._letter_bonuses:
            for position in self._letter_bonuses[score]:
                if self.is_position_valid(position):
                    row = position[0]
                    column = position[1]
                    self._bonus[row][column] = LetterBonus(score)

