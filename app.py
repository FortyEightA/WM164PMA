import pandas as pd
import math
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats
import kaleido
import time

#Function that takes a dataframe, x and y axis, title, mode, and file name and creates a scatter plot image.
def scatterPlotToImage(dataFrame, x, y, title, mode, fileName):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataFrame[x], y=dataFrame[y], mode = mode))
    fig.update_layout(autotypenumbers='convert types', title=title, title_x = 0.5)
    fig.write_image(fileName + ".png")
    
#Function that takes two dataframes and returns the average difference between individual values in the two dataframes.
def avgDifferences(firstDataFrame, secondDataFrame):
    firstDataFrame = firstDataFrame[firstDataFrame.columns[2]].astype(float)
    secondDataFrame = secondDataFrame[secondDataFrame.columns[2]].astype(float)
    firstDataFrame = firstDataFrame.to_numpy()
    secondDataFrame = secondDataFrame.to_numpy()
    differences = []
    for i in range(1, len(firstDataFrame), 1):
        if math.isnan(firstDataFrame[i]):
            differences.append(secondDataFrame[i] if not(math.isnan(secondDataFrame[i])) else 0)
        elif math.isnan(secondDataFrame[i]):
            differences.append(firstDataFrame[i] if not(math.isnan(firstDataFrame[i])) else 0)
        else:
            if float(firstDataFrame[i]) > float(secondDataFrame[i]):
                differences.append(float(firstDataFrame[i])- float(secondDataFrame[i]))
            else:
                differences.append(float(secondDataFrame[i]) - float(firstDataFrame[i]))
    return np.mean(differences)

#Main Function
def main():
    t1 = time.time()
    mainDataFrame = pd.read_csv('DTS WM164.csv')
    dataDataFrame = mainDataFrame.iloc[10:,:]
    dataDataFrame.columns=['Date', 'Time', 'PM1.0', 'Date', 'Time', 'PM1.0']
    hceDataFrame = dataDataFrame.iloc[:,0:3]
    cncDataFrame = dataDataFrame.iloc[:,3:6]
    scatterPlotToImage(hceDataFrame, 'Time', 'PM1.0', 'HCE PM1.0', 'markers', 'HCE PM1.0')
    print(avgDifferences(hceDataFrame, cncDataFrame))
    tf = time.time() - t1 
    print(tf)

if __name__ == '__main__':
    main()
