import pandas as pd
import math
import numpy as np
import scipy.stats as stats
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Data class to store dataframes and their names and locations.
class Data(pd.DataFrame):
    """Data class to store dataframes and their names and locations.

    Args:
        data (pd.DataFrame): The dataframe to be stored.
        name (str): The name of the dataframe.
        location (str): The location of the dataframe.
    """
    def __init__(self, data, name, location):
        super().__init__(data.dropna())
        self._name = name
        self._location = location

    # Getters and setters for the name and location of the dataframe. 
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

    # Method to create a graphs from the dataframe.
    def create_graph(self):
        plt.style.use("themes/nord.mplstyle")
        return [
            scatter_plot(
                self,
                "Time",
                "PM1.0",
            ),
            box_plot(self, "PM1.0"),
            bar_plot(self, "PM1.0"),
        ]


# Decorator to arrange values so that x is always larger than y.

def larger_smaller_decorator(func):
    def wrapper(x, y):
        if x > y:
            return func(x, y)
        else:
            return func(y, x)

    return wrapper


# Decorators to change values to numeric in dataframe.

def numeric_decorator_single(func):
    def wrapper(x):
        return func(pd.to_numeric(x["PM1.0"], errors="coerce"))

    return wrapper


def numeric_decorator_double(func):
    def wrapper(x, y):
        return func(
            pd.to_numeric(x["PM1.0"], errors="coerce"),
            pd.to_numeric(y["PM1.0"], errors="coerce"),
        )

    return wrapper


def numeric_decorator_specific(func):
    def wrapper(df, x):
        df[x] = pd.to_numeric(df[x], errors="coerce")
        return func(df, x)

    return wrapper


def numeric_decorator_specific_double(func):
    def wrapper(df, x, y):
        df[y] = pd.to_numeric(df[y], errors="coerce")
        return func(df, x, y)

    return wrapper


@numeric_decorator_specific_double
def scatter_plot(dataframe, x, y):
    """Create a scatter plot from a dataframe.

    Args:
        dataframe (pd.DataFrame): The dataframe to be used.
        x (str): The x axis of the scatter plot.
        y (str): The y axis of the scatter plot.

    Returns:
        fig: The scatter plot.
    """
    fig, ax = plt.subplots()
    ticks = [
        dataframe[x].iloc[i]
        for i in range(0, len(dataframe[x]), int(len(dataframe[x]) / 6))
    ]
    ax.scatter(dataframe[x], dataframe[y], s=1)
    ax.set_xticks(ticks)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(dataframe.get_name() + " Scatter Plot")
    return fig


@numeric_decorator_specific
def box_plot(data_frame, y):
    """Create a box plot from a dataframe.

    Args:
        data_frame (pd.DataFrame): The dataframe to be used.
        y (str): The y axis of the box plot.
        
    Returns:
        fig: The box plot.
    """
    fig, ax = plt.subplots()
    data_frame["PM1.0"] = pd.to_numeric(data_frame["PM1.0"])
    ax = data_frame.boxplot(column=["PM1.0"], return_type="axes", vert=False)
    ax.set_title(data_frame.get_name() + " Box Plot")
    ax.set_xlabel("PM1.0")
    return fig


@numeric_decorator_specific
def bar_plot(data_frame, x):
    """Create a bar plot from a dataframe.

    Args:
        data_frame (pd.DataFrame): The dataframe to be used.
        x (str): The x axis of the bar plot.   

    Returns:
        fig: The bar plot.
    """
    fig, ax = plt.subplots()
    ax.hist(data_frame[x], bins=12, edgecolor="black", linewidth=0.5)
    ax.set_title(data_frame.get_name() + " Histogram")
    ax.set_xlabel(x)
    ax.set_ylabel("Frequency")
    return fig


@numeric_decorator_double
def avg_differences(first_data_frame, second_data_frame):
    """Calculate the average difference between two dataframes.

    Args:
        first_data_frame (pd.DataFrame): The first dataframe to be used.
        second_data_frame (pd.DataFrame): The second dataframe to be used.
    Returns:
        tuple: The average difference between the two dataframes. Along with each of their means.
    """
    first_mean = first_data_frame.mean()
    second_mean = second_data_frame.mean()
    return_value = larger_smaller_decorator(lambda x, y: x - y)
    return first_mean, second_mean, return_value(first_mean, second_mean)


@numeric_decorator_single
def split_three_point_time(data):
    """Split a dataframe into three points and find the largest standard deviation.

    Args:
        data (pd.DataFrame): The dataframe to be used.

    Returns:
        tuple: The largest standard deviation and the index of the three points. Along with the index.
    """
    index = len(data.index)
    largest_std = 0
    largest_std_index = [0, 0, 0]
    for i in range(0, index, 1):
        three_point_df = data.iloc[i : i + 3]
        three_point_std = three_point_df.std(skipna=True)
        if three_point_std > largest_std:
            largest_std = three_point_std
            largest_std_index = [i, i + 1, i + 2]
    return largest_std, largest_std_index

# Method to read data from a csv file and return two dataframes.
def read_data():
    main_data_frame = pd.read_csv("WM164 Assignment Data Option 1.csv")
    data_data_frame = main_data_frame.iloc[8:, :]
    data_data_frame.columns = ["Date", "Time", "PM1.0", "Date", "Time", "PM1.0"]

    hce_data_frame = Data(data_data_frame.iloc[:, 0:3], name="HCE", location="HCE")
    cnc_data_frame = Data(data_data_frame.iloc[:, 3:6], name="CNC", location="CNC")
    return hce_data_frame, cnc_data_frame
