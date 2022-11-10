import tkinter as tk
from tkinter import ttk

from src.res import ThemedFrame, CompileAndRun


class Terminal(ThemedFrame):
    def __init__(self, parent, row, column, filename=None, lang=None):
        # Adding filename and language
        self.filename = filename
        self.lang = lang

        # Initialization
        super(Terminal, self).__init__(parent, row, column)
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