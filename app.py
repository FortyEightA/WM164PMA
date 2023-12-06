import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats
import kaleido

#Function that takes a dataframe, x and y axis, title, mode, and file name and creates a scatter plot image.
def scatterPlotToImage(dataFrame, x, y, title, mode, fileName):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataFrame[x], y=dataFrame[y], mode = mode))
    fig.update_layout(autotypenumbers='convert types', title=title, title_x = 0.5)
    fig.write_image(fileName + ".png")
    
def avgDifferences(firstDataFrame, secondDataFrame):
    firstDataFrame = firstDataFrame[firstDataFrame.columns[2]]
    secondDataFrame = secondDataFrame[secondDataFrame.columns[2]]
    firstDataFrame = firstDataFrame.to_numpy()
    secondDataFrame = secondDataFrame.to_numpy()
    differences = []
    for i in range(1, len(firstDataFrame), 1):
        if firstDataFrame[i] == 'nan':
            differences.append(secondDataFrame[i] if secondDataFrame[i] != 'nan' else 0)
        elif secondDataFrame[i] == 'nan':
            differences.append(firstDataFrame[i] if firstDataFrame[i] != 'nan' else 0)
        else:
            differences.append()
    # for i in range(1, 300, 1):
    #     if firstDataFrame[i] == 'NaN' or secondDataFrame[i] == 'NaN':
    #         return np.mean(differences)
    #     else:
    #         differences.append(int(firstDataFrame[i]) - int(secondDataFrame[i]))
    # return np.mean(differences)

#Main Function
def main():
    mainDataFrame = pd.read_csv('DTS WM164.csv')
    dataDataFrame = mainDataFrame.iloc[10:,:]
    dataDataFrame.columns=['Date', 'Time', 'PM1.0', 'Date', 'Time', 'PM1.0']
    hceDataFrame = dataDataFrame.iloc[:,0:3]
    cncDataFrame = dataDataFrame.iloc[:,3:6]
    scatterPlotToImage(hceDataFrame, 'Time', 'PM1.0', 'HCE PM1.0', 'markers', 'HCE PM1.0')
    avgDifferences(hceDataFrame, cncDataFrame)

if __name__ == '__main__':
    main()
