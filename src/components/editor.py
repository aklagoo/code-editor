from tkinter import ttk

from src.res import ThemedFrame, ModifiedText, SyntaxHighlighter, AutoTabber


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
