"""
CSSE1001 Assignment 3
Semester 2, 2017
"""

# There are a number of jesting comments in the support code
# They should not be taken seriously. Keep it fun folks :D
# Students are welcome to add their own source code humour, provided it remains civil


import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import os
import random

try:
    from PIL import ImageTk, Image

    HAS_PIL = True
except ImportError:
    HAS_PIL = False

from view import GridView
from game import DotGame, ObjectiveManager, CompanionGame
from dot import BasicDot,WildcardDot
from util import create_animation, ImageManager
from companion import UselessCompanion
from companion import AbstractCompanion
from cell import VoidCell
import winsound
winsound.PlaySound('music.wav',winsound.SND_ALIAS | winsound.SND_ASYNC)

# Fill these in with your details
__author__ = "Chun Ta Lee(s4470024)"
__email__ = "chunta.lee@uqconnect.edu.au"
__date__ = "28/10/2017"

__version__ = "1.1.1"


def load_image_pil(image_id, size, prefix, suffix='.png'):
    """Returns a tkinter photo image

    Parameters:
        image_id (str): The filename identifier of the image
        size (tuple<int, int>): The size of the image to load
        prefix (str): The prefix to prepend to the filepath (i.e. root directory
        suffix (str): The suffix to append to the filepath (i.e. file extension)
    """
    width, height = size
    file_path = os.path.join(prefix, "%sx%s"%(width,height), image_id + suffix)
    return ImageTk.PhotoImage(Image.open(file_path))


def load_image_tk(image_id, size, prefix, suffix='.gif'):
    """Returns a tkinter photo image

    Parameters:
        image_id (str): The filename identifier of the image
        size (tuple<int, int>): The size of the image to load
        prefix (str): The prefix to prepend to the filepath (i.e. root directory
        suffix (str): The suffix to append to the filepath (i.e. file extension)
    """
    width, height = size
    file_path = os.path.join(prefix, "%sx%s"%(width,height), image_id + suffix)
    return tk.PhotoImage(file=file_path)


# This allows you to simply load png images with PIL if you have it,
# otherwise will default to gifs through tkinter directly
load_image = load_image_pil if HAS_PIL else load_image_tk  # pylint: disable=invalid-name

DEFAULT_ANIMATION_DELAY = 0  # (ms)
ANIMATION_DELAYS = {
    # step_name => delay (ms)
    'ACTIVATE_ALL': 50,
    'ACTIVATE': 100,
    'ANIMATION_BEGIN': 300,
    'ANIMATION_DONE': 0,
    'ANIMATION_STEP': 200
}

COUNT=[]

def get_Dot(dot):
    """To get dots
    """
    if dot[-1]=='d':
         return WildcardDot()
    i=int(dot[-1])
    if dot[:-2]=='basic':
        return BasicDot(i)
    elif dot[:-2]=='companion':
        return CompanionDot(i)
    elif dot[:-4]=='beam':
        axis=dot.split('/')[1]
        return BeamDot(axis, i)
    elif dot[:-2]=='swirl':
        return SwirlDot(i)
def get_random_position(game):
	grid_list=[_ for _ in game.grid]
	while True:
		position=random.sample(grid_list,1)[0]
		if not isinstance(game.grid[position],VoidCell):
			return position


class CompanionDot(BasicDot):
	""""""
	DOT_NAME = "companion"

	def activate(self,position,game,activated,has_loop=False):
		self._expired=True
		COUNT.append(0)


class SwirlDot(BasicDot):
	"""When activated, the swirl dot changes the kind (colour) of adjacent dots to its kind."""
	DOT_NAME = "swirl"

	def activate(self,position,game,activated,has_loop=False):
		self._expired = True
		x,y=position
		for xi in range(x-1,x+2):
			for yi in range(y-1,y+2):
				dot=game.grid[(xi,yi)].get_dot()
				try:
					dot.set_kind(self.get_kind())
				except Exception:
					pass

class BeamDot(BasicDot):
    """Beam dots can be orientated horizontally,
        vertically, or both. When a beam dot is activated
         it will activate all dots along the same horizontal and vertical axis
    """
    
    DOT_NAME = "beam"

    def __init__(self,axis,kind):
	    super().__init__(kind)
	    self.axis=axis

    def get_view_id(self):
	    return "{}/{}/{}".format(self.get_name(), self.axis, self.get_kind())

    def get_axis_list(self,position):
	    x,y=position
	    if self.axis=='x':
		    self.axis_list = [(x, yi) for yi in range(8)]
	    if self.axis=='y':
		    self.axis_list = [(xi, y) for xi in range(8)]
	    if self.axis=='xy':
		    self.axis_list = [(xi, y) for xi in range(8)]+[(x, yi) for yi in range(8)]

    def activate(self,position,game,activated,has_loop=False):
	    self._expired=True
	    self.get_axis_list(position)
	    to_activate = set(self.axis_list)
	    return to_activate
	
