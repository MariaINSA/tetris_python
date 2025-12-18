import tkinter as tk
from tkinter import messagebox
import libs.graphics.name_input as name_input
from tkinter.font import Font

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        bg_im = tk.PhotoImage(file = "content/bg_main.png")
        bg_label = tk.Label(self, image=bg_im)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        # Keep a reference
        bg_label.image = bg_im

        title_label = tk.Label(self, text="TETRIS", bg="#0b316f",font=("Arial", 28, "bold"),fg="#FFFFFF")
        title_label.pack(pady=30)

        #WHY LAMBDA???????
        btn_play = tk.Button(self, text="Play", font=("Arial", 14), width=15,fg="#1E1E2F", command=self.start_game)
        btn_play.pack(pady=20)

        btn_scores = tk.Button(self, text="High Scores", font=("Arial", 14),fg="#1E1E2F", width=15, command=lambda:controller.show_frame("HighScores"))
        btn_scores.pack(pady=20)

        btn_quit = tk.Button(self, text="Quit", font=("Arial", 14),fg="#1E1E2F", width=15, command=self.controller.quit)
        btn_quit.pack(pady=20)

    def start_game(self):
        dialog = name_input.NameDialog(self)
        player_name = dialog.result
        if player_name:
            #messagebox.showinfo("Welcome", f"Starting game for {player_name}")
            self.controller.show_frame("PlayScreen",player_name)
            # Aquí iría tu lógica para iniciar el juego Tetris

    def open_options(self):
        # Ventana simple de opciones
        options_win = tk.Toplevel(self.controller)
        options_win.title("Options")

        tk.Label(options_win, text="Game options", font=("Arial", 14)).pack(pady=10)
        tk.Label(options_win, text="(Change what you will)").pack(pady=5)

        tk.Button(options_win, text="Close", command=options_win.destroy).pack(pady=10)
