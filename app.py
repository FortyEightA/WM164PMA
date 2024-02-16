import tkinter as tk
import inspect
import util
from tkinter import ttk
from tkinter.messagebox import showinfo
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

# Loading the font
ctk.FontManager.load_font("fonts/PublicSans-Regular.ttf")

# Titles class to create titles for the application.
class Titles(ctk.CTkFrame):
    """Titles class to create titles for the application.

    Args:
        master (tk.Tk): The master widget of the Frame.
        titles (list): A list of lists containing the titles to be displayed.
        fg_color_input (str, optional): The color of the text. Defaults to "transparent".
        font_size (int, optional): The size of the font. Defaults to 20.
    """
    def __init__(self, master, titles, fg_color_input="transparent", font_size=20):
        super().__init__(master, fg_color=fg_color_input)

        # Getting the width of the screen, used to ensure the titles are the correct size.
        self.width_measurement = self.winfo_screenwidth()
        # If the master is a frame, then the width is reduced by 50., this is to ensure the titles fit a Tab.
        if isinstance(master, tk.Frame):
            self.width_measurement -= 50

        # Creating a list to store the titles. Allows to access the titles later.
        self.title_arr = [[], [], [], [], [], [], [], []]

        # Looping through the titles and creating the titles.
        for i, column in enumerate(titles):
            for k, each_title_in_row in enumerate(column):
                self.grid_rowconfigure(k, weight=1)
                self.grid_columnconfigure(i, weight=1)
                self.title = ctk.CTkLabel(
                    self,
                    text=each_title_in_row,
                    width=(int(self.width_measurement / len(titles)) - 20),
                    font=("PublicSans-Regular", font_size),
                    corner_radius=6,
                )
                self.title.grid(column=i, row=k, padx=10, sticky="new")
                self.title_arr[i].append(self.title)

# Images class to create images for the application.
class Images(ctk.CTkFrame):
    """Images class to create images for the application.

    Args:
        master (tk.Tk): The master widget of the Frame.
        path_to_images (list): A list of paths to the images to be displayed.
        height (int): The height of the images.
    """
    def __init__(self, master, path_to_images, height):
        super().__init__(master, fg_color="transparent")

        self.width_measurement = self.winfo_width()

        # Looping through the images and creating the images.
        for i, image in enumerate(path_to_images):
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
            self.image_frame.grid(column=i, row=0, padx=10, sticky="new")