class PenguinCompanion(AbstractCompanion):
	NAME = 'penguin'
	_charge = 0

	def activate(self, game):
		positon = get_random_position(game)
		game.grid[positon].set_dot(WildcardDot())
		self.reset()

class EskimoCompanion(AbstractCompanion):
	NAME = 'eskimo'
	_charge = 0

	def activate(self, game):
		position=get_random_position(game)
		kind=random.randint(1,4)
		game.grid[position].set_dot(BasicDot(kind))
		self.reset()

def reset_COUNT(count_len):
    while len(COUNT)>0:
        COUNT.pop()
    for i in range(count_len):
        COUNT.append(0)

COMPANIONS = {
    'useless': UselessCompanion(),
    'eskimo': EskimoCompanion(),
    'penguin':PenguinCompanion()
}

STATE={
	1: 'normal',
	0: 'disabled'
}
class Save_Load():
    """To save the current games and to load the previous games"""
    def __init__(self,menu):
            self._Load_game=False
            self._menu=menu
            self.status=None
            self.master=''
            self.action_time=(1,1)
            self.path='memory/'
            self.files=[os.path.splitext(x)[0] for x in os.listdir(self.path) if os.path.splitext(x)[1]=='.txt']

    def save_game(self):
	    self.top=tk.Toplevel()
	    self.top.title("save the game")
	    self.top.attributes("-topmost", 1)
	    tk.Label(self.top,text="name",width=10).grid(row=0,column=0,sticky="E")
	    self.name=tk.StringVar()
	    tk.Entry(self.top,textvariable=self.name,width=20).grid(row=0,column=1)
	    tk.Button(self.top,text='Confirm',command=self.save_txt).grid(row=1,column=0)
	    tk.Button(self.top,text='Cancel',command=self.cancel_save).grid(row=1,column=1)

class ActionBar(tk.Frame):
    """To allow the users to implement soecial actions"""
    def __init__(self,master,dot, initial_time=(1,1)):
	    """
	    """
	    self.b, self.c = initial_time
	    print(initial_time)
	    self._dotsapp=dot
	    tk.Frame.__init__(self,master,bg='white')
	    self.Colour_Remover=ttk.Button(self,text='Colour Remover',width=15,command=self.remover,state=STATE[self.b])
	    self.Colour_Remover.grid(row=0,column=1,padx=10,pady=5)
	    self.Eraser=ttk.Button(self,text='Eraser',width=15,command=self.eraser, state=STATE[self.c])
	    self.Eraser.grid(row=0,column=2,padx=10,pady=5)

    def remover(self):
	    kind=random.randint(1,4)
	    self._dotsapp.remover(kind)
	    self.b=0
	    self.refresh_status()

    def eraser(self):
	    if self._dotsapp._eraser==False:
		    self._dotsapp._eraser=True
		    self.c=0
		    self.refresh_status()

    def refresh_status(self):
	    self.Colour_Remover.configure(state=STATE[self.b])
	    self.Eraser.configure(state=STATE[self.c])
	    print(self.b,self.c)
	    self._dotsapp.refresh_actionbar_time((self.b,self.c))


