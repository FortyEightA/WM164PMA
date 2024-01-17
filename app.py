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
        super().__init__(data)
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

# Decorator to change nan values to 0.


def float_nan_to_zero_decorator(func):
    def wrapper(x, y):
        if math.isnan(x):
            return func(0, y) if not (math.isnan(y)) else func(0, 0)
        elif math.isnan(y):
            return func(x, 0) if not (math.isnan(x)) else func(0, 0)
        else:
            return func(x, y)
    #Polymorphic wrapper ?
    def wrapper(x):
        print(x)
        if math.isnan(x):
            return func(0)
        else:
            return func(x)
    return wrapper

# Decorator to arrange values so that x is always larger than y.


def larger_smaller_decorator(func):
    def wrapper(x, y):
        if x > y:
            return func(x, y)
        else:
            return func(y, x)
    return wrapper

def split_three_point_time(data):
    data_time_values = data.iloc[:, 1:3]
    print(data_time_values)

def deNaN(data):
    data = data.dropna()
    return data


#######################################################################
# Section of code that is used to create graphs from the dataframes.  #
#######################################################################

# Function that takes a dataframe, x and y axis, title, mode, and file#
#name and creates a scatter plot image.
def scatter_plot_to_image(data_frame, x, y, title, mode, file_name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_frame[x], y=data_frame[y], mode=mode))
    fig.update_layout(
        autotypenumbers='convert types',
        title=title,
        title_x=0.5)
    fig.write_image(file_name + ".png")

#######################################################################
# Section of code that is used to find avg difference between values. #
#######################################################################


# Function that takes two dataframes and returns the average difference
# between individual values in the two dataframes.


def avg_differences(first_data, second_data):
    first_data_mean = first_data[['PM1.0']].mean(axis=1)
    second_data_mean = second_data[['PM1.0']].mean(axis=1)
    return first_data_mean - second_data_mean
    # jointArr = pd.concat([first_data_frame, second_data_frame], axis=1).astype(float).to_numpy()

#######################################################################
#                           Main Function                             #
#######################################################################

# Main Function


def main():
    t1 = time.time()
    main_data_frame = pd.read_csv('DTS WM164.csv')
    data_data_frame = main_data_frame.iloc[10:, :]
    data_data_frame.columns = ['Date', 'Time', 'PM1.0', 'Date', 'Time', 'PM1.0']
    hce_data_frame = Data(data_data_frame.iloc[:, 0:3], name='HCE', location='HCE')
    cnc_data_frame = Data(data_data_frame.iloc[:, 3:6], name='CNC', location='CNC')
    # hce_data_frame.display()
    # cnc_data_frame.display()
    # scatter_plot_to_image(
    #     hce_data_frame,
    #     'Time',
    #     'PM1.0',
    #     'HCE PM1.0',
    #     'markers',
    #     'HCE PM1.0')
    print(avg_differences(hce_data_frame, cnc_data_frame))
    # split_three_point_time(hce_data_frame)
    tf = time.time() - t1
    print(tf)


if __name__ == '__main__':
    main()
