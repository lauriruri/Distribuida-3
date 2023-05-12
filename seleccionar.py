import tkinter as tk
import tkinter.colorchooser as col
import tkinter.simpledialog as sd
from tkinter import messagebox


class myGraph():

    def __init__(self, root):
        self.root = root
      

    

def main():
    root = tk.Tk()
    game = myGraph(root)
    root.mainloop()
    answer = messagebox.askyesno(title="Pregunta", message="Is the Earth flat?")
    if answer == True:
        print('Flat Earther')
    else:
        print('normal people')
    

if __name__ == '__main__':
    main()

     