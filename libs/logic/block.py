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
    Represents a falling Tetris block and handles its movement,
    rotation, collision detection, and validation.

    The block uses matrix representations defined in block_shapes
    and follows the Super Rotation System (SRS) with wall kicks.
    """

     
    def __init__(self, type):
        """
        Create a new block of a given type.

        Parameters
        ----------
        type : int
            Block type (1 to 7 corresponding to I, J, L, O, S, T, Z).
        """
        self.re_init(type)

    def re_init(self, type):
        """
        Reinitialize the block with a new type.

        Parameters
        ----------
        type : int
            New block type (1 to 7).
        """
        self.block_type = type
        self.rotation=0
        self.block= block_shapes.block_order[self.block_type-1][self.rotation]*(self.block_type)
        self.position=np.array([0,5]) # spawning location

    def update_block_position(self,move_type,move_info,grid):
        """
        Update the block position based on movement type.

        Parameters
        ----------
        move_type : int
            Movement type (1 = translation, 0 = rotation, 2 = hard drop).
        move_info : list or int
            Movement or rotation information.
        grid : list of lists
            Current logic grid.

        Returns
        -------
        int
            Number of lines dropped during a hard drop.
        """
        # TRASLATION
        lines_dropped=0
        if move_type==1:
            new_pos = self.position + np.array(move_info)
            new_block = self.block
            new_rotation = self.rotation
        # ROTATION
        elif move_type==0:
            new_pos = self.position
            new_rotation = (self.rotation+move_info) % 4
            new_block = block_shapes.block_order[self.block_type-1][new_rotation]*(self.block_type)
        # HARD DROP
        elif move_type==2:
            new_pos=self.hard_drop(grid)
            lines_dropped=new_pos[0]-self.position[0]
            new_block=self.block
            new_rotation=self.rotation

        if(self.move_validation(grid,new_pos,new_block)):
            self.position=new_pos
            self.rotation=new_rotation
            self.block=new_block
        #this part is important because here goes wall kicks
        #...yay
        elif(move_type==0):
            if self.block_type == 1:
                wall_kick_offsets=block_shapes.wall_kicks_I[(self.rotation,new_rotation)]
            else:
                wall_kick_offsets= block_shapes.wall_kicks[(self.rotation,new_rotation)]
            
            for offset in wall_kick_offsets:
                offset_pos = new_pos + np.array(offset)
                if(self.move_validation(grid,offset_pos,new_block)):
                    #print("Validated SRS")
                    self.position = offset_pos
                    self.rotation = new_rotation
                    self.block    = new_block
                    break

        return lines_dropped

    #lower block till there is nothing left
    #returns down movement or position, we shall see
    def hard_drop(self,grid):
        """
        Instantly drop the block to the lowest valid position.

        Parameters
        ----------
        grid : list of lists
            Current logic grid.

        Returns
        -------
        list
            Final [row, column] position of the block.
        """
        current_pos=[0,0]
        test_pos=[0,0]
        current_pos[0],current_pos[1]=self.position[0],self.position[1]
        test_pos[0],test_pos[1]=self.position[0],self.position[1]
        
        while(self.move_validation(grid,test_pos,self.block)):
            current_pos[0],current_pos[1]=test_pos[0],test_pos[1]
            test_pos[0]=test_pos[0]+1
        return current_pos

    #pray for my soul, please
    def move_validation(self,grid,position,block):
        """
        Check if a block configuration is valid at a given position.

        Parameters
        ----------
        grid : list of lists
            Logic grid.
        position : array-like
            Proposed block position.
        block : array-like
            Block matrix.

        Returns
        -------
        bool
            True if the move is valid, False otherwise.
        """
        max_row = len(grid) - 2
        max_col = len(grid[0]) - 2
        #bounds check -> left, right, down
        for r, row in enumerate(block):
            for c, val in enumerate(row):
                if val!=0:
                    #check if out of bounds
                    if(position[0]+r >= max_row or position[1]+c < 2 or position[1]+c >= max_col):
                        return False
                    
                    #check if colliding
                    if(grid[position[0]+r][position[1]+c] != 0):
                        return False
        return True
    
    def check_game_over(self,grid,start=True):
        """
        Determine whether the game is over due to block placement.

        Parameters
        ----------
        grid : list of lists
            Logic grid.
        start : bool, optional
            Indicates whether the check is during spawning.

        Returns
        -------
        bool
            True if the game is over.
        """
        #check if there is anything in the same place that it is
        #(this is just for the "init")
        #check if is is blocked fully over the skyline
        in_bounds=False

        for r, row in enumerate(self.block):
            for c, val in enumerate(row):
                if val!=0:
                    #check if colliding on init
                    if(grid[self.position[0]+r][self.position[1]+c] != 0):
                        return True

                    if self.position[0]+r >= 2:
                        in_bounds = True
        
        if not in_bounds and not start:
            return True
        
        return False

    def check_block_under(self, grid):
        """
        Check whether there is a block or boundary directly under
        the current block.

        Parameters
        ----------
        grid : list of lists
            Logic grid.

        Returns
        -------
        bool
            True if the block cannot fall further.
        """

        max_row = len(grid) - 2
        #We have to check all cells
        for r, row in enumerate(self.block):
            for c, val in enumerate(row):
                if val!=0:
                    #check if in lastline
                    if(self.position[0]+r+1 >= max_row ):
                        return True

                    #check if there is something under
                    if(grid[self.position[0]+r+1][self.position[1]+c] != 0):
                        return True
        return False
