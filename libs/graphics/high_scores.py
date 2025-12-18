import tkinter as tk
from tkinter import messagebox
import libs.graphics.name_input as name_input
#import csv
from os import path 

class HighScores(tk.Frame):
    """
    Screen displaying the high scores of the Tetris game.
    """
    def __init__(self, parent, controller, csv_file="scores.txt"):
        """
        Initialize the HighScores screen with title, score container,
        and navigation buttons.

        Parameters
        ----------
        parent : tk.Widget
            Parent container.
        controller : ScreenManager
            Controller for changing screens.
        csv_file : str, optional
            File path for saving/loading scores (default is "scores.txt").
        """
        super().__init__(parent)
        self.controller = controller
        self.csv_file = csv_file

        title = tk.Label(self, text="High Scores", font=("Arial", 22, "bold"))
        title.pack(pady=10)

        self.scores_container = tk.Frame(self)
        self.scores_container.pack(fill="both", expand=True)

        btn_main = tk.Button(self, text="Main Menu", font=("Arial", 14), width=15, command=lambda:controller.show_frame("MainMenu"))
        btn_main.pack(pady=10)

        self.load_and_display_scores()

    def display_scores(self, scores):
        """
        Display the given list of scores in a structured grid.

        Parameters
        ----------
        scores : list of dict
            List of scores where each score contains "name", "level", "score", "lines".
        """
        # Clear old widgets
        for widget in self.scores_container.winfo_children():
            widget.destroy()

        headers = ["Rank", "Name", "Level", "Lines", "Score"]

        # Configure columns
        for col in range(len(headers)):
            self.scores_container.columnconfigure(col, weight=1)

        # Header row
        for col, text in enumerate(headers):
            tk.Label(
                self.scores_container,
                text=text,
                font=("Arial", 10, "bold"),
                anchor="center"
            ).grid(row=0, column=col, sticky="nsew", padx=5, pady=5)

        # Data rows
        for row_index, s in enumerate(scores, start=1):
            values = [
                row_index,
                s["name"],
                s["level"],
                s["lines"],
                s["score"]
            ]

            for col, value in enumerate(values):
                tk.Label(
                    self.scores_container,
                    text=value,
                    anchor="center"
                ).grid(row=row_index, column=col, sticky="nsew", padx=5, pady=2)


    def load_and_display_scores(self):
        """
        Read scores from the file, remove duplicates, sort them,
        keep top 10, save back to the file, and display them.
        """

        scores = self.read_scores()
        scores = self.remove_duplicates(scores)
        scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]

        self.save_scores(scores)
        self.display_scores(scores)

    def read_scores(self):
        """
        Read scores from the CSV file.

        Returns
        -------
        list of dict
            List of scores with keys: "name", "level", "score", "lines".
        """
        scores = []

        #checks if there is the file
        if not path.exists(self.csv_file):
            return scores

        with open(self.csv_file, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(",")
                if len(parts) != 4:
                    continue

                name, level, score, lines = parts

                scores.append({
                    "name": name,
                    "level": int(level),
                    "score": int(score),
                    "lines": int(lines)
                })

        return scores

    def remove_duplicates(self, scores):
        """
        Remove duplicate scores from the list.

        Parameters
        ----------
        scores : list of dict
            List of scores to filter.

        Returns
        -------
        list of dict
            Filtered list with unique scores.
        """
        seen = set()
        unique_scores = []

        for s in scores:
            key = (s["name"], s["level"], s["score"], s["lines"])
            if key not in seen:
                seen.add(key)
                unique_scores.append(s)

        return unique_scores

    def save_scores(self, scores):
        """
        Save the provided list of scores to the CSV file.

        Parameters
        ----------
        scores : list of dict
            Scores to save, each containing "name", "level", "score", "lines".
        """
        with open(self.csv_file, "w", encoding="utf-8") as file:
            for s in scores:
                line = f"{s['name']},{s['level']},{s['score']},{s['lines']}\n"
                file.write(line)