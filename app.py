import tkinter as tk
import util
from tkinter import ttk
from tkinter.messagebox import showinfo
from PIL import Image
import customtkinter as ctk
import sys

ctk.FontManager.load_font("fonts/PublicSans-Regular.ttf")


class Titles(ctk.CTkFrame):
    def __init__(self, master, titles):
        super().__init__(master, fg_color="transparent")

        self.titles = titles
        self.width = self.master.winfo_screenwidth()
        self.title_arr = []

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
            self.title_arr.append(self.title)


class Text(ctk.CTkFrame):
    def __init__(self, master, texts):
        super().__init__(master, fg_color="transparent")

        self.texts = texts
        self.width = self.master.winfo_screenwidth()
        self.textboxes = []

        for i, text in enumerate(self.texts):
            self.grid_columnconfigure(i, weight=1)

            self.textbox = ctk.CTkTextbox(
                self,
                width=(int(self.width / len(self.texts)) - 20),
                height=0,
                font=("PublicSans-Regular", 20),
                activate_scrollbars=False,
                corner_radius=6)
            self.textbox.insert(0.0, text, "center")
            self.textbox.configure(state="disabled")
            self.textbox.grid(
                column=i,
                row=0,
                padx=10,
                sticky="new")
            self.textboxes.append(self.textbox)

class Images(ctk.CTkFrame):
    def __init__(self, master, path_to_images, height):
        super().__init__(master, fg_color="transparent")

        self.path_to_images = path_to_images

        self.width = self.master.winfo_screenwidth()
        self.height = height

        for i, image in enumerate(self.path_to_images):
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(i, weight=1)

            self.image = ctk.CTkImage(
                light_image=Image.open(path_to_images[i]),
                dark_image=Image.open(path_to_images[i]),
                size=(int(self.width / len(self.path_to_images))+50, self.height),
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


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure the main window
        self.title('AQM Data Analysis')
        self.attributes("-fullscreen", True)

        self.bind("<Escape>", lambda x: self.destroy())

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(4, weight=1)

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
        for i in range(2): self.objective_title.title_arr[i].configure(fg_color="transparent")

        self.main_text_boxes = Text(
            self,
            [
                "HCE Mean:  \n\nCNC Mean: \n\nDifference Of Mean: ",
                "\nLocation of Largest Three Point Standard Deviation: \n\nThree point time window: \n\nLargest Standard Deviation: "])
        self.main_text_boxes.grid(
            row=2,
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
            row=5,
            column=0,
            padx=10,
            pady=(10, 10),
            sticky="esw",
            columnspan=2)

    def create_images(self, images_to_display, path_to_images, image_height):
        self.image_labels = Titles(self, images_to_display)
        self.image_labels.grid(
            row=3,
            column=0,
            padx=10,
            pady=(10, 0),
            columnspan=2,
            sticky="new")
        for i, imag in enumerate(images_to_display): self.image_labels.title_arr[i].configure(fg_color="transparent")
        self.images = Images(self, path_to_images, image_height)
        self.images.grid(
            row=4,
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

    app.main_text_boxes.textboxes[0].configure(state="normal")
    app.main_text_boxes.textboxes[1].configure(state="normal")
    app.main_text_boxes.textboxes[0].delete(0.0, tk.END)
    app.main_text_boxes.textboxes[1].delete(0.0, tk.END)
    app.main_text_boxes.textboxes[0].insert(0.0, f"HCE Mean: {hce_mean}\n\nCNC Mean: {
        cnc_mean}\n\nDifference Of Mean: {difference_of_mean}")
    app.main_text_boxes.textboxes[1].insert(
        0.0,
        f"Largest Three Point of HCE: {hce_std}\n\nLargest Three Point of CNC: {cnc_std}\n\nLargest Standard Deviation: {largest_std}")

    app.main_text_boxes.textboxes[0].configure(state="disabled")
    app.main_text_boxes.textboxes[1].configure(state="disabled")
    
    hce_data_frame.create_graph()
    cnc_data_frame.create_graph()
    
    images_to_display = ["HCE Scatter Graph", "HCE Box Plot"]
    path_to_images = ["graphs/HCE/HCE Scatter Graph.png","graphs/HCE/HCE Box Plot.png"]
    
    graph_height = 900
    app.create_images(images_to_display, path_to_images, graph_height)
    app.mainloop()
