import os
import sys
import pandas as pd
import scipy
import numpy as np

from dataloading import dataloader


Boroughs = ['Manhattan','Queens','Brooklyn','Bronx','Staten']
df_dict = dataloader(['restaurant','covid','tonnage'])
df_rest = df_dict['restaurant']
df_ton = df_dict['tonnage']
df_covid = df_dict['covid']
new_case_by_month = df_covid[['year','month','New Positives']].groupby(by=['year','month']).sum()

print('Restaurant grade:')
# get restaurant correlation coefficients
for boro in Boroughs:
    df_man = df_rest.loc[df_rest['Borough']==boro]
    target_month = [7,8,9,10,11,12]
    target_year = 2021
    dfs = df_man.groupby(by=['year','month'])
    grades = pd.DataFrame()

    for m in target_month:
        curr_df = dfs.get_group((target_year,m))[['grade','month']]
        curr_df.rename(columns={'month':'m'+str(m)}, inplace = True)
        curr_df = curr_df.groupby('grade').count()
        grades = pd.concat([grades,curr_df],axis=1)

    grades = grades.fillna(0)

    covid_counts = []
    for m in target_month:
        covid_counts.append(new_case_by_month.loc[target_year,m]['New Positives'])

    print('For borough',boro+':')
    coef_mat = np.corrcoef(grades,covid_counts)
    print(coef_mat[:,coef_mat.shape[0]-1])

print('\nTonnage:')
# get tonnage correlation coefficients
df_ton = df_ton.loc[(df_ton['year']>=2021) | (df_ton['year']==2020) & (df_ton['month']>=3)]

for boro in Boroughs:
    df_man = df_ton.loc[df_ton['Borough']==boro]
    dfs = df_man.groupby(by=['year','month']).sum()
    tonnages = pd.DataFrame()
    for ym in dfs.index.unique():
        curr_df = dfs.loc[ym[0],ym[1]][['Refuse','Paper','MGP']]
        tonnages = pd.concat([tonnages,curr_df],axis=1)

    tonnages = tonnages.fillna(0)

    covid_counts = []
    for ym in dfs.index.unique():
        covid_counts.append(new_case_by_month.loc[ym[0],ym[1]]['New Positives'])

    print('For borough',boro+':')
    coef_mat = np.corrcoef(tonnages,covid_counts)
    print(coef_mat[:,coef_mat.shape[0]-1])
