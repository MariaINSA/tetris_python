import tkinter as tk
from tkinter import font as tkfont  # python 3
import libs.graphics.main_menu as main_menu

class ScreenManager(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs) #this means self = root

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        # --- Ventana principal ---

        self.geometry("300x400")
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # creating frames (we shall see)
        self.frames = {}

        self.frames["MainMenu"] = main_menu.MainMenu(parent=container, controller=self)
        #self.frames["PageOne"] = PageOne(parent=container, controller=self)
        #self.frames["PageTwo"] = PageTwo(parent=container, controller=self)

        self.frames["MainMenu"].grid(row=0, column=0, sticky="nsew")
        #self.frames["PageOne"].grid(row=0, column=0, sticky="nsew")
        #self.frames["PageTwo"].grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        #We just raise frames one over the other
        frame.tkraise()