# Define your classes here
# You may edit as much of DotsApp as you wish
class DotsApp:
    """Top level GUI class for simple Dots & Co game"""

    def __init__(self, master,infopanel,intervalbar,companion):
        """Constructor
        Parameters:
            master (tk.Tk|tk.Frame): The parent widget
            infopanel：A instance of the InfoPanel class
            intervalbar：A instance of the IntervalBar class
            companion：A instance of the Companion class(i.e. UselessCompanion())
        """

        self._master = master
        self._infopanel = infopanel
        self.interval=intervalbar
        self.companion = companion

        self._playing = True
        self._eraser= False

        self._image_manager = ImageManager('images/dots/', loader=load_image)

        # Game
        counts = [10, 15, 25, 25]
        random.shuffle(counts)

        # randomly pair counts with each kind of dot
        objectives = zip([BasicDot(1), BasicDot(2), BasicDot(4), BasicDot(3)], counts)

        self._objectives = ObjectiveManager(objectives)

        # Game
        dead_cells = {(2, 2), (2, 3), (2, 4),
                      (3, 2), (3, 3), (3, 4),
                      (4, 2), (4, 3), (4, 4),
                      (0, 7), (1, 7), (6, 7), (7, 7)}
        if isinstance(self.companion,UselessCompanion):
            self._game = DotGame({BasicDot: 1},objectives=self._objectives, kinds=(1, 2, 3, 4), size=(8, 8),
                             dead_cells=dead_cells)

        else:
            self._game = CompanionGame({BasicDot: 1,CompanionDot: 1},companion=self.companion,objectives=self._objectives, kinds=(1, 2, 3, 4), size=(8, 8),
                             dead_cells=dead_cells)

        # Grid View
        self._grid_view = GridView(master, size=self._game.grid.size(), image_manager=self._image_manager, bg='white')
        self._grid_view.grid()
        self._grid_view.draw(self._game.grid)
        self.draw_grid_borders()

        # Events
        self.bind_events()

        # Set initial score again to trigger view update automatically
        self._refresh_status()

    def draw_grid_borders(self):
        """Draws borders around the game grid"""

        borders = list(self._game.grid.get_borders())

        # this is a hack that won't work well for multiple separate clusters
        outside = max(borders, key=lambda border: len(set(border)))

        for border in borders:
            self._grid_view.draw_border(border, fill=border != outside)

    def bind_events(self):
        """Binds relevant events"""
        self._grid_view.on('start_connection', self._drag)
        self._grid_view.on('move_connection', self._drag)
        self._grid_view.on('end_connection', self._drop)

        self._game.on('reset', self._refresh_status)
        self._game.on('complete', self._drop_complete)

        self._game.on('connect', self._connect)
        self._game.on('undo', self._undo)

    def _animation_step(self, step_name):
        """Runs for each step of an animation
        
        Parameters:
            step_name (str): The name (type) of the step    
        """
        print(step_name)
        if step_name == 'ANIMATION_DONE':
            self._refresh_status()
        self.draw_grid()

    def animate(self, steps, callback=lambda: None):
        """Animates some steps (i.e. from selecting some dots, activating companion, etc.
        
        Parameters:
            steps (generator): Generator which yields step_name (str) for each step in the animation
        """

        if steps is None:
            steps = (None for _ in range(1))

        animation = create_animation(self._master, steps,
                                     delays=ANIMATION_DELAYS, delay=DEFAULT_ANIMATION_DELAY,
                                     step=self._animation_step, callback=callback)
        animation()

    def _drop(self, position):  # pylint: disable=unused-argument
        """Handles the dropping of the dragged connection

        Parameters:
            position (tuple<int, int>): The position where the connection was
                                        dropped
        """
        if self._eraser:
            steps=self._game.activate_all([position])
            self._eraser=False
            return self.animate(steps)


        if not self._playing:
            return

        if self._game.is_resolving():
            return

        self._grid_view.clear_dragged_connections()
        self._grid_view.clear_connections()

        self.animate(self._game.drop())

    def _connect(self, start, end):
        """Draws a connection from the start point to the end point

        Parameters:
            start (tuple<int, int>): The position of the starting dot
            end (tuple<int, int>): The position of the ending dot
        """

        if self._game.is_resolving():
            return
        if not self._playing:
            return
        self._grid_view.draw_connection(start, end,
                                        self._game.grid[start].get_dot().get_kind())

    def _undo(self, positions):
        """Removes all the given dot connections from the grid view

        Parameters:
            positions (list<tuple<int, int>>): The dot connects to remove
        """
        for _ in positions:
            self._grid_view.undo_connection()

    def _drag(self, position):
        """Attempts to connect to the given position, otherwise draws a dragged
        line from the start

        Parameters:
            position (tuple<int, int>): The position to drag to
        """

        if self._game.is_resolving():
            return
        if not self._playing:
            return

        tile_position = self._grid_view.xy_to_rc(position)

        if tile_position is not None:
            cell = self._game.grid[tile_position]
            dot = cell.get_dot()

            if dot and self._game.connect(tile_position):
                self._grid_view.clear_dragged_connections()
                return

        kind = self._game.get_connection_kind()

        if not len(self._game.get_connection_path()):
            return

        start = self._game.get_connection_path()[-1]

        if start:
            self._grid_view.draw_dragged_connection(start, position, kind)

    @staticmethod
    def remove(*_):
        """Deprecated in 1.1.0"""
        raise DeprecationWarning("Deprecated in 1.1.0")

    def draw_grid(self):
        """Draws the grid"""
        self._grid_view.draw(self._game.grid)

    def reset(self):
        """Resets the game"""
        pass
        # raise NotImplementedError()

    def check_game_over(self):
        """Checks whether the game is over and shows an appropriate message box if so"""
        state = self._game.get_game_state()

        if state == self._game.GameState.WON:
            showinfo("Congratulations!", "You won!!!")
            self._playing = False
        elif state == self._game.GameState.LOST:
            showinfo("Game Over!",
                     "You didn't reach the goal in time. You got %s points"%self._game.get_score())
            self._playing = False

    def _drop_complete(self):
        """Handles the end of a drop animation"""

        # Useful for when implementing a companion
        if self.companion.is_fully_charged():
            self.companion.reset()
            steps = self.companion.activate(self._game)
            self._refresh_status()

            return self.animate(steps)

        # Need to check whether the game is over
        # raise NotImplementedError()  # no mercy for stooges

    def remover(self,kind):
        """ For ActionBar to call by using method remover in task4.
        To implement the action Colour Remover: Immediately activates (& removes) all dots of a random kind (colour)"""
        to_activate=[]
        for position in self._game.grid:
            if not isinstance(self._game.grid[position],VoidCell):
                if self._game.grid[position].get_dot().get_kind() == kind:
                    self._game.connect(position)
                    to_activate.append(position)

        steps=self._game.activate_all(to_activate)
        return self.animate(steps)

    def _refresh_status(self):
        """Handles change in score"""
        score = self._game.get_score()
        # refresh the relevant widget
        self._infopanel.set_scores(score)
        self._infopanel.set_moves(self._game._moves)
        self._infopanel.set_dots(self._objectives.get_status())
        self.interval.set_scores(score)

        self.check_game_over()
        if not isinstance(self.companion,UselessCompanion):
            print(len(COUNT))
            if len(COUNT)>=6:
                self.companion.charge(len(COUNT))
                reset_COUNT(0)

        # refresh status for the Save_Load class,so that player can save game anytime

    def refresh_actionbar_time(self,time):
        print('refresh_actionbar_time1',time)
        print('refresh_actionbar_time2',time)

