""""The class Save_Load for player to save the game and load a game."""

import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import showinfo
import os

class Save_Load():
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

	def save_txt(self):
		txt_name=self.name.get()
		print(self.files)
		if txt_name in self.files:
			res=tk.messagebox.askyesno("reminder","A file already exists with that name. ")
			if not res:
				return ""
		txt_name=self.name.get()
		self.top.destroy()
		txt_path=os.path.join(self.path,txt_name+'.txt')
		with open(txt_path,'w') as f:
			f.write('%s\n%s\n%s\n%s\n'%(self._move,self._score,self._companion.get_name(),self.count))
			for dot,count in self._objectives_status:
				f.write("%s:%s,"%(dot.get_view_id(),str(count)))
			f.write('\n')
			for position,cell in self._grid.items():
				if cell.get_dot():
					f.write("%s:%s;"%(str(position),cell.get_dot().get_view_id()))
			f.write('\n')
			f.write("{},{},{}".format(self.action_time[0],self.action_time[1],self.action_time[2]))

	def read_txt(self,txt_path):
		with open(txt_path,'r') as f:
			lines_list=f.read().split('\n')
		self._move=int(lines_list[0])
		self._score=int(lines_list[1])
		self._companion=lines_list[2]
		self.count=int(lines_list[3])
		self._objectives_count=[int(x.split(':')[1]) for x in lines_list[4].split(',') if len(x)>0]
		self.grid_list=[[item.split(':')[0],item.split(':')[1]] for item in lines_list[5].split(';') if len(item)>0]
		self.action_time=[int(i) for i in lines_list[6].split(',')]


	def cancel_save(self):
		self.top.destroy()

	def load_game(self):
		txt_path=filedialog.askopenfilename(title=u"选择文件",initialdir=os.path.abspath(self.path),filetypes=[("Txt Files",".txt")])
		if txt_path:
			self.read_txt(txt_path)
			self._Load_game=True
			self._menu.refresh_companion(self._companion)
			self._menu.new_game(self.action_time)
			self._Load_game=False

	def get_status(self,move,score,companion,objectives,grid,count_len=0):
		self._move=str(move)
		self._score=str(score)
		self._companion=companion
		self._objectives_status=objectives
		self._grid=grid
		self.count=count_len

	def get_actionbar_time(self,action_time=(1,1)):
		self.action_time=action_time


