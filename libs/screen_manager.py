import tkinter as tk
from tkinter import font as tkfont  # python 3
import libs.graphics.main_menu as main_menu
import libs.graphics.play_screen as play_screen
import libs.graphics.middle_menu as middle_menu
import libs.graphics.high_scores as high_scores

import libs.graphics.grid as ggrid
import libs.logic.grid as lgrid

class ScreenManager(tk.Tk):
    """
    Main application window and screen controller.

    This class manages all application screens (menus, game screen,
    pause menu, high scores) and handles navigation between them.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the main application window and all screens.
        """
        
        tk.Tk.__init__(self, *args, **kwargs) #this means self = root

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        # --- Ventana principal ---

        self.geometry("500x465")
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # creating frames (we shall see)
        self.frames = {}

        self.frames["MainMenu"] = main_menu.MainMenu(parent=container, controller=self)
        self.frames["PlayScreen"] = play_screen.PlayScreen(parent=container, controller=self)
        self.frames["PauseMenu"] = middle_menu.MiddleMenu(parent=container, controller=self,pause=True)
        self.frames["GameOverMenu"] = middle_menu.MiddleMenu(parent=container, controller=self,pause=False)
        self.frames["HighScores"] = high_scores.HighScores(parent=container, controller=self)

        self.frames["MainMenu"].grid(row=0, column=0, sticky="nsew")
        self.frames["PlayScreen"].grid(row=0, column=0, sticky="nsew")
        self.frames["PauseMenu"].grid(row=0, column=0, sticky="nsew")
        self.frames["GameOverMenu"].grid(row=0, column=0, sticky="nsew")
        self.frames["HighScores"].grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")
    
    def game_over(self):
        """
        Trigger a game over from external screens (e.g. pause menu).
        """
        #intermediary function for calling game over from the pause menu
        self.frames["PlayScreen"].game_over_int()

    def show_frame(self, page_name,name=None):
        """
        Display the selected screen and perform required setup.

        Parameters
        ----------
        page_name : str
            Name of the screen to display.
        name : str, optional
            Player name, used when starting a new game.
        """
        frame = self.frames[page_name]
        #We just raise frames one over the other
        if page_name=="PlayScreen":
            self.frames[page_name].game.start_game(name)
        if page_name=="HighScores":
            self.frames[page_name].load_and_display_scores()
        frame.tkraise()