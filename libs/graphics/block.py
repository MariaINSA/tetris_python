#offset between real and grey colours is 7
import tkinter as tk
import libs.logic.block_shapes as shapes

colors = [
            "#7F7F7F","#00FFFF","#0000FF","#FF7F00", 
            "#FFFF00","#00FF00", "#800080","#FF0000"
        ]


class Block(tk.Frame):
    """
        A Tkinter widget that displays a single Tetris piece centered inside a canvas.

        The piece is rendered using a matrix representation and drawn
        with colored rectangles corresponding to occupied cells.
    """

    def __init__(self, parent, canvas_size=80,
                 cell_size=18, padding=2,
                 colors=colors, *args, **kwargs):
        """
        Initialize the Block widget.

        Parameters
        ----------
        parent : tk.Widget
            Parent Tkinter widget.
        canvas_size : int, optional
            Width of the canvas in pixels (default is 80).
        cell_size : int, optional
            Size of each block cell in pixels (default is 18).
        padding : int, optional
            Padding inside each cell to create spacing (default is 2).
        colors : list of str, optional
            List of hexadecimal color strings for blocks.
        """

        super().__init__(parent, *args, **kwargs)

        self.cell_size = cell_size
        self.padding = padding
        self.colors = colors

        self.canvas = tk.Canvas(
            self,
            width=canvas_size,
            height=canvas_size*0.75,
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack()

        self.canvas.configure(takefocus=0)
        self.configure(takefocus=0)

        self.blocks = []

    def clear(self):
        """
        Remove all currently drawn block cells from the canvas.
        """
        for block in self.blocks:
            self.canvas.delete(block)
        self.blocks.clear()

    def update(self, block_number):
        """
        Render a new Tetris piece in the canvas.

        Parameters
        ----------
        block_number : int
            Index of the block shape to display, corresponding to
            the block order and color list.

        Notes
        -----
        The piece is centered in the canvas and only occupied cells
        are drawn.
        """
        self.clear()
        piece=shapes.block_order[block_number][0]

        # Find occupied cells
        cells = []
        for r, row in enumerate(piece):
            for c, val in enumerate(row):
                if val:
                    cells.append((r, c))

        if not cells:
            return

        # Bounding box of the piece
        min_r = min(r for r, _ in cells)
        max_r = max(r for r, _ in cells)
        min_c = min(c for _, c in cells)
        max_c = max(c for _, c in cells)

        piece_w = (max_c - min_c + 1) * self.cell_size
        piece_h = (max_r - min_r + 1) * self.cell_size

        canvas_w = int(self.canvas["width"])
        canvas_h = int(self.canvas["height"])

        offset_x = (canvas_w - piece_w) // 2
        offset_y = (canvas_h - piece_h) // 2

        # Draw only occupied cells
        for r, c in cells:
            x0 = offset_x + (c - min_c) * self.cell_size + self.padding
            y0 = offset_y + (r - min_r) * self.cell_size + self.padding
            x1 = x0 + self.cell_size - self.padding
            y1 = y0 + self.cell_size - self.padding

            rect = self.canvas.create_rectangle(
                x0, y0, x1, y1,
                fill=self.colors[block_number+1],
                outline=""
            )
            self.blocks.append(rect)
