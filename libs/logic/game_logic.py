
"""
tetris_logic.py
This file contains the class with the game functioning.
"""

#class Game_logic:

def place_block(grid,block):
    initial_pos=[0,0]
    initial_pos[0]=block.position[0]
    initial_pos[1]=block.position[1]

    for i in block.block:
        print(i)
        for j in i:
            grid.update_shadow(initial_pos,j)
            initial_pos[1]=initial_pos[1]+1
        initial_pos[1]=block.position[1]
        initial_pos[0]=initial_pos[0]+1

def update_block(move_list):
    pass