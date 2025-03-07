
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols
from collections import Counter #引入Counter
import pickle
from functools import reduce
import seaborn as sns
import scipy
import operator

'''
1. extract Northern Hemisphere
'''
total_occurrence = pd.read_csv('data_Occurrence5.csv')
northern = total_occurrence[total_occurrence['decimallatitude'] > 0]


'''
2.1970-2020
'''
northern['year'] = northern['eventdate'].astype(str).str.slice(0,4)
northern.drop(columns=['eventdate'], inplace=True)
northern = northern[northern['year'].astype(int) >= 1970]
northern = northern[northern['year'].astype(int) <= 2020]

northern = northern[northern['bathymetry'] >= 0].reset_index().drop(columns=['index'])

'''
3.count by family
'''
northern['count_by_family'] = northern.groupby(['family'])['decimallatitude'].transform('count')
northern.drop(columns=['Unnamed: 0', 'basisofrecord'], inplace=True)
northern.dropna(subset=['count_by_family'], inplace=True)
northern = northern.sort_values(by=['count_by_family'], ascending=False).reset_index().drop(columns=['index'])

'''
count by year
'''
northern['count_by_year'] = northern.groupby(['family','year'])['decimallatitude'].transform('count')

'''
exclude families with records less than 100 
'''
northern = northern[northern['count_by_family'].astype(int) >= 100].reset_index().drop(columns=['index'])

'''
judge belonging range
'''
northern['year'] = northern['year'].astype(int)
for i in range(3):
    northern['range' + str(i + 1)] = pd.cut(northern['decimallatitude'], [30 * i, 30 + 30 * i], labels=['({},{}]'.format(30 * i, 30 * i + 30)])
    c = northern.groupby(['family'])['range' + str(i + 1)].count().reset_index().rename(columns={'range' + str(i + 1): 'range{}_count'.format(i + 1)})
    northern = pd.merge(northern, c, on=['family'])
    # northern['range{}_count'.format(i + 1)] = northern.groupby(['family'])['range' + str(i + 1)].transform('count')
    northern.drop(columns=['range' + str(i + 1)], inplace=True)
    northern.fillna(value={'range{}_count'.format(i + 1): 0}, inplace=True)


family_belonging_df = northern.groupby(['family','year','count_by_year','range1_count','range2_count','range3_count'])['decimallatitude'].count().reset_index().drop(columns=['decimallatitude'])

family_belonging_df['belonging'] = family_belonging_df[['range1_count','range2_count','range3_count']].idxmax(axis=1)
family_belonging_df['belonging'] = family_belonging_df['belonging'].astype(str).str.slice(5,6).astype(int)

'''
get yearly median
'''
family_year_median_df = northern.groupby(['family', 'year'])['decimallatitude'].median().reset_index().rename(columns={"decimallatitude": "median"})
merge_df = pd.merge(family_belonging_df, family_year_median_df, left_on=['family','year'], right_on=['family','year'])

g = merge_df.groupby(['family'])
merge_df_processed = pd.DataFrame({})
for k, single_family in g:

    single_family_df = pd.DataFrame(single_family)

    '''
    judge belonging year = ceil[(pre + next) / 2]
    '''
    single_family_df['year'] = single_family_df['year'].astype(int)
    single_family_df['year_shift'] = single_family_df['year'].shift(1)
    single_family_df['defined_year'] = np.ceil((single_family_df['year'] + single_family_df['year_shift']) / 2)
    # single_family_df['defined_year'] = single_family_df['year']
    single_family_df.drop(columns=['year_shift'], inplace=True)
    single_family_df = single_family_df.loc[:, ['family','year','defined_year','median','count_by_year','range1_count','range2_count','range3_count','belonging']]

    single_family_df = single_family_df.fillna(method='pad', axis=1)
    merge_df_processed = merge_df_processed.append(single_family_df, ignore_index=True)


reserved_family = merge_df_processed['family'].drop_duplicates().reset_index().drop(columns=['index'])
reserved_family['reserved'] = 'True'

northern = pd.merge(northern, reserved_family, left_on='family', right_on='family')

family_count_df = northern.groupby(['family'])['decimallatitude'].count().reset_index().rename(columns={"decimallatitude": "count"})
family_count_df = family_count_df.sort_values(by=['count'], ascending=False).reset_index().drop(columns=['index'])
family_count_df['index'] = family_count_df['count'].rank(ascending=False)

final_merge_df = pd.merge(merge_df_processed, family_count_df, left_on='family', right_on='family')


'''
trophic level
'''
family_level = pd.read_csv(r'function_group_2.csv',usecols=(8,13), encoding='gbk')
family_level.drop_duplicates(subset=['family'],inplace=True)
family_level.dropna(inplace=True)
final_merge_df = pd.merge(final_merge_df, family_level, left_on='family', right_on='family')
family_year_median_df = final_merge_df[['family','level','defined_year','median','count','count_by_year','range1_count','range2_count','range3_count']]
family_year_median_df .to_csv(r'family_year_median_df.csv')
#unique_families = family_year_median_df ['family'].unique()



df = pd.read_csv('family_year_median_df.csv')

for level_value in df['level'].unique():
    level_df = df[df['level'] == level_value]
    level_df.to_csv(f'trophic_level_{level_value}.csv', index=False)
    
    
    
    