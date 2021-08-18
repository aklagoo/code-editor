import tkinter as tk
import subprocess

    

def write_slogan():
    print("Tkinter is easy to use!")

root = tk.Tk()
frame = tk.Frame(root)
frame.pack()

button = tk.Button(frame, 
                   text="button 1", 
                   fg="red",
                   command="exit")
button.pack(side=tk.LEFT)
button= tk.Button(frame,
                   text="button 2",
                   fg="blue",
                   command="exit")
button.pack(side=tk.LEFT)
button = tk.Button(frame, 
                   text="button 3", 
                   fg="yellow",
                   command="exit")
button.pack(side=tk.LEFT)
button = tk.Button(frame, 
                   text="button 4", 
                   fg="green",
                   command="exit")
button.pack(side=tk.LEFT)
button = tk.Button(frame, 
                   text="button 5", 
                   fg="grey",
                   command="exit")
button.pack(side=tk.LEFT)
button = tk.Button(frame, 
                   text="button 6", 
                   fg="red",
                   command=quit)
button.pack(side=tk.LEFT)


root.mainloop()