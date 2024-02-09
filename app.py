import tkinter as tk
import inspect
import util
from tkinter import ttk
from tkinter.messagebox import showinfo
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

ctk.FontManager.load_font("fonts/PublicSans-Regular.ttf")


class Titles(ctk.CTkFrame):
    def __init__(self, master, titles, fg_color_input="transparent", font_size=20):
        super().__init__(master, fg_color=fg_color_input)

        self.width_measurement = self.winfo_screenwidth()
        if isinstance(master, tk.Frame):
            self.width_measurement -= 50

# Array for each column
        self.title_arr = [[], [], [], [], [], [], [], []]

        for i, column in enumerate(titles):
            for k, each_title_in_row in enumerate(column):
                self.grid_rowconfigure(k, weight=1)
                self.grid_columnconfigure(i, weight=1)
                self.title = ctk.CTkLabel(
                    self,
                    text=each_title_in_row,
                    width=(int(self.width_measurement / len(titles)) - 20),
                    font=("PublicSans-Regular", font_size),
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
        
        self.width_measurement = self.winfo_width()

        self.height = height

        for i, image in enumerate(self.path_to_images):
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(i, weight=1)

            self.image = ctk.CTkImage(
                light_image=Image.open(path_to_images[i]),
                dark_image=Image.open(path_to_images[i]),
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

class Graph(ctk.CTkFrame):
    def __init__(self, master, graphs, fg_color="transparent"):
        super().__init__(master, fg_color="transparent")

        size_inch= (self.winfo_screenwidth()-50 // len(graphs)) / (192*2)
        self.canvi = []
        for i, graph in enumerate(graphs):
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(i, weight=1)
            graph.set_size_inches(size_inch, size_inch)
            graph.set_dpi(192//2)
            canvas=FigureCanvasTkAgg(graph, master=self)
            canvas.get_tk_widget().grid(row=0, column=i, padx=10, sticky="new")
            toolbar = NavigationToolbar2Tk(canvas, self, pack_toolbar=False)
            toolbar.update()
            toolbar.grid(row=1, column=i, padx=10, sticky="sew")
            canvas.draw()
            canvas.mpl_connect(
                "key_press_event", key_press_handler)

            self.canvi.append(canvas)

    def destroy(self):
        for canvas in self.canvi:
            canvas.get_tk_widget().destroy()
            
class Tab(ctk.CTkTabview):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
    
        self.add("HCE")
        self.add("CNC")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure the main window
        self.title('AQM Data Analysis')
        self.resizable(False, False)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda x: self.quit())

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.middle_title = Titles(self, [["AQM Data Analysis"]], font_size=38)
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
        
        self.graph_title = Titles(self, [["Graphs"]])
        self.graph_title.grid(
            row=3,
            column=0,
            padx=10,
            pady=(10, 0),
            columnspan=2,
            sticky="new")
        
        self.tab = Tab(self, corner_radius=6)
        self.tab.grid(
            row=4,
            column=0,
            padx=20,
            pady=(0, 0),
            columnspan=2,
            sticky="news")

        self.exit_button = ctk.CTkButton(
            self,
            font=("PublicSans-Regular", 20),
            text="Exit",
            corner_radius=6,
            command=self.close)

        self.exit_button.grid(
            row=5,
            column=0,
            padx=20,
            pady=(10, 10),
            sticky="esw",
            columnspan=2)
        
    def close(self):
        self.update()
        self.update_idletasks()
        self.graphs.destroy()
        self.quit()
        self.destroy()
        
    def create_images(self, tab, top_graph_names_to_display, top_graphs, lower_title, lower_graph):
        self.titles = Titles(tab, top_graph_names_to_display)
        self.titles.grid(
            row=0,
            column=0,
            pady=(10, 0),
            columnspan=2,
            sticky="new")
        self.graphs = Graph(tab, top_graphs)
        self.graphs.grid(
            row=1,
            column=0,
            pady=(10, 0),
            columnspan=2,
            sticky="new")
        self.titles_lower = Titles(tab, lower_title)
        self.titles_lower.grid(
            row=2,
            column=0,
            pady=(10, 0),
            columnspan=2,
            sticky="new"
        )
        self.graphs_lower = Graph(tab, lower_graph)
        self.graphs_lower.grid(
            row=3,
            column=0,
            pady=(10, 10),
            columnspan=2,
            sticky="new"
        )
        tab.grid_rowconfigure((1, 3), weight = 1)


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

    HCE_graphs = hce_data_frame.create_graph()
    CNC_graphs = cnc_data_frame.create_graph()
    HCE_tab = app.tab.tab("HCE")
    CNC_tab = app.tab.tab("CNC")
    HCE_top = [HCE_graphs[0], HCE_graphs[2]]
    CNC_top = [CNC_graphs[0], CNC_graphs[2]]
    app.create_images(CNC_tab, [["CNC Scatter Graph"], ["CNC Histogram"]], CNC_top, [["CNC Box Plot"]], [CNC_graphs[1]])
    app.create_images(HCE_tab, [["HCE Scatter Graph"], ["HCE Histogram"]], HCE_top, [["HCE Box Plot"]], [HCE_graphs[1]])
    app.mainloop()
