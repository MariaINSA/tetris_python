import tkinter as tk
from tkinter import messagebox
import libs.game_logic as game_logic
import libs.logic.grid as lgrid
import libs.graphics.grid as ggrid
import libs.graphics.block as block
import libs.keyboard_control as kb

class PlayScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

       # -------------------------
        # LEFT SIDE — HOLD + STATS
        # -------------------------
        left_frame = tk.Frame(self)
        left_frame.grid(row=0, column=0, sticky="ns", padx=10)

        # HOLD section -> SEE IF A CLASS COULD HELP
        tk.Label(left_frame, text="HOLD", font=("Arial", 14, "bold")).pack(pady=(0, 5))
        self.hold_canvas=block.Block(left_frame)
        self.hold_canvas.pack(pady=(0, 20))

        # Score/Stats
        stats_frame = tk.Frame(left_frame)
        stats_frame.pack(pady=10)

        tk.Label(stats_frame, text="Score:", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
        self.score_var = tk.StringVar(value="0")
        tk.Label(stats_frame, textvariable=self.score_var).grid(row=0, column=1, sticky="e")

        tk.Label(stats_frame, text="Lines:", font=("Arial", 12)).grid(row=1, column=0, sticky="w")
        self.lines_var = tk.StringVar(value="0")
        tk.Label(stats_frame, textvariable=self.lines_var).grid(row=1, column=1, sticky="e")

        tk.Label(stats_frame, text="Level:", font=("Arial", 12)).grid(row=2, column=0, sticky="w")
        self.level_var = tk.StringVar(value="1")
        tk.Label(stats_frame, textvariable=self.level_var).grid(row=2, column=1, sticky="e")


        # -------------------------
        # CENTER — GAME GRID
        # -------------------------

        # we shall see
        self.lgrid=lgrid.Grid((10,20))
        self.grid_frame = ggrid.Grid(self,self.lgrid)

        self.grid_frame.grid(row=0, column=1, padx=10)

        # -------------------------
        # RIGHT SIDE — NEXT QUEUE
        # -------------------------
        right_frame = tk.Frame(self)
        right_frame.grid(row=0, column=2, sticky="ns", padx=10)

        tk.Label(right_frame, text="NEXT", font=("Arial", 14, "bold")).pack(pady=(0, 5))

        # Create queue canvases for next pieces (e.g., 5 visible upcoming)
        self.next_canvases = []
        for i in range(5):
            #c = tk.Canvas(right_frame, width=80, height=80, bg="black", highlightthickness=1)
            c=block.Block(right_frame)
            c.update(i)
            c.pack(pady=5)
            self.next_canvases.append(c)

        # Allow expansion
        self.grid_columnconfigure(1, weight=1)
        self.grid_frame.grid_rowconfigure(0, weight=1)

        # Finally, we do the game controller 
        self.game = game_logic.Game_logic(self)

        self.k_events = kb.KeyBoard(controller,self.game)

    def update_hold(self,block):
        if block!=0:
            #CHECK Y I NEED THE -1
            self.hold_canvas.update(block-1)

    def update_next(self,next_list1,next_list2,position):
        position+=1
        for i in range(5):
            # this does not need the -1 because we do not need the current position on display
            if i+position<7:
                self.next_canvases[i].update(next_list1[i+position]-1)
            else:
                self.next_canvases[i].update(next_list2[i+position-7]-1)

    def update_text(self,lines,score,level):
        self.score_var.set(lines)
        self.lines_var.set(score)
        self.level_var.set(level)



