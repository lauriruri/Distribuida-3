import tkinter as tk

class myGraph:

    def __init__(self, root):
        self.root = root
        root.title('Practica 3')
        root.geometry("500x500")
        self.create_graphs()
        self.data = []
        
    def create_graphs(self):
        self.message = tk.Label(self.root, text="Instrucciones")
        self.message.pack(fill='both', expand =1)
        self.label1 = tk.Label(self.root, text="Respuesta:", \
                               font = 'Arial 14', bg = 'red')
        self.label1.pack(fill='both', expand =1)
        self.entry1 = tk.Entry(self.root, font= 'Arial 12')
        self.entry1.pack(fill='both', expand =1)
        self.message = tk.Label(self.root, text="Escribe y pulse el button")
        self.message.pack(fill='both', expand =1)

        self.button = tk.Button(self.root, text="Storar Datos",\
                                font= 'Arial 14', command=self.store_texts, bg = 'green')
        self.button.pack(fill='both', expand =1)

    def store_texts(self):
        self.text1 = self.entry1.get()
        if self.text1 :
            self.data.append(self.text1)
            self.root.destroy()
        else:
            self.message.configure(text="Escribe y pulse el button")
        print(self.data)


    def start(self):
        self.root.mainloop()
    


root = tk.Tk()
app = myGraph(root)
app.start()
