import tkinter as tk
from tkinter import messagebox

class NameDialog(tk.Toplevel):
    """
    Modal dialog for entering the player's name.
    """
    def __init__(self, parent):
        """
        Initialize the name input dialog.

        Parameters
        ----------
        parent : tk.Widget
            Parent window to center the dialog over.
        """
        super().__init__(parent)
        self.title("Enter Name")
        self.resizable(False, False)
        self.result = None

        self.transient(parent)   # Keep on top of parent
        self.grab_set()           # Make modal

        tk.Label(self, text="Enter your name:").pack(padx=10, pady=5)

        self.entry = tk.Entry(self, width=20)
        self.entry.pack(padx=10)
        self.entry.focus()

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="OK", width=8, command=self.validate).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancel", width=8, command=self.cancel).pack(side="right", padx=5)

        self.update_idletasks()      # let Tk calculate size
        self.center_window(parent)  # CENTER HERE

        
        self.bind("<Return>", lambda e: self.validate())
        self.bind("<Escape>", lambda e: self.cancel())

        self.wait_window(self)

    def center_window(self, parent):
        """
        Center the dialog over the parent window.

        Parameters
        ----------
        parent : tk.Widget
            Parent window for positioning.
        """
        self.update_idletasks()

        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()

        win_w = self.winfo_width()
        win_h = self.winfo_height()

        x = parent_x + (parent_w // 2) - (win_w // 2)
        y = parent_y + (parent_h // 2) - (win_h // 2)

        self.geometry(f"{win_w}x{win_h}+{x}+{y}")


    def validate(self):
        """
        Validate the entered name.

        Ensures the name is alphanumeric and between 1 and 7 characters.
        If valid, stores it in `self.result` and closes the dialog.
        """

        name = self.entry.get()

        if not name.isalnum():
            messagebox.showerror("Invalid Name", "Name must be alphanumeric.")
            return

        if len(name) > 7 or len(name) == 0:
            messagebox.showerror("Invalid Name", "Name must be 1 to 7 characters long.")
            return

        self.result = name
        self.destroy()

    def cancel(self):
        """
        Cancel name entry and close the dialog without storing a result.
        """
        self.destroy()
