"""
grid.py
This file contains the class related to the logic grid.
"""

import numpy as np
class Grid:
    """
    Represents the logical Tetris grid.

    This class stores the state of the game board, manages the shadow
    (ghost) piece, detects full lines, and clears them when needed.
    """
     
    def __init__(self, size:list):
        """
        Initialize the logic grid.

        Parameters
        ----------
        size : list
            Grid size as [columns, rows] (playable area).
            Extra borders are added internally.
        """
        self.cols=size[0]+4
        self.rows=size[1]+4
        self.grid = np.zeros((self.rows,self.cols),int)
        self.shadow_grid = np.zeros((self.rows,self.cols),int)

    def update_shadow(self,block):
        """
        Update the shadow grid with the current block and its ghost position.

        Parameters
        ----------
        block : Block
            Current falling block.
        """
        self.shadow_grid=self.grid.copy()
        pos=[0,0]
        pos[0]=block.position[0]
        pos[1]=block.position[1]
        shadow_pos=block.hard_drop(self.grid)

        #Getting the block in the grid
        for r, row in enumerate(block.block):
            for c, val in enumerate(row):
                if val!=0:
                    #shadow block
                    self.shadow_grid[shadow_pos[0]+r][shadow_pos[1]+c]=val+7 #(self.shadow_grid[shadow_pos[0]+r][shadow_pos[1]+c]%7)+val+7

                    #block
                    self.shadow_grid[pos[0]+r][pos[1]+c]=val #(self.shadow_grid[pos[0]+r][pos[1]+c]%7)+val
                
    def update_grid(self):
        """
        Commit the shadow grid into the main grid.
        """
        for r,row in enumerate(self.shadow_grid):
            for c, val in enumerate(row):
                self.grid[r][c]=val

    def check_full_lines(self):
        """
        Detect and clear completed lines.

        Returns
        -------
        int
            Number of cleared lines.
        """
        full_lines=[]
        for r,row in enumerate(self.grid):
            clear=True
            for c, val in enumerate(row[2:-2]):
                if val == 0: #this indicates clear space
                    clear=False
                    break
            if (clear):
                full_lines.append(r)

        if (len(full_lines)!=0):
            self.clear_full_lines(full_lines)
        return len(full_lines)
    
    def clear_full_lines(self,full_lines):
        """
        Remove completed lines and shift the grid downward.

        Parameters
        ----------
        full_lines : list of int
            Indices of rows to clear.
        """
        for r in full_lines:
            # do a round of going down
            while r >= 2:
                self.grid[r]=self.grid[r-1]
                r=r-1
    
    def delete(self):
        """
        Reset the grid to an empty state.
        """
        self.grid = np.zeros((self.rows,self.cols),int)
        self.shadow_grid = np.zeros((self.rows,self.cols),int)