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
    
#Decorator to change nan values to 0.
def nanToZeroDecorator(func):
    def wrapper(x,y):
        if math.isnan(x):
            return func(0,y) if not(math.isnan(y)) else func(0,0)
        elif math.isnan(y):
            return func(x,0) if not(math.isnan(x)) else func(0,0)
        else:
            return func(x,y)
    return wrapper

#Decorator to arrange values so that x is always larger than y.
def largerSmallerDecorator(func):
    def wrapper(x,y):
        if x > y:
            return func(x,y)
        else:
            return func(y,x)
    return wrapper

#Function that takes two values and returns the difference between them.
@nanToZeroDecorator
@largerSmallerDecorator
def diffreturn(x,y):
    return x-y
#Function that takes two dataframes and returns the average difference between individual values in the two dataframes.
def avgDifferences(firstDataFrame, secondDataFrame):
    firstDataFrame = firstDataFrame[firstDataFrame.columns[2]].astype(float)
    secondDataFrame = secondDataFrame[secondDataFrame.columns[2]].astype(float)
    jointArr = pd.concat([firstDataFrame, secondDataFrame], axis=1).to_numpy()
    differences = [diffreturn(x,y) for x,y in jointArr]
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
