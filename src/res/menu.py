import Tkinter
from Tkinter import *
from ScrolledText import *
import tkFileDialog
import tkMessageBox
import Tkinter as tk
import re

settings = {'bg': '#333',
            'fg': '#ccc',
            'font': ('Verdana', 10),
            'relief': 'flat',
            'insertbackground': '#ccc'}

theme = {'bg': [], 'fg': [], 'font': [], 'relief': [], 'insertbackground': []}
theme_syntax = {
    '#E5399E': [r'\bcontinue\b', r'\bfor\b', r'\blambda\b', r'\btry\b', r'\bclass\b', r'\bfinally\b', r'\bis\b',
                r'\breturn\b', r'\bwhile\b', r'\bdef\b', r'\bfrom\b', r'\band\b', r'\bdel\b', r'\bglobal\b', r'\bnot\b',
                r'\bwith\b', r'\bas\b', r'\belif\b', r'\bif\b', r'\bor\b', r'\byield\b', r'\bassert\b', r'\belse\b',
                r'\bimport\b', r'\bpass\b', r'\bbreak\b', r'\bexcept\b', r'\bin\b', r'\braise\b'],
    '#886ED7': [r'\bTrue\b', r'\bFalse\b', r'\bNone\b'],
    '#FFDF40': [r"'.{0,}'"],
    '#A2EF00': [r'#.{1,}\Z$', r""]}


class ModifiedText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        private_callback = self.register(self._callback)
        self.tk.eval('''
            proc widget_proxy {wid callback args} {
                set flag ::dont_recurse(wid)
                set result [uplevel [linsert $args 0 $wid]]

                if {! [info exists $flag]} {
                    if {([lindex $args 0] in {insert replace delete}) ||
                        ([lrange $args 0 2] == {mark set insert})} {
                            set $flag 1
                            catch {$callback $result {*}$args } callback_result
                            unset -nocomplain $flag
                    }
                }
                return $result
            }
            ''')
        self.tk.eval('''
            rename {widget} _{widget}
            interp alias {{}} ::{widget} {{}} widget_proxy _{widget} {callback}
        '''.format(widget=str(self), callback=private_callback))

    def _callback(self, result, *args):
        self.callback(result, *args)

    def set_callback(self, callable):
        self.callback = callable


class editor(tk.Frame):
    def add_tabs(self):
        for i in range(self.tab_count):
            self.text.insert(self.index, '\t')

    def callback(self, result, *args):
        self.index = self.text.index("insert")

    def gen_tags(self, e):

        # Tab management
        if (e.keycode == 13):
            self.add_tabs()
            self.past_keys.append(13)

        s = e.widget.get('1.0', tk.END)

        # Splitting text into lines for better scanning
        lines = s.splitlines()

        # Clear previous tags
        for tag in e.widget.tag_names():
            e.widget.tag_delete(tag)

        # Searching and adding tags
        for color in self.theme_syntax:
            for kwrd in self.theme_syntax[color]:
                l = 0
                e.widget.tag_config(color, foreground=color)
                for line in lines:
                    l += 1
                    t = [[m.start(), m.end()] for m in re.finditer(kwrd, line)]
                    if t != []:
                        for i in t:
                            t1 = str(l) + '.' + str(i[0])
                            t2 = str(l) + '.' + str(i[1])
                            e.widget.tag_add(color, t1, t2)

    def load_all(self):
        for att in self.theme:
            for widget in self.widgets:
                if att in dict(widget):
                    self.theme[att].append(widget)

    def __init__(self, parent, theme, theme_syntax):
        # Storing theme values
        self.theme = theme
        self.theme_syntax = theme_syntax

        # List of widgets
        self.widgets = []

        # Initializing tab variables
        self.tab_count = 0

        # self.past_keys
        self.past_keys = []

        # Initializing all areas
        tk.Frame.__init__(self, parent)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky='nsew')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.widgets.append(self)

        # Creating and placing the text
        self.text = ModifiedText(self)
        self.text.grid(row=0, column=0, padx=4, pady=4, sticky='nsew')
        self.text.bind('<KeyRelease>', self.gen_tags)
        self.text.set_callback(self.callback)
        self.widgets.append(self.text)

        # Connecting all the widgets
        self.load_all()


def paint_all(settings, theme):
    for k in settings:
        for w in theme[k]:
            w[k] = settings[k]


paint_all(settings, theme)

root = Tkinter.Tk(className=" Just another Text Editor")
textPad = editor(root, theme, theme_syntax)


# create a menu & define functions for each menu item

def open_command():
    file = tkFileDialog.askopenfile(parent=root, mode='rb', title='Select a file')
    if file != None:
        contents = file.read()
        textPad.insert('1.0', contents)
        file.close()


def save_command(self):
    file = tkFileDialog.asksaveasfile(mode='w')
    if file != None:
        # slice off the last character from get, as an extra return is added
        data = self.textPad.get('1.0', END + '-1c')
        file.write(data)
        file.close()


def exit_command():
    if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()


def about_command():
    label = tkMessageBox.showinfo("About", "Just Another TextPad \n Copyright \n No rights left to reserve")


def dummy():
    print("I am a Dummy Command, I will be removed in the next step")


menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=dummy)
filemenu.add_command(label="Open...", command=open_command)
filemenu.add_command(label="Save", command=save_command)
filemenu.add_command(label="Save As", command=save_command)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=exit_command)
menu.add_cascade(label="Themes", menu=filemenu)
helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=about_command)

#
textPad.pack()
root.mainloop()