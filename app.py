import tkinter as tk
import util
from tkinter import ttk
from tkinter.messagebox import showinfo
import customtkinter as ctk
import sys

ctk.FontManager.load_font("fonts/PublicSans-Regular.ttf")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure the main window
        self.title('AQM Data Analysis')
        self.attributes("-fullscreen", True)

        self.bind("<Escape>", lambda x: self.destroy())
        

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(2, weight = 1)


        self.middle_title = ctk.CTkLabel(
            self,
            text="AQM Data Analysis",
            font=("PublicSans-Regular", 20),
            corner_radius=6)

        self.middle_title.grid(
            row=0,
            column=0,
            padx=10,
            pady=(10, 0),
            sticky="new",
            columnspan=2)

        self.mean_difference_title = ctk.CTkLabel(
            self, 
            text="Mean Difference", 
            font=("PublicSans-Regular", 20),
            corner_radius=6)

        self.mean_difference_title.grid(
            row=1,
            column=0,
            padx=10,
            pady=(10, 0),
            sticky="new")

        self.mean_difference_text = ctk.CTkTextbox(
            self,
            font=("PublicSans-Regular", 20),
            height=183,
            activate_scrollbars=False,
            state="normal",
            corner_radius=6)

        self.mean_difference_text.insert(0.0, "\nHCE Mean: \n\nCNC Mean: \n\nDifference Of Mean: \n")

        self.mean_difference_text.configure(state="disabled")

        self.mean_difference_text.grid(
            row=2,
            column=0,
            padx=10,
            pady=(10, 0),
            sticky="new")

        self.three_point_std_title = ctk.CTkLabel(
            self,
            font=("PublicSans-Regular", 20),
            text="3 Point Standard Deviation",
            corner_radius=6)
        
        self.three_point_std_title.grid(
            row=1,
            column=1,
            padx=10,
            pady=(10, 0),
            sticky="new")

        self.three_point_std_text = ctk.CTkTextbox(
            self,
            font=("PublicSans-Regular", 20),
            height=183,
            state="normal",
            activate_scrollbars=False,
            corner_radius=6)

        self.three_point_std_text.insert(0.0, "\nLocation of Largest Three Point Standard Deviation: \n\nThree point time window: \n\nLargest Standard Deviation: \n")

        self.three_point_std_text.configure(state="disabled")

        self.three_point_std_text.grid(
            row=2,
            column=1,
            padx=10,
            pady=(10, 0),
            sticky="new")

        self.exit_button = ctk.CTkButton(
            self,
            font=("PublicSans-Regular", 20),
            text="Exit",
            corner_radius=6,
            command=self.destroy)

        self.exit_button.grid(
            row=3,
            column=0,
            padx=10,
            pady=(10, 10),
            sticky="esw",
            columnspan=2)

        

if __name__ == "__main__":
    ctk.set_default_color_theme("nord.json")
    app = App()
    app.mainloop()

# nord0 = "#2E3440"
# nord1 = "#3B4252"
# nord2 = "#434C5E"
# nord3 = "#4C566A"
