"""
grid.py
This file contains the class related to the logic grid.
"""
import numpy as np
class Grid:
    """
    A class used to represent a falling block
    ...

    Attributes
    ----------
    grid : basic python matrix
        (x,y) position on the grid
    cols : int
        number of columns
    rows : int
        number of rows

    Methods
    -------
    update(place:list, type:int)
        Updates one place in the grid
    """
     
    def __init__(self, size:list):
        self.cols=size[0]+4
        self.rows=size[1]+4
        self.grid = np.zeros((self.rows,self.cols),int)
        self.shadow_grid = np.zeros((self.rows,self.cols),int)

    def update_shadow(self,block):
        self.shadow_grid=self.grid.copy()
        pos=[0,0]
        pos[0]=block.position[0]
        pos[1]=block.position[1]
        for r, row in enumerate(block.block):
            for c, val in enumerate(row):
                self.shadow_grid[pos[0]+r][pos[1]+c]=self.shadow_grid[pos[0]+r][pos[1]+c]+val
       
    #def update(self,place:list, type:int):
    #    self.grid[place[0]][place[1]]=type

    def update_grid(self):
        for r,row in enumerate(self.shadow_grid):
            for c, val in enumerate(row):
                self.grid[r][c]=val

    def check_full_lines(self):
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
        return len(full_lines)*100
    
    def clear_full_lines(self,full_lines):
        for r in full_lines:
            # do a round of going down
            while r >= 2:
                self.grid[r]=self.grid[r-1]
                r=r-1
    
    def delete(self):
        self.grid= [[0 for _ in range(self.cols)] for _ in range(self.rows)]
