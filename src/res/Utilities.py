import tkinter as tk
import threading
import json
import re
import subprocess
import os

class SyntaxHighlighter(threading.Thread):
	def __init__(self, editor, lang):
		#Initializing the thread
		threading.Thread.__init__(self)

		#Storing variables
		self.lang = lang
		self.editor = editor

		#Loading syntax highlighter theme
		self.load_theme()

	def load_theme(self):
		settings = json.load(open("settings/settings.json", 'r'))
		theme = json.load(open("settings/theme.json", 'r'))
		self.single_line_theme = theme[settings["theme"]]["single_line_syntax"][self.lang]
		#self.multiline_theme = theme[settings["theme"]]["multiline_syntax"][self.lang]
		del theme

	def run(self):
		#Fetching text
		text = self.editor.get("1.0", tk.END)

		#Splitting text into lines
		lines = text.splitlines()

		#Clear previous tags
		for tag in self.editor.tag_names():
			self.editor.tag_delete(tag)

		#SINGLE LINE HIGHLIGHTING
		for color in self.single_line_theme:
			for keyword in self.single_line_theme[color]:
				l = 0
				self.editor.tag_config(color, foreground=color)
				for line in lines:
					l+=1
					matches = [[m.start(), m.end()] for m in re.finditer(re.compile(keyword), line)]

					if matches!=[]:
						for position in matches:
							start_pos = str(l)+'.'+str(position[0])
							end_pos = str(l)+'.'+str(position[1])
							self.editor.tag_add(color, start_pos, end_pos)

class AutoTabber:
	def __init__(self, editor):
		self.enter = True
		self.tab_size = 0
		self.editor = editor

	def key(self, index, event):
		if(event.keysym=="Return"):
			self.enter=True
			self.editor.insert(index, '\t'*self.tab_size)
		elif(event.keysym=="Tab"):
			if(self.enter==True):
				self.tab_size+=1
		elif(event.keysym=="BackSpace"):
			if(self.tab_size>0 and self.enter==True):
				self.tab_size-=1
		else:
			self.enter=False

class CompileAndRun:
	def __init__(self, filename, terminal, lang):
		self.filename = filename
		self.terminal = terminal
		self.lang = lang
		self.compiled = False

		js = json.load(open("settings/lang.json", 'r'))
		self.err = js["error"][json.load(open("settings/settings.json", 'r'))["system"]]
		self.compile_command = js['compile'][self.lang]
		self.execute_command = js['execute'][self.lang]

	def compile(self):
		out = "Successfully compiled!"
		for command_index in range(len(self.compile_command)):
			try:
				self.compile_command[command_index].append(self.filename)
				p = subprocess.check_output(self.compile_command[command_index], shell=True, stderr=subprocess.STDOUT)
				self.compiled = True
				self.run_index=command_index
				break
			except subprocess.CalledProcessError as exc:
				t = exc.output.decode()
				if (self.err in t)==False:
					out = t
		self.terminal.config(state="normal")
		self.terminal.delete('1.0', tk.END)
		self.terminal.insert(tk.END, out)
		self.terminal.config(state="disabled")

	def run(self):
		if(self.compiled==False):
			self.compile()
		try:
			command = self.execute_command[self.run_index]
			command.append(self.filename)
			p = os.system(' '.join(str(x) for x in command))

			return
		except Exception as exc:
			print("Jhol")
			pass
		except FileNotFoundError:
			pass
		self.terminal.config(state="normal")
		self.terminal.delete('1.0', tk.END)
		self.terminal.insert(tk.END, "Successfully executed!")
		self.terminal.config(state="disabled")