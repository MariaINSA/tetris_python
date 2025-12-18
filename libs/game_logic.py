
"""
tetris_logic.py
This file contains the class with the game functioning.
"""

import libs.logic.block as block
import libs.logic.grid as lgrid
import libs.graphics.grid as ggrid
import libs.keyboard_control as kb
import random as rd

# this list is defined by this equation
# (0.8-((level-1)*0.007))^(level-1)
# the eq is in seconds, the list in milis
# why? ask the tetris gods
speeds=(1000,793,618,473,355,262,190,135,94,64,43,28,18,11,7)

class Game_logic:
    def __init__(self, graphic):
        self.play_screen = graphic
        self.grid_logic = graphic.lgrid
        self.graphic = graphic.grid_frame
        self.canvas = self.graphic.canvas

        # blocks
        self.block_list = [1,2,3,4,5,6,7]
        self.next_block_list = [1,2,3,4,5,6,7]

        self.list_position = 0
        self.current_block = self.block_list[self.list_position]
        self.block = block.Block(self.current_block)

        #this is here to prevent name erasing when losing and trying again
        self.name=""

        # get the values to the reset state 
        self.init_game()

    def init_game(self):
        # score & state
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.paused = True #start with paused game
        self.game = 0
        self.btb = False

        rd.shuffle(self.block_list)
        rd.shuffle(self.next_block_list)

        self.list_position = 0
        self.current_block = self.block_list[self.list_position]
        self.block.re_init(self.current_block) #self.block = block.Block(self.current_block)

        # timing & physics
        self.block_delay = 500
        self.locks = 0
        self.block_under = False
        self.under_timer = None

        # hold
        self.hold_state = 0
        self.hold_block = 0

        # falling
        self.falling_speed = speeds[self.level - 1]
        self.soft_drop = False
        self.falling_timer = None
        
    def start_falling_timer(self):
        if self.falling_timer is not None:
            self.canvas.after_cancel(self.falling_timer)
        self.falling_timer = self.canvas.after(self.falling_speed, self.falling_mov)

    def falling_mov(self):
        if self.paused or not self.game:
            return

        # call for the movement of the block (may add an under flag)
        # check if something is under the block
        # if so start stop protocol
        self.update_game(1,[1,0]) #Fall one block

        #Check for a block under
        if(self.block.check_block_under(self.grid_logic.grid)):
            self.block_under=True
            self.under_timer = self.canvas.after(self.block_delay,self.place_block)

        if self.soft_drop:
            self.score+=1
        
        #Restart falling loop
        self.start_falling_timer()
 
    def place_block(self):
        if self.block.check_game_over(self.grid_logic.grid,False):
            self.game_over()

        #restarting timer
        if self.falling_timer is not None:
            self.canvas.after_cancel(self.falling_timer)
            self.falling_timer = None

        self.new_block()
        self.hold_state = False
        self.block_under=False
        self.locks=0
        #Check for clear lines
        lines = self.grid_logic.check_full_lines()
        self.lines_cleared += lines
        self.score += self.get_score(lines)
        self.next_level()

        #show the difference
        self.update_image()

    def new_block(self,hold=False):
        if(hold==False):
            self.grid_logic.update_grid()
        self.list_position=(self.list_position+1)%7
        # reshuffle when restarting the list
        if self.list_position==0:
            self.block_list=self.next_block_list[:]
            rd.shuffle(self.next_block_list)

        self.current_block=self.block_list[self.list_position]
        self.block.re_init(self.current_block)  #block.Block(self.current_block)
        if self.block.check_game_over(self.grid_logic.grid):
            self.game_over()
        self.start_falling_timer()

    def update_game(self,move_type,move_info): ##HAY QUE ORGANIZAR ESTO
        """
        Move type goes 1 for translation and 0 for rotation, 2 for hard drop
        """
        #check for state and if locked on ground and rotating or translating, reset lock delay
        if (move_type!=2 and self.block_under):
            self.canvas.after_cancel(self.under_timer)
            self.block_under=True
            self.locks=self.locks+1

        if self.locks < 15:
            lines_hard_drop=self.block.update_block_position(move_type,move_info,self.grid_logic.grid)
            self.score+=lines_hard_drop*2
        else:
            self.new_block()
            self.block_under=False
            self.locks=0
            self.hold_state=False
            #Check for clear lines
            lines = self.grid_logic.check_full_lines()
            self.lines_cleared += lines
            self.score += self.get_score(lines)
            self.next_level()

        if (self.block.check_block_under==True) and (self.block_under):
            self.under_timer = self.canvas.after(self.block_delay,self.place_block)
        else:
            self.block_under=False

        self.update_image()
        #if i move this, the hardrop doesnt work, yay
        if move_type==2:
            if self.under_timer!=None:
                self.canvas.after_cancel(self.under_timer)
            self.place_block()
        
    def get_score(self,lines):
        scores=(0,100,300,500,800)
        total= scores[lines]*self.level
        if lines ==4: # check for tetris back to back
            if not self.btb:
                self.btb=True
            else:
                total += int(total/2)
        else:
                self.btb=False
        return total
        
    def start_soft_drop(self):
        if not self.soft_drop:
            self.soft_drop=True
            self.falling_speed=int(self.falling_speed/20)
            if self.falling_speed<=0:
                self.falling_speed=1
    
    def end_soft_drop(self):
        self.soft_drop=False
        self.falling_speed=speeds[self.level-1]
        self.start_falling_timer()

    def hold(self):
        if self.hold_state == False : 
            if self.hold_block == 0:
                self.hold_block = self.current_block
                self.new_block(True)
            else:
                self.current_block, self.hold_block = self.hold_block, self.current_block
                #if we have to change the block, pause the under timer if it exists
                if (self.under_timer!=None):
                    self.canvas.after_cancel(self.under_timer)
                self.block_under=False
                self.locks=0
                self.block.re_init(self.current_block) # block.Block(self.current_block)

            self.hold_state  = True
            self.block_under = False
            self.locks = 0
            self.update_image()

    def update_image(self):
        self.grid_logic.update_shadow(self.block)
        self.graphic.update(self.grid_logic)
        self.play_screen.update_next(self.block_list,self.next_block_list,self.list_position)
        self.play_screen.update_hold(self.hold_block)
        self.play_screen.update_text(self.lines_cleared,self.score,self.level,self.name)

    def pause_game(self):
        if not self.paused:
            self.paused=True
            if (self.falling_timer!=None):
                self.canvas.after_cancel(self.falling_timer)
            if (self.under_timer!=None):
                self.canvas.after_cancel(self.under_timer)

            if self.game:
                self.play_screen.open_new_screen("PauseMenu")
            else:
                self.play_screen.open_new_screen("GameOverMenu")
            
        else:
            self.paused=False
            self.start_falling_timer()

    def next_level(self):
        #this is the fixed goal system
        # calculate what the level SHOULD be
        MAX_LEVEL = 15
        new_level = min(self.lines_cleared // 10 + 1, MAX_LEVEL)

        # only update if the level actually increased
        if new_level > self.level:
            self.level = new_level
            self.falling_speed = speeds[self.level - 1]

    def game_over(self):
        self.game=False
        #cancel timers
        self.pause_game()
        self.save_game()

        #re-initialise internal values
        #when we do this we do game=false
        self.init_game()
        # clear grid
        self.grid_logic.delete()
        self.grid_logic.update_grid()
        self.block.re_init(self.current_block)  #block.Block(self.current_block)

        # clear reupdate the graphic part
        self.update_image()

    def start_game(self,name):
        self.game=True
        if name is not None: 
            self.name=name
        self.pause_game()
        self.update_image()

    def save_game(self):
        file = open("scores.txt", "a")  # append mode
        L = self.name+","+str(self.level) +","+str(self.score)+","+str(self.lines_cleared)+"\n"
        file.write(L)
        file.close()