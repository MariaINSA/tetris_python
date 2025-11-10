#import libs.logic.game_logic as logic

"""
All types of movements:
-translation: move in x or y -> this can change in value depending on the move
-rotation: rotate the piece
"""

class KeyBoard:
    """
    A class used to manage keyboard events
    ...

    Attributes
    ----------
    keys : list of movement keys
        (left, right, soft_drop, rot_left, rot_right, double_rut, hard_drop) game keys

    Methods
    -------
    says(sound=None) EXAMPLE METHOD
        Prints the animals name and what sound it makes
    """
     
    def __init__(self,root,block,lgrid,ggrid,keys=("<Left>","<Right>","<Down>","<Up>")):
        self.block=block
        self.lgrid=lgrid
        self.ggrid=ggrid
        root.bind("<Left>", self.move_left) #type 1 move
        root.bind("<Right>", self.move_right) #type 1 move
        root.bind("<Down>", self.soft_drop) #type 1 move -> soft drop
        #root.bind("<Space bar>", self.hard_drop) #type 1 move -> soft drop
        root.bind("<z>", self.rotate_right) #type 2 move
        root.bind("<x>", self.rotate_left) #type 2 move
        root.bind("<c>", self.rotate_180) #type 2 move



    def move_left(self,event):
        self.update_game(True,[0,-1])

    def move_right(self,event):
        self.update_game(True,[0,1])
    
    def soft_drop(self,event):
        self.update_game(True,[1,0])
    
    def rotate_right(self,event):
        self.update_game(False,1)
    
    def rotate_left(self,event):
        self.update_game(False,-1)
    
    def rotate_180(self,event):
        self.update_game(False,2)

    def update_game(self,move_type,move_info):
        """
        Move type goes true for translation and false for rotation
        """
        self.block.update_block_position(move_type,move_info,self.lgrid.grid)
        self.lgrid.update_shadow(self.block)
        self.ggrid.update(self.lgrid)


