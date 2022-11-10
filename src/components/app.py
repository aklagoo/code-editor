import tkinter as tk

from src.components import Editor, Terminal
from src.res import ThemedFrame

DEFAULT_FILE = "empty.txt"


class App(ThemedFrame):
    def __init__(self, parent, row, column):
        super(App, self).__init__(parent, row, column)

        # Add editor
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.editor = Editor(self, 0, 0, DEFAULT_FILE)

        # Adding terminal
        self.terminal = Terminal(self, 1, 0, DEFAULT_FILE, "Python3")

        # Menu
        self.menu = tk.Menu(parent)
        parent.config(menu=self.menu)

        # File Menu: New, Open, Save, Save As
        menu_file = tk.Menu(self.menu, tearoff=0)
        menu_file.add_command(label="Exit", command=quit)
        self.menu.add_cascade(label="File", menu=menu_file)

        # Themes menu
        self.menu_theme = tk.Menu(self.menu, tearoff=0)
        self.menu_theme.add_radiobutton(label="Light",
                                        command=lambda: print("0"))
        self.menu_theme.add_radiobutton(label="Dark",
                                        command=lambda: print("1"))
        self.menu.add_cascade(label="Themes", menu=self.menu_theme)

        # Language menu
        self.menu_lang = tk.Menu(self.menu, tearoff=0)
        self.menu_lang.add_radiobutton(label="C", command=lambda: print("C"))
        self.menu_lang.add_radiobutton(label="C++",
                                       command=lambda: print("C++"))
        self.menu_lang.add_radiobutton(label="Java",
                                       command=lambda: print("Java"))
        self.menu_lang.add_radiobutton(label="Python2",
                                       command=lambda: print("python2"))
        self.menu_lang.add_radiobutton(label="Python3",
                                       command=lambda: print("python3"))
        self.menu.add_cascade(label="Language", menu=self.menu_lang)

        # Run menu
        self.menu_run = tk.Menu(self.menu, tearoff=0)
        self.menu_run.add_command(label="Compile",
                                  command=self.terminal.compile)
        self.menu_run.add_command(label="Run", command=self.terminal.run)
        self.menu.add_cascade(label="Run", menu=self.menu_run)

        # Show App Frame
        self.show()
