


import pandas as pd
from statistics import median
import numpy as np
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle
import pandas as pd

final_merge_df = pd.read_csv(r'final_merge_df_latitude.csv')
lat11=np.arange(0,90.25,0.25).tolist()
print(final_merge_df)

migration = [[[[] for after in range(9)] for init in range(9)] for r in range(4)]
mig_onerange_down = [[[] for after in range(9)] for r in range(4)]

g = final_merge_df.groupby(['family'])
m = pd.DataFrame({})
m['defined_year'] = np.arange(1970,2021,1)

for k, single in g:
    lat = np.array([0.0 for c in range(5)])  
    single = pd.merge(single, m, on=['defined_year'],how='outer')
    single.sort_values(by=['defined_year'],inplace=True)
    single['median'].interpolate(method='linear',order=1,inplace=True)

    for i in range(5):
        sub = single[single['defined_year'] >= 1970 + 10 * i]
        if i < 4:
            sub = sub[sub['defined_year'] < 1980 + 10 * i]
        if len(sub) == 0:
            lat[i] = np.nan
        else:
            lat[i] = sub['median'].median()

            if lat[i] >= 90 or lat[i] <= 0:
                lat[i] = np.nan

    l = pd.DataFrame({})
    l['lat'] = lat
    l.fillna(method='ffill', inplace=True)
    lat = l['lat'].values.tolist()
    for c in range(4):
        if not np.isnan(lat[c]):
            if int(lat[c] / 10) == int(lat[c + 1] / 10) and lat[c] > lat[c + 1]:
                mig_onerange_down[c][int(lat[c] / 10)].append(k)
            else:
                migration[c][int(lat[c]/10)][int(lat[c + 1]/10)].append(k)

# data
label = ["0°N~10°N", "10°N~20°N", "20°N~30°N", "30°N~40°N", "40°N~50°N", "50°N~60°N", "60°N~70°N", "70°N~80°N", "80°N~90°N","0°N~10°N", "10°N~20°N", "20°N~30°N", "30°N~40°N", "40°N~50°N", "50°N~60°N", "60°N~70°N", "70°N~80°N", "80°N~90°N","0°N~10°N", "10°N~20°N", "20°N~30°N", "30°N~40°N", "40°N~50°N", "50°N~60°N", "60°N~70°N", "70°N~80°N", "80°N~90°N","0°N~10°N", "10°N~20°N", "20°N~30°N", "30°N~40°N", "40°N~50°N", "50°N~60°N", "60°N~70°N", "70°N~80°N", "80°N~90°N","0°N~10°N", "10°N~20°N", "20°N~30°N", "30°N~40°N", "40°N~50°N", "50°N~60°N", "60°N~70°N", "70°N~80°N", "80°N~90°N"]
source = []
target = []
value = []
lcolor = []
for r in range(4):
    for i in range(9):
        source += [i + 9 * r for c in range(9)]
        target += list(np.arange(9 + 9 * r,18 + 9 * r,1))
        for j in range(9):
            value.append(len(migration[r][i][j]))
            if i <= j:
                #lcolor.append('rgba(255,151,79,{})'.format(0.5+0.1*r))
                lcolor.append('rgba(52,152,219,{})'.format(0.5+0.1*r))
            else:
                #lcolor.append('rgba(52,152,219,{})'.format(0.5+0.1*r))
                lcolor.append('rgba(255,151,79,{})'.format(0.5+0.1*r))
        source.append(i + 9 * r)
        target.append(9 + i + 9 * r)
        value.append(len(mig_onerange_down[r][i]))
        #lcolor.append('rgba(52,152,219,{})'.format(0.5+0.1*r))
        lcolor.append('rgba(255,151,79,{})'.format(0.5+0.1*r))

x = [0.01 for i in range(7)]
y = [1,0.88,0.76,0.64,0.52,0.35,0.18]
color = ['rgba(238,103,76,0.5)' for i in range(9)]

x += [0.15 for i in range(7)]
y += [0.88,0.76,0.64,0.52,0.35,0.18,0.09]
color += ['rgba(238,103,76,0.6)' for i in range(9)]

x += [0.30 for i in range(6)]
y += [0.88,0.76,0.64,0.52,0.35,0.18]
color += ['rgba(238,103,76,0.7)' for i in range(9)]

