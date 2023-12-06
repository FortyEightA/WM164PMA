import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats
import kaleido

def scatterPlotToImage(dataFrame, x, y, title, mode, fileName):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataFrame[x], y=dataFrame[y], mode = mode))
    fig.update_layout(autotypenumbers='convert types', title=title, title_x = 0.5)
    fig.write_image(fileName + ".png")
    

def main():
    mainDataFrame = pd.read_csv('DTS WM164.csv')
    dataDataFrame = mainDataFrame.iloc[10:,:]
    dataDataFrame.columns=['Date', 'Time', 'PM1.0', 'Date', 'Time', 'PM1.0']
    hceDataFrame = dataDataFrame.iloc[:,0:3]
    scatterPlotToImage(hceDataFrame, 'Time', 'PM1.0', 'HCE PM1.0', 'markers', 'HCE PM1.0')

if __name__ == '__main__':
    main()
