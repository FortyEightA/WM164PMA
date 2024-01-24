import tkinter as tk
import util
from tkinter import ttk
from tkinter.messagebox import showinfo
import customtkinter as ctk
import sys

ctk.FontManager.load_font("fonts/PublicSans-Regular.ttf")


class Titles(ctk.CTkFrame):
    def __init__(self, master, titles):
        super().__init__(master, fg_color="transparent")

        self.titles = titles
        self.width = self.master.winfo_screenwidth()

        for i, title in enumerate(self.titles):

            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(i, weight=1)

            self.title = ctk.CTkLabel(
                self,
                text=title,
                width=(int(self.width / len(self.titles)) - 20),
                font=("PublicSans-Regular", 20),
                corner_radius=6)

            self.title.grid(
                column=i,
                row=0,
                padx=10,
                sticky="new")


class Text(ctk.CTkFrame):
    def __init__(self, master, texts):
        super().__init__(master, fg_color="transparent")

        self.texts = texts
        self.width = self.master.winfo_screenwidth()
        self.textboxes = []

        for i, text in enumerate(self.texts):
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(i, weight=1)

            self.textbox = ctk.CTkTextbox(
                self,
                width=(int(self.width / len(self.texts)) - 20),
                font=("PublicSans-Regular", 20),
                activate_scrollbars=False,
                corner_radius=6)
            self.textbox.insert(0.0, text)
            self.textbox.configure(state="disabled")
            self.textbox.grid(
                column=i,
                row=0,
                padx=10,
                sticky="new")
            self.textboxes.append(self.textbox)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure the main window
        self.title('AQM Data Analysis')
        self.attributes("-fullscreen", True)

        self.bind("<Escape>", lambda x: self.destroy())

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.middle_title = Titles(self, ["AQM Data Analysis"])
        self.middle_title.grid(
            row=0,
            column=0,
            padx=10,
            pady=(10, 0),
            sticky="new",
            columnspan=2)

        self.objective_title = Titles(
            self, ["Mean Difference", "3 Point Standard Deviation"])
        self.objective_title.grid(
            row=1,
            column=0,
            padx=10,
            pady=(10, 0),
            columnspan=2,
            sticky="new")

        self.textboxes = Text(
            self,
            [
                "\nHCE Mean: \n\nCNC Mean: \n\nDifference Of Mean: \n",
                "\nLocation of Largest Three Point Standard Deviation: \n\nThree point time window: \n\nLargest Standard Deviation: \n"])
        self.textboxes.grid(
            row=2,
            column=0,
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
