import tkinter as tk
from res.Widgets import ThemedFrame
class TestClass(ThemedFrame):
	def __init__(self, parent, row, column):
		super(TestClass, self).__init__(parent, row, column)

		#Add button
		butt = tk.Button(self, text="contrast")
		butt.grid(padx=10, pady=10)
		self.add("contrast", butt)

		#Add label
		lab = tk.Label(self, text="normal")
		lab.grid(padx=10, pady=10)
		self.add("normal", lab)

		#Displaying self
		self.show()


root = tk.Tk()
f = TestClass(root, 0, 0)
root.mainloop()