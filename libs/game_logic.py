
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
    def __init__(self,graphic):
        #create grid
        self.score = 0
        self.lines_cleared = 0
        self.level=0
        self.paused = True

        self.play_screen=graphic
        self.grid_logic = graphic.lgrid #obligatory size
        self.graphic = graphic.grid_frame
        

        #create block list
        self.block_list=[1,2,3,4,5,6,7]
        self.next_block_list=[1,2,3,4,5,6,7]
        rd.shuffle(self.block_list)
        rd.shuffle(self.next_block_list)

        self.list_position=0

        self.current_block=self.block_list[self.list_position]

        #create block
        self.block = block.Block(self.current_block)

        #Time that has to pass on the ground for the block to stick
        self.block_delay=500
        self.locks=0
        self.block_under=False #no block under
        self.under_timer=None

        # hold 
        self.hold_state=0
        self.hold_block=0

        # start falling sequence
        self.falling_speed=600
        self.canvas = self.graphic.canvas
        self.falling_timer = None  #self.canvas.after(self.falling_speed,self.falling_mov)
        
    def falling_mov(self):
        #call for the movement of the block (may add an under flag)
        #check if something is under the block
        #if so start stop protocol
        self.update_game(1,[1,0]) #Fall one block

        #Check for a block under
        if(self.block.check_block_under(self.grid_logic.grid)):
            self.block_under=True
            self.under_timer = self.canvas.after(self.block_delay,self.place_block)
        
        #Restart falling loop
        self.falling_timer=self.canvas.after(self.falling_speed, self.falling_mov)
    
    def place_block(self):
        self.new_block()
        self.hold_state = False
        self.block_under=False
        self.locks=0
        #Check for clear lines
        lines, score = self.grid_logic.check_full_lines()
        self.lines_cleared += lines
        self.score += score
        #show the difference
        self.update_image()

    def new_block(self,hold=False):
        #self.canvas.after_cancel(self.under_timer)
        if(hold==False):
            self.grid_logic.update_grid()
        self.list_position=(self.list_position+1)%7
        # reshuffle when restarting the list
        if self.list_position==0:
            self.block_list=self.next_block_list[:]
            rd.shuffle(self.next_block_list)

        self.current_block=self.block_list[self.list_position]
        self.block=block.Block(self.current_block)
    
    def update_game(self,move_type,move_info): ##HAY QUE ORGANIZAR ESTO
        """
        Move type goes 1 for translation and 0 for rotation, 2 for hard drop
        """

        #check for state and if locked on ground and rotating or translating, reset lock delay
        if (move_type!=2 and self.block_under):
            #print("Lock delay number: ",self.locks)
            self.canvas.after_cancel(self.under_timer)
            self.block_under=True
            self.locks=self.locks+1

        if self.locks < 15:
            self.block.update_block_position(move_type,move_info,self.grid_logic.grid)
        else:
            self.new_block()
            self.block_under=False
            self.locks=0
            #Check for clear lines
            lines, score = self.grid_logic.check_full_lines()
            self.lines_cleared += lines
            self.score += score

        if (self.block.check_block_under==True) and (self.block_under):
            self.under_timer = self.canvas.after(self.block_delay,self.place_block)
        else:
            self.block_under=False

        self.update_image()
        #if i move this, the hardrop doesnt work, yay
        if move_type==2:
            self.place_block()

    def hold(self):
        if self.hold_state == False : 
            if self.hold_block == 0:
                self.hold_block = self.current_block
                self.new_block(True)
            else:
                self.current_block, self.hold_block = self.hold_block, self.current_block
                self.block=block.Block(self.current_block)

            self.hold_state  = True
            self.block_under = False
            self.locks = 0

    def update_image(self):
        self.grid_logic.update_shadow(self.block)
        self.graphic.update(self.grid_logic)
        self.play_screen.update_next(self.block_list,self.next_block_list,self.list_position)
        self.play_screen.update_hold(self.hold_block)
        self.play_screen.update_text(self.lines_cleared,self.score,self.level)

    def pause_game(self):
        if not self.paused:
            print("Game paused!!!!")
            self.paused=True
            if (self.falling_timer!=None):
                self.canvas.after_cancel(self.falling_timer)
            if (self.under_timer!=None):
                self.canvas.after_cancel(self.under_timer)
        else:
            print("Game unpaused!!!!")
            self.paused=False
            self.falling_timer=self.canvas.after(self.falling_speed,self.falling_mov)
