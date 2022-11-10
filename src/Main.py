import tkinter as tk
from tkinter import ttk
from src.res import ThemedFrame, ModifiedText
from src.res.Utilities import SyntaxHighlighter, AutoTabber, CompileAndRun


DEFAULT_FILE = "empty.txt"


class Editor(ThemedFrame):
    def load(self, filename):
        if filename is not None:
            file = open(filename, "r")
            l = 0
            for line in file:
                l += 1
                self.editField.insert(str(l) + '.0', line)
        if not self.highlighter.isAlive():
            self.highlighter.run()

    def __init__(self, parent, row, column, filename=None):
        # Initialization
        super(Editor, self).__init__(parent, row, column)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Adding text
        self.editField = ModifiedText(self, wrap="word", tabs=('0.4c'))
        self.editField.grid(row=0, column=0, sticky='nsew', padx=3, pady=6)
        self.editField.set_callback(self.text_callback)
        self.add("normal", self.editField)

        # Attaching higlighter
        self.highlighter = SyntaxHighlighter(self.editField, "Python2")
        self.editField.bind("<KeyRelease>", self.run_utilities)

        # Creating tabber
        self.tabber = AutoTabber(self.editField)

        # Adding scrollbar
        self.scrollbar = ttk.Scrollbar(self, command=self.editField.yview)
        self.scrollbar.grid(row=0, column=1, sticky='nsew')
        self.editField['yscrollcommand'] = self.scrollbar
        self.add("normal", self.scrollbar)

        # Loading file
        self.load(filename)

        # Displaying
        self.show()

    def text_callback(self, result, *args):
        self.index = self.editField.index("insert")

    def run_utilities(self, ev):
        if not self.highlighter.isAlive():
            self.highlighter.run()
        self.tabber.key(self.index, ev)


class CompileDisplay(ThemedFrame):
    def __init__(self, parent, row, column, filename=None, lang=None):
        # Adding filename and language
        self.filename = filename
        self.lang = lang

        # Initialization
        super(CompileDisplay, self).__init__(parent, row, column)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.add("contrast2", self)

        # Adding textfield
        self.terminal = tk.Text(self, wrap="word", tabs=('0.4c'), height=10)
        self.terminal.grid(row=0, column=0, sticky='nsew', padx=2, pady=4)
        self.add("normal", self.terminal)

        # Adding scrollbar
        self.scrollbar = ttk.Scrollbar(self, command=self.terminal.yview)
        self.scrollbar.grid(row=0, column=1, sticky='nsew')
        self.terminal['yscrollcommand'] = self.scrollbar
        self.add("normal", self.scrollbar)

        # Adding CompileAndRun module
        self.cr = self.gen_compiler()

        # Displaying
        self.show()

    def error_check(self):
        if self.filename is None:
            self.terminal.delete('1.0', tk.END)
            self.terminal.insert(tk.END, "Error: No file found!")
            return True
        elif self.lang is None:
            self.terminal.delete('1.0', tk.END)
            self.terminal.insert(tk.END, "Error: No language found!")
            return True
        return False

    def gen_compiler(self):
        if not self.error_check():
            cr = CompileAndRun(self.filename, self.terminal, self.lang)
            return cr

    def compile(self):
        self.cr.compile()

    def run(self):
        self.cr.run()


class Main(ThemedFrame):
    def __init__(self, parent, row, column):
        super(Main, self).__init__(parent, row, column)

        # Add editor
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.editor = Editor(self, 0, 0, DEFAULT_FILE)

        # Adding terminal
        self.terminal = CompileDisplay(self, 1, 0, DEFAULT_FILE, "Python3")

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


if __name__ == "__main__":
    root = tk.Tk()
    t = Main(root, 0, 0)
    root.geometry("1000x600")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.mainloop()