class MenuBar():
    """To display all the buttons.
    """
    def __init__(self,master):
        self.save=Save_Load(self)
        self._master=master
        self.companion=UselessCompanion()
        self.menu=tk.Menu(master)

        self.filemenu=tk.Menu(self.menu,tearoff =0)
        self.filemenu.add_command(label="New Game",command=self.new_game)
        self.filemenu.add_command(label="Exit",command=self.exit_game)
        self.menu.add_cascade(label="File", menu=self.filemenu)

        self.filemenu =tk.Menu(self.menu, tearoff=0)
        self.filemenu.add_command(label="Uselesscompanion",command=self.useless)
        self.filemenu.add_command(label="PenguinCompanion",command=self.penguin)
        self.filemenu.add_command(label="EskimoCompanion",command=self.eskimo)
        self.menu.add_cascade(label="Choose", menu=self.filemenu)

        self.filemenu =tk.Menu(self.menu, tearoff=0)
        self.filemenu.add_command(label="Save the game",command=self.save.save_game)
        self.menu.add_cascade(label="Save", menu=self.filemenu)

        self.frame=tk.Frame(self._master,bg='white')
        self.frame.grid()
        start_game(self)

    def new_game(self,actionbar_time=[1,1]):
        """To start a new game"""
        reset_COUNT(0)
        self.frame.destroy()
        self.frame = tk.Frame(self._master,bg='white')
        self.frame.grid()
        start_game(self,actionbar_time=actionbar_time)

    def exit_game(self):
        exit_w= tk.messagebox.askyesno("Quit game","Are you Sure？")
        if exit_w:
            self._master.quit()

    def useless(self):
        reset_COUNT(0)
        self.companion=UselessCompanion()
        self.frame.destroy()
        self.frame=tk.Frame(self._master,bg='white')
        self.frame.grid()
        start_game(self)
        
    def eskimo(self):
        reset_COUNT(0)
        self.companion=EskimoCompanion()
        self.frame.destroy()
        self.frame=tk.Frame(self._master,bg='white')
        self.frame.grid()
        start_game(self)
        
    def penguin(self):
        reset_COUNT(0)
        self.companion=PenguinCompanion()
        self.frame.destroy()
        self.frame=tk.Frame(self._master,bg='white')
        self.frame.grid()
        start_game(self)
        
    def refresh_companion(self,companion):
        """ For Save_Load class to call to refresh the companion if player load a game"""
        self.companion = COMPANIONS[companion]


