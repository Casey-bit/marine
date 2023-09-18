import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

font1 = {
        'weight': 'bold',
        'style':'normal',
        'size': 15,
        }

def set_axis(ax):
    ax.grid(False)
    ax.spines['top'].set_linewidth('2.0')
    ax.spines['bottom'].set_linewidth('2.0')
    ax.spines['left'].set_linewidth('2.0')
    ax.spines['right'].set_linewidth('2.0')
    ax.spines['top'].set_color('black')
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('black')
    for tickline in ax.xaxis.get_ticklines():
        tickline.set_visible(True)
    for tickline in ax.yaxis.get_ticklines():
        tickline.set_visible(True)
    ax.tick_params(which="major",
                    length=15,width = 2.0,
                    colors = "black",
                    direction = 'in',
                    tick2On = False)

axes = [plt.subplot(2,3,i) for i in range(1, 7)]

data = pd.read_csv(r'by_family\method_2\new230729\northern.csv',index_col=(0))

data_merge = pd.read_csv(r'by_family\method_2\new230729\final_merge_df.csv',index_col=(0))
data_merge = data_merge[['family', 'count']].drop_duplicates()
data_merge = data_merge.sort_values(by=['count'], ascending=False).reset_index()
family_count = data_merge[['family', 'count']]

data = pd.merge(data, family_count, on=['family'] )

plotdata = [data['decimallatitude']]
for i in range(5):
    subdata = data[data['year'] >= 1970 + 10 * i]
    subdata = subdata[subdata['year'] < 1980 + 10 * i]
    plotdata.append(subdata['decimallatitude'])


no = 1
label = ['A Total', 'B 1970s', 'C 1980s', 'D 1990s', 'E 2000s', 'F 2010s']
for ax in axes:
    print(no)
    ax.text(0.005, 83, label[no - 1], font1)

    sns.kdeplot(plotdata[no - 1], shade=True, color='r', vertical=True, ax=ax)

    ax.set_xlim([0,0.15])
    ax.set_ylim([0,90])
    ax.set_xticks([0.02 * i for i in range(8)])
    if no >= 4:
        ax.set_xticklabels([0.02 * i for i in range(8)], font1)
        ax.set_xlabel('Records Density',font1)
    else:
        ax.set_xticklabels([])
        ax.set_xlabel('')
    ax.set_yticks([10 * i for i in range(10)])
    if no == 1 or no == 4:
        ax.set_yticklabels([10 * i for i in range(10)], font1)
        ax.set_ylabel('Latitude (°N)',font1)
    else:
        ax.set_yticklabels([])
        ax.set_ylabel('')
    set_axis(ax)
    no += 1

plt.subplots_adjust(wspace=0.1,hspace=0.15)
fig = plt.gcf()
fig.set_size_inches(18, 10)
fig.savefig(r'by_family\method_2\new230729\count.jpg',dpi=150)