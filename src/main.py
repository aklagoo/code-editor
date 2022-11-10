import tkinter as tk
from src.components.app import App

if __name__ == "__main__":
    root = tk.Tk()
    t = App(root, 0, 0)
    root.geometry("1000x600")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.mainloop()