class InfoPanel(tk.Frame):
    """This class is used to display information to the user, such as their score, remaining moves and objectives, etc.
    """
    def __init__(self,master,companion):
        self.size=(20,20)
        self._companion=companion
        tk.Frame.__init__(self, master,bg = 'white')
        self.grid()

      
        self.create_remaining_numbers()
        self.create_scores()

      
        self.companion_img('images/companions/')
        self.companion()

       
        self.canvas = tk.Canvas(self , bg = "white")
        self.canvas.grid(row=1,column=4,columnspan=4,sticky='N',padx=20)
        self._image_manager = ImageManager('images/dots/', loader=load_image)
        self.dots=[BasicDot(1), BasicDot(2), BasicDot(4), BasicDot(3)]
        self.draw_dots = [0]*10
        for i in range(len(self.dots)):
            dot=self.dots[i]
            dot_img=self.load_image(dot,self.size)
            self.draw_dot(dot_img,i)
            self.get_dot_count(i,0)


    def create_remaining_numbers(self):
        """To show how many moves you have in the beginning"""
        self.remaining=tk.Label(self,text='20',font=("Times", "30"),bg = 'white')
        self.remaining.grid(row=1,column=0,sticky='S',padx=25)

    def create_scores(self):
        """To show how many scores you have in the beginning"""
        self.scores=tk.Label(self,text='0',font=("Times", "20"),fg='black',bg = 'white')
        self.scores.grid(column=2,row=2, sticky='E',padx=20)

    def companion_img(self,prefix):
        suffix ='.gif'
        img_path=os.path.join(prefix,self._companion.get_name()+suffix)
        load_img=Image.open(img_path)
        self.com_img=ImageTk.PhotoImage(load_img)

    def companion(self):
        self.img_logo = tk.Label(self,image=self.com_img,bg = 'white')
        self.img_logo.grid(row=0,column=3,rowspan=3)

    def load_image(self, cell, size):
        return self._image_manager.load(cell.get_view_id(), size)

    def draw_dot(self,dot_image,i):
        tk.Label(self.canvas,image=dot_image,bg = 'white').grid(row=0,column=i,sticky='N',padx=5)

    def get_dot_count(self,i,count):
        self.draw_dots[i]=tk.Label(self.canvas,text=str(count),font=("Times", "10"),bg = 'white')
        self.draw_dots[i].grid(row=1,column=i)

    def set_scores(self,score):
        """To show how many scores you have after each step"""
        self.scores.configure(text=score)

    def set_moves(self,moves):
        """To show how many moves left after each step"""
        self.remaining.configure(text=moves)

    def set_dots(self,objectives):
        for i in range(len(objectives)):
            count=objectives[i][1]
            self.draw_dots[i].configure(text=str(count))


class IntervalBar(tk.Canvas):
    """IntervalBar, which inherits from tk.Canvas. This class should display a horizontal progress bar with vertical lines dividing each step,
        allowing the user to see progress from 0, 1, …, steps-1, steps, inclusive. 
    """
    def __init__(self,master,kind):
        """
        master: The parent widget
        kind (int): The are two kinds of parameters the class use.
        """
        dict1 = {'pad':10,'x':50,'y':20,'outline':'black','fill':'blue'}
        dict2 = {'pad':5,'x':20,'y':10,'outline':'blue','fill':'red'}
        dict_list = [dict1,dict2]
        self.dict = dict_list[kind]
        self.width=self.dict['x']*6+self.dict['pad']*2
        self.height=self.dict['y']+self.dict['pad']*2
        tk.Canvas.__init__(self,master,width=self.width,height=self.height,bg='white')
        for i in range(6):
            x1=self.dict['x']*i+self.dict['pad']
            x2=self.dict['x']*(i+1)+self.dict['pad']
            y1=self.dict['pad']
            y2=self.dict['y']+self.dict['pad']
            rect='rect'+str(i)
            self.create_rectangle(x1,y1,x2,y2,outline = self.dict['outline'],width = 1,tags = rect)

    def set_scores(self,score):
        for i in range(6):
            rect='rect'+str(i)
            if i+1<=(score%6):
                self.itemconfigure(rect,fill=self.dict['fill'])
            else:
                self.itemconfigure(rect,fill='white')

def start_game(master,actionbar_time=[1,1]):
    frame=master.frame
    infol=InfoPanel(frame,master.companion)
    interval=IntervalBar(frame,0)
    interval.grid()
    dot=DotsApp(frame,infol, interval,master.companion)
    actionbar=ActionBar(frame,dot,initial_time=actionbar_time)
    actionbar.grid()
    frame.grid()

def main():
    """Sets-up the GUI for Dots & Co"""
    # Write your GUI instantiation code here
    root=tk.Tk()
    root.geometry('600x800+200+80')
    root.config(bg='white')
    root.title('Dots & Co')
    menubar = MenuBar(root)
    root.config(menu=menubar.menu)
    root.mainloop()
    # pass


if __name__ == "__main__":
    main()
