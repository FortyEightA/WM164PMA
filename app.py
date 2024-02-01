import tkinter as tk
import inspect
import util
from tkinter import ttk
from tkinter.messagebox import showinfo
from PIL import Image
import customtkinter as ctk
import sys

ctk.FontManager.load_font("fonts/PublicSans-Regular.ttf")


class Titles(ctk.CTkFrame):
    def __init__(self, master, titles, fg_color_input="transparent"):
        super().__init__(master, fg_color=fg_color_input)

        self.titles = titles
        if isinstance(master, App):
            self.width = self.winfo_screenwidth()
        elif isinstance(master, ctk.CTkFrame):
            self.width = self.master.cget("width")
            print(self.width)

        self.width = self.cget("width")
# Array for each column
        self.title_arr = [[], [], [], [], [], [], [], []]

        for i, column in enumerate(self.titles):
            for k, each_label_in_row in enumerate(column):
                self.grid_rowconfigure(k, weight=1)
                self.grid_columnconfigure(i, weight=1)
                self.title = ctk.CTkLabel(
                    self,
                    text=each_label_in_row,
                    width=(int(self.width / len(column)) - 20),
                    font=("PublicSans-Regular", 20),
                    corner_radius=6)
                self.title.grid(
                    column=i,
                    row=k,
                    padx=10,
                    sticky="new")
                self.title_arr[i].append(self.title)


class Images(ctk.CTkFrame):
    def __init__(self, master, path_to_images, height):
        super().__init__(master, fg_color="transparent")

        self.path_to_images = path_to_images
        print(isinstance(master, ctk.CTkFrame))

        if isinstance(master, App):
            self.width = self.winfo_screenwidth()
        elif isinstance(master, ctk.CTkFrame):
            self.width = self.master.cget("width")

        self.height = height

        for i, image in enumerate(self.path_to_images):
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(i, weight=1)

            self.image = ctk.CTkImage(
                light_image=Image.open(path_to_images[i]),
                dark_image=Image.open(path_to_images[i]),
                size=(int(self.width / len(self.path_to_images)) - 20, self.height),
            )
            self.image_frame = ctk.CTkLabel(
                self,
                image=self.image,
                text="",
                fg_color="transparent",
                corner_radius=6,
            )
            self.image_frame.grid(
                column=i,
                row=0,
                padx=10,
                sticky="new")

class Tab(ctk.CTkTabview):
    def __init__(self, master):
        super().__init__(master)
    
        self.add("HCE")
        self.add("CNC")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure the main window
        self.title('AQM Data Analysis')
        self.attributes("-fullscreen", True)

        self.bind("<Escape>", lambda x: self.destroy())

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.middle_title = Titles(self, [["AQM Data Analysis"]])
        self.middle_title.grid(
            row=0,
            column=0,
            padx=10,
            pady=(10, 0),
            sticky="new",
            columnspan=2)

        self.objective_title = Titles(
            self, [["Mean Difference"], ["3 Point Standard Deviation"]])
        self.objective_title.grid(
            row=1,
            column=0,
            padx=10,
            pady=(10, 0),
            columnspan=2,
            sticky="new")
        # fg_color_input="#434C5E"

        self.main_text_boxes = Titles(self,
                                      [["HCE Mean:",
                                        "CNC Mean:",
                                        "Difference Of Mean:"],
                                       ["Largest Three Point of HCE:",
                                        "Largest Three Point of CNC:",
                                        "Largest Standard Deviation:"]])
        self.main_text_boxes.grid(
            row=2,
            column=0,
            padx=10,
            pady=(10, 0),
            columnspan=2,
            sticky="new")

        self.tab = Tab(self)
        self.tab.grid_columnconfigure((0, 1), weight=1)
        self.tab.grid(
            row=3,
            column=0,
            padx=10,
            pady=(10, 0),
            columnspan=2,
            sticky="new")

        self.exit_button = ctk.CTkButton(
            self,
            font=("PublicSans-Regular", 20),
            text="Exit",
            corner_radius=6,
            command=self.destroy)

        self.exit_button.grid(
            row=4,
            column=0,
            padx=20,
            pady=(10, 10),
            sticky="esw",
            columnspan=2)

    def create_images(self, tab, images_to_display, path_to_images, image_height):
        self.image_labels = Titles(tab, images_to_display)
        self.image_labels.grid(
            row=0,
            column=0,
            padx=10,
            pady=(10, 0),
            columnspan=2,
            sticky="new")
        self.images = Images(tab, path_to_images, image_height)
        self.images.grid(
            row=1,
            column=0,
            padx=10,
            pady=(10, 0),
            columnspan=2,
            sticky="new")


if __name__ == "__main__":

    ctk.set_default_color_theme("nord.json")
    app = App()

    hce_data_frame, cnc_data_frame = util.read_data()
    hce_mean, cnc_mean, difference_of_mean = util.avg_differences(
        hce_data_frame, cnc_data_frame)

    hce_std = util.split_three_point_time(hce_data_frame)
    cnc_std = util.split_three_point_time(cnc_data_frame)

    largest_std = util.larger_smaller_decorator(
        lambda x, y: x if x > y else y)(
        hce_std, cnc_std)

    app.main_text_boxes.title_arr[0][0].configure(text=f"HCE Mean: {hce_mean}",
                                                  corner_radius=0)
    app.main_text_boxes.title_arr[0][1].configure(text=f"CNC Mean: {cnc_mean}",
                                                  corner_radius=0)
    app.main_text_boxes.title_arr[0][2].configure(
        text=f"Difference Of Mean: {difference_of_mean}",
    corner_radius=0)
    app.main_text_boxes.title_arr[1][0].configure(
        text=f"Largest Three Point of HCE: {hce_std}",
    corner_radius=0)
    app.main_text_boxes.title_arr[1][1].configure(
        text=f"Largest Three Point of CNC: {cnc_std}",
    corner_radius=0)
    app.main_text_boxes.title_arr[1][2].configure(
        text=f"Largest Standard Deviation: {largest_std}",
    corner_radius=0)

    hce_data_frame.create_graph()
    cnc_data_frame.create_graph()
    
    HCE_image_tab = app.tab.tab("HCE")
    CNC_image_tab = app.tab.tab("CNC")

    HCE_images_to_display = [["HCE Scatter Graph"], ["HCE Box Plot"]]
    HCE_path_to_images = [
        "graphs/HCE/HCE Scatter Graph.png",
        "graphs/HCE/HCE Box Plot.png"]
    CNC_images_to_display = [["CNC Scatter Graph"], ["CNC Box Plot"]]
    CNC_path_to_images = [
        "graphs/CNC/CNC Scatter Graph.png",
        "graphs/CNC/CNC Box Plot.png"]

    graph_height = 700
    app.create_images(app.tab, HCE, HCE_images_to_display, HCE_path_to_images, graph_height)
    app.create_images(app.tab, CNC, CNC_images_to_display, CNC_path_to_images, graph_height)
    app.mainloop()
