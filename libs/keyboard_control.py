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
     
    def __init__(self,root,game,keys=("<Left>","<Right>","<Down>","<Up>")):
        self.game=game
        self.paused=game.paused
        root.bind("<Left>", self.move_left) #type 1 move
        root.bind("<Right>", self.move_right) #type 1 move
        root.bind("<Down>", self.soft_drop) #type 1 move -> soft drop
        root.bind("<space>", self.hard_drop) #type 1 move -> hard drop (CHECK)
        root.bind("<z>", self.rotate_right) #type 2 move
        root.bind("<x>", self.rotate_left) #type 2 move
        root.bind("<c>", self.hold_block) #especial move -> has his own function
        root.bind("<Return>", self.pause_game) #especial move -> has his own function

    def move_left(self,event):
        self.paused=self.game.paused
        if not self.paused:
            self.game.update_game(1,[0,-1])

    def move_right(self,event):
        self.paused=self.game.paused
        if not self.paused:
            self.game.update_game(1,[0,1])
    
    def soft_drop(self,event):
        self.paused=self.game.paused
        if not self.paused:
            self.game.update_game(1,[1,0])

    def hard_drop(self,event):
        self.paused=self.game.paused
        if not self.paused:
            self.game.update_game(2,None)

    def rotate_right(self,event):
        self.paused=self.game.paused
        if not self.paused:
            self.game.update_game(0,1)
    
    def rotate_left(self,event):
        self.paused=self.game.paused
        if not self.paused:
            self.game.update_game(0,-1)

    def hold_block(self,event):
        self.paused=self.game.paused
        if not self.paused:
            self.game.hold()

    ## Aqui hay un problema!!!!!
    def pause_game(self,event):
        self.paused=not self.game.paused
        self.game.pause_game()


