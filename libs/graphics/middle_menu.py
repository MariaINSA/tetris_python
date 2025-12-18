import tkinter as tk
from tkinter import messagebox

class MiddleMenu(tk.Frame):
    """
    Display an intermediate menu during pause or game over.

    The menu shows a title and buttons to resume/retry or go back
    to the main menu.
    """
    def __init__(self, parent, controller,pause):
        """
        Initialize the intermediate menu.

        Parameters
        ----------
        parent : tk.Widget
            Parent container.
        controller : ScreenManager
            Controller to switch screens.
        pause : bool
            True if this is a pause menu, False if game over menu.
        """
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
        
        title_label = tk.Label(self, text=title, font=("Arial", 28, "bold"), fg="#1E1E2F")
        title_label.pack(pady=40)

        #WHY LAMBDA???????
        btn_play = tk.Button(self, text=play, font=("Arial", 14), width=15,fg="#1E1E2F", command= lambda:controller.show_frame("PlayScreen"))
        btn_play.pack(pady=10)

        btn_quit = tk.Button(self, text="Main Menu", font=("Arial", 14),fg="#1E1E2F", width=15, command=self.quit_to_menu)
        btn_quit.pack(pady=20)

    def quit_to_menu(self):
        """
        Return to the main menu.

        If the menu was a pause menu, trigger game over in the controller.
        """
        if self.pause:
            #see if its paused so that if were quitting to menu it saves and restarts
            self.controller.game_over()
        self.controller.show_frame("MainMenu")
