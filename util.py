import pandas as pd
import math
import numpy as np
import scipy.stats as stats
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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
        plt.style.use('nord.mplstyle')
        return [scatter_plot(
            self,
            'Time',
            'PM1.0',
        ), box_plot(
            self,
            'PM1.0'),
        bar_plot(self,
                 'PM1.0')]

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

def numeric_decorator_specific(func):
    def wrapper(df, x):
        df[x] = pd.to_numeric(df[x], errors='coerce')
        return func(df, x)
    return wrapper

def numeric_decorator_specific_double(func):
    def wrapper(df, x, y):
        df[y] = pd.to_numeric(df[y], errors='coerce')
        return func(df, x, y)
    return wrapper


#######################################################################
# Section of code that is used to create graphs from the dataframes.  #
#######################################################################

# Function that takes a dataframe, x and y axis, title, mode, and file#
# name and creates a scatter plot image.

@numeric_decorator_specific_double
def scatter_plot(dataframe, x, y):
    fig, ax = plt.subplots()
    ticks = [dataframe[x].iloc[i] for i in range(0, len(dataframe[x]), int(len(dataframe[x])/6))]
    ax.scatter(dataframe[x], dataframe[y], s=1)
    ax.set_xticks(ticks)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(dataframe.get_name() + " Scatter Plot")
    return fig
    
@numeric_decorator_specific
def box_plot(data_frame, y):
    fig, ax = plt.subplots()
    data_frame['PM1.0'] = pd.to_numeric(data_frame['PM1.0'])
    ax = data_frame.boxplot(column=['PM1.0'], return_type='axes', vert=False)
    ax.set_title(data_frame.get_name() + " Box Plot")
    ax.set_xlabel('PM1.0')
    return fig

@numeric_decorator_specific
def bar_plot(data_frame, x):
    fig, ax = plt.subplots()
    ax.hist(data_frame[x], bins=12, edgecolor='black', linewidth=0.5)
    ax.set_title(data_frame.get_name() + " Histogram")
    ax.set_xlabel(x)
    ax.set_ylabel('Frequency')
    return fig


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
