
# plotly visualize
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np

tsne = TSNE(n_components = 3, learning_rate = 150, n_iter = 1000000000)
X_tsne = tsne.fit_transform(visual)

trace2 = go.Scatter3d(x = X_tsne[:countn*-1 - 1,0], y = X_tsne[:countn*-1 - 1,1], z = X_tsne[:countn*-1 - 1,2], text = lab[:countn*-1 - 1], textfont = {"size" : 10, "color": "#b3de69"}, mode = 'markers+text', marker = dict(size = 2, opacity = 0.8))
trace0 = go.Scatter3d(x = X_tsne[-1,0], y = X_tsne[-1,1], z = X_tsne[-1,2], text = lab[-1], textfont = {"size" : 15, "color": "#bc80bd"}, mode = 'markers+text', marker = dict(size = 5, opacity = 0.9, color = 'rgba(255,0,0'))
trace1 = go.Scatter3d(x = X_tsne[countn*-1 - 1:-1,0], y = X_tsne[countn*-1 - 1:-1,1], z = X_tsne[countn*-1 - 1:-1,2], text = lab[countn*-1 - 1:-1], textfont = {"size" : 12, "color": "#bc80bd"}, mode = 'markers+text', marker = dict(size = 3, opacity = 0.9, color = 'rgba(0,255,0'))

data = [trace0, trace1, trace2]
layout = go.Layout(margin = dict(l=0,r=0,b=0,t=0), scene = dict(xaxis = dict(dtick = 20), yaxis = dict(dtick = 20), zaxis = dict(dtick = 20)))
fig = go.Figure(data= data, layout = layout)
py.iplot(fig, filename = 'nlptest_FB_Unique_etc')
# nlptest_FB_Unique saved.
