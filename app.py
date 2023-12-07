import pandas as pd
import math
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats
import kaleido
import time

# Function that takes a dataframe, x and y axis, title, mode, and file
# name and creates a scatter plot image.


def scatter_plot_to_image(data_frame, x, y, title, mode, file_name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_frame[x], y=data_frame[y], mode=mode))
    fig.update_layout(autotypenumbers='convert types',
                      title=title, title_x=0.5)
    fig.write_image(file_name + ".png")

# Function that takes two dataframes and returns the average difference
# between individual values in the two dataframes.


def avg_differences(first_data_frame, second_data_frame):
    first_data_frame = first_data_frame[first_data_frame.columns[2]].astype(float)
    second_data_frame = second_data_frame[second_data_frame.columns[2]].astype(float)
    first_data_frame = first_data_frame.to_numpy()
    second_data_frame = second_data_frame.to_numpy()
    differences = []
    for i in range(0, len(first_data_frame), 1):
        if math.isnan(first_data_frame[i]):
            differences.append(second_data_frame[i] if not (
                math.isnan(second_data_frame[i])) else 0)
        elif math.isnan(second_data_frame[i]):
            differences.append(first_data_frame[i] if not (
                math.isnan(first_data_frame[i])) else 0)
        else:
            if float(first_data_frame[i]) > float(second_data_frame[i]):
                differences.append(
                    float(first_data_frame[i]) - float(second_data_frame[i]))
            else:
                differences.append(
                    float(second_data_frame[i]) - float(first_data_frame[i]))
    return np.mean(differences)

# Main Function


def main():
    t1 = time.time()
    main_data_frame = pd.read_csv('DTS WM164.csv')
    data_data_frame = main_data_frame.iloc[10:, :]
    data_data_frame.columns = ['Date', 'Time', 'PM1.0', 'Date', 'Time', 'PM1.0']
    hce_data_frame = data_data_frame.iloc[:, 0:3]
    cnc_data_frame = data_data_frame.iloc[:, 3:6]
    scatter_plot_to_image(hce_data_frame, 'Time', 'PM1.0',
                       'HCE PM1.0', 'markers', 'HCE PM1.0')
    print(avg_differences(hce_data_frame, cnc_data_frame))
    tf = time.time() - t1
    print(tf)


if __name__ == '__main__':
    main()
