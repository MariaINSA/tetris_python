"""
block.py
This file contains the class related to the falling blocks, its possible moves and rotations.
1 -> I piece
2 -> J piece
3 -> L piece
4 -> O piece
5 -> S piece
6 -> T piece
7 -> Z piece
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
     
    def __init__(self, type):
        self.block_type = type
        self.rotation=0
        self.block= block_shapes.block_order[self.block_type-1][self.rotation]*(self.block_type)
        self.position=np.array([0,5]) # spawning location 

    def update_block_position(self,move_type,move_info,grid):
        # TRASLATION
        if move_type:
            new_pos = self.position + np.array(move_info)
            new_block=self.block
            new_rotation=self.rotation
        # ROTATION
        else:
            print("Rotation detected")
            new_pos = self.position
            new_rotation = (self.rotation+move_info) % 4
            new_block = block_shapes.block_order[self.block_type-1][new_rotation]*(self.block_type)
            print(new_block)

        if(self.move_validation(grid,new_pos,new_block)):
            print("Validated 1")
            self.position=new_pos
            self.rotation=new_rotation
            self.block=new_block

        #this part is important because here goes wall kicks
        #...yay
        elif(move_type==False):
            print("Wall kicking! Block:",self.block_type)
            print("Rotation",self.rotation,"to",new_rotation)
            if self.block_type == 1:
                wall_kick_offsets=block_shapes.wall_kicks_I[(self.rotation,new_rotation)]
            else:
                wall_kick_offsets= block_shapes.wall_kicks[(self.rotation,new_rotation)]
            
            for offset in wall_kick_offsets:
                offset_pos = new_pos + np.array(offset)
                print(offset_pos)
                if(self.move_validation(grid,offset_pos,new_block)):
                    print("Validated SRS")
                    self.position = offset_pos
                    self.rotation = new_rotation
                    self.block    = new_block
                    break

    #pray for my soul, please
    def move_validation(self,grid,position,block):
        max_row = len(grid) - 2
        max_col = len(grid[0]) - 2
        #bounds check -> left, right, down
        for r, row in enumerate(block):
            for c, val in enumerate(row):
                if val!=0:
                    #check if out of bounds
                    if(position[0]+r >= max_row or position[1]+c < 2 or position[1]+c >= max_col):
                        print("out of bounds")
                        return False
                    
                    #check if colliding
                    if(grid[position[0]+r][position[1]+c] != 0):
                        print("collision with grid")
                        return False
        return True

                    




