"""
main.py
This file contains the top layer of the game.
"""

import tkinter as tk
import libs.logic.block as block
import libs.logic.grid as lgrid
import libs.graphics.grid as ggrid
import libs.keyboard_control as kb
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Grid")
    root.resizable(False, False)  # fixed size window
    

    #Creating the thingys
    blocky = block.Block()
    grid_new= lgrid.Grid((10,20))    
    graphic=ggrid.Grid(root, grid_new)

    k_events = kb.KeyBoard(root,blocky,grid_new,graphic)

    # Optional: remove window decorations (if you want a purely visual widget)
    # root.overrideredirect(True)

    root.mainloop()

