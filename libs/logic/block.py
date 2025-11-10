"""
block.py
This file contains the class related to the falling blocks, its possible moves and rotations.
1 -> Long piece
2 -> square
3 -> triangle
4 -> s block
5 -> z block
6 -> reverse L block
7 -> L block
"""
import numpy as np
import random as rd
import libs.logic.block_shapes as block_shapes

class Block:
    """
    A class used to represent a falling block
    ...

    Attributes
    ----------
    position : list
        (x,y) position on the grid
    speed : int
        speed of the falling block (should this be here???)
    type : int
        type of the block (1 to 7)
    color : str
        color of the block???? -> to be seen -> possibly on graphics interface
    num_legs : int
        the number of legs the animal has (default 4)

    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes
    """
     
    def __init__(self):
        self.block_type = rd.randint(1,7)
        self.rotation=0
        self.block= block_shapes.block_order[self.block_type-1][self.rotation]*(self.block_type)
        self.position=[0,5] # spawning location

    def update_block_position(self,move_type,move_info,grid):
        # TRASLATION
        if move_type:
            new_pos = self.position + np.array(move_info)
            new_block=self.block
            new_rotation=self.rotation
        # ROTATION
        else:
            new_pos = self.position
            new_rotation = (self.rotation+move_info) % 4
            new_block = block_shapes.block_order[self.block_type-1][self.rotation]*(self.block_type)
        
        if(self.move_validation(grid,new_pos,new_block)):
            self.position=new_pos
            self.rotation=new_rotation
            self.block=new_block

    #pray for my soul, please
    def move_validation(self,grid,position,block):
        max_row = len(grid)
        max_col = len(grid[0])
        size_row = max_row - len(self.block)
        size_col = max_col - len(self.block[0])
        #bounds check
        if(position[0]<0 or position[1]<0 or position[0]>size_row or position[1]>size_col):
            return False
        #MORE VALIDATION COULD GO HERE
        else:
            return True


