import tkinter as tk
import json

class ThemedFrame(tk.Frame):
	def __init__(self, parent, row, col):
		#Storing row and column
		self.row = row
		self.col = col

		#Initializing display settings
		tk.Frame.__init__(self, parent)

		#Initializing dictionary widgets
		self.widgets = {"normal":[], "contrast":[], "contrast2":[]}

		#Adding self to dictionary
		self.add("normal", self)

	def paint(self):
		settings = json.load(open("settings/settings.json", 'r'))

		theme_gen = json.load(open("settings/theme.json", 'r'))
		theme_gen = theme_gen[settings["theme"]]["general"]

		#PREPROCESSING: Converting font list from JSON to tuple in dictionary for all 'normal', 'contrast' and 'contrast2' themes
		font_t = theme_gen["normal"]["font"]
		font_t = (font_t[0], font_t[1])
		theme_gen["normal"]["font"] = font_t
		font_t = theme_gen["contrast"]["font"]
		font_t = (font_t[0], font_t[1])
		theme_gen["contrast"]["font"] = font_t

		#Painting theme onto all widgets
		for scheme in theme_gen:
			for widget in self.widgets[scheme]:
				for attribute in theme_gen[scheme]:
					if attribute in dict(widget):
						widget[attribute] = theme_gen[scheme][attribute]
	def add(self, scheme, widget):
		#EDIT IN FINAL STAGE
		if scheme in self.widgets:
			self.widgets[scheme].append(widget)
		else:
			print("INVALID VALUE FOR scheme")

	def show(self):
		self.grid(row=self.row, column=self.col, sticky='nsew')
		self.paint()

#Modified Text Widget
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