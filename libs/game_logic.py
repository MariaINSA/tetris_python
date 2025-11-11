
"""
tetris_logic.py
This file contains the class with the game functioning.
"""

import libs.logic.block as block
import libs.logic.grid as lgrid
import libs.graphics.grid as ggrid
import libs.keyboard_control as kb

class Game_logic:
    def __init__(self,root):
        #create grid
        
        blocky = block.Block()
        grid_new= lgrid.Grid((10,20))   #obligatory size
        graphic=ggrid.Grid(root, grid_new)

        k_events = kb.KeyBoard(root,blocky,grid_new,graphic)

        #create block list

        #create block

        # start falling sequence

        pass
    

    def falling_mov():
        #call for the movement of the block (may add an under flag)
        #check if something is under the block
        #if so start stop protocol
        pass







def update_block(move_list):
    pass