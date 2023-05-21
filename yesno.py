from tkinter import messagebox
  
def main():
    answer = messagebox.askyesno(title="Pregunta", message="Is the Earth flat?")
    if answer == True:
        print('Flat Earther')
    else:
        print('normal people')
    

if __name__ == '__main__':
    main()

     
