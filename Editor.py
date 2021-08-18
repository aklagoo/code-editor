import tkinter as tk
from res.Widgets import ThemedFrame, ModifiedText
from res.Utilities import SyntaxHighlighter, AutoTabber

class Editor(ThemedFrame):
	def __init__(self, parent, row, column):
		#Initialization
		super(Editor, self).__init__(parent, row, column)
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)

		#Adding text
		self.editField = ModifiedText(self, wrap="word", tabs=('0.4c'))
		self.editField.grid(row=0, column=0, sticky='nsew', padx=4, pady=4)
		self.editField.set_callback(self.text_callback)
		self.add("normal", self.editField)

		#Attaching higlighter
		self.highlighter = SyntaxHighlighter(self.editField, "Python2")
		self.editField.bind("<KeyRelease>", self.run_utilities)

		#Creating tabber
		self.tabber = AutoTabber(self.editField)

		#Adding scrollbar
		self.scrollbar = tk.Scrollbar(self, command=self.editField.yview)
		self.scrollbar.grid(row=0, column=1, sticky='nsew')
		self.editField['yscrollcommand'] = self.scrollbar
		self.add("normal", self.scrollbar)

		#Displaying
		self.show()

	def text_callback(self, result, *args):
		self.index = self.editField.index("insert")

	def run_utilities(self, ev):
		if(self.highlighter.isAlive()==False):
			self.highlighter.run()
		self.tabber.key(self.index, ev)

root = tk.Tk()
e = Editor(root, 0, 0)
root.mainloop()