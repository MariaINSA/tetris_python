import tkinter as tk
from tkinter import messagebox

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
    #def __init__(self,root):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #example on how to call the changing window !!!!!!!!

        #button1 = tk.Button(self, text="Go to Page One",
        #                    command=lambda: controller.show_frame("PageOne"))
        
        title_label = tk.Label(self, text="TETRIS", font=("Arial", 28, "bold"))
        title_label.pack(pady=40)

        btn_play = tk.Button(self, text="Play", font=("Arial", 14), width=15, command=self.start_game)
        btn_play.pack(pady=10)

        btn_scores = tk.Button(self, text="High Scores", font=("Arial", 14), width=15, command=self.show_high_scores)
        btn_scores.pack(pady=10)

        btn_options = tk.Button(self, text="Options", font=("Arial", 14), width=15, command=self.open_options)
        btn_options.pack(pady=10)

        btn_quit = tk.Button(self, text="Quit", font=("Arial", 14), width=15, command=self.controller.quit)
        btn_quit.pack(pady=20)

    def start_game(self):
        # Aquí iría tu lógica para iniciar el juego Tetris
        messagebox.showinfo("Play", "Click here to start the game.")

    def show_high_scores(self):
        # Aquí podrías abrir una nueva ventana o mostrar datos reales
        messagebox.showinfo("High Scores", "No high scores yet.")

    def open_options(self):
        # Ventana simple de opciones
        options_win = tk.Toplevel(self.controller)
        options_win.title("Options")

        tk.Label(options_win, text="Game options", font=("Arial", 14)).pack(pady=10)
        tk.Label(options_win, text="(Change what you will)").pack(pady=5)

        tk.Button(options_win, text="Close", command=options_win.destroy).pack(pady=10)
