"""
The Action Bar with two actions:
Companion Charge: Immediately activates the companion
Colour Remover: Immediately activates (& removes) all dots of a random kind (colour)
Eraser: Allows the user to choose any one dot; activates (& removes) that dot
"""

import tkinter as tk
from tkinter import ttk
import random

STATE={
	1: 'normal',
	0: 'disabled'
}


class ActionBar(tk.Frame):
	def __init__(self,master,dot, initial_time=(1, 1)):
		"""
		self.b:the remaining time for Colour_Remover
		self.c:the remaining time for Eraser
		"""
		self.a, self.b, self.c = initial_time
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
		print(self.a,self.b,self.c)
		self._dotsapp.refresh_actionbar_time((self.b,self.c))
