import A_star
import Theta_star
import multiprocessing
import tkinter as tk
from turtle import ScrolledCanvas

def a_star_process():
    
    # Configuro la finestra tkinter
    root = tk.Tk()
    root.title("A* Algorithm")
    root.geometry('750x500+0+0')

    turtle_canvas = ScrolledCanvas(root)
    turtle_canvas.pack(fill=tk.BOTH, expand=True)
    
    # Eseguo l'algoritmo A* all'interno della finestra Tkinter
    A_star.a_star(root, turtle_canvas)

def theta_star_process():
    
    # Configuro la finestra tkinter
    root = tk.Tk()
    root.title("Theta* Algorithm")
    root.geometry('750x500+1000+0')
    
    turtle_canvas_theta = ScrolledCanvas(root)
    turtle_canvas_theta.pack(fill=tk.BOTH, expand=True)

    # Eseguo l'algoritmo Theta* all'interno della finestra Tkinter
    Theta_star.theta_star(root, turtle_canvas_theta)

def main(): 
    # Avvio A*
    processo_programma1 = multiprocessing.Process(target = a_star_process)
    processo_programma1.start()
    
    # Avvio Theta*
    processo_programma2 = multiprocessing.Process(target = theta_star_process)
    processo_programma2.start()

    # Attendere la fine dei processi
    processo_programma1.join()
    processo_programma2.join()

if __name__ == "__main__":
    main() 
