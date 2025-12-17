import tkinter as tk
from tkinter import messagebox

class MiddleMenu(tk.Frame):
    def __init__(self, parent, controller,pause):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.pause=pause
        if pause:
            #pause menu messages
            title="Game Paused"
            play="Resume"
        else:
            #game over menu messages
            title="Game Over"
            play="Try Again"

        #example on how to call the changing window !!!!!!!!
        
        title_label = tk.Label(self, text=title, font=("Arial", 28, "bold"))
        title_label.pack(pady=40)

        #WHY LAMBDA???????
        btn_play = tk.Button(self, text=play, font=("Arial", 14), width=15, command= lambda:controller.show_frame("PlayScreen"))
        btn_play.pack(pady=10)

        btn_quit = tk.Button(self, text="Main Menu", font=("Arial", 14), width=15, command=self.quit_to_menu())
        btn_quit.pack(pady=20)

    def quit_to_menu(self):
        if self.pause:
            #see if its paused so that if were quitting to menu it saves and restarts
            print("cp1")
            self.controller.game_over()
            
        self.controller.show_frame("MainMenu")
