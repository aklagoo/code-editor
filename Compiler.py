import tkinter as tk
from res.Widgets import ThemedFrame
from res.Utilities import CompileAndRun

class CompileDisplay(ThemedFrame):
	def __init__(self, parent, row, column, filename=None, lang=None):
		#Adding filename and language
		self.filename = filename
		self.lang = lang

		#Initialization
		super(CompileDisplay, self).__init__(parent, row, column)
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)

		#Adding textfield
		self.terminal = tk.Text(self, wrap="word", tabs=('0.4c'))
		self.terminal.grid(row=0, column=0, sticky='nsew', padx=4, pady=4)
		self.add("normal", self.terminal)

		#Adding scrollbar
		self.scrollbar = tk.Scrollbar(self, command=self.terminal.yview)
		self.scrollbar.grid(row=0, column=1, sticky='nsew')
		self.terminal['yscrollcommand'] = self.scrollbar
		self.add("normal", self.scrollbar)

		#Adding CompileAndRun module
		self.cr = self.gen_compiler()

		#Displaying
		self.show()

		self.cr.run()

	#Compiler generator
	def error_check(self):
		if(self.filename==None):
			self.terminal.delete('1.0', tk.END)
			self.terminal.insert(tk.END, "Error: No file found!")
			return True
		elif(self.lang==None):
			self.terminal.delete('1.0', tk.END)
			self.terminal.insert(tk.END, "Error: No language found!")
			return True
		return False
	def gen_compiler(self):
		if self.error_check()==False:
			cr = CompileAndRun(self.filename, self.terminal, self.lang)
			return cr

root = tk.Tk()
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.geometry("800x200")
e = CompileDisplay(root, 0, 0, "C:\\Users\\HOMEPC\\Desktop\\test.py", "Python3")
root.mainloop()