x += [0.45 for i in range(9)]
y += [1,0.88,0.76,0.64,0.52,0.35,0.18,0.09,0.001]
color += ['rgba(238,103,76,0.8)' for i in range(9)]

x += [0.60 for i in range(9)]
y += [1,0.88,0.76,0.64,0.52,0.35,0.18,0.09,0.001]
color += ['rgba(238,103,76,0.9)' for i in range(9)]

link = dict(source = source, target = target, value = value)
node = dict(label = label, pad=50, thickness=20)



fig = make_subplots(rows=1, cols=1)

fig.add_trace(go.Scatter(x=[1, 2, 3], y=[5, 10, 15]), row=1, col=1)

data = go.Sankey(link = link, node=node)# plot
fig = go.Figure(data)

fig.update_traces(node_x=x, selector=dict(type='sankey'))
fig.update_traces(node_y=y, selector=dict(type='sankey'))
fig.update_traces(node_color=color, selector=dict(type='sankey'))
fig.update_traces(link_color=lcolor, selector=dict(type='sankey'))
fig.update_traces(textfont_size=15, selector=dict(type='sankey'))
fig.update_traces(node_line_width=2, selector=dict(type='sankey'))
fig.update_traces(node_line_color='rgba(238,103,76,1)', selector=dict(type='sankey'))


fig.update_layout(
    annotations=[
        dict(
            x=0.95, y=-0.1,
            text='',
            showarrow=True, arrowhead=4, arrowwidth=12, arrowsize=0.7,
            axref='x domain', ax=-1200,
            ayref='y domain', ay=0,
            font={'size': 16, 'color': '#ffffff', 'family': 'Courier New, monospace'},
        ),
        dict(
            x=0.1, y=-0.1,
            text='1970s',
            showarrow=True, arrowhead=4, arrowwidth=12, arrowsize=0.7,
            axref='x domain', ax=-0,
            ayref='y domain', ay=0,
            font={'size': 16, 'color': '#ffffff', 'family': 'Courier New, monospace'},
            bgcolor='rgba(184,112,112,0.5)', borderpad=4, bordercolor='#c7c7c7', borderwidth=2,
            standoff=5, 
        ),
        dict(
            x=0.3, y=-0.1,
            text='1980s',
            showarrow=True, arrowhead=4, arrowwidth=12, arrowsize=0.7,
            axref='x domain', ax=-0,
            ayref='y domain', ay=0,
            font={'size': 16, 'color': '#ffffff', 'family': 'Courier New, monospace'},
            bgcolor='rgba(184,112,112,0.6)', borderpad=4, bordercolor='#c7c7c7', borderwidth=2,
            standoff=5, 
        ),
        dict(
            x=0.5, y=-0.1,
            text='1990s',
            showarrow=True, arrowhead=4, arrowwidth=12, arrowsize=0.7,
            axref='x domain', ax=-0,
            ayref='y domain', ay=0,
            font={'size': 16, 'color': '#ffffff', 'family': 'Courier New, monospace'},
            bgcolor='rgba(184,112,112,0.7)', borderpad=4, bordercolor='#c7c7c7', borderwidth=2,
            standoff=5, 
        ),
        dict(
            x=0.7, y=-0.1,
            text='2000s',
            showarrow=True, arrowhead=4, arrowwidth=12, arrowsize=0.7,
            axref='x domain', ax=-0,
            ayref='y domain', ay=0,
            font={'size': 16, 'color': '#ffffff', 'family': 'Courier New, monospace'},
            bgcolor='rgba(184,112,112,0.8)', borderpad=4, bordercolor='#c7c7c7', borderwidth=2,
            standoff=5, 
        ),
        dict(
            x=0.9, y=-0.1,
            text='2010s',
            showarrow=True, arrowhead=4, arrowwidth=12, arrowsize=0.7,
            axref='x domain', ax=-0,
            ayref='y domain', ay=0,
            font={'size': 16, 'color': '#ffffff', 'family': 'Courier New, monospace'},
            bgcolor='rgba(184,112,112,0.9)', borderpad=4, bordercolor='#c7c7c7', borderwidth=2,
            standoff=5, 
        )
    ]
)

                  
fig.show()