# Graph class to create graphs for the application.
class Graph(ctk.CTkFrame):
    """Graph class to create graphs for the application.

    Args:
        master (tk.Tk): The master widget of the Frame.
        graphs (list): A list of matplotlib figures to be displayed.
        fg_color (str, optional): The color of the text. Defaults to "transparent".
    """
    def __init__(self, master, graphs, fg_color="transparent"):
        super().__init__(master, fg_color="transparent")

        # Getting the width of the screen, used to ensure the graphs are the correct size.
        # Matplotlib figures use inches to measure size, so the width is divided by the number of graphs.
        # The width is then divided by 192, as 192 is the dpi of the figures.
        size_inch = (self.winfo_screenwidth() - 50 // len(graphs)) / (192 * 2)
        
        # Creating a list to store the canvases. Allows to access the canvases later.
        self.canvi = []
        
        # Looping through the graphs and creating the graphs.
        for i, graph in enumerate(graphs):
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(i, weight=1)
            graph.set_size_inches(size_inch, size_inch)
            
            # Lowers the DPI of the graph to 96, as this helps with smaller screens.
            graph.set_dpi(192 // 2)
            canvas = FigureCanvasTkAgg(graph, master=self)
            canvas.get_tk_widget().grid(row=0, column=i, padx=10, sticky="new")
            
            # Adds a toolbar to the graph, allowing the user to interact with the graph.
            toolbar = NavigationToolbar2Tk(canvas, self, pack_toolbar=False)
            toolbar.update()
            toolbar.grid(row=1, column=i, padx=10, sticky="sew")
            canvas.draw()
            
            # Adds a key press handler to the graph, allowing the user to interact with the graph, using a keyboard.
            canvas.mpl_connect("key_press_event", key_press_handler)

            self.canvi.append(canvas)

    # Destroys the canvases, allowing the application to be closed.
    def destroy(self):
        for canvas in self.canvi:
            canvas.get_tk_widget().destroy()

# Tab class to create tabs for the application.
class Tab(ctk.CTkTabview):
    """Tab class to create tabs for the application.

    Args:
        master (tk.Tk): The master widget of the Frame.
        tabs (list): A list of tabs to be created.
    """
    
    def __init__(self, master, tabs, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        for i, tab in enumerate(tabs):
            self.add(tab)

# Main app class
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AQM Data Analysis")
        self.resizable(False, False)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda x: self.quit())

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.middle_title = Titles(self, [["AQM Data Analysis"]], font_size=38)
        self.middle_title.grid(
            row=0, column=0, padx=10, pady=(10, 0), sticky="new", columnspan=2
        )

        self.objective_title = Titles(
            self, [["Mean Difference"], ["3 Point Standard Deviation"]]
        )
        self.objective_title.grid(
            row=1, column=0, padx=10, pady=(10, 0), columnspan=2, sticky="new"
        )

        self.main_text_boxes = Titles(
            self,
            [
                ["HCE Mean:", "CNC Mean:", "Difference Of Mean:"],
                [
                    "Largest Three Point of HCE:",
                    "Largest Three Point of CNC:",
                    "Largest Standard Deviation:",
                ],
            ],
        )
        self.main_text_boxes.grid(
            row=2, column=0, padx=10, pady=(10, 0), columnspan=2, sticky="new"
        )

        self.graph_title = Titles(self, [["Graphs"]])
        self.graph_title.grid(
            row=3, column=0, padx=10, pady=(10, 0), columnspan=2, sticky="new"
        )

        self.tab = Tab(self, ["HCE", "CNC"], corner_radius=6)
        self.tab.grid(
            row=4, column=0, padx=20, pady=(0, 0), columnspan=2, sticky="news"
        )

        self.exit_button = ctk.CTkButton(
            self,
            font=("PublicSans-Regular", 20),
            text="Exit",
            corner_radius=6,
            command=self.close,
        )

        self.exit_button.grid(
            row=5, column=0, padx=20, pady=(10, 10), sticky="esw", columnspan=2
        )

    # Method to close all the canvases, allowing the application to be closed.
    def close(self):
        self.update()
        self.update_idletasks()
        self.graphs.destroy()
        self.quit()
        self.destroy()

    # 
    def create_graphs_in_tab(
        self, tab, top_graph_names_to_display, top_graphs, lower_title, lower_graph
    ):
        """Creates the graphs in the tab.

        Args:
            tab (tk.Tk): The tab to create the graphs in.
            top_graph_names_to_display (list): The names of the top graphs to display.
            top_graphs (list): The top graphs to display.
            lower_title (list): The title of the lower graph to display.
            lower_graph (list): The lower graph to display.
        """
        
        self.titles = Titles(tab, top_graph_names_to_display)
        self.titles.grid(row=0, column=0, pady=(10, 0), columnspan=2, sticky="new")

        self.graphs = Graph(tab, top_graphs)
        self.graphs.grid(row=1, column=0, pady=(10, 0), columnspan=2, sticky="new")

        self.titles_lower = Titles(tab, lower_title)
        self.titles_lower.grid(
            row=2, column=0, pady=(10, 0), columnspan=2, sticky="new"
        )

        self.graphs_lower = Graph(tab, lower_graph)
        self.graphs_lower.grid(
            row=3, column=0, pady=(10, 10), columnspan=2, sticky="new"
        )

        tab.grid_rowconfigure((1, 3), weight=1)


if __name__ == "__main__":

    # Setting the default color theme to nord.json
    ctk.set_default_color_theme("themes/nord.json")
    
    # Creating the app
    app = App()

    # Reading the data
    hce_data_frame, cnc_data_frame = util.read_data()
    
    # Getting the mean difference and the 3 point standard deviation
    hce_mean, cnc_mean, difference_of_mean = util.avg_differences(
        hce_data_frame, cnc_data_frame
    )

    hce_std, hce_std_3pt = util.split_three_point_time(hce_data_frame)
    cnc_std, cnc_std_3pt = util.split_three_point_time(cnc_data_frame)

    largest_std = util.larger_smaller_decorator(lambda x, y: x if x > y else y)(
        hce_std, cnc_std
    )

    if largest_std == hce_std:
        largest_3pt = hce_std_3pt
        largest_location = "Henry Church Of England"
        largest_df = hce_data_frame
    else:
        largest_location = "Cardinal Newman Catholic School"
        largest_df = cnc_data_frame
        largest_3pt = cnc_std_3pt

    # Displaying the data
    app.main_text_boxes.title_arr[0][0].configure(
        text=f"HCE Mean: {hce_mean}", corner_radius=0
    )
    app.main_text_boxes.title_arr[0][1].configure(
        text=f"CNC Mean: {cnc_mean}", corner_radius=0
    )

    app.main_text_boxes.title_arr[0][2].configure(
        text=f"Difference Of Mean: {difference_of_mean}", corner_radius=0
    )

    app.main_text_boxes.title_arr[1][0].configure(
        text=f"Location Of Largest Standard Deviation: {largest_location}",
        corner_radius=0,
    )

    app.main_text_boxes.title_arr[1][1].configure(
        text=f"Time of Largest 3pt Window STD: {largest_df["Time"].iloc[largest_3pt[0]]}, {
        largest_df["Time"].iloc[largest_3pt[1]]}, {largest_df["Time"].iloc[largest_3pt[2]]}",
        corner_radius=0
    )

    app.main_text_boxes.title_arr[1][2].configure(
        text=f"Largest Standard Deviation: {largest_std}", corner_radius=0
    )

    # Creating the graphs
    HCE_graphs = hce_data_frame.create_graph()
    CNC_graphs = cnc_data_frame.create_graph()
    HCE_tab = app.tab.tab("HCE")
    CNC_tab = app.tab.tab("CNC")
    HCE_top = [HCE_graphs[0], HCE_graphs[2]]
    CNC_top = [CNC_graphs[0], CNC_graphs[2]]

    # Creating the graphs in the tab
    app.create_graphs_in_tab(
        CNC_tab,
        [["CNC Scatter Graph"], ["CNC Histogram"]],
        CNC_top,
        [["CNC Box Plot"]],
        [CNC_graphs[1]],
    )

    app.create_graphs_in_tab(
        HCE_tab,
        [["HCE Scatter Graph"], ["HCE Histogram"]],
        HCE_top,
        [["HCE Box Plot"]],
        [HCE_graphs[1]],
    )

    app.mainloop()
