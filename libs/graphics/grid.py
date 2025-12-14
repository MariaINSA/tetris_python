"""
grid.py
This file contains the class related to the graphic grid.
"""
import tkinter as tk

#offset between real and grey colours is 7
colors = [
            "#7F7F7F","#00FFFF","#0000FF","#FF7F00", 
            "#FFFF00","#00FF00", "#800080","#FF0000",
            "#009999", "#000099", "#995200",
            "#999900", "#009900", "#4D004D", "#990000"
        ]

class Grid(tk.Frame):
    def __init__(self, root, lgrid, colors=colors, cell_size=20, padding=2,*args, **kwargs):
        super().__init__(root, *args, **kwargs)

        cols=len(lgrid.shadow_grid[0])-4
        rows=len(lgrid.shadow_grid)-4

        self.colors=colors
        self.rectangles = [[None for _ in range(cols)] for _ in range(rows)]

    
        canvas_width = cols * cell_size + (cols + 1) * padding
        canvas_height = rows * cell_size + (rows + 1) * padding

        self.canvas = tk.Canvas(self,
                       width=canvas_width,
                       height=canvas_height,
                       highlightthickness=0)
        
        self.canvas.pack(padx=10, pady=10)

        for r in range(rows):
            for c in range(cols):
                x0 = padding + c * (cell_size + padding)
                y0 = padding + r * (cell_size + padding)
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                color = colors[int(lgrid.shadow_grid[r+2][c+2])]

                rect_id = self.canvas.create_rectangle(x0, y0, x1, y1,
                                              fill=color,
                                              outline="")
                
                self.rectangles[r][c] = rect_id

                # Disable the canvas item so it does not take events
                #self.canvas.itemconfigure(rect_id, state="disabled")

        # Make sure canvas itself doesn't take keyboard focus
        self.canvas.configure(takefocus=0)
        self.configure(takefocus=0)

        return None
        
    def update(self,lgrid):
        cols=len(lgrid.shadow_grid[0])-4
        rows=len(lgrid.shadow_grid)-4

        for r in range(rows):
            for c in range(cols):
                color = self.colors[lgrid.shadow_grid[r+2][c+2]]
                self.canvas.itemconfig(self.rectangles[r][c], fill=color)
