import pandas as pd
import math
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats
import kaleido
import time


class Data(pd.DataFrame):
    def __init__(self, data, name, location):
        super().__init__(data.dropna())
        self._name = name
        self._location = location

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_location(self):
        return self._location

    def set_location(self, location):
        self._location = location

    def display(self):
        print(self.get_name())
        print(self.get_location())
        print(self.head())

    def create_graph(self):
        scatter_plot_to_image(
            self,
            'Time',
            'PM1.0',
            self.get_name(),
            'markers',
            self.get_name()
        )
        box_plot_to_image(
            self,
            'PM1.0',
            self.get_name(),
            self.get_name()
        )


# Decorator to change nan values to 0.
# Used previously to change nan values to 0, but now preceded with .dropna()

# def float_nan_to_zero_decorator(func):
#     def wrapper(x, y):
#         if math.isnan(x):
#             return func(0, y) if not (math.isnan(y)) else func(0, 0)
#         elif math.isnan(y):
#             return func(x, 0) if not (math.isnan(x)) else func(0, 0)
#         else:
#             return func(x, y)
#     # Polymorphic wrapper ?
#
#     def wrapper(x):
#         print(x)
#         if math.isnan(x):
#             return func(0)
#         else:
#             return func(x)
#     return wrapper
#
# Decorator to arrange values so that x is always larger than y.


def larger_smaller_decorator(func):
    def wrapper(x, y):
        if x > y:
            return func(x, y)
        else:
            return func(y, x)
    return wrapper

# Decorator to change values to numeric in dataframe.


def numeric_decorator_single(func):
    def wrapper(x):
        return func(pd.to_numeric(x['PM1.0'], errors='coerce'))
    return wrapper


def numeric_decorator_double(func):
    def wrapper(x, y):
        return func(
            pd.to_numeric(
                x['PM1.0'], errors='coerce'), pd.to_numeric(
                y['PM1.0'], errors='coerce'))
    return wrapper




#######################################################################
# Section of code that is used to create graphs from the dataframes.  #
#######################################################################

# Function that takes a dataframe, x and y axis, title, mode, and file#
# name and creates a scatter plot image.


def scatter_plot_to_image(data_frame, x, y, title, mode, file_name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_frame[x], y=data_frame[y], mode=mode))
    fig.update_layout(
        autotypenumbers='convert types',
        title=title,
        title_x=0.5)
    fig.write_image(
        "graphs/" +
        file_name +
        "/" +
        file_name +
        " Scatter Graph.png")


def box_plot_to_image(data_frame, y, title, file_name):
    fig = px.box(data_frame, y=data_frame[y], title=title)
    fig.update_layout(
        autotypenumbers='convert types',
        title=title,
        title_x=0.5
    )
    fig.write_image("graphs/" + file_name + "/" + file_name + " Box Plot.png")
#######################################################################
# Section of code that is used to find avg difference between values. #
#######################################################################


# Function that takes two dataframes and returns the average difference
# between individual values in the two dataframes.

@numeric_decorator_double
def avg_differences(first_data_frame, second_data_frame):
    first_mean = first_data_frame.mean()
    second_mean = second_data_frame.mean()
    return_value = larger_smaller_decorator(lambda x, y: x - y)
    return first_mean, second_mean, return_value(first_mean, second_mean)

@numeric_decorator_single
def split_three_point_time(data):
    index = len(data.index)
    largest_std = 0
    for i in range(0, index, 1):
        three_point_df = data.iloc[i:i + 3]
        three_point_std = three_point_df.std(
            skipna=True)
        if three_point_std > largest_std:
            largest_std = three_point_std
            largest_std_index = i
    return largest_std

#######################################################################
#                           Main Function                             #
#######################################################################

# Main Function


def read_data():
    main_data_frame = pd.read_csv('DTS WM164.csv')
    data_data_frame = main_data_frame.iloc[8:, :]
    data_data_frame.columns = [
        'Date',
        'Time',
        'PM1.0',
        'Date',
        'Time',
        'PM1.0']
    hce_data_frame = Data(
        data_data_frame.iloc[:, 0:3], name='HCE', location='HCE')
    cnc_data_frame = Data(
        data_data_frame.iloc[:, 3:6], name='CNC', location='CNC')
    return hce_data_frame, cnc_data_frame

# def main():
#     t1 = time.time()
#     main_data_frame = pd.read_csv('DTS WM164.csv')
#     data_data_frame = main_data_frame.iloc[8:, :]
#     data_data_frame.columns = [
#         'Date',
#         'Time',
#         'PM1.0',
#         'Date',
#         'Time',
#         'PM1.0']
#     hce_data_frame = Data(
#         data_data_frame.iloc[:, 0:3], name='HCE', location='HCE')
#     cnc_data_frame = Data(
#         data_data_frame.iloc[:, 3:6], name='CNC', location='CNC')
#     print(avg_differences(hce_data_frame, cnc_data_frame))
#     print(split_three_point_time(hce_data_frame))
#     tf = time.time() - t1
#     print(tf)
#
#
# if __name__ == '__main__':
#     main()
