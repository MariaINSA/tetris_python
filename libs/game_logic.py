
"""
tetris_logic.py
This file contains the class with the game functioning.
"""

import libs.logic.block as block
import libs.logic.grid as lgrid
import libs.graphics.grid as ggrid
import libs.keyboard_control as kb
import random as rd

class Game_logic:
    def __init__(self,root):
        #create grid
        
        self.grid_logic= lgrid.Grid((10,20))   #obligatory size
        self.graphic=ggrid.Grid(root, self.grid_logic)

        #create block list
        self.block_list=[1,2,3,4,5,6,7]
        rd.shuffle(self.block_list)
        self.list_position=0

        self.current_block=self.block_list[self.list_position]
        self.hold=0 #Block on hold is none

        #create block
        self.block = block.Block(self.current_block)
        self.k_events = kb.KeyBoard(root,self)

        #Time that has to pass on the ground for the block to stick
        self.block_delay=300

        # start falling sequence
        self.falling_speed=600
        self.canvas = self.graphic.canvas
        self.canvas.after(self.falling_speed,self.falling_mov)
        

    def falling_mov(self):
        #call for the movement of the block (may add an under flag)
        #check if something is under the block
        #if so start stop protocol
        self.update_game(True,[1,0]) #Fall one block

        #Check for a block under
        if(self.block.check_block_under(self.grid_logic.grid)):
            print("There is a block under")
            self.new_block()

        #Check for clear lines
        print(self.grid_logic.check_full_lines())
        #Restart falling loop
        self.canvas.after(self.falling_speed, self.falling_mov)

    def new_block(self):
        self.grid_logic.update_grid()
        self.list_position=(self.list_position+1)%7
        if self.list_position==0:
            rd.shuffle(self.block_list)

        self.current_block=self.block_list[self.list_position]
        self.block=block.Block(self.current_block)
        



    def update_game(self,move_type,move_info):
        """
        Move type goes true for translation and false for rotation
        """
        #check for state and if locked on ground and rotating, reset lock delay
        self.block.update_block_position(move_type,move_info,self.grid_logic.grid)
        self.grid_logic.update_shadow(self.block)
        self.graphic.update(self.grid_logic)