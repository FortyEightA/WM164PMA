import tkinter as tk
import util
from tkinter import ttk
from tkinter.messagebox import showinfo
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('AQM Data Analysis')
        self.attributes("-fullscreen", True)

        self.grid_columnconfigure((0, 1), weight=1)

        self.middle_title = ctk.CTkLabel(
            self,
            text="AQM Data Analysis",
            fg_color="grey40",
            corner_radius=6)
        self.middle_title.grid(
            row=0, column=0, padx=10, pady=(
                10, 0), sticky="ew", columnspan=2)

        self.mean_difference_text = ctk.CTkLabel(
            self, text="Mean Difference", fg_color="transparent", corner_radius=6)
        self.mean_difference_text.grid(
            row=1, column=0, padx=10, pady=(
                10, 0), sticky="ew")

        self.three_point_std_text = ctk.CTkLabel(
            self,
            text="3 Point Standard Deviation",
            fg_color="transparent",
            corner_radius=6)
        self.three_point_std_text.grid(
            row=1, column=1, padx=10, pady=(
                10, 0), sticky="ew")


if __name__ == "__main__":
    app = App()
    app.mainloop()
