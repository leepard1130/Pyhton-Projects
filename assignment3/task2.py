"""
Dots and Companions classes for task2 and task4
The Dots I choose:WildcardDot,SwirlDot,BeamDot
The Companions I choose:BuffaloCompanion,EskimoCompanion,CaptainCompanion
"""

from dot import BasicDot,WildcardDot
from companion import AbstractCompanion
from cell import VoidCell
import random

#the COUNT is a list
#every time a companiondot is activated,the COUNT.append(0)
#so the len(COUNT) can tell us how much charge the companion has after each move
COUNT=[]


def get_random_position(game):
	grid_list=[_ for _ in game.grid]
	while True:
		position=random.sample(grid_list,1)[0]
		if not isinstance(game.grid[position],VoidCell):
			return position


class CompanionDot(BasicDot):
	"""A companion dot"""
	DOT_NAME = "companion"

	def activate(self,position,game,activated,has_loop=False):
		self._expired=True
		COUNT.append(0)


class SwirlDot(BasicDot):
	"""A swirldot dot"""
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


class BuffaloCompanion(AbstractCompanion):
	NAME = 'buffalo'
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
		game.grid[position].set_dot(SwirlDot(kind))
		self.reset()


class CaptainCompanion(AbstractCompanion):
	NAME = 'captain'
	_charge = 0
	axis_kind=['x','y','xy']

	def activate(self, game):
		position = get_random_position(game)
		kind = random.randint(1,4)
		axis = random.sample(self.axis_kind,1)[0]
		game.grid[position].set_dot(BeamDot(axis,kind))