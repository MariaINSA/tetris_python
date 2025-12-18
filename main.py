"""
main.py
This file contains the top layer of the game.
"""

import tkinter as tk
import libs.screen_manager as screen_manager
import libs.game_logic as game_logic

if __name__ == "__main__":
    root = screen_manager.ScreenManager()
    root.mainloop()