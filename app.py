import pandas as pd
import math
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats
import kaleido
import time

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

# Decorator to change nan values to 0.


def nan_to_zero_decorator(func):
    def wrapper(x, y):
        if math.isnan(x):
            return func(0, y) if not (math.isnan(y)) else func(0, 0)
        elif math.isnan(y):
            return func(x, 0) if not (math.isnan(x)) else func(0, 0)
        else:
            return func(x, y)
    return wrapper

# Decorator to arrange values so that x is always larger than y.


def larger_smaller_decorator(func):
    def wrapper(x, y):
        if x > y:
            return func(x, y)
        else:
            return func(y, x)
    return wrapper

# Function that takes two dataframes and returns the average difference
# between individual values in the two dataframes.


def avg_differences(first_data_frame, second_data_frame):
    first_data_frame = first_data_frame[first_data_frame.columns[2]].astype(float)
    second_data_frame = second_data_frame[second_data_frame.columns[2]].astype(float)
    jointArr = pd.concat([first_data_frame, second_data_frame], axis=1).to_numpy()
    diff_return = nan_to_zero_decorator(larger_smaller_decorator(lambda x, y: x - y))
    differences = [diff_return(x, y) for x, y in jointArr]
    return np.mean(differences)

#######################################################################
#                           Main Function                             #
#######################################################################

# Main Function


def main():
    t1 = time.time()
    main_data_frame = pd.read_csv('DTS WM164.csv')
    data_data_frame = main_data_frame.iloc[10:, :]
    data_data_frame.columns = ['Date', 'Time', 'PM1.0', 'Date', 'Time', 'PM1.0']
    hce_data_frame = data_data_frame.iloc[:, 0:3]
    cnc_data_frame = data_data_frame.iloc[:, 3:6]
    scatter_plot_to_image(
        hce_data_frame,
        'Time',
        'PM1.0',
        'HCE PM1.0',
        'markers',
        'HCE PM1.0')
    print(avg_differences(hce_data_frame, cnc_data_frame))
    tf = time.time() - t1
    print(tf)


if __name__ == '__main__':
    main()
