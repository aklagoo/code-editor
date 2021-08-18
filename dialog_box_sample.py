import tkinter as tk

#Warning: USE GRID ONLY. DON'T USE PACK.

#Creating defaults
theme_settings = {'bg': '#357',
                'fg': '#cde',
                'font': ('Verdana', 10),
                'relief': 'flat',
                'insertbackground' : '#ccc',
                'activebackground': 'black',
                'activeforeground': '#adc'}

theme_widgets = {'bg':[], 'fg':[], 'activebackground':[], 'activeforeground':[], 'font':[], 'relief':[], 'insertbackground':[]}

theme_syntax = {'#9C02A7':[r'\bcontinue\b', r'\bfor\b', r'\blambda\b', r'\btry\b', r'\bclass\b', r'\bfinally\b', r'\bis\b', r'\breturn\b', r'\bwhile\b', r'\bdef\b', r'\bfrom\b', r'\band\b', r'\bdel\b', r'\bglobal\b', r'\bnot\b', r'\bwith\b', r'\bas\b', r'\belif\b', r'\bif\b', r'\bor\b', r'\byield\b', r'\bassert\b', r'\belse\b', r'\bimport\b',r'\bpass\b',r'\bbreak\b',r'\bexcept\b',r'\bin\b',r'\braise\b'],
                '#0A67A3':[r'\bTrue\b', r'\bFalse\b', r'\bNone\b', r'\bint\b', r'\bstr\b'],
                '#FF8E00': [r"'.{0,}'"],
                '#D2F700':[r'#.{1,}\Z$', r""]}

class ThemeDialog(tk.Frame):

    #Function for loading
    def load_all(self):
        for att in self.theme_widgets:
            for widget in self.widgets:
                if att in dict(widget):
                    self.theme_widgets[att].append(widget)
    
    def __init__(self, parent, theme_widgets, theme_syntax, theme_settings):
        tk.Frame.__init__(self, parent)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky='nsew')

        #Initializing variables
        self.widgets = []                       #List of all widgets in the frame
        self.theme_widgets = theme_widgets      #IGNORE: Dictionary containing widgets classified attributes
        self.theme_settings = theme_settings    #Dictionary containing attribute values
        self.theme_syntax = theme_syntax        #Dictionary containing syntax highlighting color schemes.............CHANGE KEYS (they contain color values), NOT VALUES
        
        #Add your content here
                
        self.label = tk.Label(self, text="This is some sample text")
        self.label.grid()
        self.widgets.append(self.label) 
        self.font = tk.Label(self, text="Font:")
        self.font.grid()
        self.widgets.append(self.font)
        self.fontsize = tk.Label(self, text="Font size:")
        self.fontsize.grid(row=0, column=3)
        self.widgets.append(self.fontsize)
        e1 = tk.Entry(self)
        e2 = tk.Entry(self)

        e1.grid(row=0, column=1)
        e2.grid(row=0, column=4)
                
        self.ok = tk.Button(self, text="OK")
        self.ok.grid(row=4, column=1, sticky='nsew', pady=4)
        self.widgets.append(self.ok)
                
        self.cancel=tk.Button(self,text="CANCEL")
        self.cancel.grid(row=4, column=0, sticky='nsew', pady=4)#Cancel button
        self.widgets.append(self.cancel)
        #At the end, use load_all
        self.load_all()

        #Use self.paint_all to apply the changes
        self.paint_all()

    def paint_all(self):
        for k in self.theme_settings:
            for w in self.theme_widgets[k]:
                w[k] = self.theme_settings[k]

root = tk.Tk()
t = ThemeDialog(root, theme_widgets, theme_syntax, theme_settings)
root.mainloop()
