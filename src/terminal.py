import tkinter as tk
import subprocess
import re

settings = {'bg': '#333',
            'fg': '#ccc',
            'font': ('Verdana', 10),
            'relief': 'flat',
            'insertbackground' : '#ccc'}

theme = {'bg':[], 'fg':[], 'font':[], 'relief':[], 'insertbackground':[]}
theme_syntax = {'#E5399E':[r'\bcontinue\b', r'\bfor\b', r'\blambda\b', r'\btry\b', r'\bclass\b', r'\bfinally\b', r'\bis\b', r'\breturn\b', r'\bwhile\b', r'\bdef\b', r'\bfrom\b', r'\band\b', r'\bdel\b', r'\bglobal\b', r'\bnot\b', r'\bwith\b', r'\bas\b', r'\belif\b', r'\bif\b', r'\bor\b', r'\byield\b', r'\bassert\b', r'\belse\b', r'\bimport\b',r'\bpass\b',r'\bbreak\b',r'\bexcept\b',r'\bin\b',r'\braise\b'],
                '#886ED7':[r'\bTrue\b', r'\bFalse\b', r'\bNone\b', r'\bint\b', r'\bstr\b'],
                '#FFDF40': [r"'.{0,}'"],
                '#A2EF00':[r'#.{1,}\Z$', r""]}

class terminal(tk.Frame):
    def load_all(self):
        for att in self.theme:
            for widget in self.widgets:
                if att in dict(widget):
                    self.theme[att].append(widget)
    
    def __init__(self, parent, theme, theme_syntax):
        #Storing theme values
        self.theme = theme
        self.theme_syntax = theme_syntax

        #List of widgets
        self.widgets = []
        
        #Initializing all areas
        tk.Frame.__init__(self, parent)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky='nsew')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.widgets.append(self)

        #Creating and placing the text
        self.console = tk.Text(self, state=tk.DISABLED)
        self.console.grid(row=0, column=0, sticky='nsew')
        self.widgets.append(self.console)

        #Connecting all the widgets
        self.load_all()

    def comp(self, filename, language):
        self.err = False
        self.err_line = 0
        if(language=='Python'):
            try:
                output = subprocess.check_output(['python', 'filename'], stderr=subprocess.STDOUT, shell=True, timeout=3)
            except subprocess.CalledProcessError as exc:
                print(exc.output)
                err=True
                self.err_line = re.search(r'(?<=line )(\d*)(?=\))', exc.output)

def paint_all(settings, theme):
    for k in settings:
        for w in theme[k]:
            w[k] = settings[k]

root = tk.Tk()
root.geometry("800x600")
t = terminal(root, theme, theme_syntax)

paint_all(settings, theme)

root.mainloop()
